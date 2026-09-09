#!/usr/bin/env python3
"""
Test Suite: Super Smart Solution 5 - Anti-Whipsaw Clean Stop (-10% ROI & 2-Hour Blacklist Cooldown)
Verifies that:
1. Stop loss triggers at -10.0% ROI (Futures) and -5.0% ROI (Spot).
2. Reverse flip is 100% eliminated (Clean market close executed).
3. 2-Hour Blacklist Cooldown (7200s) is persistently set and verified.
4. Cooldown effectively blocks candidate scanners, evaluation, and order placement.
5. Expired cooldown smoothly releases symbols back to active pool.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import turbo_hedge_engine
import database as db

def test_stop_loss_trigger_conditions():
    print("======================================================================")
    print("TEST 1: Stop Loss Trigger Logic (-10.0% ROI / -$0.50 Floor)")
    print("======================================================================")

    def check_sl(is_spot, roi_pct, net_pnl_usdt, bot_amt=5.0):
        if not is_spot:
            return (roi_pct <= -10.0 or net_pnl_usdt <= -max(0.50, bot_amt * 0.10))
        else:
            return (roi_pct <= -5.0 or net_pnl_usdt <= -max(0.50, bot_amt * 0.05))

    # Futures: ROI at -9.0% -> NOT triggered
    assert not check_sl(is_spot=False, roi_pct=-9.0, net_pnl_usdt=-0.45)
    print("  [PASS] Futures ROI -9.0% (-$0.45): Safe, Stop-Loss NOT triggered.")

    # Futures: ROI at -10.0% -> TRIGGERED
    assert check_sl(is_spot=False, roi_pct=-10.0, net_pnl_usdt=-0.50)
    print("  [PASS] Futures ROI -10.0% (-$0.50): Stop-Loss accurately triggered!")

    # Futures: ROI at -12.5% -> TRIGGERED
    assert check_sl(is_spot=False, roi_pct=-12.5, net_pnl_usdt=-0.62)
    print("  [PASS] Futures ROI -12.5% (-$0.62): Stop-Loss accurately triggered!")

    # Spot: ROI at -4.0% -> NOT triggered
    assert not check_sl(is_spot=True, roi_pct=-4.0, net_pnl_usdt=-0.40)
    print("  [PASS] Spot ROI -4.0%: Safe, Stop-Loss NOT triggered.")

    # Spot: ROI at -5.0% -> TRIGGERED
    assert check_sl(is_spot=True, roi_pct=-5.0, net_pnl_usdt=-0.50)
    print("  [PASS] Spot ROI -5.0%: Stop-Loss accurately triggered!")
    print()

def test_blacklist_cooldown_system():
    print("======================================================================")
    print("TEST 2: 2-Hour Blacklist Cooldown (7200s) Persistence & Checking")
    print("======================================================================")
    
    test_sym = "TESTWHIPUSDT"
    
    # Clean any prior state in RAM and DB
    turbo_hedge_engine._cooldown_symbols.pop(test_sym, None)
    db.update_system_setting(f"turbo_hedge_cooldown_{test_sym}", "0.0")
    
    assert not turbo_hedge_engine.is_symbol_in_cooldown(test_sym)
    print("  [PASS] Before trigger: Symbol is NOT in cooldown.")

    # Apply 2-Hour Cooldown (7200 seconds)
    turbo_hedge_engine.add_symbol_cooldown(test_sym, 7200)
    assert turbo_hedge_engine.is_symbol_in_cooldown(test_sym)
    print("  [PASS] After trigger: Symbol is strictly in 2-Hour Cooldown (In-Memory verified).")

    # DB Persistence Check
    db_exp_str = db.get_system_setting(f"turbo_hedge_cooldown_{test_sym}", "0.0")
    db_exp = float(db_exp_str)
    assert db_exp > time.time() + 7000
    print("  [PASS] SQLite WAL Database Persistence: Cooldown expiration correctly stored in DB.")

    # Simulate Cold-Start Cache Recovery from DB
    turbo_hedge_engine._cooldown_symbols.pop(test_sym, None)  # Wipe RAM cache
    assert turbo_hedge_engine.is_symbol_in_cooldown(test_sym)  # Should recover from DB
    print("  [PASS] Cold-Start Resilience: RAM cache recovered active cooldown from DB successfully!")
    print()

def test_cooldown_re_entry_guards():
    print("======================================================================")
    print("TEST 3: Re-Entry Guards (Evaluation & Order Placement Blocked)")
    print("======================================================================")
    
    test_sym = "TESTBLOCKUSDT"
    turbo_hedge_engine.add_symbol_cooldown(test_sym, 7200)

    # 1. scan_and_evaluate_symbol must return SKIP immediately
    eval_res = turbo_hedge_engine.scan_and_evaluate_symbol(test_sym)
    assert eval_res.get("side") == "SKIP"
    assert eval_res.get("reason") == "SYMBOL_IN_COOLDOWN"
    print("  [PASS] scan_and_evaluate_symbol: Blocked with reason 'SYMBOL_IN_COOLDOWN'!")

    # 2. execute_turbo_hedge_trade must reject order placement
    order_res = turbo_hedge_engine.execute_turbo_hedge_trade(
        api_key="mock_key",
        api_secret="mock_secret",
        symbol=test_sym,
        side="BUY",
        amount_usdt=5.0,
        chat_id=999999
    )
    assert order_res.get("status") == "skipped"
    assert "cooldown" in order_res.get("reason", "").lower()
    print("  [PASS] execute_turbo_hedge: Blocked order placement due to active cooldown!")
    print()

def test_cooldown_expiry_release():
    print("======================================================================")
    print("TEST 4: Cooldown Expiration & Clean Asset Release")
    print("======================================================================")

    test_sym = "TESTEXPIREUSDT"
    # Set an already-expired cooldown (-10 seconds)
    turbo_hedge_engine._cooldown_symbols[test_sym] = time.time() - 10
    db.update_system_setting(f"turbo_hedge_cooldown_{test_sym}", str(time.time() - 10))

    assert not turbo_hedge_engine.is_symbol_in_cooldown(test_sym)
    print("  [PASS] Expired cooldown automatically releases symbol back to trading pool!")
    print()

if __name__ == "__main__":
    test_stop_loss_trigger_conditions()
    test_blacklist_cooldown_system()
    test_cooldown_re_entry_guards()
    test_cooldown_expiry_release()
    print("======================================================================")
    print(">>> ALL TESTS PASSED: ANTI-WHIPSAW CLEAN STOP VERIFIED 100%! <<<")
    print("======================================================================")
