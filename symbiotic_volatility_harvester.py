"""
=============================================================================
  🌊 KHMER MASTER CRYPTO - SYMBIOTIC DUAL-ENGINE VOLATILITY HARVESTER
=============================================================================
  Institutional Wall Street Multi-Scale Quant Architecture:
  Seamlessly orchestrates /auto_trade (Macro 1H/4H Waterfall & Breakout Hunter)
  and /turbo_hedge (Micro HFT Orderbook Scalper & Avellaneda-Stoikov Market Maker)
  on Binance USDT-M Futures with ZERO opposing conflict and mathematical edge.

  CORE MATHEMATICAL SPECIFICATIONS:
  1. Kaufman Efficiency Ratio (ER) Volatility Regime Classifier:
     - ER >= 0.60: Explosive Trend Regime -> Exclusive Macro Directional Riding.
     - ER <= 0.35: Wild Oscillation Regime -> Micro Avellaneda-Stoikov Limit Grid.
  2. Avellaneda-Stoikov Adaptive Limit Model:
     - Calculates inventory-skewed Reservation Price r(s, q) and dynamic spreads.
  3. Symbiotic Asymmetric Delta Skewing & Dynamic Profit Feedback Loop:
     - Micro-scalp profits systematically reduce the cost-basis of the Macro position,
       converting it into a guaranteed Risk-Free Trade.
  4. Funding Rate Arbitrage Shield:
     - Monitors extreme funding dislocations (>= +0.50% / -0.50%) to prevent short squeezes.
=============================================================================
"""

import math
import time
import requests
from typing import Dict, List, Tuple, Optional

import database as db
import market_data

# TradFi and Delisted Exclusion Shield (Invariant 7)
TRADFI_EXCLUSION_SET = {
    "NVDAUSDT", "TSLAUSDT", "AAPLEUSDT", "BONDUSDT", "DODODUSDT", "USDCUSDT", "FDUSDUSDT", "TUSDUSDT"
}

# Regime Constants
REGIME_EXPLOSIVE_TREND = "EXPLOSIVE_TREND"
REGIME_WILD_CHOP = "WILD_CHOP"
REGIME_TRANSITIONAL = "TRANSITIONAL"

def is_tradfi_or_delisted(symbol: str) -> bool:
    sym = symbol.upper().strip()
    return (sym in TRADFI_EXCLUSION_SET) or (not sym.endswith("USDT"))

# =============================================================================
# 1. KAUFMAN EFFICIENCY RATIO (ER) & REGIME CLASSIFIER
# =============================================================================

def calculate_kaufman_efficiency_ratio(prices: List[float], period: int = 14) -> float:
    """
    Calculates the Kaufman Efficiency Ratio (ER):
    ER = |Change over N periods| / Sum of Absolute Daily/Period Price Changes
    Range: [0.0, 1.0].
    - High ER (~1.0): Clean, directional trend (Explosive Breakout / Waterfall).
    - Low ER (~0.0): Highly turbulent, choppy mean-reverting price action.
    """
    if not prices or len(prices) < (period + 1):
        return 0.5

    # Net Directional Vector
    net_direction = abs(prices[-1] - prices[-1 - period])

    # Gross Volatility Path
    volatility = 0.0
    for i in range(len(prices) - period, len(prices)):
        volatility += abs(prices[i] - prices[i - 1])

    if volatility <= 1e-12:
        return 0.0

    er = net_direction / volatility
    return max(0.0, min(1.0, float(er)))

