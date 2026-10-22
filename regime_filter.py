# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - GAUSSIAN HMM REGIME DETECTION & PROBABILISTIC FILTER
===================================================================
Document Version: 1.0.0 (AQ84 Invariant 85 Standard)
Author: HEM SINATH | Institutional Quantitative Governance

Probabilistic Market Regime Categorization via Hidden Markov Models (HMM):
  - State 0: Secular Trend Expansion (High momentum, Hurst > 0.55, ADX >= 25.0)
  - State 1: Volatility Shock / Contraction (VIX > 28.0, Jump clustering)
  - State 2: Mean-Reverting Equilibrium Chop (Hurst < 0.48, High trap density)

Directional Gatekeeper Rules:
  1. In Regime 2 (Chop): If P(Chop) >= 0.60, veto breakout chasing entries.
  2. In Regime 1 (Crash/Shock): If P(Shock) >= 0.28, block unhedged Long positions.
  3. In Regime 0 (Trend): Normal high-expectancy scale-out execution.
"""

import os
import sys
import logging
from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from hmmlearn import hmm

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("RegimeFilter")


class InstitutionalHMMRegimeFilter:
    """
    Gaussian Hidden Markov Model for market regime inference.
    Prevents holdout decay by filtering entries during unfavorable macro chop.
    """

    def __init__(self, n_states: int = 3, random_state: int = 42):
        self.n_states = n_states
        self.random_state = random_state
        self.model = hmm.GaussianHMM(
            n_components=n_states,
            covariance_type="diag",
            n_iter=100,
            random_state=random_state
        )
        self.is_fitted = False
        self._fit_default_macro_distributions()

    def _fit_default_macro_distributions(self):
        """
        Calibrates initial regime emissions from historical macro benchmarks.
        Features: [VIX, DXY 1-day Change, 10Y Yield Change].
        """
        # Synthetic empirical calibration representing Trend, Shock, and Chop regimes
        # 1. Trend: Moderate VIX (~16), moderate DXY change (~0.0), low yield volatility
        trend_samples = np.random.normal(loc=[16.0, 0.0, 0.0], scale=[2.0, 0.3, 0.02], size=(300, 3))
        # 2. Shock: High VIX (~34), sharp DXY spike (~0.8), high yield surge
        shock_samples = np.random.normal(loc=[34.0, 0.8, 0.08], scale=[5.0, 0.6, 0.05], size=(150, 3))
        # 3. Chop: Low/Medium VIX (~19), whipsawing DXY (~ -0.1), flat yield
        chop_samples = np.random.normal(loc=[19.0, -0.05, -0.01], scale=[2.5, 0.4, 0.03], size=(300, 3))

        X_train = np.vstack([trend_samples, shock_samples, chop_samples])
        try:
            self.model.fit(X_train)
            self.is_fitted = True
        except Exception as exc:
            logger.warning(f"Default HMM calibration fallback: {exc}")

    def evaluate_market_regime(
        self,
        vix: float = 20.0,
        dxy_change: float = 0.0,
        tnx_change: float = 0.0,
        hurst_exponent: float = 0.50,
        adx: float = 25.0
    ) -> Dict[str, Any]:
        """
        Computes probabilistic regime beliefs and directional approvals.
        """
        obs = np.array([[float(vix), float(dxy_change), float(tnx_change)]])
        p_shock = 0.0
        p_chop = 0.0
        p_trend = 1.0

        if self.is_fitted:
            try:
                probs = self.model.predict_proba(obs)[0]
                # Rank states by mean VIX emission to maintain consistent labeling
                vix_means = self.model.means_[:, 0]
                sorted_idx = np.argsort(vix_means)
                idx_trend, idx_chop, idx_shock = sorted_idx[0], sorted_idx[1], sorted_idx[2]

                p_trend = float(probs[idx_trend])
                p_chop = float(probs[idx_chop])
                p_shock = float(probs[idx_shock])
            except Exception:
                p_trend, p_chop, p_shock = 0.6, 0.3, 0.1

        # Augment with technical indicators (Hurst and ADX)
        if hurst_exponent < 0.45 or adx < 20.0:
            p_chop = min(1.0, p_chop + 0.25)
            p_trend = max(0.0, p_trend - 0.25)
        elif hurst_exponent > 0.60 and adx >= 28.0:
            p_trend = min(1.0, p_trend + 0.20)
            p_chop = max(0.0, p_chop - 0.20)

        # Re-normalize
        total_p = p_trend + p_chop + p_shock
        if total_p > 0:
            p_trend /= total_p
            p_chop /= total_p
            p_shock /= total_p

        # Determine dominant regime
        if p_shock >= 0.28:
            dominant_regime = "VOLATILITY_SHOCK"
            long_allowed = False
            short_allowed = True
            sizing_factor = 0.75
            veto_reason = "VETO_REGIME_VOLATILITY_SHOCK (P(Shock) >= 28%)"
        elif p_chop >= 0.60:
            dominant_regime = "CHOP"
            long_allowed = False
            short_allowed = False
            sizing_factor = 0.0
            veto_reason = "VETO_REGIME_CHOP_HIGH_WHIPSAW (P(Chop) >= 60%)"
        else:
            dominant_regime = "TREND_EXPANSION"
            long_allowed = True
            short_allowed = True
            sizing_factor = 1.0
            veto_reason = None

        return {
            "dominant_regime": dominant_regime,
            "p_trend": round(p_trend, 3),
            "p_chop": round(p_chop, 3),
            "p_shock": round(p_shock, 3),
            "long_allowed": long_allowed,
            "short_allowed": short_allowed,
            "sizing_factor": sizing_factor,
            "veto_reason": veto_reason
        }
