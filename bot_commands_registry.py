# -*- coding: utf-8 -*-
"""
KHMER MASTER CRYPTO - INSTITUTIONAL BOT COMMANDS REGISTRY
Document Version: 13.0.0
Ground Truth Authority: Invariant 23 (AGENTS.md)

Single canonical source of truth for Telegram Bot Commands across:
- bot_thread.py (post_init & post_init_set_commands)
- set_bot_commands.py
- force_clear_and_set_commands.py
- audit_system.py
"""

from telegram import BotCommand


def get_public_bot_commands():
    """
    Public VIP User Command List (Super Smart & Beautiful Institutional Hierarchy)
    Hierarchy:
      1. Initiation & Master Navigation: /start, /menu
      2. Spot Investment Engines (100% Spot, Zero Leverage): /compound_grid, /infinity_matrix, /smart_trade
      3. Futures & Hedge Engines: /turbo_hedge, /smartx, /scalp, /auto_trade
      4. CeDeFi & Arbitrage Engines: /flash_loan, /smart_swap, /cross_arb, /funding_harvester, /web3_wallet
      5. Market Intelligence & Radars: /whales, /flash_crash, /pre_pump, /news, /analyze, /predict, /top
      6. Portfolio, Risk & Account Security: /balance, /portfolio, /status, /report, /paper_trading, /alert, /stop, /set_pin, /reset_pin
    """
    return [
        # --- [1] INITIATION & MASTER NAVIGATION ---
        BotCommand("start", "🚀 Start Angkor Quant & Language"),
        BotCommand("menu", "🎛️ Angkor Quant Control Panel"),
        BotCommand("webapp", "📱 Angkor Quant Mini App Web GUI"),

        # --- [2] SPOT INVESTMENT ENGINES (100% Spot, 0% Liquidation Risk) ---
        BotCommand("compound_grid", "📈 Angkor Compound Grid (100% Spot)"),
        BotCommand("infinity_matrix", "♾️ Angkor Infinity Matrix (Fibonacci)"),
        BotCommand("smart_trade", "💎 Angkor Smart Trade (Spot Accumulator)"),
        BotCommand("spot_harvest", "🏦 Angkor Spot Harvest (Profit Vault)"),

        # --- [3] FUTURES & HEDGE ENGINES (Delta-Neutral & Precision Execution) ---
        BotCommand("wealth", "💎 Angkor Wealth Engine (Spot & Futures)"),
        BotCommand("turbo_hedge", "🛡️ Angkor Turbo Hedge (Dual-Side Engine)"),
        BotCommand("smartx", "👑 Angkor Intelligence X (33 AI Swarm)"),
        BotCommand("smartx_reachsey_meas", "🥇 Angkor Gold Matrix (Pending Stop)"),
        BotCommand("smartx_reachsey_crypto", "🪙 Angkor Crypto Matrix (Multi-Asset)"),
        BotCommand("scalp", "🏓 Angkor Precision Scalper (Micro-Vol)"),
        BotCommand("auto_trade", "🤖 Angkor AutoTrade (Macro Waterfall)"),
        BotCommand("command", "🦅 Angkor Command AI (Omni-Swarm)"),
        BotCommand("skynet", "🦅 Angkor Command AI (Legacy /skynet)"),

        # --- [4] CEDEFI & ARBITRAGE ENGINES (MEV & High-Yield Harvester) ---
        BotCommand("capital", "🏛️ Angkor Capital (Gold, Oil, US500)"),
        BotCommand("forex", "💱 Angkor Forex (24/7 Global Satellite)"),
        BotCommand("mt5", "⚡ Angkor MT5 (Tokyo GTCFX Master Pool)"),
        BotCommand("mt5_reachsey", "👑 Angkor MT5 Matrix (5-Position Basket)"),
        BotCommand("mt5_hf", "🤗 Angkor MT5 Free 16GB Worker"),
        BotCommand("capital_ib", "🤝 Angkor Capital IB Rebates (30%-50%)"),
        BotCommand("capital_orb", "🎯 Angkor London & NY 15m ORB Breakout"),
        BotCommand("capital_kelly", "📐 Angkor Fractional Kelly Position Sizer"),
        BotCommand("capital_spread", "🛡️ Angkor Spread Drag Elimination (10x)"),
        BotCommand("capital_news", "⚡ Angkor Post-News Volatility Harvester"),
        BotCommand("capital_scalp", "⚡ Angkor 24/7 Trend Scalp Engine"),
        BotCommand("flash_loan", "⚡ Angkor Quantum CeDeFi Arbitrage"),
        BotCommand("smart_swap", "⚡ Angkor DEX & AI Gem Sniper"),
        BotCommand("cross_arb", "⚡ Angkor Cross-Market Arbitrage"),
        BotCommand("funding_harvester", "🌾 Angkor Delta-Neutral Funding Harvester"),
        BotCommand("web3_wallet", "💼 Angkor Web3 Settlement Wallet"),

        # --- [5] MARKET INTELLIGENCE & RADARS (AGI & Multi-Timeframe) ---
        BotCommand("csx", "🏛️ Angkor CSX Stock Radar (Cambodia)"),
        BotCommand("whales", "🐋 Angkor Whale Radar L2"),
        BotCommand("flash_crash", "🎯 Angkor Crash Hunter"),
        BotCommand("pre_pump", "🔥 Angkor Pre-Pump Radar"),
        BotCommand("news", "📰 Angkor News Intelligence"),
        BotCommand("macro", "🛰️ Angkor Macro Satellite"),
        BotCommand("analyze", "🧠 Angkor Intelligence Deep Analysis"),
        BotCommand("predict", "📈 Angkor 24h Trend Forecast"),
        BotCommand("top", "🔥 Angkor Volatile Gainers & Losers"),

        # --- [6] PORTFOLIO, RISK & ACCOUNT SECURITY ---
        BotCommand("balance", "💰 Angkor Multi-Wallet USDT Balance"),
        BotCommand("portfolio", "💼 Angkor Unified Portfolio & Net PnL"),
        BotCommand("status", "📊 Angkor Active Trades & Live PnL"),
        BotCommand("journal", "📓 Angkor Trading Journal & Mistake Tag"),
        BotCommand("report", "📊 Angkor Multi-Timeframe Engine Audit"),
        BotCommand("audit", "👑 APEX VIP 24H Daily Audit & Fleet Telemetry"),
        BotCommand("daily_audit", "⏰ 24H Daily Institutional Audit"),
        BotCommand("paper_trading", "🧪 Angkor Paper vs Live Trading Mode"),
        BotCommand("alert", "🔔 Angkor Real-Time Price Alert"),
        BotCommand("stop", "🛑 Angkor Emergency Stop Trading"),
        BotCommand("set_pin", "🔒 Angkor Configure 2FA Security PIN"),
        BotCommand("reset_pin", "🔒 Angkor 2FA Security PIN Recovery"),
        BotCommand("citadel", "🛡️ Angkor Risk Citadel & Virtualizer"),
        BotCommand("agreement", "✍️ Angkor Private Agreement & Risk Waiver"),
        BotCommand("about", "📜 Angkor Terms, Agreement & Legal Notice"),
    ]


