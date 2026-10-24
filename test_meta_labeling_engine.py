# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - UNIT TESTS FOR MARCOS LÓPEZ DE PRADO 2-MODEL META-LABELING (AQ84 INVARIANT 85)
=============================================================================================
Author: HEM SINATH | Institutional Quantitative Governance
"""

import os
import unittest
import numpy as np
from capital_meta_labeling_engine import (
    CapitalMetaLabelingEngine,
    FEATURE_COLUMNS,
    InstitutionalMultiModelStackingClassifier
)


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
        self.assertEqual(len(FEATURE_COLUMNS), 32)
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
        res_approved = CapitalMetaLabelingEngine.predict_meta_label(self.sample_features, threshold=0.10)
        self.assertTrue(res_approved["is_approved"])
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

    def test_multi_model_stacking_classifier_fit_predict(self):
        """InstitutionalMultiModelStackingClassifier must fit base models and predict valid probability bounds."""
        import pandas as pd
        X_toy = pd.DataFrame(np.random.randn(40, len(FEATURE_COLUMNS)), columns=FEATURE_COLUMNS)
        y_toy = pd.Series(np.random.randint(0, 2, 40))
        stack = InstitutionalMultiModelStackingClassifier(weights=(0.40, 0.40, 0.20), random_state=42)
        stack.fit(X_toy, y_toy)

        probs = stack.predict_proba(X_toy.iloc[:5])
        self.assertEqual(probs.shape, (5, 2))
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(5), atol=1e-5)
        self.assertTrue(hasattr(stack, "models_"))
        self.assertIn("xgb", stack.models_)
        self.assertIn("lgb", stack.models_)
        self.assertIn("cat", stack.models_)

        details = stack.predict_detailed(X_toy.iloc[:1], threshold=0.55)
        self.assertIn("stacked_prob", details)
        self.assertIn("prob_xgb", details)
        self.assertIn("prob_lgb", details)
        self.assertIn("prob_cat", details)
        self.assertIn("consensus_ratio", details)
        self.assertIn("dispersion", details)
        self.assertTrue(0.0 <= details["consensus_ratio"] <= 1.0)

    def test_multi_model_stacking_loaded_inference(self):
        """Loaded meta-model must provide multi-model consensus and breakdown."""
        res = CapitalMetaLabelingEngine.predict_meta_label(self.sample_features, threshold=0.55)
        self.assertTrue(res["is_ml_inferred"])
        self.assertTrue(res.get("is_stacked_ensemble", False))
        self.assertIn("model_breakdown", res)
        self.assertIn("consensus_ratio", res)
        self.assertIn("model_dispersion", res)
        if res["model_breakdown"] is not None:
            self.assertIn("xgb", res["model_breakdown"])
            self.assertIn("lgb", res["model_breakdown"])
            self.assertIn("cat", res["model_breakdown"])

    def test_smart_money_divergence_governor(self):
        """Smart Money Divergence <= -25% must unconditionally crush BUY win prob to 0.0, and >= +25% must crush SELL."""
        import capital_market_report_engine as cmre

        # Extreme Bearish SMD: Gold -71.0% (Retail 84% Long vs LevFunds 13% Long / 87% Short)
        f_buy_gold = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=85.0, calib_p=0.80, epic="GOLD", price=4023.61,
            smart_money_divergence=-71.0, client_long_pct=84.0, leveraged_funds_long_pct=13.0
        )
        self.assertEqual(f_buy_gold["smart_money_divergence"], -71.0)
        res_buy = CapitalMetaLabelingEngine.predict_meta_label(f_buy_gold, threshold=0.55)
        self.assertEqual(res_buy["meta_win_prob"], 0.0)
        self.assertFalse(res_buy["is_approved"])
        self.assertEqual(res_buy["sizing_multiplier"], 0.0)
        self.assertEqual(res_buy["verdict"], "META_REJECTED")
        self.assertIn("BLOCKED_SMART_MONEY_EXTREME_BEARISH_DIVERGENCE", res_buy["reason"])
        self.assertEqual(res_buy["true_institutional_winner"], "SELL")

        # Bullish SMD >= +25% must crush SELL win prob to 0.0
        f_sell_trap = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=85.0, calib_p=0.80,
            smart_money_divergence=45.0, client_long_pct=25.0, leveraged_funds_long_pct=70.0
        )
        res_sell = CapitalMetaLabelingEngine.predict_meta_label(f_sell_trap, threshold=0.55)
        self.assertEqual(res_sell["meta_win_prob"], 0.0)
        self.assertFalse(res_sell["is_approved"])
        self.assertEqual(res_sell["verdict"], "META_REJECTED")
        self.assertIn("BLOCKED_SMART_MONEY_EXTREME_BULLISH_DIVERGENCE", res_sell["reason"])
        self.assertEqual(res_sell["true_institutional_winner"], "BUY")

        # Strict 25% boundary test: SMD = -26.0% must veto BUY
        f_boundary_buy = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=80.0, calib_p=0.75,
            smart_money_divergence=-26.0, client_long_pct=60.0, leveraged_funds_long_pct=34.0
        )
        res_boundary_buy = CapitalMetaLabelingEngine.predict_meta_label(f_boundary_buy, threshold=0.55)
        self.assertEqual(res_boundary_buy["meta_win_prob"], 0.0)
        self.assertFalse(res_boundary_buy["is_approved"])

        # SmartMoneyDivergenceGovernor direct evaluation on Gold and US500
        smd_gold_buy = cmre.SmartMoneyDivergenceGovernor.evaluate_smd("GOLD", direction="BUY", custom_client_long=84.0, custom_lev_funds_long=13.0)
        self.assertTrue(smd_gold_buy["is_vetoed"])
        self.assertEqual(smd_gold_buy["true_institutional_winner"], "SELL")
        self.assertIn("SMD_INSTITUTIONAL_DIRECTION_VETO", smd_gold_buy["veto_reason"])

        smd_gold_sell = cmre.SmartMoneyDivergenceGovernor.evaluate_smd("GOLD", direction="SELL", custom_client_long=84.0, custom_lev_funds_long=13.0)
        self.assertFalse(smd_gold_sell["is_vetoed"])
        self.assertTrue(smd_gold_sell["is_aligned"])
        self.assertEqual(smd_gold_sell["score_boost"], 30.0)

    def test_conformal_prediction_regime_coupling(self):
        """Conformal Prediction must reject BUY trades in Bear Average and require strict singleton in Volatile Consolidation."""
        import capital_advanced_quant_models as caqm

        # 1. Bear Average must veto BUY trades
        eval_bear_buy = caqm.ConformalPredictionGovernor.evaluate_conformal_approval(
            predicted_prob_win=0.72, alpha=0.10, direction="BUY", daily_regime="Bear Average"
        )
        self.assertFalse(eval_bear_buy["is_conformal_approved"])
        self.assertIn("CONFORMAL_INSTITUTIONAL_REGIME_VETO", eval_bear_buy.get("rejection_reason", ""))
        self.assertIn("BUY trade strictly rejected in 'Bear Average'", eval_bear_buy.get("rejection_reason", ""))

        # 2. Bull Average must veto SELL trades
        eval_bull_sell = caqm.ConformalPredictionGovernor.evaluate_conformal_approval(
            predicted_prob_win=0.72, alpha=0.10, direction="SELL", daily_regime="Bull Average"
        )
        self.assertFalse(eval_bull_sell["is_conformal_approved"])
        self.assertIn("CONFORMAL_INSTITUTIONAL_REGIME_VETO", eval_bull_sell.get("rejection_reason", ""))
        self.assertIn("SELL trade strictly rejected in 'Bull Average'", eval_bull_sell.get("rejection_reason", ""))

        # 3. Consolidation Volatile requires P(Win) >= 70% and 95% coverage
        eval_whipsaw = caqm.ConformalPredictionGovernor.evaluate_conformal_approval(
            predicted_prob_win=0.62, alpha=0.10, direction="BUY", daily_regime="Consolidation - Volatile"
        )
        self.assertFalse(eval_whipsaw["is_conformal_approved"])
        self.assertEqual(eval_whipsaw["coverage_guarantee_pct"], 95.0)

        # 4. Bear Average with SELL (aligned trend) approves high-conviction short
        eval_bear_sell = caqm.ConformalPredictionGovernor.evaluate_conformal_approval(
            predicted_prob_win=0.75, alpha=0.10, direction="SELL", daily_regime="Bear Average"
        )
        self.assertTrue(eval_bear_sell["is_conformal_approved"])

    def test_realtime_deep_regime_transition_detector(self):
        """Deep Learning Real-Time Regime Transition Detector must detect shock dump in <5ms and veto Longs."""
        import capital_advanced_quant_models as caqm

        # 1. Normal sequence
        normal_rets = [0.0001, -0.0002, 0.0003, 0.0001, -0.0001, 0.0002, 0.0000, 0.0001]
        norm_eval = caqm.RealTimeDeepRegimeDetector.evaluate_realtime_regime(
            returns=normal_rets, volume_ratios=[1.0]*8, direction="BUY"
        )
        self.assertFalse(norm_eval["is_shock_regime"])
        self.assertFalse(norm_eval["veto_longs"])
        self.assertLess(norm_eval["panic_liquidation_prob"], 0.20)
        self.assertLess(norm_eval["execution_latency_ms"], 5.0)

        # 2. Panic Liquidation Shock sequence (Wall Street Cash Open shock dump)
        shock_rets = [-0.015, -0.022, -0.018, -0.025, -0.030, -0.028, -0.032, -0.029]
        shock_eval = caqm.RealTimeDeepRegimeDetector.evaluate_realtime_regime(
            returns=shock_rets, volume_ratios=[3.0]*8, direction="BUY"
        )
        self.assertTrue(shock_eval["is_shock_regime"])
        self.assertTrue(shock_eval["veto_longs"])
        self.assertGreaterEqual(shock_eval["panic_liquidation_prob"], 0.50)
        self.assertEqual(shock_eval["dominant_regime"], "PANIC_LIQUIDATION")
        self.assertGreater(shock_eval["autoencoder_recon_error"], 1.50)
        self.assertLess(shock_eval["execution_latency_ms"], 5.0)

    def test_vpin_toxic_order_flow_governor(self):
        """VPIN >= 0.65 must veto opposing trades and approve/boost aligned trades (Invariant 101)."""
        import vpin_order_flow_engine as vpin_eng

        # 1. Bearish toxic flow (VPIN >= 0.65 with BEARISH dominant flow) must veto BUY trades
        f_buy_into_dump = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=85.0, calib_p=0.80,
            vpin=0.72, vpin_toxicity_direction="BEARISH", vpin_is_toxic=True
        )
        self.assertEqual(f_buy_into_dump["vpin"], 0.72)
        self.assertTrue(f_buy_into_dump["vpin_is_toxic"])
        self.assertEqual(f_buy_into_dump["vpin_toxicity_direction"], "BEARISH")

        res_buy_dump = CapitalMetaLabelingEngine.predict_meta_label(f_buy_into_dump, threshold=0.55)
        self.assertEqual(res_buy_dump["meta_win_prob"], 0.0)
        self.assertFalse(res_buy_dump["is_approved"])
        self.assertEqual(res_buy_dump["sizing_multiplier"], 0.0)
        self.assertEqual(res_buy_dump["verdict"], "META_REJECTED")
        self.assertIn("BLOCKED_TOXIC_ORDER_FLOW_VPIN_VETO", res_buy_dump["reason"])
        self.assertTrue(res_buy_dump["vpin_is_toxic"])

        # 2. Bullish toxic flow (VPIN >= 0.65 with BULLISH dominant flow) must veto SELL trades
        f_sell_into_pump = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=85.0, calib_p=0.80,
            vpin=0.68, vpin_toxicity_direction="BULLISH", vpin_is_toxic=True
        )
        res_sell_pump = CapitalMetaLabelingEngine.predict_meta_label(f_sell_into_pump, threshold=0.55)
        self.assertEqual(res_sell_pump["meta_win_prob"], 0.0)
        self.assertFalse(res_sell_pump["is_approved"])
        self.assertEqual(res_sell_pump["verdict"], "META_REJECTED")
        self.assertIn("BLOCKED_TOXIC_ORDER_FLOW_VPIN_VETO", res_sell_pump["reason"])

        # 3. Aligned trades receive boost
        f_buy_aligned = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=80.0, calib_p=0.75,
            vpin=0.70, vpin_toxicity_direction="BULLISH", vpin_is_toxic=True
        )
        f_buy_baseline = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=80.0, calib_p=0.75,
            vpin=0.50, vpin_toxicity_direction="BALANCED", vpin_is_toxic=False
        )
        res_buy_aligned = CapitalMetaLabelingEngine.predict_meta_label(f_buy_aligned, threshold=0.55)
        res_buy_baseline = CapitalMetaLabelingEngine.predict_meta_label(f_buy_baseline, threshold=0.55)
        self.assertGreater(res_buy_aligned["meta_win_prob"], res_buy_baseline["meta_win_prob"])
        self.assertTrue(res_buy_aligned["vpin_is_toxic"])
        self.assertEqual(res_buy_aligned["vpin_toxicity_direction"], "BULLISH")

        # 4. Normal flow (< 0.65) must not veto
        f_normal = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=80.0, calib_p=0.75,
            vpin=0.45, vpin_toxicity_direction="BALANCED", vpin_is_toxic=False
        )
        res_normal = CapitalMetaLabelingEngine.predict_meta_label(f_normal, threshold=0.55)
        self.assertFalse(res_normal["vpin_is_toxic"])

        # 5. Direct gatekeeper evaluation
        from test_vpin_order_flow_engine import _generate_synthetic_vpin_candles
        bull_candles = _generate_synthetic_vpin_candles(n=30, flow_type="BULLISH_TOXIC")
        gate_buy = vpin_eng.evaluate_vpin_toxicity(bull_candles, "BUY")
        self.assertFalse(gate_buy["is_vetoed"])
        self.assertTrue(gate_buy["is_aligned"])
        self.assertEqual(gate_buy["score_boost"], 30.0)
        self.assertEqual(gate_buy["action"], "RIDE_TOXIC_BULLISH_WAVE")

        gate_sell = vpin_eng.evaluate_vpin_toxicity(bull_candles, "SELL")
        self.assertTrue(gate_sell["is_vetoed"])
        self.assertFalse(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], -35.0)
        self.assertIn("VPIN_INSTITUTIONAL_TOXICITY_VETO", gate_sell["veto_reason"])

    def test_order_flow_delta_absorption_governor(self):
        """Order Flow Delta Absorption at R1/S1 must veto opposing trades and boost aligned trades (Invariant 102)."""
        import order_flow_delta_absorption_engine as ofda

        # 1. Bull Exhaustion at R1 (Institutional Limit Sellers absorb Buy Flow):
        # Proposed BUY must be strictly VETOED with 0.0% P(Win)
        f_buy_r1 = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=85.0, calib_p=0.80,
            is_delta_absorption_active=True, delta_absorption_winner="SELL",
            delta_absorption_regime="BEARISH_ABSORPTION_AT_R1"
        )
        self.assertTrue(f_buy_r1["is_delta_absorption_active"])
        self.assertEqual(f_buy_r1["delta_absorption_winner"], "SELL")

        res_buy_r1 = CapitalMetaLabelingEngine.predict_meta_label(f_buy_r1, threshold=0.55)
        self.assertEqual(res_buy_r1["meta_win_prob"], 0.0)
        self.assertFalse(res_buy_r1["is_approved"])
        self.assertEqual(res_buy_r1["sizing_multiplier"], 0.0)
        self.assertEqual(res_buy_r1["verdict"], "META_REJECTED")
        self.assertIn("BLOCKED_ORDER_FLOW_BULL_EXHAUSTION_VETO", res_buy_r1["reason"])

        # 2. Bull Exhaustion at R1:
        # Proposed SELL is aligned with institutional ceiling (boosted)
        f_sell_r1 = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=80.0, calib_p=0.75,
            is_delta_absorption_active=True, delta_absorption_winner="SELL",
            delta_absorption_regime="BEARISH_ABSORPTION_AT_R1"
        )
        f_sell_base = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=80.0, calib_p=0.75,
            is_delta_absorption_active=False, delta_absorption_winner="NEUTRAL"
        )
        res_sell_r1 = CapitalMetaLabelingEngine.predict_meta_label(f_sell_r1, threshold=0.55)
        res_sell_base = CapitalMetaLabelingEngine.predict_meta_label(f_sell_base, threshold=0.55)
        self.assertGreater(res_sell_r1["meta_win_prob"], res_sell_base["meta_win_prob"])
        self.assertTrue(res_sell_r1["is_delta_absorption_active"])
        self.assertEqual(res_sell_r1["delta_absorption_winner"], "SELL")

        # 3. Bear Exhaustion at S1 (Institutional Limit Buyers absorb Sell Flow):
        # Proposed SELL must be strictly VETOED with 0.0% P(Win)
        f_sell_s1 = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=85.0, calib_p=0.80,
            is_delta_absorption_active=True, delta_absorption_winner="BUY",
            delta_absorption_regime="BULLISH_ABSORPTION_AT_S1"
        )
        res_sell_s1 = CapitalMetaLabelingEngine.predict_meta_label(f_sell_s1, threshold=0.55)
        self.assertEqual(res_sell_s1["meta_win_prob"], 0.0)
        self.assertFalse(res_sell_s1["is_approved"])
        self.assertEqual(res_sell_s1["verdict"], "META_REJECTED")
        self.assertIn("BLOCKED_ORDER_FLOW_BEAR_EXHAUSTION_VETO", res_sell_s1["reason"])

        # 4. Direct Gatekeeper Evaluation
        from test_order_flow_delta_absorption_engine import _generate_synthetic_boundary_candles
        r1_candles = _generate_synthetic_boundary_candles(setup_type="BULL_EXHAUSTION_R1")
        gate_sell = ofda.evaluate_boundary_absorption_gatekeeper("GOLD", "SELL", 4046.0, r1_candles, r1=4050.0, s1=3950.0)
        self.assertFalse(gate_sell["is_vetoed"])
        self.assertTrue(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], 35.0)

        gate_buy = ofda.evaluate_boundary_absorption_gatekeeper("GOLD", "BUY", 4046.0, r1_candles, r1=4050.0, s1=3950.0)
        self.assertTrue(gate_buy["is_vetoed"])
        self.assertFalse(gate_buy["is_aligned"])
        self.assertIn("BLOCKED_ORDER_FLOW_BULL_EXHAUSTION_VETO", gate_buy["veto_reason"])

    def test_dealing_range_equilibrium_chop_governor(self):
        """Dealing range equilibrium chop (35%-65%) must strictly veto directional market orders (Invariant 103)."""
        import dealing_range_equilibrium_chop_engine as drec

        # 1. Equilibrium Chop (50% Range): Must be strictly vetoed
        f_chop = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=85.0, calib_p=0.80,
            range_pct=50.0, is_equilibrium_chop=True, equilibrium_zone="EQUILIBRIUM_CHOP_ZONE"
        )
        self.assertTrue(f_chop["is_equilibrium_chop"])
        self.assertEqual(f_chop["equilibrium_zone"], "EQUILIBRIUM_CHOP_ZONE")

        res_chop = CapitalMetaLabelingEngine.predict_meta_label(f_chop, threshold=0.55)
        self.assertEqual(res_chop["meta_win_prob"], 0.0)
        self.assertFalse(res_chop["is_approved"])
        self.assertEqual(res_chop["sizing_multiplier"], 0.0)
        self.assertEqual(res_chop["verdict"], "META_REJECTED")
        self.assertIn("BLOCKED_DEALING_RANGE_EQUILIBRIUM_CHOP_VETO", res_chop["reason"])

        # 2. Discount Boundary (< 35% Range near S1): BUY is awarded boundary edge (+0.10 expansion)
        f_discount_base = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=75.0, calib_p=0.70,
            range_pct=50.0, is_equilibrium_chop=False
        )
        res_discount_base = CapitalMetaLabelingEngine.predict_meta_label(f_discount_base, threshold=0.55)

        f_discount_buy = CapitalMetaLabelingEngine.extract_features(
            direction="BUY", raw_score=75.0, calib_p=0.70,
            range_pct=20.0, is_equilibrium_chop=False, equilibrium_zone="DISCOUNT_BOUNDARY_ZONE"
        )
        res_discount_buy = CapitalMetaLabelingEngine.predict_meta_label(f_discount_buy, threshold=0.55)
        self.assertGreater(res_discount_buy["meta_win_prob"], res_discount_base["meta_win_prob"])
        self.assertEqual(res_discount_buy["equilibrium_zone"], "DISCOUNT_BOUNDARY_ZONE")

        # 3. Premium Boundary (> 65% Range near R1): SELL is awarded boundary edge (+0.10 expansion)
        f_premium_base = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=75.0, calib_p=0.70,
            range_pct=50.0, is_equilibrium_chop=False
        )
        res_premium_base = CapitalMetaLabelingEngine.predict_meta_label(f_premium_base, threshold=0.55)

        f_premium_sell = CapitalMetaLabelingEngine.extract_features(
            direction="SELL", raw_score=75.0, calib_p=0.70,
            range_pct=80.0, is_equilibrium_chop=False, equilibrium_zone="PREMIUM_BOUNDARY_ZONE"
        )
        res_premium_sell = CapitalMetaLabelingEngine.predict_meta_label(f_premium_sell, threshold=0.55)
        self.assertGreater(res_premium_sell["meta_win_prob"], res_premium_base["meta_win_prob"])
        self.assertEqual(res_premium_sell["equilibrium_zone"], "PREMIUM_BOUNDARY_ZONE")


if __name__ == "__main__":
    unittest.main()


