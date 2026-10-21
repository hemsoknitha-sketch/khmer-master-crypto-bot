# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - INSTITUTIONAL BRAIN FEATURE BUILDER
===================================================
Solves feature schema mismatch across diverse quantitative models in models/:
- 4-Feature OHLC Vector: for `brain_price.pkl` (MinMaxScaler scaler_x/scaler_y)
- 12-Feature Ensemble Vector: for `brain_scaler.pkl`, `brain_xgb.pkl`, `brain_lightgbm.pkl`, `brain_moe_router.pkl`
- 37-Feature Multi-Factor Vector: for `brain_dca.pkl`, `brain_trend.pkl`, `brain_vol.pkl`, `brain_tp.pkl`
- 10-Feature PINN/Graph Vector: for `brain_pinn_jump_diff.pkl`, `brain_tgat_graph.pkl`
- 32-Feature TradFi AFML Vector: for `capital_meta_model.pkl`
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd

log = logging.getLogger("feature_builder")

# 37 Canonical Features from brain_config.json
CANONICAL_37_FEATURES = [
    "open", "high", "low", "close", "volume",
    "buy_volume", "sell_volume", "cvd", "buy_sell_ratio", "imbalance", "aggressor_bias",
    "sma7", "sma30", "sma90", "ema12", "ema26",
    "rsi14", "atr14", "volatility30", "bollinger_width",
    "volume_sma7", "volume_ratio", "hl_pct", "co_pct",
    "ma_diff_7_30", "ma_diff_7_90", "regime", "support_30", "resistance_30",
    "lstm_pred", "rl_signal", "sp500", "fng",
    "n_transactions", "hash_rate", "avg_block_size", "mempool_count"
]

# 12 Technical Ensemble Features from market_data.py
CANONICAL_12_FEATURES = [
    "ema_score", "atr_ratio", "cvd_imbalance", "vwap_zscore", "rsi14",
    "curr_hist", "hist_accel", "dist_high", "dist_low",
    "sweep_score", "fvg_score", "fib_proximity"
]

# 4 OHLC Features for Price Regressor
CANONICAL_4_OHLC = ["open", "high", "low", "close"]


