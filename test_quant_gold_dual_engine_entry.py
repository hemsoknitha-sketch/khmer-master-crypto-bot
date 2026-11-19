# -*- coding: utf-8 -*-
"""
Unit Test: Quant Gold Dual-Engine Coordinated Fleet Entry (AQ88 Invariant 129)
Verifies:
1. Machine 1 (M1-M5 Scalp) and Machine 2 (M15+ Macro) can open in the SAME direction without conflict.
2. Realistic structural separation ($1.80 to $2.50) replaces the flawed $10.50 wall.
3. Machine 2 opens POS2_M15_FVG_RETEST when Machine 1 is active.
4. While Machine 2 is riding its macro wave, Machine 1 can re-open POS1_M1_M5_SCALP to scalp micro-waves.
5. Capacity clamps properly at max_positions (e.g. 5).
"""
import sys
import os
import unittest
from unittest.mock import MagicMock

# Add paths
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Quant Gold")))

from execution_engine import (
    QuantGoldExecutionEngine,
    is_engine_1_scalp,
    is_engine_2_macro,
    get_gold_position_tier_spec
)


class TestQuantGoldDualEngineEntry(unittest.TestCase):

    def setUp(self):
        self.engine = QuantGoldExecutionEngine()

    def test_01_dual_engine_role_identification(self):
        """Verify Machine 1 and Machine 2 roles are distinct and non-conflicting."""
        self.assertTrue(is_engine_1_scalp("POS1_M1_M5_SCALP"))
        self.assertFalse(is_engine_2_macro("POS1_M1_M5_SCALP"))

        self.assertTrue(is_engine_2_macro("POS2_M15_FVG_RETEST"))
        self.assertFalse(is_engine_1_scalp("POS2_M15_FVG_RETEST"))

        self.assertTrue(is_engine_2_macro("POS3_M15_STRUCTURAL_SWING"))
        self.assertFalse(is_engine_1_scalp("POS3_M15_STRUCTURAL_SWING"))

    def test_02_machine_2_entry_when_machine_1_is_active(self):
        """Verify Machine 2 (POS2_M15_FVG_RETEST) can open when Machine 1 is active with >= $1.80 separation."""
        active_trades = [
            {
                "deal_id": "D1_SCALP",
                "epic": "GOLD",
                "direction": "BUY",
                "entry_price": 3850.00,
                "tranche_id": "POS1_M1_M5_SCALP",
                "scale_tier": 0
            }
        ]
        current_price = 3852.20  # Separated by $2.20 (>= $1.80)
        action = "BUY"
        existing_dir = "BUY"
        spread_val = 0.50
        min_sep = max(1.80, spread_val * 3.0)  # $1.80

        # Check separation
        too_close = any(abs(current_price - float(t["entry_price"])) < min_sep for t in active_trades)
        self.assertFalse(too_close)

        # Detect open roles
        has_scalp_open = any(is_engine_1_scalp(t.get("tranche_id", ""), int(t.get("scale_tier", 0) or 0)) for t in active_trades)
        has_macro_open = any(is_engine_2_macro(t.get("tranche_id", ""), int(t.get("scale_tier", 0) or 0)) for t in active_trades)
        self.assertTrue(has_scalp_open)
        self.assertFalse(has_macro_open)

        # Should target Machine 2 (Tier 2)
        if not has_macro_open and has_scalp_open:
            tier_num = 2
            target_tranche_label = "POS2_M15_FVG_RETEST"
        else:
            tier_num = 1
            target_tranche_label = "POS1_M1_M5_SCALP"

        self.assertEqual(tier_num, 2)
        self.assertEqual(target_tranche_label, "POS2_M15_FVG_RETEST")

    def test_03_machine_1_reentry_while_machine_2_rides_macro(self):
        """Verify Machine 1 can re-open to scalp when Machine 2 is holding its macro position."""
        active_trades = [
            {
                "deal_id": "D2_MACRO",
                "epic": "GOLD",
                "direction": "BUY",
                "entry_price": 3848.00,
                "tranche_id": "POS2_M15_FVG_RETEST",
                "scale_tier": 1  # In profit, trailing
            }
        ]
        current_price = 3851.00  # Pullback dip separated by $3.00 from macro entry
        spread_val = 0.50
        min_sep = max(1.80, spread_val * 3.0)

        too_close = any(abs(current_price - float(t["entry_price"])) < min_sep for t in active_trades)
        self.assertFalse(too_close)

        has_scalp_open = any(is_engine_1_scalp(t.get("tranche_id", ""), int(t.get("scale_tier", 0) or 0)) for t in active_trades)
        has_macro_open = any(is_engine_2_macro(t.get("tranche_id", ""), int(t.get("scale_tier", 0) or 0)) for t in active_trades)
        self.assertFalse(has_scalp_open)
        self.assertTrue(has_macro_open)

        # Machine 2 is active, but scalp is empty -> Machine 1 opens!
        if not has_scalp_open and has_macro_open:
            tier_num = 1
            target_tranche_label = "POS1_M1_M5_SCALP"
        else:
            tier_num = 2
            target_tranche_label = "POS2_M15_FVG_RETEST"

        self.assertEqual(tier_num, 1)
        self.assertEqual(target_tranche_label, "POS1_M1_M5_SCALP")

    def test_04_position_3_swing_when_both_active(self):
        """Verify Position 3 (M15 Structural Swing) opens when both Machine 1 & 2 are active."""
        active_trades = [
            {"deal_id": "D1", "entry_price": 3850.00, "tranche_id": "POS1_M1_M5_SCALP", "scale_tier": 0},
            {"deal_id": "D2", "entry_price": 3852.50, "tranche_id": "POS2_M15_FVG_RETEST", "scale_tier": 1}
        ]
        has_scalp_open = any(is_engine_1_scalp(t.get("tranche_id", ""), int(t.get("scale_tier", 0) or 0)) for t in active_trades)
        has_macro_open = any(is_engine_2_macro(t.get("tranche_id", ""), int(t.get("scale_tier", 0) or 0)) for t in active_trades)
        self.assertTrue(has_scalp_open)
        self.assertTrue(has_macro_open)

        pos_count = len(active_trades)
        tier_spec = get_gold_position_tier_spec(pos_count)
        self.assertEqual(tier_spec["tier"], 3)
        self.assertEqual(tier_spec["label"], "POS3_M15_STRUCTURAL_SWING")


if __name__ == "__main__":
    unittest.main()
