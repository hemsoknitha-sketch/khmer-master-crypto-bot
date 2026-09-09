import os
import sys
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import database as db
import smart_x_engine

class TestSmartXDbFix(unittest.TestCase):
    def test_01_api_keys_aliases(self):
        # Verify get_user_api, get_api_keys, and get_user_api_keys are identical callables
        self.assertEqual(db.get_api_keys, db.get_user_api)
        self.assertEqual(db.get_user_api_keys, db.get_user_api)
        res1 = db.get_user_api(999999999)
        res2 = db.get_user_api_keys(999999999)
        res3 = db.get_api_keys(999999999)
        self.assertEqual(res1, res2)
        self.assertEqual(res2, res3)

    def test_02_active_trades_alias(self):
        self.assertEqual(db.get_active_trades, db.get_active_trades_by_user)
        trades = db.get_active_trades(999999999)
        self.assertIsInstance(trades, list)

    def test_03_helper_functions(self):
        symbols = db.get_all_active_symbols(999999999)
        self.assertIsInstance(symbols, list)
        
        cfg = db.get_user_config(999999999, "auto_trade")
        self.assertTrue(cfg is None or isinstance(cfg, dict))

        db.set_defender_active(True)
        db.set_defender_active(False)

        db.update_trade_entry_price(999999999, "BTCUSDT", 65000.0)
        db.update_compound_grid_state(999999999, 10.0, 5.0, 100.0)
        db.delete_user_api(999999999)

    def test_04_delta_neutral_bot_cycle(self):
        db.add_delta_neutral_bot(999999999, "TESTUSDT", 50.0, 0.5, 0.5)
        user_bots = db.get_user_delta_neutral_bots(999999999)
        self.assertGreaterEqual(len(user_bots), 1)
        self.assertEqual(user_bots[0]["symbol"], "TESTUSDT")
        
        # Stop test bot
        db.stop_delta_neutral_bot(user_bots[0]["id"])
        remaining = db.get_user_delta_neutral_bots(999999999)
        self.assertEqual(len(remaining), 0)

    def test_05_smart_x_futures_execution_no_attribute_error(self):
        # Calling with dummy chat_id should return clean message, NOT raise AttributeError
        res = smart_x_engine.execute_smart_x_futures(
            chat_id=999999999,
            symbol="BTCUSDT",
            amount_usdt=10.0,
            leverage=5
        )
        self.assertIsInstance(res, dict)
        self.assertIn("status", res)
        self.assertEqual(res["status"], "error")
        # Ensure it failed gracefully on missing API keys or macro guard, NOT AttributeError
        self.assertIn("Binance API Keys missing", res["message"])

if __name__ == "__main__":
    unittest.main()
