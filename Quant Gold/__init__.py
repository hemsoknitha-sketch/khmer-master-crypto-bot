# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD ENGINE (AQ84 INSTITUTIONAL GROUND TRUTH)
==================================================================
Package Name: Quant Gold
Specialization: 100% Dedicated Institutional Spot Gold (XAUUSD / Gold) Engine
Hierarchy: 19 Timeframes (M1, M2, M3, M4, M5, M10, M15, M20, M30, M45, H1, H2, H3, H4, H6, H8, D1, W1, MN)
AI Infrastructure: Google Gemini Flash + Hugging Face Serverless (DeepSeek-R1, Llama-3-70B, Qwen-2.5) via HF_TOKEN
Mathematical Disciplines: Multi-Scale Hurst, 2D Kalman Filter, Ornstein-Uhlenbeck, Hawkes Point Process, SGE-LBMA Arbitrage, Conformal Prediction
Risk Management: Structural Invalidation SL, Breakeven Armor (+2.5R), 3-Stage Scale-Out, Shock Early Harvest, Adaptive Post-Loss Re-Study
==================================================================
"""

import os
import sys

# Ensure package root is importable
_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
if _PKG_DIR not in sys.path:
    sys.path.insert(0, _PKG_DIR)

__version__ = "1.0.0"
__asset__ = "GOLD"
__canonical_symbol__ = "XAUUSD"

try:
    from .timeframes import (
        TIMEFRAMES_19,
        GoldMultiTimeframeEngine,
        get_gold_mtf_engine
    )
    from .mathematical_engine import (
        GoldMathematicalCore,
        get_gold_math_core
    )
    from .ai_models import (
        GoldAISwarmEngine,
        get_gold_ai_swarm
    )
    from .execution_engine import (
        QuantGoldExecutionEngine,
        get_quant_gold_execution_engine
    )
    from .capital_gold_bridge import (
        QuantGoldCapitalBridge,
        get_quant_gold_capital_bridge
    )
except (ImportError, ValueError):
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