def get_admin_bot_commands():
    """
    Super Admin Command List
    Appends the 9 Super Admin exclusive commands strictly at the BOTTOM.
    """
    return list(get_public_bot_commands()) + [
        # --- [7] SUPER ADMIN EXCLUSIVE (Placed at the bottom) ---
        BotCommand("admin", "👑 Angkor Admin Executive Control Panel"),
        BotCommand("admin_users", "👥 Angkor VIP Users Directory"),
        BotCommand("admin_agreements", "📜 Angkor User Legal Contracts & PDF Vault"),
        BotCommand("admin_license", "🔑 Angkor VIP License Manager"),
        BotCommand("admin_broadcast", "📢 Angkor Global Urgent Broadcast"),
        BotCommand("admin_stats", "📊 Angkor Platform Volume & Stats"),
        BotCommand("admin_config", "⚙️ Angkor Live System Configuration"),
        BotCommand("health", "🩺 Angkor VPS Health & Diagnostics"),
        BotCommand("sync_brain", "📦 Angkor Hot-Reload AI Models"),
        BotCommand("hf_data", "🤗 Angkor Ultra-Fast HF Storage"),
        BotCommand("admin_capital", "🏢 Angkor Capital Live Approver"),
        BotCommand("admin_mt5", "🏛️ Angkor MT5 Live Approver"),
        BotCommand("master_sync", "🚂 Angkor Master Locomotive Sync"),
        BotCommand("master_close_all", "🚨 Master Close All Positions"),
        BotCommand("master_protect", "🛡️ Master Emergency Armor Protection"),
        BotCommand("admin_nuke", "🛑 Angkor Emergency Kill Switch & Shutdown"),
    ]
