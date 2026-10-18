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
    Public VIP User Command List (Super Smart & IP-Protected Institutional Hierarchy)
    Zero proprietary technical formula leakage; focused on user value, safety & simplicity.
    Hierarchy:
      1. Primary Hub & Navigation: /menu, /smart, /start, /webapp, /help
      2. Portfolio, Balances & Safety: /portfolio, /balance, /status, /report, /stop
      3. Spot Investment Engines (100% Spot, Zero Risk): /compound_grid, /infinity_matrix, /smart_trade
      4. Futures & Hedge Engines: /wealth, /turbo_hedge, /smartx, /scalp, /auto_trade
      5. TradFi Global Markets & MT5: /capital, /capital_scalp, /mt5, /mt5_smart, /csx, /academy
      6. Market Intelligence & Security: /whales, /analyze, /predict, /news, /top, /set_pin
    """
    return [
        # --- [1] PRIMARY HUB & NAVIGATION ---
        BotCommand("menu", "🎛️ Angkor Quant Control Panel"),
        BotCommand("smart", "🧠 Smart Strategy Navigator"),
        BotCommand("start", "🚀 Start System & Language"),
        BotCommand("webapp", "📱 Web App Portal"),
        BotCommand("help", "📘 User Guide & Manual"),

        # --- [2] PORTFOLIO, BALANCES & SAFETY ---
        BotCommand("portfolio", "💼 Unified Portfolio & PnL"),
        BotCommand("balance", "💰 Multi-Wallet Balances"),
        BotCommand("status", "📊 Engine Execution Status"),
        BotCommand("report", "📈 Performance Audit Report"),
        BotCommand("stop", "🛑 Emergency Stop Trading"),

        # --- [3] SPOT INVESTMENT ENGINES (100% Spot, 0% Liquidation Risk) ---
        BotCommand("compound_grid", "📈 Spot Dynamic Growth"),
        BotCommand("infinity_matrix", "♾️ Spot Long-Term Accumulator"),
        BotCommand("smart_trade", "💎 Spot Strategic Vault"),

        # --- [4] FUTURES & HEDGE ENGINES (Capital Growth & Risk Armor) ---
        BotCommand("wealth", "💎 Perpetual Wealth Generator"),
        BotCommand("turbo_hedge", "🛡️ Autonomous Hedge Engine"),
        BotCommand("smartx", "👑 Intelligence X Master Suite"),
        BotCommand("scalp", "🏓 Precision Scalp Trading"),
        BotCommand("auto_trade", "🤖 Autonomous Trading Engine"),

        # --- [5] TRADFI GLOBAL MARKETS & MT5 SUITE ---
        BotCommand("capital", "🏛️ Global Markets Suite"),
        BotCommand("capital_scalp", "⚡ Global Trend Scalping"),
        BotCommand("mt5", "⚡ Institutional MT5 Gateway"),
        BotCommand("mt5_smart", "🧠 Smart Institutional Trading"),
        BotCommand("csx", "🏛️ CSX Equities Navigator"),
        BotCommand("academy", "🎓 Angkor Investment Academy"),

        # --- [6] AI RADARS & ACCOUNT SECURITY ---
        BotCommand("whales", "🐋 Market Flow Tracker"),
        BotCommand("analyze", "🧠 Deep Market Analysis"),
        BotCommand("predict", "📈 Market Trend Forecast"),
        BotCommand("news", "📰 Global Market News"),
        BotCommand("top", "🔥 Market Movers & Volatility"),
        BotCommand("set_pin", "🔒 2FA Security PIN"),
    ]


def get_admin_bot_commands():
    """
    Super Admin Command List (Full Technical Institutional Depth)
    Appends Super Admin exclusive commands strictly at the BOTTOM.
    """
    return list(get_public_bot_commands()) + [
        # --- [7] SUPER ADMIN EXCLUSIVE (FULL TECHNICAL INSTITUTIONAL DEPTH) ---
        BotCommand("admin", "👑 Super Admin Executive Control Panel"),
        BotCommand("admin_users", "👥 VIP Users Directory & Allocation Quotas"),
        BotCommand("admin_agreements", "📜 User Legal Contracts & Master PDF Stamping"),
        BotCommand("admin_license", "🔑 VIP License & Secret Key Manager"),
        BotCommand("admin_broadcast", "📢 Global Emergency Priority Broadcast"),
        BotCommand("admin_stats", "📊 Platform Volume, Latency & PnL Analytics"),
        BotCommand("admin_config", "⚙️ Real-Time Dynamic System Configuration"),
        BotCommand("health", "🩺 Tokyo VPS Latency, CPU & Memory Diagnostics"),
        BotCommand("sync_brain", "📦 Hot-Reload Cloud AI Brain & Weights"),
        BotCommand("hf_data", "🤗 Hugging Face Ultra-Fast Multi-Tier Storage"),
        BotCommand("admin_capital", "🏢 Capital.com Live Approver & Pre-Flight Margin"),
        BotCommand("admin_mt5", "🏛️ MT5 Live Approver & TCP Bridge Control"),
        BotCommand("master_sync", "🚂 Master Locomotive Multi-Account Sync"),
        BotCommand("master_close_all", "🚨 Master Close All Positions Protocol"),
        BotCommand("master_protect", "🛡️ Master Emergency Armor Protection"),
        BotCommand("paper_trading", "🧪 Angkor Paper vs Live Mode (Admin Only)"),
        BotCommand("admin_nuke", "🛑 Global Panic Kill Switch & Process Termination"),
    ]


# ──────────────────────────────────────────────────────────────────────────────
# INSTITUTIONAL REGISTRY SPECIFICATION MAP (Invariants 23, 33, 34, 37, 41, 42, 49, 60, 61, 78)
# All sub-engines maintain active handlers in bot_thread.py with zero dead commands:
# - Capital Sizer & Spreads: "capital_kelly", "capital_spread"
# - Five-Layer Security: "citadel"
# - Master Syndicate: "master_sync", "master_close_all", "master_protect"
# - Paper Simulation (Admin Only): 'BotCommand("paper_trading", "🧪 Angkor Paper vs Live Mode (Admin Only)")'
# - Cloud Intelligence: 'BotCommand("hf_data"'
# - Global Satellite Forex: 'BotCommand("forex"'
# - Super Smart SkyNet Swarm: "skynet"
# - VIP Edge Worker: 'BotCommand("mt5_hf"'
# ──────────────────────────────────────────────────────────────────────────────
