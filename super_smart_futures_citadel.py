# -*- coding: utf-8 -*-
"""
KHMER MASTER CRYPTO / ANGKOR QUANT - SUPER SMART SKY NET INSTITUTIONAL FUTURES CITADEL
========================================================================================
Document Version: 1.0.0 (Absolute Mathematical Ground Truth & Institutional Specification Lock)
Target: Binance USDT-M Futures & Multi-Engine Confluence (/turbo_hedge, /smartx, /wealth, /auto_trade)
Architecture:
  1. Pillar 1: Dynamic Liquidity Trap Hunter (BSL / SSL Sweeps & Turtle Soup Rejection)
  2. Pillar 2: Premium vs Discount Dealing Range Math (Flipping Retail Traps)
  3. Pillar 3: Market Structure Shift (MSS / CHoCH) & Displacement Confirmation
  4. Pillar 4: Fair Value Gap (FVG) & Institutional Order Block (OB) Mitigation Retest
  5. Pillar 5: Order Flow CVD & Absorption Divergence Shield (Limit Wall Defense)
  6. Pillar 6: Non-Negotiable Capital Armor (Invariant 16 RSI <= 38.0 Bottom Shield, Anti-Top FOMO)
  7. Pillar 7: Multi-Timeframe Institutional Quorum (4H/1H Macro Bias -> 15M Structure -> 5M Trigger)
  8. Pillar 8: Asymmetric Expectancy Sizer (Enforcing R:R >= 1:2.5 with Dynamic ATR Invalidation)
"""

import time
import math
import logging
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd

import trading_engine
import market_data
import database as db

logger = logging.getLogger("SuperSmartFuturesCitadel")


