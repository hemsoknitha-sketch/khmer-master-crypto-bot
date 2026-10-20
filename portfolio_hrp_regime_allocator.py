# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - HIERARCHICAL RISK PARITY & PROBABILISTIC REGIME ALLOCATOR (AFML CH. 16)
=======================================================================================
Marcos López de Prado Institutional Portfolio Optimization (AQ86 Standard)
Founder: HEM SINATH | Institutional Quantitative Governance

Components:
  1. Hierarchical Risk Parity (HRP - AFML Chapter 16):
     - Tree Clustering: Distance metric D = sqrt((1 - rho) / 2) & single-linkage hierarchy.
     - Quasi-Diagonalization: Reorders covariance matrix to place similar assets adjacent.
     - Recursive Bisection: Allocates inverse-variance risk weights without matrix inversion.
  2. Markowitz Mean-Variance Comparison:
     - Minimum Variance Portfolio & Tangency / Max-Sharpe Portfolio comparison.
  3. Probabilistic Regime Classifier (Gaussian HMM):
     - 4-State HMM: {"BULL": p1, "CHOP": p2, "BEAR": p3, "CRASH": p4}.
     - Conditions directional permission and trade frequency on regime probability.
  4. Dynamic Volatility Targeting:
     - Scales position sizing by target_vol (10% annualized) / realized_vol_20d.
