# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - INSTITUTIONAL BOT COMMANDS REGISTRY (AQ76)
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
    Public VIP User Command List (9 Core Commands - Clean, Simple & Unambiguous)
    Strictly follows Founder Specification:
    1. /menu      — 🎛️ ផ្ទាំងបញ្ជាធំឆ្លាតវៃ (Master Control Panel)
    2. /smart     — 🧠 មគ្គុទ្ទេសក៍ឆ្លាតវៃ & Strategy Selector
    3. /portfolio — 💼 ផលប័ត្រ & ប្រាក់ចំណេញសុទ្ធ Live PnL
    4. /balance   — 💰 សមតុល្យកាបូប Spot / Futures / TradFi
    5. /status    — 📊 ស្ថានភាពដំណើរការម៉ាស៊ីន 24/7
    6. /webapp    — 📱 Mini App Web Portal (Modern Web GUI)
    7. /report    — 📈 របាយការណ៍សវនកម្ម 24H Executive Audit
    8. /stop      — 🛑 ហ្វ្រាំងបន្ទាន់ Stop All Trading
    9. /help      — 📘 សៀវភៅណែនាំ & សេវាគាំទ្រ VIP
    """
    return [
        BotCommand("menu", "🎛️ ផ្ទាំងបញ្ជាធំឆ្លាតវៃ (Master Control Panel)"),
        BotCommand("smart", "🧠 មគ្គុទ្ទេសក៍ឆ្លាតវៃ & Strategy Selector"),
        BotCommand("portfolio", "💼 ផលប័ត្រ & ប្រាក់ចំណេញសុទ្ធ Live PnL"),
        BotCommand("balance", "💰 សមតុល្យកាបូប Spot / Futures / TradFi"),
        BotCommand("status", "📊 ស្ថានភាពដំណើរការម៉ាស៊ីន 24/7"),
        BotCommand("webapp", "📱 Mini App Web Portal (Modern Web GUI)"),
        BotCommand("report", "📈 របាយការណ៍សវនកម្ម 24H Executive Audit"),
        BotCommand("stop", "🛑 ហ្វ្រាំងបន្ទាន់ Stop All Trading"),
        BotCommand("help", "📘 សៀវភៅណែនាំ & សេវាគាំទ្រ VIP"),
    ]


def get_admin_bot_commands():
    """
    Super Admin Command List (9 Core Commands + Super Admin Controls strictly at bottom)
    Super Admin Additions:
    - /admin           — 👑 ផ្ទាំងបញ្ជាប្រតិបត្តិ Super Admin Panel
    - /admin_users     — 👥 បញ្ជី VIP Users & កូតាបែងចែកដើមទុន
    - /admin_license   — 🔑 គ្រប់គ្រង VIP License & Secret Keys
    - /admin_broadcast — 📢 ប្រកាសអាសន្នជាសកល Global Priority Broadcast
    - /health          — 🩺 វិនិច្ឆ័យ Latency, CPU & Memory លើ VPS
    - /admin_nuke      — 🛑 កុងតាក់អាសន្នសម្លាប់ដំណើរការ Global Kill Switch
    """
    return list(get_public_bot_commands()) + [
        BotCommand("admin", "👑 ផ្ទាំងបញ្ជាប្រតិបត្តិ Super Admin Panel"),
        BotCommand("admin_users", "👥 បញ្ជី VIP Users & កូតាបែងចែកដើមទុន"),
        BotCommand("admin_license", "🔑 គ្រប់គ្រង VIP License & Secret Keys"),
        BotCommand("admin_broadcast", "📢 ប្រកាសអាសន្នជាសកល Global Priority Broadcast"),
        BotCommand("health", "🩺 វិនិច្ឆ័យ Latency, CPU & Memory លើ VPS"),
        BotCommand("admin_nuke", "🛑 កុងតាក់អាសន្នសម្លាប់ដំណើរការ Global Kill Switch"),
    ]


def get_registered_commands():
    """
    Complete mapping of all active engine handlers across the Angkor Quant architecture.
    Ensures zero dead code and full parity across all sub-engines.
    """
    return list(get_admin_bot_commands()) + [
        BotCommand("compound_grid", "Spot Dynamic Growth"),
        BotCommand("infinity_matrix", "Spot Long-Term Accumulator"),
        BotCommand("smart_trade", "Spot Strategic Vault"),
        BotCommand("wealth", "Perpetual Wealth Generator"),
        BotCommand("turbo_hedge", "Autonomous Hedge Engine"),
        BotCommand("smartx", "Intelligence X Master Suite"),
        BotCommand("scalp", "Precision Scalp Trading"),
        BotCommand("auto_trade", "Autonomous Trading Engine"),
        BotCommand("capital", "Global Markets Suite"),
        BotCommand("capital_scalp", "Global Trend Scalping"),
        BotCommand("mt5", "GTC PAMM Institutional Gateway"),
        BotCommand("mt5_smart", "Smart Institutional Trading"),
        BotCommand("csx", "CSX Equities Navigator"),
        BotCommand("academy", "Angkor Investment Academy"),
        BotCommand("whales", "Market Flow Tracker"),
        BotCommand("analyze", "Deep Market Analysis"),
        BotCommand("predict", "Market Trend Forecast"),
        BotCommand("news", "Global Market News"),
        BotCommand("conference", "Live Conference & Speech Wire"),
        BotCommand("top", "Market Movers & Volatility"),
        BotCommand("set_pin", "2FA Security PIN"),
        BotCommand("admin_agreements", "User Legal Contracts"),
        BotCommand("admin_stats", "Platform Volume Analytics"),
        BotCommand("admin_config", "System Configuration"),
        BotCommand("sync_brain", "Cloud AI Brain Weights"),
        BotCommand("hf_data", "Hugging Face Multi-Tier Storage"),
        BotCommand("admin_capital", "Capital.com Live Approver"),
        BotCommand("admin_mt5", "MT5 Live Approver"),
        BotCommand("master_sync", "Master Syndicate Sync"),
        BotCommand("master_close_all", "Master Close All Protocol"),
        BotCommand("master_protect", "Master Armor Protection"),
        BotCommand("paper_trading", "🧪 Angkor Paper vs Live Mode (Admin Only)"),
        BotCommand("citadel", "Institutional Citadel"),
        BotCommand("forex", "Forex Satellite Radar"),
        BotCommand("skynet", "Super Smart SkyNet Swarm"),
        BotCommand("mt5_hf", "MT5 HF Edge Worker"),
        BotCommand("capital_kelly", "Capital Kelly Sizer"),
        BotCommand("capital_spread", "Capital Spread Drag Manager"),
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
# - Capital Referral Admin: "admin_capital"
# ──────────────────────────────────────────────────────────────────────────────
