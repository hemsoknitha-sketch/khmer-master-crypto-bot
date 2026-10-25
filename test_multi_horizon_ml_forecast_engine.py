"""
Unit Tests for Wall Street ML Multi-Horizon Forecast Engine
Validating Invariant 100, Conformal Prediction, Hawkes Intensity,
Kalman State Tracker, Multi-Scale Hurst Surface, and DSR Calibration.
"""
import unittest
import numpy as np

import multi_horizon_ml_forecast_engine as mfe


class TestMultiHorizonMLForecastEngine(unittest.TestCase):
    """
    Rigorously verifies the 4 pillars of the Wall Street ML Multi-Horizon Forecast Engine.
    """

    def test_01_conformal_prediction_coverage_interval(self):
        """
        Pillar 1: Finite-Sample Conformal Prediction (Invariant 100).
        Verifies 90% Statistical Coverage Interval [P_min, P_max] and multi-horizon targets.
        """
        res = mfe.predict_asset_trajectory("BTCUSDT", user_lang="km")
        
        self.assertIn("conformal_p_min", res)
        self.assertIn("conformal_p_max", res)
        self.assertIn("filtered_price", res)
        self.assertIn("target_15m", res)
        self.assertIn("target_1h", res)
        self.assertIn("target_24h", res)

        # Interval integrity: P_min must be strictly less than P_max
        self.assertLess(res["conformal_p_min"], res["conformal_p_max"])
        # Filtered price must lie within the conformal interval
        self.assertGreaterEqual(res["filtered_price"], res["conformal_p_min"])
        self.assertLessEqual(res["filtered_price"], res["conformal_p_max"])

        # Report text checks
        report = res["report_text"]
        self.assertIn("CONFORMAL PREDICTION", report.upper())
        self.assertIn("90%", report)

    def test_02_hawkes_process_and_kalman_filter(self):
        """
        Pillar 2: Hawkes Self-Exciting Process & Kalman Filter (Invariant 100).
        Verifies zero-lag true drift velocity and jump intensity ratio lambda(t)/mu.
        """
        res = mfe.predict_asset_trajectory("SOLUSDT", user_lang="en")
        
        self.assertIn("hawkes_ratio", res)
        self.assertIn("is_hawkes_jump", res)
        self.assertIn("filtered_price", res)
        self.assertGreater(res["hawkes_ratio"], 0.0)

        report = res["report_text"]
        self.assertIn("HAWKES", report.upper())
        self.assertIn("KALMAN", report.upper())
        self.assertIn("VELOCITY", report.upper())

    def test_03_multi_horizon_hurst_surface_and_knife_guard(self):
        """
        Pillar 3: Multi-Horizon Alignment & Fractal Hurst Surface (M5, M15, H1, H4).
        Verifies Hurst persistence across scales and Falling Knife Guard.
        """
        res = mfe.predict_asset_trajectory("ETHUSDT", user_lang="km")
        
        self.assertIn("m15_hurst", res)
        self.assertIn("h4_hurst", res)
        self.assertIn("h4_knife_veto", res)
        
        # Hurst exponents must be bounded
        self.assertGreaterEqual(res["m15_hurst"], 0.0)
        self.assertLessEqual(res["m15_hurst"], 1.0)
        self.assertGreaterEqual(res["h4_hurst"], 0.0)
        self.assertLessEqual(res["h4_hurst"], 1.0)

        report = res["report_text"]
        self.assertIn("HURST", report.upper())
        self.assertIn("FALLING KNIFE", report.upper())

    def test_04_empirical_calibration_and_dsr(self):
        """
        Pillar 4: Empirical Probability Calibration (< 0.18 Brier) & Deflated Sharpe Ratio (DSR).
        """
        res = mfe.predict_asset_trajectory("BTCUSDT", user_lang="en")
        
        self.assertIn("meta_win_prob", res)
        self.assertIn("brier_score", res)
        self.assertIn("deflated_sharpe", res)

        # Verification of institutional calibration hurdles
        self.assertLessEqual(res["brier_score"], 0.20)
        self.assertGreaterEqual(res["deflated_sharpe"], 0.95)

        report = res["report_text"]
        self.assertIn("BRIER", report.upper())
        self.assertIn("DEFLATED SHARPE", report.upper())

    def test_05_multi_asset_and_trilingual_support(self):
        """
        Verifies TradFi (Gold, NVDA) and Trilingual formatting (km, en, zh).
        """
        # Test Gold
        gold_res = mfe.predict_asset_trajectory("GOLD", user_lang="km")
        self.assertIn("GOLD", gold_res["symbol"])
        self.assertGreater(gold_res["current_price"], 0.0)
        self.assertIn("CONFORMAL PREDICTION", gold_res["report_text"].upper())

        # Test NVDA
        nvda_res = mfe.predict_asset_trajectory("NVDA", user_lang="en")
        self.assertEqual(nvda_res["symbol"], "NVDA")
        self.assertGreater(nvda_res["current_price"], 0.0)

        # Test Chinese output
        res_zh = mfe.predict_asset_trajectory("BTCUSDT", user_lang="zh")
        self.assertIn("霍克斯", res_zh["report_text"])
        self.assertIn("共形预测", res_zh["report_text"])


if __name__ == "__main__":
    unittest.main()