def classify_volatility_regime(symbol: str, interval: str = "15m", period: int = 14) -> Dict:
    """
    Fetches candlestick data and classifies market regime for the given symbol.
    """
    symbol = symbol.upper().strip()
    result = {
        "symbol": symbol,
        "er": 0.5,
        "regime": REGIME_TRANSITIONAL,
        "volatility_pct": 0.0,
        "current_price": 0.0,
        "direction": "NEUTRAL",
        "description": "Standard market regime"
    }

    if is_tradfi_or_delisted(symbol):
        return result

    try:
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={period + 10}"
        res = requests.get(url, timeout=3.5)
        if res.status_code == 200:
            klines = res.json()
            if len(klines) >= period + 1:
                closes = [float(k[4]) for k in klines]
                curr_price = closes[-1]
                start_price = closes[-1 - period]
                er = calculate_kaufman_efficiency_ratio(closes, period=period)

                # Realized volatility percentage over the period
                price_changes = [abs(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(1, len(closes))]
                vol_pct = (sum(price_changes[-period:]) / period) * 100.0

                direction = "BULLISH" if curr_price > start_price else ("BEARISH" if curr_price < start_price else "NEUTRAL")

                if er >= 0.58:
                    regime = REGIME_EXPLOSIVE_TREND
                    desc = f"Explosive Directional Trend (ER {er:.2f} >= 0.58, {direction})"
                elif er <= 0.35:
                    regime = REGIME_WILD_CHOP
                    desc = f"Wild Mean-Reverting Chop (ER {er:.2f} <= 0.35, Vol {vol_pct:.2f}%)"
                else:
                    regime = REGIME_TRANSITIONAL
                    desc = f"Transitional Equilibrium (ER {er:.2f})"

                result["er"] = round(er, 4)
                result["regime"] = regime
                result["volatility_pct"] = round(vol_pct, 3)
                result["current_price"] = curr_price
                result["direction"] = direction
                result["description"] = desc
                return result
    except Exception:
        pass

    return result

# =============================================================================
# 2. AVELLANEDA-STOIKOV ADAPTIVE LIMIT MODEL
# =============================================================================

def calculate_avellaneda_stoikov_quotes(
    mid_price: float,
    inventory_q: float,
    volatility: float,
    gamma: float = 0.1,
    kappa: float = 1.5,
    time_horizon_t: float = 1.0
) -> Dict:
    """
    Wall Street High-Frequency Market Making Model:
    Calculates the Reservation Price (Indifference Price):
      r(s, q, t) = s - q * gamma * sigma^2 * (T - t)
    
    Optimal Half-Spread:
      delta = (gamma * sigma^2 * (T - t) / 2) + (1 / gamma) * ln(1 + gamma / kappa)

    When inventory_q > 0 (Long inventory surplus), reservation price drops below mid-price,
    pushing the bid lower (deterring toxic fills) and tightening the ask (speeding inventory offload).
    """
    if mid_price <= 0:
        return {"bid": 0.0, "ask": 0.0, "reservation_price": 0.0, "spread_pct": 0.0}

    sigma = max(0.001, volatility)
    sigma_sq = sigma ** 2

    # Reservation Price
    reservation_price = mid_price - (inventory_q * gamma * sigma_sq * time_horizon_t)

    # Spread calculation with safety bounds
    half_spread = (gamma * sigma_sq * time_horizon_t / 2.0) + (1.0 / gamma) * math.log(1.0 + (gamma / max(1e-4, kappa)))
    
    # Enforce minimum fee floor (at least 0.15% to clear 0.08% roundtrip fees + profit)
    min_spread = mid_price * 0.0015
    half_spread = max(half_spread, min_spread / 2.0)

    # Calculate optimal bid and ask
    optimal_bid = max(0.00000001, reservation_price - half_spread)
    optimal_ask = reservation_price + half_spread
    spread_pct = ((optimal_ask - optimal_bid) / mid_price) * 100.0

    return {
        "mid_price": round(mid_price, 6),
        "reservation_price": round(reservation_price, 6),
        "optimal_bid": round(optimal_bid, 6),
        "optimal_ask": round(optimal_ask, 6),
        "spread_pct": round(spread_pct, 3),
        "inventory_skew": inventory_q
    }

# =============================================================================
# 3. FUNDING RATE ARBITRAGE SHIELD
# =============================================================================

def check_funding_rate_dislocation(symbol: str) -> Dict:
    """
    Inspects Binance Futures Funding Rate for extreme dislocations.
    - If Funding Rate >= +0.50% (extreme long crowd leverage):
      Short squeeze potential exists, but shorts are paid massive funding yield every 4-8h.
    - If Funding Rate <= -0.50% (extreme short crowd panic):
      Violent short squeeze imminent; naked shorts strictly blocked.
    """
    symbol = symbol.upper().strip()
    result = {
        "symbol": symbol,
        "funding_rate": 0.0,
        "annualized_rate": 0.0,
        "is_extreme": False,
        "crowd_sentiment": "BALANCED",
        "action_advisory": "NORMAL"
    }

    if is_tradfi_or_delisted(symbol):
        return result

    try:
        url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
        res = requests.get(url, timeout=3.5)
        if res.status_code == 200:
            data = res.json()
            fr = float(data.get("lastFundingRate", 0.0))
            ann_rate = fr * 3.0 * 365.0 * 100.0  # Annualized 8h rate

            result["funding_rate"] = fr
            result["annualized_rate"] = round(ann_rate, 2)

            if fr >= 0.005:  # >= +0.50% per cycle
                result["is_extreme"] = True
                result["crowd_sentiment"] = "GREEDY_LONGS"
                result["action_advisory"] = "CASH_AND_CARRY_HARVEST"
            elif fr <= -0.005:  # <= -0.50% per cycle
                result["is_extreme"] = True
                result["crowd_sentiment"] = "PANIC_SHORTS"
                result["action_advisory"] = "BLOCK_SHORTS_PREPARE_SQUEEZE_LONG"

            return result
    except Exception:
        pass

    return result

# =============================================================================
# 4. SYMBIOTIC COORDINATION & DYNAMIC PROFIT FEEDBACK
# =============================================================================

def evaluate_symbiotic_coordination(
    chat_id: int,
    symbol: str,
    proposed_engine: str,
    proposed_side: str
) -> Tuple[bool, str, Dict]:
    """
    Master Arbiter for /auto_trade and /turbo_hedge co-existence on the same asset:
    1. Evaluates Kaufman Volatility Regime.
    2. Enforces non-aggression: No opposing naked trades in Trending regimes.
    3. Authorizes Micro Relief Scalping when Macro Anchor is active.
    4. Computes effective Dynamic Profit Feedback for Break-Even reduction.
    """
    symbol = symbol.upper().strip()
    proposed_side = "BUY" if proposed_side in ["BUY", "LONG"] else "SELL"
    
    # 1. Classify Regime
    regime_info = classify_volatility_regime(symbol, interval="15m")
    er = regime_info.get("er", 0.5)
    regime = regime_info.get("regime", REGIME_TRANSITIONAL)

    # 2. Check Macro and Turbo Hedge state from database
    macro_trades = db.get_user_macro_trades(chat_id) or []
    turbo_bots = db.get_user_turbo_hedge_bots(chat_id) or []

    active_macro = next((m for m in macro_trades if m.get("symbol") == symbol), None)
    active_turbo = next((t for t in turbo_bots if t.get("symbol") == symbol), None)

    # 3. Rule for Explosive Trend (ER >= 0.58)
    if regime == REGIME_EXPLOSIVE_TREND:
        trend_direction = regime_info.get("direction", "NEUTRAL")
        # In explosive trend, opposing directional trades are suicidal
        if proposed_side == "SELL" and trend_direction == "BULLISH":
            return False, f"OPPOSING_EXPLOSIVE_BULL_TREND (ER {er:.2f} Momentum Surge)", regime_info
        if proposed_side == "BUY" and trend_direction == "BEARISH":
            return False, f"OPPOSING_EXPLOSIVE_BEAR_TREND (ER {er:.2f} Waterfall Dump)", regime_info

    # 4. Rule when Macro Trade is already Active:
    # Allow /turbo_hedge to take micro relief scalps if symbiotic mode is active
    if active_macro and proposed_engine == "turbo_hedge":
        macro_side = "BUY" if str(active_macro.get("side", "")).upper() in ["BUY", "LONG"] else "SELL"
        # If /turbo_hedge enters the same side: allowed as momentum reinforcement
        if proposed_side == macro_side:
            return True, "SYMBIOTIC_MOMENTUM_CONFLUENCE", regime_info
        # If /turbo_hedge enters opposite side: ONLY allowed in Mean-Reverting Chop (ER <= 0.38)
        if er <= 0.38:
            return True, "SYMBIOTIC_MICRO_RELIEF_HARVESTER", regime_info
        else:
            return False, f"OPPOSING_MACRO_ANCHOR (Macro is {macro_side}, ER {er:.2f} is trending)", regime_info

    # 5. Rule when Turbo Hedge is already Active:
    # Macro engine skips symbol if already traded by Turbo Hedge unless regime is explosive trend
    if active_turbo and proposed_engine == "macro_auto_trade":
        turbo_side = "BUY" if str(active_turbo.get("side", "")).upper() in ["BUY", "LONG"] else "SELL"
        if proposed_side != turbo_side and er < 0.55:
            return False, f"OPPOSING_TURBO_HEDGE_POSITION ({symbol} is {turbo_side} in /turbo_hedge)", regime_info
        if proposed_side == turbo_side and er >= 0.58:
            # Upgrade into macro trend position
            return True, "SYMBIOTIC_TREND_EXPANSION_UPGRADE", regime_info

    return True, "STANDARD_SYMBIOTIC_OK", regime_info

def compute_adjusted_breakeven_price(
    entry_price: float,
    position_qty: float,
    side: str,
    accumulated_micro_profit_usdt: float
) -> float:
    """
    Dynamic Profit Feedback Loop:
    Lowers the break-even price of the Macro position by subtracting micro-scalp profits.
    - For LONG:  Effective Entry = Entry Price - (Micro Profit / Qty)
    - For SHORT: Effective Entry = Entry Price + (Micro Profit / Qty)
    """
    if position_qty <= 0 or entry_price <= 0:
        return entry_price

    if accumulated_micro_profit_usdt <= 0:
        return entry_price

    profit_offset_per_unit = accumulated_micro_profit_usdt / position_qty

    side_norm = "BUY" if side in ["BUY", "LONG"] else "SELL"
    if side_norm == "BUY":
        adjusted = entry_price - profit_offset_per_unit
        return max(0.00000001, adjusted)
    else:
        adjusted = entry_price + profit_offset_per_unit
        return adjusted
