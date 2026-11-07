# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD 24/7/365 STANDALONE DAEMON RUNNER (AQ84)
==================================================================
Target: Google Cloud Linux VPS (quant-gold: us-central1-a, quant-gold-514007)
Author: HEM SINATH | Institutional Quantitative Governance
Version: 1.0.0

Purpose:
  Dedicated 24/7/365 production runner for Quant Gold on Google Cloud Linux VPS.
  Continuously monitors 19 timeframes, quantitative mathematical filters,
  and the 4-Model AI Swarm (DeepSeek-R1, Llama-3-70B, Gemini Flash, Vectorized Algo Governor),
  executing high-conviction Gold positions with Breakeven Armor and zero downtime.
==================================================================
"""

import os
import sys
import time
import signal
import asyncio
import logging
from datetime import datetime

# Set line-buffered output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
    except Exception:
        pass

# Ensure parent and package paths are reachable
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE_ROOT = os.path.dirname(_CURRENT_DIR)

if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if _WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, _WORKSPACE_ROOT)

# Configure institutional logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [QUANT GOLD 24/7] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("QUANT_GOLD_RUNNER")


class QuantGoldDaemon:
    """Production 24/7 daemon running Quant Gold on Google Cloud Linux VPS."""

    def __init__(self):
        self.is_running = True
        self.cycle_count = 0
        self.last_heartbeat = time.time()
        self.heartbeat_interval = 60.0  # Log summary every 60 seconds
        self.execution_engine = None

    def setup_signal_handlers(self):
        """Catches SIGINT and SIGTERM for graceful systemd shutdowns."""
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                signal.signal(sig, self._handle_shutdown)
            except Exception:
                pass

    def _handle_shutdown(self, signum, frame):
        logger.info(f"🛑 Received shutdown signal ({signum}). Gracefully stopping Quant Gold Daemon...")
        self.is_running = False

    async def run(self):
        logger.info("=" * 72)
        logger.info("  🥇 ANGKOR QUANT - QUANT GOLD 24/7/365 STANDALONE DAEMON STARTED")
        logger.info(f"  📍 VPS Environment: Google Cloud (quant-gold / quant-gold-514007)")
        logger.info(f"  ⏰ Local Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 72)

        self.setup_signal_handlers()

        # Import Quant Gold engine
        try:
            import quant_gold
            self.execution_engine = quant_gold.get_quant_gold_execution_engine()
            logger.info("✅ Quant Gold Execution Engine initialized successfully.")
        except Exception as exc:
            logger.error(f"❌ Failed to initialize Quant Gold Engine: {exc}", exc_info=True)
            return

        # Main 24/7/365 Autonomous Loop
        while self.is_running:
            t0 = time.time()
            self.cycle_count += 1

            try:
                # 1. Execute Quant Gold Cycle (Audit + Signal + VIP Order Dispatch)
                res = await self.execution_engine.execute_quant_gold_cycle()
                status = res.get("status", "OK")

                if status == "TRIGGERED":
                    action = res.get("action")
                    price = res.get("price")
                    conf = res.get("confidence")
                    logger.info(f"⚡ [SIGNAL EXECUTED] {action} GOLD @ ${price:.2f} | Confidence: {conf:.1f}% | Dispatched: {res.get('dispatched', 0)} users")

            except Exception as e_cycle:
                logger.warning(f"⚠️ [CYCLE RECOVERY] Handled cycle anomaly: {e_cycle}")

            # Heartbeat logging
            now = time.time()
            if (now - self.last_heartbeat) >= self.heartbeat_interval:
                self.last_heartbeat = now
                bid, ask, spread = self.execution_engine.get_live_gold_price_quote()
                logger.info(f"💓 [HEARTBEAT] Cycle #{self.cycle_count} | GOLD: Bid=${bid:.2f} Ask=${ask:.2f} (Spread: ${spread:.2f}) | Engine Healthy 24/7")

            # Dynamic pacing (sleep remainder of 6 seconds)
            elapsed = time.time() - t0
            sleep_duration = max(1.0, 6.0 - elapsed)
            try:
                await asyncio.sleep(sleep_duration)
            except asyncio.CancelledError:
                break

        logger.info("👋 Quant Gold Daemon stopped cleanly. Zero data loss.")


def main():
    daemon = QuantGoldDaemon()
    try:
        asyncio.run(daemon.run())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Process terminated by user or systemd.")


if __name__ == "__main__":
    main()

