import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot, BotCommand

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

async def set_menu_commands():
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN missing in .env!")
        return

    bot = Bot(token=TOKEN)
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
    try:
        await bot.set_my_commands(commands)
        print("✅ [SUCCESS] Telegram Bot Menu updated to 18 clean v12.00 Flagship Commands on Telegram Cloud Servers!")
    except Exception as e:
        print(f"❌ Error setting commands: {e}")

if __name__ == "__main__":
    asyncio.run(set_menu_commands())
