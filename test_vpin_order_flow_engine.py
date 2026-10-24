#!/usr/bin/env python3
"""
Unit tests for VPINOrderFlowEngine (Volume-Synchronized Probability of Toxicity - Invariant 101)
================================================================================================
"""

import unittest
from typing import List, Dict, Any
from vpin_order_flow_engine import VPINOrderFlowEngine, compute_vpin, evaluate_vpin_toxicity


def _generate_synthetic_vpin_candles(n: int = 30, flow_type: str = "BALANCED") -> List[Dict[str, Any]]:
    candles = []
    base_p = 4000.0
    for i in range(n):
        if flow_type == "BULLISH_TOXIC":
            # Consistent heavy aggressive buying thrusts
            o = base_p + i * 3.0
            c = o + 4.5
            h = c + 0.5
            l = o - 0.2
            v = 2500.0 + (i * 20.0)
        elif flow_type == "BEARISH_TOXIC":
            # Consistent heavy aggressive liquidation dumps
            o = base_p - i * 3.0
            c = o - 4.5
            h = o + 0.2
            l = c - 0.5
            v = 2500.0 + (i * 20.0)
        else: # BALANCED
            # Symmetrical two-sided oscillations
            is_up = (i % 2 == 0)
            o = base_p + (1.0 if is_up else -1.0)
            c = base_p + (2.0 if is_up else -2.0)
            h = base_p + 3.0
            l = base_p - 3.0
            v = 1000.0
        candles.append({"open": o, "high": h, "low": l, "close": c, "volume": v})
    return candles


class TestVPINOrderFlowEngine(unittest.TestCase):
    def test_vpin_balanced_flow(self):
        """Balanced two-sided flow must produce VPIN < 0.65 and no toxicity."""
        candles = _generate_synthetic_vpin_candles(n=30, flow_type="BALANCED")
        res = compute_vpin(candles)
        self.assertIn("vpin", res)
        self.assertFalse(res["is_toxic"])
        self.assertLess(res["vpin"], 0.65)
        self.assertEqual(res["dominant_toxic_flow"], "BALANCED")
        self.assertEqual(res["true_institutional_winner"], "NEUTRAL")

        gate_buy = evaluate_vpin_toxicity(candles, "BUY")
        self.assertFalse(gate_buy["is_vetoed"])
        self.assertTrue(gate_buy["is_aligned"])

        gate_sell = evaluate_vpin_toxicity(candles, "SELL")
        self.assertFalse(gate_sell["is_vetoed"])
        self.assertTrue(gate_sell["is_aligned"])

    def test_vpin_bullish_toxic_flow(self):
        """Aggressive one-sided buying must produce VPIN >= 0.65, approve BUY, and VETO SELL."""
        candles = _generate_synthetic_vpin_candles(n=35, flow_type="BULLISH_TOXIC")
        res = compute_vpin(candles)
        self.assertTrue(res["is_toxic"])
        self.assertGreaterEqual(res["vpin"], 0.65)
        self.assertEqual(res["dominant_toxic_flow"], "BULLISH")
        self.assertEqual(res["true_institutional_winner"], "BUY")
        self.assertGreater(res["net_toxicity_ratio"], 0.50)

        # BUY is aligned with institutional toxic buying wave (+30 boost)
        gate_buy = evaluate_vpin_toxicity(candles, "BUY")
        self.assertFalse(gate_buy["is_vetoed"])
        self.assertTrue(gate_buy["is_aligned"])
        self.assertEqual(gate_buy["score_boost"], 30.0)
        self.assertEqual(gate_buy["action"], "RIDE_TOXIC_BULLISH_WAVE")

        # SELL opposes institutional toxic buying wave -> STRICT VETO
        gate_sell = evaluate_vpin_toxicity(candles, "SELL")
        self.assertTrue(gate_sell["is_vetoed"])
        self.assertFalse(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], -35.0)
        self.assertIn("VPIN_INSTITUTIONAL_TOXICITY_VETO", gate_sell["veto_reason"])
        self.assertEqual(gate_sell["action"], "VETO_TOXIC_COUNTER_TRADE")

    def test_vpin_bearish_toxic_flow(self):
        """Aggressive one-sided liquidation must produce VPIN >= 0.65, approve SELL, and VETO BUY."""
        candles = _generate_synthetic_vpin_candles(n=35, flow_type="BEARISH_TOXIC")
        res = compute_vpin(candles)
        self.assertTrue(res["is_toxic"])
        self.assertGreaterEqual(res["vpin"], 0.65)
        self.assertEqual(res["dominant_toxic_flow"], "BEARISH")
        self.assertEqual(res["true_institutional_winner"], "SELL")
        self.assertLess(res["net_toxicity_ratio"], -0.50)

        # SELL is aligned with institutional toxic selling wave (+30 boost)
        gate_sell = evaluate_vpin_toxicity(candles, "SELL")
        self.assertFalse(gate_sell["is_vetoed"])
        self.assertTrue(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], 30.0)
        self.assertEqual(gate_sell["action"], "RIDE_TOXIC_BEARISH_WAVE")

        # BUY opposes institutional toxic liquidation wave -> STRICT VETO
        gate_buy = evaluate_vpin_toxicity(candles, "BUY")
        self.assertTrue(gate_buy["is_vetoed"])
        self.assertFalse(gate_buy["is_aligned"])
        self.assertEqual(gate_buy["score_boost"], -35.0)
        self.assertIn("VPIN_INSTITUTIONAL_TOXICITY_VETO", gate_buy["veto_reason"])
        self.assertEqual(gate_buy["action"], "VETO_TOXIC_COUNTER_TRADE")

    def test_vpin_bucket_construction(self):
        """Equal volume buckets must be correctly discretized."""
        candles = _generate_synthetic_vpin_candles(n=20, flow_type="BALANCED")
        res = VPINOrderFlowEngine.compute_vpin(candles, num_buckets=10)
        self.assertGreater(res["completed_buckets"], 5)
        self.assertGreater(res["bucket_volume"], 0)


if __name__ == "__main__":
    unittest.main()
