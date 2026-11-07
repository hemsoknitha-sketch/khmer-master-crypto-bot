# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD 24/7/365 PURE GOLD LAUNCHER (AQ84)
=============================================================
Target: Google Cloud Linux VPS 'quant-gold' (us-central1-a, quant-gold-514007)
Author: HEM SINATH | Institutional Quantitative Governance
Version: 2.0.0

Purpose:
  Dedicated launcher for the 100% PURE Quant Gold Engine & Telegram Bot.
  Completely bypasses all legacy crypto background jobs:
    - ZERO Binance WebSockets (eliminates HTTP 451 legal errors on US VPS)
    - ZERO Solana Smart Swap
    - ZERO CSX Cambodia Stock Exchange
    - ZERO MT5 wine bridge watchdog warnings
    - ZERO generic crypto multi-engine /start welcome menu
  Launches the pure, institutional Quant Gold Bot & 19-TF Autonomous Cycle!
=============================================================
"""

import os
import sys

# Force headless CLI mode
if "--cli" not in sys.argv:
    sys.argv.append("--cli")

# Set line-buffered UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
    except Exception:
        pass

_DIR = os.path.dirname(os.path.abspath(__file__))
_QG_DIR = os.path.join(_DIR, "Quant Gold")

if _QG_DIR not in sys.path:
    sys.path.insert(0, _QG_DIR)
if _DIR not in sys.path:
    sys.path.insert(1, _DIR)

from main import main as quant_gold_main

if __name__ == "__main__":
    quant_gold_main()
