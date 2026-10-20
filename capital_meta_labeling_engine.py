# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - CAPITAL META-LABELING ENGINE (MARCOS LÓPEZ DE PRADO ARCHITECTURE)
================================================================================
Institutional 2-Model Meta-Labeling Framework (AQ84 Invariant 85)
Founder: HEM SINATH | Institutional Quantitative Governance

Architecture:
  - Model 1 (Primary Model): Side / Direction prediction (Heuristic Citadel Confluence)
    Determines Direction: BUY if buy_score >= 68.0, SELL if sell_score >= 68.0.
    Maximizes recall to uncover all viable market opportunities.
  - Model 2 (Meta-Model): Binary Classifier (XGBoost / Calibrated Probability)
    Predicts: P(Trade is Profitable = 1 | Primary Signal, Microstructure, Regime, Macro).
    Acts as the Institutional Quality Filter & Bet Sizing Governor.
    Rule:
      meta_win_prob = xgboost_model.predict_proba(features)[1]
      if meta_win_prob >= 0.60:
          execute_trade(sizing_multiplier = clamp(1.0 + (meta_win_prob - 0.60)*2.0, 0.75, 1.50))
      else:
          veto_trade("META_MODEL_REJECTED: Win probability below 60% threshold")
"""

import os
import sys
import json
import time
import pickle
import logging
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List

import numpy as np
import pandas as pd

logger = logging.getLogger("CapitalMetaLabelingEngine")

DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "capital_meta_model.pkl")
DEFAULT_METRICS_PATH = os.path.join(os.path.dirname(__file__), "models", "capital_meta_training_metrics.json")
DEFAULT_DATASET_PATH = os.path.join(os.path.dirname(__file__), "data", "capital_meta_dataset.csv")

FEATURE_COLUMNS = [
    "direction_num",    # +1 for BUY, -1 for SELL
    "raw_score",        # Primary model raw confidence score (68.0 to 99.5)
    "calib_p",          # Primary model calibrated probability (0.50 to 0.95)
    "adx14",            # Trend strength (ADX)
    "rsi14",            # Momentum oscillator (RSI)
    "range_pct",        # Dealing range position (0.0 to 100.0%)
    "atr_norm_pct",     # Relative volatility: ATR14 / Price * 100
    "spread_drag_pct",  # Spread drag friction: Spread / ATR14 * 100
    "ema20_dist_pct",   # Short-term trend distance: (Price / EMA20 - 1) * 100
    "ema50_dist_pct",   # Intermediate trend distance: (Price / EMA50 - 1) * 100
    "ema200_dist_pct",  # Macro trend distance: (Price / EMA200 - 1) * 100
    "dxy_change",       # Macro Dollar index 1-day % change
    "vix",              # Market volatility index level
    "day_of_week"       # Day of week (0=Mon, 4=Fri)
]


class CapitalMetaLabelingEngine:
    """
    Marcos López de Prado 2-Model Meta-Labeling Quantitative Engine.
    Filters raw directional signals through a secondary machine learning model
    to eliminate false positives, boost Precision/Win-Rate, and optimize bet sizing.
    """

    _CACHED_MODEL = None
    _CACHED_METRICS = None
    _MODEL_LOAD_TIME = 0.0

    @classmethod
    def get_feature_columns(cls) -> List[str]:
        return list(FEATURE_COLUMNS)

    @classmethod
    def extract_features(
        cls,
        direction: str,
        raw_score: float,
        calib_p: float,
        adx14: float,
        rsi14: float,
        range_pct: float,
        atr14: float,
        price: float,
        spread: float,
        ema20: float,
        ema50: float,
        ema200: float,
        dxy_change: float = 0.0,
        vix: float = 20.0,
        day_of_week: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Extracts a clean, normalized feature vector for the secondary Meta-Model.
        """
        dir_clean = str(direction or "").upper().strip()
        dir_num = 1.0 if dir_clean == "BUY" else (-1.0 if dir_clean == "SELL" else 0.0)

        price_val = max(1e-5, float(price or 1.0))
        atr_val = max(1e-5, float(atr14 or (price_val * 0.01)))
        spread_val = max(0.0, float(spread or 0.0))

        e20 = float(ema20 or price_val)
        e50 = float(ema50 or price_val)
        e200 = float(ema200 or price_val)

        ema20_dist = ((price_val / max(1e-5, e20)) - 1.0) * 100.0
        ema50_dist = ((price_val / max(1e-5, e50)) - 1.0) * 100.0
        ema200_dist = ((price_val / max(1e-5, e200)) - 1.0) * 100.0

        atr_norm = (atr_val / price_val) * 100.0
        spread_drag = (spread_val / atr_val) * 100.0

        if day_of_week is None:
            day_of_week = datetime.now().weekday()

        return {
            "direction_num": float(dir_num),
            "raw_score": float(max(50.0, min(100.0, raw_score))),
            "calib_p": float(max(0.0, min(1.0, calib_p))),
            "adx14": float(max(0.0, min(100.0, adx14))),
            "rsi14": float(max(0.0, min(100.0, rsi14))),
            "range_pct": float(max(0.0, min(100.0, range_pct))),
            "atr_norm_pct": float(max(0.0, min(50.0, atr_norm))),
            "spread_drag_pct": float(max(0.0, min(100.0, spread_drag))),
            "ema20_dist_pct": float(max(-50.0, min(50.0, ema20_dist))),
            "ema50_dist_pct": float(max(-50.0, min(50.0, ema50_dist))),
            "ema200_dist_pct": float(max(-50.0, min(50.0, ema200_dist))),
            "dxy_change": float(max(-10.0, min(10.0, dxy_change))),
            "vix": float(max(5.0, min(100.0, vix))),
            "day_of_week": float(max(0, min(6, int(day_of_week))))
        }

    @classmethod
    def load_model(cls, model_path: str = DEFAULT_MODEL_PATH) -> Optional[Any]:
        """
        Loads the trained XGBoost Meta-Model from disk into Python memory cache.
        Cached permanently for sub-millisecond tick inference.
        """
        if cls._CACHED_MODEL is not None:
            return cls._CACHED_MODEL

        if not os.path.exists(model_path):
            logger.warning(f"Meta-Model artifact not found at {model_path}. Fallback active.")
            return None

        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            cls._CACHED_MODEL = model
            cls._MODEL_LOAD_TIME = time.time()
            logger.info(f"Loaded XGBoost Meta-Model successfully from {model_path}")
            return cls._CACHED_MODEL
        except Exception as e:
            logger.error(f"Failed to load Meta-Model from {model_path}: {e}")
            return None

    @classmethod
    def load_metrics(cls, metrics_path: str = DEFAULT_METRICS_PATH) -> Dict[str, Any]:
        """Loads metadata and validation metrics of the trained meta-model."""
        if cls._CACHED_METRICS is not None:
            return cls._CACHED_METRICS

        if os.path.exists(metrics_path):
            try:
                with open(metrics_path, "r", encoding="utf-8") as f:
                    cls._CACHED_METRICS = json.load(f)
                    return cls._CACHED_METRICS
            except Exception:
                pass
        return {}

    @classmethod
    def predict_meta_label(
        cls,
        features: Dict[str, float],
        threshold: float = 0.60,
        model_path: str = DEFAULT_MODEL_PATH
    ) -> Dict[str, Any]:
        """
        Model 2 (Meta-Model) Inference:
        Evaluates whether Model 1's proposed trade will be profitable.
        
        Returns:
          - meta_win_prob: float in [0.0, 1.0]
          - is_approved: True if meta_win_prob >= threshold, else False
          - sizing_multiplier: Recommended bet size (1.0 to 1.5x) or 0.0x if rejected
          - verdict: "META_APPROVED" or "META_REJECTED"
          - reason: Human-readable quantitative audit trail
        """
        model = cls.load_model(model_path)
        
        # Build DataFrame with exact feature order
        row_vals = [features.get(col, 0.0) for col in FEATURE_COLUMNS]
        X = pd.DataFrame([row_vals], columns=FEATURE_COLUMNS)

        if model is not None:
            try:
                probs = model.predict_proba(X)
                meta_win_prob = float(probs[0, 1])
                is_ml_inferred = True
            except Exception as e:
                logger.warning(f"XGBoost inference failed ({e}), using analytical fallback.")
                meta_win_prob = cls._analytical_fallback_prob(features)
                is_ml_inferred = False
        else:
            meta_win_prob = cls._analytical_fallback_prob(features)
            is_ml_inferred = False

        is_approved = bool(meta_win_prob >= threshold)

        # Dynamic Bet Sizing Conviction:
        # At threshold 0.60 -> sizing_multiplier = 1.00
        # At prob 0.75 -> sizing_multiplier = 1.30
        # At prob >= 0.85 -> sizing_multiplier = 1.50 (clamped maximum)
        # If rejected -> sizing_multiplier = 0.00
        if is_approved:
            conviction_delta = meta_win_prob - threshold
            sizing_mult = float(np.clip(1.0 + (conviction_delta * 2.0), 0.75, 1.50))
            verdict = "META_APPROVED"
            reason = (
                f"META_APPROVED: P(Win)={meta_win_prob*100:.1f}% >= {threshold*100:.1f}% "
                f"(Conviction Sizing: {sizing_mult:.2f}x)"
            )
        else:
            sizing_mult = 0.0
            verdict = "META_REJECTED"
            reason = (
                f"META_REJECTED: P(Win)={meta_win_prob*100:.1f}% < {threshold*100:.1f}% "
                f"(Avoided false breakout / negative expectancy)"
            )

        return {
            "is_approved": is_approved,
            "meta_win_prob": float(meta_win_prob),
            "threshold": float(threshold),
            "sizing_multiplier": float(sizing_mult),
            "verdict": verdict,
            "reason": reason,
            "is_ml_inferred": is_ml_inferred,
            "features": features
        }

    @staticmethod
    def _analytical_fallback_prob(features: Dict[str, float]) -> float:
        """
        Mathematical Sigmoid fallback when ML model artifact is unavailable.
        Uses calibrated weights from empirical logistic regression.
        """
        z = (
            -0.80
            + 0.015 * features.get("raw_score", 50.0)
            + 1.20 * features.get("calib_p", 0.50)
            + 0.010 * features.get("adx14", 25.0)
            - 0.015 * abs(features.get("rsi14", 50.0) - 50.0)
            - 0.012 * features.get("spread_drag_pct", 5.0)
        )
        prob = 1.0 / (1.0 + np.exp(-np.clip(z, -5.0, 5.0)))
        return float(prob)

    @classmethod
    def build_training_dataset(
        cls,
        save_csv: str = DEFAULT_DATASET_PATH,
        warmup_bars: int = 200,
        holding_bars: int = 45
    ) -> pd.DataFrame:
        """
        Simulates forward trade execution across 10-year historical bars to label
        true ground truth outcomes (y in {0, 1}) for every Model 1 signal.
        """
        import capital_10y_backtester as bt
        
        logger.info("Building 10-year Meta-Labeling training dataset...")
        assets, macro, manifest = bt.load_dataset_clean()
        processed = {sym: bt.compute_indicators(df) for sym, df in assets.items()}

        dxy_df = macro.get("DXY")
        dxy_map = {}
        if dxy_df is not None:
            dxy_df = dxy_df.copy()
            dxy_df["dxy_change"] = dxy_df["close"].pct_change() * 100.0
            for _, r in dxy_df.iterrows():
                dxy_map[r["Date"]] = float(r["dxy_change"]) if not pd.isna(r["dxy_change"]) else 0.0

        vix_df = macro.get("VIX")
        vix_map = {}
        if vix_df is not None:
            for _, r in vix_df.iterrows():
                vix_map[r["Date"]] = float(r["close"]) if not pd.isna(r["close"]) else 20.0

        records = []
        for sym, df in processed.items():
            spec = bt.ASSET_SPECS[sym]
            for i in range(warmup_bars, len(df) - holding_bars):
                row = df.iloc[i]
                prev_rows = df.iloc[max(0, i-35):i]
                curr_d = row["Date"]
                macro_info = {
                    "dxy_change": dxy_map.get(curr_d, 0.0),
                    "vix": vix_map.get(curr_d, 20.0)
                }

                # Model 1 (Primary Model): Side & Confluence
                dir_signal, raw_score, calib_p, meta = bt.evaluate_bar_signals(
                    row=row,
                    prev_rows=prev_rows,
                    spec=spec,
                    macro_row=macro_info
                )
                if dir_signal is not None:
                    next_bar = df.iloc[i+1]
                    entry_p = float(next_bar["open"])
                    atr_val = float(row["atr14"])
                    sp_val = float(spec["spread"])
                    min_dist = max(spec["atr_sl_mult"] * atr_val, 3.5 * sp_val, entry_p * 0.0035)
                    sl_p = entry_p - min_dist if dir_signal == "BUY" else entry_p + min_dist

                    # Simulate trade forward
                    tr = bt.Trade(
                        trade_id=len(records)+1,
                        symbol=sym,
                        direction=dir_signal,
                        entry_date=next_bar["Date"].date(),
                        entry_price=entry_p,
                        sl_price=sl_p,
                        atr_15m=atr_val,
                        spread=sp_val,
                        calibrated_prob=calib_p,
                        raw_score=raw_score,
                        contract_multiplier=spec["contract_multiplier"],
                        regime="TEST",
                        ablation_mode="BASELINE"
                    )
                    swap_rate = spec["daily_swap_long"] if dir_signal == "BUY" else spec["daily_swap_short"]
                    for k in range(i+1, min(len(df), i + holding_bars + 1)):
                        if tr.step(df.iloc[k], swap_rate):
                            break

                    y_win = 1 if tr.pnl_r > 0 else 0

                    feat = cls.extract_features(
                        direction=dir_signal,
                        raw_score=raw_score,
                        calib_p=calib_p,
                        adx14=float(row["adx14"]),
                        rsi14=float(row["rsi14"]),
                        range_pct=float(row["range_pct"]),
                        atr14=atr_val,
                        price=entry_p,
                        spread=sp_val,
                        ema20=float(row["ema20"]),
                        ema50=float(row["ema50"]),
                        ema200=float(row["ema200"]),
                        dxy_change=macro_info["dxy_change"],
                        vix=macro_info["vix"],
                        day_of_week=curr_d.dayofweek
                    )
                    feat["symbol"] = sym
                    feat["date"] = str(curr_d.date())
                    feat["target_win"] = int(y_win)
                    feat["pnl_r"] = float(tr.pnl_r)
                    feat["exit_reason"] = tr.exit_reason
                    records.append(feat)

        df_dataset = pd.DataFrame(records).sort_values("date").reset_index(drop=True)
        if save_csv:
            os.makedirs(os.path.dirname(save_csv), exist_ok=True)
            df_dataset.to_csv(save_csv, index=False)
            logger.info(f"Saved {len(df_dataset)} meta-labeling samples to {save_csv}")

        return df_dataset

    @classmethod
    def train_meta_model(
        cls,
        dataset_csv: str = DEFAULT_DATASET_PATH,
        model_save_path: str = DEFAULT_MODEL_PATH,
        metrics_save_path: str = DEFAULT_METRICS_PATH,
        train_ratio: float = 0.70
    ) -> Dict[str, Any]:
        """
        Trains the XGBoost Meta-Model strictly with chronological split (Zero Look-Ahead).
        Evaluates out-of-sample edge against raw Model 1 baseline.
        """
        import xgboost as xgb
        from sklearn.metrics import roc_auc_score, brier_score_loss, accuracy_score, precision_score

        if not os.path.exists(dataset_csv):
            df_all = cls.build_training_dataset(save_csv=dataset_csv)
        else:
            df_all = pd.read_csv(dataset_csv)

        df_all = df_all.sort_values("date").reset_index(drop=True)
        total_samples = len(df_all)
        if total_samples < 50:
            raise ValueError(f"Insufficient samples for training meta-model: {total_samples}")

        # Chronological Split: 70% In-Sample Train / 30% Out-of-Sample Test
        split_idx = int(total_samples * train_ratio)
        train_df = df_all.iloc[:split_idx]
        test_df = df_all.iloc[split_idx:].copy()

        X_train = train_df[FEATURE_COLUMNS]
        y_train = train_df["target_win"]
        X_test = test_df[FEATURE_COLUMNS]
        y_test = test_df["target_win"]

        logger.info(f"Training XGBoost Meta-Model on {len(X_train)} Train, {len(X_test)} Test samples...")

        clf = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric="logloss"
        )
        clf.fit(X_train, y_train)

        # In-Sample Predictions
        train_probs = clf.predict_proba(X_train)[:, 1]
        train_auc = float(roc_auc_score(y_train, train_probs))
        train_brier = float(brier_score_loss(y_train, train_probs))

        # Out-of-Sample Predictions
        test_probs = clf.predict_proba(X_test)[:, 1]
        test_auc = float(roc_auc_score(y_test, test_probs))
        test_brier = float(brier_score_loss(y_test, test_probs))

        test_df["meta_prob"] = test_probs

        # Baseline (Model 1 alone)
        base_signals = len(test_df)
        base_wins = int((test_df["target_win"] == 1).sum())
        base_wr = (base_wins / max(1, base_signals)) * 100.0
        base_pnl_r = float(test_df["pnl_r"].sum())

        # Meta-Model Filtered (prob >= 0.60)
        approved_df = test_df[test_df["meta_prob"] >= 0.60]
        meta_signals = len(approved_df)
        meta_wins = int((approved_df["target_win"] == 1).sum())
        meta_wr = (meta_wins / max(1, meta_signals)) * 100.0 if meta_signals > 0 else 0.0
        meta_pnl_r = float(approved_df["pnl_r"].sum())

        # Dynamic Sizing Sized PnL
        test_df["sizing_mult"] = test_df["meta_prob"].apply(
            lambda p: float(np.clip(1.0 + (p - 0.60) * 2.0, 0.75, 1.50)) if p >= 0.60 else 0.0
        )
        dynamic_pnl_r = float((test_df["pnl_r"] * test_df["sizing_mult"]).sum())

        # Feature Importances
        imp_series = pd.Series(clf.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)
        feature_importances = {feat: float(score) for feat, score in imp_series.items()}

        metrics = {
            "total_dataset_samples": total_samples,
            "train_samples": len(train_df),
            "test_samples": len(test_df),
            "train_period": f"{train_df['date'].iloc[0]} to {train_df['date'].iloc[-1]}",
            "test_period": f"{test_df['date'].iloc[0]} to {test_df['date'].iloc[-1]}",
            "train_auc": train_auc,
            "train_brier_score": train_brier,
            "test_auc": test_auc,
            "test_brier_score": test_brier,
            "baseline_model1": {
                "signals": base_signals,
                "wins": base_wins,
                "win_rate_pct": round(base_wr, 2),
                "total_pnl_r": round(base_pnl_r, 2)
            },
            "meta_model2_filtered_0_60": {
                "signals": meta_signals,
                "wins": meta_wins,
                "win_rate_pct": round(meta_wr, 2),
                "total_pnl_r": round(meta_pnl_r, 2),
                "avoided_bad_trades": base_signals - meta_signals,
                "win_rate_improvement_pct": round(meta_wr - base_wr, 2),
                "pnl_r_improvement": round(meta_pnl_r - base_pnl_r, 2),
                "dynamic_conviction_pnl_r": round(dynamic_pnl_r, 2)
            },
            "feature_importances": feature_importances,
            "trained_at": datetime.now().isoformat()
        }

        # Save artifacts
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        with open(model_save_path, "wb") as f:
            pickle.dump(clf, f)
        cls._CACHED_MODEL = clf
        cls._MODEL_LOAD_TIME = time.time()

        os.makedirs(os.path.dirname(metrics_save_path), exist_ok=True)
        with open(metrics_save_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        cls._CACHED_METRICS = metrics

        logger.info(
            f"Meta-Model training complete! Out-of-sample Win Rate improved from "
            f"{base_wr:.2f}% -> {meta_wr:.2f}% (+{meta_wr-base_wr:.2f}%), "
            f"Total R: {base_pnl_r:.2f}R -> {meta_pnl_r:.2f}R (+{meta_pnl_r-base_pnl_r:.2f}R). "
            f"Artifacts saved to {model_save_path} and {metrics_save_path}"
        )

        return metrics

    @classmethod
    def calculate_conviction_sizing(cls, meta_win_prob: float, threshold: float = 0.60) -> float:
        """
        Dynamically calculates conviction sizing multiplier in range [0.75, 1.50],
        or returns 0.0 if win probability is below threshold.
        """
        if meta_win_prob < threshold:
            return 0.0
        conviction_delta = meta_win_prob - threshold
        return float(np.clip(1.0 + (conviction_delta * 2.0), 0.75, 1.50))

    @classmethod
    def predict_meta_edge(
        cls,
        features: Dict[str, float],
        threshold: float = 0.60,
        model_path: str = DEFAULT_MODEL_PATH
    ) -> Dict[str, Any]:
        """
        Evaluates quantitative edge with feature aliasing and returns edge approval status.
        """
        feat = dict(features)
        if "raw_score" not in feat and "primary_score" in feat:
            feat["raw_score"] = feat["primary_score"]
        if "rsi14" not in feat and "rsi_15m" in feat:
            feat["rsi14"] = feat["rsi_15m"]
        if "adx14" not in feat and "adx_15m" in feat:
            feat["adx14"] = feat["adx_15m"]
        if "ema200_dist_pct" not in feat and "dist_to_ema200" in feat:
            val = float(feat["dist_to_ema200"])
            feat["ema200_dist_pct"] = val * 100.0 if abs(val) < 1.0 else val
        if "dxy_change" not in feat and "dxy_trend" in feat:
            feat["dxy_change"] = feat["dxy_trend"]
        if "vix" not in feat and "vix_level" in feat:
            feat["vix"] = feat["vix_level"]
        if "atr_norm_pct" not in feat and "atr_pct" in feat:
            val = float(feat["atr_pct"])
            feat["atr_norm_pct"] = val * 100.0 if abs(val) < 1.0 else val
        if "spread_drag_pct" not in feat and "spread_atr_ratio" in feat:
            val = float(feat["spread_atr_ratio"])
            feat["spread_drag_pct"] = val * 100.0 if abs(val) < 1.0 else val

        res = cls.predict_meta_label(feat, threshold=threshold, model_path=model_path)
        return {
            "is_edge_approved": res["is_approved"],
            "meta_win_prob": res["meta_win_prob"],
            "threshold": res["threshold"],
            "sizing_multiplier": res["sizing_multiplier"],
            "verdict": res["verdict"],
            "reason": res["reason"],
            "is_ml_inferred": res.get("is_ml_inferred", False),
            "features": res.get("features", feat)
        }


def get_meta_labeling_engine() -> Any:
    """Returns the CapitalMetaLabelingEngine class singleton."""
    return CapitalMetaLabelingEngine


def predict_meta_edge(features: Dict[str, float], threshold: float = 0.60) -> Dict[str, Any]:
    """Module-level helper to evaluate meta-label edge."""
    return CapitalMetaLabelingEngine.predict_meta_edge(features, threshold=threshold)


def calculate_conviction_sizing(meta_win_prob: float, threshold: float = 0.60) -> float:
    """Module-level helper to calculate conviction sizing."""
    return CapitalMetaLabelingEngine.calculate_conviction_sizing(meta_win_prob, threshold=threshold)

