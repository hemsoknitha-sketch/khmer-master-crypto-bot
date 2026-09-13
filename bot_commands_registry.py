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
        BotCommand("start", "🚀 Start Bot & Choose Language"),
        BotCommand("menu", "🎛️ Interactive Master Control Panel"),

        # --- [2] SPOT INVESTMENT ENGINES (100% Spot, 0% Liquidation Risk) ---
        BotCommand("compound_grid", "📈 100% Spot Snowball Compound Grid"),
        BotCommand("infinity_matrix", "♾️ 100% Spot Dynamic Fibonacci Matrix"),
        BotCommand("smart_trade", "💎 Institutional Spot Auto Accumulator"),

        # --- [3] FUTURES & HEDGE ENGINES (Delta-Neutral & Precision Execution) ---
        BotCommand("turbo_hedge", "🛡️ Institutional Dual-Side Delta-Neutral Hedge"),
        BotCommand("smartx", "👑 5-Agent Swarm + 12 Wall Street ML Ensembles"),
        BotCommand("scalp", "🏓 Micro-Volatility Precision Scalper"),
        BotCommand("auto_trade", "🤖 24/7 Hands-Free Multi-Asset Auto-Trader"),

        # --- [4] CEDEFI & ARBITRAGE ENGINES (MEV & High-Yield Harvester) ---
        BotCommand("flash_loan", "⚡ Aave V3 Tokyo HFT MEV 0-Risk Arbitrage"),
        BotCommand("smart_swap", "⚡ Multi-Chain DEX & AI Gem Sniper"),
        BotCommand("cross_arb", "⚡ Sub-5ms Cross-Exchange Arbitrage"),
        BotCommand("funding_harvester", "🌾 Delta-Neutral 30%-120% APY Harvester"),
        BotCommand("web3_wallet", "💼 Link Web3 Settlement Wallet (MetaMask)"),

        # --- [5] MARKET INTELLIGENCE & RADARS (AGI & Multi-Timeframe) ---
        BotCommand("whales", "🐋 Whale Orderflow Front-Running Radar"),
        BotCommand("flash_crash", "🎯 Liquidation Cascade Deep Wick Hunter"),
        BotCommand("pre_pump", "🔥 Pre-Pump Accumulation Radar"),
        BotCommand("news", "📰 3-Paragraph Journalistic Crypto News"),
        BotCommand("analyze", "🧠 5-Agent AGI Deep Market Analysis"),
        BotCommand("predict", "📈 Wall Street ML 24h Price Prediction"),
        BotCommand("top", "🔥 Top Volatile Gainers & Losers"),

        # --- [6] PORTFOLIO, RISK & ACCOUNT SECURITY ---
        BotCommand("balance", "💰 Check Spot & Futures USDT Balance"),
        BotCommand("portfolio", "💼 Unified Portfolio & Net Realized PnL"),
        BotCommand("status", "📊 View Active Trades & Real-Time PnL"),
        BotCommand("report", "📊 Dedicated Multi-Timeframe & Engine Audit"),
        BotCommand("paper_trading", "🧪 Toggle Paper vs Live Trading Mode"),
        BotCommand("alert", "🔔 Real-Time Price Alert Notification"),
        BotCommand("stop", "🛑 Emergency Stop Trading & Market Close"),
        BotCommand("set_pin", "🔒 Configure 2FA Security PIN"),
        BotCommand("reset_pin", "🔒 2FA Security PIN Reset & Recovery"),
    ]


def get_admin_bot_commands():
    """
    Super Admin Command List
    Appends the 9 Super Admin exclusive commands strictly at the BOTTOM.
    """
    return list(get_public_bot_commands()) + [
        # --- [7] SUPER ADMIN EXCLUSIVE (Placed at the bottom) ---
        BotCommand("admin", "👑 Super Admin Executive Control Panel"),
        BotCommand("admin_users", "👥 View Registered VIP Users Directory"),
        BotCommand("admin_license", "🔑 Grant or Renew VIP License"),
        BotCommand("admin_broadcast", "📢 Broadcast Urgent Announcement"),
        BotCommand("admin_stats", "📊 Platform Volume & Performance Stats"),
        BotCommand("admin_config", "⚙️ Modify Live System Parameters"),
        BotCommand("admin_nuke", "☢️ Emergency Panic Nuke & Shutdown"),
        BotCommand("health", "🩺 Check VPS Hardware & Engine Diagnostics"),
        BotCommand("sync_brain", "📦 Hot-Reload AI Models from Cloud"),
    ]