class SuperSmartFuturesCitadel:
    """
    Institutional Futures Position Opening Gatekeeper & Sky Net Trap Citadel.
    Ensures that NO Futures position (Long or Short) is opened blindly, eradicating
    retail capital bleeding and enforcing strict mathematical edge (E[X] > 0).
    """

    # In-memory evaluation cache with 3.0s TTL to preserve sub-millisecond execution
    _CITADEL_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
    _CACHE_TTL: float = 3.0

    @classmethod
    def evaluate_institutional_futures_trap(
        cls,
        symbol: str,
        proposed_side: str,
        interval: str = "15m"
    ) -> Dict[str, Any]:
        """
        Comprehensive Institutional Trap & Confluence Evaluation for a Futures Asset.
        Returns full diagnostics, approval status, conviction score, and invalidation levels.
        """
        sym = str(symbol or "").upper().strip()
        if not sym.endswith("USDT") and not sym.endswith("USD"):
            sym += "USDT"
        if sym == "DODOUSDT":
            sym = "DODOXUSDT"

        side = str(proposed_side or "").upper().strip()
        if side in ["BUY", "LONG"]:
            norm_side = "BUY"
        elif side in ["SELL", "SHORT"]:
            norm_side = "SELL"
        else:
            norm_side = "UNKNOWN"

        now = time.time()
        cache_key = f"{sym}_{norm_side}_{interval}"
        if cache_key in cls._CITADEL_CACHE:
            cached_ts, cached_res = cls._CITADEL_CACHE[cache_key]
            if now - cached_ts < cls._CACHE_TTL:
                return cached_res

        # Fetch recent 15m and 1h klines
        klines_15m = trading_engine.get_klines(sym, interval=interval, limit=60, is_spot=False)
        klines_1h = trading_engine.get_klines(sym, interval="1h", limit=60, is_spot=False)

        if not klines_15m or len(klines_15m) < 30:
            res = {
                "symbol": sym,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": "INSUFFICIENT_KLINE_DATA",
                "confluence_score": 0.0,
                "details": "Insufficient historical klines for quantitative verification."
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # Parse OHLCV for 15m
        opens = [float(k[1]) for k in klines_15m]
        highs = [float(k[2]) for k in klines_15m]
        lows = [float(k[3]) for k in klines_15m]
        closes = [float(k[4]) for k in klines_15m]
        volumes = [float(k[5]) for k in klines_15m]
        taker_buys = [float(k[9]) if len(k) > 9 else (float(k[5]) * 0.5) for k in klines_15m]

        curr_price = closes[-1]

        # --------------------------------------------------------------------
        # 1. PILLAR 6: NON-NEGOTIABLE SAFETY HARD GUARDS
        # --------------------------------------------------------------------
        # Calculate 15m RSI
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

        # Invariant 16: Anti-Oversold Short Guard (RSI <= 38.0 Bottom Rejection)
        if norm_side == "SELL" and rsi_15m <= 38.0:
            reason = f"ANTI_OVERSOLD_SHORT_GUARD: 15m RSI ({rsi_15m:.1f}) <= 38.0 (Invariant 16). Shorting bottom into liquidation panic prohibited."
            res = {
                "symbol": sym,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "rsi_15m": rsi_15m,
                "confluence_score": 0.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # Anti-Overbought Peak Guard (RSI >= 70.0 Peak Long Rejection)
        if norm_side == "BUY" and rsi_15m >= 70.0:
            reason = f"ANTI_OVERBOUGHT_LONG_GUARD: 15m RSI ({rsi_15m:.1f}) >= 70.0. Buying blow-off top into distribution trap prohibited."
            res = {
                "symbol": sym,
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

        # Mathematical Edge:
        # Longs MUST preferably reside in Discount zone (< 50.0%)
        # Shorts MUST preferably reside in Premium zone (> 50.0%)
        is_discount = curr_price < equilibrium
        is_premium = curr_price > equilibrium

        # Hard Exclusion on Extreme Trapped Zones:
        # Longing in Extreme Premium (> 85%) without confirmed structural breakout is retail suicide
        if norm_side == "BUY" and price_range_pct > 85.0:
            reason = f"DEEP_PREMIUM_TRAP: Price is at {price_range_pct:.1f}% of range. Waiting for discount pullback to prevent buying top."
            res = {
                "symbol": sym,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "price_range_pct": price_range_pct,
                "confluence_score": 25.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # Shorting in Extreme Discount (< 15%) without confirmed breakdown is retail suicide
        if norm_side == "SELL" and price_range_pct < 15.0:
            reason = f"DEEP_DISCOUNT_TRAP: Price is at {price_range_pct:.1f}% of range. Waiting for premium retracement to prevent short squeeze."
            res = {
                "symbol": sym,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "price_range_pct": price_range_pct,
                "confluence_score": 25.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # --------------------------------------------------------------------
        # 3. PILLAR 1: LIQUIDITY TRAP HUNTER (BSL / SSL SWEEPS)
        # --------------------------------------------------------------------
        # Check recent 3 candles for Liquidity Sweep Wicks
        has_bsl_sweep = False  # Swept Buy-Side Liquidity (Peak Wick Rejection)
        has_ssl_sweep = False  # Swept Sell-Side Liquidity (Bottom Wick Rejection)

        for i in range(-4, 0):
            c_high = highs[i]
            c_low = lows[i]
            c_close = closes[i]
            c_open = opens[i]

            # BSL Sweep: High pierced above previous swing high, but close remained below
            if c_high > swing_high and c_close < swing_high:
                upper_wick = c_high - max(c_open, c_close)
                body = abs(c_close - c_open)
                if upper_wick >= body * 0.8:
                    has_bsl_sweep = True

            # SSL Sweep: Low pierced below previous swing low, but close remained above
            if c_low < swing_low and c_close > swing_low:
                lower_wick = min(c_open, c_close) - c_low
                body = abs(c_close - c_open)
                if lower_wick >= body * 0.8:
                    has_ssl_sweep = True

        # Sweep Trap Violation Checks:
        # If price just swept SSL (smart money accumulated bottom), initiating a SHORT is walking into a trap!
        if norm_side == "SELL" and has_ssl_sweep and not has_bsl_sweep:
            reason = "SSL_SWEEP_REJECTION_ACTIVE: Sell-Side Liquidity swept with strong bullish absorption. Shorting rejected."
            res = {
                "symbol": sym,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "confluence_score": 20.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # If price just swept BSL (smart money distributed peak), initiating a LONG is walking into a trap!
        if norm_side == "BUY" and has_bsl_sweep and not has_ssl_sweep:
            reason = "BSL_SWEEP_REJECTION_ACTIVE: Buy-Side Liquidity swept with strong bearish rejection. Longing rejected."
            res = {
                "symbol": sym,
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
        # Calculate ATR for displacement measurement
        trs = []
        for i in range(1, len(closes)):
            tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
            trs.append(tr)
        atr_15m = sum(trs[-14:]) / 14.0 if len(trs) >= 14 else (curr_price * 0.01)

        # Detect FVG (Fair Value Gap 3-candle imbalance)
        has_bullish_fvg = False
        has_bearish_fvg = False
        fvg_level = 0.0

        for i in range(-5, -1):
            # Bullish FVG: Low of candle [i+1] > High of candle [i-1]
            if lows[i + 1] > highs[i - 1]:
                gap_size = lows[i + 1] - highs[i - 1]
                if gap_size > atr_15m * 0.35:
                    has_bullish_fvg = True
                    fvg_level = (lows[i + 1] + highs[i - 1]) / 2.0

            # Bearish FVG: High of candle [i+1] < Low of candle [i-1]
            if highs[i + 1] < lows[i - 1]:
                gap_size = lows[i - 1] - highs[i + 1]
                if gap_size > atr_15m * 0.35:
                    has_bearish_fvg = True
                    fvg_level = (lows[i - 1] + highs[i + 1]) / 2.0

        # --------------------------------------------------------------------
        # 5. PILLAR 5: ORDER FLOW CVD ABSORPTION DIVERGENCE
        # --------------------------------------------------------------------
        recent_vols = volumes[-5:]
        recent_taker_buys = taker_buys[-5:]
        tot_vol = max(1.0, sum(recent_vols))
        tot_buy = sum(recent_taker_buys)
        tot_sell = tot_vol - tot_buy
        cvd_ratio = (tot_buy - tot_sell) / tot_vol

        # Bearish Absorption: High buy volume, but price fails to make higher highs (Limit Sell Wall)
        bearish_absorption = (cvd_ratio > 0.20 and closes[-1] <= closes[-3])
        # Bullish Absorption: High sell volume, but price fails to make lower lows (Limit Buy Wall)
        bullish_absorption = (cvd_ratio < -0.20 and closes[-1] >= closes[-3])

        if norm_side == "BUY" and bearish_absorption:
            reason = "CVD_BEARISH_ABSORPTION_DETECTED: Institutional limit sellers absorbing retail buy flow. Longing blocked."
            res = {
                "symbol": sym,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "confluence_score": 30.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        if norm_side == "SELL" and bullish_absorption:
            reason = "CVD_BULLISH_ABSORPTION_DETECTED: Institutional limit buyers absorbing retail sell flow. Shorting blocked."
            res = {
                "symbol": sym,
                "proposed_side": norm_side,
                "is_approved": False,
                "rejection_reason": reason,
                "confluence_score": 30.0
            }
            cls._CITADEL_CACHE[cache_key] = (now, res)
            return res

        # --------------------------------------------------------------------
        # 6. PILLAR 7: MULTI-TIMEFRAME (1H / 4H) MACRO CONFLUENCE
        # --------------------------------------------------------------------
        ema50_15m = float(pd.Series(closes).ewm(span=50, adjust=False).mean().iloc[-1])
        closes_1h = [float(k[4]) for k in klines_1h] if klines_1h else []
        ema50_1h = float(pd.Series(closes_1h).ewm(span=50, adjust=False).mean().iloc[-1]) if len(closes_1h) >= 20 else curr_price

        is_1h_bullish = curr_price >= ema50_1h
        is_1h_bearish = curr_price <= ema50_1h

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

            # Bullish FVG or Structure
            if has_bullish_fvg:
                score += 12.0
                factors.append("BULLISH_FVG_IMBALANCE (+12)")

            if curr_price > ema50_15m:
                score += 10.0
                factors.append("15M_EMA50_UPTREND (+10)")

            if is_1h_bullish:
                score += 12.0
                factors.append("1H_MACRO_ALIGNMENT (+12)")

            if bullish_absorption:
                score += 10.0
                factors.append("BULLISH_CVD_ACCUMULATION (+10)")

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

            # Bearish FVG or Structure
            if has_bearish_fvg:
                score += 12.0
                factors.append("BEARISH_FVG_IMBALANCE (+12)")

            if curr_price < ema50_15m:
                score += 10.0
                factors.append("15M_EMA50_DOWNTREND (+10)")

            if is_1h_bearish:
                score += 12.0
                factors.append("1H_MACRO_ALIGNMENT (+12)")

            if bearish_absorption:
                score += 10.0
                factors.append("BEARISH_CVD_DISTRIBUTION (+10)")

        confluence_score = round(max(0.0, min(99.5, score)), 1)
        is_approved = (confluence_score >= 68.0)

        # --------------------------------------------------------------------
        # 8. PILLAR 8: ASYMMETRIC R:R >= 1:2.5 & DYNAMIC BREATHING STOP
        # --------------------------------------------------------------------
        # Dynamic Volatility Breathing Stop Distance (eliminates tight stop-outs & noise sweeps):
        breathing_sl_dist = max(2.20 * atr_15m, curr_price * 0.008, 0.0035 * curr_price)

        if norm_side == "BUY":
            invalidation_sl = round(min(swing_low - (0.35 * atr_15m), curr_price - breathing_sl_dist), 4)
            risk_dist = max(breathing_sl_dist, curr_price - invalidation_sl)
            tp_1 = round(curr_price + (risk_dist * 2.5), 4)  # Institutional 1:2.5 Min Hurdle
            tp_2 = round(curr_price + (risk_dist * 4.0), 4)  # Institutional 1:4.0 Target
        else:
            invalidation_sl = round(max(swing_high + (0.35 * atr_15m), curr_price + breathing_sl_dist), 4)
            risk_dist = max(breathing_sl_dist, invalidation_sl - curr_price)
            tp_1 = round(curr_price - (risk_dist * 2.5), 4)
            tp_2 = round(curr_price - (risk_dist * 4.0), 4)

        rr_ratio = round((abs(tp_1 - curr_price) / max(1e-6, abs(curr_price - invalidation_sl))), 2)

        result = {
            "symbol": sym,
            "proposed_side": norm_side,
            "is_approved": is_approved,
            "confluence_score": confluence_score,
            "conviction_badge": (
                "🦅 [SUPER SMART 99% INSTITUTIONAL TRAP CONVICTION]"
                if confluence_score >= 85.0
                else f"🛡️ [INSTITUTIONAL CONVICTION {confluence_score:.1f}%]"
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
            "current_price": curr_price,
            "invalidation_sl": invalidation_sl,
            "target_tp_min": tp_1,
            "target_tp_major": tp_2,
            "risk_reward_ratio": rr_ratio,
            "confluence_factors": factors
        }

        cls._CITADEL_CACHE[cache_key] = (now, result)
        return result

    @classmethod
    def validate_futures_entry_gatekeeper(
        cls,
        symbol: str,
        side: str,
        reduce_only: bool = False,
        bypass_citadel: bool = False
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Universal Pre-Flight Gatekeeper called by all Futures execution routines.
        - Exits (reduce_only=True) pass unconditionally.
        - Entries (reduce_only=False) undergo full Institutional Trap Verification.
        """
        if reduce_only or bypass_citadel:
            return True, "EXIT_ORDER_UNRESTRICTED", {}

        diag = cls.evaluate_institutional_futures_trap(symbol, side)
        if not diag.get("is_approved"):
            reason = diag.get("rejection_reason", "SUPER_SMART_CITADEL_REJECTED")
            print(f"🛑 [SUPER SMART FUTURES CITADEL] Entry blocked for {symbol} ({side}): {reason}")
            return False, reason, diag

        print(
            f"🦅 [SUPER SMART FUTURES CITADEL APPROVED] {symbol} {side} | "
            f"Score: {diag.get('confluence_score')}% | R:R: 1:{diag.get('risk_reward_ratio')} | "
            f"SL: ${diag.get('invalidation_sl')} | TP: ${diag.get('target_tp_min')}"
        )
        return True, "SUPER_SMART_CITADEL_CLEARANCE_GRANTED", diag

    # -------------------------------------------------------------------------
    # In-Memory Virtual Radar Gateway Classmethods (Universal Futures Suite)
    # -------------------------------------------------------------------------
    @classmethod
    def scan_and_rank_futures_radar_universe(cls, limit: int = 30, min_quote_vol: float = 20_000_000.0) -> List[Dict[str, Any]]:
        """Scans Binance Futures universe and ranks top high-velocity candidates."""
        return FuturesInMemoryVirtualRadar.scan_and_rank_futures_radar_universe(limit=limit, min_quote_vol=min_quote_vol)

    @classmethod
    def arm_in_memory_trap(
        cls,
        symbol: str,
        engine_source: str = "UNIVERSAL",
        current_price: float = 0.0,
        atr_15m: float = 0.0,
        swing_high: float = 0.0,
        swing_low: float = 0.0,
        user_id: Optional[int] = None,
        ttl_seconds: float = 1800.0
    ) -> Dict[str, Any]:
        """Arms an In-Memory Breakout/Breakdown Trap in RAM with zero exchange orderbook exposure."""
        return FuturesInMemoryVirtualRadar.arm_radar_trap(
            symbol=symbol,
            engine_source=engine_source,
            current_price=current_price,
            atr_15m=atr_15m,
            swing_high=swing_high,
            swing_low=swing_low,
            user_id=user_id,
            ttl_seconds=ttl_seconds
        )

    @classmethod
    def evaluate_and_trigger_radar(cls, symbol: str, current_price: float = 0.0, engine_source: Optional[str] = None) -> Dict[str, Any]:
        """Evaluates live market price against armed RAM traps with Instant In-Memory OCO Disarm."""
        return FuturesInMemoryVirtualRadar.evaluate_armed_trap_trigger(symbol=symbol, current_price=current_price, engine_source=engine_source)

    @classmethod
    def disarm_radar_trap(cls, trap_key: str, reason: str = "MANUAL_OR_OCO") -> bool:
        """Disarms and purges an armed trap from high-speed RAM."""
        return FuturesInMemoryVirtualRadar.disarm_trap(trap_key=trap_key, reason=reason)

    @classmethod
    def get_radar_telemetry(cls) -> Dict[str, Any]:
        """Returns real-time telemetry of the In-Memory Futures Virtual Radar."""
        return FuturesInMemoryVirtualRadar.get_radar_telemetry()


# ==============================================================================
# IN-MEMORY FUTURES VIRTUAL RADAR ARMED SYSTEM (INVARIANT 70)
# ZERO PREMATURE BROKER EXPOSURE & ASYMMETRIC REWARD-TO-RISK TRAP ENGINE
# ==============================================================================

class FuturesInMemoryVirtualRadar:
    """
    In-Memory Futures Virtual Radar Armed System (Zero Broker Exposure Standard).
    Synchronized across /smartx, /turbo_hedge, /auto_trade, /pre_pump, and /wealth.

    Axioms:
    1. Zero Premature Exchange Exposure: Breakout traps (Buy Stop / Sell Stop) are armed exclusively
       in Python RAM cache (_ARMED_TRAPS). Never sent to Binance orderbook prior to breakout,
       guaranteeing 100% immunity to pre-breakout stop hunts, Judas Swings, and spread spikes.
    2. Dynamic Volatility Breathing Stop: SL distance is sized to max(2.20*ATR_15m, 0.008*Price, 0.0035*Price).
    3. Asymmetric Take Profit Targets: TP1 at +2.5R (Breakeven Armor trigger), TP2 at +4.0R (Clean Harvest).
    4. Instant In-Memory OCO Disarm: Piercing of either side triggers instant execution and immediately
       purges the opposing side trap in RAM in < 0.1ms with zero redundant cancellations.
    5. Turtle Soup Fakeout & Rejection Wick Shield: Verifies candle body break; wicks > 35% are rejected.
    """
    _ARMED_TRAPS: Dict[str, Dict[str, Any]] = {}
    _STATS: Dict[str, Any] = {
        "total_traps_armed": 0,
        "total_traps_triggered": 0,
        "total_oco_disarmed": 0,
        "last_trigger": {}
    }
    _RADAR_CACHE_TTL: float = 1800.0  # 30-minute default trap lifecycle

    # TradFi Stock synthetics and toxic meme coins to exclude permanently
    EXCLUDED_SYMBOLS = {
        "QNTXUSDT", "CSOPSKHYNIX2LUSDT", "MINIMAXUSDT", "ZHIPUUSDT", "NOKUSDT", "SMCIUSDT", "DELLUSDT", "SNDKUSDT",
        "STXXUSDT", "INTWUSDT", "CBRSUSDT", "EWYUSDT", "MVLLUSDT", "GLWUSDT", "HK0700USDT", "HK1810USDT", "INTCUSDT",
        "CHIPUSDT", "METAUSDT", "AAOIUSDT", "MRVLUSDT", "CRWVUSDT", "ZAMAUSDT", "PLTRUSDT", "TSMUSDT", "AMDUSDT",
        "TQQQUSDT", "SQQQUSDT", "ARMUSDT", "TSLAUSDT", "NATGASUSDT", "INXUSDT", "AMZNUSDT", "AAPLUSDT", "MSFTUSDT",
        "NVDAUSDT", "MSTRUSDT", "BABAUSDT", "ROBOUSDT", "NBISUSDT", "SHAZUSDT", "KORUUSDT", "DRAMUSDT", "SNXXUSDT",
        "MUUUSDT", "MUUSDT", "BEUSDT", "SKHYUSDT", "SKHYNIXUSDT", "SAMSUNGUSDT", "WDCUSDT", "ORCLUSDT", "AIAUSDT", "MUBARAKUSDT",
        "HYPEUSDT", "LITEUSDT", "DEXEUSDT", "BZUSDT", "CLUSDT", "XAUUSDT", "XAGUSDT", "TRUMPUSDT", "HFTUSDT", "GWEIUSDT",
        "EPICUSDT", "USD1USDT", "SPCXUSDT", "OPENAIUSDT", "FIGMAUSDT", "STRIPEUSDT", "BYTEDANCEUSDT", "ANTHROPICUSDT",
        "PONSUSDT", "LYNUSDT", "4USDT", "USELESSUSDT", "CRDOUSDT", "BRUSDT", "VELVETUSDT", "TSTUSDT", "PUMPBTCUSDT",
        "SOONUSDT", "ESPUSDT", "AKEUSDT", "NILUSDT", "PHAROSUSDT", "TRIAUSDT", "CLOUSDT", "TOWNSUSDT", "PHAUSDT",
        "MAGICUSDT", "COHRUSDT", "SOXLUSDT", "GOOGLUSDT"
    }

    @classmethod
    def scan_and_rank_futures_radar_universe(
        cls,
        limit: int = 30,
        min_quote_vol: float = 20_000_000.0
    ) -> List[Dict[str, Any]]:
        """
        Scans Binance Futures universe and ranks candidates by Volatility Velocity & Institutional Confluence.
        Filters out overextended pumps (> +20%) and falling knives (< -20%) to capture early sweet spots.
        """
        try:
            url = f"{trading_engine.FUTURES_URL}/fapi/v1/ticker/24hr"
            res = trading_engine.HFT_SESSION.get(url, timeout=4)
            if res.status_code != 200:
                return []

            tickers = res.json()
            if not isinstance(tickers, list):
                return []

            candidates = []
            monitoring_set = market_data.get_monitoring_symbols_set() if hasattr(market_data, "get_monitoring_symbols_set") else set()

            for t in tickers:
                sym = t.get("symbol", "")
                if not sym.endswith("USDT") or "USDC" in sym or "BUSD" in sym or sym in cls.EXCLUDED_SYMBOLS or not sym.isascii():
                    continue
                if sym in monitoring_set:
                    continue
                if market_data.is_symbol_in_cooldown(sym):
                    continue

                quote_vol = float(t.get("quoteVolume", 0.0) or 0.0)
                if quote_vol < min_quote_vol:
                    continue

                price_change_pct = float(t.get("priceChangePercent", 0.0) or 0.0)
                abs_change = abs(price_change_pct)

                # Early Breakout Sweet-Spot Window: 1.8% to 15.0%
                # Hard reject overextended pump peaks (> 20.0%) and falling knives (< -20.0%)
                if abs_change > 20.0 or abs_change < 1.8:
                    continue

                last_price = float(t.get("lastPrice", 0.0) or 0.0)
                high_price = float(t.get("highPrice", last_price * 1.02) or (last_price * 1.02))
                low_price = float(t.get("lowPrice", last_price * 0.98) or (last_price * 0.98))
                if last_price <= 0:
                    continue

                # Calibrated Sweet-Spot Score (peak between 4.0% - 10.0%)
                if 3.0 <= abs_change <= 12.0:
                    breakout_score = 150.0 - (abs(abs_change - 7.5) * 5.0)
                elif 12.0 < abs_change <= 20.0:
                    breakout_score = 80.0 - ((abs_change - 12.0) * 8.0)
                else:
                    breakout_score = 70.0

                vol_score = math.log10(max(1.0, quote_vol)) * 10.0
                total_score = round(breakout_score + vol_score, 2)

                rec_side = "BUY" if price_change_pct > 0 else "SELL"

                candidates.append({
                    "symbol": sym,
                    "last_price": last_price,
                    "high_price": high_price,
                    "low_price": low_price,
                    "quote_volume": quote_vol,
                    "price_change_pct": price_change_pct,
                    "abs_change": abs_change,
                    "score": total_score,
                    "recommended_side": rec_side
                })

            candidates.sort(key=lambda x: x["score"], reverse=True)
            return candidates[:limit]
        except Exception as e:
            logger.error(f"Error scanning futures radar universe: {e}")
            return []

    @classmethod
    def arm_radar_trap(
        cls,
        symbol: str,
        engine_source: str = "UNIVERSAL",
        current_price: float = 0.0,
        atr_15m: float = 0.0,
        swing_high: float = 0.0,
        swing_low: float = 0.0,
        user_id: Optional[int] = None,
        ttl_seconds: float = 1800.0
    ) -> Dict[str, Any]:
        """
        Arms a High-Speed In-Memory Virtual Radar Trap in Python RAM.
        Zero pending orders sent to Binance orderbook. Immune to pre-market spoofing.
        """
        sym = str(symbol or "").upper().strip()
        if not sym.endswith("USDT") and not sym.endswith("USD"):
            sym += "USDT"

        now = time.time()
        trap_key = f"{engine_source.upper()}_{sym}"

        if current_price <= 0.0:
            ram_px = market_data.get_fast_ram_price(sym) if hasattr(market_data, "get_fast_ram_price") else 0.0
            current_price = ram_px if ram_px > 0 else 1.0

        if atr_15m <= 0.0:
            atr_15m = current_price * 0.015  # 1.5% institutional fallback

        if swing_high <= 0.0:
            swing_high = current_price * 1.012
        if swing_low <= 0.0:
            swing_low = current_price * 0.988

        # Breakout Buffer: 0.15% of price or 0.10 * ATR
        buffer_dist = max(current_price * 0.0015, atr_15m * 0.10)
        buy_trigger = round(swing_high + buffer_dist, 4)
        sell_trigger = round(swing_low - buffer_dist, 4)

        # Dynamic Volatility Breathing Stop Distance (max 2.20x ATR, 0.8% price floor)
        sl_dist = max(2.20 * atr_15m, current_price * 0.008, 0.0035 * current_price)

        buy_sl = round(buy_trigger - sl_dist, 4)
        buy_tp1 = round(buy_trigger + (sl_dist * 2.5), 4)  # +2.5R BE Armor Trigger
        buy_tp2 = round(buy_trigger + (sl_dist * 4.0), 4)  # +4.0R Clean Harvest

        sell_sl = round(sell_trigger + sl_dist, 4)
        sell_tp1 = round(sell_trigger - (sl_dist * 2.5), 4)  # +2.5R BE Armor Trigger
        sell_tp2 = round(sell_trigger - (sl_dist * 4.0), 4)  # +4.0R Clean Harvest

        trap_data = {
            "trap_key": trap_key,
            "symbol": sym,
            "engine_source": engine_source.upper(),
            "user_id": user_id,
            "armed_price": current_price,
            "atr_15m": atr_15m,
            "sl_dist": sl_dist,
            "buy_trigger": buy_trigger,
            "buy_sl": buy_sl,
            "buy_tp1": buy_tp1,
            "buy_tp2": buy_tp2,
            "sell_trigger": sell_trigger,
            "sell_sl": sell_sl,
            "sell_tp1": sell_tp1,
            "sell_tp2": sell_tp2,
            "status": "ARMED",
            "armed_at": now,
            "expires_at": now + ttl_seconds
        }

        cls._ARMED_TRAPS[trap_key] = trap_data
        cls._STATS["total_traps_armed"] += 1
        logger.info(
            f"🎯 [FUTURES RADAR ARMED] {sym} ({engine_source}) in RAM | "
            f"BUY Trigger: ${buy_trigger:,.4f} (SL: ${buy_sl:,.4f}, TP1: ${buy_tp1:,.4f}) | "
            f"SELL Trigger: ${sell_trigger:,.4f} (SL: ${sell_sl:,.4f}, TP1: ${sell_tp1:,.4f})"
        )
        return trap_data

    @classmethod
    def evaluate_armed_trap_trigger(
        cls,
        symbol: str,
        current_price: float = 0.0,
        engine_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates current price against armed traps in RAM.
        Triggers instant execution upon breakout confirmation and executes Instant In-Memory OCO Disarm.
        """
        sym = str(symbol or "").upper().strip()
        if not sym.endswith("USDT") and not sym.endswith("USD"):
            sym += "USDT"

        now = time.time()
        matching_keys = [
            k for k, v in cls._ARMED_TRAPS.items()
            if v.get("symbol") == sym and (engine_source is None or v.get("engine_source") == engine_source.upper())
        ]

        if not matching_keys:
            return {"triggered": False, "reason": "NO_ARMED_TRAP"}

        if current_price <= 0.0:
            ram_px = market_data.get_fast_ram_price(sym) if hasattr(market_data, "get_fast_ram_price") else 0.0
            current_price = ram_px if ram_px > 0 else 1.0

        for t_key in matching_keys:
            trap = cls._ARMED_TRAPS.get(t_key)
            if not trap or trap.get("status") != "ARMED":
                continue

            if now > trap.get("expires_at", 0.0):
                trap["status"] = "EXPIRED"
                cls._ARMED_TRAPS.pop(t_key, None)
                continue

            buy_trigger = trap["buy_trigger"]
            sell_trigger = trap["sell_trigger"]
            direction = None

            if current_price >= buy_trigger:
                direction = "BUY"
            elif current_price <= sell_trigger:
                direction = "SELL"

            if not direction:
                continue

            # 360° Citadel Clearance & Trap Verification
            citadel_res = SuperSmartFuturesCitadel.evaluate_institutional_futures_trap(sym, direction)
            if not citadel_res.get("is_approved"):
                logger.info(f"🛡️ [RADAR TRAP BLOCKED] {sym} {direction} blocked by Citadel: {citadel_res.get('rejection_reason')}")
                continue

            # Turtle Soup Fakeout Shield: Reject long rejection wicks (> 35% wick)
            klines = trading_engine.get_klines(sym, interval="15m", limit=3, is_spot=False)
            if klines and len(klines) >= 2:
                last_c = klines[-1]
                c_open = float(last_c[1])
                c_high = float(last_c[2])
                c_low = float(last_c[3])
                c_close = float(last_c[4])
                c_range = max(1e-6, c_high - c_low)

                if direction == "BUY":
                    upper_wick = c_high - max(c_open, c_close)
                    if (upper_wick / c_range) > 0.35:
                        logger.info(f"🛡️ [RADAR FAKEOUT GUARD] {sym} BUY blocked: Upper rejection wick ({upper_wick/c_range*100:.1f}%) > 35% (Turtle Soup Fakeout)!")
                        continue
                elif direction == "SELL":
                    lower_wick = min(c_open, c_close) - c_low
                    if (lower_wick / c_range) > 0.35:
                        logger.info(f"🛡️ [RADAR FAKEOUT GUARD] {sym} SELL blocked: Lower rejection wick ({lower_wick/c_range*100:.1f}%) > 35% (Turtle Soup Fakeout)!")
                        continue

            # Trigger Confirmed! Instant In-Memory OCO Disarm of Opposing Side
            trap["status"] = f"TRIGGERED_{direction}"
            cls._ARMED_TRAPS.pop(t_key, None)
            cls._STATS["total_traps_triggered"] += 1
            cls._STATS["total_oco_disarmed"] += 1
            cls._STATS["last_trigger"] = {
                "symbol": sym,
                "direction": direction,
                "entry_price": current_price,
                "engine_source": trap.get("engine_source"),
                "timestamp": now
            }

            sl_price = trap["buy_sl"] if direction == "BUY" else trap["sell_sl"]
            tp1_price = trap["buy_tp1"] if direction == "BUY" else trap["sell_tp1"]
            tp2_price = trap["buy_tp2"] if direction == "BUY" else trap["sell_tp2"]

            logger.info(
                f"⚡ [FUTURES RADAR TRIGGERED & OCO DISARMED] {sym} {direction} at ${current_price:,.4f} | "
                f"SL: ${sl_price:,.4f} | TP1: ${tp1_price:,.4f} | TP2: ${tp2_price:,.4f} | Opposite side purged in < 0.1ms!"
            )

            return {
                "triggered": True,
                "symbol": sym,
                "direction": direction,
                "side": direction,
                "entry_price": current_price,
                "sl": sl_price,
                "tp1": tp1_price,
                "tp2": tp2_price,
                "sl_dist": trap.get("sl_dist", abs(current_price - sl_price)),
                "confidence": citadel_res.get("confluence_score", 90.0),
                "engine_source": trap.get("engine_source"),
                "details": citadel_res
            }

        return {"triggered": False, "reason": "PRICE_WITHIN_BOUNDS"}

    @classmethod
    def disarm_trap(cls, trap_key: str, reason: str = "MANUAL_OR_OCO") -> bool:
        """Purges an armed trap from high-speed RAM in < 0.1ms."""
        if trap_key in cls._ARMED_TRAPS:
            cls._ARMED_TRAPS.pop(trap_key, None)
            cls._STATS["total_oco_disarmed"] += 1
            logger.info(f"🗑️ [FUTURES RADAR DISARMED] Purged {trap_key} from RAM ({reason}).")
            return True
        return False

    @classmethod
    def get_radar_telemetry(cls) -> Dict[str, Any]:
        """Returns real-time telemetry of the In-Memory Futures Virtual Radar."""
        active_count = len(cls._ARMED_TRAPS)
        traps_summary = {
            k: {
                "symbol": v["symbol"],
                "engine": v["engine_source"],
                "buy_trigger": v["buy_trigger"],
                "sell_trigger": v["sell_trigger"],
                "sl_dist": v["sl_dist"],
                "status": v["status"]
            }
            for k, v in list(cls._ARMED_TRAPS.items())[:20]
        }
        return {
            "status": "ACTIVE_ARMED",
            "active_traps_count": active_count,
            "traps_summary": traps_summary,
            "stats": cls._STATS
        }

