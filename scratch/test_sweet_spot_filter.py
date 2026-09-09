import os
import sys
import unittest
from unittest.mock import patch, MagicMock

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import turbo_hedge_engine

class TestEarlyBreakoutSweetSpotFilter(unittest.TestCase):
    def test_01_futures_scanner_rejects_overextended_coins(self):
        # Mock /fapi/v1/ticker/24hr
        mock_tickers = [
            {"symbol": "IOSTUSDT", "quoteVolume": "15000000.0", "priceChangePercent": "38.5"},   # > +20% => MUST BE SKIPPED
            {"symbol": "FORMUSDT", "quoteVolume": "25000000.0", "priceChangePercent": "45.0"},   # > +20% => MUST BE SKIPPED
            {"symbol": "FFUSDT",   "quoteVolume": "12000000.0", "priceChangePercent": "-28.0"},  # < -20% => MUST BE SKIPPED
            {"symbol": "XANUSDT",  "quoteVolume": "18000000.0", "priceChangePercent": "31.2"},   # > +20% => MUST BE SKIPPED
            {"symbol": "BORINGUSDT", "quoteVolume": "20000000.0", "priceChangePercent": "1.2"},  # < 2.5% => MUST BE SKIPPED
            {"symbol": "SWEET1USDT", "quoteVolume": "30000000.0", "priceChangePercent": "5.5"},  # In sweet-spot (5.5%) => MUST BE ACCEPTED
            {"symbol": "SWEET2USDT", "quoteVolume": "25000000.0", "priceChangePercent": "8.0"},  # In sweet-spot (8.0%) => MUST BE ACCEPTED
            {"symbol": "SWEET3USDT", "quoteVolume": "20000000.0", "priceChangePercent": "11.5"}, # In sweet-spot (11.5%) => MUST BE ACCEPTED
        ]

        with patch("trading_engine.HFT_SESSION.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = mock_tickers
            mock_get.return_value = mock_resp

            with patch("trading_engine.get_futures_symbol_info") as mock_info:
                mock_info.return_value = {"status": "TRADING"}
                results = turbo_hedge_engine.get_active_high_velocity_coins(limit=10)

                # IOST, FORM, FF, XAN, BORING must NEVER be in results
                self.assertNotIn("IOSTUSDT", results)
                self.assertNotIn("FORMUSDT", results)
                self.assertNotIn("FFUSDT", results)
                self.assertNotIn("XANUSDT", results)
                self.assertNotIn("BORINGUSDT", results)

                # Sweet spot coins must be returned
                self.assertIn("SWEET1USDT", results)
                self.assertIn("SWEET2USDT", results)
                self.assertIn("SWEET3USDT", results)

    def test_02_spot_scanner_rejects_overextended_coins(self):
        mock_tickers = [
            {"symbol": "PUMP1USDT", "quoteVolume": "10000000.0", "priceChangePercent": "28.5"},   # > +20% => SKIP
            {"symbol": "DUMP1USDT", "quoteVolume": "10000000.0", "priceChangePercent": "-25.0"},  # < -20% => SKIP
            {"symbol": "FLAT1USDT", "quoteVolume": "10000000.0", "priceChangePercent": "1.0"},    # < 2.5% => SKIP
            {"symbol": "ALPHAUSDT", "quoteVolume": "15000000.0", "priceChangePercent": "6.8"},    # Sweet-spot => KEEP
        ]

        with patch("trading_engine.HFT_SESSION.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = mock_tickers
            mock_get.return_value = mock_resp

            with patch("trading_engine.get_symbol_info") as mock_info:
                mock_info.return_value = {"status": "TRADING", "isSpotTradingAllowed": True, "tags": []}
                results = turbo_hedge_engine.get_active_high_velocity_spot_coins(limit=10)

                self.assertNotIn("PUMP1USDT", results)
                self.assertNotIn("DUMP1USDT", results)
                self.assertNotIn("FLAT1USDT", results)
                self.assertIn("ALPHAUSDT", results)

    def test_03_scan_and_evaluate_symbol_anti_fomo_guard(self):
        # Test direct call with an overextended symbol > +20%
        with patch("trading_engine.HFT_SESSION.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"symbol": "IOSTUSDT", "priceChangePercent": "35.0"}
            mock_get.return_value = mock_resp

            res = turbo_hedge_engine.scan_and_evaluate_symbol("IOSTUSDT")
            self.assertEqual(res["side"], "SKIP")
            self.assertEqual(res["reason"], "OVEREXTENDED_PUMP_PEAK")

        # Test direct call with a collapsing symbol < -20%
        with patch("trading_engine.HFT_SESSION.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"symbol": "DUMPUSDT", "priceChangePercent": "-27.0"}
            mock_get.return_value = mock_resp

            res = turbo_hedge_engine.scan_and_evaluate_symbol("DUMPUSDT")
            self.assertEqual(res["side"], "SKIP")
            self.assertEqual(res["reason"], "OVEREXTENDED_DUMP_BOTTOM")

if __name__ == "__main__":
    unittest.main()
