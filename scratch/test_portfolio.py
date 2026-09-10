import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
import portfolio_engine

def test_portfolio_data_aggregation():
    print("======================================================================")
    print("  [TEST 1/3] Portfolio Multi-Engine Data Aggregation Test")
    print("======================================================================")
    test_chat_id = 859271875 # Admin test ID
    data = portfolio_engine.get_full_system_portfolio_data(test_chat_id)
    
    print(f"  Chat ID: {data['chat_id']}")
    print(f"  Net Worth: ${data['total_portfolio_net_worth']:,.2f}")
    print(f"  Invested: ${data['total_invested_usd']:,.2f}")
    print(f"  Floating PnL: ${data['total_unrealized_pnl']:,.2f} ({data['total_roi_pct']:+.2f}%)")
    print(f"  Spot Free USDT: ${data['spot_usdt_free']:,.2f}")
    print(f"  Spot Alt Exposure: ${data['spot_alt_exposure']:,.2f}")
    print(f"  Futures Wallet USDT: ${data['futures_wallet_usdt']:,.2f}")
    print(f"  On-Chain DEX Capital: ${data['total_onchain_capital']:,.2f}")
    
    # Assert critical structural keys
    required_keys = [
        "total_portfolio_net_worth", "total_invested_usd", "total_unrealized_pnl", "total_roi_pct",
        "spot_usdt_free", "spot_alt_exposure", "futures_wallet_usdt", "total_onchain_capital",
        "active_futures_positions", "active_spot_trades", "user_turbo_bots", "active_smart_swaps",
        "active_grids", "user_snipers", "funding_cfg", "is_flash_loan_auto", "is_defender_active",
        "uptime_str", "cpu_usage", "ram_usage_mb", "db_size_mb"
    ]
    for k in required_keys:
        assert k in data, f"Missing critical portfolio key: {k}"
        
    print("  >>> [PASS] All Required Portfolio Keys & Metrics Aggregated! <<<\n")

def test_portfolio_card_rendering_and_all_10_engines():
    print("======================================================================")
    print("  [TEST 2/3] 100% Comprehensive 10-Engine Audit & Formatting Test")
    print("======================================================================")
    test_chat_id = 859271875
    data = portfolio_engine.get_full_system_portfolio_data(test_chat_id)
    
    # Test Khmer Rendering
    card_km = portfolio_engine.render_portfolio_card(data, user_lang="km")
    print(f"  Khmer Card Length: {len(card_km)} characters")
    
    # Verify all 10 engines appear in the card
    all_10_engines_km = [
        "Turbo Hedge",
        "Super Smart Trade Suite",
        "Smart X Quant Suite",
        "Smart Swap Multi-Chain DEX",
        "Dynamic Infinity Matrix",
        "Smart Listing & Pre-Pump Sniper",
        "8-Hour Funding Rate",
        "Gold Turbo & Macro Radar",
        "DeFi Flash Loan",
        "Liquidation Defender"
    ]
    for eng in all_10_engines_km:
        assert eng in card_km, f"Engine '{eng}' missing from Khmer portfolio card!"
        print(f"  [PASS] Verified Engine: {eng}")

    # Test English Rendering
    card_en = portfolio_engine.render_portfolio_card(data, user_lang="en")
    print(f"\n  English Card Length: {len(card_en)} characters")
    for eng in all_10_engines_km:
        assert eng in card_en, f"Engine '{eng}' missing from English portfolio card!"
        
    print("  >>> [PASS] All 10 Investment Engines Explicitly Audited & Formatted! <<<\n")

