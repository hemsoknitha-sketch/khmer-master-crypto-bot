# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - ALPHA EDGE VALIDATOR & STATISTICAL AUDITOR
=========================================================
Institutional Framework for Verifying Alpha Signal Predictive Power:
1. Information Coefficient (Rank IC / Spearman Correlation)
2. Deflated Sharpe Ratio with Unbiased Moments & Multi-Testing Corrections
3. Continuous Kelly Fraction & Dynamic Expectancy (f(p_hat))
4. Asymmetric Exit Simulation (Right-Tail Harvest with Trailing Stops)
5. Verified Ledger & Strict Freeze Protocol (TradeRecord, VerifiedLedger)
6. Bootstrap MDD Distribution (B=10000 paths) & Scaled Risk Budget Rule
7. Paired Bootstrap Test for Kelly Alpha (95% CI)
8. Multi-Regime Attribution & Institutional Deployment Decision Governor

Founder: HEM SINATH | Institutional Quantitative Governance
"""

import math
import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr, skew, kurtosis
from typing import Dict, List, Any, Tuple, Optional, Union
from dataclasses import dataclass, field

BPS = 10000.0
BOOTSTRAP_B = 10000


@dataclass
class TradeRecord:
    timestamp_utc: str
    symbol: str
    p_hat: float
    realized_r: float
    allocation_pct: float
    exit_reason: str


@dataclass
class VerifiedLedger:
    """
    Prevents post-hoc threshold selection bias and enforces risk limits.
    All trades recorded must have timestamp strictly greater than freeze_date_utc.
    """
    freeze_date_utc: str
    kappa: float = 0.25
    max_risk_pct: float = 0.02
    threshold_p_hat: float = 0.50
    trades: List[TradeRecord] = field(default_factory=list)

    def record(self, trade: TradeRecord) -> None:
        if trade.timestamp_utc <= self.freeze_date_utc:
            raise ValueError("Integrity Breach: Trade predates freeze date")
        if trade.allocation_pct > self.max_risk_pct + 1e-12:
            raise ValueError(f"Risk Cap Breach: allocation {trade.allocation_pct:.4f} exceeds max_risk_pct {self.max_risk_pct:.4f}")
        self.trades.append(trade)

    def weighted_returns(self) -> np.ndarray:
        return np.array([t.realized_r * t.allocation_pct for t in self.trades], dtype=float)

    def realized_r(self) -> np.ndarray:
        return np.array([t.realized_r for t in self.trades], dtype=float)

    def p_hats(self) -> np.ndarray:
        return np.array([t.p_hat for t in self.trades], dtype=float)

    def size(self) -> int:
        return len(self.trades)


# Backward compatibility alias
FrozenThresholdLedger = VerifiedLedger


def p_breakeven(payoff_ratio: float) -> float:
    """Computes breakeven win rate: p_be = 1.0 / (1.0 + payoff_ratio)."""
    if payoff_ratio <= 0:
        return 1.0
    return float(1.0 / (1.0 + payoff_ratio))


def break_even_payoff_at_win_rate(win_rate: float) -> float:
    """Computes required payoff ratio b for a given win rate: b = (1 - wr) / wr."""
    if win_rate <= 0 or win_rate >= 1.0:
        return float("inf")
    return float((1.0 - win_rate) / win_rate)


def continuous_kelly_fraction(
    p_hat: float,
    payoff_ratio: float = 2.01,
    kappa: float = 0.25,
    max_risk_pct: float = 0.02,
    p_cut: Optional[float] = None
) -> float:
    """
    Continuous sizing function:
      f(p_hat) = kappa * max(0, (p_hat - p_base) / (1 - p_base))
    where p_base is max(p_breakeven, p_cut).
    Clamped strictly to max_risk_pct.
    """
    if payoff_ratio <= 0 or p_hat <= 0:
        return 0.0
    pb = p_breakeven(payoff_ratio)
    p_base = max(pb, p_cut) if p_cut is not None else pb
    if p_hat <= p_base:
        return 0.0
    edge_fraction = (p_hat - p_base) / (1.0 - p_base)
    raw = kappa * edge_fraction
    return float(min(raw, max_risk_pct))


def dsr_with_moments(returns: np.ndarray, total_trials: int = 700) -> Dict[str, float]:
    """
    Computes Deflated Sharpe Ratio (DSR) using unbiased sample moments (skewness and kurtosis).
    """
    ret_arr = np.asarray(returns, dtype=float).ravel()
    ret_arr = ret_arr[~(np.isnan(ret_arr) | np.isinf(ret_arr))]
    n = len(ret_arr)
    if n < 30:
        return {"dsr": 0.0, "sr": 0.0, "sr_star": 0.0, "skew": 0.0, "kurt": 0.0, "denom": 1.0}

    mean_r = float(np.mean(ret_arr))
    std_r = float(np.std(ret_arr, ddof=1))
    if std_r <= 1e-12:
        return {"dsr": 0.0, "sr": 0.0, "sr_star": 0.0, "skew": 0.0, "kurt": 0.0, "denom": 1.0}

    sr = mean_r / std_r
    sk = float(skew(ret_arr, bias=False))
    ku = float(kurtosis(ret_arr, fisher=False, bias=False))
    if ku < 1.0:
        ku = 3.0

    trials = max(2, total_trials)
    # Conservative DSR Variant: sr_star = sqrt(2*ln(trials)/n) without scaling by denom.
    # Note: When denom < 1.0 (as with negative skew/fat tails, denom=0.8550), unscaled sr_star
    # produces a strictly higher threshold hurdle (~1.17x stricter) than Standard Bailey-Lopez de Prado
    # where sr_star = denom * sqrt(2*ln(trials)/(n-1)).
    sr_star = float(np.sqrt(2.0 * np.log(trials) / n))
    denom = float(np.sqrt(max(1e-9, 1.0 - sk * sr + ((ku - 1.0) / 4.0) * (sr ** 2))))
    if denom <= 0:
        return {"dsr": 0.0, "sr": sr, "sr_star": sr_star, "skew": sk, "kurt": ku, "denom": 1.0}

    z = (sr - sr_star) * np.sqrt(max(1, n - 1)) / denom
    dsr = float(norm.cdf(z))
    return {
        "dsr": float(np.clip(dsr, 0.0, 1.0)),
        "sr": sr,
        "sr_star": sr_star,
        "skew": sk,
        "kurt": ku,
        "denom": denom,
    }


def verified_dsr(returns: np.ndarray, total_trials: int = 700) -> Tuple[float, float, float]:
    """Computes Deflated Sharpe Ratio (DSR) under true search-space trial count."""
    info = dsr_with_moments(returns, total_trials=total_trials)
    return info["dsr"], info["sr"], info["sr_star"]


def multi_testing_deflated_sharpe(
    returns: np.ndarray,
    num_thresholds_scanned: int = 7,
    num_models_scanned: int = 1,
    num_symbols_scanned: int = 10,
    num_timeframes_scanned: int = 1,
    total_trials: Optional[int] = None
) -> Tuple[float, float]:
    """Wrapper for multi-testing DSR declaring explicit search space dimensions."""
    trials = total_trials if total_trials is not None else max(
        1, num_thresholds_scanned * num_models_scanned * num_symbols_scanned * num_timeframes_scanned
    )
    info = dsr_with_moments(returns, total_trials=trials)
    return info["dsr"], float(trials)


def required_sample_for_dsr(
    target_dsr: float = 0.95,
    per_trade_sr: float = 0.26,
    total_trials: int = 700,
    denom: float = 1.0,
    skewness: Optional[float] = None,
    kurt: Optional[float] = None,
    denom_mode: str = "recomputed_at_sr",
    conservative_variant: bool = True,
    rounding_mode: str = "ceil_buffer"
) -> int:
    """
    Computes minimum sample size N required for DSR >= target_dsr.
    Incorporates variance denominator factor denom = sqrt(1 - skew*SR + (kurt-1)/4 * SR^2).

    Note: denom(SR) is an Asymptotic Taylor Approximation (Bailey & Lopez de Prado 2014)
    derived under large-sample assumptions and finite 4th moments. For empirical crypto
    distributions with fat tails and serial dependence, N_req is a calibrated fiduciary
    estimate rather than an exact distribution-free invariant.

    denom_mode:
      - "recomputed_at_sr": Recomputes denom dynamically at per_trade_sr using skewness and kurt.
                            This is epistemologically rigorous when testing counterfactual lower-SR bounds.
      - "point_estimate": Keeps the input denom constant regardless of per_trade_sr.

    conservative_variant:
      - True (default): sr_star = sqrt(2*ln(trials)/N), producing a stricter fiduciary buffer
                        (~1.25x larger N when denom < 1.0).
      - False (Standard Bailey-Lopez de Prado 2014): sr_star is scaled by denom.

    rounding_mode:
      - "ceil_buffer" (default): Adds +1 fiduciary safety buffer to the crossing root (e.g., 543 -> 544,
                                710 -> 711) ensuring strict over-compliance under discrete trade arrivals.
      - "exact_root": Returns the exact minimum integer N where the condition holds (e.g., 543, 710).
    """
    if per_trade_sr <= 0:
        return 99999
    z_target = float(norm.ppf(target_dsr))
    a = np.sqrt(2.0 * np.log(max(2, total_trials)))

    if denom_mode == "recomputed_at_sr" and skewness is not None and kurt is not None:
        sk = float(skewness)
        ku = float(kurt)
        d = float(np.sqrt(max(1e-9, 1.0 - sk * per_trade_sr + ((ku - 1.0) / 4.0) * (per_trade_sr ** 2))))
    else:
        d = max(1e-9, float(denom))

    lo, hi = 30, 100000
    for _ in range(80):
        mid = (lo + hi) // 2
        if conservative_variant:
            sr_star = a / np.sqrt(mid)
            z_obs = (per_trade_sr - sr_star) * np.sqrt(mid - 1) / d
        else:
            z_obs = (per_trade_sr * np.sqrt(mid - 1) / d) - a
        if z_obs >= z_target:
            hi = mid
        else:
            lo = mid
    return int(hi + 1) if rounding_mode == "ceil_buffer" else int(hi)


def bootstrap_mdd(
    realized_r: np.ndarray,
    target_n: int,
    allocation_pct: float,
    block_length: int = 5,
    B: int = BOOTSTRAP_B,
    seed: int = 42
) -> Dict[str, float]:
    """
    Resamples trade sequences with replacement B=10,000 times to construct
    the distribution of expected maximum drawdown over target_n trades.
    Uses Circular Block Bootstrap (Politis & Romano) when block_length > 1
    to preserve autocorrelation and volatility clustering, avoiding optimistic tail bias.
    """
    rng = np.random.default_rng(seed)
    r_arr = np.asarray(realized_r, dtype=float).ravel()
    r_clean = r_arr[~(np.isnan(r_arr) | np.isinf(r_arr))]
    n_src = len(r_clean)
    if n_src == 0 or target_n <= 0:
        return {"mdd_mean": 0.0, "mdd_median": 0.0, "mdd_95": 0.0, "mdd_99": 0.0}

    blk = max(1, int(block_length))
    n_blocks = int(np.ceil(target_n / blk))
    mdds = np.empty(B, dtype=float)

    for b_idx in range(B):
        if blk == 1:
            idx = rng.integers(0, n_src, size=target_n)
            sample = r_clean[idx]
        else:
            starts = rng.integers(0, n_src, size=n_blocks)
            sample_list = []
            for s in starts:
                for k in range(blk):
                    sample_list.append(r_clean[(s + k) % n_src])
            sample = np.array(sample_list[:target_n], dtype=float)

        equity = np.cumprod(1.0 + sample * allocation_pct)
        peak = np.maximum.accumulate(equity)
        dd = (equity - peak) / peak
        mdds[b_idx] = float(np.min(dd))

    return {
        "mdd_mean": float(np.mean(mdds)) * 100.0,
        "mdd_median": float(np.median(mdds)) * 100.0,
        "mdd_95": float(np.percentile(mdds, 5)) * 100.0,
        "mdd_99": float(np.percentile(mdds, 1)) * 100.0,
        "block_length": blk,
    }


def scaled_risk_budget(
    mdd_pct: float,
    hard_cap_pct: float = 15.0,
    max_risk_pct: float = 2.0,
    validation_stress_multiplier: float = 1.0
) -> float:
    """
    Dynamically clamps position risk so that expected drawdown over target_n trades
    does not exceed hard_cap_pct (15.0%). Supports validation stress multiplier
    to account for regime differences between validation and holdout periods.
    """
    mdd_abs = abs(mdd_pct) * max(1.0, float(validation_stress_multiplier))
    if mdd_abs <= 0:
        return max_risk_pct
    scaled = (hard_cap_pct / mdd_abs) * max_risk_pct
    return float(min(max_risk_pct, scaled))


def paired_kelly_alpha_test(
    realized_r: np.ndarray,
    p_hats: np.ndarray,
    kappa: float = 0.25,
    p_breakeven: float = 0.50,
    max_risk_pct: float = 0.02,
    flat_pct: float = 0.01,
    B: int = BOOTSTRAP_B,
    seed: int = 42
) -> Dict[str, float]:
    """
    Performs Paired Bootstrap hypothesis test comparing Kelly allocation vs Flat 1% sizing.
    Computes 95% Confidence Interval [alpha_ci_low, alpha_ci_high].
    """
    rng = np.random.default_rng(seed)
    r_arr = np.asarray(realized_r, dtype=float).ravel()
    p_arr = np.asarray(p_hats, dtype=float).ravel()
    n = len(r_arr)
    if n < 10:
        return {
            "alpha_point_pct": 0.0,
            "alpha_ci_low_pct": 0.0,
            "alpha_ci_high_pct": 0.0,
            "kelly_total_pct": 0.0,
            "flat_total_pct": 0.0,
            "p_positive_alpha": 0.0,
        }

    kelly_alloc = np.zeros(n, dtype=float)
    for i in range(n):
        p = float(p_arr[i])
        if p <= p_breakeven:
            kelly_alloc[i] = 0.0
        else:
            raw = kappa * (p - p_breakeven) / (1.0 - p_breakeven)
            kelly_alloc[i] = min(raw, max_risk_pct)

    kelly_returns = r_arr * kelly_alloc
    flat_returns = r_arr * flat_pct
    kelly_total = float(np.prod(1.0 + kelly_returns) - 1.0)
    flat_total = float(np.prod(1.0 + flat_returns) - 1.0)

    diffs = np.empty(B, dtype=float)
    for b_idx in range(B):
        idx = rng.integers(0, n, size=n)
        k = float(np.prod(1.0 + kelly_returns[idx]) - 1.0)
        f = float(np.prod(1.0 + flat_returns[idx]) - 1.0)
        diffs[b_idx] = k - f

    return {
        "alpha_point_pct": round((kelly_total - flat_total) * 100.0, 2),
        "alpha_ci_low_pct": round(float(np.percentile(diffs, 2.5)) * 100.0, 2),
        "alpha_ci_high_pct": round(float(np.percentile(diffs, 97.5)) * 100.0, 2),
        "kelly_total_pct": round(kelly_total * 100.0, 2),
        "flat_total_pct": round(flat_total * 100.0, 2),
        "p_positive_alpha": round(float(np.mean(diffs > 0)) * 100.0, 2),
    }


def regime_attribution(realized_r: np.ndarray, regimes: np.ndarray) -> List[Dict[str, Any]]:
    """Segment trade expectancy and outcomes across market regimes."""
    r_arr = np.asarray(realized_r, dtype=float).ravel()
    reg_arr = np.asarray(regimes).ravel()
    out = []
    for r in sorted(set(reg_arr.tolist())):
        mask = reg_arr == r
        subset = r_arr[mask]
        if len(subset) == 0:
            continue
        wins = subset > 0
        wr = float(np.mean(wins))
        avg_win = float(np.mean(subset[wins])) if wins.any() else 0.0
        avg_loss = float(np.abs(np.mean(subset[~wins]))) if (~wins).any() else 0.0
        er = wr * avg_win - (1.0 - wr) * avg_loss
        out.append({
            "regime": str(r),
            "n": int(len(subset)),
            "win_rate_pct": round(wr * 100.0, 2),
            "avg_win_r": round(avg_win, 2),
            "avg_loss_r": round(avg_loss, 2),
            "expected_r": round(er, 4),
        })
    return out


def deploy_decision(
    holdout_returns: np.ndarray,
    holdout_realized_r: np.ndarray,
    holdout_p_hats: np.ndarray,
    regimes: Optional[np.ndarray] = None,
    total_trials: int = 700,
    target_n: int = 350,
    block_length: int = 5,
    percentile_anchor: str = "mdd_95",
    validation_stress_multiplier: float = 1.0
) -> Dict[str, Any]:
    """
    Master Institutional Fiduciary Deployment Decision Governor.
    Certifies whether strategy can scale beyond 0.1% capital.
    Enforces strict input shape invariance and robust block-resampled drawdown metrics.
    """
    # Strict Input Shape Invariance Validation
    n_ret = len(holdout_returns)
    n_real = len(holdout_realized_r)
    n_p = len(holdout_p_hats)
    if not (n_ret == n_real == n_p and n_real > 0):
        raise ValueError(
            f"Shape Invariant Violation in deploy_decision: holdout_returns({n_ret}), "
            f"holdout_realized_r({n_real}), holdout_p_hats({n_p}) must have identical positive lengths."
        )
    if regimes is not None and len(regimes) != n_real:
        raise ValueError(
            f"Shape Invariant Violation in deploy_decision: regimes length ({len(regimes)}) "
            f"does not match realized_r length ({n_real})."
        )

    dsr_info = dsr_with_moments(holdout_returns, total_trials)
    mdd_info = bootstrap_mdd(holdout_realized_r, target_n, allocation_pct=0.01, block_length=block_length)
    
    anchor_metric = mdd_info["mdd_99"] if percentile_anchor == "mdd_99" else mdd_info["mdd_95"]
    risk_budget = scaled_risk_budget(
        anchor_metric,
        hard_cap_pct=15.0,
        max_risk_pct=2.0,
        validation_stress_multiplier=validation_stress_multiplier
    )
    alpha_info = paired_kelly_alpha_test(
        holdout_realized_r, holdout_p_hats,
        kappa=0.25, p_breakeven=0.50,
        max_risk_pct=0.02, flat_pct=0.01,
    )
    reg_attr = regime_attribution(holdout_realized_r, regimes) if regimes is not None else []

    is_certified = bool(
        dsr_info["dsr"] >= 0.95 and
        risk_budget > 0.0 and
        alpha_info["alpha_ci_low_pct"] > 0.0
    )

    return {
        "dsr": dsr_info,
        "bootstrap_mdd": mdd_info,
        "percentile_anchor": percentile_anchor,
        "scaled_risk_budget_pct": round(risk_budget, 4),
        "kelly_alpha": alpha_info,
        "regime_attribution": reg_attr,
        "certified": is_certified,
    }


def win_rate_by_decile(
    p_hats: np.ndarray,
    realized_r: np.ndarray,
    n_deciles: int = 10
) -> List[Dict[str, Any]]:
    """Validates monotonic calibration of meta-model predictions against trade outcomes."""
    if len(p_hats) < n_deciles * 5:
        return []
    order = np.argsort(p_hats)
    sorted_p = p_hats[order]
    sorted_r = realized_r[order]
    deciles = []
    chunk = len(sorted_p) // n_deciles
    for i in range(n_deciles):
        lo = i * chunk
        hi = (i + 1) * chunk if i < n_deciles - 1 else len(sorted_p)
        subset_p = sorted_p[lo:hi]
        subset_r = sorted_r[lo:hi]
        wins = subset_r > 0
        if len(subset_r) == 0:
            continue
        wr = float(np.mean(wins))
        avg_win = float(np.mean(subset_r[wins])) if wins.any() else 0.0
        avg_loss = float(np.abs(np.mean(subset_r[~wins]))) if (~wins).any() else 0.0
        er = wr * avg_win - (1.0 - wr) * avg_loss
        deciles.append({
            "decile": i + 1,
            "n": int(len(subset_r)),
            "p_hat_min": float(np.min(subset_p)),
            "p_hat_max": float(np.max(subset_p)),
            "p_hat_mean": float(np.mean(subset_p)),
            "win_rate_pct": round(wr * 100.0, 2),
            "avg_win_r": round(avg_win, 2),
            "avg_loss_r": round(avg_loss, 2),
            "expected_r": round(er, 4),
        })
    return deciles


def max_drawdown(returns: np.ndarray, allocation_pct: float) -> float:
    """Computes true geometric maximum peak-to-trough drawdown."""
    if len(returns) == 0:
        return 0.0
    equity = np.cumprod(1.0 + returns * allocation_pct)
    peak = np.maximum.accumulate(equity)
    dd = (equity - peak) / peak
    return float(np.min(dd))


def flat_sizing_benchmark(
    realized_r: np.ndarray,
    allocation_pct: float = 0.01
) -> Dict[str, Any]:
    """Computes reference performance under fixed uncalibrated 1% sizing."""
    if len(realized_r) == 0:
        return {"total_return_pct": 0.0, "max_dd_pct": 0.0}
    equity = np.cumprod(1.0 + realized_r * allocation_pct)
    total_ret = float(equity[-1] - 1.0) * 100.0
    peak = np.maximum.accumulate(equity)
    dd = float(np.min((equity - peak) / peak)) * 100.0
    return {"total_return_pct": round(total_ret, 2), "max_dd_pct": round(dd, 2)}


def full_verification(ledger: VerifiedLedger, total_trials: int = 700) -> Dict[str, Any]:
    """Executes 360-degree statistical edge audit on an active ledger."""
    returns = ledger.weighted_returns()
    realized = ledger.realized_r()
    p_hats = ledger.p_hats()
    dsr_info = dsr_with_moments(returns, total_trials)
    dsr = dsr_info["dsr"]
    sr = dsr_info["sr"]
    sr_star = dsr_info["sr_star"]
    denom = dsr_info.get("denom", 1.0)
    skew_val = dsr_info.get("skew", 0.0)
    kurt_val = dsr_info.get("kurt", 3.0)
    n = ledger.size()
    per_trade_sr = sr if sr > 0 else 0.0
    required_n = required_sample_for_dsr(
        0.95, per_trade_sr, total_trials, denom=denom, skewness=skew_val, kurt=kurt_val, denom_mode="recomputed_at_sr"
    ) if per_trade_sr > 0 else 99999
    deciles = win_rate_by_decile(p_hats, realized)

    mean_alloc = float(np.mean([t.allocation_pct for t in ledger.trades])) if ledger.trades else 0.01
    mdd = max_drawdown(realized, mean_alloc)
    flat = flat_sizing_benchmark(realized, 0.01)

    return {
        "n_trades": n,
        "dsr": round(dsr, 4),
        "per_trade_sr": round(per_trade_sr, 4),
        "sr_star": round(sr_star, 4),
        "required_n_for_dsr_095": int(required_n),
        "certified": bool(dsr >= 0.95 and n >= required_n),
        "max_drawdown_pct": round(mdd * 100.0, 2),
        "flat_1pct_benchmark": flat,
        "decile_analysis": deciles,
    }


@dataclass
class AsymmetricExitConfig:
    """
    Asymmetric exit configuration shifting payoff ratio upward:
    Fixed stop-loss + trailing take-profit harvesting right tail of returns.
    """
    stop_r: float = 0.95
    trailing_activation_r: float = 0.80
    trailing_distance_r: float = 0.40
    hard_take_r: float = 6.0


def simulate_asymmetric_exit(
    path_high: np.ndarray,
    path_low: np.ndarray,
    path_close: np.ndarray,
    entry: float,
    stop_price: float,
    cfg: AsymmetricExitConfig
) -> Tuple[float, str]:
    """Simulates asymmetric trailing exit with conservative stop-first precedence."""
    stop_dist = abs(entry - stop_price)
    if stop_dist <= 1e-9:
        return 0.0, "invalid_stop"

    peak_r = 0.0
    for hi, lo, cl in zip(path_high, path_low, path_close):
        hi_r = (hi - entry) / stop_dist
        lo_r = (lo - entry) / stop_dist

        if lo_r <= -cfg.stop_r:
            return -cfg.stop_r, "stop"

        if hi_r > peak_r:
            peak_r = hi_r

        if peak_r >= cfg.trailing_activation_r:
            trail_stop_r = peak_r - cfg.trailing_distance_r
            if lo_r <= trail_stop_r:
                return float(trail_stop_r), "trailing"

        if hi_r >= cfg.hard_take_r:
            return float(cfg.hard_take_r), "hard_take"

    return float((path_close[-1] - entry) / stop_dist), "close"


def information_coefficient(predicted: np.ndarray, realized: np.ndarray) -> float:
    """Computes Spearman Rank Information Coefficient (Rank IC)."""
    pred_arr = np.asarray(predicted, dtype=float).ravel()
    real_arr = np.asarray(realized, dtype=float).ravel()
    mask = ~(np.isnan(pred_arr) | np.isnan(real_arr) | np.isinf(pred_arr) | np.isinf(real_arr))
    p_clean = pred_arr[mask]
    r_clean = real_arr[mask]

    if len(p_clean) < 30 or np.all(p_clean == p_clean[0]) or np.all(r_clean == r_clean[0]):
        return 0.0

    pred_rank = np.argsort(np.argsort(p_clean))
    real_rank = np.argsort(np.argsort(r_clean))
    corr = np.corrcoef(pred_rank, real_rank)[0, 1]
    return float(corr) if not np.isnan(corr) else 0.0


def deflated_sharpe_ratio(
    returns: np.ndarray,
    num_trials: int = 700,
    annualization_factor: float = 1.0
) -> float:
    """Computes Deflated Sharpe Ratio."""
    info = dsr_with_moments(returns, total_trials=num_trials)
    return info["dsr"]


def expected_r(win_rate: float, avg_win_r: float, avg_loss_r: float) -> float:
    """E[R] = P(Win) * AvgWin_R - (1 - P(Win)) * AvgLoss_R."""
    wr = float(np.clip(win_rate, 0.0, 1.0))
    aw = max(0.0, float(avg_win_r))
    al = max(0.0, float(avg_loss_r))
    return float(wr * aw - (1.0 - wr) * al)


def edge_verdict(ic: float, dsr: float, expected_r_value: float) -> str:
    """Evaluates quantitative alpha validity."""
    if ic < 0.03:
        return "NO_EDGE_SIGNAL_DEAD"
    if expected_r_value <= 0:
        return "NEGATIVE_EXPECTANCY"
    if dsr < 0.95:
        return "NOT_STATISTICALLY_SIGNIFICANT"
    return "EDGE_CONFIRMED"
