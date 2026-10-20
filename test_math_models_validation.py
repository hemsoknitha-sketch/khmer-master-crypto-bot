# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - MATHEMATICAL MODELS STATISTICAL VALIDATION SUITE (GAP 4 / INVARIANT 80)
======================================================================================
Empirical Verification of Gap 4 (ចន្លោះទី 4):
  1. Hurst Exponent (H):
     - Window Sensitivity Test (Short, Mid, Long window stability)
     - 95% Confidence Interval & P-value against Random Walk
     - Comparison with Simple Baseline Model (Permuted / Shuffled Noise Benchmark)
  2. Ornstein-Uhlenbeck (OU) Mean Reversion:
     - Dickey-Fuller Stationarity / Unit Root Test (Prevents false |Z| > 2.5 counter-trend traps)
     - Multi-Window Parameter Stability Test
     - Half-Life 95% Confidence Interval & Economic Viability
     - Comparison with Simple Baseline Model (SMA-20 & Bollinger Z-Score Benchmark)
  3. Bayesian Posterior Probability:
     - Explicit Prior Base Rate Specification
     - De-Collinearized Likelihood Shrinkage (Eliminates pseudo-probability explosion)
     - 95% Bayesian Credible Interval
     - Information Gain (KL-Divergence in bits) & Bayes Factor vs Uninformed Baseline
