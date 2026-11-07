# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD ENTRYPOINT LAUNCHER
==============================================
Convenient root launcher for Quant Gold 24/7 standalone runner.
Usage:
  python run_quant_gold.py
"""

import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

_QG_DIR = os.path.join(_DIR, "Quant Gold")
if _QG_DIR not in sys.path:
    sys.path.insert(0, _QG_DIR)

from standalone_runner import main

if __name__ == "__main__":
    main()

