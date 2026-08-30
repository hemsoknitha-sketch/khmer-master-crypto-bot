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
        # 1. Navigation & Account
        BotCommand("start", "🚀 Start Bot & Select Language"),
        BotCommand("menu", "🎛️ Master Control Panel & Interactive Menu"),
        BotCommand("balance", "💰 Check Spot & Futures Balance"),
        BotCommand("portfolio", "💼 View Active Positions & PnL"),

        # 2. 5 Super Smart Engines
        BotCommand("hyper_trade", "🚀 Hyper-Trade HFT Sub-Second Scalper"),
        BotCommand("auto_arb", "⚡ Delta-Neutral 0% Risk Arbitrage"),
        BotCommand("sweep_auto", "🛡️ Liquidity Sweep Bottom Wick Sniper"),
        BotCommand("funding_harvester", "🌾 30%-120% APY Perpetual Funding Yield"),
        BotCommand("trailing_guard", "🛡️ Auto-Liquidation Guard & Trailing Lock"),

        # 3. AI Quant Trading Strategies
        BotCommand("turbo_hedge", "🚀 Turbo Hedge Futures 5x Engine"),
        BotCommand("infinity_matrix", "♾️ Unified Smart Grid Strategy"),
        BotCommand("smart_dca", "🎯 Smart DCA Martingale Ladder"),
        BotCommand("grid_bot", "📊 24/7 Grid Trading Engine"),

        # 4. AI Analytics & Market Intelligence
        BotCommand("analyze", "🧠 5-Agent AGI Market Analysis"),
        BotCommand("predict", "📈 Wall Street ML 24h Prediction"),
        BotCommand("gold_radar", "🏆 PAXG Gold Wealth Protection Radar"),
        BotCommand("whales", "🐋 On-Chain Whale Inflow/Outflow Tracker"),
        BotCommand("news", "📰 AI Journalistic Crypto News & Impact"),

        # 5. Emergency Stop
        BotCommand("stop", "🛑 Emergency Stop All Active Trading"),
    ]

    admin_commands = [
        BotCommand("admin", "👑 Open Super Admin Control Panel"),
        BotCommand("health", "🩺 VPS Hardware & Engine Diagnostics"),
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
