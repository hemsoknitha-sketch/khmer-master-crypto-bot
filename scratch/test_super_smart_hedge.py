import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import turbo_hedge_engine
import trading_engine

def test_hedge_consensus():
    print("Testing evaluate_smart_hedge_consensus...")
    for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]:
        ev = turbo_hedge_engine.evaluate_smart_hedge_consensus(sym)
        print(f"[{sym}] Price: ${ev['price']:,.2f} | Funding: {ev['funding_rate_pct']:+.4f}% | APR: {ev['annualized_apr']:+.2f}% | Action: {ev['action']} | Score: {ev['score']}")
        assert "action" in ev
        assert "score" in ev
        assert "confidence_pct" in ev
    
    # Test for $20 capital (should choose SOL, ETH, or BNB because BTC requires ~$78 min contract)
    best_20 = turbo_hedge_engine.get_best_hedge_coin(20.0)
    print(f"Best Hedge Coin for $20: {best_20}")
    assert best_20 in ["SOLUSDT", "ETHUSDT", "BNBUSDT"]
    
    # Test for $100 capital (BTC is allowed)
    best_100 = turbo_hedge_engine.get_best_hedge_coin(100.0)
    print(f"Best Hedge Coin for $100: {best_100}")
    assert best_100 in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
    print("PASS: evaluate_smart_hedge_consensus & get_best_hedge_coin")

def test_delta_neutral_math():
    print("\nTesting Delta-Neutral sizing math for $20 capital...")
    # Test $20 capital on SOLUSDT
    sol_price = trading_engine.get_current_price("SOLUSDT")
    if sol_price <= 0: sol_price = 100.0
    amount_usdt = 20.0
    eff_amount = max(10.50, amount_usdt)
    spot_qty = eff_amount / sol_price
    futures_qty = trading_engine.get_futures_max_sellable_qty("SOLUSDT", spot_qty)
    delta = spot_qty - futures_qty
    print(f"[SOLUSDT] Amount: ${eff_amount:.2f} | Price: ${sol_price:.2f} | Spot Qty: {spot_qty:.4f} | Futures Qty: {futures_qty:.4f} | Delta: {delta:.4f}")
    assert futures_qty > 0
    assert abs(delta) < 0.05

    # Test $100 capital on BTCUSDT
    print("\nTesting Delta-Neutral sizing math for $100 capital on BTCUSDT...")
    btc_price = trading_engine.get_current_price("BTCUSDT")
    if btc_price <= 0: btc_price = 78000.0
    btc_amount = 100.0
    btc_spot_qty = btc_amount / btc_price
    btc_futures_qty = trading_engine.get_futures_max_sellable_qty("BTCUSDT", btc_spot_qty)
    btc_delta = btc_spot_qty - btc_futures_qty
    print(f"[BTCUSDT] Amount: ${btc_amount:.2f} | Price: ${btc_price:.2f} | Spot Qty: {btc_spot_qty:.6f} | Futures Qty: {btc_futures_qty:.6f} | Delta: {btc_delta:.6f}")
    assert btc_futures_qty > 0
    assert abs(btc_delta) < 0.001

    # Test that $20 on BTCUSDT returns the protective lot size error cleanly
    print("\nTesting protective LOT_SIZE check for $20 on BTCUSDT...")
    res = turbo_hedge_engine.execute_super_delta_neutral_hedge("dummy_key", "dummy_secret", "BTCUSDT", 20.0, leverage=1)
    print(f"BTC $20 Guard Result: {res.get('reason')} - {res.get('msg')}")
    assert res.get("status") == "error"
    assert res.get("reason") == "AMOUNT_BELOW_MIN_LOT_SIZE"

    print("PASS: Delta-Neutral sizing math & safety guards")

if __name__ == "__main__":
    test_hedge_consensus()
    test_delta_neutral_math()
    print("\nALL SUPER SMART HEDGE TESTS PASSED 100%!")
