import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Bot, BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeChat
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
        
        # Crucial: Purge custom chat scope commands for all admin chat IDs
        try:
            admins = db.get_all_admins()
            for admin_id in admins:
                try:
                    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=admin_id))
                    print(f"  └─ Purged custom BotCommandScopeChat for Admin: {admin_id}")
                except Exception:
                    pass
        except Exception:
            pass
            
        print("  └─ Cleaned default, private, group, and admin chat command scopes!")
    except Exception as e_del:
        print(f"  └─ Delete notice: {e_del}")

    commands = [
        BotCommand("start", "🚀 Start Bot & Choose Language"),
        BotCommand("menu", "🎛️ Interactive Master Control Panel"),
        BotCommand("turbo_hedge", "🚀 HFT Multi/Single Trading Engine"),
        BotCommand("infinity_grid", "♾️ Unified Smart Grid Engine"),
        BotCommand("snipe", "🎯 Listing & Volatility Sniper"),
        BotCommand("funding_harvester", "🌾 8-Hour Funding Yield Harvester"),
        BotCommand("gold_radar", "🛡️ AI Gold Guard & Macro Radar"),
        BotCommand("analyze", "🧠 5-Agent AGI Market Analysis"),
        BotCommand("predict", "📈 Wall Street ML 24h Prediction"),
        BotCommand("balance", "💰 Check Spot & Futures Balance"),
        BotCommand("status", "📊 View Active Trades & PnL"),
        BotCommand("health", "🩺 Check VPS & Engine Diagnostics"),
        BotCommand("sync_brain", "📦 Hot-Reload AI Models from Cloud"),
        BotCommand("whales", "🐋 Track On-Chain Whale Movements"),
        BotCommand("news", "📰 3-Paragraph Journalistic Crypto News"),
        BotCommand("top", "🔥 Top Volatile Gainers & Losers"),
        BotCommand("alert", "🔔 Set Price Alert"),
        BotCommand("stop", "🛑 Stop Trading / Market Close"),
    ]
    
    print("✨ [2/3] Registering 18 clean v12.00 Flagship Commands...")
    try:
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
        await bot.set_my_commands(commands, scope=BotCommandScopeAllPrivateChats())
        print("  └─ Registered for Default and All Private Chats scopes!")
    except Exception as e_set:
        print(f"  └─ Error setting commands: {e_set}")

    print("🎉 [3/3] TELEGRAM BOT MENU FORCE RESET SUCCESSFUL!")

if __name__ == "__main__":
    asyncio.run(force_reset_menu())
