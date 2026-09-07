import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Bot, BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeChat

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

async def set_menu_commands():
    if not TOKEN:
        print("[ERROR] TELEGRAM_BOT_TOKEN missing in .env!")
        return

    bot = Bot(token=TOKEN)
    public_commands = [
        BotCommand("start", "🚀 Start Bot & Choose Language"),
        BotCommand("menu", "🎛️ Interactive Master Control Panel"),
        BotCommand("flash_loan", "⚡ MEV & Flash Loan 0-Risk Arbitrage"),
        BotCommand("set_web3_wallet", "💼 Configure Web3 Settlement Wallet"),
        BotCommand("cross_arb", "⚡ Sub-5ms Cross-Exchange Arbitrage"),
        BotCommand("funding_harvester", "🌾 Delta-Neutral 30%-120% APY Harvester"),
        BotCommand("whales", "🐋 Whale Orderflow Front-Running Radar"),
        BotCommand("infinity_matrix", "📈 Dynamic Compound Infinity Matrix"),
        BotCommand("flash_crash", "🎯 Liquidation Cascade Deep Wick Hunter"),
        BotCommand("gold_turbo", "🥇 PAXG Macro Gold Correlation Radar"),
        BotCommand("snipe", "🎯 Smart Listing Token Sniper"),
        BotCommand("pre_pump", "🔥 Pre-Pump Accumulation Sniper"),
        BotCommand("smart_trade", "🛒 Spot 6-Tier Breakout Engine"),
        BotCommand("turbo_hedge", "🛡️ Futures Dual-Side Delta-Neutral Hedge"),
        BotCommand("scalp", "🏓 Micro-Volatility Precision Scalper"),
        BotCommand("auto_trade", "🤖 24/7 Hands-Free Multi-Asset Auto-Trader"),
        BotCommand("analyze", "🧠 5-Agent AGI Market Analysis"),
        BotCommand("predict", "📈 Wall Street ML 24h Prediction"),
        BotCommand("balance", "💰 Check Spot & Futures Balance"),
        BotCommand("portfolio", "💼 Unified Portfolio & Net PnL"),
        BotCommand("status", "📊 View Active Trades & PnL"),
        BotCommand("paper_trading", "🧪 Toggle Paper vs Live Trading"),
        BotCommand("news", "📰 3-Paragraph Journalistic Crypto News"),
        BotCommand("top", "🔥 Top Volatile Gainers & Losers"),
        BotCommand("alert", "🔔 Set Price Alert"),
        BotCommand("stop", "🛑 Stop Trading / Market Close"),
    ]

    admin_commands = [
        BotCommand("admin", "👑 Open Super Admin Control Panel"),
        BotCommand("admin_users", "👥 View Registered Users Directory"),
        BotCommand("admin_license", "🔑 Grant or Renew VIP License"),
        BotCommand("admin_broadcast", "📢 Broadcast Urgent Message to Users"),
        BotCommand("admin_stats", "📊 View Platform Volume & Stats"),
        BotCommand("admin_config", "⚙️ Modify Live System Parameters"),
        BotCommand("admin_nuke", "☢️ Emergency Panic Nuke & Shutdown"),
        BotCommand("health", "🩺 Check VPS Hardware & Engine Diagnostics"),
        BotCommand("sync_brain", "📦 Hot-Reload AI Models from Cloud"),
    ] + public_commands


    try:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
        await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
        await bot.set_my_commands(public_commands, scope=BotCommandScopeDefault())
        await bot.set_my_commands(public_commands, scope=BotCommandScopeAllPrivateChats())
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=859271875))
        except Exception:
            pass
        print("[SUCCESS] Telegram Bot Menu updated to v13.00 Absolute Ultimate AGI Public VIP & Super Admin Scopes!")
    except Exception as e:
        print(f"[ERROR] Error setting commands: {e}")

if __name__ == "__main__":
    asyncio.run(set_menu_commands())
