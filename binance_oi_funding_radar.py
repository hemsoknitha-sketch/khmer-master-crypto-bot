"""
Khmer Master Crypto - Binance Futures OI & Funding Rate Squeeze Radar (Pillar 3)
Document Version: 1.0.0 (Institutional Ground Truth)
Authority: Architectural Specification Lock

Analyzes real-time Open Interest (OI) and Funding Rate positioning on Binance Futures
to detect institutional squeeze traps and liquidation cascades:
1. Extreme Positive Funding (>= +0.05%): Over-leveraged retail Longs. High risk of Long Liquidation Dump.
   -> Enforces Long-entry block to prevent buying into top liquidation cascades.
2. Extreme Negative Funding (<= -0.04%): Crowded retail Shorts paying high fees to Longs.
   -> Blocks Shorting into bottom liquidity traps and triggers Short-Squeeze Long breakout bias.
"""

import time
import logging
import requests
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger("BinanceOIFundingRadar")

# High-speed cache: symbol -> (cached_ts, radar_dict)
_RADAR_CACHE: Dict[str, Any] = {}
_CACHE_TTL_SECONDS = 30.0

HIGH_FUNDING_THRESHOLD_PCT = 0.05   # +0.05% per 8h
NEGATIVE_FUNDING_THRESHOLD_PCT = -0.04  # -0.04% per 8h


def get_binance_futures_market_regime(symbol: str = "BTCUSDT") -> Dict[str, Any]:
    """
    Fetches real-time Funding Rate and Open Interest for a Binance Futures contract.
    Cached for 30 seconds for sub-millisecond execution loops.
    """
    global _RADAR_CACHE
    now = time.time()
    sym_u = symbol.upper()

    if sym_u in _RADAR_CACHE:
        cached_ts, cached_data = _RADAR_CACHE[sym_u]
        if now - cached_ts < _CACHE_TTL_SECONDS:
            return cached_data

    # Default institutional baseline
    res_data = {
        "symbol": sym_u,
        "funding_rate_pct": 0.01,
        "open_interest": 0.0,
        "squeeze_regime": "NEUTRAL",
        "block_longs": False,
        "block_shorts": False,
        "squeeze_boost_direction": "NONE",
        "advisory": "Normal funding conditions",
        "timestamp": now
    }

    try:
        # 1. Fetch current funding rate
        fr_url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={sym_u}&limit=1"
        fr_res = requests.get(fr_url, timeout=4)
        if fr_res.status_code == 200:
            fr_json = fr_res.json()
            if fr_json and len(fr_json) > 0:
                raw_fr = float(fr_json[0].get("fundingRate", 0.0001))
                fr_pct = round(raw_fr * 100.0, 4)
                res_data["funding_rate_pct"] = fr_pct

        # 2. Fetch Open Interest
        oi_url = f"https://fapi.binance.com/fapi/v1/openInterest?symbol={sym_u}"
        oi_res = requests.get(oi_url, timeout=4)
        if oi_res.status_code == 200:
            oi_json = oi_res.json()
            res_data["open_interest"] = float(oi_json.get("openInterest", 0.0))

        # 3. Analyze Crowded Positioning & Squeeze Risk
        fr_pct = res_data["funding_rate_pct"]
        if fr_pct >= HIGH_FUNDING_THRESHOLD_PCT:
            res_data["squeeze_regime"] = "EXTREME_LONG_CROWDED"
            res_data["block_longs"] = True
            res_data["squeeze_boost_direction"] = "SHORT"
            res_data["advisory"] = f"Crowded Longs (FR: +{fr_pct:.4f}%). High Long Squeeze Dump risk. Longs blocked."
            logger.warning(f"⚠️ [OI RADAR] {sym_u} Extreme Positive Funding (+{fr_pct:.4f}%). Longs blocked.")
        elif fr_pct <= NEGATIVE_FUNDING_THRESHOLD_PCT:
            res_data["squeeze_regime"] = "EXTREME_SHORT_CROWDED"
            res_data["block_shorts"] = True
            res_data["squeeze_boost_direction"] = "LONG"
            res_data["advisory"] = f"Crowded Shorts (FR: {fr_pct:.4f}%). High Short Squeeze Pump risk. Shorts blocked."
            logger.info(f"💎 [OI RADAR] {sym_u} Extreme Negative Funding ({fr_pct:.4f}%). Shorts blocked; Short Squeeze Long favored.")
    except Exception as e:
        logger.debug(f"Binance OI Radar query note for {sym_u}: {e}")

    _RADAR_CACHE[sym_u] = (now, res_data)
    return res_data


def validate_crypto_trade_against_funding_radar(symbol: str, direction: str) -> Tuple[bool, str]:
    """
    Validates a proposed directional crypto trade against live funding rate extremes.
    Returns (is_allowed: bool, reason: str).
    """
    regime = get_binance_futures_market_regime(symbol)
    dir_u = direction.upper()

    if dir_u in ["BUY", "LONG"] and regime.get("block_longs"):
        return False, regime.get("advisory", "Blocked: Extreme positive funding rate (Long squeeze risk)")

    if dir_u in ["SELL", "SHORT"] and regime.get("block_shorts"):
        return False, regime.get("advisory", "Blocked: Extreme negative funding rate (Short squeeze risk)")

    return True, "Passed Funding Squeeze Guard"
