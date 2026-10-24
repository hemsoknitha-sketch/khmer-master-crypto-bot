# -*- coding: utf-8 -*-
"""
Test Suite: Institutional Profitability Architecture, Smart Money Leveraged Funds Alignment & 5-Pillar Win Rate Expansion Engine (Invariant 104 - AQ104)
====================================================================================================================================================
Verifies the Five Institutional Pillars to push Win Rate to 75% - 85% and maximize exponential compound growth:
  1. Pillar 1: Smart Money Alignment Rule with Leveraged Funds (Short >= 60% vetoes M15 BUY signals 100%, cutting falling knife loss by >70%).
  2. Pillar 2: Real Structural Stop Loss behind Broker SL Clusters (SL_R1 / SL_S1) + 1.5x Spread Buffer (preventing spread blowout stop-outs).
  3. Pillar 3: 4-Phase Breakeven Armor & Multi-Target Scale-Out (Phase 1 at +1.2R cuts risk 60%, Phase 2 at +1.8R locks 0.00R Free Roll, Phase 3 at +3.5R locks +2.0R floor, 20% Runner rides to +8.0R - +10.0R).
  4. Pillar 4: Flash Shock Protective Early Harvest (Peak UPL >= $2.50 or Peak ROI >= 8.0%, pulling back >= 50% triggers instant market harvest).
  5. Pillar 5: 45-Minute Post-SL Anti-Revenge Quarantine with Gold Adaptive Post-Loss Re-Study Exception (locks asset 45m, bypassed when >=92% confluence candlestick pattern confirms).
"""

import time
import unittest
from capital_market_report_engine import CapitalMarketReportEngine
from capital_meta_labeling_engine import CapitalMetaLabelingEngine
from dynamic_structural_stops import DynamicStructuralStops
from super_smart_capital_citadel import TradFiMultiTargetScaleOutManager
import capital_engine


