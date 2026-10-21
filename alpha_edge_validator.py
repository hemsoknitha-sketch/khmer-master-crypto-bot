# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - ALPHA EDGE VALIDATOR & STATISTICAL AUDITOR
=========================================================
Institutional Framework for Verifying Alpha Signal Predictive Power:
1. Information Coefficient (Rank IC / Spearman Correlation)
2. Deflated Sharpe Ratio (Bailey & López de Prado 2014) with Multi-Testing Corrections
3. Continuous Kelly Fraction & Dynamic Expectancy (f(p_hat))
4. Asymmetric Exit Simulation (Right-Tail Harvest with Trailing Stops)
5. Frozen Threshold Ledger for Selection Bias Prevention
6. Certification Sample Size Calculator (required_sample_for_dsr)

Founder: HEM SINATH | Institutional Quantitative Governance
"""

import math
import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr
from typing import Dict, List, Any, Tuple, Optional, Union
from dataclasses import dataclass, field

BPS = 10000.0


@dataclass
class FrozenThresholdLedger:
    """
    Prevents post-hoc threshold selection bias.
    All trades recorded must have timestamp strictly greater than freeze_date_utc.
    """
    threshold: float
    freeze_date_utc: str
    trades: List[Dict] = field(default_factory=list)

    def record(self, trade: Dict) -> None:
        if trade.get("timestamp_utc", "") <= self.freeze_date_utc:
            raise ValueError("Integrity Breach: Trade predates freeze date")
        self.trades.append(trade)

    def realized_r_multiples(self) -> np.ndarray:
        return np.array([t.get("r_multiple", 0.0) for t in self.trades], dtype=float)

    def sample_size(self) -> int:
        return len(self.trades)


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
    payoff_ratio: float,
    kappa: float = 0.25,
    max_risk_pct: float = 0.02
) -> float:
    """
    Continuous sizing function replacing destructive binary filter:
      f(p_hat) = kappa * max(0, (p_hat - p_be) / (1 - p_be))
    Retains 100% of signals with edge while sizing smoothly according to conviction.
    """
    if payoff_ratio <= 0 or p_hat <= 0:
        return 0.0
    pb = p_breakeven(payoff_ratio)
    if p_hat <= pb:
        return 0.0
    edge_fraction = (p_hat - pb) / (1.0 - pb)
    raw = kappa * edge_fraction
    return float(min(raw, max_risk_pct))


def multi_testing_deflated_sharpe(
    returns: np.ndarray,
    num_thresholds_scanned: int = 7,
    num_models_scanned: int = 1,
    num_symbols_scanned: int = 10,
    num_timeframes_scanned: int = 1,
    total_trials: Optional[int] = None
) -> Tuple[float, float]:
    """
    Computes Deflated Sharpe Ratio (DSR) under true search-space trial count.
    Total trials = thresholds * models * symbols * timeframes.
    """
    ret_arr = np.asarray(returns, dtype=float).ravel()
    ret_arr = ret_arr[~(np.isnan(ret_arr) | np.isinf(ret_arr))]
    n = len(ret_arr)
    if n < 30:
        trials = total_trials or (num_thresholds_scanned * num_models_scanned * num_symbols_scanned * num_timeframes_scanned)
        return 0.0, float(trials)

    sr = float(np.mean(ret_arr) / max(np.std(ret_arr, ddof=1), 1e-12))
    centered = (ret_arr - np.mean(ret_arr)) / max(np.std(ret_arr, ddof=1), 1e-12)
    skew = float(np.mean(centered ** 3))
    kurt = float(np.mean(centered ** 4))
    if kurt < 1.0:
        kurt = 3.0

    trials = total_trials if total_trials is not None else max(
        1, num_thresholds_scanned * num_models_scanned * num_symbols_scanned * num_timeframes_scanned
    )

    sr_star = float(np.sqrt(2.0 * np.log(max(2, trials)) / n))
    denom = float(np.sqrt(max(1e-9, 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * (sr ** 2))))
    if denom <= 0:
        return 0.0, float(trials)

    z = (sr - sr_star) * np.sqrt(max(1, n - 1)) / denom
    dsr = float(norm.cdf(z))
    return float(np.clip(dsr, 0.0, 1.0)), float(trials)


def required_sample_for_dsr(
    target_dsr: float = 0.95,
    per_trade_sr: float = 0.26,
    total_trials: int = 700
) -> int:
    """
    Computes minimum out-of-sample sample size N required for DSR >= target_dsr
    under multiple testing penalty of total_trials.
    """
    z_target = float(norm.ppf(target_dsr))
    a = np.sqrt(2.0 * np.log(max(2, total_trials)))
    lo, hi = 30, 100000
    for _ in range(80):
        mid = (lo + hi) // 2
        sr_star = a / np.sqrt(mid)
        z_obs = (per_trade_sr - sr_star) * np.sqrt(mid - 1)
        if z_obs >= z_target:
            hi = mid
        else:
            lo = mid
    return int(hi)


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
    """
    Simulates asymmetric trailing exit with conservative stop-first precedence.
    """
    stop_dist = abs(entry - stop_price)
    if stop_dist <= 1e-9:
        return 0.0, "invalid_stop"

    peak_r = 0.0
    for hi, lo, cl in zip(path_high, path_low, path_close):
        hi_r = (hi - entry) / stop_dist
        lo_r = (lo - entry) / stop_dist

        # Conservative intrabar precedence: check stop loss first
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
    num_trials: int = 100,
    annualization_factor: float = 1.0
) -> float:
    """Computes Deflated Sharpe Ratio."""
    dsr, _ = multi_testing_deflated_sharpe(returns, total_trials=num_trials)
    return dsr


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


def evaluate_signal_dataset(
    predictions: np.ndarray,
    realized_returns: np.ndarray,
    num_trials: int = 700,
    min_confidence_filter: Optional[float] = None
) -> Dict[str, Any]:
    """Runs full quantitative edge audit with multi-testing DSR."""
    p_all = np.asarray(predictions, dtype=float).ravel()
    r_all = np.asarray(realized_returns, dtype=float).ravel()

    if min_confidence_filter is not None:
        mask = p_all >= float(min_confidence_filter)
        p = p_all[mask]
        r = r_all[mask]
    else:
        p = p_all
        r = r_all

    n_samples = len(r)
    if n_samples == 0:
        return {
            "n_samples": 0,
            "rank_ic": 0.0,
            "win_rate_pct": 0.0,
            "avg_win_r": 0.0,
            "avg_loss_r": 0.0,
            "expected_r": 0.0,
            "sharpe_ratio": 0.0,
            "deflated_sharpe_ratio": 0.0,
            "verdict": "NO_EDGE_SIGNAL_DEAD"
        }

    ic = information_coefficient(p, r)
    wins = r[r > 0]
    losses = r[r <= 0]
    wr = float(len(wins) / n_samples)
    avg_w = float(np.mean(wins)) if len(wins) > 0 else 0.0
    avg_l = float(np.abs(np.mean(losses))) if len(losses) > 0 else 1.0
    e_r = expected_r(wr, avg_w, avg_l)

    std_r = float(np.std(r, ddof=1)) if n_samples > 1 else 0.0
    sr = float(np.mean(r) / std_r) if std_r > 1e-9 else 0.0
    dsr, total_t = multi_testing_deflated_sharpe(r, total_trials=num_trials)
    verd = edge_verdict(ic, dsr, e_r)

    return {
        "n_samples": n_samples,
        "rank_ic": round(ic, 4),
        "win_rate_pct": round(wr * 100.0, 2),
        "avg_win_r": round(avg_w, 2),
        "avg_loss_r": round(avg_l, 2),
        "expected_r": round(e_r, 4),
        "sharpe_ratio": round(sr, 4),
        "deflated_sharpe_ratio": round(dsr, 4),
        "total_trials": int(total_t),
        "verdict": verd
    }