def test_portfolio_with_simulated_active_positions():
    print("======================================================================")
    print("  [TEST 3/3] Live Coin Transparency & Real-Time Holdings Test")
    print("======================================================================")
    mock_data = {
        "chat_id": 12345678,
        "is_paper": False,
        "total_portfolio_net_worth": 12500.50,
        "total_invested_usd": 4500.00,
        "total_unrealized_pnl": 345.20,
        "total_roi_pct": 7.67,
        "spot_usdt_free": 5000.00,
        "spot_alt_exposure": 2500.50,
        "spot_holdings": {"SOL": {"qty": 10.0, "price": 150.0, "value_usdt": 1500.0}},
        "futures_wallet_usdt": 5000.00,
        "futures_unrealized_pnl": 250.00,
        "total_onchain_capital": 500.00,
        "web3_wallets": {},
        "primary_web3": "0x123...456",
        "active_futures_positions": [
            {
                "symbol": "BTCUSDT",
                "side": "LONG",
                "leverage": 10,
                "qty": 0.5,
                "entry_price": 60000.0,
                "mark_price": 62000.0,
                "margin_usd": 3000.0,
                "pnl_usd": 1000.0,
                "roi_pct": 33.33
            }
        ],
        "active_spot_trades": [
            {
                "id": 1,
                "symbol": "ETHUSDT",
                "qty": 1.0,
                "buy_price": 2500.0,
                "current_price": 2650.0,
                "invested_usd": 2500.0,
                "pnl_usd": 150.0,
                "roi_pct": 6.00,
                "stop_loss_pct": 3.0
            }
        ],
        "user_turbo_bots": [
            {
                "symbol": "SOLUSDT",
                "amount_usd": 100.0,
                "leverage": 5,
                "side": "HEDGE",
                "target_tp_pct": 20.0,
                "entry_price": 150.0,
                "current_price": 152.5
            }
        ],
        "active_smart_swaps": [
            {
                "id": 1,
                "chain": "SOLANA",
                "symbol": "BONK",
                "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "amount_usd": 50.0,
                "current_val_usd": 75.0,
                "token_qty": 2500000.0,
                "entry_price": 0.000020,
                "current_price": 0.000030,
                "pnl_usd": 25.0,
                "roi_pct": 50.0,
                "scale_out_level": 1
            }
        ],
        "active_grids": [],
        "user_snipers": [],
        "funding_cfg": {"enabled": True, "amount": 100.0},
        "is_flash_loan_auto": True,
        "flash_loan_pnl": {"count": 12, "total_profit": 85.50},
        "is_defender_active": True,
        "circuit_breaker": {"tripped": False},
        "uptime_str": "12h 30m 00s",
        "cpu_usage": 15.2,
        "ram_usage_mb": 512,
        "ram_total_mb": 2048,
        "ram_pct": 25.0,
        "disk_used_gb": 12.5,
        "disk_total_gb": 50.0,
        "db_size_mb": 1.25
    }

    card = portfolio_engine.render_portfolio_card(mock_data, user_lang="km")
    
    # Assert exact coins appear in the output text
    assert "BTCUSDT" in card, "BTCUSDT position should be displayed"
    assert "ETHUSDT" in card, "ETHUSDT spot trade should be displayed"
    assert "SOLUSDT" in card, "SOLUSDT turbo hedge bot should be displayed"
    assert "BONK" in card, "BONK smart swap position should be displayed"
    assert "+$345.20 USD" in card, "Consolidated floating PnL should be displayed"
    assert "50% Moonbag" in card, "Scale out Moonbag level should be displayed"

    print("  • Sample Output Preview:\n" + "-"*50)
    print(card[:800] + "\n...")
    print("-"*50)
    print("  >>> [PASS] Live Coin Transparency & PnL Fully Verified! <<<\n")

if __name__ == "__main__":
    print("\n⚡ RUNNING SUPER SMART PORTFOLIO TEST SUITE 🛡️\n")
    test_portfolio_data_aggregation()
    test_portfolio_card_rendering_and_all_10_engines()
    test_portfolio_with_simulated_active_positions()
    print("======================================================================")
    print("  🎯 ALL 3 SUPER SMART PORTFOLIO TESTS PASSED (100% SUCCESS)!")
    print("======================================================================\n")