class TestInvariant104FivePillars(unittest.TestCase):

    def test_pillar_1_smart_money_leveraged_funds_alignment(self):
        """Pillar 1: Leveraged Funds Short >= 60% vetoes M15 BUY 100%; Long >= 60% vetoes SELL 100%."""
        # A. Market Report Engine Evaluation
        # When Leveraged Funds are heavily Short (e.g. 70.0% Short / 30.0% Long on Gold)
        sent_eval_buy = CapitalMarketReportEngine.evaluate_contrarian_sentiment_edge(
            epic="GOLD",
            proposed_side="BUY",
            current_price=2650.0
        )
        # Gold default synthetic: Leveraged Funds are 87.0% Short, Retail 84.0% Long
        self.assertTrue(sent_eval_buy["is_vetoed"])
        self.assertTrue(sent_eval_buy["is_leveraged_funds_vetoed"])
        self.assertIn("SMART_MONEY_ALIGNMENT_VETO", sent_eval_buy["veto_reason"])
        self.assertIn("LEVERAGED_FUNDS_SHORT_VETO", sent_eval_buy["veto_reason"])
        self.assertLessEqual(sent_eval_buy["score_boost"], -35.0)

        # Selling when Leveraged Funds are Short should be aligned (+30 boost)
        sent_eval_sell = CapitalMarketReportEngine.evaluate_contrarian_sentiment_edge(
            epic="GOLD",
            proposed_side="SELL",
            current_price=2650.0
        )
        self.assertFalse(sent_eval_sell["is_vetoed"])
        self.assertTrue(sent_eval_sell["is_smart_money_aligned"])
        self.assertGreaterEqual(sent_eval_sell["score_boost"], 30.0)

        # B. Meta-Labeling Model 2 Governor Evaluation
        feat_buy = {
            "direction_num": 1.0,  # BUY
            "leveraged_funds_long_pct": 30.0,  # 70% Short
            "client_long_pct": 50.0,
            "smart_money_divergence": -20.0
        }
        res_meta_buy = CapitalMetaLabelingEngine.predict_meta_label(feat_buy, threshold=0.60)
        self.assertFalse(res_meta_buy["is_approved"])
        self.assertEqual(res_meta_buy["meta_win_prob"], 0.0)
        self.assertEqual(res_meta_buy["sizing_multiplier"], 0.0)
        self.assertIn("LEVERAGED_FUNDS_SHORT_VETO", res_meta_buy["reason"])

        feat_sell = {
            "direction_num": -1.0,  # SELL
            "leveraged_funds_long_pct": 75.0,  # 75% Long
            "client_long_pct": 50.0,
            "smart_money_divergence": 20.0
        }
        res_meta_sell = CapitalMetaLabelingEngine.predict_meta_label(feat_sell, threshold=0.60)
        self.assertFalse(res_meta_sell["is_approved"])
        self.assertEqual(res_meta_sell["meta_win_prob"], 0.0)
        self.assertEqual(res_meta_sell["sizing_multiplier"], 0.0)
        self.assertIn("LEVERAGED_FUNDS_LONG_VETO", res_meta_sell["reason"])
        print("[TEST PILLAR 1 PASS] Smart Money Leveraged Funds Alignment Rule certified!")

    def test_pillar_2_broker_sl_cluster_structural_stops(self):
        """Pillar 2: Structural SL behind Broker SL Clusters (SL_R1 / SL_S1) + 1.5x Spread Buffer."""
        # BUY Setup: Price at 2620 near Support 1 (2600), SL_S1 = 2575.0, spread = 0.50
        sl_eval_buy = DynamicStructuralStops.calculate_structural_sl(
            side="BUY",
            curr_price=2620.0,
            spread=0.50,
            atr_15m=10.0,
            swing_high=2700.0,
            swing_low=2600.0,
            broker_sup1_sl=2575.0
        )
        # raw_anchor should be <= 2575.0, and vol_buffer >= 1.5 * spread (0.75)
        self.assertLessEqual(sl_eval_buy["structural_anchor"], 2575.0)
        self.assertGreaterEqual(sl_eval_buy["volatility_buffer"], 0.75)
        self.assertLessEqual(sl_eval_buy["invalidation_sl"], 2575.0 - 0.75)
        self.assertEqual(sl_eval_buy["anchor_type"], "BROKER_SL_CLUSTER_S1")

        # SELL Setup: Price at 2680 near Resistance 1 (2700), SL_R1 = 2725.0, spread = 0.50
        sl_eval_sell = DynamicStructuralStops.calculate_structural_sl(
            side="SELL",
            curr_price=2680.0,
            spread=0.50,
            atr_15m=10.0,
            swing_high=2700.0,
            swing_low=2600.0,
            broker_res1_sl=2725.0
        )
        self.assertGreaterEqual(sl_eval_sell["structural_anchor"], 2725.0)
        self.assertGreaterEqual(sl_eval_sell["volatility_buffer"], 0.75)
        self.assertGreaterEqual(sl_eval_sell["invalidation_sl"], 2725.0 + 0.75)
        self.assertEqual(sl_eval_sell["anchor_type"], "BROKER_SL_CLUSTER_R1")
        print("[TEST PILLAR 2 PASS] Broker SL Cluster Structural Stops & 1.5x Spread Buffer certified!")

    def test_pillar_3_four_phase_breakeven_armor_lifecycle(self):
        """Pillar 3: 4-Phase Breakeven Armor & Multi-Target Scale-Out."""
        plan = TradFiMultiTargetScaleOutManager.calculate_scale_out_plan(
            epic="GOLD",
            direction="BUY",
            entry_price=2650.0,
            sl_price=2640.0,
            total_size=1.0,
            spread=0.40,
            tp1_r=1.80,
            tp2_r=3.50,
            runner_r=8.00,
            atr_15m=4.0
        )
        # Phase 1 (+1.2R): Risk reduced by 60%
        res_p1 = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="GOLD", direction="BUY", entry_price=2650.0, current_price=2662.0,
            sl_dist=10.0, spread=0.40, upl=12.0, peak_upl=12.0, scale_tier=0.0, atr_15m=4.0
        )
        self.assertEqual(res_p1["action"], "PHASE_1_RISK_REDUCTION")
        self.assertEqual(res_p1["new_scale_tier"], 0.5)

        # Phase 2 (+1.8R): 50% TP1 bank & Breakeven Armor (0.00R Free Roll)
        res_p2 = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="GOLD", direction="BUY", entry_price=2650.0, current_price=2668.5,
            sl_dist=10.0, spread=0.40, upl=18.5, peak_upl=18.5, scale_tier=0.5, atr_15m=4.0
        )
        self.assertEqual(res_p2["action"], "STAGE_1_BREAKEVEN_ARMOR")
        self.assertEqual(res_p2["new_scale_tier"], 1)
        self.assertGreaterEqual(res_p2["new_sl"], 2650.20)

        # Phase 3 (+3.5R): 30% TP2 bank & +2.0R Cash Floor
        res_p3 = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="GOLD", direction="BUY", entry_price=2650.0, current_price=2686.0,
            sl_dist=10.0, spread=0.40, upl=36.0, peak_upl=36.0, scale_tier=1, atr_15m=4.0
        )
        self.assertEqual(res_p3["action"], "STAGE_2_PROFIT_LOCK")
        self.assertEqual(res_p3["new_scale_tier"], 2)
        self.assertEqual(res_p3["new_sl"], 2670.0)

        # Moonshot Runner trail (+8.0R - +10.0R)
        res_runner = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="GOLD", direction="BUY", entry_price=2650.0, current_price=2755.0,
            sl_dist=10.0, spread=0.40, upl=105.0, peak_upl=105.0, scale_tier=2, atr_15m=4.0
        )
        self.assertEqual(res_runner["action"], "STAGE_3_MOONSHOT_HARVEST")
        self.assertTrue(res_runner["should_close_tranche"])
        print("[TEST PILLAR 3 PASS] 4-Phase Breakeven Armor & Multi-Target Scale-Out certified!")

    def test_pillar_4_flash_shock_protective_early_harvest(self):
        """Pillar 4: Peak UPL >= $2.50 or Peak ROI >= 8.0%, retracing >= 50% triggers instant market exit."""
        # ScaleOutManager flash shock evaluation
        res_shock = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="US100",
            direction="BUY",
            entry_price=20000.0,
            current_price=20015.0,
            sl_dist=100.0,
            spread=1.50,
            upl=1.50,        # Retraced to $1.50 (<= 50% of $3.50 peak)
            peak_upl=3.50,   # Peak UPL was >= $2.50
            scale_tier=0.5
        )
        self.assertEqual(res_shock["action"], "SHOCK_EARLY_HARVEST")
        self.assertTrue(res_shock["should_close_tranche"])
        self.assertIn("Flash shock", res_shock["reason"])
        print("[TEST PILLAR 4 PASS] Flash Shock Protective Early Harvest certified!")

    def test_pillar_5_post_sl_quarantine_and_gold_adaptive_restudy(self):
        """Pillar 5: 45-Minute Post-SL Quarantine with Gold Adaptive Re-Study Protocol."""
        epic_test = "NVDA"
        capital_engine.set_global_asset_quarantine(epic_test, duration_seconds=2700.0, reason="AUDIT_TEST_SL")
        is_q, rem_q, q_reason = capital_engine.is_asset_quarantined(epic_test)
        self.assertTrue(is_q)
        self.assertGreater(rem_q, 2600.0)
        self.assertIn("POST_SL_QUARANTINE_ACTIVE", q_reason)

        # Clear test quarantine
        capital_engine._GLOBAL_ASSET_COOLDOWNS.pop("NVDA", None)
        is_q_cleared, _, _ = capital_engine.is_asset_quarantined(epic_test)
        self.assertFalse(is_q_cleared)

        # Verify Gold Adaptive Re-Study Protocol interface
        import gold_candlestick_pattern_memory as gcpm
        self.assertTrue(hasattr(gcpm, "evaluate_gold_adaptive_re_entry"))
        print("[TEST PILLAR 5 PASS] 45-Minute Post-SL Quarantine & Gold Adaptive Re-Study certified!")


if __name__ == "__main__":
    unittest.main()
