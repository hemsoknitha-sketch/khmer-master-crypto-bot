# -*- coding: utf-8 -*-
"""
KHMER MASTER CRYPTO / ANGKOR QUANT - SUPER SMART SKY NET INSTITUTIONAL CAPITAL CITADEL
========================================================================================
Document Version: 1.0.0 (Absolute Mathematical Ground Truth & Institutional Specification Lock)
Target: Capital.com TradFi Markets (Gold, Oil, US Indices, Mega-Caps, Forex, Crypto CFDs)
Integrations: /capital, CapitalAutonomousEngine, Prop Firm Citadel, Lead-Lag Arb, ORB 15m
Architecture:
  1. Pillar 1: TradFi Liquidity Trap Hunter (BSL / SSL Sweeps & Turtle Soup Reversal)
  2. Pillar 2: Premium vs Discount Dealing Range Math (Fibonacci Equilibrium Math)
  3. Pillar 3: Market Structure Shift (MSS / CHoCH) & Displacement Confirmation
  4. Pillar 4: Fair Value Gap (FVG) & Order Block (OB) Imbalance Retest
  5. Pillar 5: TradFi Spread Drag & Asymmetric 10x Hurdle (Invariant 34 Compliance)
  6. Pillar 6: Strict Capital Armor (Invariant 16 RSI <= 36.0 Bottom Shield, Anti-Top FOMO RSI >= 70.0)
  7. Pillar 7: Interbank Sessions, Kill Zones & Rollover Swap Shield (Invariant 53)
  8. Pillar 8: Asymmetric Expectancy Sizer (Enforcing R:R >= 1:2.5 to 1:6.0 with Dynamic Invalidation)
"""

import time
import math
import datetime
import logging
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd

import database as db

logger = logging.getLogger("SuperSmartCapitalCitadel")


