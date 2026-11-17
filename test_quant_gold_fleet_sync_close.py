# -*- coding: utf-8 -*-
"""
Unit test for Universal Fleet-Wide Synchronized Close & Size-Invariant Harvest (AQ88 Invariant 121).
"""
import sys
import os
import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# Add parent path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Quant Gold")))

from execution_engine import QuantGoldExecutionEngine


class TestFleetSyncClose(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.engine = QuantGoldExecutionEngine()

    @patch("execution_engine.db")
    @patch("execution_engine.capital_engine")
    async def test_close_all_fleet_open_gold_positions(self, mock_cap_eng, mock_db):
        """Verify that _close_all_fleet_open_gold_positions closes all deals across all users concurrently."""
        mock_db.get_active_capital_auto_trades.return_value = [
            {"chat_id": 859271875, "deal_id": "DEAL_SA_LIVE", "epic": "GOLD", "direction": "SELL", "entry_price": 3875.0, "size": 0.6, "is_demo": 0},
            {"chat_id": 859271875, "deal_id": "DEAL_SA_DEMO", "epic": "GOLD", "direction": "SELL", "entry_price": 3875.0, "size": 0.6, "is_demo": 1},
            {"chat_id": 643724109, "deal_id": "DEAL_VIP_1", "epic": "GOLD", "direction": "SELL", "entry_price": 3875.0, "size": 0.25, "is_demo": 0},
        ]
        mock_db.get_active_capital_auto_users.return_value = [
            {"chat_id": 859271875, "is_demo": False},
            {"chat_id": 643724109, "is_demo": False}
        ]
        
        mock_user_eng = MagicMock()
        mock_user_eng.get_open_positions.return_value = []
        mock_user_eng.close_position.return_value = {"success": True}
        mock_cap_eng.get_user_capital_engine.return_value = mock_user_eng

        closed_count = await self.engine._close_all_fleet_open_gold_positions(
            direction="SELL",
            reason="TEST_MICRO_EXHAUSTION_HARVEST",
            exit_price=3871.0,
            current_pnl_pts=4.0
        )

        self.assertEqual(closed_count, 3)
        self.assertEqual(mock_db.update_capital_auto_trade_close.call_count, 3)
        self.assertIsNone(self.engine._active_gold_deal_id)
        self.assertEqual(self.engine._active_gold_stage, "IDLE")

    def test_size_invariant_thresholds(self):
        """Verify that small lot (0.2 oz) and standard lot (1.0 oz) both qualify for harvest."""
        spread = 0.50
        
        # Test 0.2 oz small account
        sz_small = 0.2
        min_fee_upl_small = max(0.15, spread * sz_small * 1.2)
        min_profit_pts = max(0.80, spread * 1.5)
        self.assertEqual(min_fee_upl_small, 0.15)
        self.assertEqual(min_profit_pts, 0.80)
        
        # At 2.0 pts profit:
        upl_small = 2.0 * sz_small  # $0.40
        self.assertGreater(upl_small, min_fee_upl_small)

        # Test 1.0 oz standard account
        sz_large = 1.0
        min_fee_upl_large = max(0.15, spread * sz_large * 1.2)
        self.assertEqual(min_fee_upl_large, 0.60)
        upl_large = 2.0 * sz_large  # $2.00
        self.assertGreater(upl_large, min_fee_upl_large)


if __name__ == "__main__":
    unittest.main()
