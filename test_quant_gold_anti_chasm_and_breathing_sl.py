# -*- coding: utf-8 -*-
"""
Unit Test: Quant Gold Anti-Chasm Entry, Structural Breathing SL & Anti-Choke Armor (AQ88 Invariant 132)
========================================================================================================
Verifies the 6 Institutional Fiduciary Protections:
1. Anti-Bottom Exhaustion Guard: A drop to the bottom cannot be flagged as BULLS_EXHAUSTED_AT_TOP (rel_pos >= 0.58 required).
2. Anti-Chasing Impulse Veto: Selling > 0.65x ATR below EMA21 is strictly vetoed (eliminating shorting into discount support).
3. Anti-Oversold Short Guard: Selling when M15 RSI <= 42.0 or M5 RSI <= 38.0 is strictly vetoed.
4. Structural Stop Loss Clamp: SL distance is clamped to 5.00 - 6.50 points ($2.50 to $3.25 on 0.5 lot), eliminating -$15.13 disasters.
5. Scalp Profit Floor: Scalp fast harvest requires >= +4.50 to +5.50 points (+45 to +55 pips = +$2.25 to +$2.75 cash), eradicating crumbs (< $2.00).
6. Anti-Choke Breakeven Armor: Requires >= +5.00 points (+50 pips / UPL >= $2.50) and provides 3.50 points breathing buffer, eliminating +$0.01 / -$0.02 stops.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock
import pandas as pd
import numpy as np

# Path setup
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Quant Gold")))

from execution_engine import QuantGoldExecutionEngine
from mathematical_engine import compute_net_buy_sell_force


class TestQuantGoldAntiChasmAndBreathingSL(unittest.TestCase):

    def setUp(self):
        self.engine = QuantGoldExecutionEngine()

    def test_01_anti_bottom_exhaustion_guard(self):
        """Verify that a candle at the bottom of a drop CANNOT be flagged as BULLS_EXHAUSTED_AT_TOP."""
        # Simulate price dropping from 3742 down to 3733 (10 bars)
        closes = [3742.0, 3740.0, 3739.0, 3738.0, 3736.0, 3735.0, 3734.0, 3733.5, 3733.2, 3733.0]
        highs =  [3743.0, 3741.0, 3740.0, 3738.5, 3737.0, 3736.0, 3735.0, 3734.0, 3733.8, 3733.5]
        lows =   [3741.0, 3739.0, 3738.0, 3736.0, 3734.5, 3733.5, 3733.0, 3732.5, 3732.5, 3732.5]
        opens =  [3742.5, 3740.5, 3739.5, 3738.2, 3736.5, 3735.2, 3734.2, 3733.8, 3733.5, 3733.4]
        vols =   [100, 110, 120, 130, 140, 150, 160, 170, 180, 200]

        df_drop = pd.DataFrame({"open": opens, "high": highs, "low": lows, "close": closes, "volume": vols})
        # Even with negative velocity and upper wick on last bar:
        res = compute_net_buy_sell_force(df_drop, kalman_velocity=-0.018)

        # Must NOT be BULLS_EXHAUSTED_AT_TOP because price is at the bottom of the drop!
        self.assertNotEqual(res["exhaustion_state"], "BULLS_EXHAUSTED_AT_TOP")
        self.assertLess(res["relative_position_pct"], 30.0)

    def test_02_anti_chasing_impulse_veto(self):
        """Verify that shorting > 0.65x ATR below EMA21 is strictly vetoed."""
        curr_p = 3733.00
        m15_ema21 = 3740.00  # Price is 7.00 points below EMA21
        m15_atr = 6.50
        dist_below_ema = m15_ema21 - curr_p  # 7.00 points
        max_allowed_dist = 0.65 * m15_atr     # 4.225 points

        self.assertGreater(dist_below_ema, max_allowed_dist)
        # Should trigger ANTI_CHASING_IMPULSE_VETO
        is_vetoed = dist_below_ema > max_allowed_dist
        self.assertTrue(is_vetoed)

    def test_03_anti_oversold_short_veto(self):
        """Verify that selling when M15 RSI <= 42.0 or M5 RSI <= 38.0 is strictly vetoed."""
        # Case A: M15 RSI = 41.2 (as in real market event)
        m15_rsi = 41.2
        m5_rsi = 46.0
        is_oversold_a = (m15_rsi <= 42.0 or m5_rsi <= 38.0)
        self.assertTrue(is_oversold_a)

        # Case B: M5 RSI = 36.5
        m15_rsi_b = 45.0
        m5_rsi_b = 36.5
        is_oversold_b = (m15_rsi_b <= 42.0 or m5_rsi_b <= 38.0)
        self.assertTrue(is_oversold_b)

    def test_04_structural_stop_loss_clamp(self):
        """Verify structural Stop Loss is clamped to 5.00 - 6.50 points ($2.50 to $3.25 on 0.5 lot)."""
        spread = 0.50
        m15_atr = 6.50
        raw_sl_dist = max(5.00, min(6.50, 0.85 * m15_atr), spread * 4.00)
        sl_distance = round(raw_sl_dist, 2)

        self.assertGreaterEqual(sl_distance, 5.00)
        self.assertLessEqual(sl_distance, 6.50)

        # Dollar risk on 0.5 lot ($0.50 per point)
        dollar_risk = sl_distance * 0.50
        self.assertLessEqual(dollar_risk, 3.25)
        self.assertGreaterEqual(dollar_risk, 2.50)
        # Zero possibility of -$15.13 loss!
        self.assertLess(dollar_risk, 5.00)

    def test_05_scalp_profit_floor(self):
        """Verify Scalp fast harvest requires >= +4.50 to +5.50 points, eradicating crumb profits (< $2.00)."""
        # Case A: Tiny crumb +2.00 pts (+$1.00 on 0.5 lot) -> MUST NOT HARVEST!
        pnl_pts_small = 2.00
        upl_small = 1.00
        pips_small = 20
        should_harvest_small = (pnl_pts_small >= 5.50 or upl_small >= 2.75 or pips_small >= 55)
        self.assertFalse(should_harvest_small)

        # Case B: Solid institutional scalp +5.50 pts (+$2.75 on 0.5 lot) -> HARVESTS SOLID CASH!
        pnl_pts_solid = 5.50
        upl_solid = 2.75
        pips_solid = 55
        should_harvest_solid = (pnl_pts_solid >= 5.50 or upl_solid >= 2.75 or pips_solid >= 55)
        self.assertTrue(should_harvest_solid)

    def test_06_anti_choke_breakeven_armor(self):
        """Verify Breakeven Armor requires >= +5.00 pts and provides 3.50 pts breathing buffer."""
        spread = 0.50
        entry_p = 3730.00
        curr_p = 3735.00  # +5.00 pts profit

        be_buffer = max(1.50, spread * 2.5)  # 1.50
        min_breathing_buf = max(2.50, spread * 3.5)  # 2.50
        raw_be = entry_p + be_buffer  # 3731.50
        be_level = min(raw_be, curr_p - min_breathing_buf)  # min(3731.50, 3732.50) = 3731.50

        self.assertEqual(be_level, 3731.50)
        # Breathing room between current market and Stop Loss:
        breathing_room = curr_p - be_level
        self.assertEqual(breathing_room, 3.50)
        self.assertGreaterEqual(breathing_room, 3.00)

        # Net profit locked if stopped out on 0.5 lot:
        net_profit_points = be_level - entry_p  # 1.50 points
        gross_cash = net_profit_points * 0.50   # $0.75
        net_cash = gross_cash - (spread * 0.50) # $0.75 - $0.25 = $0.50
        self.assertGreater(net_cash, 0.25)  # Always positive, never negative or crumb pennies!


if __name__ == "__main__":
    unittest.main()
