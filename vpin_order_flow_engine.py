#!/usr/bin/env python3
"""
VPIN Order Flow Engine - Institutional Volume-Synchronized Probability of Toxicity (AQ84 Pillar 2 / Invariant 101)
===================================================================================================================
Author: Angkor Quant Institutional Engineering
Authority: Absolute Architectural Ground Truth (Invariant 101)

Mathematical Mechanics:
Based on David Easley, Marcos López de Prado, and Maureen O'Hara (2011, 2012):
"The Volume-Synchronized Probability of Toxicity (VPIN)"

Instead of slicing price into fixed clock time bars (where volume fluctuates wildly),
VPIN discretizes trading volume into equal-sized volume buckets of size V_bucket.
In each bucket tau:
    V_tau^B = Volume of buyer-initiated trades
    V_tau^S = Volume of seller-initiated trades
    V_tau^B + V_tau^S = V_bucket

The order flow imbalance in bucket tau is:
    Imbalance_tau = |V_tau^B - V_tau^S|

The VPIN metric over a rolling window of N completed buckets is:
    VPIN = (sum_{tau=1}^N |V_tau^B - V_tau^S|) / (N * V_bucket)
    where VPIN in [0.0, 1.0].

Institutional Governance & Unilateral Attack Guard:
When VPIN rises above 0.65 (VPIN >= 0.65):
    - Toxicity is EXTREME (Informed institutional flow attacking one side of the market).
    - If Net Toxic Flow > 0 (Bullish Toxicity):
        * Dominant flow is aggressive institutional buying.
        * BUY trades are ALIGNED: Ride the wave (+30.0 score boost, meta-prob expanded).
        * SELL trades are STRICTLY VETOED (VPIN_INSTITUTIONAL_TOXICITY_VETO).
    - If Net Toxic Flow < 0 (Bearish Toxicity):
        * Dominant flow is aggressive institutional liquidation.
        * SELL trades are ALIGNED: Ride the wave (+30.0 score boost, meta-prob expanded).
        * BUY trades are STRICTLY VETOED (VPIN_INSTITUTIONAL_TOXICITY_VETO).
"""

import math
import logging
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger("VPINOrderFlowEngine")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s [%(name)s][%(levelname)s] %(message)s"))
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)


