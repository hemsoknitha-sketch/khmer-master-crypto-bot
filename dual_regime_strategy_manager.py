# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - DUAL-REGIME STRATEGY MANAGER (GAP 3 / AQ76 SPECIFICATION)
========================================================================
Solves Gap 3 (ចន្លោះទី 3): Decoupling Hard Vetoes between Trend-Following and Mean-Reversion.

Core Problem:
Static global hard vetoes (e.g. RSI >= 70 unconditionally blocks BUY, RSI <= 36 unconditionally
blocks SELL, and H4 Bullish unconditionally blocks SELL) can choke high-conviction trades:
  1. In raging trend breakouts, RSI stays overbought (70-78) while price continues to expand.
  2. In counter-trend exhaustion setups, high RSI (72-78) + Liquidity Sweep of BSL is the
     exact textbook prerequisite for a short, but static H4/RSI vetoes blocked it.
  3. However, naively deleting guards causes catastrophic drawdown (buying tops and panic shorting).

Solution:
Decouple the trading system into two distinct, mathematically specialized Strategy Regimes:
  - STRATEGY A: TREND_FOLLOWING (Momentum Expansion & Pullback Continuation)
  - STRATEGY B: MEAN_REVERSION (Institutional Exhaustion & Turtle Soup Sweep Reversal)