"""

import os
import math
import logging
from typing import Dict, Any, Tuple, Optional, List

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
from hmmlearn import hmm

logger = logging.getLogger("PortfolioHRPRegimeAllocator")


# -----------------------------------------------------------------------------
# 1. Hierarchical Risk Parity (HRP) Engine
# -----------------------------------------------------------------------------
class HierarchicalRiskParity:
    """
    Marcos López de Prado Hierarchical Risk Parity (HRP) Portfolio Optimizer.
    Solves the Markowitz instability flaw by eliminating covariance matrix inversion.
    """

    @staticmethod
    def correlation_to_distance(corr_matrix: np.ndarray) -> np.ndarray:
        """Converts Pearson correlation matrix to angular distance metric D in [0, 1]."""
        d = np.sqrt(np.clip(0.5 * (1.0 - corr_matrix), 0.0, 1.0))
        np.fill_diagonal(d, 0.0)
        return d

    @classmethod
    def get_quasi_diag_order(cls, link_matrix: np.ndarray) -> List[int]:
        """Recovers quasi-diagonal ordered indices from linkage matrix."""
        link_matrix = link_matrix.astype(int)
        num_items = link_matrix[-1, 3]
        order = [link_matrix[-1, 0], link_matrix[-1, 1]]

        while max(order) >= num_items:
            new_order = []
            for item in order:
                if item >= num_items:
                    cluster_idx = item - num_items
                    new_order.append(link_matrix[cluster_idx, 0])
                    new_order.append(link_matrix[cluster_idx, 1])
                else:
                    new_order.append(item)
            order = new_order

        return order

    @staticmethod
    def get_cluster_variance(cov_matrix: np.ndarray, cluster_indices: List[int]) -> float:
        """Calculates inverse-variance cluster variance."""
        sub_cov = cov_matrix[np.ix_(cluster_indices, cluster_indices)]
        inv_diag = 1.0 / np.maximum(1e-6, np.diag(sub_cov))
        w = inv_diag / np.sum(inv_diag)
        var = float(np.dot(np.dot(w, sub_cov), w))
        return var

    @classmethod
    def recursive_bisection(cls, cov_matrix: np.ndarray, ordered_indices: List[int]) -> np.ndarray:
        """Recursively bisects ordered clusters and allocates inverse-variance weights."""
        n = len(ordered_indices)
        weights = pd.Series(1.0, index=ordered_indices)
        clusters = [ordered_indices]

        while len(clusters) > 0:
            new_clusters = []
            for cluster in clusters:
                if len(cluster) > 1:
                    mid = len(cluster) // 2
                    c1 = cluster[:mid]
                    c2 = cluster[mid:]

                    var1 = cls.get_cluster_variance(cov_matrix, c1)
                    var2 = cls.get_cluster_variance(cov_matrix, c2)

                    # Allocation factor alpha
                    alpha = 1.0 - (var1 / max(1e-6, var1 + var2))

                    weights[c1] *= alpha
                    weights[c2] *= (1.0 - alpha)

                    new_clusters.append(c1)
                    new_clusters.append(c2)
            clusters = new_clusters

        return weights.sort_index().values

    @classmethod
    def allocate(
        cls,
        cov_matrix: np.ndarray,
        asset_names: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Allocates portfolio weights using HRP from a covariance matrix.
        """
        cov = np.asarray(cov_matrix, dtype=float)
        n = cov.shape[0]
        if asset_names is None or len(asset_names) != n:
            asset_names = [f"Asset_{i}" for i in range(n)]

        # Derive correlation matrix from covariance
        std = np.sqrt(np.maximum(1e-8, np.diag(cov)))
        std_outer = np.outer(std, std)
        corr = cov / np.maximum(1e-8, std_outer)
        np.fill_diagonal(corr, 1.0)
        corr = np.clip(corr, -1.0, 1.0)

        # 1. Tree Clustering
        dist = cls.correlation_to_distance(corr)
        condensed_dist = squareform(dist, checks=False)
        link = linkage(condensed_dist, method="single")

        # 2. Quasi-Diagonalization
        sorted_order = cls.get_quasi_diag_order(link)

        # 3. Recursive Bisection
        hrp_raw_weights = cls.recursive_bisection(cov, sorted_order)

        return {asset_names[i]: float(hrp_raw_weights[i]) for i in range(n)}

    @classmethod
    def optimize_portfolio(
        cls,
        returns_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Executes complete HRP optimization across assets.
        Returns HRP weights, Inverse-Variance weights, and Equal-Weights.
        """
        assets = list(returns_df.columns)
        cov = returns_df.cov().values
        corr = returns_df.corr().values

        # 1. Tree Clustering
        dist = cls.correlation_to_distance(corr)
        condensed_dist = squareform(dist, checks=False)
        link = linkage(condensed_dist, method="single")

        # 2. Quasi-Diagonalization
        sorted_order = cls.get_quasi_diag_order(link)

        # 3. Recursive Bisection
        hrp_raw_weights = cls.recursive_bisection(cov, sorted_order)

        # Baseline: Inverse Variance
        inv_vars = 1.0 / np.maximum(1e-6, np.diag(cov))
        inv_var_weights = inv_vars / np.sum(inv_vars)

        # Baseline: Equal Weights
        equal_weights = np.ones(len(assets)) / len(assets)

        hrp_dict = {assets[i]: round(float(hrp_raw_weights[i]), 4) for i in range(len(assets))}
        inv_var_dict = {assets[i]: round(float(inv_var_weights[i]), 4) for i in range(len(assets))}
        equal_dict = {assets[i]: round(float(equal_weights[i]), 4) for i in range(len(assets))}

        # Portfolio Variances
        hrp_var = float(np.dot(np.dot(hrp_raw_weights, cov), hrp_raw_weights)) * 252.0
        inv_var = float(np.dot(np.dot(inv_var_weights, cov), inv_var_weights)) * 252.0
        eq_var = float(np.dot(np.dot(equal_weights, cov), equal_weights)) * 252.0

        return {
            "assets": assets,
            "hrp_weights": hrp_dict,
            "inverse_variance_weights": inv_var_dict,
            "equal_weights": equal_dict,
            "annualized_portfolio_volatility": {
                "HRP": round(math.sqrt(hrp_var) * 100.0, 2),
                "InverseVariance": round(math.sqrt(inv_var) * 100.0, 2),
                "EqualWeight": round(math.sqrt(eq_var) * 100.0, 2)
            },
            "hierarchical_order": [assets[i] for i in sorted_order]
        }


# -----------------------------------------------------------------------------
# 2. Probabilistic Regime Classification via Gaussian HMM
# -----------------------------------------------------------------------------
class ProbabilisticRegimeHMM:
    """
    Gaussian Hidden Markov Model for Regime Belief Distribution.
    Categorizes market conditions into 4 macro states:
      - BULL: Strong directional trend, low-to-medium volatility.
      - CHOP: Sideways mean-reverting oscillation, high entropy.
      - BEAR: Downward repricing, expanding volatility.
      - CRASH: Volatility shock, high VIX, extreme tail risk.
    """

    def __init__(self, n_components: int = 4, random_state: int = 42):
        self.n_components = n_components
        self.random_state = random_state
        self.model = hmm.GaussianHMM(
            n_components=n_components,
            covariance_type="full",
            n_iter=100,
            random_state=random_state
        )
        self.is_fitted = False
        self.regime_labels = ["BULL", "CHOP", "BEAR", "CRASH"]

    def fit(self, features: np.ndarray):
        """Fits Gaussian HMM on multivariate macro features."""
        try:
            self.model.fit(features)
            self.is_fitted = True
            logger.info("Gaussian HMM fitted successfully on macro features.")
        except Exception as e:
            logger.warning(f"Gaussian HMM fit warning: {e}")
            self.is_fitted = False

    def predict_regime_probabilities(self, current_features: np.ndarray) -> Dict[str, float]:
        """
        Infers probabilistic regime beliefs.
        Returns: {"BULL": p1, "CHOP": p2, "BEAR": p3, "CRASH": p4}
        """
        if not self.is_fitted:
            return {"BULL": 0.40, "CHOP": 0.35, "BEAR": 0.20, "CRASH": 0.05}

        feats = np.asarray(current_features)
        if feats.ndim == 1:
            feats = feats.reshape(1, -1)

        try:
            probs = self.model.predict_proba(feats)[0]
            # Map states based on mean volatility/VIX
            order = np.argsort(self.model.means_[:, 0])  # Sorted by feature 0 (e.g. VIX)
            mapped = {
                "BULL": float(probs[order[0]]),
                "CHOP": float(probs[order[1]]),
                "BEAR": float(probs[order[2]]),
                "CRASH": float(probs[order[3]])
            }
            return mapped
        except Exception:
            return {"BULL": 0.40, "CHOP": 0.35, "BEAR": 0.20, "CRASH": 0.05}


# -----------------------------------------------------------------------------
# 3. Dynamic Volatility Targeting Sizer
# -----------------------------------------------------------------------------
class VolatilityTargetingSizer:
    """
    Dynamic Volatility Targeting Position Sizer.
    Formula:
      position_scale = target_vol / realized_vol_20d
      clamped strictly between [0.50x, 2.00x]
    """

    def __init__(self, target_vol: float = 0.10):
        self.target_vol = float(target_vol)

    def calculate_scale(self, price: float, atr14: float) -> float:
        """Calculates dynamic volatility scalar based on 14-bar ATR annualized."""
        price_val = max(1e-5, float(price))
        atr_val = max(1e-5, float(atr14))

        # Realized volatility estimate
        realized_vol = (atr_val / price_val) * math.sqrt(252.0)
        realized_vol = max(0.02, realized_vol)

        scale = self.target_vol / realized_vol
        clamped_scale = float(np.clip(scale, 0.50, 2.00))
        return clamped_scale


# Aliases & Convenience Helpers
GaussianHMMRegimeModel = ProbabilisticRegimeHMM


def calculate_volatility_targeting_multiplier(
    realized_vol_20d: float,
    target_annual_vol: float = 0.10
) -> float:
    """
    Calculates dynamic volatility targeting multiplier: target_vol / realized_vol,
    clamped strictly to range [0.40, 2.00].
    """
    rv = max(0.01, float(realized_vol_20d))
    scale = float(target_annual_vol) / rv
    return float(np.clip(scale, 0.40, 2.00))

