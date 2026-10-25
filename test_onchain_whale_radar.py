#!/usr/bin/env python3
"""
Unit tests for onchain_whale_radar.py (Whale Orderflow & Front-Running Radar v14.50)
Verifies:
1. Cross-Chain Multi-Entity Graph Ingestion (BTC, ETH, SOL, TRON)
2. Cumulative Volume Delta (CVD) & Dark Pool Iceberg Absorption
3. VPIN Order Flow Toxicity (Invariant 101) & Attack Wave Detection
4. Direct Capital Feedback Loop (Kelly Multiplier & Dump Risk Veto)
5. Multilingual Report Formatting (Khmer, English, Chinese)
"""

import unittest
import time
import onchain_whale_radar as owr

class TestOnChainWhaleRadar(unittest.TestCase):

    def test_cross_chain_whale_transfers(self):
        data = owr.whale_radar.scan_cross_chain_whale_transfers(force_refresh=True)
        self.assertIn("transactions", data)
        self.assertIn("net_inflow_usdt", data)
        self.assertIn("net_outflow_usdt", data)
        self.assertIn("tether_minted_usdt", data)
        self.assertIn("bias_status", data)
        self.assertGreaterEqual(len(data["transactions"]), 1)

    def test_cvd_microstructure_absorption(self):
        cvd = owr.whale_radar.compute_cvd_microstructure("BTCUSDT", limit=20)
        self.assertIn("cvd_net", cvd)
        self.assertIn("cvd_buy_ratio_pct", cvd)
        self.assertIn("regime", cvd)
        self.assertIn("regime_desc", cvd)
        self.assertIn("absorption_action", cvd)
        self.assertIn(cvd["regime"], [
            "BULLISH_ABSORPTION", "BEARISH_ABSORPTION",
            "AGGRESSIVE_BUY_THRUST", "AGGRESSIVE_SELL_DUMP"
        ])

    def test_vpin_order_flow_toxicity(self):
        vpin_info = owr.whale_radar.compute_vpin_order_flow("BTCUSDT")
        self.assertIn("vpin", vpin_info)
        self.assertIn("is_toxic", vpin_info)
        self.assertIn("dominant_toxic_flow", vpin_info)
        self.assertIn("attack_desc", vpin_info)
        self.assertIn("recommended_action", vpin_info)
        self.assertGreaterEqual(vpin_info["vpin"], 0.0)
        self.assertLessEqual(vpin_info["vpin"], 1.0)

    def test_dumping_risk_lockout_and_veto(self):
        test_sym = "TESTWHALEUSDT"
        # Initially not locked
        is_dump, _ = owr.is_dumping_risk_active(test_sym)
        self.assertFalse(is_dump)

        # Set dumping lockout for 10 minutes
        owr.set_dumping_risk_lockout(test_sym, duration_mins=10)
        is_dump_active, rem_mins = owr.is_dumping_risk_active(test_sym)
        self.assertTrue(is_dump_active)
        self.assertGreaterEqual(rem_mins, 9)

        # BUY trade must be vetoed
        is_vetoed, reason = owr.check_whale_dump_risk_veto(test_sym, "BUY")
        self.assertTrue(is_vetoed)
        self.assertIn("WHALE_DUMP_RISK_VETO", reason)

        # Kelly multiplier must contract to 0.50x
        km = owr.get_whale_kelly_multiplier(test_sym)
        self.assertEqual(km, 0.50)

    def test_multilingual_reports(self):
        for lang in ["km", "en", "zh"]:
            rep = owr.get_whale_radar_report("BTCUSDT", lang=lang)
            self.assertIsInstance(rep, str)
            self.assertGreater(len(rep), 300)
            self.assertIn("BTCUSDT", rep)
            self.assertIn("VPIN", rep)
            self.assertIn("CVD", rep)

if __name__ == "__main__":
    unittest.main()
