# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - INSTITUTIONAL DEALING RANGE EQUILIBRIUM CHOP ENGINE
==================================================================
AQ84 Pillar 4 / Invariant 103: Dealing Range Equilibrium Chop Veto & Boundary Acceleration Engine
Founder: HEM SINATH | Institutional Quantitative Governance

Mathematical Thesis:
Between 35.0% and 65.0% of the Dealing Range relative to P0 (Equilibrium Starting Point),
Resistance 1 (R1), and Support 1 (S1), price dynamics operate strictly via Brownian Motion
Random Walk. Directional momentum has negative mathematical expectancy (E[X] <= 0), and
order flow is dominated by retail herd infighting without institutional liquidity commitment.

Over 90% of retail traders bleed and blow up accounts by taking market orders in the middle
of chop. The system strictly VETOES any directional entries within this 35% - 65% equilibrium
zone, crushes bet sizing to 0.0, and waits until price reaches boundary zones:
  - Discount Boundary Zone (< 35.0% near S1): Where institutional limit buyers accumulate
    liquidity, absorb panic dumps (Bear Exhaustion), and spring Turtle Soup reversals.
  - Premium Boundary Zone (> 65.0% near R1): Where institutional limit sellers distribute
    liquidity, absorb euphoric breakouts (Bull Exhaustion), and spring upthrust reversals.
