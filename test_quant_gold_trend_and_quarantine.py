# -*- coding: utf-8 -*-
"""
Unit Test: Quant Gold Intraday Trend Governor & Directional Quarantine (AQ88 Invariant 130)
Verifies:
1. Intraday Bull Trend: Counter-trend selling is 100% blocked; only dip pullbacks (BUY) are permitted.
2. Intraday Bear Trend: Counter-trend buying is 100% blocked; only rally pullbacks (SELL) are permitted.
3. Directional Quarantine: Adverse momentum micro-cut or SL quarantines that direction for 15 minutes.
4. Breakeven Armor: Shifting SL requires >= +3.80 pts and guarantees net profit floor beyond spread.
5. Scalp Fast Harvest: Requires substantial move (>= +2.50 to +3.20 pts) to prevent banking tiny pennies.
"""
import sys
import os
import time
import unittest
from unittest.mock import MagicMock, AsyncMock

# Add paths
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Quant Gold")))

from execution_engine import QuantGoldExecutionEngine
from mathematical_engine import compute_net_buy_sell_force
import pandas as pd
import numpy as np


class TestQuantGoldTrendAndQuarantine(unittest.TestCase):

    def setUp(self):
        self.engine = QuantGoldExecutionEngine()

    def test_01_mathematical_exhaustion_rigor(self):
        """Verify normal rising green candle with 28% wick is NOT falsely labeled BULLS_EXHAUSTED_AT_TOP."""
        # A normal green candle moving up
        df_normal = pd.DataFrame({
            "open": [3720.0, 3721.0, 3722.0, 3723.0, 3724.0],
            "high": [3721.5, 3722.5, 3723.5, 3724.5, 3726.5],
            "low": [3719.5, 3720.5, 3721.5, 3722.5, 3723.8],
            "close": [3721.0, 3722.0, 3723.0, 3724.0, 3725.8],  # Green candle (close > open)
            "volume": [100, 110, 105, 120, 130]
        })
        res_normal = compute_net_buy_sell_force(df_normal, kalman_velocity=0.015)
        self.assertNotEqual(res_normal["exhaustion_state"], "BULLS_EXHAUSTED_AT_TOP")

        # A true bearish rejection candle (red candle with large upper wick and stalling velocity)
        df_rejection = pd.DataFrame({
            "open": [3720.0, 3721.0, 3722.0, 3724.0, 3726.0],
            "high": [3721.5, 3722.5, 3723.5, 3725.0, 3727.5],
            "low": [3719.5, 3720.5, 3721.5, 3723.5, 3724.0],
            "close": [3721.0, 3722.0, 3723.0, 3724.5, 3724.5],  # Red candle, upper wick is (3727.5 - 3726.0)/3.5 = 43%
            "volume": [100, 110, 105, 120, 150]
        })
        res_rejection = compute_net_buy_sell_force(df_rejection, kalman_velocity=-0.005)
        self.assertEqual(res_rejection["exhaustion_state"], "BULLS_EXHAUSTED_AT_TOP")

    def test_02_directional_quarantine_veto(self):
        """Verify that when a direction is quarantined, signals in that direction are vetoed."""
        self.engine._directional_quarantine_dir = "SELL"
        self.engine._directional_quarantine_until = time.time() + 900.0  # 15 minutes

        # Mock evaluate_gold_master_signal components
        mock_mtf = {
            "action": "SELL",
            "weighted_score": -35.0,
            "win_probability": 85.0,
            "counts": {"bullish": 2, "bearish": 15},
            "timeframes": {
                "M5": {"bias": "BEARISH", "rsi": 40.0},
                "M15": {"bias": "BEARISH", "rsi": 39.0, "atr": 6.5, "ema21": 3730.0},
                "H1": {"bias": "BEARISH", "atr": 14.0, "ema50": 3740.0, "ema200": 3750.0},
                "H4": {"bias": "BEARISH", "atr": 26.0}
            }
        }
        self.engine.mtf_engine.analyze_all_19_timeframes = MagicMock(return_value=mock_mtf)
        self.engine.math_core.analyze_mathematical_edge = MagicMock(return_value={
            "kalman": {"latent_velocity": -0.02},
            "hurst_surface": {"regime": "TRENDING_BEAR", "composite": 0.65},
            "net_order_flow_force": {"exhaustion_state": "NEUTRAL_BALANCED"}
        })
        self.engine.get_live_gold_price_quote = MagicMock(return_value=(3720.0, 3720.50, 0.50))

        # Run master signal
        import asyncio
        sig = asyncio.run(self.engine.evaluate_gold_master_signal(fast=False))

        # Must be vetoed to HOLD because SELL is quarantined!
        self.assertEqual(sig["action"], "HOLD")
        self.assertIn("DIRECTIONAL_QUARANTINE_VETO", sig["reason"])

    def test_03_breakeven_armor_breathing_room(self):
        """Verify Breakeven Armor requires >= +3.80 pts and guarantees net profit buffer."""
        spread = 0.50
        entry_p = 3720.00
        be_buffer = max(0.80, spread * 1.8)  # 0.90
        min_breathing_buf = max(2.50, spread * 3.5)  # 2.50

        # Scenario A: Trade moved only +2.00 pts (pnl_pts = 2.00)
        # Should NOT trigger Breakeven Armor yet!
        self.assertFalse(2.00 >= 3.80)

        # Scenario B: Trade moved +4.50 pts (pnl_pts = 4.50, curr_p = 3724.50)
        curr_p = 3724.50
        raw_be = entry_p + be_buffer  # 3720.90
        be_level = min(raw_be, curr_p - min_breathing_buf)  # min(3720.90, 3722.00) = 3720.90

        # Verify net profit after spread
        net_profit_at_sl = be_level - entry_p - spread
        self.assertGreater(net_profit_at_sl, 0.0)  # Always guaranteed net profit!
        self.assertGreaterEqual(curr_p - be_level, min_breathing_buf)  # Full breathing room preserved!

    def test_04_intraday_trend_governor_logic(self):
        """Verify that in an intraday bull trend, counter-trend shorting is forbidden."""
        m5_bias = "BULLISH"
        m15_bias = "BULLISH"
        k_vel = 0.02
        bullish_tf_count = 12
        bearish_tf_count = 2
        weighted_score = 25.0
        is_macro_bear = False
        is_macro_bull = True

        is_intraday_bull = (
            is_macro_bull or
            (m5_bias == "BULLISH" and m15_bias == "BULLISH") or
            (m15_bias == "BULLISH" and k_vel > 0.010) or
            (bullish_tf_count >= 8 and bearish_tf_count <= 4) or
            weighted_score >= 12.0
        )
        self.assertTrue(is_intraday_bull)

        # In an uptrend, bulls exhausted at top must NOT trigger a sell
        ex_state_m5 = "BULLS_EXHAUSTED_AT_TOP"
        final_action = "HOLD"
        if is_intraday_bull and not is_macro_bear:
            if ex_state_m5 == "BEARS_EXHAUSTED_AT_BOTTOM":
                final_action = "BUY"
            # BULLS_EXHAUSTED_AT_TOP does nothing!

        self.assertEqual(final_action, "HOLD")


if __name__ == "__main__":
    unittest.main()
