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
        BotCommand("start", "🚀 Start v13.00 AGI Super Brain Control"),
        BotCommand("menu", "🎛️ v13.00 Interactive Control Keyboard"),
        BotCommand("balance", "💰 Spot, Futures & Gold Vault Balance"),
        BotCommand("portfolio", "💼 Active Positions & Delta-Neutral PnL"),

        # 2. 6 Super Smart Wall Street Engines
        BotCommand("hyper_trade", "🚀 Sub-5ms HFT Orderbook CVD Scalper"),
        BotCommand("auto_arb", "⚡ Delta-Neutral 0% Risk Arbitrage"),
        BotCommand("sweep_auto", "🛡️ Liquidity Sweep Bottom Wick Sniper"),
        BotCommand("funding_harvester", "🌾 30%-120% APY Perpetual Funding Yield"),
        BotCommand("trailing_guard", "🛡️ Auto-Liquidation Guard & Trailing Lock"),

        # 3. AI Quant Trading Strategies
        BotCommand("turbo_hedge", "🚀 Turbo Hedge Futures 5x/15x Engine"),
        BotCommand("infinity_matrix", "♾️ Smart Grid 100% Profit Compounding"),
        BotCommand("smart_dca", "🎯 HMM Regime Smart DCA Martingale"),
        BotCommand("grid_bot", "📊 24/7 Smart Grid Trading Engine"),

        # 4. 16-Model AI Super Brain & Market Intel
        BotCommand("analyze", "🧠 5-Agent AGI Swarm Market Analysis"),
        BotCommand("predict", "📈 Wall Street 16-Model ML Prediction"),
        BotCommand("moe_route", "🔀 MoE Router Dynamic AI Classifier"),
        BotCommand("gold_radar", "🏆 PAXG Gold Wealth Protection Radar"),
        BotCommand("whales", "🐋 On-Chain Whale Front-Running Radar"),
        BotCommand("news", "📰 Nano-NLP Firehose & News Impact Alerts"),

        # 5. Emergency Stop & Circuit Breaker
        BotCommand("stop", "🛑 Emergency Circuit Breaker & Close All"),
    ]

    admin_commands = [
        BotCommand("admin", "👑 Super Admin v13.00 Control Panel"),
        BotCommand("health", "🩺 VPS Hardware, RAM & Engine Diagnostics"),
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