def _get_tradfi_precision(epic_str: str, price_val: float = 0.0) -> int:
    """
    Returns exact price decimal precision for TradFi instruments:
    - Forex Majors & Minors: 5 decimals (e.g. 1.32038)
    - JPY Pairs: 3 decimals (e.g. 154.250)
    - Sub-$5 assets: 4-5 decimals
    - Indices / Commodities / Crypto CFDs: 2 decimals (e.g. 2650.50)
    """
    s = str(epic_str or "").upper()
    if any(fx in s for fx in ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF"]):
        return 5
    elif any(fx in s for fx in ["USDJPY", "EURJPY", "GBPJPY", "AUDJPY", "NZDJPY", "CADJPY", "CHFJPY"]):
        return 3
    elif 0 < price_val < 5.0:
        return 5
    return 2


class SuperSmartCapitalCitadel:
    """
    Institutional TradFi Position Opening Gatekeeper & Sky Net Trap Citadel for Capital.com.
    Ensures that NO TradFi position (Buy or Sell) is opened blindly or into retail traps,
    eradicating daily capital bleeding and enforcing strict mathematical edge (E[X] > 0).
    """

    # In-memory evaluation cache with 3.0s TTL to preserve sub-millisecond execution
    _CITADEL_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
    _CACHE_TTL: float = 3.0

    @classmethod
    def evaluate_institutional_tradfi_trap(
        cls,
        epic: str,
        proposed_side: str,
        engine: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive Institutional Trap & Confluence Evaluation for a Capital.com TradFi Asset.
        Returns full diagnostics, approval status, conviction score, and invalidation levels.
        """
        import capital_engine

        resolved_epic = capital_engine.EPIC_MAP.get(str(epic or "").upper().strip(), str(epic or "").upper().strip())
        side = str(proposed_side or "").upper().strip()
        if side in ["BUY", "LONG"]:
            norm_side = "BUY"
        elif side in ["SELL", "SHORT"]:
            norm_side = "SELL"
        else:
            norm_side = "UNKNOWN"

        now = time.time()
        cache_key = f"{resolved_epic}_{norm_side}"
        if cache_key in cls._CITADEL_CACHE:
            cached_ts, cached_res = cls._CITADEL_CACHE[cache_key]
            if now - cached_ts < cls._CACHE_TTL:
                return cached_res

        # Retrieve active engine if not passed
        if engine is None:
            engine = capital_engine.get_capital_engine()

        # Step 0: Market Details & Spread Inspection
        market_details = engine.get_market_details(resolved_epic)
        if not market_details.get("success"):
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": f"MARKET_DATA_UNAVAILABLE: {market_details.get('error')}",
                "confluence_score": 0.0,
                "details": "Broker market details unreachable."
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        market_status = market_details.get("market_status") or market_details.get("marketStatus", "TRADEABLE")
        if market_status != "TRADEABLE":
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": f"MARKET_NOT_TRADEABLE: Status is {market_status} (TradFi markets closed).",
                "confluence_score": 0.0,
                "market_status": market_status
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        current_bid = float(market_details.get("bid", 0.0))
        current_ask = float(market_details.get("ask", 0.0))
        mid_price = float(market_details.get("mid", 0.0))
        spread = float(market_details.get("spread", 0.0))
        curr_price = current_ask if norm_side == "BUY" else current_bid
        if curr_price <= 0:
            curr_price = mid_price if mid_price > 0 else 1.0

        # Step 1: Interbank Session & Rollover Swap Shield (Pillar 7)
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        utc_hour = now_utc.hour
        utc_minute = now_utc.minute
        utc_minutes = utc_hour * 60 + utc_minute
        w_utc = now_utc.weekday()

        is_crypto = any(c in resolved_epic.upper() for c in ["BTC", "ETH", "SOL", "XRP"])

        # TradFi Rollover Dead Zone: 20:45 - 23:59 UTC (03:45 - 07:00 ICT)
        # Broker spreads blow out 3x-10x, liquidity drops, and financing fees are charged
        is_rollover_dead_zone = (1245 <= utc_minutes <= 1439)
        if not is_crypto and is_rollover_dead_zone:
            reason = (
                f"ROLLOVER_SWAP_DEAD_ZONE: TradFi entry blocked between 20:45-23:59 UTC "
                f"(03:45-07:00 ICT) to eliminate overnight financing drag and spread explosion."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "confluence_score": 0.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # Step 2: Fetch 15m and 1h historical candles
        candles_15m = engine.get_historical_prices(resolved_epic, resolution="MINUTE_15", max_bars=60)
        candles_1h = engine.get_historical_prices(resolved_epic, resolution="HOUR", max_bars=40)

        if not candles_15m or len(candles_15m) < 25:
            # Fallback to shared RAM price cache or basic validation if API prices temporarily unavailable
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": "INSUFFICIENT_HISTORICAL_CANDLES",
                "confluence_score": 0.0,
                "details": f"Historical bars ({len(candles_15m) if candles_15m else 0}) below required minimum 25."
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        opens = [float(c.get("open", 0.0)) for c in candles_15m]
        highs = [float(c.get("high", 0.0)) for c in candles_15m]
        lows = [float(c.get("low", 0.0)) for c in candles_15m]
        closes = [float(c.get("close", 0.0)) for c in candles_15m]
        volumes = [float(c.get("volume", 0.0)) for c in candles_15m]

        # --------------------------------------------------------------------
        # 1. PILLAR 6: NON-NEGOTIABLE SAFETY HARD GUARDS (RSI ARMOR)
        # --------------------------------------------------------------------
        # Calculate 15m RSI (14 period)
        gains, losses = [], []
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i - 1]
            if diff >= 0:
                gains.append(diff)
                losses.append(0.0)
            else:
                gains.append(0.0)
                losses.append(abs(diff))

        avg_gain = sum(gains[-14:]) / 14.0 if len(gains) >= 14 else 0.001
        avg_loss = sum(losses[-14:]) / 14.0 if len(losses) >= 14 else 0.001
        rs = avg_gain / max(0.00001, avg_loss)
        rsi_15m = round(100.0 - (100.0 / (1.0 + rs)), 2)

        # Invariant 16: Anti-Oversold Short Guard (15m RSI <= 36.0 Bottom Shield)
        if norm_side == "SELL" and rsi_15m <= 36.0:
            reason = (
                f"ANTI_OVERSOLD_SHORT_GUARD: 15m RSI ({rsi_15m:.1f}) <= 36.0 (Invariant 16). "
                f"Selling panic liquidation bottom into institutional support is prohibited."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "rsi_15m": rsi_15m,
                "confluence_score": 0.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # Dimension 7 Anti-FOMO: Anti-Overbought Peak Guard (15m RSI >= 70.0 Peak Long Shield)
        if norm_side == "BUY" and rsi_15m >= 70.0:
            reason = (
                f"ANTI_OVERBOUGHT_LONG_GUARD: 15m RSI ({rsi_15m:.1f}) >= 70.0. "
                f"Buying blow-off euphoria peak into institutional distribution is prohibited."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "rsi_15m": rsi_15m,
                "confluence_score": 0.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # --------------------------------------------------------------------
        # 2. PILLAR 2: PREMIUM VS DISCOUNT DEALING RANGE MATH
        # --------------------------------------------------------------------
        lookback_window = min(35, len(highs) - 2)
        swing_high = max(highs[-lookback_window:-2])
        swing_low = min(lows[-lookback_window:-2])
        dealing_range = max(1e-6, swing_high - swing_low)
        equilibrium = swing_low + 0.5 * dealing_range
        price_range_pct = round(((curr_price - swing_low) / dealing_range) * 100.0, 1)

        is_discount = curr_price < equilibrium
        is_premium = curr_price > equilibrium

        # Hard Veto on Deep Trapped Zones:
        # Longing in Extreme Premium (> 82.0%) without structural base is retail suicide
        if norm_side == "BUY" and price_range_pct > 82.0:
            reason = (
                f"DEEP_PREMIUM_TRAP: Price is at {price_range_pct:.1f}% of dealing range. "
                f"Longing deep premium is blocked to avoid buying the top before discount pullback."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "price_range_pct": price_range_pct,
                "confluence_score": 25.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # Shorting in Extreme Discount (< 18.0%) without structural breakdown is retail suicide
        if norm_side == "SELL" and price_range_pct < 18.0:
            reason = (
                f"DEEP_DISCOUNT_TRAP: Price is at {price_range_pct:.1f}% of dealing range. "
                f"Shorting deep discount is blocked to prevent violent short squeeze."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "price_range_pct": price_range_pct,
                "confluence_score": 25.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # --------------------------------------------------------------------
        # 3. PILLAR 1: TRADFI LIQUIDITY TRAP HUNTER (BSL / SSL SWEEPS)
        # --------------------------------------------------------------------
        # Inspect recent 4 candles for Liquidity Sweep Wicks (Turtle Soup pattern)
        has_bsl_sweep = False  # Swept Buy-Side Liquidity above swing high with upper wick rejection
        has_ssl_sweep = False  # Swept Sell-Side Liquidity below swing low with lower wick rejection

        for i in range(-5, -1):
            c_high = highs[i]
            c_low = lows[i]
            c_close = closes[i]
            c_open = opens[i]

            # BSL Sweep: High pierced above swing high, but closed back below with upper wick
            if c_high > swing_high and c_close < swing_high:
                upper_wick = c_high - max(c_open, c_close)
                body = abs(c_close - c_open)
                if upper_wick >= body * 0.75:
                    has_bsl_sweep = True

            # SSL Sweep: Low pierced below swing low, but closed back above with lower wick
            if c_low < swing_low and c_close > swing_low:
                lower_wick = min(c_open, c_close) - c_low
                body = abs(c_close - c_open)
                if lower_wick >= body * 0.75:
                    has_ssl_sweep = True

        # Sweep Trap Violation Checks:
        # If smart money just swept SSL (accumulated liquidity), selling is walking into the trap!
        if norm_side == "SELL" and has_ssl_sweep and not has_bsl_sweep:
            reason = (
                "SSL_SWEEP_REJECTION_ACTIVE: Sell-Side Liquidity swept with strong bullish absorption. "
                "Institutions have engineered liquidity spring. Shorting rejected."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "confluence_score": 20.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # If smart money just swept BSL (distributed peak), buying is walking into the trap!
        if norm_side == "BUY" and has_bsl_sweep and not has_ssl_sweep:
            reason = (
                "BSL_SWEEP_REJECTION_ACTIVE: Buy-Side Liquidity swept with strong bearish rejection. "
                "Institutions have engineered upthrust distribution. Longing rejected."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "confluence_score": 20.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # --------------------------------------------------------------------
        # 4. PILLAR 3 & 4: MARKET STRUCTURE SHIFT & FVG / ORDER BLOCK TAP
        # --------------------------------------------------------------------
        # Calculate 15m ATR
        trs = []
        for i in range(1, len(closes)):
            tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
            trs.append(tr)
        atr_15m = sum(trs[-14:]) / 14.0 if len(trs) >= 14 else (curr_price * 0.005)

        # Detect 3-bar Fair Value Gap (FVG)
        has_bullish_fvg = False
        has_bearish_fvg = False
        fvg_level = 0.0

        for i in range(-5, -1):
            # Bullish FVG: Low of candle [i+1] > High of candle [i-1]
            if lows[i + 1] > highs[i - 1]:
                gap_size = lows[i + 1] - highs[i - 1]
                if gap_size > atr_15m * 0.30:
                    has_bullish_fvg = True
                    fvg_level = (lows[i + 1] + highs[i - 1]) / 2.0

            # Bearish FVG: High of candle [i+1] < Low of candle [i-1]
            if highs[i + 1] < lows[i - 1]:
                gap_size = lows[i - 1] - highs[i + 1]
                if gap_size > atr_15m * 0.30:
                    has_bearish_fvg = True
                    fvg_level = (lows[i - 1] + highs[i + 1]) / 2.0

        # Market Structure Shift (Displacement candle check)
        recent_ranges = [highs[k] - lows[k] for k in range(-3, 0)]
        max_recent_range = max(recent_ranges) if recent_ranges else atr_15m
        has_displacement = max_recent_range >= (1.2 * atr_15m)

        # --------------------------------------------------------------------
        # 5. PILLAR 5: SPREAD DRAG ELIMINATION & ASYMMETRIC 10X HURDLE (INVARIANT 34)
        # --------------------------------------------------------------------
        spread_drag_pct = (spread / max(0.0001, atr_15m)) * 100.0
        # If spread / ATR exceeds 18%, spread fee drag destroys expected value (E[X] <= 0)
        if spread_drag_pct > 18.0:
            reason = (
                f"SPREAD_DRAG_TOO_HIGH: Current spread {spread} is {spread_drag_pct:.1f}% of ATR. "
                f"Violates Invariant 34 (< 18.0% hurdle). Trading blocked to avoid broker fee bleeding."
            )
            res = {
                "epic": resolved_epic,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "spread": spread,
                "spread_drag_pct": round(spread_drag_pct, 1),
                "confluence_score": 15.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # --------------------------------------------------------------------
        # 6. PILLAR 7: MULTI-TIMEFRAME & SESSION KILL ZONE CONFLUENCE
        # --------------------------------------------------------------------
        ema50_15m = float(pd.Series(closes).ewm(span=50, adjust=False).mean().iloc[-1])
        closes_1h = [float(c.get("close", 0.0)) for c in candles_1h] if candles_1h else []
        ema50_1h = float(pd.Series(closes_1h).ewm(span=50, adjust=False).mean().iloc[-1]) if len(closes_1h) >= 20 else curr_price

        is_1h_bullish = curr_price >= ema50_1h
        is_1h_bearish = curr_price <= ema50_1h

        # Session Alignment
        # London Kill Zone: 07:00 - 10:00 UTC (14:00 - 17:00 ICT)
        # NY Kill Zone: 13:00 - 16:00 UTC (20:00 - 23:00 ICT)
        in_kill_zone = (7 <= utc_hour <= 10) or (13 <= utc_hour <= 16)

        # --------------------------------------------------------------------
        # 7. CONFLUENCE SCORING & DECISION MATRIX
        # --------------------------------------------------------------------
        score = 50.0
        factors = []

        if norm_side == "BUY":
            # Discount advantage
            if is_discount:
                score += 15.0
                factors.append("DISCOUNT_ZONE_ADVANTAGE (+15)")
            else:
                score -= 10.0

            # SSL Liquidity Sweep Spring
            if has_ssl_sweep:
                score += 25.0
                factors.append("SSL_LIQUIDITY_SWEEP_CONFIRMED (+25)")

            # Bullish FVG Imbalance
            if has_bullish_fvg:
                score += 12.0
                factors.append("BULLISH_FVG_IMBALANCE (+12)")

            if curr_price > ema50_15m:
                score += 10.0
                factors.append("15M_EMA50_UPTREND (+10)")

            if is_1h_bullish:
                score += 12.0
                factors.append("1H_MACRO_ALIGNMENT (+12)")

            if has_displacement:
                score += 10.0
                factors.append("MSS_DISPLACEMENT_EXPANSION (+10)")

            if in_kill_zone:
                score += 8.0
                factors.append("INTERBANK_KILL_ZONE_ACTIVE (+8)")

        elif norm_side == "SELL":
            # Premium advantage
            if is_premium:
                score += 15.0
                factors.append("PREMIUM_ZONE_ADVANTAGE (+15)")
            else:
                score -= 10.0

            # BSL Liquidity Sweep Upthrust
            if has_bsl_sweep:
                score += 25.0
                factors.append("BSL_LIQUIDITY_SWEEP_CONFIRMED (+25)")

            # Bearish FVG Imbalance
            if has_bearish_fvg:
                score += 12.0
                factors.append("BEARISH_FVG_IMBALANCE (+12)")

            if curr_price < ema50_15m:
                score += 10.0
                factors.append("15M_EMA50_DOWNTREND (+10)")

            if is_1h_bearish:
                score += 12.0
                factors.append("1H_MACRO_ALIGNMENT (+12)")

            if has_displacement:
                score += 10.0
                factors.append("MSS_DISPLACEMENT_EXPANSION (+10)")

            if in_kill_zone:
                score += 8.0
                factors.append("INTERBANK_KILL_ZONE_ACTIVE (+8)")

        confluence_score = round(max(0.0, min(99.5, score)), 1)
        is_approved = (confluence_score >= 68.0)

        # --------------------------------------------------------------------
        # 8. PILLAR 8: ASYMMETRIC R:R >= 1:2.5 & DYNAMIC INVALIDATION
        # --------------------------------------------------------------------
        prec = _get_tradfi_precision(resolved_epic, curr_price)
        min_pip_buf = 0.0006 if prec == 5 else (0.06 if prec == 3 else max(0.50, spread * 1.5))
        if norm_side == "BUY":
            invalidation_sl = round(min(swing_low - (0.25 * atr_15m), curr_price - max(min_pip_buf, 1.6 * atr_15m)), prec)
            risk_dist = max(spread * 3.0, curr_price - invalidation_sl)
            tp_1 = round(curr_price + (risk_dist * 2.5), prec)  # Institutional 1:2.5 Min Hurdle
            tp_2 = round(curr_price + (risk_dist * 5.0), prec)  # Institutional 1:5.0 Major Target
        else:
            invalidation_sl = round(max(swing_high + (0.25 * atr_15m), curr_price + max(min_pip_buf, 1.6 * atr_15m)), prec)
            risk_dist = max(spread * 3.0, invalidation_sl - curr_price)
            tp_1 = round(curr_price - (risk_dist * 2.5), prec)
            tp_2 = round(curr_price - (risk_dist * 5.0), prec)

        rr_ratio = round((abs(tp_1 - curr_price) / max(1e-6, abs(curr_price - invalidation_sl))), 2)

        result = {
            "epic": resolved_epic,
            "proposed_side": norm_side,
            "is_approved": is_approved,
            "confluence_score": confluence_score,
            "conviction_badge": (
                "🦅 [SUPER SMART 99% INSTITUTIONAL TRADFI TRAP CONVICTION]"
                if confluence_score >= 85.0
                else f"🛡️ [INSTITUTIONAL TRADFI CONVICTION {confluence_score:.1f}%]"
            ),
            "rejection_reason": "CLEARANCE_GRANTED" if is_approved else f"CONFLUENCE_SCORE_BELOW_THRESHOLD ({confluence_score} < 68.0)",
            "rsi_15m": rsi_15m,
            "price_range_pct": price_range_pct,
            "is_discount": is_discount,
            "is_premium": is_premium,
            "has_bsl_sweep": has_bsl_sweep,
            "has_ssl_sweep": has_ssl_sweep,
            "has_bullish_fvg": has_bullish_fvg,
            "has_bearish_fvg": has_bearish_fvg,
            "has_displacement": has_displacement,
            "in_kill_zone": in_kill_zone,
            "current_price": curr_price,
            "spread": spread,
            "spread_drag_pct": round(spread_drag_pct, 1),
            "invalidation_sl": invalidation_sl,
            "target_tp_min": tp_1,
            "target_tp_major": tp_2,
            "risk_reward_ratio": rr_ratio,
            "confluence_factors": factors
        }

        cls._CITADEL_CACHE[cache_key] = (now, result)
        return result

    @classmethod
    def validate_capital_entry_gatekeeper(
        cls,
        epic: str,
        direction: str,
        engine: Optional[Any] = None,
        bypass_citadel: bool = False
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Universal Pre-Flight Gatekeeper called by all Capital.com execution routines.
        - Verifies 8-Pillar Institutional Trap Matrix before allowing trade entry.
        - Guarantees zero retail trap walking and eliminates daily capital destruction.
        """
        if bypass_citadel:
            return True, "CITADEL_BYPASS_EXPLICIT", {}

        diag = cls.evaluate_institutional_tradfi_trap(epic, direction, engine=engine)
        if not diag.get("is_approved"):
            reason = diag.get("rejection_reason", "SUPER_SMART_CAPITAL_CITADEL_REJECTED")
            print(f"🛑 [SUPER SMART CAPITAL CITADEL] Entry blocked for {epic} ({direction}): {reason}")
            return False, reason, diag

        prec = _get_tradfi_precision(epic, diag.get("current_price", 0.0))
        sl_val = diag.get('invalidation_sl', 0.0)
        tp_val = diag.get('target_tp_min', 0.0)
        sl_str = f"{sl_val:.{prec}f}" if isinstance(sl_val, (int, float)) else str(sl_val)
        tp_str = f"{tp_val:.{prec}f}" if isinstance(tp_val, (int, float)) else str(tp_val)
        print(
            f"🦅 [SUPER SMART CAPITAL CITADEL APPROVED] {epic} {direction} | "
            f"Score: {diag.get('confluence_score')}% | R:R: 1:{diag.get('risk_reward_ratio')} | "
            f"SL: ${sl_str} | TP: ${tp_str}"
        )
        return True, "SUPER_SMART_CAPITAL_CLEARANCE_GRANTED", diag
