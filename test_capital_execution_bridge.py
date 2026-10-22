# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - CAPITAL EXECUTION BRIDGE & CVD MICROSTRUCTURE PROXY TESTS
========================================================================
Validates:
  1. CVD Microstructure Proxy calculation (Delta, Aggressor Ratio, Slope).
  2. Order flow regimes: Bullish/Bearish Aggression, Bullish/Bearish Absorption.
  3. Smart Limit Price calculation capturing the spread discount.
  4. Large Spread Limit Working Order routing trigger (spread > 1.5x avg, vol drag, adverse CVD).
  5. Active working order registry lifecycle and auto-timeout cancellation.
"""

import unittest
import time
from typing import List, Dict, Any
from capital_execution_bridge import CapitalExecutionBridge, CVDMicrostructureProxy


def _generate_synthetic_candles(n: int = 30, trend: str = "FLAT") -> List[Dict[str, Any]]:
    candles = []
    base_p = 2000.0
    for i in range(n):
        if trend == "UP":
            o = base_p + i * 2.0
            c = o + 3.0
            h = c + 1.0
            l = o - 0.5
            v = 1500.0 + i * 10
        elif trend == "DOWN":
            o = base_p - i * 2.0
            c = o - 3.0
            h = o + 0.5
            l = c - 1.0
            v = 1500.0 + i * 10
        elif trend == "BEARISH_ABSORPTION":
            o = base_p + i * 2.0
            if i >= n - 5:
                # Strong selling thrust on heavy volume after pushing up
                h = o + 8.0
                c = o - 2.5
                l = o - 3.0
                v = 6000.0
            else:
                c = o + 1.5
                h = c + 1.0
                l = o - 0.5
                v = 1000.0
        elif trend == "BULLISH_ABSORPTION":
            o = base_p - i * 2.0
            if i >= n - 5:
                # Strong buying thrust on heavy volume after pushing down
                l = o - 8.0
                c = o + 2.5
                h = o + 3.0
                v = 6000.0
            else:
                c = o - 1.5
                l = c - 1.0
                h = o + 0.5
                v = 1000.0
        else:
            o = base_p
            c = base_p + (1.0 if i % 2 == 0 else -1.0)
            h = base_p + 2.0
            l = base_p - 2.0
            v = 1000.0
        candles.append({"open": o, "high": h, "low": l, "close": c, "volume": v})
    return candles


class TestCapitalExecutionBridgeAndCVD(unittest.TestCase):

    def setUp(self):
        self.bridge = CapitalExecutionBridge(is_demo=True)
        # Mock session tokens to run unit tests offline without broker latency
        self.bridge.cst_token = "MOCK_CST_TOKEN"
        self.bridge.x_security_token = "MOCK_SECURITY_TOKEN"
        self.bridge.session_expiry = time.time() + 3600.0

        class MockResponse:
            def __init__(self, status_code=200, json_data=None):
                self.status_code = status_code
                self._json = json_data or {"dealReference": "MOCK_LIMIT_DEAL_REF_101"}
                self.text = "OK"

            def json(self):
                return self._json

        self.bridge.session.post = lambda *args, **kwargs: MockResponse(200, {"dealReference": "MOCK_LIMIT_DEAL_REF_101"})
        self.bridge.session.delete = lambda *args, **kwargs: MockResponse(204, {})

    def test_cvd_microstructure_proxy_balanced_flow(self):
        candles = _generate_synthetic_candles(n=20, trend="FLAT")
        res = CVDMicrostructureProxy.compute_cvd_microstructure(candles)
        self.assertIn("cvd_value", res)
        self.assertIn("cvd_aggressor_ratio", res)
        self.assertIn("order_flow_regime", res)
        self.assertAlmostEqual(res["cvd_aggressor_ratio"], 0.0, delta=0.25)
        self.assertEqual(res["order_flow_regime"], "BALANCED_FLOW")

    def test_cvd_microstructure_proxy_bullish_aggression(self):
        candles = _generate_synthetic_candles(n=25, trend="UP")
        res = CVDMicrostructureProxy.compute_cvd_microstructure(candles)
        self.assertGreater(res["cvd_value"], 0)
        self.assertGreater(res["cvd_aggressor_ratio"], 0.20)
        self.assertEqual(res["order_flow_regime"], "BULLISH_AGGRESSION")
        self.assertFalse(res["is_bearish_absorption"])

    def test_cvd_microstructure_proxy_bearish_absorption(self):
        candles = _generate_synthetic_candles(n=30, trend="BEARISH_ABSORPTION")
        res = CVDMicrostructureProxy.compute_cvd_microstructure(candles)
        self.assertTrue(res["is_bearish_absorption"])
        self.assertEqual(res["order_flow_regime"], "BEARISH_ABSORPTION")

    def test_cvd_microstructure_proxy_bullish_absorption(self):
        candles = _generate_synthetic_candles(n=30, trend="BULLISH_ABSORPTION")
        res = CVDMicrostructureProxy.compute_cvd_microstructure(candles)
        self.assertTrue(res["is_bullish_absorption"])
        self.assertEqual(res["order_flow_regime"], "BULLISH_ABSORPTION")

    def test_calculate_smart_limit_price(self):
        # BUY: expected 2000.0, spread 2.0, atr 10.0 -> discount = max(0.25*2, 0.05*10) = 0.50
        limit_buy = CVDMicrostructureProxy.calculate_smart_limit_price(
            direction="BUY",
            expected_price=2000.0,
            current_spread=2.0,
            atr_15m=10.0
        )
        self.assertEqual(limit_buy, 1999.50)

        # SELL: expected 2000.0, spread 2.0, atr 10.0 -> limit = 2000.50
        limit_sell = CVDMicrostructureProxy.calculate_smart_limit_price(
            direction="SELL",
            expected_price=2000.0,
            current_spread=2.0,
            atr_15m=10.0
        )
        self.assertEqual(limit_sell, 2000.50)

    def test_large_spread_routing_by_ratio(self):
        # Current spread 3.0 > 1.5 * 1.0 (avg) -> Must route as Limit Working Order
        res = self.bridge.place_smart_order_latency_aware(
            epic="GOLD",
            direction="BUY",
            size=0.1,
            expected_price=2600.0,
            current_spread=3.0,
            avg_spread=1.0,
            atr_15m=12.0
        )
        self.assertTrue(res.get("is_large_spread"))
        self.assertEqual(res.get("order_type"), "LIMIT_WORKING_ORDER")
        self.assertIn("SPREAD_RATIO_EXPANDED", res.get("large_spread_reason", ""))
        self.assertIn(res.get("deal_reference"), self.bridge._active_working_orders)

    def test_large_spread_routing_by_volatility_drag(self):
        # Current spread 1.5 <= 1.5 * 1.2 (1.8), BUT spread 1.5 >= 10% of ATR (12.0 * 0.10 = 1.20)
        res = self.bridge.place_smart_order_latency_aware(
            epic="GOLD",
            direction="BUY",
            size=0.1,
            expected_price=2600.0,
            current_spread=1.5,
            avg_spread=1.2,
            atr_15m=12.0
        )
        self.assertTrue(res.get("is_large_spread"))
        self.assertEqual(res.get("order_type"), "LIMIT_WORKING_ORDER")
        self.assertIn("VOLATILITY_SPREAD_DRAG", res.get("large_spread_reason", ""))

    def test_large_spread_routing_by_adverse_cvd(self):
        # Normal spread, but candles show BEARISH_ABSORPTION on BUY signal -> Must enforce Limit Order
        candles = _generate_synthetic_candles(n=30, trend="BEARISH_ABSORPTION")
        res = self.bridge.place_smart_order_latency_aware(
            epic="GOLD",
            direction="BUY",
            size=0.1,
            expected_price=2600.0,
            current_spread=0.5,
            avg_spread=0.5,
            atr_15m=20.0,
            candles_15m=candles
        )
        self.assertTrue(res.get("is_large_spread"))
        self.assertEqual(res.get("order_type"), "LIMIT_WORKING_ORDER")
        self.assertIn("ADVERSE_CVD_ABSORPTION", res.get("large_spread_reason", ""))
        self.assertTrue(res["cvd_microstructure"]["is_bearish_absorption"])

    def test_audit_and_purge_expired_working_orders(self):
        now = time.time()
        # Inject mock active order that is 40s old (timeout = 30s)
        self.bridge._active_working_orders["MOCK_REF_123"] = {
            "deal_reference": "MOCK_REF_123",
            "epic": "GOLD",
            "direction": "BUY",
            "size": 0.1,
            "created_at": now - 40.0,
            "timeout_seconds": 30.0,
            "status": "ACCEPTED"
        }
        # Inject mock active order that is 5s old (not expired)
        self.bridge._active_working_orders["MOCK_REF_456"] = {
            "deal_reference": "MOCK_REF_456",
            "epic": "US100",
            "direction": "BUY",
            "size": 0.05,
            "created_at": now - 5.0,
            "timeout_seconds": 30.0,
            "status": "ACCEPTED"
        }

        purged = self.bridge.audit_and_purge_expired_working_orders(timeout_seconds=30.0)
        self.assertEqual(len(purged), 1)
        self.assertEqual(purged[0]["deal_reference"], "MOCK_REF_123")
        self.assertNotIn("MOCK_REF_123", self.bridge._active_working_orders)
        self.assertIn("MOCK_REF_456", self.bridge._active_working_orders)


if __name__ == "__main__":
    unittest.main()
