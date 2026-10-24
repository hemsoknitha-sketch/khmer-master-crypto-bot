#!/usr/bin/env python3
"""
Unit tests for OrderFlowDeltaAbsorptionEngine (AQ84 Pillar 3 / Invariant 102)
=============================================================================
"""

import unittest
from typing import List, Dict, Any
from order_flow_delta_absorption_engine import (
    OrderFlowDeltaAbsorptionEngine,
    evaluate_delta_absorption,
    evaluate_boundary_absorption_gatekeeper
)


def _generate_synthetic_boundary_candles(setup_type: str = "BALANCED") -> List[Dict[str, Any]]:
    candles = []
    base_p = 4000.0
    for i in range(25):
        # Baseline historical bars with normal volume 1000
        o = base_p + (i * 0.5)
        c = o + 0.8
        h = c + 0.5
        l = o - 0.5
        v = 1000.0
        candles.append({"open": o, "high": h, "low": l, "close": c, "volume": v})

    if setup_type == "BULL_EXHAUSTION_R1":
        # Price surges into R1 (4050.0) on heavy volume 3500 (RVOL 3.5x),
        # but stalls and creates large upper rejection wick!
        r1 = 4050.0
        o = 4045.0
        h = 4052.0  # Pierced R1
        c = 4046.0  # Rejected back below R1!
        l = 4044.0
        v = 3500.0  # Heavy buying surge absorbed by limit sellers
        candles.append({"open": o, "high": h, "low": l, "close": c, "volume": v})

    elif setup_type == "BEAR_EXHAUSTION_S1":
        # Price dumps into S1 (3950.0) on heavy volume 3500 (RVOL 3.5x),
        # but stalls and creates large lower rejection wick!
        s1 = 3950.0
        o = 3955.0
        l = 3948.0  # Pierced S1
        c = 3954.0  # Rejected back above S1!
        h = 3956.0
        v = 3500.0  # Heavy selling surge absorbed by limit buyers
        candles.append({"open": o, "high": h, "low": l, "close": c, "volume": v})

    else: # BALANCED
        o = base_p + 12.0
        c = o + 0.5
        h = c + 0.5
        l = o - 0.5
        v = 1000.0
        candles.append({"open": o, "high": h, "low": l, "close": c, "volume": v})

    return candles


class TestOrderFlowDeltaAbsorptionEngine(unittest.TestCase):
    def test_balanced_flow(self):
        """Normal flow far from boundaries must not trigger absorption."""
        candles = _generate_synthetic_boundary_candles(setup_type="BALANCED")
        res = evaluate_delta_absorption("GOLD", 4012.5, candles, r1=4100.0, s1=3900.0, atr_15m=10.0)
        self.assertFalse(res["is_absorption_active"])
        self.assertFalse(res["is_bull_exhaustion"])
        self.assertFalse(res["is_bear_exhaustion"])
        self.assertEqual(res["true_institutional_winner"], "NEUTRAL")

        gate_buy = evaluate_boundary_absorption_gatekeeper("GOLD", "BUY", 4012.5, candles, r1=4100.0, s1=3900.0)
        self.assertFalse(gate_buy["is_vetoed"])
        self.assertTrue(gate_buy["is_aligned"])

    def test_bull_exhaustion_at_r1(self):
        """High volume buying surge stalling at R1 must trigger Bull Exhaustion, approve SELL, and veto BUY."""
        candles = _generate_synthetic_boundary_candles(setup_type="BULL_EXHAUSTION_R1")
        r1 = 4050.0
        res = evaluate_delta_absorption("GOLD", 4046.0, candles, r1=r1, s1=3950.0, atr_15m=8.0, spread=0.50)

        self.assertTrue(res["is_absorption_active"])
        self.assertTrue(res["is_bull_exhaustion"])
        self.assertFalse(res["is_bear_exhaustion"])
        self.assertEqual(res["true_institutional_winner"], "SELL")
        self.assertEqual(res["score_boost"], 35.0)
        self.assertIsNotNone(res["structural_sl"])
        self.assertGreater(res["structural_sl"], 4052.0)  # Tightly above high wick

        # Gatekeeper evaluation:
        # SELL is aligned with institutional absorption winners (+35 boost)
        gate_sell = evaluate_boundary_absorption_gatekeeper("GOLD", "SELL", 4046.0, candles, r1=r1, s1=3950.0, atr_15m=8.0, spread=0.50)
        self.assertFalse(gate_sell["is_vetoed"])
        self.assertTrue(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], 35.0)
        self.assertEqual(gate_sell["true_institutional_winner"], "SELL")

        # BUY opposes institutional limit sell absorption -> STRICT VETO
        gate_buy = evaluate_boundary_absorption_gatekeeper("GOLD", "BUY", 4046.0, candles, r1=r1, s1=3950.0, atr_15m=8.0, spread=0.50)
        self.assertTrue(gate_buy["is_vetoed"])
        self.assertFalse(gate_buy["is_aligned"])
        self.assertEqual(gate_buy["score_boost"], -35.0)
        self.assertIn("BLOCKED_ORDER_FLOW_BULL_EXHAUSTION_VETO", gate_buy["veto_reason"])

    def test_bear_exhaustion_at_s1(self):
        """High volume selling surge stalling at S1 must trigger Bear Exhaustion, approve BUY, and veto SELL."""
        candles = _generate_synthetic_boundary_candles(setup_type="BEAR_EXHAUSTION_S1")
        s1 = 3950.0
        res = evaluate_delta_absorption("GOLD", 3954.0, candles, r1=4050.0, s1=s1, atr_15m=8.0, spread=0.50)

        self.assertTrue(res["is_absorption_active"])
        self.assertTrue(res["is_bear_exhaustion"])
        self.assertFalse(res["is_bull_exhaustion"])
        self.assertEqual(res["true_institutional_winner"], "BUY")
        self.assertEqual(res["score_boost"], 35.0)
        self.assertIsNotNone(res["structural_sl"])
        self.assertLess(res["structural_sl"], 3948.0)  # Tightly below low wick

        # Gatekeeper evaluation:
        # BUY is aligned with institutional absorption winners (+35 boost)
        gate_buy = evaluate_boundary_absorption_gatekeeper("GOLD", "BUY", 3954.0, candles, r1=4050.0, s1=s1, atr_15m=8.0, spread=0.50)
        self.assertFalse(gate_buy["is_vetoed"])
        self.assertTrue(gate_buy["is_aligned"])
        self.assertEqual(gate_buy["score_boost"], 35.0)
        self.assertEqual(gate_buy["true_institutional_winner"], "BUY")

        # SELL opposes institutional limit buy absorption -> STRICT VETO
        gate_sell = evaluate_boundary_absorption_gatekeeper("GOLD", "SELL", 3954.0, candles, r1=4050.0, s1=s1, atr_15m=8.0, spread=0.50)
        self.assertTrue(gate_sell["is_vetoed"])
        self.assertFalse(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], -35.0)
        self.assertIn("BLOCKED_ORDER_FLOW_BEAR_EXHAUSTION_VETO", gate_sell["veto_reason"])


if __name__ == "__main__":
    unittest.main()
