#!/usr/bin/env python3
"""
Order Flow Delta Absorption Engine - Institutional Boundary Absorption Footprint (AQ84 Pillar 3 / Invariant 102)
===================================================================================================================
Author: Angkor Quant Institutional Engineering
Authority: Absolute Architectural Ground Truth (Invariant 102)

Mathematical Mechanics & Market Microstructure:
When price advances into key structural boundaries such as Resistance 1 (R1) or Support 1 (S1)
(derived from Monte Safieddine's Capital.com Daily Market Report or broker volatility coordinates),
the system measures the Footprint Delta Absorption by evaluating the ratio between price displacement
(result) and traded volume delta (effort):

    Effort vs Result Ratio = RVOL / max(0.02, |Close - Open| / ATR_15m)

1. Bull Exhaustion & Bearish Delta Absorption at Resistance 1 (R1):
   - Price pushes into or pierces Resistance 1 (R1).
   - High aggressive buying volume arrives (RVOL >= 1.15x, positive volume delta).
   - Price stalls and fails to advance through R1 (Effort vs Result >= 2.0, or Upper Wick >= 35% of bar range).
   - Institutional Mechanics: Passive Institutional Limit Sell Orders (iceberg sell walls) absorb all
     market buy orders. Buyers exhaust their capital against the institutional ceiling.
   - True Institutional Winner: SELL
   - System Action:
     * Approves SELL with a +35.0 Citadel confluence score boost.
     * Anchors tight structural Stop Loss above the absorption high wick:
       SL = High_wick + max(2.0 * spread, 0.20 * ATR_15m)
     * Strictly VETOES BUY orders with BLOCKED_ORDER_FLOW_BULL_EXHAUSTION_VETO.

2. Bear Exhaustion & Bullish Delta Absorption at Support 1 (S1):
   - Price pushes into or pierces Support 1 (S1).
   - High aggressive panic sell volume arrives (RVOL >= 1.15x, negative volume delta).
   - Price stalls and fails to advance lower through S1 (Effort vs Result >= 2.0, or Lower Wick >= 35% of bar range).
   - Institutional Mechanics: Passive Institutional Limit Buy Orders (iceberg buy walls) absorb all
     panic sell orders. Sellers exhaust their capital against the institutional floor.
   - True Institutional Winner: BUY
   - System Action:
     * Approves BUY with a +35.0 Citadel confluence score boost.
     * Anchors tight structural Stop Loss below the absorption low wick:
       SL = Low_wick - max(2.0 * spread, 0.20 * ATR_15m)
     * Strictly VETOES SELL orders with BLOCKED_ORDER_FLOW_BEAR_EXHAUSTION_VETO.
"""

import math
import logging
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger("OrderFlowDeltaAbsorptionEngine")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s [%(name)s][%(levelname)s] %(message)s"))
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)