Each strategy applies tailored, mathematically calibrated boundary vetoes.
"""

import math
import logging
from enum import Enum
from typing import Dict, Any, Tuple, Optional, List

logger = logging.getLogger("DualRegimeStrategyManager")


class StrategyRegime(str, Enum):
    TREND_FOLLOWING = "TREND_FOLLOWING"
    MEAN_REVERSION = "MEAN_REVERSION"
    EQUILIBRIUM_CHOP = "EQUILIBRIUM_CHOP"
    UNKNOWN = "UNKNOWN"


class DualRegimeStrategyManager:
    """
    Decouples and manages market regimes, selecting appropriate risk models and
    tailoring entry guards so neither trend runners nor counter-trend exhausts are choked.
    """

    @classmethod
    def classify_market_regime(
        cls,
        side: str,
        price_range_pct: float,
        adx_15m: float,
        rsi_15m: float,
        has_liquidity_sweep: bool,
        has_choch: bool,
        has_bos: bool,
        is_triple_ema_aligned: bool,
        h4_bias: str,
        has_order_block_test: bool = False,
        hurst_exponent: float = 0.50
    ) -> Tuple[StrategyRegime, Dict[str, Any]]:
        """
        Classifies current market setup into TREND_FOLLOWING, MEAN_REVERSION, or EQUILIBRIUM_CHOP.
        """
        norm_side = str(side or "BUY").upper().strip()
        regime_evidence = []

        # 1. Equilibrium Chop Zone Check (35% - 65% dealing range with low momentum)
        if 35.0 <= price_range_pct <= 65.0 and adx_15m < 22.0 and not has_liquidity_sweep:
            regime_evidence.append(f"EQUILIBRIUM_CHOP: Range {price_range_pct:.1f}% with ADX {adx_15m:.1f} < 22.0")
            return StrategyRegime.EQUILIBRIUM_CHOP, {
                "regime": StrategyRegime.EQUILIBRIUM_CHOP.value,
                "evidence": regime_evidence,
                "confidence": 0.90
            }

        # 2. Mean-Reversion / Exhaustion Characteristics:
        # - Price is at Range Extremes (>=75% for Short or <=25% for Long)
        # - Liquidity Sweep (BSL / SSL swept) OR Order Block Mitigation confirmed
        # - RSI is extreme (Overbought >= 55 for Sell, Oversold <= 45 for Buy)
        is_at_extreme = (price_range_pct >= 70.0 if norm_side == "SELL" else price_range_pct <= 30.0)
        has_institutional_edge = has_liquidity_sweep or has_order_block_test or has_choch

        if has_institutional_edge and is_at_extreme:
            if has_liquidity_sweep:
                regime_evidence.append(f"LIQUIDITY_SWEEP_EXTREME: Sweep at {price_range_pct:.1f}% range")
            if has_order_block_test:
                regime_evidence.append(f"ORDER_BLOCK_MITIGATION: OB Test at {price_range_pct:.1f}% range")
            if (norm_side == "SELL" and rsi_15m >= 55.0) or (norm_side == "BUY" and rsi_15m <= 45.0):
                regime_evidence.append(f"RSI_EXHAUSTION_ALIGNED: RSI {rsi_15m:.1f}")
            if hurst_exponent < 0.48:
                regime_evidence.append(f"HURST_MEAN_REVERTING: H={hurst_exponent:.2f} < 0.48")
            
            return StrategyRegime.MEAN_REVERSION, {
                "regime": StrategyRegime.MEAN_REVERSION.value,
                "evidence": regime_evidence,
                "confidence": 0.88
            }

        # 3. Trend-Following / Momentum Characteristics:
        # - ADX >= 25.0
        # - H4 Trend Alignment (Bullish for Buy, Bearish for Sell)
        # - Triple EMA stacked or BOS present
        # - Dealing Range not at counter-extreme
        is_h4_aligned = (h4_bias == ("BULLISH" if norm_side == "BUY" else "BEARISH"))
        if is_h4_aligned and (adx_15m >= 24.0 or is_triple_ema_aligned or has_bos):
            regime_evidence.append(f"H4_TREND_ALIGNED: {h4_bias}")
            if adx_15m >= 25.0:
                regime_evidence.append(f"ADX_MOMENTUM_EXPANSION: {adx_15m:.1f} >= 25.0")
            if is_triple_ema_aligned:
                regime_evidence.append("TRIPLE_EMA_STACK_ACTIVE")
            if has_bos:
                regime_evidence.append("BREAK_OF_STRUCTURE_BOS")

            return StrategyRegime.TREND_FOLLOWING, {
                "regime": StrategyRegime.TREND_FOLLOWING.value,
                "evidence": regime_evidence,
                "confidence": 0.88
            }

        # 4. Fallback: If price swept liquidity elsewhere, evaluate as Mean-Reversion; otherwise Trend-Following
        if has_liquidity_sweep or has_choch:
            return StrategyRegime.MEAN_REVERSION, {
                "regime": StrategyRegime.MEAN_REVERSION.value,
                "evidence": ["SWEEP_OR_CHOCH_DETECTED"],
                "confidence": 0.65
            }
        
        return StrategyRegime.TREND_FOLLOWING, {
            "regime": StrategyRegime.TREND_FOLLOWING.value,
            "evidence": ["DEFAULT_TREND_CONTINUATION"],
            "confidence": 0.60
        }

    @classmethod
    def evaluate_regime_vetoes(
        cls,
        strategy_regime: StrategyRegime,
        side: str,
        rsi_15m: float,
        adx_15m: float,
        price_range_pct: float,
        h4_bias: str,
        has_liquidity_sweep: bool,
        has_choch: bool,
        is_triple_ema_aligned: bool,
        has_order_block_test: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates tailored entry guards based on the active strategy regime.
        
        Returns:
            Dict containing:
              - is_vetoed: bool
              - veto_code: str ("PASSED", or specific rejection reason)
              - strategy_regime: str
              - explanation: str
        """
        norm_side = str(side or "BUY").upper().strip()

        # ====================================================================
        # CASE 0: EQUILIBRIUM CHOP ZONE VETO (Universal Invariant 76)
        # ====================================================================
        if strategy_regime == StrategyRegime.EQUILIBRIUM_CHOP:
            return {
                "is_vetoed": True,
                "veto_code": "VETO_EQUILIBRIUM_CHOP",
                "strategy_regime": strategy_regime.value,
                "explanation": (
                    f"EQUILIBRIUM_CHOP_VETO: Price is at {price_range_pct:.1f}% of dealing range "
                    f"with ADX {adx_15m:.1f} < 22.0. Trading inside the middle 30% of chop is strictly "
                    f"prohibited to eliminate Brownian random walk losses."
                )
            }

        # ====================================================================
        # CASE 1: STRATEGY A - TREND FOLLOWING REGIME
        # ====================================================================
        if strategy_regime == StrategyRegime.TREND_FOLLOWING:
            # Veto A1: H4 Macro Directional Alignment Anchor
            # Trend followers MUST NEVER fight the H4 Macro Trend!
            if norm_side == "SELL" and h4_bias == "BULLISH":
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_H4_TREND_FOLLOWING_SHORT",
                    "strategy_regime": strategy_regime.value,
                    "explanation": (
                        "H4_MACRO_TREND_VETO: H4 structure is BULLISH. Trend-following strategy "
                        "strictly forbids shorting against the institutional macro uptrend."
                    )
                }

            if norm_side == "BUY" and h4_bias == "BEARISH":
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_H4_TREND_FOLLOWING_LONG",
                    "strategy_regime": strategy_regime.value,
                    "explanation": (
                        "H4_MACRO_TREND_VETO: H4 structure is BEARISH. Trend-following strategy "
                        "strictly forbids buying against the institutional macro downtrend (Falling Knife)."
                    )
                }

            # Veto A2: Dynamic RSI Momentum & Blow-Off Euphoria Guard
            if norm_side == "BUY":
                # In strong momentum breakout (ADX >= 30, Triple EMA stacked), RSI can extend up to 78.0
                is_high_momentum = (adx_15m >= 30.0 and is_triple_ema_aligned)
                rsi_max_allowed = 78.0 if is_high_momentum else 68.0

                if rsi_15m > rsi_max_allowed:
                    return {
                        "is_vetoed": True,
                        "veto_code": "VETO_TREND_OVERBOUGHT_EUPHORIA",
                        "strategy_regime": strategy_regime.value,
                        "explanation": (
                            f"ANTI_OVERBOUGHT_GUARD: 15m RSI ({rsi_15m:.1f}) exceeds threshold ({rsi_max_allowed:.1f}). "
                            f"{'Even with strong ADX, buying above 78.0 is blow-off euphoria suicide.' if is_high_momentum else 'Without strong ADX momentum, buying above 68.0 is overextended.'}"
                        )
                    }

            if norm_side == "SELL":
                # In strong bear breakout (ADX >= 30, Bearish EMA stack), RSI can extend down to 28.0
                is_high_momentum = (adx_15m >= 30.0 and is_triple_ema_aligned)
                rsi_min_allowed = 28.0 if is_high_momentum else 38.0

                if rsi_15m < rsi_min_allowed:
                    return {
                        "is_vetoed": True,
                        "veto_code": "VETO_TREND_OVERSOLD_PANIC",
                        "strategy_regime": strategy_regime.value,
                        "explanation": (
                            f"ANTI_OVERSOLD_SHORT_GUARD: 15m RSI ({rsi_15m:.1f}) below threshold ({rsi_min_allowed:.1f}). "
                            f"{'Selling below 28.0 is panic bottom chasing even in bear trend.' if is_high_momentum else 'Selling below 38.0 without high ADX risks violent short squeeze.'}"
                        )
                    }

            # Veto A3: Deep Counter-Range Trap
            if norm_side == "BUY" and price_range_pct > 82.0 and not is_triple_ema_aligned:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_DEEP_PREMIUM_WITHOUT_MOMENTUM",
                    "strategy_regime": strategy_regime.value,
                    "explanation": f"DEEP_PREMIUM_TRAP: Price is at {price_range_pct:.1f}% without momentum stack."
                }

            if norm_side == "SELL" and price_range_pct < 18.0 and not is_triple_ema_aligned:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_DEEP_DISCOUNT_WITHOUT_MOMENTUM",
                    "strategy_regime": strategy_regime.value,
                    "explanation": f"DEEP_DISCOUNT_TRAP: Price is at {price_range_pct:.1f}% without momentum stack."
                }

            return {
                "is_vetoed": False,
                "veto_code": "PASSED_TREND_FOLLOWING",
                "strategy_regime": strategy_regime.value,
                "explanation": "Clearance granted for Trend-Following continuation."
            }

        # ====================================================================
        # CASE 2: STRATEGY B - MEAN REVERSION REGIME (TURTLE SOUP / EXHAUSTION)
        # ====================================================================
        if strategy_regime == StrategyRegime.MEAN_REVERSION:
            # Rule B1: MANDATORY INSTITUTIONAL EDGE REQUIREMENT
            # Counter-trend / Mean-reversion without a confirmed liquidity sweep or order block mitigation is RETAIL GAMBLING.
            has_edge = (has_liquidity_sweep or has_order_block_test or has_choch)
            if not has_edge:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_MEAN_REVERSION_NO_EDGE",
                    "strategy_regime": strategy_regime.value,
                    "explanation": (
                        "UNCONFIRMED_COUNTER_TREND: Mean-reversion entries strictly require confirmed "
                        "institutional evidence (Liquidity Sweep, Order Block mitigation, or CHoCH). "
                        "Trading counter-trend blindly is strictly prohibited."
                    )
                }

            # Rule B2: RUNAWAY FREIGHT TRAIN GUARD (ADX >= 42 without sweep)
            if adx_15m >= 42.0 and not has_liquidity_sweep:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_RUNAWAY_FREIGHT_TRAIN",
                    "strategy_regime": strategy_regime.value,
                    "explanation": (
                        f"RUNAWAY_TREND_GUARD: ADX ({adx_15m:.1f}) >= 42.0 indicates an institutional runaway "
                        f"freight train. Stepping in front of a parabolic trend without liquidity sweep is prohibited."
                    )
                }

            # Rule B3: EXHAUSTION PREREQUISITE (High RSI for Short, Low RSI for Long)
            # In Mean Reversion, RSI >= 50 is required for Shorting, RSI <= 50 for Longing.
            if norm_side == "SELL" and rsi_15m < 50.0:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_SHORT_NOT_OVERBOUGHT",
                    "strategy_regime": strategy_regime.value,
                    "explanation": f"MEAN_REVERSION_SHORT requires overbought conditions (RSI >= 50.0, got {rsi_15m:.1f})."
                }

            if norm_side == "BUY" and rsi_15m > 50.0:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_LONG_NOT_OVERSOLD",
                    "strategy_regime": strategy_regime.value,
                    "explanation": f"MEAN_REVERSION_LONG requires oversold conditions (RSI <= 50.0, got {rsi_15m:.1f})."
                }

            # Rule B4: RANGE BOUNDARY RESTRICTION (Must be at range extreme >= 65% for Short, <= 35% for Long)
            if norm_side == "SELL" and price_range_pct < 65.0:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_SHORT_NOT_PREMIUM",
                    "strategy_regime": strategy_regime.value,
                    "explanation": f"Mean-reversion Short requires Premium zone (Range >= 65%, got {price_range_pct:.1f}%)."
                }

            if norm_side == "BUY" and price_range_pct > 35.0:
                return {
                    "is_vetoed": True,
                    "veto_code": "VETO_LONG_NOT_DISCOUNT",
                    "strategy_regime": strategy_regime.value,
                    "explanation": f"Mean-reversion Long requires Discount zone (Range <= 35%, got {price_range_pct:.1f}%)."
                }

            # Notice: If H4 is Bullish, but price swept BSL or mitigated OB at 85% range with RSI >= 50,
            # CLEARANCE IS GRANTED for Mean-Reversion Short with tight SL behind the sweep wick!
            return {
                "is_vetoed": False,
                "veto_code": "PASSED_MEAN_REVERSION_EXHAUSTION",
                "strategy_regime": strategy_regime.value,
                "explanation": (
                    "Clearance granted for Institutional Mean-Reversion. "
                    "Liquidity Sweep / Order Block mitigation confirmed with tight SL."
                )
            }

        return {
            "is_vetoed": False,
            "veto_code": "PASSED_STANDARD",
            "strategy_regime": "UNKNOWN",
            "explanation": "Standard clearance granted."
        }