"""

import math
import logging
from typing import Dict, Any, Tuple, Optional, List

logger = logging.getLogger("DealingRangeEquilibriumChopEngine")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [EquilibriumChopEngine] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)


class DealingRangeEquilibriumChopEngine:
    """
    AQ84 Pillar 4 / Invariant 103 Engine:
    Detects and filters out random Brownian retail chop in the middle 30% of Dealing Range (35%-65%),
    while identifying high-conviction boundary acceleration near R1 and S1.
    """

    CHOP_LOWER_BOUND: float = 35.0
    CHOP_UPPER_BOUND: float = 65.0
    EXTREME_DISCOUNT_BOUND: float = 18.0
    EXTREME_PREMIUM_BOUND: float = 82.0

    @classmethod
    def resolve_dealing_range_coordinates(
        cls,
        epic: str,
        current_price: float,
        p0: Optional[float] = None,
        r1: Optional[float] = None,
        s1: Optional[float] = None,
        candles_15m: Optional[List[Dict[str, Any]]] = None,
        lookback: int = 35
    ) -> Dict[str, float]:
        """
        Resolves exact dealing range coordinates (P0, R1, S1, range_low, range_high, dealing_range).
        Prioritizes Monte Safieddine's Daily Market Report or broker volatility coordinates.
        Falls back to 15m candle swing structures.
        """
        resolved_p0 = p0
        resolved_r1 = r1
        resolved_s1 = s1

        # Fallback to candle lookback if coordinates are incomplete
        if resolved_r1 is None or resolved_s1 is None:
            if candles_15m and len(candles_15m) >= 15:
                window = min(lookback, len(candles_15m) - 2)
                sub_candles = candles_15m[-window:-2] if len(candles_15m) > 5 else candles_15m
                highs = [float(c.get("high", c.get("close", 0.0))) for c in sub_candles]
                lows = [float(c.get("low", c.get("close", 0.0))) for c in sub_candles]
                resolved_r1 = max(highs) if highs else current_price * 1.01
                resolved_s1 = min(lows) if lows else current_price * 0.99
            else:
                resolved_r1 = current_price * 1.015
                resolved_s1 = current_price * 0.985

        if resolved_p0 is None:
            resolved_p0 = (resolved_r1 + resolved_s1) / 2.0

        dealing_range = max(1e-6, resolved_r1 - resolved_s1)

        return {
            "p0": float(resolved_p0),
            "r1": float(resolved_r1),
            "s1": float(resolved_s1),
            "range_high": float(resolved_r1),
            "range_low": float(resolved_s1),
            "dealing_range": float(dealing_range)
        }

    @classmethod
    def calculate_dealing_range_position(
        cls,
        current_price: float,
        coords: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculates normalized dealing range percentage and quadrant positions.
        """
        r1 = coords["r1"]
        s1 = coords["s1"]
        p0 = coords["p0"]
        d_range = coords["dealing_range"]

        range_pct = ((current_price - s1) / d_range) * 100.0
        range_pct = round(max(-20.0, min(120.0, range_pct)), 2)

        # Quadrant positioning
        dist_to_p0 = current_price - p0
        dist_to_r1 = r1 - current_price
        dist_to_s1 = current_price - s1

        is_chop_zone = (cls.CHOP_LOWER_BOUND <= range_pct <= cls.CHOP_UPPER_BOUND)
        is_discount_zone = (range_pct < cls.CHOP_LOWER_BOUND)
        is_premium_zone = (range_pct > cls.CHOP_UPPER_BOUND)

        if is_chop_zone:
            zone_name = "EQUILIBRIUM_CHOP_ZONE"
        elif is_discount_zone:
            zone_name = "DISCOUNT_BOUNDARY_ZONE"
        else:
            zone_name = "PREMIUM_BOUNDARY_ZONE"

        return {
            "range_pct": range_pct,
            "p0": p0,
            "r1": r1,
            "s1": s1,
            "dealing_range": d_range,
            "dist_to_p0": round(dist_to_p0, 4),
            "dist_to_r1": round(dist_to_r1, 4),
            "dist_to_s1": round(dist_to_s1, 4),
            "is_chop_zone": is_chop_zone,
            "is_discount_zone": is_discount_zone,
            "is_premium_zone": is_premium_zone,
            "zone_name": zone_name
        }

    @classmethod
    def evaluate_equilibrium_chop_regime(
        cls,
        epic: str,
        current_price: float,
        p0: Optional[float] = None,
        r1: Optional[float] = None,
        s1: Optional[float] = None,
        candles_15m: Optional[List[Dict[str, Any]]] = None,
        atr_15m: Optional[float] = None,
        spread: float = 0.0
    ) -> Dict[str, Any]:
        """
        Evaluates dealing range equilibrium status for an asset.
        Returns detailed structural metrics, regime classification, and boundary proximity.
        """
        coords = cls.resolve_dealing_range_coordinates(
            epic=epic,
            current_price=current_price,
            p0=p0,
            r1=r1,
            s1=s1,
            candles_15m=candles_15m
        )
        pos = cls.calculate_dealing_range_position(current_price, coords)

        range_pct = pos["range_pct"]
        is_chop = pos["is_chop_zone"]

        if is_chop:
            action = "WAIT_FOR_BOUNDARY_REACTION"
            true_institutional_winner = "NONE_RETAIL_CHOP"
            explanation = (
                f"Price {current_price:.2f} is at {range_pct:.1f}% of Dealing Range [35.0% - 65.0%]. "
                f"Middle equilibrium around P0 ({coords['p0']:.2f}) is Brownian motion retail infighting without edge. "
                f"Wait for boundary approach (S1: {coords['s1']:.2f} or R1: {coords['r1']:.2f})."
            )
        elif pos["is_discount_zone"]:
            action = "EVALUATE_DISCOUNT_BOUNDARY_ACCELERATION"
            true_institutional_winner = "BUY_ACCUMULATION_FAVORED"
            explanation = (
                f"Price {current_price:.2f} is at {range_pct:.1f}% of Dealing Range (< 35.0%). "
                f"Approaching Support 1 boundary ({coords['s1']:.2f}). Institutional accumulation & sweep traps active."
            )
        else: # Premium zone
            action = "EVALUATE_PREMIUM_BOUNDARY_ACCELERATION"
            true_institutional_winner = "SELL_DISTRIBUTION_FAVORED"
            explanation = (
                f"Price {current_price:.2f} is at {range_pct:.1f}% of Dealing Range (> 65.0%). "
                f"Approaching Resistance 1 boundary ({coords['r1']:.2f}). Institutional distribution & upthrust traps active."
            )

        return {
            "epic": epic,
            "current_price": current_price,
            "range_pct": range_pct,
            "p0": coords["p0"],
            "r1": coords["r1"],
            "s1": coords["s1"],
            "dealing_range": coords["dealing_range"],
            "is_chop_zone": is_chop,
            "is_discount_zone": pos["is_discount_zone"],
            "is_premium_zone": pos["is_premium_zone"],
            "zone_name": pos["zone_name"],
            "action": action,
            "true_institutional_winner": true_institutional_winner,
            "explanation": explanation
        }

    @classmethod
    def evaluate_dealing_range_equilibrium_gatekeeper(
        cls,
        epic: str,
        direction: str,
        current_price: float,
        p0: Optional[float] = None,
        r1: Optional[float] = None,
        s1: Optional[float] = None,
        candles_15m: Optional[List[Dict[str, Any]]] = None,
        atr_15m: Optional[float] = None,
        spread: float = 0.0
    ) -> Dict[str, Any]:
        """
        Gatekeeper for Capital Citadel and Meta-Labeling Governor.
        Strictly VETOES directional market orders inside the middle 35%-65% chop zone.
        Awards +25.0 score boost when trading boundary-aligned momentum near R1 or S1.
        """
        norm_dir = str(direction or "").upper()
        res = cls.evaluate_equilibrium_chop_regime(
            epic=epic,
            current_price=current_price,
            p0=p0,
            r1=r1,
            s1=s1,
            candles_15m=candles_15m,
            atr_15m=atr_15m,
            spread=spread
        )

        range_pct = res["range_pct"]
        is_chop = res["is_chop_zone"]

        if is_chop:
            veto_reason = (
                f"BLOCKED_DEALING_RANGE_EQUILIBRIUM_CHOP_VETO: Price is at {range_pct:.1f}% of Dealing Range "
                f"[35.0% - 65.0%]. Middle equilibrium is Brownian motion retail chop without institutional edge. "
                f"Awaiting boundary approach to S1 ({res['s1']:.2f}) or R1 ({res['r1']:.2f})."
            )
            return {
                "is_vetoed": True,
                "is_aligned": False,
                "score_boost": -40.0,
                "veto_reason": veto_reason,
                "zone_name": res["zone_name"],
                "range_pct": range_pct,
                "action": res["action"],
                "true_institutional_winner": "NONE_RETAIL_CHOP"
            }

        # Boundary Zone Evaluation
        is_aligned = False
        score_boost = 0.0

        if res["is_discount_zone"]:
            # Discount zone near S1 favors BUY setups (accumulation / spring sweep)
            if norm_dir == "BUY":
                is_aligned = True
                score_boost = 25.0
            elif norm_dir == "SELL":
                is_aligned = False
                score_boost = -15.0 # Selling into support penalty unless structural breakdown
        elif res["is_premium_zone"]:
            # Premium zone near R1 favors SELL setups (distribution / upthrust sweep)
            if norm_dir == "SELL":
                is_aligned = True
                score_boost = 25.0
            elif norm_dir == "BUY":
                is_aligned = False
                score_boost = -15.0 # Buying into resistance penalty unless structural breakout

        return {
            "is_vetoed": False,
            "is_aligned": is_aligned,
            "score_boost": score_boost,
            "veto_reason": "",
            "zone_name": res["zone_name"],
            "range_pct": range_pct,
            "action": res["action"],
            "true_institutional_winner": res["true_institutional_winner"]
        }


# Convenience module-level aliases
evaluate_equilibrium_chop_regime = DealingRangeEquilibriumChopEngine.evaluate_equilibrium_chop_regime
evaluate_dealing_range_equilibrium_gatekeeper = DealingRangeEquilibriumChopEngine.evaluate_dealing_range_equilibrium_gatekeeper
