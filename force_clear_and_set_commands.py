import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Bot, BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators, BotCommandScopeChat
import database as db

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

async def force_reset_menu():
    if not TOKEN:
        print("[ERROR] TELEGRAM_BOT_TOKEN missing in .env!")
        return

    bot = Bot(token=TOKEN)
    
    print("🧹 [1/3] Deleting old cached commands from all Telegram scopes & Admin chat scopes...")
    try:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
        await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
        await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
        await bot.delete_my_commands(scope=BotCommandScopeAllChatAdministrators())
        
        try:
            all_users = db.get_vip_users_with_lang()
            for u in all_users:
                u_id = u[0] if isinstance(u, (tuple, list)) else u
                if u_id != 859271875:
                    try:
                        await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=int(u_id)))
                    except Exception:
                        pass
        except Exception:
            pass
            
        print("  └─ Cleaned default, private, group, and VIP chat command scopes!")
    except Exception as e_del:
        print(f"  └─ Delete notice: {e_del}")

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
        BotCommand("health", "🩺 Check VPS Hardware & Engine Diagnostics"),
        BotCommand("sync_brain", "📦 Hot-Reload AI Models from Cloud"),
    ] + public_commands

    print("✨ [2/3] Registering v12.00 Public VIP Commands (with 6 Flagship Engines)...")
    try:
        await bot.set_my_commands(public_commands, scope=BotCommandScopeDefault())
        await bot.set_my_commands(public_commands, scope=BotCommandScopeAllPrivateChats())
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=859271875))
        except Exception:
            pass
        print("  └─ Registered for Default and All Private Chats scopes + Super Admin Scope!")
    except Exception as e_set:
        print(f"  └─ Error setting commands: {e_set}")

    print("🎉 [3/3] TELEGRAM BOT MENU FORCE RESET SUCCESSFUL!")

if __name__ == "__main__":
    asyncio.run(force_reset_menu())
