#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD TELEGRAM BOT COMMANDS SYNCHRONIZER (AQ84)
==================================================================
Location: Quant Gold/sync_telegram_commands.py
Forces full synchronization of clean Quant Gold commands to Telegram API server:
- Deletes stale commands from BotCommandScopeDefault, BotCommandScopeAllPrivateChats,
  BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators, and BotCommandScopeChat(859271875).
- Registers the 14 official Quant Gold commands to Default & AllPrivateChats.
- Registers dedicated Admin commands to Super Admin Chat (859271875).
==================================================================
"""

import os
import sys
import asyncio

# 0. Auto-relaunch inside virtual environment if available (prevents ModuleNotFoundError)
if "venv" not in sys.executable:
    for candidate in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "venv", "bin", "python3"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "venv", "bin", "python"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python3"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python"),
        "/opt/khmer-master-crypto-bot/venv/bin/python3",
        "/opt/khmer-master-crypto-bot/venv/bin/python",
    ]:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            os.execv(candidate, [candidate] + sys.argv)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure paths
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE_ROOT = os.path.dirname(_CURRENT_DIR)
for p in [_CURRENT_DIR, _WORKSPACE_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Load .env
for env_f in [os.path.join(_CURRENT_DIR, ".env"), os.path.join(_WORKSPACE_ROOT, ".env")]:
    if os.path.exists(env_f):
        try:
            with open(env_f, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip("'").strip('"'))
        except Exception:
            pass

from telegram import (
    Bot,
    BotCommand,
    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeChat
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()


async def sync_menu():
    if not TOKEN:
        print("❌ [ERROR] TELEGRAM_BOT_TOKEN not found in environment!")
        return

    bot = Bot(token=TOKEN)
    me = await bot.get_me()
    print(f"🤖 Connected to Bot: @{me.username} (ID: {me.id})")

    # Define clean Quant Gold public commands for all users
    commands = [
        BotCommand("start", "🥇 Open Quant Gold Dashboard & 19-TF Spectrum"),
        BotCommand("signal", "🎯 View Current Super Smart Gold Signal & Levels"),
        BotCommand("capital", "🏛️ Capital.com Live Gold Trading Deck"),
        BotCommand("auto", "🤖 Toggle 24/7 Autonomous Gold Trading"),
        BotCommand("status", "💵 Live Gold Price, Spread & Capital Session"),
        BotCommand("help", "📖 User Guide & Fiduciary Covenant")
    ]

    # Dedicated Admin commands for Super Admin scope ONLY (859271875 @Soknitha)
    admin_commands = list(commands) + [
        BotCommand("health", "🖥️ Google Cloud VPS System Health & Latency"),
        BotCommand("security", "🛡️ View Institutional Security Citadel Status"),
        BotCommand("admin_users", "👥 Inspect & Manage All Users Dossiers"),
        BotCommand("admin_capital", "👑 Super Admin Capital.com Fleet Controller"),
        BotCommand("admin_license", "👑 VIP License Approvals & Database Pruning"),
        BotCommand("emergency_stop", "🚨 Super Admin Emergency Trading Freeze"),
        BotCommand("unlock", "🟢 Super Admin Release Trading Freeze")
    ]

    print("🧹 [1/3] Deleting stale commands from all scopes & Admin chat scopes...")
    for scope in [
        BotCommandScopeDefault(),
        BotCommandScopeAllPrivateChats(),
        BotCommandScopeAllGroupChats(),
        BotCommandScopeAllChatAdministrators()
    ]:
        try:
            await bot.delete_my_commands(scope=scope)
        except Exception as e:
            print(f"  └─ Delete scope notice: {e}")

    for admin_id in [859271875, 537186806]:
        try:
            await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=admin_id))
            print(f"  └─ Wiped custom scope for Admin {admin_id}")
        except Exception:
            pass

    print("✨ [2/3] Setting clean 14 Quant Gold commands...")
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_my_commands(commands, scope=BotCommandScopeAllPrivateChats())
    print("  └─ Registered for Default and All Private Chats.")

    for admin_id in [859271875]:
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin_id))
            print(f"  └─ Registered 15 commands for Super Admin {admin_id}.")
        except Exception as e:
            print(f"  └─ Admin set notice: {e}")

    print("🔍 [3/3] Verifying active commands on Telegram API...")
    admin_active = await bot.get_my_commands(scope=BotCommandScopeChat(chat_id=859271875))
    print(f"  └─ Active commands for Super Admin (859271875): {len(admin_active)} commands")
    for c in admin_active:
        print(f"     /{c.command} - {c.description}")

    print("=" * 70)
    print("🎉 SUCCESS! Quant Gold Bot Commands are 100% synchronized with Telegram!")
    print("======================================================================")


if __name__ == "__main__":
    asyncio.run(sync_menu())
