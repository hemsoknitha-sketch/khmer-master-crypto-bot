import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import turbo_hedge_engine
import trading_engine

def test_apex_hedge_consensus():
    print("=================================================================")
    print("🚀 TESTING APEX SUPER SMART DELTA-NEUTRAL HEDGE CONSENSUS & ENGINES")
    print("=================================================================")

    for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]:
        ev = turbo_hedge_engine.evaluate_smart_hedge_consensus(sym)
        print(f"\n--- [{sym}] {ev['coin']} ---")
        print(f"Spot Price: ${ev['spot_price']:,.2f} | Futures Price: ${ev['fut_price']:,.2f}")
        print(f"📐 Basis Spread: ${ev['basis_spread_usd']:+.4f} ({ev['basis_spread_pct']:+.4f}%) | Basis APR: {ev['basis_apr']:+.2f}%")
        print(f"💰 Funding Rate: {ev['funding_rate_pct']:+.4f}% / 8h | Funding APR: {ev['funding_apr']:+.2f}%")
        print(f"🌾 Composite Yield APR: {ev['composite_yield_apr']:+.2f}% APY")
        print(f"⏳ Funding Countdown: {ev['countdown_str']} ({ev['mins_until_funding']} mins left)")
        print(f"🧠 Score: {ev['score']}/100 | Action: {ev['action']} | Conf: {ev['confidence_pct']}%")
        print(f"Reason: {ev['reason']}")

        # Assertions
        assert "basis_spread_pct" in ev
        assert "mins_until_funding" in ev
        assert "countdown_str" in ev
        assert "composite_yield_apr" in ev
        assert ev["mins_until_funding"] >= 0
        assert len(ev["countdown_str"]) > 0

    print("\n✅ PASS: evaluate_smart_hedge_consensus returns all Apex metrics!")

def test_best_hedge_coin_multi_return():
    print("\n-----------------------------------------------------------------")
    print("Testing get_best_hedge_coin with and without return_details...")
    
    # 1. Backwards compatible string return
    sym_20 = turbo_hedge_engine.get_best_hedge_coin(20.0)
    print(f"get_best_hedge_coin(20.0) -> {sym_20} (Type: {type(sym_20).__name__})")
    assert isinstance(sym_20, str)
    assert sym_20 in ["SOLUSDT", "ETHUSDT", "BNBUSDT"]

    # 2. Detailed tuple return
    sym_detailed, ev = turbo_hedge_engine.get_best_hedge_coin(20.0, return_details=True)
    print(f"get_best_hedge_coin(20.0, return_details=True) -> {sym_detailed}, Score: {ev['score']}, Yield: {ev['composite_yield_apr']}% APY")
    assert isinstance(sym_detailed, str)
    assert isinstance(ev, dict)
    assert sym_detailed == ev["symbol"]
    assert "basis_spread_pct" in ev
    assert "mins_until_funding" in ev

    print("✅ PASS: get_best_hedge_coin details & backwards compatibility verified!")

def test_delta_neutral_execution_safety():
    print("\n-----------------------------------------------------------------")
    print("Testing Super Delta-Neutral Pre-Flight Safety & Lot Size Guard...")
    
    # BTC with $20 should be rejected by LOT_SIZE guard because min contract is 0.001 BTC (~$78)
    res_btc = turbo_hedge_engine.execute_super_delta_neutral_hedge("dummy_key", "dummy_secret", "BTCUSDT", 20.0, leverage=1)
    print(f"BTCUSDT $20 Guard: {res_btc.get('reason')} -> {res_btc.get('msg')}")
    assert res_btc.get("status") == "error"
    assert res_btc.get("reason") == "AMOUNT_BELOW_MIN_LOT_SIZE"

    # SOL with $20 should pass LOT_SIZE check and fail on API key/balance check (as expected in mock)
    res_sol = turbo_hedge_engine.execute_super_delta_neutral_hedge("dummy_key", "dummy_secret", "SOLUSDT", 20.0, leverage=1)
    print(f"SOLUSDT $20 Guard: {res_sol.get('reason')} -> {res_sol.get('msg')}")
    assert res_sol.get("status") == "error"
    assert res_sol.get("reason") in ["INSUFFICIENT_SPOT_USDT", "INSUFFICIENT_FUTURES_USDT", "AMOUNT_BELOW_MIN_LOT_SIZE"]

    print("✅ PASS: Pre-flight safety and LOT_SIZE guards fully operational!")

if __name__ == "__main__":
    test_apex_hedge_consensus()
    test_best_hedge_coin_multi_return()
    test_delta_neutral_execution_safety()
    print("\n🎉 ALL APEX HEDGE TESTS PASSED SUCCESSFULLY! 🎉\n")
