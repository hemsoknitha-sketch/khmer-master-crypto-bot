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

    import bot_commands_registry
    public_commands = bot_commands_registry.get_public_bot_commands()
    admin_commands = bot_commands_registry.get_admin_bot_commands()

    print("✨ [2/3] Registering v13.00 Absolute Ultimate AGI Public VIP Commands...")
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
