# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - UNIT TESTS FOR MARCOS LÓPEZ DE PRADO 2-MODEL META-LABELING (AQ84 INVARIANT 85)
=============================================================================================
Author: HEM SINATH | Institutional Quantitative Governance
"""

import os
import unittest
import numpy as np
from capital_meta_labeling_engine import CapitalMetaLabelingEngine, FEATURE_COLUMNS


class TestMetaLabelingEngine(unittest.TestCase):
    """Rigorous verification suite for 2-Model Meta-Labeling architecture."""

    def setUp(self):
        self.sample_features = CapitalMetaLabelingEngine.extract_features(
            direction="BUY",
            raw_score=76.0,
            calib_p=0.68,
            adx14=32.5,
            rsi14=52.0,
            range_pct=42.0,
            atr14=25.0,
            price=2650.0,
            spread=0.35,
            ema20=2640.0,
            ema50=2610.0,
            ema200=2500.0,
            dxy_change=-0.25,
            vix=17.5,
            day_of_week=2
        )

    def test_feature_columns_completeness(self):
        """Feature vector must contain all required 14 features without missing keys."""
        self.assertEqual(len(FEATURE_COLUMNS), 14)
        for col in FEATURE_COLUMNS:
            self.assertIn(col, self.sample_features)
            self.assertFalse(np.isnan(self.sample_features[col]))

    def test_direction_encoding(self):
        """Direction must be encoded as +1.0 for BUY, -1.0 for SELL, 0.0 otherwise."""
        f_buy = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=70.0, calib_p=0.6, adx14=30, rsi14=50,
            range_pct=40, atr14=10, price=1000, spread=0.5, ema20=990, ema50=980, ema200=950
        )
        self.assertEqual(f_buy["direction_num"], 1.0)

        f_sell = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=70.0, calib_p=0.6, adx14=30, rsi14=50,
            range_pct=60, atr14=10, price=1000, spread=0.5, ema20=1010, ema50=1020, ema200=1050
        )
        self.assertEqual(f_sell["direction_num"], -1.0)

    def test_prediction_output_contract(self):
        """Prediction result must adhere strictly to the institutional dictionary schema."""
        res = CapitalMetaLabelingEngine.predict_meta_label(self.sample_features, threshold=0.60)
        self.assertIn("is_approved", res)
        self.assertIn("meta_win_prob", res)
        self.assertIn("threshold", res)
        self.assertIn("sizing_multiplier", res)
        self.assertIn("verdict", res)
        self.assertIn("reason", res)
        self.assertIn("is_ml_inferred", res)
        self.assertTrue(0.0 <= res["meta_win_prob"] <= 1.0)

    def test_threshold_gating(self):
        """If meta_win_prob < threshold, trade must be rejected with sizing multiplier 0.0."""
        # Ultra high threshold forces rejection
        res_rejected = CapitalMetaLabelingEngine.predict_meta_label(self.sample_features, threshold=0.99)
        self.assertFalse(res_rejected["is_approved"])
        self.assertEqual(res_rejected["sizing_multiplier"], 0.0)
        self.assertEqual(res_rejected["verdict"], "META_REJECTED")

        # Low threshold forces approval
        res_approved = CapitalMetaLabelingEngine.predict_meta_label(self.sample_features, threshold=0.20)
        self.assertTrue(res_approved["is_approved"])
        self.assertGreaterEqual(res_approved["sizing_multiplier"], 0.75)
        self.assertEqual(res_approved["verdict"], "META_APPROVED")

    def test_dynamic_bet_sizing_conviction(self):
        """High conviction signals must scale bet sizing up to 1.5x."""
        res_appr = CapitalMetaLabelingEngine.predict_meta_label(self.sample_features, threshold=0.60)
        if res_appr["is_approved"]:
            self.assertGreaterEqual(res_appr["sizing_multiplier"], 1.0)
            self.assertLessEqual(res_appr["sizing_multiplier"], 1.50)

    def test_analytical_fallback_safety(self):
        """Analytical fallback must produce valid probabilities without throwing errors."""
        res = CapitalMetaLabelingEngine.predict_meta_label(
            self.sample_features,
            threshold=0.60,
            model_path="non_existent_model_file.pkl"
        )
        self.assertFalse(res["is_ml_inferred"])
        self.assertTrue(0.0 < res["meta_win_prob"] < 1.0)


if __name__ == "__main__":
    unittest.main()
