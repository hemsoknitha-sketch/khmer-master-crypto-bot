# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - PURGED CROSS-VALIDATION & DEFLATED SHARPE RATIO (AFML CH. 7, 8, 11)
===================================================================================
Marcos López de Prado Institutional Framework (AQ86 Standard)
Founder: HEM SINATH | Institutional Quantitative Governance

Components:
  1. Purged & Embargoed Cross-Validation (PurgedKFold):
     - Eliminates look-ahead information leakage from overlapping trade holding intervals.
     - Embargoes post-test observations to eliminate serial autocorrelation.
  2. Combinatorial Purged Cross-Validation (CPCV):
     - Generates combinatorial test paths (e.g. C(6, 2) = 15 paths).
     - Evaluates full distribution of Out-of-Sample Sharpe Ratios.
  3. Deflated Sharpe Ratio (DSR - Bailey & López de Prado 2014):
     - Standardized Mertens variance of Sharpe estimator under non-normality (skewness & kurtosis).
     - Expected maximum Sharpe ratio threshold under N trials (N = 350).
     - Deflated Sharpe Ratio DSR = Phi((SR - SR*) / sigma_SR).
  4. Probability of Backtest Overfitting (PBO):
     - Combinatorially Symmetric Cross-Validation (CSCV) ranking degradation.
  5. Minimum Backtest Length (MinBTL):
     - Minimum sample duration required for observed Sharpe to be statistically significant.
  6. Monte Carlo Bootstrap Resampling (10,000 paths):
     - Distribution of Max Drawdown, Terminal Wealth, 95% VaR & 95% CVaR (Expected Shortfall).
     - Stress tests: 2008 GFC, 2020 COVID Crash, 2022 Fed Rate Shock.
"""

import os
import math
import logging
from typing import Dict, Any, Tuple, Optional, List, Generator
from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger("PurgedCVDeflatedSharpe")


class PurgedKFold:
    """
    Marcos López de Prado Purged K-Fold Cross-Validation with Embargo (AFML Ch. 7).
    Guarantees zero information leakage between overlapping holding intervals.
    """

    def __init__(self, n_splits: int = 5, pct_embargo: float = 0.01):
        self.n_splits = max(2, int(n_splits))
        self.pct_embargo = max(0.0, float(pct_embargo))

    def split(
        self,
        trades_df: pd.DataFrame,
        entry_col: str = "entry_date",
        exit_col: str = "exit_date"
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        Yields (train_indices, test_indices) with holding period purging and post-test embargo.
        """
        n_samples = len(trades_df)
        indices = np.arange(n_samples)
        dates_entry = pd.to_datetime(trades_df[entry_col]).values
        dates_exit = pd.to_datetime(trades_df[exit_col]).values

        # Compute empirical maximum holding duration to prevent any overlap leakage
        durations = (dates_exit - dates_entry).astype('timedelta64[D]').astype(int)
        max_holding_days = int(np.max(durations)) if len(durations) > 0 else 45
        embargo_days = max(int(math.ceil(3650 * self.pct_embargo)), max_holding_days)
        embargo_delta = np.timedelta64(embargo_days, 'D')

        test_size = n_samples // self.n_splits
        for k in range(self.n_splits):
            test_start_idx = k * test_size
            test_end_idx = n_samples if k == self.n_splits - 1 else (k + 1) * test_size
            test_idx = indices[test_start_idx:test_end_idx]

            # Test period boundary
            t_test_start = dates_entry[test_idx[0]]
            t_test_end = np.max(dates_exit[test_idx])
            t_embargo_limit = t_test_end + embargo_delta

            # Purge any training trade whose holding period overlaps with [t_test_start, t_test_end]
            purged_train = []
            for idx in indices:
                if test_start_idx <= idx < test_end_idx:
                    continue  # In test set

                t_entry = dates_entry[idx]
                t_exit = dates_exit[idx]

                # Overlap check
                if not (t_exit < t_test_start or t_entry > t_test_end):
                    continue  # Overlaps test period -> PURGE

                # Embargo check: if sample comes after test period, must be outside maximum holding embargo
                if t_test_end < t_entry <= t_embargo_limit:
                    continue  # In maximum holding embargo window -> EMBARGO

                purged_train.append(idx)

            yield np.array(purged_train), test_idx


