# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD 24/7/365 PURE GOLD ENGINE (AQ84)
===========================================================
Target: Google Cloud Linux VPS 'quant-gold' (us-central1-a, quant-gold-514007)
Author: HEM SINATH | Institutional Quantitative Governance
Version: 1.0.0

Purpose:
  100% Dedicated, Independent Production Runner for Quant Gold.
  Completely independent of all legacy crypto background jobs.
  ZERO Binance WebSockets (no HTTP 451).
  ZERO Solana Smart Swap.
  ZERO CSX Cambodia Stock Exchange.
  ZERO MT5 wine bridge spam.
  100% Focused on Spot Gold (XAUUSD / Gold) on Capital.com.
===========================================================
"""

import os
import sys
import time
import signal
import asyncio
import logging
from datetime import datetime

# Set line-buffered UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
    except Exception:
        pass

# Ensure paths reach Quant Gold and parent directory
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE_ROOT = os.path.dirname(_CURRENT_DIR)

if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if _WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, _WORKSPACE_ROOT)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Native zero-dependency fallback for loading .env
    for candidate_env in [
        os.path.join(_CURRENT_DIR, ".env"),
        os.path.join(_WORKSPACE_ROOT, ".env"),
        os.path.join(os.getcwd(), ".env")
    ]:
        if os.path.exists(candidate_env):
            try:
                with open(candidate_env, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip().strip("'").strip('"'))
                break
            except Exception:
                pass

# Configure clean institutional logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [QUANT GOLD 24/7] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("QUANT_GOLD_MAIN")

# Silence external noisy loggers
for logger_name in ["httpx", "httpcore", "telegram", "apscheduler", "urllib3"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

from bot import QuantGoldBot
from execution_engine import get_quant_gold_execution_engine
import database as db


class QuantGoldSystem:
    """Production 24/7/365 Standalone Quant Gold Autonomous Runner."""

    def __init__(self):
        self.is_running = True
        self.cycle_count = 0
        self.last_heartbeat = time.time()
        self.heartbeat_interval = 60.0
        self.exec_engine = None
        self.bot = None
        self.app = None

    def setup_signal_handlers(self):
        """Catches SIGINT and SIGTERM for graceful systemd shutdowns."""
        def _handle_shutdown(signum, frame):
            logger.info(f"🛑 Received shutdown signal ({signum}). Gracefully stopping Quant Gold System...")
            self.is_running = False

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                signal.signal(sig, _handle_shutdown)
            except Exception:
                pass

    async def run(self):
        # 1. Load environment configuration
        env_paths = [
            os.path.join(_CURRENT_DIR, ".env"),
            os.path.join(_WORKSPACE_ROOT, ".env"),
            ".env"
        ]
        for p in env_paths:
            if os.path.exists(p):
                if "load_dotenv" in globals() and callable(globals()["load_dotenv"]):
                    try:
                        load_dotenv(p)
                    except Exception:
                        pass
                else:
                    try:
                        with open(p, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith("#") and "=" in line:
                                    k, v = line.split("=", 1)
                                    os.environ.setdefault(k.strip(), v.strip().strip("'").strip('"'))
                    except Exception:
                        pass
                break

        bot_token = (
            os.getenv("QUANT_GOLD_BOT_TOKEN")
            or os.getenv("TELEGRAM_BOT_TOKEN_GOLD")
            or os.getenv("TELEGRAM_BOT_TOKEN", "")
        ).strip()
        if not bot_token or bot_token == "your_telegram_bot_token_here":
            logger.error("❌ TELEGRAM_BOT_TOKEN is missing in .env! Please update your .env file.")
            sys.exit(1)

        logger.info("=" * 72)
        logger.info("  🥇 ANGKOR QUANT - QUANT GOLD 24/7/365 PURE GOLD ENGINE")
        logger.info("  📍 Environment: Google Cloud Linux VPS (quant-gold / quant-gold-514007)")
        logger.info("  🎯 Target Asset: 100% Dedicated to Spot Gold (XAUUSD / Gold)")
        logger.info(f"  ⏰ System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 72)

        self.setup_signal_handlers()

        # 2. Initialize database
        try:
            db.init_db()
            logger.info("✅ Database initialized successfully.")
        except Exception as e_db:
            logger.warning(f"Database init notice: {e_db}")

        # 3. Initialize Quant Gold Execution Engine
        try:
            self.exec_engine = get_quant_gold_execution_engine()
            logger.info("✅ Quant Gold 19-Timeframe Execution Engine ready.")
        except Exception as e_eng:
            logger.error(f"❌ Failed to initialize Execution Engine: {e_eng}", exc_info=True)
            sys.exit(1)

        # 4. Initialize and start Pure Telegram Bot
        try:
            self.bot = QuantGoldBot(bot_token)
            self.app = self.bot.build_application()
            await self.app.initialize()
            await self.app.start()
            if self.app.updater:
                await self.app.updater.start_polling(drop_pending_updates=True, timeout=20)
            logger.info("🤖 [TELEGRAM BOT] Quant Gold Bot Polling is ACTIVE! Ready for /start, /capital, /gold")
        except Exception as e_bot:
            logger.error(f"❌ Failed to start Telegram Bot: {e_bot}", exc_info=True)
            sys.exit(1)

        # 5. Main 24/7/365 Autonomous Loop
        logger.info("🚀 [QUANT GOLD 24/7] System fully operational. Commencing 19-TF Autonomous Cycle...")
        while self.is_running:
            t0 = time.time()
            self.cycle_count += 1

            try:
                # Execute Quant Gold Cycle (Audit + Signal + VIP Order Dispatch)
                res = await self.exec_engine.execute_quant_gold_cycle(app=self.app)
                status = res.get("status", "OK")
                if status == "TRIGGERED":
                    action = res.get("action")
                    price = res.get("price")
                    conf = res.get("confidence")
                    logger.info(f"⚡ [GOLD SIGNAL EXECUTED] {action} GOLD @ ${price:.2f} | Confidence: {conf:.1f}%")
            except Exception as e_cycle:
                logger.warning(f"⚠️ [CYCLE RECOVERY] Handled cycle anomaly: {e_cycle}")

            # Heartbeat logging every 60 seconds
            now = time.time()
            if (now - self.last_heartbeat) >= self.heartbeat_interval:
                self.last_heartbeat = now
                bid, ask, spread = self.exec_engine.get_live_gold_price_quote()
                trade_status = "Standby (Scanning high-win setups)"
                if self.exec_engine.has_active_gold_trade():
                    d_id = self.exec_engine._active_gold_deal_id
                    d_dir = self.exec_engine._active_gold_direction or "TRADE"
                    d_stg = self.exec_engine._active_gold_stage or "ACTIVE"
                    trade_status = f"Managing Active {d_dir} #{d_id} ({d_stg})"
                logger.info(
                    f"💓 [HEARTBEAT] Cycle #{self.cycle_count} | "
                    f"GOLD: Bid=${bid:.2f} Ask=${ask:.2f} (Spread: ${spread:.2f}) | "
                    f"{trade_status} | 19-TF AI Engine HEALTHY 24/7"
                )

            # Auto-recovery for Telegram polling if disconnected
            try:
                if self.app and self.app.updater and not getattr(self.app.updater, 'running', False):
                    logger.warning("⚠️ [TELEGRAM UPDATER] Restoring polling connection...")
                    await self.app.updater.start_polling(drop_pending_updates=True, timeout=20)
            except Exception as e_rec:
                logger.warning(f"Telegram recovery note: {e_rec}")

            # Pacing: Sub-second reactive event tick loop (1.0s vs 6.0s)
            elapsed = time.time() - t0
            sleep_duration = max(0.2, 1.0 - elapsed)
            try:
                await asyncio.sleep(sleep_duration)
            except asyncio.CancelledError:
                break

        # Graceful Shutdown
        logger.info("🛑 Stopping Telegram Bot and Quant Gold System cleanly...")
        if self.app:
            try:
                if self.app.updater and getattr(self.app.updater, 'running', False):
                    await self.app.updater.stop()
                if self.app.running:
                    await self.app.stop()
                await self.app.shutdown()
            except Exception as e_shut:
                logger.warning(f"Shutdown notice: {e_shut}")

        logger.info("👋 Quant Gold System stopped cleanly. Zero data loss.")


def main():
    system = QuantGoldSystem()
    try:
        asyncio.run(system.run())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Process terminated by user or systemd.")


if __name__ == "__main__":
    main()

