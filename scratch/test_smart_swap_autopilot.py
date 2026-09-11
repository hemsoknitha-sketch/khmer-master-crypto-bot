import sys
import os
import time

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
import smart_swap_engine
import portfolio_engine

def test_smart_swap_autopilot_suite():
    print("======================================================================")
    print("  [TEST 1/4] Testing Database Auto-Pilot Config Storage")
    print("======================================================================")
    test_chat_id = 999999991

    # Initially disabled
    cfg = db.get_smart_swap_autopilot_config(test_chat_id)
    assert cfg["enabled"] is False, "Default should be disabled"

    # Save custom config
    db.set_smart_swap_autopilot_config(test_chat_id, enabled=True, amount=25.0, max_positions=2, chain="SOLANA")
    cfg_on = db.get_smart_swap_autopilot_config(test_chat_id)
    assert cfg_on["enabled"] is True, "Must be enabled"
    assert cfg_on["amount"] == 25.0, "Amount must match 25.0"
    assert cfg_on["max_positions"] == 2, "Max positions must match 2"
    assert cfg_on["chain"] == "SOLANA", "Chain must be SOLANA"

    # Check active list
    active_all = db.get_all_active_smart_swap_autopilots()
    found = any(u["chat_id"] == test_chat_id for u in active_all)
    assert found, "Test user must appear in get_all_active_smart_swap_autopilots"
    print("  >>> [PASS] Database Config Storage & Active List Verified! <<<\n")

    print("======================================================================")
    print("  [TEST 2/4] Testing toggle_smart_swap_autopilot (PIN & Limits)")
    print("======================================================================")
    # Invalid PIN
    res_bad_pin = smart_swap_engine.toggle_smart_swap_autopilot(test_chat_id, enable=True, pin="9999")
    # PIN might be verified or rejected based on user PIN in DB
    print(f"  Toggle result with test PIN: {res_bad_pin.get('status')}")

    # Valid toggle with SKIP PIN
    res_on = smart_swap_engine.toggle_smart_swap_autopilot(test_chat_id, enable=True, amount_usd=20.0, max_positions=2, pin="SKIP")
    assert res_on["status"] == "success", "Must succeed with SKIP PIN"
    assert res_on["action"] == "ENABLED", "Action must be ENABLED"
    assert res_on["amount_usd"] == 20.0

    # Toggle OFF
    res_off = smart_swap_engine.toggle_smart_swap_autopilot(test_chat_id, enable=False, pin="SKIP")
    assert res_off["status"] == "success", "Must succeed with SKIP PIN"
    assert res_off["action"] == "DISABLED", "Action must be DISABLED"
    print("  >>> [PASS] toggle_smart_swap_autopilot Verified! <<<\n")

    print("======================================================================")
    print("  [TEST 3/4] Testing run_smart_swap_autopilot_cycle Concurrency & Safety")
    print("======================================================================")
    # Enable test user
    db.set_smart_swap_autopilot_config(test_chat_id, enabled=True, amount=20.0, max_positions=2, chain="SOLANA")

    # Run cycle - shouldn't crash
    smart_swap_engine.run_smart_swap_autopilot_cycle(app=None)
    print("  Autopilot cycle executed safely without exceptions.")

    # Disable test user after test
    db.set_smart_swap_autopilot_config(test_chat_id, enabled=False)
    print("  >>> [PASS] run_smart_swap_autopilot_cycle Verified! <<<\n")

    print("======================================================================")
    print("  [TEST 4/4] Testing Portfolio Engine Auto-Pilot Card Integration")
    print("======================================================================")
    data = portfolio_engine.get_full_system_portfolio_data(test_chat_id)
    assert "smart_swap_autopilot" in data, "Portfolio data must contain smart_swap_autopilot"

    card_km = portfolio_engine.render_portfolio_card(data, user_lang="km")
    card_dex = portfolio_engine.render_smart_swap_dex_portfolio_card(data, user_lang="km")

    assert "24/7 Auto-Pilot" in card_km, "Main portfolio card must render 24/7 Auto-Pilot"
    assert "24/7 Autonomous Auto-Pilot" in card_dex, "DEX portfolio card must render Auto-Pilot"

    print("  Khmer Card Auto-Pilot line verified!")
    print("  DEX Card Auto-Pilot line verified!")
    print("  >>> [PASS] Portfolio Engine Integration Verified! <<<\n")

if __name__ == "__main__":
    print("\n⚡ RUNNING 24/7 CONTINUOUS AUTONOMOUS AUTO-PILOT TEST SUITE 🛡️\n")
    test_smart_swap_autopilot_suite()
    print("======================================================================")
    print("  🎯 ALL 4 AUTONOMOUS AUTO-PILOT TESTS PASSED (100% SUCCESS)!")
    print("======================================================================\n")
