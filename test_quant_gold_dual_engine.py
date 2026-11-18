# -*- coding: utf-8 -*-
"""
Unit test for Dual Independent Trading Engines (AQ88 Invariant 125):
- Machine 1: M1 - M5 Scalping Fast Harvester
- Machine 2: M15+ Institutional Macro / Swing Trend
- Non-Conflict & Multi-Position Independence Guarantee
"""
import sys
import os
import unittest
import asyncio
from unittest.mock import MagicMock, patch

# Add paths
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Quant Gold")))

from execution_engine import (
    QuantGoldExecutionEngine,
    is_engine_1_scalp,
    is_engine_2_macro,
    get_gold_position_tier_spec,
    calculate_capital_gold_lot_size
)


class TestQuantGoldDualEngine(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.engine = QuantGoldExecutionEngine()

    def test_engine_classification(self):
        """Verify that Machine 1 Scalp and Machine 2 Macro positions are cleanly classified."""
        # Machine 1 Scalp
        self.assertTrue(is_engine_1_scalp("POS1_M1_M5_SCALP", 0))
        self.assertTrue(is_engine_1_scalp("ENGINE_1_M1_M5_SCALP", 0))
        self.assertTrue(is_engine_1_scalp("SCALP_FAST", 0))
        self.assertFalse(is_engine_2_macro("POS1_M1_M5_SCALP", 0))

        # Machine 2 Macro
        self.assertTrue(is_engine_2_macro("POS2_M15_FVG_RETEST", 1))
        self.assertTrue(is_engine_2_macro("POS3_M15_STRUCTURAL_SWING", 2))
        self.assertTrue(is_engine_2_macro("POS4_H1_TREND_PYRAMID", 3))
        self.assertTrue(is_engine_2_macro("POS5_H4_MOONSHOT_RUNNER", 4))
        self.assertTrue(is_engine_2_macro("ENGINE_2_M15_MACRO", 1))
        self.assertFalse(is_engine_1_scalp("POS2_M15_FVG_RETEST", 1))

    @patch("execution_engine.db")
    @patch("execution_engine.capital_engine")
    async def test_scoped_fleet_close_scalp_only(self, mock_cap_eng, mock_db):
        """Verify that target_scope='SCALP_ONLY' closes ONLY Machine 1 trades and preserves Machine 2."""
        mock_db.get_active_capital_auto_trades.return_value = [
            # Machine 1 Scalp trade
            {"chat_id": 859271875, "deal_id": "DEAL_SCALP_1", "epic": "GOLD", "direction": "BUY", "entry_price": 3870.0, "size": 0.5, "is_demo": 0, "tranche_id": "POS1_M1_M5_SCALP", "scale_tier": 0},
            # Machine 2 Macro trade
            {"chat_id": 859271875, "deal_id": "DEAL_MACRO_2", "epic": "GOLD", "direction": "BUY", "entry_price": 3865.0, "size": 0.5, "is_demo": 0, "tranche_id": "POS2_M15_FVG_RETEST", "scale_tier": 1},
        ]
        mock_db.get_active_capital_auto_users.return_value = [
            {"chat_id": 859271875, "is_demo": False}
        ]

        mock_user_eng = MagicMock()
        mock_user_eng.get_open_positions.return_value = []
        mock_user_eng.close_position.return_value = {"success": True}
        mock_cap_eng.get_user_capital_engine.return_value = mock_user_eng

        # Execute close with target_scope='SCALP_ONLY'
        closed_count = await self.engine._close_all_fleet_open_gold_positions(
            direction="BUY",
            reason="M1_M5_SCALP_EXHAUSTION_HARVEST",
            exit_price=3872.5,
            current_pnl_pts=2.5,
            target_scope="SCALP_ONLY"
        )

        # Only DEAL_SCALP_1 should be closed (count=1), DEAL_MACRO_2 remains open!
        self.assertEqual(closed_count, 1)
        mock_db.update_capital_auto_trade_close.assert_called_once_with("DEAL_SCALP_1", exit_price=3872.5, pnl=1.25)

    @patch("execution_engine.db")
    @patch("execution_engine.capital_engine")
    async def test_scoped_fleet_close_macro_only(self, mock_cap_eng, mock_db):
        """Verify that target_scope='MACRO_ONLY' closes ONLY Machine 2 trades and preserves Machine 1."""
        mock_db.get_active_capital_auto_trades.return_value = [
            {"chat_id": 859271875, "deal_id": "DEAL_SCALP_1", "epic": "GOLD", "direction": "BUY", "entry_price": 3870.0, "size": 0.5, "is_demo": 0, "tranche_id": "POS1_M1_M5_SCALP", "scale_tier": 0},
            {"chat_id": 859271875, "deal_id": "DEAL_MACRO_2", "epic": "GOLD", "direction": "BUY", "entry_price": 3865.0, "size": 0.5, "is_demo": 0, "tranche_id": "POS2_M15_FVG_RETEST", "scale_tier": 1},
        ]
        mock_db.get_active_capital_auto_users.return_value = [
            {"chat_id": 859271875, "is_demo": False}
        ]

        mock_user_eng = MagicMock()
        mock_user_eng.get_open_positions.return_value = []
        mock_user_eng.close_position.return_value = {"success": True}
        mock_cap_eng.get_user_capital_engine.return_value = mock_user_eng

        closed_count = await self.engine._close_all_fleet_open_gold_positions(
            direction="BUY",
            reason="MACRO_SWING_TP_HARVEST",
            exit_price=3880.0,
            current_pnl_pts=15.0,
            target_scope="MACRO_ONLY"
        )

        # Only DEAL_MACRO_2 should be closed (count=1), DEAL_SCALP_1 remains open!
        self.assertEqual(closed_count, 1)
        mock_db.update_capital_auto_trade_close.assert_called_once_with("DEAL_MACRO_2", exit_price=3880.0, pnl=7.5)

    def test_capital_gold_lot_size_tiers_and_conviction(self):
        """Verify dynamic lot sizing across capital tiers ($100 -> 0.5 oz, $200 -> 1.0 oz, $300 -> 1.5 oz) and conviction scaling."""
        # Baseline Sizing (Confidence 75%)
        self.assertEqual(calculate_capital_gold_lot_size(budget=100.0, confidence=75.0), 0.50)
        self.assertEqual(calculate_capital_gold_lot_size(budget=200.0, confidence=75.0), 1.00)
        self.assertEqual(calculate_capital_gold_lot_size(budget=300.0, confidence=75.0), 1.50)
        self.assertEqual(calculate_capital_gold_lot_size(budget=400.0, confidence=75.0), 2.00)

        # High Conviction (Confidence 85% -> 1.15x)
        self.assertEqual(calculate_capital_gold_lot_size(budget=100.0, confidence=85.0), 0.57)
        self.assertEqual(calculate_capital_gold_lot_size(budget=200.0, confidence=85.0), 1.15)
        self.assertEqual(calculate_capital_gold_lot_size(budget=300.0, confidence=85.0), 1.72)

        # Supreme Conviction (Confidence 95% -> 1.25x)
        self.assertEqual(calculate_capital_gold_lot_size(budget=100.0, confidence=95.0), 0.62)
        self.assertEqual(calculate_capital_gold_lot_size(budget=200.0, confidence=95.0), 1.25)
        self.assertEqual(calculate_capital_gold_lot_size(budget=300.0, confidence=95.0), 1.88)

        # Micro-Capital Safeguard
        self.assertEqual(calculate_capital_gold_lot_size(budget=20.0, confidence=75.0), 0.10)
        self.assertEqual(calculate_capital_gold_lot_size(budget=50.0, confidence=75.0), 0.25)


if __name__ == "__main__":
    unittest.main()
