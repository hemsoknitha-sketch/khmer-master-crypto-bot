import os
import sys
import unittest
from datetime import datetime

# Set utf-8 stdout
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

class TestSyncBrainSuperSmart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from ai_engine import AIInvestmentEngine
        cls.ai_engine = AIInvestmentEngine(api_key="mock_key_for_test")

    def test_01_get_brain_status_overview(self):
        overview = self.ai_engine.get_brain_status_overview()
        self.assertIsInstance(overview, dict)
        self.assertIn("total_artifacts", overview)
        self.assertIn("total_size_mb", overview)
        self.assertIn("ml_models_count", overview)
        self.assertIn("smart_x_models_count", overview)
        self.assertGreaterEqual(overview["total_artifacts"], 20)
        self.assertLess(overview["total_size_mb"], 15.0) # Institutional limit
        print(f"[TEST 01 PASS] Total artifacts: {overview['total_artifacts']}, Size: {overview['total_size_mb']} MB")

    def test_02_predict_quant_ml_inference(self):
        features = {
            "rsi_14": 56.5,
            "macd_hist": 8.2,
            "vol_ratio": 2.4,
            "ema_spread": 0.92,
            "volatility_atr": 1.20,
            "price_change_pct": 3.5
        }
        res = self.ai_engine.predict_quant_ml(features)
        self.assertIsInstance(res, dict)
        self.assertIn("trend", res)
        self.assertIn("confidence", res)
        self.assertIn(res["trend"], ["BULLISH", "BEARISH", "NEUTRAL"])
        print(f"[TEST 02 PASS] Quant ML Inference: Trend={res['trend']}, Confidence={res['confidence']}%")

    def test_03_smart_x_brain_integration(self):
        import smart_x_engine
        smart_x_models = list(smart_x_engine.BRAIN.models.keys())
        self.assertGreaterEqual(len(smart_x_models), 10)
        print(f"[TEST 03 PASS] SmartX Brain models in RAM: {len(smart_x_models)}")

if __name__ == "__main__":
    unittest.main()
