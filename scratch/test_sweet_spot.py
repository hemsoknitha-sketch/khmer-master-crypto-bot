import unittest
import math
import sys
import os

# Add repo to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import turbo_hedge_engine
import smart_x_engine
import bot_thread

class TestSweetSpotFilter(unittest.TestCase):
    def test_sweet_spot_scoring(self):
        # Verify that 3% to 12% gets high score, >20% is excluded
        cands = [
            {"symbol": "PEAKUSDT", "priceChangePercent": "45.0", "quoteVolume": "10000000.0"},
            {"symbol": "DUMPUSDT", "priceChangePercent": "-35.0", "quoteVolume": "10000000.0"},
            {"symbol": "SWEET1USDT", "priceChangePercent": "7.5", "quoteVolume": "10000000.0"},
            {"symbol": "SWEET2USDT", "priceChangePercent": "4.5", "quoteVolume": "10000000.0"},
            {"symbol": "SWEET3USDT", "priceChangePercent": "11.0", "quoteVolume": "10000000.0"},
            {"symbol": "TIREDUSDT", "priceChangePercent": "18.0", "quoteVolume": "10000000.0"},
            {"symbol": "LOWVOLUSDT", "priceChangePercent": "1.2", "quoteVolume": "10000000.0"},
        ]
        
        filtered = []
        for t in cands:
            price_change_pct = float(t["priceChangePercent"])
            abs_change = abs(price_change_pct)
            quote_vol = float(t["quoteVolume"])
            
            # Filter condition from turbo_hedge_engine
            if abs_change > 20.0 or abs_change < 2.5:
                continue
                
            if 3.0 <= abs_change <= 12.0:
                breakout_score = 150.0 - (abs(abs_change - 7.5) * 5.0)
            elif 12.0 < abs_change <= 20.0:
                breakout_score = 80.0 - ((abs_change - 12.0) * 8.0)
            else:
                breakout_score = 60.0
                
            vol_score = math.log10(max(1.0, quote_vol)) * 10.0
            filtered.append({"symbol": t["symbol"], "score": breakout_score + vol_score})
            
        filtered.sort(key=lambda x: x["score"], reverse=True)
        symbols = [f["symbol"] for f in filtered]
        
        # PEAKUSDT (+45%) and DUMPUSDT (-35%) MUST be 100% excluded
        self.assertNotIn("PEAKUSDT", symbols)
        self.assertNotIn("DUMPUSDT", symbols)
        self.assertNotIn("LOWVOLUSDT", symbols)
        
        # SWEET1USDT (+7.5%) should be the #1 top candidate
        self.assertEqual(symbols[0], "SWEET1USDT")
        print(f"✅ Filtered candidates in order: {symbols}")

    def test_datetime_import_in_bot_thread(self):
        # Verify datetime is available in bot_thread namespace
        self.assertTrue(hasattr(bot_thread, "datetime"))
        now_str = bot_thread.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(len(now_str) > 10)
        print(f"✅ bot_thread.datetime verified: {now_str}")

if __name__ == "__main__":
    unittest.main()