class OrderFlowDeltaAbsorptionEngine:
    """
    Institutional Order Flow Delta Absorption Engine.
    Detects iceberg limit absorption and buyer/seller exhaustion at Resistance 1 and Support 1.
    """

    DEFAULT_EFFORT_RESULT_THRESHOLD: float = 2.0
    DEFAULT_RVOL_THRESHOLD: float = 1.15
    DEFAULT_WICK_RATIO_THRESHOLD: float = 0.35

    @classmethod
    def calculate_candle_delta_metrics(
        cls,
        candles_15m: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates bar level price progress, relative volume (RVOL), volume delta,
        and effort versus result ratio from recent candlestick bars.
        """
        if not candles_15m or len(candles_15m) < 3:
            return {
                "rvol": 1.0,
                "volume_delta": 0.0,
                "buy_vol": 0.0,
                "sell_vol": 0.0,
                "price_progress": 0.0,
                "effort_vs_result": 1.0,
                "upper_wick_ratio": 0.0,
                "lower_wick_ratio": 0.0,
                "high_wick": 0.0,
                "low_wick": 0.0,
                "close_price": 0.0
            }

        volumes = [float(c.get("volume", c.get("vol", c.get("v", 100.0))) or 100.0) for c in candles_15m]
        avg_vol = float(sum(volumes[-20:]) / max(1, len(volumes[-20:]))) if len(volumes) >= 5 else max(1.0, volumes[-1])
        curr_vol = float(volumes[-1])
        rvol = float(curr_vol / max(1e-5, avg_vol))

        last_c = candles_15m[-1]
        o = float(last_c.get("open", last_c.get("o", 0.0)) or 0.0)
        h = float(last_c.get("high", last_c.get("h", 0.0)) or 0.0)
        l = float(last_c.get("low", last_c.get("l", 0.0)) or 0.0)
        c = float(last_c.get("close", last_c.get("c", 0.0)) or 0.0)

        b_range = max(1e-5, h - l)
        body = abs(c - o)
        upper_wick = max(0.0, h - max(o, c))
        lower_wick = max(0.0, min(o, c) - l)

        upper_wick_ratio = float(upper_wick / b_range)
        lower_wick_ratio = float(lower_wick / b_range)

        # Bulk volume classification proxy
        w_buy = max(0.0, min(1.0, 0.5 + (0.5 * ((c - o) / b_range))))
        buy_vol = curr_vol * w_buy
        sell_vol = curr_vol * (1.0 - w_buy)
        vol_delta = buy_vol - sell_vol

        # Estimate 15m ATR
        trs = []
        for i in range(1, len(candles_15m)):
            hi = float(candles_15m[i].get("high", 0.0))
            lo = float(candles_15m[i].get("low", 0.0))
            cp = float(candles_15m[i-1].get("close", 0.0))
            trs.append(max(hi - lo, abs(hi - cp), abs(lo - cp)))
        atr_15m = float(sum(trs[-14:]) / max(1, len(trs[-14:]))) if trs else max(1e-5, c * 0.005)

        price_progress = float(body / max(1e-5, atr_15m))
        effort_vs_result = float(rvol / max(0.02, price_progress))

        return {
            "rvol": round(rvol, 3),
            "volume_delta": round(vol_delta, 2),
            "buy_vol": round(buy_vol, 2),
            "sell_vol": round(sell_vol, 2),
            "price_progress": round(price_progress, 3),
            "effort_vs_result": round(effort_vs_result, 3),
            "upper_wick_ratio": round(upper_wick_ratio, 3),
            "lower_wick_ratio": round(lower_wick_ratio, 3),
            "high_wick": h,
            "low_wick": l,
            "close_price": c,
            "atr_15m": round(atr_15m, 4)
        }

    @classmethod
    def evaluate_delta_absorption(
        cls,
        epic: str,
        current_price: float,
        candles_15m: List[Dict[str, Any]],
        r1: Optional[float] = None,
        s1: Optional[float] = None,
        atr_15m: Optional[float] = None,
        spread: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Evaluates Order Flow Delta Absorption at Resistance 1 and Support 1.
        
        Args:
            epic: Asset symbol (e.g. GOLD, US100, NVDA, TSLA)
            current_price: Current market price
            candles_15m: Intraday 15m candlestick bars
            r1: Explicit Resistance 1 level. If None, queries CapitalMarketReportEngine.
            s1: Explicit Support 1 level. If None, queries CapitalMarketReportEngine.
            atr_15m: 15m ATR. If None, derived from candles.
            spread: Current broker spread.
            
        Returns:
            Dictionary with absorption regime, true institutional winner, structural stop, and telemetry.
        """
        metrics = cls.calculate_candle_delta_metrics(candles_15m)
        c_price = float(current_price or metrics.get("close_price", 1.0))
        atr_val = float(atr_15m or metrics.get("atr_15m", c_price * 0.005))
        sp_val = float(spread or (0.35 if "GOLD" in str(epic).upper() else 0.50))

        # Retrieve R1 and S1 from CapitalMarketReportEngine if not explicitly passed
        r1_val = r1
        s1_val = s1
        if r1_val is None or s1_val is None:
            try:
                import capital_market_report_engine as cmre
                rep = cmre.CapitalMarketReportEngine.get_market_report_data(epic, current_price=c_price)
                if r1_val is None and rep.get("res1"):
                    r1_val = float(rep["res1"])
                if s1_val is None and rep.get("sup1"):
                    s1_val = float(rep["sup1"])
            except Exception as e_rep:
                logger.debug(f"Market report fetch note: {e_rep}")

        # Fallback to dynamic swing boundaries if market report coordinates are unavailable
        if (r1_val is None or s1_val is None) and candles_15m and len(candles_15m) >= 15:
            highs = [float(c.get("high", 0.0)) for c in candles_15m[-25:]]
            lows = [float(c.get("low", 0.0)) for c in candles_15m[-25:]]
            if r1_val is None:
                r1_val = float(max(highs))
            if s1_val is None:
                s1_val = float(min(lows))

        r1_val = float(r1_val or (c_price + 2.0 * atr_val))
        s1_val = float(s1_val or (c_price - 2.0 * atr_val))

        rvol = metrics["rvol"]
        vol_delta = metrics["volume_delta"]
        effort_vs_result = metrics["effort_vs_result"]
        upper_wick_ratio = metrics["upper_wick_ratio"]
        lower_wick_ratio = metrics["lower_wick_ratio"]
        h_wick = metrics["high_wick"]
        l_wick = metrics["low_wick"]

        # Check multi-bar boundary interaction (current or recent 3 bars touched R1 or S1)
        recent_sub = candles_15m[-min(3, len(candles_15m)):] if candles_15m else []
        recent_highs = [float(c.get("high", 0.0)) for c in recent_sub] or [h_wick]
        recent_lows = [float(c.get("low", 0.0)) for c in recent_sub] or [l_wick]
        max_recent_high = max(recent_highs)
        min_recent_low = min(recent_lows)

        is_near_r1 = (abs(c_price - r1_val) <= 0.85 * atr_val) or (max_recent_high >= r1_val - 0.35 * atr_val)
        is_near_s1 = (abs(c_price - s1_val) <= 0.85 * atr_val) or (min_recent_low <= s1_val + 0.35 * atr_val)

        is_bull_exhaustion = False
        is_bear_exhaustion = False
        structural_sl = None
        score_boost = 0.0
        regime = "NORMAL_ORDER_FLOW"
        true_winner = "NEUTRAL"
        action = "NORMAL_CLEARANCE"
        reason = "Order flow within standard boundary tolerances."

        # Case 1: Bull Exhaustion / Bearish Absorption at Resistance 1
        if is_near_r1:
            # Aggressive buy flow entered, but price halted at R1
            has_buy_effort = (rvol >= cls.DEFAULT_RVOL_THRESHOLD or vol_delta > 0.0)
            has_absorption_stall = (
                upper_wick_ratio >= cls.DEFAULT_WICK_RATIO_THRESHOLD or
                effort_vs_result >= cls.DEFAULT_EFFORT_RESULT_THRESHOLD or
                (c_price <= r1_val + 0.15 * atr_val and max_recent_high >= r1_val - 0.15 * atr_val)
            )

            if has_buy_effort and has_absorption_stall:
                is_bull_exhaustion = True
                regime = "BEARISH_ABSORPTION_AT_R1"
                true_winner = "SELL"
                score_boost = 35.0
                action = "OPEN_INSTITUTIONAL_SELL"
                # Stop loss anchored tightly right above the absorption high wick
                sl_buffer = max(2.0 * sp_val, 0.20 * atr_val)
                structural_sl = round(max(h_wick, max_recent_high) + sl_buffer, 5)
                reason = (
                    f"BEARISH_DELTA_ABSORPTION_AT_R1: Price stalled at Resistance 1 (${r1_val:,.2f}) "
                    f"despite heavy buy volume (RVOL={rvol:.2f}x, Effort/Result={effort_vs_result:.2f}, Upper Wick={upper_wick_ratio*100:.1f}%). "
                    f"Institutional limit sell orders have absorbed all buy flow (Bull Exhaustion). Sellers Win."
                )

        # Case 2: Bear Exhaustion / Bullish Absorption at Support 1
        elif is_near_s1:
            # Aggressive sell flow entered, but price halted at S1
            has_sell_effort = (rvol >= cls.DEFAULT_RVOL_THRESHOLD or vol_delta < 0.0)
            has_absorption_stall = (
                lower_wick_ratio >= cls.DEFAULT_WICK_RATIO_THRESHOLD or
                effort_vs_result >= cls.DEFAULT_EFFORT_RESULT_THRESHOLD or
                (c_price >= s1_val - 0.15 * atr_val and min_recent_low <= s1_val + 0.15 * atr_val)
            )

            if has_sell_effort and has_absorption_stall:
                is_bear_exhaustion = True
                regime = "BULLISH_ABSORPTION_AT_S1"
                true_winner = "BUY"
                score_boost = 35.0
                action = "OPEN_INSTITUTIONAL_BUY"
                # Stop loss anchored tightly right below the absorption low wick
                sl_buffer = max(2.0 * sp_val, 0.20 * atr_val)
                structural_sl = round(min(l_wick, min_recent_low) - sl_buffer, 5)
                reason = (
                    f"BULLISH_DELTA_ABSORPTION_AT_S1: Price stalled at Support 1 (${s1_val:,.2f}) "
                    f"despite heavy sell volume (RVOL={rvol:.2f}x, Effort/Result={effort_vs_result:.2f}, Lower Wick={lower_wick_ratio*100:.1f}%). "
                    f"Institutional limit buy orders have absorbed all sell flow (Bear Exhaustion). Buyers Win."
                )

        is_absorption_active = is_bull_exhaustion or is_bear_exhaustion

        return {
            "epic": epic,
            "current_price": c_price,
            "r1": r1_val,
            "s1": s1_val,
            "is_absorption_active": is_absorption_active,
            "is_bull_exhaustion": is_bull_exhaustion,
            "is_bear_exhaustion": is_bear_exhaustion,
            "regime": regime,
            "true_institutional_winner": true_winner,
            "score_boost": score_boost,
            "structural_sl": structural_sl,
            "action": action,
            "reason": reason,
            "metrics": metrics
        }

    @classmethod
    def evaluate_boundary_absorption_gatekeeper(
        cls,
        epic: str,
        direction: str,
        current_price: float,
        candles_15m: List[Dict[str, Any]],
        r1: Optional[float] = None,
        s1: Optional[float] = None,
        atr_15m: Optional[float] = None,
        spread: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Gatekeeper evaluating proposed trade direction against boundary delta absorption.
        
        Rules:
        - If Bull Exhaustion at R1:
            * Proposed SELL is ALIGNED: Approved with +35.0 score boost and tight structural SL.
            * Proposed BUY is VETOED: BLOCKED_ORDER_FLOW_BULL_EXHAUSTION_VETO.
        - If Bear Exhaustion at S1:
            * Proposed BUY is ALIGNED: Approved with +35.0 score boost and tight structural SL.
            * Proposed SELL is VETOED: BLOCKED_ORDER_FLOW_BEAR_EXHAUSTION_VETO.
        - Otherwise: Normal clearance.
        """
        eval_res = cls.evaluate_delta_absorption(
            epic=epic,
            current_price=current_price,
            candles_15m=candles_15m,
            r1=r1,
            s1=s1,
            atr_15m=atr_15m,
            spread=spread
        )

        norm_dir = "BUY" if str(direction or "").upper() in ["BUY", "LONG"] else (
            "SELL" if str(direction or "").upper() in ["SELL", "SHORT"] else "HOLD"
        )

        is_aligned = True
        is_vetoed = False
        veto_reason = ""
        score_boost = 0.0
        action = "NORMAL_CLEARANCE"
        structural_sl = eval_res.get("structural_sl")

        if eval_res["is_bull_exhaustion"]:
            if norm_dir == "SELL":
                is_aligned = True
                is_vetoed = False
                score_boost = 35.0
                action = "RIDE_INSTITUTIONAL_SELL_AT_R1"
            elif norm_dir == "BUY":
                is_aligned = False
                is_vetoed = True
                score_boost = -35.0
                action = "VETO_BULL_EXHAUSTION_AT_R1"
                veto_reason = (
                    f"BLOCKED_ORDER_FLOW_BULL_EXHAUSTION_VETO: Price stalled at Resistance 1 (${eval_res['r1']:,.2f}) "
                    f"despite heavy buy volume delta (RVOL={eval_res['metrics']['rvol']}x). "
                    f"Institutional limit sellers have absorbed all buy flow (Bull Exhaustion). Longing into resistance wall prohibited."
                )

        elif eval_res["is_bear_exhaustion"]:
            if norm_dir == "BUY":
                is_aligned = True
                is_vetoed = False
                score_boost = 35.0
                action = "RIDE_INSTITUTIONAL_BUY_AT_S1"
            elif norm_dir == "SELL":
                is_aligned = False
                is_vetoed = True
                score_boost = -35.0
                action = "VETO_BEAR_EXHAUSTION_AT_S1"
                veto_reason = (
                    f"BLOCKED_ORDER_FLOW_BEAR_EXHAUSTION_VETO: Price stalled at Support 1 (${eval_res['s1']:,.2f}) "
                    f"despite heavy sell volume delta (RVOL={eval_res['metrics']['rvol']}x). "
                    f"Institutional limit buyers have absorbed all sell flow (Bear Exhaustion). Shorting into support floor prohibited."
                )

        return {
            "epic": epic,
            "direction": norm_dir,
            "is_absorption_active": eval_res["is_absorption_active"],
            "is_aligned": is_aligned,
            "is_vetoed": is_vetoed,
            "veto_reason": veto_reason,
            "score_boost": score_boost,
            "structural_sl": structural_sl,
            "true_institutional_winner": eval_res["true_institutional_winner"],
            "regime": eval_res["regime"],
            "action": action,
            "absorption_details": eval_res
        }


def evaluate_delta_absorption(epic: str, current_price: float, candles_15m: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Helper function evaluating delta absorption."""
    return OrderFlowDeltaAbsorptionEngine.evaluate_delta_absorption(epic, current_price, candles_15m, **kwargs)


def evaluate_boundary_absorption_gatekeeper(epic: str, direction: str, current_price: float, candles_15m: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Helper function evaluating boundary absorption gatekeeper."""
    return OrderFlowDeltaAbsorptionEngine.evaluate_boundary_absorption_gatekeeper(epic, direction, current_price, candles_15m, **kwargs)
