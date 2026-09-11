import sys
import os
import unittest

sys.path.insert(0, os.path.abspath("."))

class TestSmartXSonicGold(unittest.TestCase):
    def setUp(self):
        import smart_x_engine
        self.engine = smart_x_engine

    def test_01_brain_models_loaded(self):
        brain = self.engine.BRAIN
        models = brain.models
        print(f"\n[TEST 01] Loaded Models in RAM: {len(models)}")
        self.assertGreaterEqual(len(models), 10, "Brain should have loaded core models into RAM")
        self.assertIn("moe_router", models)
        self.assertIn("pinn_jump_diff", models)
        print("  -> Brain models loaded successfully!")

    def test_02_sonic_session_clock(self):
        session_info = self.engine.SonicGoldScalper.get_current_session_window()
        print(f"[TEST 02] Session Clock: {session_info['session_name']} (UTC Hour: {session_info['utc_hour']}, DeadZone: {session_info['is_dead_zone']})")
        self.assertIn("session_name", session_info)
        self.assertIn("liquidity_score", session_info)
        print("  -> Session clock evaluated successfully!")

    def test_03_asian_range_sweeps(self):
        sweep = self.engine.SonicGoldScalper.analyze_asian_range_sweeps("PAXGUSDT")
        print(f"[TEST 03] Asian Sweep: {sweep['signal']} (Type: {sweep['type']}, Asian High: {sweep['asian_high']}, Asian Low: {sweep['asian_low']})")
        self.assertIn("signal", sweep)
        self.assertIn("type", sweep)
        print("  -> Asian range sweeps evaluated successfully!")

    def test_04_macro_event_guard(self):
        macro = self.engine.MacroEventNLPGuard.check_macro_guard()
        print(f"[TEST 04] Macro Event Guard: Frozen={macro['is_frozen']}, MaxLev={macro['max_allowed_leverage']}")
        self.assertIn("is_frozen", macro)
        self.assertIn("max_allowed_leverage", macro)
        print("  -> Macro Event Guard evaluated successfully!")

    def test_05_adaptive_kelly_risk_guard(self):
        plan_small = self.engine.AdaptiveKellyDrawdownGuard.calculate_optimal_gold_position(
            account_balance=80.0,
            current_price=2650.0
        )
        print(f"[TEST 05a] Sub-$100 Account ($80): Trade=${plan_small['allocated_trade_usd']}, Lev={plan_small['recommended_leverage']}x")
        self.assertLessEqual(plan_small['recommended_leverage'], 10, "Invariant 8: sub-$100 leverage must be <= 10x")
        self.assertGreaterEqual(plan_small['allocated_trade_usd'], 10.50, "Invariant 1: MIN_NOTIONAL floor")

        plan_large = self.engine.AdaptiveKellyDrawdownGuard.calculate_optimal_gold_position(
            account_balance=6000.0,
            current_price=2650.0
        )
        print(f"[TEST 05b] SONIC Account ($6,000): Trade=${plan_large['allocated_trade_usd']}, MaxDD Limit=${plan_large['max_daily_drawdown_limit_usd']}")
        self.assertLessEqual(plan_large['recommended_leverage'], 30, "SONIC leverage capped at 1:30")
        print("  -> Adaptive Kelly and small capital clamp passed!")

    def test_06_gold_signal_synthesis(self):
        sig = self.engine.SmartXEngine.generate_smart_x_signal("PAXGUSDT")
        print(f"[TEST 06] Gold Signal: {sig['side']} ({sig['confidence_pct']}% Conf) Strategy: {sig['strategy']}")
        self.assertIn("side", sig)
        self.assertIn("confidence_pct", sig)
        self.assertIn("sonic_benchmarks", sig)
        bench = sig["sonic_benchmarks"]
        self.assertEqual(bench["target_win_rate"], "87.12%")
        self.assertEqual(bench["target_max_dd"], "0.26%")
        print("  -> Signal synthesis with SONIC benchmarks verified!")

    def test_07_central_bank_sge_radar(self):
        import central_bank_gold_radar
        sge = central_bank_gold_radar.fetch_sge_lbma_premium()
        print(f"[TEST 07] SGE Premium: +${sge.get('sge_premium_usdt')}/oz | PBOC: {sge.get('pboc_status')}")
        self.assertIn("sge_premium_usdt", sge)
        self.assertIn("pboc_status", sge)
        print("  -> Central Bank SGE Radar verified!")

    def test_08_macro_gold_engine(self):
        import macro_gold_engine
        macro = macro_gold_engine.fetch_macro_gold_indicators()
        print(f"[TEST 08] DXY: {macro.get('dxy_index')} | 10Y Real Yield: {macro.get('real_yield_10y')}%")
        self.assertIn("dxy_index", macro)
        self.assertIn("real_yield_10y", macro)
        print("  -> Macro Gold Engine verified!")

    def test_09_black_swan_safe_haven_guard(self):
        import black_swan_gold_guard
        res = black_swan_gold_guard.PAXGGoldSafeHavenSwitcherEngine().scan_geopolitical_black_swan()
        print(f"[TEST 09] Safe Haven: Crisis={res.get('crisis_detected')}, Action={res.get('action_signal')}")
        self.assertIn("crisis_detected", res)
        self.assertIn("action_signal", res)
        print("  -> Black Swan Safe Haven Guard verified!")

if __name__ == "__main__":
    unittest.main()