class VPINOrderFlowEngine:
    """
    Institutional VPIN (Volume-Synchronized Probability of Toxicity) Engine.
    Discretizes volume into equal-sized buckets and measures informed trader imbalance.
    """

    DEFAULT_TOXICITY_THRESHOLD: float = 0.65
    DEFAULT_NUM_BUCKETS: int = 20
    MIN_CANDLES_REQUIRED: int = 5

    @classmethod
    def decompose_candle_volume_bvc(
        cls,
        open_p: float,
        high_p: float,
        low_p: float,
        close_p: float,
        volume: float,
        sigma_dp: Optional[float] = None,
        prev_close: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Bulk Volume Classification (BVC) decomposition into Buy Volume and Sell Volume.
        If sigma_dp and prev_close are provided, uses standardized normal CDF Phi(DeltaP / sigma).
        Otherwise, uses the intraday candle microstructure range: (Close - Low) / (High - Low).
        """
        if volume <= 0.0:
            return 0.0, 0.0

        b_range = high_p - low_p
        if b_range > 1e-6:
            # Microstructure range positioning
            range_weight = max(0.0, min(1.0, (close_p - low_p) / b_range))
            
            # Body thrust factor
            body_thrust = (close_p - open_p) / b_range
            thrust_weight = max(0.0, min(1.0, 0.5 + 0.5 * body_thrust))
            
            # Continuous CDF factor if inter-bar delta is available
            if sigma_dp is not None and sigma_dp > 1e-6 and prev_close is not None:
                z = (close_p - prev_close) / sigma_dp
                # Phi(z) = 0.5 * (1 + erf(z / sqrt(2)))
                cdf_weight = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
                w_buy = (range_weight * 0.40) + (thrust_weight * 0.35) + (cdf_weight * 0.25)
            else:
                w_buy = (range_weight * 0.50) + (thrust_weight * 0.50)
        else:
            w_buy = 0.50

        w_buy = max(0.0, min(1.0, w_buy))
        buy_vol = volume * w_buy
        sell_vol = volume * (1.0 - w_buy)
        return buy_vol, sell_vol

    @classmethod
    def compute_vpin(
        cls,
        candles_15m: List[Dict[str, Any]],
        num_buckets: int = 20,
        lookback_bars: int = 40,
        bucket_volume: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Discretizes intraday candle volume into equal-sized Volume Buckets and calculates VPIN.
        
        Args:
            candles_15m: List of candle dicts with open, high, low, close, volume
            num_buckets: Number of equal-volume buckets in the evaluation window (default 20)
            lookback_bars: Number of recent bars to consider (default 40)
            bucket_volume: Explicit bucket volume size. If None, derives V_bucket = Total_Volume / num_buckets
            
        Returns:
            Dictionary with VPIN, toxicity metrics, dominant flow direction, and bucket telemetry.
        """
        if not candles_15m or len(candles_15m) < cls.MIN_CANDLES_REQUIRED:
            return {
                "vpin": 0.50,
                "is_toxic": False,
                "toxicity_threshold": cls.DEFAULT_TOXICITY_THRESHOLD,
                "net_toxicity_ratio": 0.0,
                "dominant_toxic_flow": "BALANCED",
                "true_institutional_winner": "NEUTRAL",
                "completed_buckets": 0,
                "bucket_volume": 0.0,
                "total_volume": 0.0,
                "avg_imbalance_per_bucket": 0.0,
                "regime": "INSUFFICIENT_DATA"
            }

        sub = candles_15m[-min(lookback_bars, len(candles_15m)):]
        opens = [float(c.get("open", c.get("o", 0.0)) or 0.0) for c in sub]
        highs = [float(c.get("high", c.get("h", 0.0)) or 0.0) for c in sub]
        lows = [float(c.get("low", c.get("l", 0.0)) or 0.0) for c in sub]
        closes = [float(c.get("close", c.get("c", 0.0)) or 0.0) for c in sub]
        volumes = [float(c.get("volume", c.get("vol", c.get("v", 100.0))) or 100.0) for c in sub]

        total_vol = sum(volumes)
        if total_vol <= 0.0:
            return {
                "vpin": 0.50,
                "is_toxic": False,
                "toxicity_threshold": cls.DEFAULT_TOXICITY_THRESHOLD,
                "net_toxicity_ratio": 0.0,
                "dominant_toxic_flow": "BALANCED",
                "true_institutional_winner": "NEUTRAL",
                "completed_buckets": 0,
                "bucket_volume": 0.0,
                "total_volume": 0.0,
                "avg_imbalance_per_bucket": 0.0,
                "regime": "ZERO_VOLUME"
            }

        # Calculate price delta standard deviation for BVC CDF
        dp_list = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
        if dp_list:
            mean_dp = sum(dp_list) / len(dp_list)
            var_dp = sum((x - mean_dp) ** 2 for x in dp_list) / max(1, len(dp_list) - 1)
            sigma_dp = math.sqrt(var_dp)
        else:
            sigma_dp = 0.01

        # Determine target bucket volume V_bucket
        if bucket_volume and bucket_volume > 0.0:
            v_bucket = float(bucket_volume)
        else:
            v_bucket = max(1.0, total_vol / float(num_buckets))

        # Discretize into equal volume buckets
        buckets = []  # List of (buy_vol, sell_vol)
        curr_bucket_buy = 0.0
        curr_bucket_sell = 0.0
        curr_bucket_rem = v_bucket

        for i in range(len(sub)):
            o = opens[i]
            h = highs[i]
            l = lows[i]
            c = closes[i]
            v = volumes[i]
            prev_c = closes[i - 1] if i > 0 else o

            b_vol, s_vol = cls.decompose_candle_volume_bvc(
                open_p=o, high_p=h, low_p=l, close_p=c, volume=v,
                sigma_dp=sigma_dp, prev_close=prev_c
            )

            # Candle's buy/sell fraction
            frac_buy = b_vol / max(1e-6, v)
            frac_sell = s_vol / max(1e-6, v)
            candle_rem = v

            while candle_rem > 0:
                if candle_rem >= curr_bucket_rem:
                    # Fill the remaining space in current bucket
                    curr_bucket_buy += curr_bucket_rem * frac_buy
                    curr_bucket_sell += curr_bucket_rem * frac_sell
                    candle_rem -= curr_bucket_rem

                    # Bucket completed!
                    buckets.append((curr_bucket_buy, curr_bucket_sell))

                    # Reset for next bucket
                    curr_bucket_buy = 0.0
                    curr_bucket_sell = 0.0
                    curr_bucket_rem = v_bucket
                else:
                    # Partially fill current bucket
                    curr_bucket_buy += candle_rem * frac_buy
                    curr_bucket_sell += candle_rem * frac_sell
                    curr_bucket_rem -= candle_rem
                    candle_rem = 0.0

        # If last partial bucket is at least 50% filled, include it proportionally
        if (v_bucket - curr_bucket_rem) >= (0.50 * v_bucket):
            filled = v_bucket - curr_bucket_rem
            scale = v_bucket / max(1e-6, filled)
            buckets.append((curr_bucket_buy * scale, curr_bucket_sell * scale))

        if not buckets:
            return {
                "vpin": 0.50,
                "is_toxic": False,
                "toxicity_threshold": cls.DEFAULT_TOXICITY_THRESHOLD,
                "net_toxicity_ratio": 0.0,
                "dominant_toxic_flow": "BALANCED",
                "true_institutional_winner": "NEUTRAL",
                "completed_buckets": 0,
                "bucket_volume": round(v_bucket, 2),
                "total_volume": round(total_vol, 2),
                "avg_imbalance_per_bucket": 0.0,
                "regime": "INSUFFICIENT_BUCKETS"
            }

        # Rolling VPIN calculation over recent N completed buckets
        active_buckets = buckets[-min(len(buckets), num_buckets):]
        n_act = len(active_buckets)

        abs_imbalances = [abs(b - s) for b, s in active_buckets]
        signed_imbalances = [b - s for b, s in active_buckets]

        sum_abs_imbalance = sum(abs_imbalances)
        sum_signed_imbalance = sum(signed_imbalances)
        total_eval_volume = n_act * v_bucket

        vpin = float(sum_abs_imbalance / max(1e-6, total_eval_volume))
        vpin = max(0.0, min(1.0, vpin))

        net_toxicity_ratio = float(sum_signed_imbalance / max(1e-6, total_eval_volume))
        net_toxicity_ratio = max(-1.0, min(1.0, net_toxicity_ratio))

        is_toxic = bool(vpin >= cls.DEFAULT_TOXICITY_THRESHOLD)

        if is_toxic:
            if net_toxicity_ratio > 0.0:
                dominant_toxic_flow = "BULLISH"
                true_winner = "BUY"
                regime = "HIGH_TOXICITY_BULLISH_WAVE"
            else:
                dominant_toxic_flow = "BEARISH"
                true_winner = "SELL"
                regime = "HIGH_TOXICITY_BEARISH_WAVE"
        else:
            dominant_toxic_flow = "BALANCED"
            true_winner = "NEUTRAL"
            regime = "NORMAL_BALANCED_FLOW"

        return {
            "vpin": round(vpin, 4),
            "is_toxic": is_toxic,
            "toxicity_threshold": cls.DEFAULT_TOXICITY_THRESHOLD,
            "net_toxicity_ratio": round(net_toxicity_ratio, 4),
            "dominant_toxic_flow": dominant_toxic_flow,
            "true_institutional_winner": true_winner,
            "completed_buckets": len(buckets),
            "eval_buckets": n_act,
            "bucket_volume": round(v_bucket, 2),
            "total_volume": round(total_vol, 2),
            "avg_imbalance_per_bucket": round(sum_abs_imbalance / max(1, n_act), 2),
            "regime": regime
        }

    @classmethod
    def evaluate_vpin_toxicity_gatekeeper(
        cls,
        candles_15m: List[Dict[str, Any]],
        proposed_side: str,
        threshold: float = 0.65
    ) -> Dict[str, Any]:
        """
        Gatekeeper evaluating proposed trade direction against institutional order flow toxicity.
        
        Rules:
        - If VPIN >= 0.65:
            * If side is ALIGNED with dominant toxic flow:
                is_aligned = True, is_vetoed = False, score_boost = +30.0 (Ride the wave).
            * If side OPPOSES dominant toxic flow:
                is_aligned = False, is_vetoed = True, score_boost = -35.0 (Strict Veto).
        - If VPIN < 0.65:
            * Normal clearance, no toxicity veto.
        """
        vpin_res = cls.compute_vpin(candles_15m)
        vpin = vpin_res.get("vpin", 0.50)
        is_toxic = bool(vpin >= threshold)
        dominant_flow = vpin_res.get("dominant_toxic_flow", "BALANCED")
        net_tox = vpin_res.get("net_toxicity_ratio", 0.0)

        norm_side = "BUY" if str(proposed_side or "").upper() in ["BUY", "LONG"] else (
            "SELL" if str(proposed_side or "").upper() in ["SELL", "SHORT"] else "HOLD"
        )

        is_aligned = True
        is_vetoed = False
        veto_reason = ""
        score_boost = 0.0
        action = "NORMAL_CLEARANCE"

        is_bull_flow = dominant_flow in ["BULLISH", "BUY"]
        is_bear_flow = dominant_flow in ["BEARISH", "SELL"]
        is_match = (norm_side == "BUY" and is_bull_flow) or (norm_side == "SELL" and is_bear_flow)

        if is_toxic:
            if is_match:
                is_aligned = True
                is_vetoed = False
                score_boost = 30.0
                action = f"RIDE_TOXIC_{dominant_flow}_WAVE"
            else:
                is_aligned = False
                is_vetoed = True
                score_boost = -35.0
                action = "VETO_TOXIC_COUNTER_TRADE"
                veto_reason = (
                    f"VPIN_INSTITUTIONAL_TOXICITY_VETO: VPIN={vpin:.3f} >= {threshold:.2f} proves "
                    f"aggressive {dominant_flow} institutional order flow attack (Net Toxicity: {net_tox:+.2f}). "
                    f"{norm_side} trade is strictly prohibited to prevent capital destruction."
                )

        return {
            "vpin": vpin,
            "is_toxic": is_toxic,
            "threshold": threshold,
            "proposed_side": norm_side,
            "dominant_toxic_flow": dominant_flow,
            "true_institutional_winner": vpin_res.get("true_institutional_winner", "NEUTRAL"),
            "net_toxicity_ratio": net_tox,
            "is_aligned": is_aligned,
            "is_vetoed": is_vetoed,
            "veto_reason": veto_reason,
            "score_boost": score_boost,
            "action": action,
            "vpin_telemetry": vpin_res
        }


def compute_vpin(candles_15m: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
    """Helper function computing VPIN metrics."""
    return VPINOrderFlowEngine.compute_vpin(candles_15m, **kwargs)


def evaluate_vpin_toxicity(candles_15m: List[Dict[str, Any]], proposed_side: str, **kwargs) -> Dict[str, Any]:
    """Helper function evaluating VPIN toxicity gatekeeper."""
    return VPINOrderFlowEngine.evaluate_vpin_toxicity_gatekeeper(candles_15m, proposed_side, **kwargs)