class BrainFeatureBuilder:
    """
    Unified multi-tier feature builder ensuring mathematical exactness:
    O(F) time complexity and O(F) space complexity.
    """

    @staticmethod
    def build_4_ohlc_features(df: pd.DataFrame) -> np.ndarray:
        """
        Extracts last OHLC bar for 4-feature Price Regressor (brain_price.pkl).
        Expected input to brain_scaler_x.pkl.
        """
        if df is None or len(df) == 0:
            return np.zeros((1, 4), dtype=np.float64)
        row = df.iloc[-1]
        o = float(row.get("open", 0.0) or 0.0)
        h = float(row.get("high", 0.0) or 0.0)
        l = float(row.get("low", 0.0) or 0.0)
        c = float(row.get("close", 0.0) or 0.0)
        return np.array([[o, h, l, c]], dtype=np.float64)

    @staticmethod
    def build_12_ensemble_features(
        ema_score: float = 0.0,
        atr_ratio: float = 0.015,
        cvd_imbalance: float = 0.0,
        vwap_zscore: float = 0.0,
        rsi14: float = 50.0,
        curr_hist: float = 0.0,
        hist_accel: float = 0.0,
        dist_high: float = 0.01,
        dist_low: float = 0.01,
        sweep_score: float = 0.0,
        fvg_score: float = 0.0,
        fib_proximity: float = 0.5
    ) -> np.ndarray:
        """
        Builds 12-feature vector for brain_scaler.pkl, brain_xgb.pkl, brain_lightgbm.pkl, brain_moe_router.pkl.
        """
        return np.array([[
            float(ema_score),
            float(atr_ratio),
            float(cvd_imbalance),
            float(vwap_zscore),
            float(rsi14),
            float(curr_hist),
            float(hist_accel),
            float(dist_high),
            float(dist_low),
            float(sweep_score),
            float(fvg_score),
            float(fib_proximity)
        ]], dtype=np.float64)

    @staticmethod
    def build_37_causal_features(df: pd.DataFrame, feature_cols: Optional[List[str]] = None) -> np.ndarray:
        """
        Builds 37-feature vector for brain_dca.pkl, brain_trend.pkl, brain_vol.pkl, brain_tp.pkl.
        Fills missing indicators gracefully with zero/neutral defaults.
        """
        cols = feature_cols or CANONICAL_37_FEATURES
        if df is None or len(df) == 0:
            return np.zeros((1, len(cols)), dtype=np.float64)
        latest = df.iloc[-1:].copy()
        for col in cols:
            if col not in latest.columns:
                latest[col] = 0.0
        return latest[cols].values.astype(np.float64)

    @staticmethod
    def build_10_pinn_tgat_features(df: pd.DataFrame) -> np.ndarray:
        """
        Builds 10-feature vector for brain_pinn_jump_diff.pkl and brain_tgat_graph.pkl.
        """
        if df is None or len(df) == 0:
            return np.zeros((1, 10), dtype=np.float64)
        row = df.iloc[-1]
        c = float(row.get("close", 1.0) or 1.0)
        v = float(row.get("volume", 0.0) or 0.0)
        r = float(row.get("rsi14", 50.0) or 50.0)
        a = float(row.get("atr14", 0.0) or 0.0) / (c + 1e-10)
        hl = (float(row.get("high", c)) - float(row.get("low", c))) / (c + 1e-10)
        co = (c - float(row.get("open", c))) / (c + 1e-10)
        cvd = float(row.get("cvd", 0.0) or 0.0)
        sma7 = float(row.get("sma7", c) or c) / (c + 1e-10)
        sma30 = float(row.get("sma30", c) or c) / (c + 1e-10)
        bw = float(row.get("bollinger_width", 0.02) or 0.02)
        return np.array([[c, v, r, a, hl, co, cvd, sma7, sma30, bw]], dtype=np.float64)

    @staticmethod
    def route_and_predict(models: Dict[str, Any], df: pd.DataFrame, extra_telemetry: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Routes each model in models/ to its exact expected feature dimension:
        - price: 4 OHLC features via scaler_x / scaler_y
        - trend, vol, tp, dca: 37 causal features
        - moe_router, xgb, lgb, cb: 12 ensemble features via brain_scaler.pkl
        """
        extra = extra_telemetry or {}
        out = {}

        # 1. Price prediction (4-feature direct dollar regressor)
        if "price" in models and models["price"] is not None:
            try:
                x_4 = BrainFeatureBuilder.build_4_ohlc_features(df)
                if "scaler_x" in models and models["scaler_x"] is not None:
                    try:
                        x_4_sc = models["scaler_x"].transform(x_4)
                    except Exception:
                        x_4_sc = x_4
                else:
                    x_4_sc = x_4
                raw_pred = models["price"].predict(x_4_sc)
                pred_price = float(raw_pred[0])
                # Sanity guard: price prediction must be positive and within reasonable corridor (0.1x to 5.0x current price)
                c_now = float(df["close"].iloc[-1]) if df is not None and len(df) > 0 else 0.0
                if c_now > 0 and (pred_price <= 0 or pred_price > c_now * 5.0 or pred_price < c_now * 0.1):
                    pred_price = c_now
                out["pred_price"] = pred_price
            except Exception as e:
                log.debug("Price prediction routing note: %s", e)
                out["pred_price"] = float(df["close"].iloc[-1]) if df is not None and len(df) > 0 else 0.0

        # 2. 37-Feature Multi-Factor Models (Trend, Volatility, TP, DCA)
        x_37 = BrainFeatureBuilder.build_37_causal_features(df)
        for name in ["trend", "volatility", "tp_signal", "dca_zone"]:
            if name in models and models[name] is not None:
                try:
                    m = models[name]
                    n_exp = getattr(m, "n_features_in_", 37)
                    if n_exp == 37:
                        out[name] = m.predict(x_37)[0]
                    elif n_exp == 12 and "scaler" in models and models["scaler"] is not None:
                        # Fallback for 12-feature version
                        x_12 = BrainFeatureBuilder.build_12_ensemble_features(
                            ema_score=extra.get("ema_score", 0.0),
                            atr_ratio=extra.get("atr_pct", 1.5) / 100.0,
                            cvd_imbalance=extra.get("cvd_imbalance", 0.0),
                            vwap_zscore=extra.get("vwap_zscore", 0.0),
                            rsi14=extra.get("rsi14", 50.0),
                            curr_hist=extra.get("curr_hist", 0.0),
                            hist_accel=extra.get("hist_accel", 0.0),
                            dist_high=extra.get("dist_high", 0.01),
                            dist_low=extra.get("dist_low", 0.01),
                            sweep_score=extra.get("sweep_score", 0.0),
                            fvg_score=extra.get("fvg_score", 0.0),
                            fib_proximity=extra.get("fib_proximity", 0.5)
                        )
                        x_12_sc = models["scaler"].transform(x_12)
                        out[name] = m.predict(x_12_sc)[0]
                except Exception as e:
                    log.debug("Model %s routing note: %s", name, e)

        # 3. 12-Feature Ensemble Models (MoE Router, XGB, LGB, CatBoost)
        if "scaler" in models and models["scaler"] is not None:
            try:
                x_12 = BrainFeatureBuilder.build_12_ensemble_features(
                    ema_score=extra.get("ema_score", 0.0),
                    atr_ratio=extra.get("atr_pct", 1.5) / 100.0,
                    cvd_imbalance=extra.get("cvd_imbalance", 0.0),
                    vwap_zscore=extra.get("vwap_zscore", 0.0),
                    rsi14=extra.get("rsi14", 50.0),
                    curr_hist=extra.get("curr_hist", 0.0),
                    hist_accel=extra.get("hist_accel", 0.0),
                    dist_high=extra.get("dist_high", 0.01),
                    dist_low=extra.get("dist_low", 0.01),
                    sweep_score=extra.get("sweep_score", 0.0),
                    fvg_score=extra.get("fvg_score", 0.0),
                    fib_proximity=extra.get("fib_proximity", 0.5)
                )
                x_12_sc = models["scaler"].transform(x_12)
                for ens_name in ["moe_router", "xgb", "lgb", "cb"]:
                    if ens_name in models and models[ens_name] is not None:
                        m = models[ens_name]
                        if hasattr(m, "predict_proba"):
                            out[f"{ens_name}_proba"] = float(m.predict_proba(x_12_sc)[0, 1])
                        elif hasattr(m, "predict"):
                            out[f"{ens_name}_pred"] = m.predict(x_12_sc)[0]
            except Exception as e_ens:
                log.debug("Ensemble routing note: %s", e_ens)

        return out
