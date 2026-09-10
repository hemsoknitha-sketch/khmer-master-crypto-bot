import sys
import os
import time

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
import smart_swap_engine

def test_jupiter_aggregator_quote():
    print("======================================================================")
    print("  [TEST 1/6] Jupiter Aggregator v6 Quote & Routing Test")
    print("======================================================================")
    sol_mint = smart_swap_engine.SOLANA_TOKENS["SOL"]
    usdc_mint = smart_swap_engine.SOLANA_TOKENS["USDC"]
    amount_atomic = int(0.1 * 1e9) # 0.1 SOL

    t0 = time.time()
    quote = smart_swap_engine.get_solana_jupiter_quote(sol_mint, usdc_mint, amount_atomic, slippage_bps=50)
    elapsed_ms = (time.time() - t0) * 1000

    print(f"  Status: {quote.get('status')}")
    print(f"  In Amount: {quote.get('in_amount')} lamports")
    print(f"  Out Amount: {quote.get('out_amount')} micro-USDC")
    print(f"  Price Impact: {quote.get('price_impact_pct')}%")
    print(f"  Route Steps: {quote.get('route_steps')}")
    print(f"  Latency: {elapsed_ms:.1f} ms")

    assert quote.get("status") == "success", f"Jupiter quote failed: {quote}"
    assert quote.get("out_amount", 0) > 0, "Out amount should be greater than 0"
    print("  >>> [PASS] Jupiter v6 Multi-DEX Aggregator Quote Verified! <<<\n")

def test_honeypot_rugpull_shield():
    print("======================================================================")
    print("  [TEST 2/6] Sub-Second Honeypot & Rug-Pull AI Security Shield")
    print("======================================================================")
    
    # 1. Test Verified Blue-Chip (SOL)
    res_sol = smart_swap_engine.evaluate_token_security("SOLANA", smart_swap_engine.SOLANA_TOKENS["SOL"])
    print(f"  SOL Security Audit: is_safe={res_sol['is_safe']}, risk_score={res_sol['risk_score']}, reasons={res_sol['reasons']}")
    assert res_sol["is_safe"] is True, "SOL should pass security audit"
    assert res_sol["risk_score"] == 0.0, "SOL risk score should be 0.0"

    # 2. Test Verified Blue-Chip (USDC)
    res_usdc = smart_swap_engine.evaluate_token_security("SOLANA", smart_swap_engine.SOLANA_TOKENS["USDC"])
    print(f"  USDC Security Audit: is_safe={res_usdc['is_safe']}, risk_score={res_usdc['risk_score']}")
    assert res_usdc["is_safe"] is True, "USDC should pass security audit"

    # 3. Test Unknown/Zero-Liquidity Fake Token
    fake_token = "0x000000000000000000000000000000000000dEaD"
    res_fake = smart_swap_engine.evaluate_token_security("BSC", fake_token)
    print(f"  Fake Token Audit: is_safe={res_fake['is_safe']}, status={res_fake['status']}, reasons={res_fake['reasons']}")
    assert res_fake["is_safe"] is False, "Dead/Fake token should be flagged unsafe"
    print("  >>> [PASS] Honeypot & Rug-Pull AI Shield Verified! <<<\n")

def test_volume_velocity_and_ai_momentum():
    print("======================================================================")
    print("  [TEST 3/6] Volume Velocity & AI Momentum Gem Scanner")
    print("======================================================================")
    gems = smart_swap_engine.scan_onchain_momentum_gems("SOLANA", limit=4)
    print(f"  Scanned Discovered Gems Count: {len(gems)}")
    for idx, g in enumerate(gems, 1):
        print(f"    {idx}. {g['symbol']} | Dex: {g['dex']} | Price: ${g['price_usd']:.6f} | Liq: ${g['liquidity_usd']:,.0f} | AI Score: {g['score']}/100")
        assert g["score"] >= 50.0, "AI Momentum score should be valid"
        assert g["liquidity_usd"] >= 8000, "Liquidity floor must be enforced"

    assert len(gems) > 0, "Should discover at least one qualified momentum gem"
    print("  >>> [PASS] Volume Velocity & AI Momentum Scanner Verified! <<<\n")

def test_database_smart_swap_lifecycle():
    print("======================================================================")
    print("  [TEST 4/6] Database Active Smart Swap Position Tracking & PnL")
    print("======================================================================")
    test_chat_id = 999999999
    # Clean up any leftover test data
    leftovers = db.get_active_smart_swaps(chat_id=test_chat_id)
    for l in leftovers:
        db.remove_active_smart_swap(l["id"])

    swap_id = db.add_active_smart_swap(
        chat_id=test_chat_id,
        chain="SOLANA",
        token_address=smart_swap_engine.SOLANA_TOKENS["BONK"],
        token_symbol="BONK",
        amount_in_usd=20.0,
        token_qty=1000000.0,
        entry_price=0.000020,
        tx_hash="test_tx_hash_123"
    )
    print(f"  Inserted Smart Swap ID: {swap_id}")
    assert swap_id > 0, "Swap ID must be positive integer"

    active = db.get_active_smart_swaps(chat_id=test_chat_id)
    assert len(active) == 1, "Should retrieve 1 active swap"
    pos = active[0]
    assert pos["token_symbol"] == "BONK"
    assert pos["amount_in_usd"] == 20.0
    assert pos["scale_out_level"] == 0

    # Test peak price and scale out update
    db.update_smart_swap_peak(swap_id, 0.000030, scale_out_level=1)
    updated = db.get_active_smart_swaps(chat_id=test_chat_id)[0]
    assert updated["peak_price"] >= 0.000030, "Peak price should be updated"
    assert updated["scale_out_level"] == 1, "Scale out level should be updated to 1"

    # Test removing swap
    db.remove_active_smart_swap(swap_id)
    remaining = db.get_active_smart_swaps(chat_id=test_chat_id)
    assert len(remaining) == 0, "Position should be removed cleanly"
    print("  >>> [PASS] Database Active Swap Lifecycle Verified! <<<\n")

