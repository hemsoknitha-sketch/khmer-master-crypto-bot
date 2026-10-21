# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - ALPHA EDGE VALIDATOR & STATISTICAL AUDITOR
=========================================================
Institutional Framework for Verifying Alpha Signal Predictive Power:
1. Information Coefficient (Rank IC / Spearman Correlation)
2. Deflated Sharpe Ratio (Bailey & López de Prado 2014) with Multi-Testing Corrections
3. Continuous Kelly Fraction & Dynamic Expectancy (f(p_hat))
4. Asymmetric Exit Simulation (Right-Tail Harvest with Trailing Stops)
5. Verified Ledger & Strict Freeze Protocol (TradeRecord, VerifiedLedger)
6. Decile Analysis, True Geometric MDD, & Flat 1% Benchmarking
7. Certification Target & Full Verification Suite (full_verification)

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
    Continuous sizing function replacing destructive binary filter:
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


def verified_dsr(returns: np.ndarray, total_trials: int = 700) -> Tuple[float, float, float]:
    """
    Computes Deflated Sharpe Ratio (DSR) under true search-space trial count.
    Returns: (dsr, sample_sr, sr_star)
    """
    ret_arr = np.asarray(returns, dtype=float).ravel()
    ret_arr = ret_arr[~(np.isnan(ret_arr) | np.isinf(ret_arr))]
    n = len(ret_arr)
    if n < 30:
        return 0.0, 0.0, 0.0

    mean_r = float(np.mean(ret_arr))
    std_r = float(np.std(ret_arr, ddof=1))
    if std_r <= 1e-12:
        return 0.0, 0.0, 0.0

    sr = mean_r / std_r
    centered = (ret_arr - mean_r) / std_r
    skew = float(np.mean(centered ** 3))
    kurt = float(np.mean(centered ** 4))
    if kurt < 1.0:
        kurt = 3.0

    trials = max(2, total_trials)
    sr_star = float(np.sqrt(2.0 * np.log(trials) / n))
    denom = float(np.sqrt(max(1e-9, 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * (sr ** 2))))
    if denom <= 0:
        return 0.0, sr, sr_star

    z = (sr - sr_star) * np.sqrt(max(1, n - 1)) / denom
    dsr = float(norm.cdf(z))
    return float(np.clip(dsr, 0.0, 1.0)), sr, sr_star


def multi_testing_deflated_sharpe(
    returns: np.ndarray,
    num_thresholds_scanned: int = 7,
    num_models_scanned: int = 1,
    num_symbols_scanned: int = 10,
    num_timeframes_scanned: int = 1,
    total_trials: Optional[int] = None
) -> Tuple[float, float]:
    """
    Wrapper for multi-testing DSR declaring explicit search space dimensions.
    """
    trials = total_trials if total_trials is not None else max(
        1, num_thresholds_scanned * num_models_scanned * num_symbols_scanned * num_timeframes_scanned
    )
    dsr, sr, _ = verified_dsr(returns, total_trials=trials)
    return dsr, float(trials)


def required_sample_for_dsr(
    target_dsr: float = 0.95,
    per_trade_sr: float = 0.26,
    total_trials: int = 700
) -> int:
    """
    Computes minimum out-of-sample sample size N required for DSR >= target_dsr
    under multiple testing penalty of total_trials.
    """
    if per_trade_sr <= 0:
        return 99999
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


def win_rate_by_decile(
    p_hats: np.ndarray,
    realized_r: np.ndarray,
    n_deciles: int = 10
) -> List[Dict[str, Any]]:
    """
    Validates monotonic calibration of meta-model predictions against trade outcomes.
    """
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
        avg_loss = float(np.mean(subset_r[~wins])) if (~wins).any() else 0.0
        er = wr * avg_win + (1.0 - wr) * avg_loss
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
    """
    Executes 360-degree statistical edge audit on an active ledger.
    """
    returns = ledger.weighted_returns()
    realized = ledger.realized_r()
    p_hats = ledger.p_hats()
    dsr, sr, sr_star = verified_dsr(returns, total_trials)
    n = ledger.size()
    per_trade_sr = sr if sr > 0 else 0.0
    required_n = required_sample_for_dsr(0.95, per_trade_sr, total_trials) if per_trade_sr > 0 else 99999
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
    num_trials: int = 700,
    annualization_factor: float = 1.0
) -> float:
    """Computes Deflated Sharpe Ratio."""
    dsr, _, _ = verified_dsr(returns, total_trials=num_trials)
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
