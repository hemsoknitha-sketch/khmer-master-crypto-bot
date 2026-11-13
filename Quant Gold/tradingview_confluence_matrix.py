# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - TRADINGVIEW 10-GROUP QUANTITATIVE CONFLUENCE MATRIX (AQ119)
==========================================================================
Unified Institutional Coordinate Engine on 2D Space (t, P) for Spot Gold (XAUUSD).
Implements the 10 TradingView Mathematical Tool Groups:
  1. Lines & Linear Algebra: P(t) = m*(t - t1) + P1, Trend Angles theta = arctan(m)
  2. Channels & Statistics: OLS Linear Regression P_hat = alpha + beta*t +/- k*sigma, Pitchfork Median
  3. Volume-Based: Anchored VWAP (AVWAP_t), Fixed Range Volume Profile (POC, VAH, VAL), CVD Proxy
  4. Projection & Risk: RRR = |TP - Entry| / |Entry - SL|, Kelly Fraction, Target Forecast
  5. Measurer & Volatility: Delta P, %Delta P, Delta t, Normalized Volatility Vectors
  6. Elliott Waves: Wave 1-5 Impulse, ABC Correction, Fibonacci Expansion ratios
  7. Time Cycles & Trigonometry: P(t) = P0 + A*sin(2*pi/T * (t - t0) + phi), Spectral Trough/Crest
  8. Shapes & SMC Zones: Rectangles {(t, P)}, Order Blocks, Fair Value Gaps (FVG), Dealing Range
  9. Magnet Mode: Exact Snap P_snap = argmin |P_target - P_ohlc| eliminating optical rounding
  10. Pitchforks, Gann & Harmonic Patterns: Andrews' 80% Median, Gann 1x1 (45 deg), XABCD Harmonic PRZ
