import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import portfolio_engine
import database as db

def test_portfolio_smart_swap_integration():
    print("======================================================================")
    print("  [TEST 1/3] Testing get_full_system_portfolio_data with Smart Swap")
    print("======================================================================")
    test_chat_id = 859271875 # Known admin / keeper user
    data = portfolio_engine.get_full_system_portfolio_data(test_chat_id)

    print(f"  Chat ID: {data.get('chat_id')}")
    print(f"  Total Net Worth: ${data.get('total_portfolio_net_worth')}")
    print(f"  Total On-Chain Capital: ${data.get('total_onchain_capital')}")
    print(f"  Solana Trading Wallet: {data.get('user_sol_pubkey')}")
    print(f"  Solana Balance: {data.get('user_sol_bal')} SOL (${data.get('user_sol_usd')} USD)")
    print(f"  Phantom Vault: {data.get('phantom_vault')}")
    print(f"  Active Smart Swaps Count: {len(data.get('active_smart_swaps', []))}")
    print(f"  Realized Swap PnL: ${data.get('total_realized_swap_pnl')}")

    assert "user_sol_pubkey" in data, "Must contain user_sol_pubkey"
    assert "user_sol_bal" in data, "Must contain user_sol_bal"
    assert "total_onchain_capital" in data, "Must contain total_onchain_capital"
    assert data["total_portfolio_net_worth"] >= 0.0, "Net worth must be >= 0"
    print("  >>> [PASS] get_full_system_portfolio_data Verified! <<<\n")

    print("======================================================================")
    print("  [TEST 2/3] Testing render_portfolio_card (Khmer & English)")
    print("======================================================================")
    card_km = portfolio_engine.render_portfolio_card(data, user_lang="km")
    card_en = portfolio_engine.render_portfolio_card(data, user_lang="en")

    assert "Solana Trading Wallet" in card_km, "Card KM must mention Solana Trading Wallet"
    assert "Phantom Vault" in card_km, "Card KM must mention Phantom Vault"
    assert "Smart Swap Multi-Chain DEX & AI Sniper" in card_km, "Card KM must audit Smart Swap"
    assert "Solana Trading Wallet" in card_en, "Card EN must mention Solana Trading Wallet"
    assert "Smart Swap Multi-Chain DEX & AI Sniper" in card_en, "Card EN must audit Smart Swap"

    print("  Khmer Card Snippet:")
    for line in card_km.split("\n")[:15]:
        print(f"    {line}")
    print("  >>> [PASS] render_portfolio_card Verified! <<<\n")

    print("======================================================================")
    print("  [TEST 3/3] Testing render_smart_swap_dex_portfolio_card")
    print("======================================================================")
    dex_km = portfolio_engine.render_smart_swap_dex_portfolio_card(data, user_lang="km")
    dex_en = portfolio_engine.render_smart_swap_dex_portfolio_card(data, user_lang="en")

    assert "SUPER SMART ON-CHAIN DEX PORTFOLIO" in dex_km, "DEX KM card title match"
    assert "Jupiter Aggregator v6" in dex_km, "DEX KM must mention Jupiter"
    assert "Jito Private Bundle" in dex_km, "DEX KM must mention Jito MEV"
    assert "SUPER SMART ON-CHAIN DEX PORTFOLIO" in dex_en, "DEX EN card title match"

    print("  DEX Card Snippet:")
    for line in dex_km.split("\n")[:18]:
        print(f"    {line}")
    print("  >>> [PASS] render_smart_swap_dex_portfolio_card Verified! <<<\n")

if __name__ == "__main__":
    print("\n⚡ RUNNING SUPER SMART PORTFOLIO + SMART SWAP TEST SUITE 🛡️\n")
    test_portfolio_smart_swap_integration()
    print("======================================================================")
    print("  🎯 ALL PORTFOLIO TESTS PASSED (100% SUCCESS)!")
    print("======================================================================\n")
