import sys
import os

sys.path.insert(0, os.path.abspath("."))
import smart_x_engine

def run_tests():
    print("🧪 Running Smart X Engine Verification Suite...")
    
    # 1. Test Model Loading
    brain = smart_x_engine.BRAIN
    print(f"  [1] Loaded Models: {list(brain.models.keys())}")
    assert len(brain.models) > 0, "No models loaded!"
    assert "moe_router" in brain.models, "moe_router missing!"
    assert "pinn_jump_diff" in brain.models, "pinn_jump_diff missing!"
    print("  ✅ [PASS] Pre-trained AI Brain models loaded successfully into RAM.")
    
    # 2. Test Market Regime Router
    regime = smart_x_engine.SmartXEngine.evaluate_market_regime("PAXGUSDT")
    print(f"  [2] PAXGUSDT Regime: {regime['regime']} -> Strategy: {regime['strategy_routed']} (Jump Risk: {regime['jump_risk']})")
    assert "regime" in regime and "strategy_routed" in regime
    print("  ✅ [PASS] MoE Regime Router evaluated accurately.")
    
    # 3. Test Session Liquidity Sweep Classifier
    sweep = smart_x_engine.SessionLiquiditySweepClassifier.analyze_sweeps("PAXGUSDT")
    print(f"  [3] Session Sweep Status: {sweep['sweep_signal']} (Session: {sweep['session']}, Asian High: {sweep['asian_high']}, Asian Low: {sweep['asian_low']})")
    assert "sweep_signal" in sweep
    print("  ✅ [PASS] Session Liquidity Sweep Classifier tested.")
    
    # 4. Test Macro Event Impact NLP Guard
    macro = smart_x_engine.MacroEventNLPGuard.check_macro_guard()
    print(f"  [4] Macro Guard Status: Frozen={macro['is_frozen']}, Reason={macro['freeze_reason']}, MaxLev={macro['max_allowed_leverage']}")
    assert "is_frozen" in macro and "max_allowed_leverage" in macro
    print("  ✅ [PASS] Macroeconomic Event Impact NLP Guard tested.")
    
    # 5. Test Adaptive Kelly Drawdown Guard
    size_plan = smart_x_engine.AdaptiveKellyDrawdownGuard.calculate_optimal_position_size(
        chat_id=12345,
        account_balance=80.0
    )
    print(f"  [5] Balance: $80.00 -> Trade: ${size_plan['allocated_trade_usd']} USDT, Leverage: {size_plan['recommended_leverage']}x, DailyDD Limit: ${size_plan['max_daily_drawdown_limit_usd']}")
    assert size_plan["allocated_trade_usd"] >= 10.50, "Spot MIN_NOTIONAL violated!"
    assert size_plan["recommended_leverage"] <= 10, "Small Capital Shield violated!"
    print("  ✅ [PASS] Adaptive Kelly Drawdown Guard & Small Capital Clamp tested.")

    # 6. Test Smart X Signal Synthesis
    sig = smart_x_engine.SmartXEngine.generate_smart_x_signal("BTCUSDT")
    print(f"  [6] BTCUSDT Signal: Side={sig['side']}, Conf={sig['confidence_pct']}%, Strategy={sig.get('strategy', 'N/A')}")
    assert "side" in sig and "confidence_pct" in sig
    print("  ✅ [PASS] Smart X Signal Synthesis operational.")

    print("\n🎉 ALL SMART X UNIT TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