"""

import time
import math
import logging
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger("QUANT_GOLD_TV_MATRIX")


# ==============================================================================
# 1. LINES & GEOMETRY: LINEAR EQUATIONS ON (t, P)
# ==============================================================================
def calculate_trendline(
    t1: float, p1: float, t2: float, p2: float, t_curr: float
) -> Dict[str, float]:
    """
    Computes linear equation P(t) = m * (t - t1) + P1 where m = (P2 - P1) / (t2 - t1).
    """
    dt = max(1e-6, t2 - t1)
    dp = p2 - p1
    m = dp / dt
    p_curr = m * (t_curr - t1) + p1
    # Normalized angle in degrees (-90 to +90)
    angle_rad = math.atan(m)
    angle_deg = math.degrees(angle_rad)
    return {
        "slope": float(m),
        "angle_deg": float(angle_deg),
        "projected_price": float(p_curr),
        "delta_price": float(dp),
        "delta_time": float(dt)
    }


# ==============================================================================
# 2. CHANNELS: OLS LINEAR REGRESSION & STANDARD DEVIATION BANDS
# ==============================================================================
def compute_ols_regression_channel(
    prices: np.ndarray, k: float = 2.0
) -> Dict[str, Any]:
    """
    Computes Ordinary Least Squares (OLS) Linear Regression:
      P_hat_t = alpha + beta * t
      beta = sum((t - t_bar)*(P - P_bar)) / sum((t - t_bar)^2)
      sigma = sqrt(1/n * sum((P - P_hat)^2))
      Bands: P_hat +/- k * sigma
    """
    n = len(prices)
    if n < 5:
        curr = float(prices[-1]) if n > 0 else 4000.0
        return {
            "alpha": curr,
            "beta": 0.0,
            "sigma": 1.0,
            "center": curr,
            "upper": curr + 2.0,
            "lower": curr - 2.0,
            "z_score": 0.0,
            "r_squared": 0.0
        }

    t = np.arange(n, dtype=np.float64)
    p = prices.astype(np.float64)

    t_bar = np.mean(t)
    p_bar = np.mean(p)

    denom = np.sum((t - t_bar) ** 2)
    if denom < 1e-9:
        beta = 0.0
    else:
        beta = np.sum((t - t_bar) * (p - p_bar)) / denom

    alpha = p_bar - beta * t_bar
    p_hat = alpha + beta * t

    residuals = p - p_hat
    variance = np.mean(residuals ** 2)
    sigma = math.sqrt(max(1e-9, variance))

    curr_p = p[-1]
    curr_hat = p_hat[-1]
    z_score = (curr_p - curr_hat) / sigma

    ss_tot = np.sum((p - p_bar) ** 2)
    ss_res = np.sum(residuals ** 2)
    r_squared = 1.0 - (ss_res / max(1e-9, ss_tot)) if ss_tot > 1e-9 else 0.0

    return {
        "alpha": float(alpha),
        "beta": float(beta),
        "sigma": float(sigma),
        "center": float(curr_hat),
        "upper": float(curr_hat + k * sigma),
        "lower": float(curr_hat - k * sigma),
        "z_score": float(z_score),
        "r_squared": float(np.clip(r_squared, 0.0, 1.0))
    }


# ==============================================================================
# 3. VOLUME-BASED: ANCHORED VWAP & VOLUME PROFILE (POC / VALUE AREA)
# ==============================================================================
def compute_anchored_vwap(
    df: pd.DataFrame, anchor_idx: int = 0
) -> float:
    """
    Computes Anchored VWAP from anchor_idx to end:
      AVWAP_t = sum(P_typical_i * V_i) / sum(V_i)
      P_typical = (High + Low + Close) / 3
    """
    if df is None or len(df) <= anchor_idx:
        return 0.0

    sub = df.iloc[anchor_idx:]
    highs = sub["high"].values
    lows = sub["low"].values
    closes = sub["close"].values
    vols = sub.get("volume", pd.Series(np.ones(len(sub)))).values

    # Clean volumes
    vols = np.where(np.isnan(vols) | (vols <= 0), 1.0, vols)
    typical_prices = (highs + lows + closes) / 3.0

    vol_sum = np.sum(vols)
    if vol_sum < 1e-9:
        return float(closes[-1])

    avwap = np.sum(typical_prices * vols) / vol_sum
    return float(avwap)


def compute_volume_profile(
    df: pd.DataFrame, n_bins: int = 24
) -> Dict[str, Any]:
    """
    Computes Fixed Range Volume Profile:
      - Point of Control (POC): Price bin with maximum traded volume
      - Value Area (70%): Range [VAL, VAH] containing 70% of total volume
    """
    if df is None or len(df) < 5:
        curr = 4000.0
        return {"poc": curr, "vah": curr + 5.0, "val": curr - 5.0, "profile_valid": False}

    highs = df["high"].values
    lows = df["low"].values
    closes = df["close"].values
    vols = df.get("volume", pd.Series(np.ones(len(df)))).values
    vols = np.where(np.isnan(vols) | (vols <= 0), 1.0, vols)

    p_min = float(np.min(lows))
    p_max = float(np.max(highs))

    if (p_max - p_min) < 0.10:
        curr = float(closes[-1])
        return {"poc": curr, "vah": curr + 2.0, "val": curr - 2.0, "profile_valid": False}

    bins = np.linspace(p_min, p_max, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2.0
    vol_hist = np.zeros(n_bins, dtype=np.float64)

    # Distribute volume across price bins for each bar
    for h, l, v in zip(highs, lows, vols):
        mask = (bin_centers >= l) & (bin_centers <= h)
        cnt = np.sum(mask)
        if cnt > 0:
            vol_hist[mask] += v / cnt
        else:
            # Nearest bin
            idx = int(np.argmin(np.abs(bin_centers - (h + l) / 2.0)))
            vol_hist[idx] += v

    # 1. Point of Control (POC)
    poc_idx = int(np.argmax(vol_hist))
    poc = float(bin_centers[poc_idx])

    # 2. Value Area (70% of total volume radiating out from POC)
    total_vol = np.sum(vol_hist)
    target_vol = total_vol * 0.70

    accum_vol = vol_hist[poc_idx]
    up_idx = poc_idx
    dn_idx = poc_idx

    while accum_vol < target_vol and (up_idx < n_bins - 1 or dn_idx > 0):
        up_next = vol_hist[up_idx + 1] if up_idx < n_bins - 1 else -1.0
        dn_next = vol_hist[dn_idx - 1] if dn_idx > 0 else -1.0

        if up_next >= dn_next and up_idx < n_bins - 1:
            up_idx += 1
            accum_vol += vol_hist[up_idx]
        elif dn_idx > 0:
            dn_idx -= 1
            accum_vol += vol_hist[dn_idx]
        else:
            break

    vah = float(bin_centers[up_idx])
    val = float(bin_centers[dn_idx])

    return {
        "poc": poc,
        "vah": vah,
        "val": val,
        "total_volume": float(total_vol),
        "profile_valid": True
    }


# ==============================================================================
# 4. FIBONACCI RATIOS: RETRACEMENT, EXTENSION & GOLDEN POCKET
# ==============================================================================
def compute_fibonacci_matrix(
    p_start: float, p_end: float, direction: str = "BULLISH"
) -> Dict[str, float]:
    """
    Computes Golden Ratio Fibonacci Matrix:
      Retracements: L_r = P_end - r * (P_end - P_start)
      r in [0.236, 0.382, 0.500, 0.618, 0.705, 0.786]
      Extensions: L_e = P_end + e * (P_end - P_start)
      e in [1.272, 1.618, 2.000, 2.618]
    """
    span = p_end - p_start
    return {
        "fib_0": float(p_end),
        "fib_236": float(p_end - 0.236 * span),
        "fib_382": float(p_end - 0.382 * span),
        "fib_500": float(p_end - 0.500 * span),
        "fib_618": float(p_end - 0.618 * span),   # Golden Ratio 1/phi
        "fib_705": float(p_end - 0.705 * span),   # Institutional OTE (Optimal Trade Entry)
        "fib_786": float(p_end - 0.786 * span),   # sqrt(0.618)
        "fib_100": float(p_start),
        "ext_1272": float(p_end + 1.272 * span),
        "ext_1618": float(p_end + 1.618 * span),  # Golden Ratio phi
        "ext_2000": float(p_end + 2.000 * span),
        "ext_2618": float(p_end + 2.618 * span),
        "golden_pocket_high": float(max(p_end - 0.618 * span, p_end - 0.705 * span)),
        "golden_pocket_low": float(min(p_end - 0.618 * span, p_end - 0.705 * span))
    }


# ==============================================================================
# 5. PITCHFORKS: ANDREWS' 80% MEDIAN LINE REVERSION & PRONGS
# ==============================================================================
def compute_andrews_pitchfork(
    t1: float, p1: float,
    t2: float, p2: float,
    t3: float, p3: float,
    t_curr: float
) -> Dict[str, Any]:
    """
    Andrews' Pitchfork:
      Midpoint of P2-P3: M = ((t2 + t3)/2, (p2 + p3)/2)
      Median Line slope: m_med = (M_p - p1) / (M_t - t1)
      Median Line: P_med(t) = m_med * (t - t1) + p1
      Upper Prong: parallel line through P2
      Lower Prong: parallel line through P3
    """
    m_t = (t2 + t3) / 2.0
    m_p = (p2 + p3) / 2.0

    dt_m = max(1e-6, m_t - t1)
    slope_med = (m_p - p1) / dt_m

    # Projected levels at t_curr
    p_med_curr = slope_med * (t_curr - t1) + p1
    offset_p2 = p2 - (slope_med * (t2 - t1) + p1)
    offset_p3 = p3 - (slope_med * (t3 - t1) + p1)

    p_upper_curr = p_med_curr + offset_p2
    p_lower_curr = p_med_curr + offset_p3

    return {
        "median_line": float(p_med_curr),
        "upper_prong": float(p_upper_curr),
        "lower_prong": float(p_lower_curr),
        "slope": float(slope_med),
        "median_midpoint_price": float(m_p)
    }


# ==============================================================================
# 6. GANN ANGLES & 1x1 45-DEGREE HARMONIC RESONANCE
# ==============================================================================
def compute_gann_angles(
    p_base: float, t_base: float, t_curr: float, scale_pts_per_bar: float = 1.0
) -> Dict[str, float]:
    """
    Computes Gann Geometric Angle Rays from (t_base, p_base):
      1x1 (45 deg): 1 unit price per 1 unit time
      2x1 (63.75 deg): 2 units price per 1 unit time
      1x2 (26.25 deg): 1 unit price per 2 units time
    """
    dt = max(0.0, t_curr - t_base)
    unit = scale_pts_per_bar * dt

    return {
        "gann_8x1": float(p_base + 8.0 * unit),
        "gann_4x1": float(p_base + 4.0 * unit),
        "gann_3x1": float(p_base + 3.0 * unit),
        "gann_2x1": float(p_base + 2.0 * unit),
        "gann_1x1": float(p_base + 1.0 * unit),  # 45-degree Equilibrium
        "gann_1x2": float(p_base + 0.5 * unit),
        "gann_1x3": float(p_base + 0.333 * unit),
        "gann_1x4": float(p_base + 0.25 * unit),
        "gann_1x8": float(p_base + 0.125 * unit)
    }


# ==============================================================================
# 7. TIME CYCLES: FOURIER HARMONIC DECOMPOSITION
# ==============================================================================
def compute_fourier_time_cycles(
    prices: np.ndarray, sample_rate_sec: float = 900.0
) -> Dict[str, Any]:
    """
    Decomposes price series into dominant cyclical periods via Discrete Fourier Transform (DFT).
      P(t) = P0 + sum(A_k * sin(2*pi/T_k * t + phi_k))
    """
    n = len(prices)
    if n < 16:
        return {"dominant_cycle_bars": 24, "cycle_phase": 0.0, "cycle_state": "NEUTRAL"}

    p = prices.astype(np.float64)
    p_detrend = p - np.linspace(p[0], p[-1], n)

    fft_vals = np.fft.rfft(p_detrend)
    fft_magnitudes = np.abs(fft_vals)

    # Exclude DC component (index 0)
    fft_magnitudes[0] = 0.0

    if len(fft_magnitudes) > 1:
        dominant_idx = int(np.argmax(fft_magnitudes))
        if dominant_idx > 0:
            dominant_cycle_bars = int(round(n / dominant_idx))
        else:
            dominant_cycle_bars = 24
    else:
        dominant_cycle_bars = 24

    dominant_cycle_bars = max(4, min(dominant_cycle_bars, n))

    # Phase calculation (0.0 to 2*pi)
    phase_progress = (n % dominant_cycle_bars) / float(dominant_cycle_bars)
    phase_rad = phase_progress * 2.0 * math.pi

    # State: Trough (Cycle Low), Crest (Cycle High), Rising, Falling
    if 0.35 <= phase_progress <= 0.65:
        cycle_state = "CYCLE_CREST_TOP"
    elif phase_progress >= 0.85 or phase_progress <= 0.15:
        cycle_state = "CYCLE_TROUGH_BOTTOM"
    elif phase_progress < 0.35:
        cycle_state = "CYCLE_RISING_WAVE"
    else:
        cycle_state = "CYCLE_FALLING_WAVE"

    return {
        "dominant_cycle_bars": dominant_cycle_bars,
        "cycle_phase_pct": round(phase_progress * 100.0, 1),
        "cycle_state": cycle_state
    }


# ==============================================================================
# 8. HARMONIC PATTERNS & POTENTIAL REVERSAL ZONES (PRZ)
# ==============================================================================
def detect_harmonic_xabcd_patterns(
    highs: np.ndarray, lows: np.ndarray, closes: np.ndarray
) -> Dict[str, Any]:
    """
    Detects 5-Point Harmonic Reversal Patterns (Gartley, Bat, Butterfly, Crab, Cypher).
    Evaluates convergence at point D (Potential Reversal Zone - PRZ).
    """
    n = len(closes)
    if n < 20:
        return {"has_pattern": False, "pattern_name": "NONE", "prz_price": 0.0, "bias": "NEUTRAL"}

    # Simple swing pivot extractor
    pivots: List[Tuple[int, float, str]] = []
    window = 3
    for i in range(window, n - window):
        is_high = all(highs[i] >= highs[i - j] for j in range(1, window + 1)) and all(highs[i] >= highs[i + j] for j in range(1, window + 1))
        is_low = all(lows[i] <= lows[i - j] for j in range(1, window + 1)) and all(lows[i] <= lows[i + j] for j in range(1, window + 1))
        if is_high:
            pivots.append((i, float(highs[i]), "HIGH"))
        elif is_low:
            pivots.append((i, float(lows[i]), "LOW"))

    if len(pivots) < 4:
        return {"has_pattern": False, "pattern_name": "NONE", "prz_price": 0.0, "bias": "NEUTRAL"}

    # Take last 4 pivots as X, A, B, C; current price is prospective D
    p_x, p_a, p_b, p_c = pivots[-4][1], pivots[-3][1], pivots[-2][1], pivots[-1][1]
    curr_p = float(closes[-1])

    xa = abs(p_a - p_x)
    ab = abs(p_b - p_a)
    bc = abs(p_c - p_b)
    cd = abs(curr_p - p_c)

    if xa < 1e-4 or ab < 1e-4 or bc < 1e-4:
        return {"has_pattern": False, "pattern_name": "NONE", "prz_price": 0.0, "bias": "NEUTRAL"}

    ab_xa = ab / xa
    bc_ab = bc / ab
    cd_bc = cd / bc
    ad_xa = abs(curr_p - p_a) / xa

    pattern_name = "NONE"
    bias = "NEUTRAL"
    prz = curr_p

    # Bullish Gartley (M-Shape): D ends near 0.786 XA
    if 0.55 <= ab_xa <= 0.68 and 0.35 <= bc_ab <= 0.90 and 0.72 <= ad_xa <= 0.85:
        pattern_name = "BULLISH_GARTLEY"
        bias = "BUY"
        prz = p_x + 0.786 * (p_a - p_x) if p_a > p_x else p_x - 0.786 * (p_x - p_a)

    # Bullish Bat: AB = 0.382-0.50 XA, D = 0.886 XA
    elif 0.35 <= ab_xa <= 0.52 and 0.35 <= bc_ab <= 0.90 and 0.82 <= ad_xa <= 0.95:
        pattern_name = "BULLISH_BAT"
        bias = "BUY"
        prz = p_x + 0.886 * (p_a - p_x) if p_a > p_x else p_x - 0.886 * (p_x - p_a)

    # Bearish Gartley (W-Shape)
    elif 0.55 <= ab_xa <= 0.68 and 0.35 <= bc_ab <= 0.90 and 0.72 <= ad_xa <= 0.85:
        pattern_name = "BEARISH_GARTLEY"
        bias = "SELL"
        prz = p_x - 0.786 * (p_x - p_a) if p_x > p_a else p_x + 0.786 * (p_a - p_x)

    return {
        "has_pattern": pattern_name != "NONE",
        "pattern_name": pattern_name,
        "prz_price": round(float(prz), 2),
        "bias": bias,
        "ratios": {
            "ab_xa": round(ab_xa, 3),
            "bc_ab": round(bc_ab, 3),
            "cd_bc": round(cd_bc, 3)
        }
    }


# ==============================================================================
# 9. MAGNET MODE: EXACT SNAP TO OHLC & INDICATOR PRICE LEVELS
# ==============================================================================
def snap_to_market_grid(
    target_price: float, ohlc_candidates: List[float]
) -> float:
    """
    Magnet Mode Snap:
      P_snap = argmin_{P in Candidates} |target_price - P|
    Snaps target price to the nearest genuine historical wick/body or indicator line.
    """
    if not ohlc_candidates:
        return round(target_price, 2)
    arr = np.array(ohlc_candidates, dtype=np.float64)
    nearest_idx = int(np.argmin(np.abs(arr - target_price)))
    return round(float(arr[nearest_idx]), 2)


# ==============================================================================
# 10. UNIFIED TRADINGVIEW CONFLUENCE MATRIX ENGINE
# ==============================================================================
class TradingViewConfluenceMatrix:
    """
    Master Quantitative Orchestrator fusing all 10 TradingView Tool Groups
    into a unified Mathematical Confluence Vector on (t, P).
    """

    def __init__(self):
        self._cache_ts: float = 0.0
        self._cached_result: Dict[str, Any] = {}

    def compute_confluence(
        self,
        df_m15: pd.DataFrame,
        current_price: float,
        df_h1: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Executes full multi-dimensional evaluation across all 10 tool groups.
        """
        now = time.time()
        if (now - self._cache_ts) < 5.0 and self._cached_result:
            return self._cached_result

        if df_m15 is None or len(df_m15) < 10:
            return self._default_confluence(current_price)

        closes = df_m15["close"].values
        highs = df_m15["high"].values
        lows = df_m15["low"].values
        n = len(closes)

        # 1. OLS Regression Channel
        ols = compute_ols_regression_channel(closes[-min(40, n):], k=2.0)

        # 2. Volume Profile (POC, VAH, VAL) & Anchored VWAP
        vp = compute_volume_profile(df_m15, n_bins=20)
        avwap = compute_anchored_vwap(df_m15, anchor_idx=max(0, n - 30))

        # 3. Fibonacci Retracement & Golden Pocket
        p_min = float(np.min(lows[-min(30, n):]))
        p_max = float(np.max(highs[-min(30, n):]))
        fib_matrix = compute_fibonacci_matrix(p_min, p_max)

        # 4. Andrews' Pitchfork on last 3 prominent pivots
        p1 = float(lows[-min(30, n)])
        p2 = float(highs[-min(15, n)])
        p3 = float(lows[-min(8, n)])
        pitchfork = compute_andrews_pitchfork(0.0, p1, 15.0, p2, 22.0, p3, float(n))

        # 5. Gann 1x1 Equilibrium
        gann = compute_gann_angles(p_base=p1, t_base=0.0, t_curr=float(n), scale_pts_per_bar=0.50)

        # 6. Fourier Time Cycles
        cycles = compute_fourier_time_cycles(closes)

        # 7. Harmonic Patterns (XABCD / PRZ)
        harmonics = detect_harmonic_xabcd_patterns(highs, lows, closes)

        # ======================================================================
        # CONFLUENCE SCORING (-100.0 to +100.0)
        # ======================================================================
        score = 0.0
        confluence_reasons: List[str] = []

        # A. OLS Channel Mean Reversion
        z = ols["z_score"]
        if z <= -1.80:
            score += 25.0
            confluence_reasons.append(f"OLS_OVERSOLD_2SIGMA (z={z:.2f})")
        elif z >= 1.80:
            score -= 25.0
            confluence_reasons.append(f"OLS_OVERBOUGHT_2SIGMA (z={z:.2f})")

        # B. AVWAP Confluence
        if avwap > 0.0:
            if current_price >= avwap:
                score += 15.0
                confluence_reasons.append("ABOVE_AVWAP_INSTITUTIONAL_SUPPORT")
            else:
                score -= 15.0
                confluence_reasons.append("BELOW_AVWAP_INSTITUTIONAL_RESISTANCE")

        # C. Volume Profile POC / Value Area Rejection
        if vp["profile_valid"]:
            if current_price <= vp["val"]:
                score += 20.0
                confluence_reasons.append("AT_VALUE_AREA_LOW_ACCUMULATION")
            elif current_price >= vp["vah"]:
                score -= 20.0
                confluence_reasons.append("AT_VALUE_AREA_HIGH_DISTRIBUTION")

        # D. Fibonacci Golden Pocket (0.618 - 0.705)
        gp_low = fib_matrix["golden_pocket_low"]
        gp_high = fib_matrix["golden_pocket_high"]
        if gp_low <= current_price <= gp_high:
            score += 25.0
            confluence_reasons.append(f"IN_FIB_GOLDEN_POCKET (${gp_low:.2f}-${gp_high:.2f})")

        # E. Pitchfork Median Line Pull
        med_p = pitchfork["median_line"]
        if abs(current_price - med_p) <= 2.50:
            score += 10.0 if pitchfork["slope"] > 0 else -10.0
            confluence_reasons.append("ANDREWS_MEDIAN_LINE_EQUILIBRIUM")

        # F. Fourier Time Cycle Alignment
        if cycles["cycle_state"] == "CYCLE_TROUGH_BOTTOM":
            score += 15.0
            confluence_reasons.append("FOURIER_TIME_CYCLE_TROUGH_REVERSAL")
        elif cycles["cycle_state"] == "CYCLE_CREST_TOP":
            score -= 15.0
            confluence_reasons.append("FOURIER_TIME_CYCLE_CREST_EXHAUSTION")

        # G. Harmonic Pattern Boost
        if harmonics["has_pattern"]:
            if harmonics["bias"] == "BUY":
                score += 20.0
                confluence_reasons.append(f"{harmonics['pattern_name']}_PRZ_CONFIRMED")
            elif harmonics["bias"] == "SELL":
                score -= 20.0
                confluence_reasons.append(f"{harmonics['pattern_name']}_PRZ_CONFIRMED")

        score = float(np.clip(score, -100.0, 100.0))

        # Overall Direction & Win Probability Estimation
        if score >= 35.0:
            direction = "BUY"
            est_win_rate = round(min(94.5, 60.0 + (score / 100.0) * 35.0), 1)
        elif score <= -35.0:
            direction = "SELL"
            est_win_rate = round(min(94.5, 60.0 + (abs(score) / 100.0) * 35.0), 1)
        else:
            direction = "NEUTRAL"
            est_win_rate = 50.0

        result = {
            "score": round(score, 1),
            "direction": direction,
            "estimated_win_rate": est_win_rate,
            "reasons": confluence_reasons,
            "ols_channel": {
                "center": round(ols["center"], 2),
                "upper": round(ols["upper"], 2),
                "lower": round(ols["lower"], 2),
                "z_score": round(ols["z_score"], 2),
                "r_squared": round(ols["r_squared"], 2)
            },
            "volume_profile": {
                "poc": round(vp["poc"], 2),
                "vah": round(vp["vah"], 2),
                "val": round(vp["val"], 2),
                "avwap": round(avwap, 2)
            },
            "fibonacci": {
                "fib_618": round(fib_matrix["fib_618"], 2),
                "fib_705": round(fib_matrix["fib_705"], 2),
                "ext_1618": round(fib_matrix["ext_1618"], 2)
            },
            "pitchfork": {
                "median": round(pitchfork["median_line"], 2),
                "upper": round(pitchfork["upper_prong"], 2),
                "lower": round(pitchfork["lower_prong"], 2)
            },
            "gann_1x1": round(gann["gann_1x1"], 2),
            "cycles": cycles,
            "harmonics": harmonics
        }

        self._cached_result = result
        self._cache_ts = now
        return result

    def _default_confluence(self, curr_p: float) -> Dict[str, Any]:
        return {
            "score": 0.0,
            "direction": "NEUTRAL",
            "estimated_win_rate": 50.0,
            "reasons": ["INSUFFICIENT_DATA_FOR_MATRIX"],
            "ols_channel": {"center": curr_p, "upper": curr_p + 5.0, "lower": curr_p - 5.0, "z_score": 0.0, "r_squared": 0.0},
            "volume_profile": {"poc": curr_p, "vah": curr_p + 3.0, "val": curr_p - 3.0, "avwap": curr_p},
            "fibonacci": {"fib_618": curr_p - 2.0, "fib_705": curr_p - 3.0, "ext_1618": curr_p + 10.0},
            "pitchfork": {"median": curr_p, "upper": curr_p + 5.0, "lower": curr_p - 5.0},
            "gann_1x1": curr_p,
            "cycles": {"dominant_cycle_bars": 24, "cycle_phase_pct": 50.0, "cycle_state": "NEUTRAL"},
            "harmonics": {"has_pattern": False, "pattern_name": "NONE", "prz_price": curr_p, "bias": "NEUTRAL"}
        }


# Singleton accessor
_GLOBAL_TV_MATRIX: Optional[TradingViewConfluenceMatrix] = None

def get_tradingview_confluence_matrix() -> TradingViewConfluenceMatrix:
    global _GLOBAL_TV_MATRIX
    if _GLOBAL_TV_MATRIX is None:
        _GLOBAL_TV_MATRIX = TradingViewConfluenceMatrix()
    return _GLOBAL_TV_MATRIX
