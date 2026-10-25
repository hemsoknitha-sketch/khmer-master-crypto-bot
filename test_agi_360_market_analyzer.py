"""
Unit Tests for AGI 360 Market Analyzer (5-Agent AGI Swarm)
Validating Invariants 85, 86, 89, 95, 96, and 103.
"""
import unittest
import pandas as pd
import numpy as np

import agi_360_market_analyzer as a360


class TestAGI360MarketAnalyzer(unittest.TestCase):
    """
    Rigorously verifies the 4 pillars of the 5-Agent AGI 360° Technical & Structural Market Analyzer.
    """

    def test_01_afml_meta_labeling_integration(self):
        """
        Pillar 1: AFML Marcos López de Prado Meta-Labeling Integration (Invariants 85 & 96).
        Model 1 Citadel Score & Model 2 Win Expectancy (p_hat >= 0.55 threshold) with sizing multiplier.
        """
        res = a360.analyze_market_asset("BTCUSDT", user_lang="km")
        self.assertIn("citadel_score", res)
        self.assertIn("meta_win_prob", res)
        self.assertIn("sizing_multiplier", res)
        self.assertIn("is_meta_approved", res)
        
        # Verify scores are valid bounds
        self.assertGreaterEqual(res["citadel_score"], 0.0)
        self.assertLessEqual(res["citadel_score"], 100.0)
        self.assertGreaterEqual(res["meta_win_prob"], 0.0)
        self.assertLessEqual(res["meta_win_prob"], 1.0)
        self.assertGreaterEqual(res["sizing_multiplier"], 0.0)

        # Verify report contains AFML Meta-Labeling text
        report = res["report_text"]
        self.assertIn("META-LABELING", report.upper())
        self.assertTrue("MODEL 1" in report.upper() or "MODEL 2" in report.upper())

    def test_02_gaussian_hmm_and_equilibrium_chop_guard(self):
        """
        Pillar 2: Gaussian HMM 3-State Regime Detector (Invariant 86) &
        35%-65% Dealing Range Equilibrium Chop Engine (Invariant 103).
        """
        res = a360.analyze_market_asset("SOLUSDT", user_lang="en")
        self.assertIn("hmm_state", res)
        self.assertIn(res["hmm_state"], [
            "STATE_0_TREND_EXPANSION",
            "STATE_1_VOLATILITY_SHOCK",
            "STATE_2_MEAN_REVERTING_CHOP"
        ])
        self.assertIn("is_equilibrium_chop", res)
        self.assertIn("range_pct", res)
        
        # Check that range_pct is bounded 0-100%
        self.assertGreaterEqual(res["range_pct"], 0.0)
        self.assertLessEqual(res["range_pct"], 100.0)

        # If range is within 35% - 65%, is_equilibrium_chop must be True
        if 35.0 <= res["range_pct"] <= 65.0:
            self.assertTrue(res["is_equilibrium_chop"])
            self.assertIn("BLOCK_CHOP_ZONE", res["report_text"])

    def test_03_smc_turtle_soup_and_breakeven_armor(self):
        """
        Pillar 3: Smart Money Concepts (SMC) & Turtle Soup Detection (Invariant 95).
        Coordinates for Liquidity Sweeps, Structural SL, Breakeven Armor Net Floor, and asymmetric targets.
        """
        res = a360.analyze_market_asset("ETHUSDT", user_lang="km")
        self.assertIn("structural_sl", res)
        self.assertIn("tp1_target", res)
        self.assertIn("tp2_target", res)
        self.assertGreater(res["current_price"], 0.0)
        self.assertGreater(res["structural_sl"], 0.0)

        report = res["report_text"]
        self.assertIn("BREAKEVEN ARMOR", report.upper())
        self.assertIn("TURTLE SOUP", report.upper())
        self.assertIn("TP1", report.upper())
        self.assertIn("TP2", report.upper())

    def test_04_multi_asset_tri_regional_universe(self):
        """
        Pillar 4: Multi-Asset Universe (Invariant 89).
        Supports Crypto (BTC, SOL) and TradFi (Spot Gold XAUUSD, US100, NVDA) from Tri-Regional RAM.
        """
        # Test Gold
        gold_res = a360.analyze_market_asset("GOLD", user_lang="km")
        self.assertIn("GOLD", gold_res["symbol"])
        self.assertGreater(gold_res["current_price"], 0.0)
        self.assertIn("Precious Metals", gold_res["report_text"])

        # Test US Tech Equity
        nvda_res = a360.analyze_market_asset("NVDA", user_lang="en")
        self.assertEqual(nvda_res["symbol"], "NVDA")
        self.assertGreater(nvda_res["current_price"], 0.0)
        self.assertIn("Semiconductors", nvda_res["report_text"])

    def test_05_trilingual_support(self):
        """
        Verifies Khmer, English, and Chinese formatting.
        """
        res_km = a360.analyze_market_asset("BTCUSDT", user_lang="km")
        res_en = a360.analyze_market_asset("BTCUSDT", user_lang="en")
        res_zh = a360.analyze_market_asset("BTCUSDT", user_lang="zh")

        self.assertIn("ស្ថាបត្យកម្ម", res_km["report_text"])
        self.assertIn("EXPECTANCY", res_en["report_text"].upper())
        self.assertIn("胜率", res_zh["report_text"])


if __name__ == "__main__":
    unittest.main()
