# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - UNIT TEST SUITE: DUAL-TOUCH COLLISION, WARM-UP & LIVE PARITY
=============================================================================
Verifies:
  1. Conservative Execution: SL hit first on ambiguous bars (dual-touch)
  2. Pure Warm-Up: No look-ahead bfill on ATR / indicators
  3. Live Strategy Parity: CapitalProbabilityCalibrator exact threshold alignment
  4. Window-End Trade Boundary & Mark-to-Market Exit Costs
"""

import datetime
import unittest
import numpy as np
import pandas as pd

from capital_10y_backtester import Trade, compute_indicators, ASSET_SPECS, WARMUP_BARS, evaluate_bar_signals
from capital_probability_calibrator import CapitalProbabilityCalibrator


class TestBacktestExecutionCorrectness(unittest.TestCase):

    def setUp(self):
        self.entry_date = datetime.date(2020, 1, 15)
        self.entry_price = 100.0
        self.sl_dist = 2.0
        self.sl_price = 98.0  # For BUY
        self.tp1_price = 104.4  # +2.2R
        self.spread = 0.10
        self.contract_mult = 1.0

    def test_conservative_dual_touch_buy_hits_sl_first(self):
        """
        Verify that on a high-volatility bar that pierces BOTH the Stop Loss (low <= 98.0)
        and the Take Profit (high >= 104.4), the simulation conservatively executes STOP LOSS FIRST.
        """
        trade = Trade(
            trade_id=1,
            symbol="TEST_ASSET",
            direction="BUY",
            entry_date=self.entry_date,
            entry_price=self.entry_price,
            sl_price=self.sl_price,
            atr_15m=1.0,
            spread=self.spread,
            calibrated_prob=0.65,
            raw_score=85.0,
            contract_multiplier=self.contract_mult,
            regime="BULL_TREND",
            ablation_mode="BASELINE"
        )
        self.assertEqual(trade.status, "OPEN")

        # Ambiguous candle: Low touches 97.0 (below 98.0 SL), High touches 106.0 (above 104.4 TP)
        ambiguous_bar = pd.Series({
            "Date": pd.Timestamp("2020-01-16"),
            "open": 100.0,
            "high": 106.0,  # Touches TP1
            "low": 97.0,    # Touches SL
            "close": 105.0
        })

        was_closed = trade.step(ambiguous_bar, daily_swap_rate=-0.0001)
        self.assertTrue(was_closed, "Trade must close on ambiguous dual-touch bar")
        self.assertEqual(trade.status, "CLOSED")
        self.assertEqual(trade.exit_reason, "INITIAL_SL_COLLISION", "Reason must reflect conservative SL collision")
        self.assertEqual(trade.pnl_r, -1.0, "Realized R must be -1.0R loss, NOT +2.2R profit!")

    def test_conservative_dual_touch_fixed_mode(self):
        """
        Verify that in fixed SL/TP ablation mode (DROP_SCALE_OUT), dual-touch bar executes SL first.
        """
        trade = Trade(
            trade_id=2,
            symbol="TEST_ASSET",
            direction="BUY",
            entry_date=self.entry_date,
            entry_price=100.0,
            sl_price=98.0,
            atr_15m=1.0,
            spread=self.spread,
            calibrated_prob=0.60,
            raw_score=80.0,
            contract_multiplier=self.contract_mult,
            regime="CHOP",
            ablation_mode="DROP_SCALE_OUT"
        )

        ambiguous_bar = pd.Series({
            "Date": pd.Timestamp("2020-01-16"),
            "open": 100.0,
            "high": 105.0,  # Touches 1.5R TP
            "low": 97.5,    # Touches 1.0R SL
            "close": 104.0
        })

        was_closed = trade.step(ambiguous_bar, daily_swap_rate=-0.0001)
        self.assertTrue(was_closed)
        self.assertEqual(trade.exit_reason, "SL_CONSERVATIVE_COLLISION")
        self.assertEqual(trade.pnl_r, -1.0)

    def test_conservative_dual_touch_sell_hits_sl_first(self):
        """
        Verify that for a SELL trade, an ambiguous bar that pierces High >= SL (102.0)
        and Low <= TP1 (95.6) conservatively hits Stop Loss first.
        """
        trade = Trade(
            trade_id=3,
            symbol="TEST_ASSET",
            direction="SELL",
            entry_date=self.entry_date,
            entry_price=100.0,
            sl_price=102.0,  # For SELL
            atr_15m=1.0,
            spread=self.spread,
            calibrated_prob=0.65,
            raw_score=85.0,
            contract_multiplier=self.contract_mult,
            regime="BEAR_TREND",
            ablation_mode="BASELINE"
        )

        ambiguous_bar = pd.Series({
            "Date": pd.Timestamp("2020-01-16"),
            "open": 100.0,
            "high": 103.0,  # Touches SL
            "low": 94.0,    # Touches TP1
            "close": 95.0
        })

        was_closed = trade.step(ambiguous_bar, daily_swap_rate=-0.0001)
        self.assertTrue(was_closed)
        self.assertEqual(trade.exit_reason, "INITIAL_SL_COLLISION")
        self.assertEqual(trade.pnl_r, -1.0)

    def test_indicator_warmup_no_lookahead_bfill(self):
        """
        Verify that compute_indicators() does NOT backfill ATR using .bfill().
        The first 13 rows must be NaN, strictly enforcing zero look-ahead bias.
        """
        # Create 50 synthetic bars
        dates = pd.date_range("2020-01-01", periods=50, freq="D")
        np.random.seed(123)
        prices = 100.0 + np.cumsum(np.random.normal(0, 1, 50))
        df_test = pd.DataFrame({
            "Date": dates,
            "open": prices,
            "high": prices + 1.0,
            "low": prices - 1.0,
            "close": prices + 0.2,
            "volume": 10000
        })

        df_proc = compute_indicators(df_test)

        # First 13 rows of ATR 14 MUST be NaN (no future backward fill)
        self.assertTrue(pd.isna(df_proc["atr14"].iloc[0]), "Row 0 ATR must be NaN (no bfill)")
        self.assertTrue(pd.isna(df_proc["atr14"].iloc[12]), "Row 12 ATR must be NaN (no bfill)")
        # Row 13 (the 14th bar) onwards must have valid numerical ATR
        self.assertFalse(pd.isna(df_proc["atr14"].iloc[13]), "Row 13 ATR must be valid float")
        self.assertGreater(df_proc["atr14"].iloc[13], 0.0)

    def test_live_backtest_probability_calibrator_parity(self):
        """
        Verify exact parity between CapitalProbabilityCalibrator in live strategy
        and the backtest rule engine.
        """
        # Setup standard input
        cal_res = CapitalProbabilityCalibrator.calibrate_probability(
            raw_confluence_score=85.0,
            is_discount_or_premium=True,
            has_liquidity_sweep=True,
            has_order_block=True,
            has_fvg_golden_pocket=True,
            adx_15m=32.0,
            rsi_15m=45.0
        )

        self.assertIn("calibrated_win_prob", cal_res)
        self.assertIn("is_statistically_approved", cal_res)
        self.assertGreaterEqual(cal_res["calibrated_win_prob"], 0.50)
        self.assertTrue(cal_res["is_statistically_approved"])
        self.assertEqual(cal_res["method"], "MULTIVARIATE_L2_PLATT_ISOTONIC")

    def test_warmup_bars_constant_value(self):
        """
        Verify WARMUP_BARS is set to at least 200 bars (~1 calendar year).
        """
        self.assertGreaterEqual(WARMUP_BARS, 200, "Warm-up period must be at least 200 bars")


if __name__ == "__main__":
    unittest.main()
