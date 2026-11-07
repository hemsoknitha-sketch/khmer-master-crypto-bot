# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD & TELEGRAM BOT 24/7/365 LAUNCHER (AQ84)
=================================================================
Target: Google Cloud Linux VPS 'quant-gold' (us-central1-a, quant-gold-514007)
Author: HEM SINATH | Institutional Quantitative Governance
Version: 1.0.0

Purpose:
  Launches the full Angkor Quant & Quant Gold Telegram Bot & AI Trading Engine
  in 24/7 Headless VPS Mode (--cli).
  Ensures:
    1. Telegram Bot polls and responds instantly to /start, /capital, /capital gold.
    2. Interactive 1-tap inline buttons and callbacks are 100% active.
    3. 24/7 Background Scheduler runs Quant Gold 19-TF execution engine.
    4. Clean signal handling for zero-downtime Systemd restarts.
=================================================================
"""

import os
import sys
import signal
import threading

# Force headless CLI mode for VPS
if "--cli" not in sys.argv:
    sys.argv.append("--cli")

# Set line-buffered UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
    except Exception:
        pass

_DIR = os.path.dirname(os.path.abspath(__file__))
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

_QG_DIR = os.path.join(_DIR, "Quant Gold")
if _QG_DIR not in sys.path:
    sys.path.insert(0, _QG_DIR)

from dotenv import load_dotenv

def main():
    # Load environment variables (.env)
    env_paths = [
        os.path.join(_DIR, ".env"),
        os.path.join(_QG_DIR, ".env"),
        ".env"
    ]
    for p in env_paths:
        if os.path.exists(p):
            load_dotenv(p)
            break

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not bot_token or bot_token == "your_telegram_bot_token_here":
        print("❌ Error: TELEGRAM_BOT_TOKEN is missing in .env! Please update your .env file.")
        sys.exit(1)

    print("=" * 72)
    print("  🥇 ANGKOR QUANT - QUANT GOLD & TELEGRAM BOT RUNNING 24/7/365")
    print("  📍 Mode: Pure Headless VPS Daemon (--cli)")
    print("  🤖 Telegram Polling: ACTIVE (Responding to /start, /capital, /capital gold)")
    print("  📈 Quant Gold Engine: 19-TF Confluence & AI Swarm ACTIVE")
    print("=" * 72)

    import database as db
    db.init_db()

    from ai_engine import AIInvestmentEngine
    from bot_thread import TelegramBotThread
    from standalone_runner import QuantGoldDaemon

    # 1. Start Autonomous Quant Gold 19-TF Cycle in dedicated thread
    gold_daemon = QuantGoldDaemon()

    def run_gold_daemon():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(gold_daemon.run())
        except Exception as e_daemon:
            print(f"⚠️ [QUANT GOLD DAEMON BACKGROUND EXCEPTION]: {e_daemon}")

    daemon_thread = threading.Thread(target=run_gold_daemon, daemon=True, name="QuantGoldAutonomousThread")
    daemon_thread.start()
    print("🥇 [AUTONOMOUS ENGINE] Quant Gold 19-TF 24/7 autonomous daemon started in background thread.")

    # 2. Initialize Telegram Bot Thread
    ai_engine = AIInvestmentEngine(api_key=gemini_key)
    bot_service = TelegramBotThread(bot_token, ai_engine)

    def sig_handler(signum, frame):
        print(f"\n🛑 Shutdown signal ({signum}) received. Stopping Bot gracefully...")
        gold_daemon.is_running = False
        bot_service.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    print("🛡️ [24/7 VPS ENGINE] Telegram Bot polling active. Ready for user commands!")
    bot_service.run()

if __name__ == "__main__":
    main()