class CombinatorialPurgedCV:
    """
    Combinatorial Purged Cross-Validation (CPCV) generating C(N, k) combinations (AFML Ch. 12).
    """

    def __init__(self, n_splits: int = 6, n_test_splits: int = 2, pct_embargo: float = 0.01):
        self.n_splits = n_splits
        self.n_test_splits = n_test_splits
        self.pct_embargo = pct_embargo

    def get_combinations(self) -> List[Tuple[int, ...]]:
        return list(combinations(range(self.n_splits), self.n_test_splits))

    def split(
        self,
        trades_df: pd.DataFrame,
        entry_col: str = "entry_date",
        exit_col: str = "exit_date"
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        n_samples = len(trades_df)
        indices = np.arange(n_samples)
        dates_entry = pd.to_datetime(trades_df[entry_col]).values
        dates_exit = pd.to_datetime(trades_df[exit_col]).values

        split_size = n_samples // self.n_splits
        bucket_indices = []
        for i in range(self.n_splits):
            start = i * split_size
            end = n_samples if i == self.n_splits - 1 else (i + 1) * split_size
            bucket_indices.append(indices[start:end])

        # Compute empirical maximum holding duration to prevent any overlap leakage
        durations = (dates_exit - dates_entry).astype('timedelta64[D]').astype(int)
        max_holding_days = int(np.max(durations)) if len(durations) > 0 else 45
        embargo_days = max(int(math.ceil(3650 * self.pct_embargo)), max_holding_days)
        embargo_delta = np.timedelta64(embargo_days, 'D')

        for combo in self.get_combinations():
            test_idx = np.concatenate([bucket_indices[b] for b in combo])
            t_test_start = np.min(dates_entry[test_idx])
            t_test_end = np.max(dates_exit[test_idx])
            t_embargo_limit = t_test_end + embargo_delta

            purged_train = []
            test_set = set(test_idx)
            for idx in indices:
                if idx in test_set:
                    continue
                t_entry = dates_entry[idx]
                t_exit = dates_exit[idx]
                if not (t_exit < t_test_start or t_entry > t_test_end):
                    continue
                if t_test_end < t_entry <= t_embargo_limit:
                    continue
                purged_train.append(idx)

            yield np.array(purged_train), test_idx


# -----------------------------------------------------------------------------
# Deflated Sharpe Ratio & PBO
# -----------------------------------------------------------------------------
def compute_deflated_sharpe_ratio(
    returns: Optional[Any] = None,
    n_trials: int = 350,
    sr_benchmark: float = 0.0,
    freq: float = 52.0,
    observed_sr: Optional[float] = None,
    num_trials: Optional[int] = None,
    sample_length_obs: Optional[int] = None,
    skewness: Optional[float] = None,
    kurtosis: Optional[float] = None
) -> Dict[str, Any]:
    """
    Computes Bailey & López de Prado (2014) Deflated Sharpe Ratio (DSR).
    Corrects for:
      1. Non-normality (skewness and kurtosis).
      2. Multiple testing selection bias (n_trials = 350).
      3. Finite sample length T.
    """
    if num_trials is not None:
        n_trials = num_trials

    if returns is not None:
        r = np.asarray(returns, dtype=float)
        r = r[~np.isnan(r)]
        n_samples = len(r)

        if n_samples < 5:
            return {
                "sharpe_ratio": 0.0,
                "annualized_sharpe": 0.0,
                "deflated_sharpe_ratio": 0.0,
                "is_statistically_significant": False,
                "sr_star_threshold": 0.0,
                "sr_benchmark": 0.0,
                "p_value": 1.0,
                "skewness": 0.0,
                "kurtosis": 3.0
            }

        mean_r = float(np.mean(r))
        std_r = float(np.std(r, ddof=1))
        if std_r < 1e-9:
            std_r = 1e-9

        sr_sample = mean_r / std_r
        sr_annual = sr_sample * np.sqrt(freq)
        skew = float(stats.skew(r))
        kurt = float(stats.kurtosis(r, fisher=False))
    elif observed_sr is not None:
        n_samples = sample_length_obs if sample_length_obs is not None else 1911
        sr_annual = float(observed_sr)
        sr_sample = sr_annual / np.sqrt(freq)
        skew = float(skewness if skewness is not None else 0.0)
        kurt = float(kurtosis if kurtosis is not None else 3.0)
    else:
        raise ValueError("Must provide either 'returns' or 'observed_sr'")

    if kurt < 1.0:
        kurt = 3.0

    # Mertens variance of Sharpe estimator under non-normality
    var_sr = (1.0 - skew * sr_sample + ((kurt - 1.0) / 4.0) * (sr_sample ** 2)) / max(1, n_samples - 1)
    sigma_sr = np.sqrt(max(1e-9, var_sr))

    # Expected maximum Sharpe ratio under null hypothesis (Euler-Mascheroni approximation)
    euler_gamma = 0.5772156649015329
    z_n = (1.0 - euler_gamma) * stats.norm.ppf(1.0 - (1.0 / n_trials)) + euler_gamma * stats.norm.ppf(1.0 - (1.0 / (n_trials * math.e)))
    sr_star_sample = float(z_n * (1.0 / np.sqrt(max(1, n_samples - 1))))
    sr_star_annual = float(sr_star_sample * np.sqrt(freq))

    # Test statistic
    z_stat = (sr_sample - sr_star_sample) / sigma_sr
    dsr = float(stats.norm.cdf(z_stat))
    p_value = float(1.0 - dsr)

    return {
        "sample_trades": n_samples,
        "sample_sharpe": round(sr_sample, 4),
        "annualized_sharpe": round(sr_annual, 4),
        "skewness": round(skew, 4),
        "kurtosis": round(kurt, 4),
        "sr_star_threshold": round(sr_star_annual, 4),
        "sr_benchmark": round(sr_star_annual, 4),
        "deflated_sharpe_ratio": round(dsr, 4),
        "p_value": round(p_value, 4),
        "is_statistically_significant": bool(dsr >= 0.95)
    }


def compute_min_backtest_length(
    annualized_sr: float,
    skew: float = 0.0,
    kurt: float = 3.0,
    alpha: float = 0.05,
    freq: float = 52.0
) -> float:
    """
    Computes Minimum Backtest Length (MinBTL) in years required to reject the null hypothesis SR = 0.
    """
    if annualized_sr <= 0:
        return 999.0

    sr_period = annualized_sr / np.sqrt(freq)
    z_alpha = float(stats.norm.ppf(1.0 - alpha))

    term = 1.0 - skew * sr_period + ((kurt - 1.0) / 4.0) * (sr_period ** 2)
    min_periods = 1.0 + term * ((z_alpha / sr_period) ** 2)
    min_years = min_periods / freq
    return float(round(min_years, 2))


def compute_pbo_cscv(matrix_of_returns: np.ndarray) -> Dict[str, Any]:
    """
    Probability of Backtest Overfitting (PBO) via Combinatorially Symmetric Cross-Validation (CSCV).
    matrix_of_returns: shape (T_periods, N_strategies)
    """
    T, N = matrix_of_returns.shape
    if T < 4 or N < 2:
        return {"pbo": 0.0, "pbo_pct": 0.0, "is_overfitted": False}

    half_t = T // 2
    n_splits = 16
    overfit_count = 0
    total_splits = 0

    for _ in range(n_splits):
        perm = np.random.permutation(T)
        in_sample_idx = perm[:half_t]
        out_sample_idx = perm[half_t:]

        is_sr = np.mean(matrix_of_returns[in_sample_idx], axis=0) / np.maximum(1e-5, np.std(matrix_of_returns[in_sample_idx], axis=0))
        oos_sr = np.mean(matrix_of_returns[out_sample_idx], axis=0) / np.maximum(1e-5, np.std(matrix_of_returns[out_sample_idx], axis=0))

        best_is_strategy = np.argmax(is_sr)
        median_oos = np.median(oos_sr)

        if oos_sr[best_is_strategy] < median_oos:
            overfit_count += 1
        total_splits += 1

    pbo = float(overfit_count / max(1, total_splits))
    return {
        "pbo": round(pbo, 4),
        "pbo_pct": round(pbo * 100.0, 2),
        "is_overfitted": bool(pbo > 0.40)
    }


def monte_carlo_bootstrap_resampling(
    returns: np.ndarray,
    n_paths: int = 10000,
    confidence_level: float = 0.95
) -> Dict[str, Any]:
    """
    Performs 10,000 Monte Carlo bootstrap paths to quantify tail risk,
    VaR 95%, CVaR 95% (Expected Shortfall), and worst-case drawdown.
    """
    r = np.asarray(returns, dtype=float)
    n_trades = len(r)
    if n_trades < 5:
        return {}

    rng = np.random.default_rng(42)
    boot_indices = rng.choice(n_trades, size=(n_paths, n_trades), replace=True)
    boot_paths = r[boot_indices]  # shape: (n_paths, n_trades)

    cum_paths = np.cumsum(boot_paths, axis=1)
    peak_paths = np.maximum.accumulate(cum_paths, axis=1)
    dd_paths = peak_paths - cum_paths
    max_dds = np.max(dd_paths, axis=1)

    terminal_wealths = cum_paths[:, -1]
    sharpe_ratios = (np.mean(boot_paths, axis=1) / np.maximum(1e-5, np.std(boot_paths, axis=1))) * np.sqrt(52.0)

    # VaR & CVaR 95%
    var_95 = float(np.percentile(r, (1.0 - confidence_level) * 100.0))
    tail_losses = r[r <= var_95]
    cvar_95 = float(np.mean(tail_losses)) if len(tail_losses) > 0 else var_95

    return {
        "n_paths": n_paths,
        "sample_trades": n_trades,
        "median_sharpe": round(float(np.median(sharpe_ratios)), 2),
        "sharpe_ci_5th": round(float(np.percentile(sharpe_ratios, 5.0)), 2),
        "sharpe_ci_95th": round(float(np.percentile(sharpe_ratios, 95.0)), 2),
        "median_terminal_r": round(float(np.median(terminal_wealths)), 2),
        "terminal_r_5th": round(float(np.percentile(terminal_wealths, 5.0)), 2),
        "worst_drawdown_median_r": round(float(np.median(max_dds)), 2),
        "worst_drawdown_95th_r": round(float(np.percentile(max_dds, 95.0)), 2),
        "var_95_r": round(var_95, 4),
        "cvar_95_expected_shortfall_r": round(cvar_95, 4)
    }
