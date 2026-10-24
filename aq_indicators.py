# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - UNIFIED QUANTITATIVE INDICATORS AND FAST RAM CACHE
Module: aq_indicators.py
Author: Angkor Quant Institutional Infrastructure
Standard: The 84 Pillars and Sub-Microsecond RAM Data Access
Vectorized Technical Indicator Computation and Global RAM Cache
"""

import math
import operator
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

_RAM_PRICE_REGISTRY: Dict[str, Dict[str, float]] = {}


def register_ram_tick(symbol: str, bid: float, ask: float, timestamp: float) -> None:
    """Updates the high-speed RAM market price cache with sub-microsecond latency."""
    clean_sym = symbol.upper().strip()
    mid_px = operator.mul(operator.add(bid, ask), 0.50)
    spread_val = abs(operator.sub(ask, bid))
    _RAM_PRICE_REGISTRY[clean_sym] = {
        "bid": float(bid),
        "ask": float(ask),
        "mid": float(mid_px),
        "spread": float(spread_val),
        "timestamp": float(timestamp)
    }


def get_fast_ram_price(symbol: str) -> Optional[Dict[str, float]]:
    """Retrieves tick data from RAM cache in O(1) time complexity."""
    return _RAM_PRICE_REGISTRY.get(symbol.upper().strip())


def calculate_vectorized_atr(
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    close_prices: np.ndarray,
    period: int = 14
) -> float:
    """Calculates Wilder Average True Range using vectorized array operations."""
    sample_length = len(high_prices)
    if sample_length < operator.add(period, 1):
        return 0.0

    current_high = high_prices[1:]
    current_low = low_prices[1:]
    previous_close = close_prices[:-1]

    tr_high_low = current_high - current_low
    tr_high_prev = np.abs(current_high - previous_close)
    tr_low_prev = np.abs(current_low - previous_close)

    true_range = np.maximum(tr_high_low, np.maximum(tr_high_prev, tr_low_prev))
    atr_values = np.zeros(len(true_range))
    atr_values[operator.sub(period, 1)] = float(np.mean(true_range[:period]))

    alpha = 1.0 / float(period)
    one_minus_alpha = operator.sub(1.0, alpha)

    for idx in range(period, len(true_range)):
        prev_atr = atr_values[operator.sub(idx, 1)]
        new_val = operator.add(
            operator.mul(true_range[idx], alpha),
            operator.mul(prev_atr, one_minus_alpha)
        )
        atr_values[idx] = new_val

    return float(atr_values[-1])


def calculate_vectorized_ema(series_data: np.ndarray, period: int = 20) -> float:
    """Calculates Exponential Moving Average with O(N) array slicing."""
    if len(series_data) < period:
        return float(np.mean(series_data)) if len(series_data) > 0 else 0.0

    multiplier = 2.0 / float(operator.add(period, 1))
    one_minus_mult = operator.sub(1.0, multiplier)
    ema_current = float(np.mean(series_data[:period]))

    for price in series_data[period:]:
        ema_current = operator.add(
            operator.mul(price, multiplier),
            operator.mul(ema_current, one_minus_mult)
        )

    return float(ema_current)