def test_smart_swap_execution_and_vault():
    print("======================================================================")
    print("  [TEST 5/6] Direct Swap Execution & Keeper Relayer Vault Fallback")
    print("======================================================================")
    test_chat_id = 999999998
    # Clean up test swaps
    for s in db.get_active_smart_swaps(chat_id=test_chat_id):
        db.remove_active_smart_swap(s["id"])

    import trading_engine

    # 1. Test Live Trading with Unfunded Wallet -> Expect INSUFFICIENT_SOL_BALANCE rejection
    trading_engine.PAPER_TRADING = False
    res_unfunded = smart_swap_engine.execute_smart_swap(
        chat_id=test_chat_id,
        chain="SOLANA",
        from_token="SOL",
        to_token="USDC",
        amount=0.1,
        slippage_pct=0.5,
        pin="1234"
    )
    print(f"  Unfunded Live Swap: status={res_unfunded.get('status')}, reason={res_unfunded.get('reason')}")
    assert res_unfunded.get("status") == "error", "Unfunded wallet must not execute live on-chain"
    assert res_unfunded.get("reason") == "INSUFFICIENT_SOL_BALANCE", "Reason must be INSUFFICIENT_SOL_BALANCE"

    # 2. Test Paper Trading Execution -> Expect Success & Recorded Position
    trading_engine.PAPER_TRADING = True
    res = smart_swap_engine.execute_smart_swap(
        chat_id=test_chat_id,
        chain="SOLANA",
        from_token="SOL",
        to_token="USDC",
        amount=0.1,
        slippage_pct=0.5,
        pin="1234"
    )
    print(f"  Execution Status: {res.get('status')}")
    print(f"  Route: {res.get('amount_in')} {res.get('from_token')} -> {res.get('token_qty')} {res.get('to_token')}")
    print(f"  USD Value: ${res.get('amount_usd')}")
    print(f"  Price Impact: {res.get('price_impact_pct')}%")
    print(f"  Recipient Vault: {res.get('recipient')} (is_vault: {res.get('is_vault')})")
    print(f"  MEV Shield: {res.get('mev_shield')}")

    assert res.get("status") == "success", f"Paper swap failed: {res}"
    assert res.get("token_qty", 0) > 0, "Token quantity must be > 0"
    assert res.get("is_vault") is True, "Should use vault fallback when no user wallet linked"

    # Verify active swap recorded
    active = db.get_active_smart_swaps(chat_id=test_chat_id)
    assert len(active) == 1, "Active swap should be recorded in database"
    print("  >>> [PASS] Direct Swap Execution & Vault Verified! <<<\n")

def test_status_overview_and_stop_swap():
    print("======================================================================")
    print("  [TEST 6/6] Status Overview & Instant Stop Swap (Market Exit)")
    print("======================================================================")
    test_chat_id = 999999998
    overview = smart_swap_engine.get_smart_swap_status_overview(test_chat_id)
    print(f"  Active Positions in Status: {overview['active_count']}")
    print(f"  Total USD Value: ${overview['total_value_usd']}")
    print(f"  Unrealized PnL: ${overview['total_unrealized_pnl']}")
    assert overview["active_count"] >= 1, "Should find at least 1 active position"

    # Stop Swap
    stop_res = smart_swap_engine.stop_smart_swap(test_chat_id, "ALL")
    print(f"  Stop Swap Status: {stop_res.get('status')}")
    print(f"  Closed Positions Count: {stop_res.get('closed_count')}")
    print(f"  Closed Symbols: {stop_res.get('symbols')}")
    print(f"  Realized USD: ${stop_res.get('total_realized_usd')}")

    assert stop_res.get("status") == "success", f"Stop swap failed: {stop_res}"
    assert stop_res.get("closed_count") >= 1, "Should close active positions"

    # Verify 0 active swaps remaining
    remaining = db.get_active_smart_swaps(chat_id=test_chat_id)
    assert len(remaining) == 0, "All positions should be closed"
    print("  >>> [PASS] Status Overview & Instant Stop Swap Verified! <<<\n")

if __name__ == "__main__":
    print("\n⚡ RUNNING INSTITUTIONAL SMART SWAP ENGINE TEST SUITE 🛡️\n")
    test_jupiter_aggregator_quote()
    test_honeypot_rugpull_shield()
    test_volume_velocity_and_ai_momentum()
    test_database_smart_swap_lifecycle()
    test_smart_swap_execution_and_vault()
    test_status_overview_and_stop_swap()
    print("======================================================================")
    print("  🎯 ALL 6 INSTITUTIONAL SMART SWAP TESTS PASSED (100% SUCCESS)!")
    print("======================================================================\n")
