#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD TELEGRAM BOT COMMANDS SYNCHRONIZER WRAPPER (AQ84)
===========================================================================
Delegates execution directly to 'Quant Gold/sync_telegram_commands.py'.
Auto-bootstraps into the virtual environment (venv) to prevent ModuleNotFoundError.
===========================================================================
"""

import os
import sys

# 0. Auto-relaunch inside virtual environment if available (prevents ModuleNotFoundError)
if "venv" not in sys.executable:
    for candidate in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python3"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python"),
        "/opt/khmer-master-crypto-bot/venv/bin/python3",
        "/opt/khmer-master-crypto-bot/venv/bin/python",
    ]:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            os.execv(candidate, [candidate] + sys.argv)

_DIR = os.path.dirname(os.path.abspath(__file__))
_TARGET = os.path.join(_DIR, "Quant Gold", "sync_telegram_commands.py")

if os.path.exists(_TARGET):
    with open(_TARGET, "r", encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, _TARGET, "exec"), globals())
else:
    print(f"❌ Target not found: {_TARGET}")
