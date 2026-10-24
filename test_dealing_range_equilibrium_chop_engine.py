# -*- coding: utf-8 -*-
"""
Unit tests for DealingRangeEquilibriumChopEngine (AQ84 Pillar 4 / Invariant 103)
==============================================================================
"""

import unittest
from typing import List, Dict, Any
from dealing_range_equilibrium_chop_engine import (
    DealingRangeEquilibriumChopEngine,
    evaluate_equilibrium_chop_regime,
    evaluate_dealing_range_equilibrium_gatekeeper
)


def _generate_synthetic_range_candles(high_val: float = 2700.0, low_val: float = 2600.0, count: int = 35) -> List[Dict[str, Any]]:
    candles = []
    step = (high_val - low_val) / count
    for i in range(count):
        o = low_val + (i * step)
        c = o + 2.0
        h = max(o, c) + 3.0
        l = min(o, c) - 3.0
        candles.append({"open": o, "high": h, "low": l, "close": c, "volume": 1000.0})
    # Ensure extreme high and low are present
    candles[5]["low"] = low_val
    candles[20]["high"] = high_val
    return candles


class TestDealingRangeEquilibriumChopEngine(unittest.TestCase):
    def setUp(self):
        self.p0 = 2650.0
        self.r1 = 2700.0
        self.s1 = 2600.0
        self.epic = "GOLD"

    def test_middle_equilibrium_chop_veto(self):
        """Price in 35%-65% Dealing Range must trigger strict veto (Brownian Motion Retail Chop)."""
        # Exactly at P0 (50.0% of dealing range)
        mid_price = 2650.0
        regime = evaluate_equilibrium_chop_regime(
            epic=self.epic, current_price=mid_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertTrue(regime["is_chop_zone"])
        self.assertEqual(regime["zone_name"], "EQUILIBRIUM_CHOP_ZONE")
        self.assertEqual(regime["range_pct"], 50.0)
        self.assertEqual(regime["true_institutional_winner"], "NONE_RETAIL_CHOP")
        self.assertEqual(regime["action"], "WAIT_FOR_BOUNDARY_REACTION")

        # Gatekeeper evaluation for BUY
        gate_buy = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="BUY", current_price=mid_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertTrue(gate_buy["is_vetoed"])
        self.assertFalse(gate_buy["is_aligned"])
        self.assertEqual(gate_buy["score_boost"], -40.0)
        self.assertIn("BLOCKED_DEALING_RANGE_EQUILIBRIUM_CHOP_VETO", gate_buy["veto_reason"])

        # Gatekeeper evaluation for SELL
        gate_sell = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="SELL", current_price=mid_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertTrue(gate_sell["is_vetoed"])
        self.assertFalse(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], -40.0)
        self.assertIn("BLOCKED_DEALING_RANGE_EQUILIBRIUM_CHOP_VETO", gate_sell["veto_reason"])

        # Boundary threshold test: 45.0% and 55.0% must also be vetoed
        gate_45 = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="BUY", current_price=2645.0, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertTrue(gate_45["is_vetoed"])

    def test_discount_boundary_zone_near_s1(self):
        """Price < 35% near S1 must clear chop veto and favor BUY setups (accumulation)."""
        # Price at 2620.0 (20.0% of dealing range)
        discount_price = 2620.0
        regime = evaluate_equilibrium_chop_regime(
            epic=self.epic, current_price=discount_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertFalse(regime["is_chop_zone"])
        self.assertTrue(regime["is_discount_zone"])
        self.assertEqual(regime["zone_name"], "DISCOUNT_BOUNDARY_ZONE")
        self.assertEqual(regime["range_pct"], 20.0)
        self.assertEqual(regime["true_institutional_winner"], "BUY_ACCUMULATION_FAVORED")

        # Gatekeeper evaluation for BUY: Aligned with discount accumulation
        gate_buy = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="BUY", current_price=discount_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertFalse(gate_buy["is_vetoed"])
        self.assertTrue(gate_buy["is_aligned"])
        self.assertEqual(gate_buy["score_boost"], 25.0)

        # Gatekeeper evaluation for SELL: Not aligned (selling into support)
        gate_sell = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="SELL", current_price=discount_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertFalse(gate_sell["is_vetoed"])
        self.assertFalse(gate_sell["is_aligned"])
        self.assertLess(gate_sell["score_boost"], 0.0)

    def test_premium_boundary_zone_near_r1(self):
        """Price > 65% near R1 must clear chop veto and favor SELL setups (distribution)."""
        # Price at 2680.0 (80.0% of dealing range)
        premium_price = 2680.0
        regime = evaluate_equilibrium_chop_regime(
            epic=self.epic, current_price=premium_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertFalse(regime["is_chop_zone"])
        self.assertTrue(regime["is_premium_zone"])
        self.assertEqual(regime["zone_name"], "PREMIUM_BOUNDARY_ZONE")
        self.assertEqual(regime["range_pct"], 80.0)
        self.assertEqual(regime["true_institutional_winner"], "SELL_DISTRIBUTION_FAVORED")

        # Gatekeeper evaluation for SELL: Aligned with premium distribution
        gate_sell = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="SELL", current_price=premium_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertFalse(gate_sell["is_vetoed"])
        self.assertTrue(gate_sell["is_aligned"])
        self.assertEqual(gate_sell["score_boost"], 25.0)

        # Gatekeeper evaluation for BUY: Not aligned (buying into resistance)
        gate_buy = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="BUY", current_price=premium_price, p0=self.p0, r1=self.r1, s1=self.s1
        )
        self.assertFalse(gate_buy["is_vetoed"])
        self.assertFalse(gate_buy["is_aligned"])
        self.assertLess(gate_buy["score_boost"], 0.0)

    def test_dynamic_candle_fallback(self):
        """When R1 and S1 are omitted, coordinates must be resolved accurately from 15m candle highs/lows."""
        candles = _generate_synthetic_range_candles(high_val=2700.0, low_val=2600.0, count=35)
        # Price at 2650.0 without explicit r1/s1
        gate = evaluate_dealing_range_equilibrium_gatekeeper(
            epic=self.epic, direction="BUY", current_price=2650.0, candles_15m=candles
        )
        self.assertTrue(gate["is_vetoed"])
        self.assertEqual(gate["zone_name"], "EQUILIBRIUM_CHOP_ZONE")


if __name__ == "__main__":
    unittest.main()
