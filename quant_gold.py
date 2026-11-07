# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD ROOT SHIM & FACADE
============================================
Allows standard Python imports:
  import quant_gold
  from quant_gold import QuantGoldExecutionEngine, get_quant_gold_execution_engine
Pointing directly to the 'Quant Gold' package directory.
============================================
"""

import os
import sys
import importlib.util

# Load the package from "Quant Gold" folder
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PKG_DIR = os.path.join(_CURRENT_DIR, "Quant Gold")

if _PKG_DIR not in sys.path:
    sys.path.insert(0, _PKG_DIR)

__version__ = "1.0.0"
__asset__ = "GOLD"
__canonical_symbol__ = "XAUUSD"

from timeframes import (
    TIMEFRAMES_19,
    GoldMultiTimeframeEngine,
    get_gold_mtf_engine
)

from mathematical_engine import (
    GoldMathematicalCore,
    get_gold_math_core
)

from ai_models import (
    GoldAISwarmEngine,
    get_gold_ai_swarm
)

from execution_engine import (
    QuantGoldExecutionEngine,
    get_quant_gold_execution_engine
)

from capital_gold_bridge import (
    QuantGoldCapitalBridge,
    get_quant_gold_capital_bridge
)

__all__ = [
    "TIMEFRAMES_19",
    "GoldMultiTimeframeEngine",
    "get_gold_mtf_engine",
    "GoldMathematicalCore",
    "get_gold_math_core",
    "GoldAISwarmEngine",
    "get_gold_ai_swarm",
    "QuantGoldExecutionEngine",
    "get_quant_gold_execution_engine",
    "QuantGoldCapitalBridge",
    "get_quant_gold_capital_bridge"
]