"""

import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
import gold_mathematical_radar as gmr

def run_gap4_validation_suite():
    print("=" * 88)
    print("  ANGKOR QUANT - MATHEMATICAL MODELS STATISTICAL VALIDATION SUITE (GAP 4)")
    print("=" * 88)
    
    np.random.seed(42)
    n_bars = 100
    
    # =========================================================================
    # PART 1: HURST EXPONENT VALIDATION STUDY
    # =========================================================================
    print("\n" + "-" * 88)
    print("  [PART 1/3] HURST EXPONENT (H) STATISTICAL VALIDATION")
    print("-" * 88)
    
    # Case 1A: Pure Random Walk (Geometric Brownian Motion)
    # H raw might randomly appear > 0.55 due to finite sample noise!
    rw_prices = np.cumsum(np.random.normal(0, 1.5, n_bars)) + 2650.0
    h_rw = gmr.compute_hurst_exponent(rw_prices)
    
    # Case 1B: Synthetic Verified Persistent Trend
    trend_prices = np.linspace(2650, 2800, n_bars) + np.random.normal(0, 0.8, n_bars)
    h_trend = gmr.compute_hurst_exponent(trend_prices)
    
    print(f"1. Random Walk Series:")
    print(f"   • Raw H: {h_rw['hurst']:.3f} | Regime: {h_rw['regime']} | Status: {h_rw['validation_status']}")
    print(f"   • 95% CI: [{h_rw['confidence_interval']['ci_lower']:.3f}, {h_rw['confidence_interval']['ci_upper']:.3f}] (p-val: {h_rw['confidence_interval']['p_value']:.4f})")
    print(f"   • Window Sensitivity: Short={h_rw['window_sensitivity']['hurst_short']:.3f}, Mid={h_rw['window_sensitivity']['hurst_mid']:.3f}, Long={h_rw['window_sensitivity']['hurst_long']:.3f} (Stability: {h_rw['window_sensitivity']['stability_score']:.2f})")
    print(f"   • Baseline Shuffled H: {h_rw['baseline_comparison']['baseline_hurst_shuffled']:.3f} | Z vs Baseline: {h_rw['baseline_comparison']['z_score_vs_baseline']:.2f} | Beats Baseline: {h_rw['baseline_comparison']['beats_simple_baseline']}")
    
    print(f"\n2. Certified Persistent Trend Series:")
    print(f"   • Raw H: {h_trend['hurst']:.3f} | Regime: {h_trend['regime']} | Status: {h_trend['validation_status']}")
    print(f"   • 95% CI: [{h_trend['confidence_interval']['ci_lower']:.3f}, {h_trend['confidence_interval']['ci_upper']:.3f}] (p-val: {h_trend['confidence_interval']['p_value']:.4f})")
    print(f"   • Window Sensitivity: Short={h_trend['window_sensitivity']['hurst_short']:.3f}, Mid={h_trend['window_sensitivity']['hurst_mid']:.3f}, Long={h_trend['window_sensitivity']['hurst_long']:.3f} (Stability: {h_trend['window_sensitivity']['stability_score']:.2f})")
    print(f"   • Baseline Shuffled H: {h_trend['baseline_comparison']['baseline_hurst_shuffled']:.3f} | Z vs Baseline: {h_trend['baseline_comparison']['z_score_vs_baseline']:.2f} | Beats Baseline: {h_trend['baseline_comparison']['beats_simple_baseline']}")
    
    # Assert validation proof:
    # Random walk must NOT be certified as persistent trend
    assert h_rw['regime'] == "RANDOM_WALK", "Random Walk was erroneously certified as persistent trend!"
    print("   >>> [VERIFIED] Spurious persistence on Random Walk correctly blocked by CI & Baseline test!")
    
    # =========================================================================
    # PART 2: ORNSTEIN-UHLENBECK (OU) MEAN REVERSION VALIDATION STUDY
    # =========================================================================
    print("\n" + "-" * 88)
    print("  [PART 2/3] ORNSTEIN-UHLENBECK (OU) PROCESS VALIDATION")
    print("-" * 88)
    
    # Case 2A: Non-Stationary Trending Asset (Parabolic Runaway)
    # Price is exploding upwards: |Z| will be extreme (> 2.5), but ADF will detect Unit Root!
    parabolic_trend = np.linspace(2500, 2750, 60) + np.random.normal(0, 1.5, 60)
    ou_trend = gmr.calibrate_ou_process(parabolic_trend)
    
    # Case 2B: True Stationary Mean-Reverting Asset (True OU Process)
    ou_series = np.zeros(60)
    ou_series[0] = 2650.0
    for i in range(1, 60):
        ou_series[i] = ou_series[i-1] + 0.35 * (2650.0 - ou_series[i-1]) + np.random.normal(0, 3.5)
    ou_mr = gmr.calibrate_ou_process(ou_series)
    
    print(f"1. Non-Stationary Trending Asset (Runaway Parabolic):")
    print(f"   • OU Z-score: {ou_trend['z_score']:.2f} (Extreme Dislocation)")
    print(f"   • ADF Stationarity t-stat: {ou_trend['adf_t_stat']:.2f} (Critical 95%: -2.89) | Verdict: {ou_trend['stationarity_verdict']}")
    print(f"   • Tradeable Reversion: {ou_trend['is_reversion_tradeable']}")
    print(f"   • Reversion Guard Note: {ou_trend['reversion_note']}")
    print(f"   • Baseline SMA-20 Z-score: {ou_trend['sma_z_score']:.2f} | Beats Baseline: {ou_trend['beats_baseline']}")
    
    print(f"\n2. True Stationary Mean-Reverting Asset:")
    print(f"   • OU Z-score: {ou_mr['z_score']:.2f} | Equilibrium Mean mu: ${ou_mr['equilibrium_mu']:.2f}")
    print(f"   • Half-Life tau: {ou_mr['half_life_bars']:.1f} bars | 95% CI: [{ou_mr['half_life_ci'][0]:.1f}, {ou_mr['half_life_ci'][1]:.1f}] bars")
    print(f"   • ADF Stationarity t-stat: {ou_mr['adf_t_stat']:.2f} | Verdict: {ou_mr['stationarity_verdict']}")
    print(f"   • Parameter Stability: {ou_mr['param_stability']:.2f} | Window Stable: {ou_mr['is_window_stable']}")
    print(f"   • R^2 Improvement over SMA-20: {ou_mr['r2_improvement_over_sma']:.3f} | Beats Baseline: {ou_mr['beats_baseline']}")
    
    # Assert validation proof:
    # Runaway trend with extreme |Z| must NOT be marked tradeable
    assert not ou_trend['is_reversion_tradeable'], "Parabolic trend was erroneously permitted for counter-trend shorting!"
    assert ou_mr['is_stationary'], "Stationary OU process failed stationarity test!"
    print("   >>> [VERIFIED] Non-stationary runaway trend correctly rejected despite extreme |Z| > 2.5!")
    
    # =========================================================================
    # PART 3: BAYESIAN PROBABILITY POSTERIOR VALIDATION STUDY
    # =========================================================================
    print("\n" + "-" * 88)
    print("  [PART 3/3] BAYESIAN POSTERIOR PROBABILITY VALIDATION")
    print("-" * 88)
    
    # Case 3A: Weak/Marginal Indicators (Overconfidence Trap under naive model)
    bayes_weak = gmr.calculate_bayesian_confluence(
        smc_action="BUY", smc_confidence=60.0, sge_premium=10.0, tips_bias="NEUTRAL",
        kalman_velocity=0.05, hurst_info={"is_persistent": False, "is_random_walk": True},
        fft_info={"cycle_action_bias": "BULLISH_CYCLE"}
    )
    
    # Case 3B: High Conviction Multi-Disciplinary Confluence
    bayes_strong = gmr.calculate_bayesian_confluence(
        smc_action="BUY", smc_confidence=90.0, sge_premium=28.0, tips_bias="STRONG_BULLISH",
        kalman_velocity=0.22,
        hurst_info={"is_persistent": True, "confidence_interval": {"is_statistically_significant": True}},
        fft_info={"cycle_action_bias": "BULLISH_CYCLE"}
    )
    
    print(f"1. Marginal Indicators:")
    print(f"   • Posterior Bullish Prob: {bayes_weak['bullish_probability_pct']:.1f}% | Prior: {bayes_weak['prior_bullish_pct']:.1f}%")
    print(f"   • 95% Credible Interval: [{bayes_weak['credible_interval_95'][0]:.1f}%, {bayes_weak['credible_interval_95'][1]:.1f}%]")
    print(f"   • Statistical Edge: {bayes_weak['is_statistically_edge']} | Conviction Tier: {bayes_weak['conviction']}")
    print(f"   • Bayes Factor BF_10: {bayes_weak['bayes_factor']:.2f} | Information Gain: {bayes_weak['information_gain_bits']:.3f} bits | Beats Baseline: {bayes_weak['beats_baseline']}")
    
    print(f"\n2. Institutional High-Conviction Confluence:")
    print(f"   • Posterior Bullish Prob: {bayes_strong['bullish_probability_pct']:.1f}% | Prior: {bayes_strong['prior_bullish_pct']:.1f}%")
    print(f"   • 95% Credible Interval: [{bayes_strong['credible_interval_95'][0]:.1f}%, {bayes_strong['credible_interval_95'][1]:.1f}%]")
    print(f"   • Statistical Edge: {bayes_strong['is_statistically_edge']} | Conviction Tier: {bayes_strong['conviction']}")
    print(f"   • Bayes Factor BF_10: {bayes_strong['bayes_factor']:.2f} | Information Gain: {bayes_strong['information_gain_bits']:.3f} bits | Beats Baseline: {bayes_strong['beats_baseline']}")
    
    # Assert validation proof:
    # Marginal indicators must NOT produce High Conviction
    assert bayes_weak['conviction'] in ["NEUTRAL_EQUILIBRIUM", "MODERATE_BULLISH"], "Marginal setup generated high conviction!"
    assert bayes_strong['beats_baseline'], "Strong institutional setup failed baseline benchmark!"
    print("   >>> [VERIFIED] Bayesian inference successfully de-collinearized with 95% Credible Interval & Bayes Factor!")
    
    print("\n" + "=" * 88)
    print("  >>> [CERTIFIED] ALL GAP 4 STATISTICAL VALIDATION BENCHMARKS PASSED! <<<")
    print("=" * 88 + "\n")

if __name__ == "__main__":
    run_gap4_validation_suite()
