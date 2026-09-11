"""
Unit Tests for VIP Layered Wealth Protocol (70:20:10 Allocation)
================================================================
Validates:
1. Capital Allocation Mathematical Rigor (70% Core, 20% Growth, 10% Reserve).
2. Strategic Liquid Reserve Isolation & Unlocking.
3. Microstructure Orderbook Imbalance Guard.
4. 5% Global Portfolio Circuit Breaker Tripping & Freeze.
5. End-to-End Status Reporting.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database as db
from capital_orchestrator import LayeredWealthProtocolEngine
import turbo_hedge_engine
from turbo_hedge_engine import MicrostructureOrderbookGuard, GlobalPortfolioCircuitBreaker

class TestLayeredWealthProtocol(unittest.TestCase):
    def setUp(self):
        self.test_chat_id = 999999999
        # Clean test state
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_active", "0")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_reserve_alloc", "0.0")
        db.update_system_setting(f"turbo_hedge_circuit_breaker_{self.test_chat_id}", "0")
        db.update_system_setting(f"turbo_hedge_cb_time_{self.test_chat_id}", "0")

    def tearDown(self):
        # Clean up
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_active", "0")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_reserve_alloc", "0.0")
        db.update_system_setting(f"turbo_hedge_circuit_breaker_{self.test_chat_id}", "0")

    def test_01_math_allocation_split(self):
        """Test exact 70:20:10 ratio calculation"""
        # Test $100 capital
        layers100 = LayeredWealthProtocolEngine.calculate_wealth_layers(100.0)
        self.assertAlmostEqual(layers100["core_layer_usd"], 70.0, places=2)
        self.assertAlmostEqual(layers100["growth_layer_usd"], 20.0, places=2)
        self.assertAlmostEqual(layers100["strategic_reserve_usd"], 10.0, places=2)
        self.assertAlmostEqual(layers100["total_capital"], 100.0, places=2)

        # Test $500 capital
        layers500 = LayeredWealthProtocolEngine.calculate_wealth_layers(500.0)
        self.assertAlmostEqual(layers500["core_layer_usd"], 350.0, places=2)
        self.assertAlmostEqual(layers500["growth_layer_usd"], 100.0, places=2)
        self.assertAlmostEqual(layers500["strategic_reserve_usd"], 50.0, places=2)

        # Test sum invariance
        for cap in [25.0, 77.77, 1250.0]:
            l = LayeredWealthProtocolEngine.calculate_wealth_layers(cap)
            total = l["core_layer_usd"] + l["growth_layer_usd"] + l["strategic_reserve_usd"]
            self.assertAlmostEqual(total, cap, places=2)

    def test_02_strategic_reserve_lock_and_unlock(self):
        """Test locking 10% reserve and isolating from deployable balance"""
        # Lock $25 reserve
        LayeredWealthProtocolEngine.lock_strategic_reserve(self.test_chat_id, 25.0)
        locked = LayeredWealthProtocolEngine.get_locked_reserve(self.test_chat_id)
        self.assertEqual(locked, 25.0)

        # Deployable capital out of $100 total should be $75
        deployable = LayeredWealthProtocolEngine.get_deployable_capital_excluding_reserve(self.test_chat_id, 100.0)
        self.assertEqual(deployable, 75.0)

        # Unlock reserve
        LayeredWealthProtocolEngine.unlock_strategic_reserve(self.test_chat_id)
        locked_after = LayeredWealthProtocolEngine.get_locked_reserve(self.test_chat_id)
        self.assertEqual(locked_after, 0.0)
        deployable_after = LayeredWealthProtocolEngine.get_deployable_capital_excluding_reserve(self.test_chat_id, 100.0)
        self.assertEqual(deployable_after, 100.0)

    def test_03_orderbook_imbalance_guard(self):
        """Test L2 orderbook imbalance microstructure evaluation"""
        # Normal evaluation on BTCUSDT or fallback
        guard = MicrostructureOrderbookGuard.evaluate_orderbook_microstructure("BTCUSDT")
        self.assertIn("symbol", guard)
        self.assertIn("imbalance_ratio", guard)
        self.assertIn("high_ev_signal", guard)
        self.assertIn(guard["high_ev_signal"], ["BUY", "SELL", "NEUTRAL"])
        self.assertGreater(guard["imbalance_ratio"], 0.0)

    def test_04_circuit_breaker_trip_and_freeze(self):
        """Test 5% drawdown circuit breaker trigger and 24h freeze"""
        # Initially circuit breaker is normal
        cb_init = GlobalPortfolioCircuitBreaker.check_circuit_breaker(self.test_chat_id, 100.0)
        self.assertFalse(cb_init["is_tripped"])

        # Simulate setting circuit breaker tripped manually
        db.update_system_setting(f"turbo_hedge_circuit_breaker_{self.test_chat_id}", "1")
        import time
        db.update_system_setting(f"turbo_hedge_cb_time_{self.test_chat_id}", str(time.time()))

        cb_tripped = GlobalPortfolioCircuitBreaker.check_circuit_breaker(self.test_chat_id, 100.0)
        self.assertTrue(cb_tripped["is_tripped"])
        self.assertEqual(cb_tripped["reason"], "CIRCUIT_BREAKER_ACTIVE_24H_FREEZE")

        # Reset circuit breaker
        GlobalPortfolioCircuitBreaker.reset_circuit_breaker(self.test_chat_id)
        cb_reset = GlobalPortfolioCircuitBreaker.check_circuit_breaker(self.test_chat_id, 100.0)
        self.assertFalse(cb_reset["is_tripped"])

    def test_05_layered_wealth_status_reporting(self):
        """Test full protocol status introspection"""
        # Activate protocol settings in DB
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_active", "1")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_total_capital", "200.0")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_core_alloc", "140.0")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_growth_alloc", "40.0")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_reserve_alloc", "20.0")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_core_sym", "PAXGUSDT")
        db.update_system_setting(f"turbo_hedge_wealth_{self.test_chat_id}_growth_sym", "BTCUSDT")

        status = turbo_hedge_engine.get_layered_wealth_status(self.test_chat_id)
        self.assertTrue(status["is_active"])
        self.assertEqual(status["total_capital"], 200.0)
        self.assertEqual(status["core_alloc"], 140.0)
        self.assertEqual(status["growth_alloc"], 40.0)
        self.assertEqual(status["reserve_alloc"], 20.0)
        self.assertEqual(status["core_symbol"], "PAXGUSDT")
        self.assertEqual(status["growth_symbol"], "BTCUSDT")
        self.assertIn("circuit_breaker", status)

if __name__ == "__main__":
    unittest.main()
