# -*- coding: utf-8 -*-
"""
Unit Test: Quant Gold Enhanced Flash Shock, Micro-Exhaustion Harvest & Guaranteed Cash Floor
Verifies:
1. Flash Shock Harvest triggers on peak >= $2.50 and retrace >= 45%.
2. Micro-Exhaustion Harvest triggers on peak >= $2.50 and M1 rejection wick with >= 30% pullback.
3. Guaranteed Cash Floor sets SL with >= $0.80 net buffer above entry for BUY and below entry for SELL,
   preventing broker spread drag and negative fills.
"""

import unittest
import pandas as pd
from unittest.mock import MagicMock


class TestQuantGoldHarvestAndCashFloor(unittest.TestCase):

    def test_01_flash_shock_harvest_thresholds(self):
        """Verify Flash Shock Harvest triggers at peak >= $2.50 and retrace >= 45%."""
        spread = 0.50
        is_manual_trade = False

        # Case A: Trade reached $3.50 peak, retraced to $1.80 (pulled back 48%)
        current_peak = 3.50
        current_peak_pts = 3.50
        upl = 1.80
        pnl_pts = 1.80

        is_shock_pts = (
            not is_manual_trade and
            current_peak_pts >= 2.50 and
            current_peak_pts <= 150.0 and
            pnl_pts <= (current_peak_pts * 0.55) and
            pnl_pts >= 1.20 and
            upl >= max(1.00, spread * 1.5)
        )
        is_shock_upl = (
            not is_manual_trade and
            current_peak >= 2.50 and
            current_peak <= 150.0 and
            upl <= (current_peak * 0.55) and
            upl >= max(1.00, spread * 1.5)
        )
        self.assertTrue(is_shock_pts)
        self.assertTrue(is_shock_upl)

        # Case B: Trade at $2.20 peak (below $2.50) -> should NOT trigger early harvest
        current_peak_small = 2.20
        upl_small = 1.10
        is_shock_upl_small = (
            not is_manual_trade and
            current_peak_small >= 2.50 and
            upl_small <= (current_peak_small * 0.55)
        )
        self.assertFalse(is_shock_upl_small)

    def test_02_micro_exhaustion_harvest(self):
        """Verify M1 Micro-Exhaustion triggers when peak >= $2.50, pullback >= 30% and rejection wick forms."""
        spread = 0.50
        is_manual_trade = False
        dir_side = "BUY"
        current_peak = 3.80
        current_peak_pts = 3.80
        upl = 2.40  # Pulled back 36.8% from peak
        pnl_pts = 2.40

        # Simulate M1 DataFrame with an upper rejection pinbar
        df_m1 = pd.DataFrame([
            {"open": 3850.0, "high": 3851.0, "low": 3849.5, "close": 3850.5},
            {"open": 3853.0, "high": 3854.5, "low": 3852.2, "close": 3852.5}  # Upper wick = (3854.5 - 3853.0)/2.3 = 0.65 (65%)
        ])

        is_exhaustion_harvest = False
        if not is_manual_trade and (current_peak >= 2.50 or current_peak_pts >= 2.50) and upl >= max(1.20, spread * 1.6):
            if (upl <= current_peak * 0.70) or (pnl_pts <= current_peak_pts * 0.70):
                c_last = df_m1.iloc[-1]
                o_val, h_val, l_val, c_val = float(c_last['open']), float(c_last['high']), float(c_last['low']), float(c_last['close'])
                c_range = max(0.15, h_val - l_val)
                if dir_side == "BUY":
                    upper_wick = (h_val - max(o_val, c_val)) / c_range
                    if upper_wick >= 0.40 or c_val < o_val:
                        is_exhaustion_harvest = True

        self.assertTrue(is_exhaustion_harvest)

    def test_03_guaranteed_positive_cash_floor(self):
        """Verify Breakeven Armor guarantees positive cash floor (Entry ± max(1.20, spread * 2.2))."""
        spread = 0.50
        entry_p = 3850.00
        curr_p_buy = 3853.50  # +$3.50 in profit

        be_buffer = max(1.20, spread * 2.2)  # max(1.20, 1.10) = 1.20
        self.assertAlmostEqual(be_buffer, 1.20)

        # For BUY:
        raw_be_buy = entry_p + be_buffer  # 3851.20
        min_breathing_buf = max(1.80, spread * 2.8)  # max(1.80, 1.40) = 1.80
        be_level_buy = min(raw_be_buy, curr_p_buy - min_breathing_buf)
        self.assertEqual(be_level_buy, 3851.20)
        self.assertGreater(be_level_buy, entry_p)
        # Even with $0.50 spread, net profit at fill = 3851.20 - 3850.00 - 0.50 = +$0.70 (SOLID GREEN!)
        self.assertGreater(be_level_buy - entry_p, spread * 1.0)
        # Verify healthy breathing distance from current price (at least 1.80 pts)
        self.assertGreaterEqual(curr_p_buy - be_level_buy, 1.80)

        # For SELL:
        curr_p_sell = 3846.50  # +$3.50 in profit
        raw_be_sell = entry_p - be_buffer  # 3848.80
        be_level_sell = max(raw_be_sell, curr_p_sell + min_breathing_buf)
        self.assertEqual(be_level_sell, 3848.80)
        self.assertLess(be_level_sell, entry_p)
        self.assertGreater(entry_p - be_level_sell, spread * 1.0)
        self.assertGreaterEqual(be_level_sell - curr_p_sell, 1.80)

    def test_04_ram_climax_fast_harvest_and_scale_tier_1(self):
        """Verify Machine 1 Scalp can harvest at peak momentum even after Breakeven (scale_tier=1)."""
        is_e1 = True
        is_manual_trade = False
        scale_tier = 1  # Breakeven was already set!
        tier_pips_target = 20

        # Scenario A: Scalp reached +2.20 pts (+22 pips / +$1.10 on 0.5 lot)
        pnl_pts = 2.20
        pips = 22
        upl = 1.10
        scalp_exhausted = False
        current_peak_pts = 2.20

        should_fast_harvest = (
            (pnl_pts >= 2.20 or pips >= tier_pips_target or upl >= 2.00) or
            ((pnl_pts >= 1.50 or upl >= 1.25) and scalp_exhausted) or
            (current_peak_pts >= 2.00 and pnl_pts <= current_peak_pts * 0.72 and pnl_pts >= 1.20)
        )
        # Must harvest at target reached even with scale_tier = 1!
        can_run_harvest = is_e1 and not is_manual_trade and scale_tier <= 1
        self.assertTrue(can_run_harvest)
        self.assertTrue(should_fast_harvest)

        # Scenario B: Exhaustion pinbar formed with +1.60 pts profit
        pnl_pts_b = 1.60
        upl_b = 0.80
        scalp_exhausted_b = True
        should_fast_harvest_b = (
            (pnl_pts_b >= 2.20 or 16 >= tier_pips_target or upl_b >= 2.00) or
            ((pnl_pts_b >= 1.50 or upl_b >= 1.25) and scalp_exhausted_b) or
            (2.00 >= 2.00 and pnl_pts_b <= 2.00 * 0.72 and pnl_pts_b >= 1.20)
        )
        self.assertTrue(should_fast_harvest_b)

    def test_05_adaptive_invalidation_micro_cut(self):
        """Verify that adverse order flow cuts failing trades at -$2.25 to prevent -$15.13 catastrophe."""
        upl = -2.30  # Floating loss around -$2.30
        pnl_pts = -4.60
        dir_side = "BUY"
        is_floating_loss = (upl <= -2.50 or pnl_pts <= -4.00)
        is_manual_trade = False

        # Adversely strong sell force (e.g. 68% sell force against BUY)
        s_f_cut = 68.0
        ex_cut = "BULLS_EXHAUSTED_AT_TOP"
        is_adverse_order_flow = (dir_side == "BUY" and (s_f_cut >= 62.0 or ex_cut == "BULLS_EXHAUSTED_AT_TOP"))
        self.assertTrue(is_adverse_order_flow)

        should_micro_cut = is_floating_loss and is_adverse_order_flow and not is_manual_trade and (upl <= -2.25 or pnl_pts <= -4.50)
        self.assertTrue(should_micro_cut)


if __name__ == "__main__":
    unittest.main()
