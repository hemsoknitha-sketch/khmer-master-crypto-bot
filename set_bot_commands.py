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
    import bot_commands_registry
    public_commands = bot_commands_registry.get_public_bot_commands()
    admin_commands = bot_commands_registry.get_admin_bot_commands()


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
