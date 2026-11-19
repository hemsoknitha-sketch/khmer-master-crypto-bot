import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
import capital_engine
import importlib
qg_exec = importlib.import_module("Quant Gold.execution_engine")
QuantGoldExecutionEngine = qg_exec.QuantGoldExecutionEngine


class TestQuantGoldMultiUserDeduplication(unittest.TestCase):
    def setUp(self):
        self.engine = QuantGoldExecutionEngine()

    def test_cross_account_contamination_guard_in_capital_engine(self):
        """
        AQ88 Invariant 135: If desired_account_id is specified but active_account_id differs,
        order placement MUST be rejected with CROSS_ACCOUNT_COLLISION_BLOCKED to prevent
        host account contamination.
        """
        c_eng = capital_engine.CapitalComEngine(is_demo=False, desired_account_id="332192407263204548")
        c_eng.active_account_id = "216890638652757188"  # Host Super Admin account
        res = c_eng.execute_smart_tradfi_order(
            epic="GOLD",
            direction="BUY",
            size=0.1,
            sl=2600.0,
            tp=2620.0
        )
        self.assertFalse(res.get("success"))
        self.assertIn("CROSS_ACCOUNT_COLLISION_BLOCKED", res.get("error", ""))

    @patch("database.get_capital_auto_trades_for_user")
    @patch("database.get_active_capital_auto_users")
    @patch("capital_engine.get_user_capital_engine")
    def test_dispatch_gold_signal_broker_account_deduplication(self, mock_get_eng, mock_get_users, mock_get_trades):
        """
        AQ88 Invariant 135: When multiple VIP users in database point to the same underlying
        broker account, dispatch_gold_signal_to_fleet must ONLY place ONE order and skip duplicates.
        """
        mock_get_trades.return_value = []
        mock_get_users.return_value = [
            {"chat_id": 859271875, "budget": 50.0, "max_positions": 5, "is_demo": False},
            {"chat_id": 1744387717, "budget": 35.0, "max_positions": 5, "is_demo": False}
        ]

        mock_eng_shared = MagicMock()
        mock_eng_shared.active_account_id = "216890638652757188"
        mock_eng_shared.desired_account_id = "216890638652757188"
        mock_eng_shared.get_open_positions.return_value = []
        mock_eng_shared.execute_smart_tradfi_order.return_value = {"success": True, "deal_reference": "DEAL_1"}
        mock_eng_shared.get_account_balance.return_value = {"available": 300.0}
        mock_get_eng.return_value = mock_eng_shared

        async def run_dispatch():
            return await self.engine.dispatch_gold_signal_to_fleet(
                action="BUY",
                current_price=2650.0,
                sl=2640.0,
                tp1=2660.0,
                tp2=2675.0,
                tp3=2690.0,
                broadcast_telegram=False
            )

        fleet_res = asyncio.run(run_dispatch())
        # Exactly 1 order must have been dispatched, and the 2nd user skipped for deduplication
        self.assertEqual(fleet_res.get("dispatched_count"), 1)
        user_res = fleet_res.get("user_results", [])
        self.assertEqual(len(user_res), 2)
        successes = [r for r in user_res if r.get("success")]
        failures = [r for r in user_res if not r.get("success")]
        self.assertEqual(len(successes), 1)
        self.assertEqual(len(failures), 1)
        self.assertIn("already received order", failures[0].get("reason", ""))


if __name__ == "__main__":
    unittest.main()
