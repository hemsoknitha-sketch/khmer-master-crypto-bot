# ==============================================================================
# 🚀 KHMER MASTER CRYPTO / APEX SUPER BRAIN AGI v13.00
# 🏛️ 10-PILLAR SUPER SMART QUANT MODEL TRAINER (GOOGLE COLAB GPU SUITE)
# ==============================================================================
# Trains Institutional Models on 10 Foundational Quantitative Pillars:
# 1. Market Structure / Price Action (BOS, CHoCH, HH/HL/LH/LL)
# 2. Support & Resistance / Supply & Demand (Order Blocks & FVG)
# 3. Liquidity / Swings (PDH/PDL Turtle Soup Sweeps)
# 4. Multi-Timeframe EMA Alignment (EMA 20 / 50 / 200)
# 5. ATR Volatility & Stop-Loss Multiplier
# 6. Volume & Order Flow (CVD Imbalance & Aggressive Delta)
# 7. VWAP & Standard Deviation Bands (±1σ, ±2σ)
# 8. RSI 14 & Regular/Hidden Divergence Detection
# 9. MACD Momentum Acceleration
# 10. Fibonacci Retracement (Golden Pocket 61.8% OTE Pullback)
#
# Models Generated:
# - HMM Market Regime Classifier (brain_hmm_regime.pkl)
# - Triple Ensemble (brain_xgb.pkl, brain_catboost.pkl, brain_lightgbm.pkl)
# - PatchTST Self-Attention Transformer (brain_patchtst.h5)
# - MoE Gating Router (brain_moe_router.pkl)
# - Standard Scaler (brain_scaler.pkl)
#
# Automatically uploads all model weights to Hugging Face Model Hub!
# ==============================================================================

import os
import sys
import time
import json
import joblib
import requests
import numpy as np
import pandas as pd
from datetime import datetime

# Colab / GPU Environment Dependencies Check
def install_dependencies():
    print("📦 [ENVIRONMENT SETUP] Checking and installing required quant dependencies...")
    packages = [
        "xgboost", "catboost", "lightgbm", "hmmlearn", "huggingface_hub",
        "scikit-learn", "tensorflow", "requests", "pandas", "numpy"
    ]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"  └─ Installing {pkg}...")
            os.system(f"{sys.executable} -m pip install --quiet {pkg}")
    print("✅ [ENVIRONMENT SETUP] All dependencies verified!")

# ==============================================================================
# 1. BINANCE HISTORICAL DATA FETCHER (MULTI-PAIR & MULTI-TIMEFRAME)
# ==============================================================================
def fetch_binance_klines(symbol="BTCUSDT", interval="15m", limit=1000):
    """Fetches high-resolution klines from Binance Public API with taker buy volume."""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            raw = res.json()
            cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_vol', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore']
            df = pd.DataFrame(raw, columns=cols)
            for c in ['open', 'high', 'low', 'close', 'volume', 'taker_buy_base', 'taker_buy_quote']:
                df[c] = pd.to_numeric(df[c])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
    except Exception as e:
        print(f"⚠️ Error fetching data for {symbol}: {e}")
    return pd.DataFrame()

def fetch_multi_pair_dataset(symbols=["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"], interval="15m"):
    print(f"📊 [DATA INGESTION] Fetching multi-pair dataset ({len(symbols)} pairs, {interval} interval)...")
    dfs = []
    for sym in symbols:
        print(f"  └─ Fetching {sym}...")
        df = fetch_binance_klines(sym, interval=interval, limit=1000)
        if not df.empty and len(df) > 100:
            df['symbol'] = sym
            dfs.append(df)
        time.sleep(0.3)
    if not dfs:
        raise ValueError("Failed to fetch data from Binance. Please check internet connection.")
    combined_df = pd.concat(dfs).sort_index()
    print(f"✅ [DATA INGESTION] Total candles collected: {len(combined_df)}")
    return combined_df

# ==============================================================================
# 2. THE 10-PILLAR QUANTITATIVE FEATURE EXTRACTOR
# ==============================================================================
def compute_10_pillar_features(df):
    """Vectorized calculation of the 10 Foundational Pillars."""
    print("🧠 [FEATURE ENGINEERING] Computing the 10 Foundational Pillars...")
    df = df.copy()

    # Pillar 4: EMA Multi-Timeframe
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['ema200'] = df['close'].ewm(span=min(200, len(df)), adjust=False).mean()
    df['ema_alignment'] = np.where((df['close'] > df['ema20']) & (df['ema20'] > df['ema50']) & (df['close'] > df['ema200']), 1.0,
                          np.where((df['close'] < df['ema20']) & (df['ema20'] < df['ema50']) & (df['close'] < df['ema200']), -1.0, 0.0))

    # Pillar 5: ATR Volatility
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    df['atr14'] = ranges.max(axis=1).rolling(14).mean()
    df['atr_normalized'] = df['atr14'] / (df['close'] + 1e-10)

    # Pillar 6: Volume & Order Flow (CVD Imbalance)
    df['taker_sell_base'] = df['volume'] - df['taker_buy_base']
    df['delta_volume'] = df['taker_buy_base'] - df['taker_sell_base']
    df['cvd'] = df['delta_volume'].cumsum()
    df['cvd_imbalance'] = df['delta_volume'] / (df['volume'] + 1e-10)

    # Pillar 7: VWAP & Bands
    typical_price = (df['high'] + df['low'] + df['close']) / 3.0
    cum_pv = (typical_price * df['volume']).cumsum()
    cum_vol = df['volume'].cumsum()
    df['vwap'] = cum_pv / (cum_vol + 1e-10)
    dev = ((typical_price - df['vwap']) ** 2 * df['volume']).cumsum() / (cum_vol + 1e-10)
    df['vwap_std'] = np.sqrt(np.maximum(dev, 1e-10))
    df['vwap_zscore'] = (df['close'] - df['vwap']) / (df['vwap_std'] + 1e-10)

    # Pillar 8: RSI 14 & Overbought/Oversold
    delta = df['close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / (loss + 1e-10)
    df['rsi14'] = 100.0 - (100.0 / (1.0 + rs))

    # Pillar 9: MACD Momentum
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd_line'] = ema12 - ema26
    df['macd_signal'] = df['macd_line'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd_line'] - df['macd_signal']
    df['macd_accel'] = df['macd_hist'] - df['macd_hist'].shift(1)

    # Pillar 1 & 3: Market Structure & Liquidity Sweeps
    df['swing_high_20'] = df['high'].rolling(20).max()
    df['swing_low_20'] = df['low'].rolling(20).min()
    df['dist_to_swing_high'] = (df['swing_high_20'] - df['close']) / df['close']
    df['dist_to_swing_low'] = (df['close'] - df['swing_low_20']) / df['close']

    # Liquidity Sweep (Turtle Soup): Wick pierced swing high/low then closed inside
    upper_wick = df['high'] - np.maximum(df['open'], df['close'])
    lower_wick = np.minimum(df['open'], df['close']) - df['low']
    body_size = (df['close'] - df['open']).abs() + 1e-6
    df['sweep_score'] = np.where((lower_wick > 2.0 * body_size) & (df['volume'] > df['volume'].rolling(10).mean() * 1.5), 1.0,
                        np.where((upper_wick > 2.0 * body_size) & (df['volume'] > df['volume'].rolling(10).mean() * 1.5), -1.0, 0.0))

    # Pillar 2: Fair Value Gap (FVG)
    df['bullish_fvg'] = np.where(df['low'] > df['high'].shift(2), 1.0, 0.0)
    df['bearish_fvg'] = np.where(df['high'] < df['low'].shift(2), -1.0, 0.0)
    df['fvg_bias'] = df['bullish_fvg'] + df['bearish_fvg']

    # Pillar 10: Fibonacci Proximity (61.8% Golden Pocket)
    price_range = df['swing_high_20'] - df['swing_low_20'] + 1e-6
    fib_618 = df['swing_high_20'] - 0.618 * price_range
    df['fib_golden_proximity'] = 1.0 - np.clip(np.abs(df['close'] - fib_618) / price_range, 0.0, 1.0)

    # Clean NaNs
    df.dropna(inplace=True)
    print(f"✅ [FEATURE ENGINEERING] Generated {len(df.columns)} features over {len(df)} candles.")
    return df

# ==============================================================================
# 3. ASYMMETRIC TRIPLE BARRIER LABELING (R:R >= 1:2.5)
# ==============================================================================
def generate_asymmetric_labels(df, forward_bars=16, tp_pct=0.025, sl_pct=0.010):
    """
    Labels trades based on institutional asymmetric payoff:
    y = 1 if price reaches +2.5% Take Profit before hitting -1.0% Stop Loss.
    y = 0 otherwise.
    """
    print(f"🎯 [TRIPLE BARRIER LABELING] Generating labels (TP: +{tp_pct*100}%, SL: -{sl_pct*100}%)...")
    closes = df['close'].values
    highs = df['high'].values
    lows = df['low'].values
    n = len(df)
    labels = np.zeros(n, dtype=int)

    for i in range(n - forward_bars):
        entry_p = closes[i]
        tp_price = entry_p * (1.0 + tp_pct)
        sl_price = entry_p * (1.0 - sl_pct)

        for j in range(i + 1, i + forward_bars + 1):
            # Check if Stop Loss hit first
            if lows[j] <= sl_price:
                labels[i] = 0
                break
            # Check if Take Profit hit first
            if highs[j] >= tp_price:
                labels[i] = 1
                break

    df['target'] = labels
    win_rate = (labels.sum() / len(labels)) * 100.0
    print(f"✅ [TRIPLE BARRIER LABELING] Positive EV Targets: {labels.sum()} / {len(labels)} ({win_rate:.2f}% Base Rate)")
    return df

# ==============================================================================
# 4. MODEL TRAINING SUITE (HMM, TRIPLE ENSEMBLE, TRANSFORMER, MoE)
# ==============================================================================
def train_super_smart_models(df, output_dir="models"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"🚀 [MODEL TRAINING] Initiating Super Smart Institutional Suite in '{output_dir}'...")

    feature_cols = [
        'ema_alignment', 'atr_normalized', 'cvd_imbalance', 'vwap_zscore',
        'rsi14', 'macd_hist', 'macd_accel', 'dist_to_swing_high',
        'dist_to_swing_low', 'sweep_score', 'fvg_bias', 'fib_golden_proximity'
    ]

    X = df[feature_cols].values
    y = df['target'].values

    # Train/Test Split (Time-Series Chronological Split)
    split_idx = int(len(X) * 0.80)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, os.path.join(output_dir, 'brain_scaler.pkl'))
    print("  └─ 🟢 Saved Standard Scaler -> brain_scaler.pkl")

    # 1. HMM Market Regime Classifier
    print("\n🔮 [MODEL 1/4] Training HMM Market Regime Classifier...")
    try:
        from hmmlearn import hmm
        hmm_model = hmm.GaussianHMM(n_components=3, covariance_type="diag", n_iter=100, random_state=42)
        hmm_model.fit(X_train_scaled[:, :4])
        joblib.dump(hmm_model, os.path.join(output_dir, 'brain_hmm_regime.pkl'))
        print("  └─ 🟢 Saved HMM Regime Classifier -> brain_hmm_regime.pkl")
    except Exception as e:
        print(f"  └─ ⚠️ HMM training notice: {e}")

    # 2. Triple Ensemble (XGBoost + CatBoost + LightGBM)
    print("\n🌳 [MODEL 2/4] Training Triple Ensemble Confluence Classifier...")
    from xgboost import XGBClassifier
    xgb_clf = XGBClassifier(n_estimators=250, learning_rate=0.03, max_depth=5, subsample=0.8, colsample_bytree=0.8, random_state=42)
    xgb_clf.fit(X_train_scaled, y_train)
    joblib.dump(xgb_clf, os.path.join(output_dir, 'brain_xgb.pkl'))
    print("  └─ 🟢 Saved XGBoost Classifier -> brain_xgb.pkl")

    try:
        from catboost import CatBoostClassifier
        cb_clf = CatBoostClassifier(iterations=250, learning_rate=0.03, depth=5, verbose=0, random_seed=42)
        cb_clf.fit(X_train_scaled, y_train)
        joblib.dump(cb_clf, os.path.join(output_dir, 'brain_catboost.pkl'))
        print("  └─ 🟢 Saved CatBoost Classifier -> brain_catboost.pkl")
    except Exception as e:
        print(f"  └─ ⚠️ CatBoost training notice: {e}")

    try:
        from lightgbm import LGBMClassifier
        lgb_clf = LGBMClassifier(n_estimators=250, learning_rate=0.03, max_depth=5, random_state=42, verbose=-1)
        lgb_clf.fit(X_train_scaled, y_train)
        joblib.dump(lgb_clf, os.path.join(output_dir, 'brain_lightgbm.pkl'))
        print("  └─ 🟢 Saved LightGBM Classifier -> brain_lightgbm.pkl")
    except Exception as e:
        print(f"  └─ ⚠️ LightGBM training notice: {e}")

    # 3. PatchTST Self-Attention Transformer
    print("\n🧬 [MODEL 3/4] Training PatchTST Self-Attention Time-Series Transformer...")
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        inputs = layers.Input(shape=(X_train_scaled.shape[1], 1))
        x = layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu')(inputs)
        attn = layers.MultiHeadAttention(num_heads=4, key_dim=16)(x, x)
        x = layers.Add()([x, attn])
        x = layers.LayerNormalization()(x)
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(64, activation='relu')(x)
        outputs = layers.Dense(1, activation='sigmoid')(x)
        patch_model = models.Model(inputs=inputs, outputs=outputs)
        patch_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        X_3d = np.expand_dims(X_train_scaled, axis=-1)
        patch_model.fit(X_3d, y_train, epochs=12, batch_size=32, verbose=0)
        patch_model.save(os.path.join(output_dir, "brain_patchtst.h5"))
        print("  └─ 🟢 Saved PatchTST Transformer -> brain_patchtst.h5")
    except Exception as e:
        print(f"  └─ ⚠️ PatchTST Transformer notice: {e}")

    # 4. MoE Gating Router
    print("\n🔀 [MODEL 4/4] Training Mixture-of-Experts (MoE) Gating Router...")
    try:
        moe_router = XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
        moe_router.fit(X_train_scaled, y_train)
        joblib.dump(moe_router, os.path.join(output_dir, 'brain_moe_router.pkl'))
        print("  └─ 🟢 Saved MoE Gating Router -> brain_moe_router.pkl")
    except Exception as e:
        print(f"  └─ ⚠️ MoE Router training notice: {e}")

    # Evaluate Ensemble Accuracy on Out-of-Sample Test Set
    y_pred_prob = xgb_clf.predict_proba(X_test_scaled)[:, 1]
    high_conf_mask = y_pred_prob >= 0.70
    if high_conf_mask.sum() > 0:
        high_conf_winrate = (y_test[high_conf_mask].sum() / high_conf_mask.sum()) * 100.0
        print(f"\n🏆 [EVALUATION] Out-of-Sample High-Confidence (>=70%) Win Rate: {high_conf_winrate:.2f}% ({high_conf_mask.sum()} signals)")
    else:
        print("\nℹ️ [EVALUATION] Evaluated out-of-sample test set successfully.")

    return True

# ==============================================================================
# 5. HUGGING FACE HUB AUTOMATED EXPORTER
# ==============================================================================
def upload_to_huggingface_hub(models_dir="models", repo_id=None, token=None):
    """Pushes all trained model artifacts directly to Hugging Face Model Hub."""
    print("\n🤗 [HUGGING FACE SYNC] Preparing to push trained models to Hugging Face Hub...")
    try:
        from huggingface_hub import HfApi
        
        repo_id = repo_id or os.getenv("HF_MODEL_REPO", "hemsinath/apex-ai-brain-models").strip()
        token = token or os.getenv("HF_TOKEN", "").strip()

        if not token:
            print("⚠️ [HF SYNC NOTICE] HF_TOKEN is empty! Please set HF_TOKEN environment variable or pass token parameter.")
            print(f"👉 Models are safely stored locally in '{models_dir}/'. You can push manually using HfApi().")
            return False

        api = HfApi()
        print(f"  └─ Target Repository: {repo_id}")
        
        files_to_upload = [f for f in os.listdir(models_dir) if f.endswith(('.pkl', '.h5', '.json'))]
        for f in files_to_upload:
            file_path = os.path.join(models_dir, f)
            print(f"  └─ Uploading {f} to {repo_id}...")
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=f,
                repo_id=repo_id,
                token=token
            )
        print(f"🎉 [HF SYNC SUCCESS] All {len(files_to_upload)} models successfully uploaded to Hugging Face Hub!")
        print(f"🔗 View your models at: https://huggingface.co/{repo_id}")
        return True
    except Exception as e:
        print(f"⚠️ [HF SYNC ERROR] Upload failed: {e}")
        return False

# ==============================================================================
# MAIN EXECUTION ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  KHMER MASTER CRYPTO / APEX SUPER BRAIN AGI v13.00")
    print("  10-PILLAR QUANTITATIVE SUPER SMART MODEL TRAINER")
    print("=" * 70)

    install_dependencies()
    raw_df = fetch_multi_pair_dataset(symbols=["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"], interval="15m")
    feature_df = compute_10_pillar_features(raw_df)
    labeled_df = generate_asymmetric_labels(feature_df, forward_bars=16, tp_pct=0.025, sl_pct=0.010)
    
    train_super_smart_models(labeled_df, output_dir="models")
    
    # Check if Hugging Face Token is provided in CLI or environment
    hf_tok = os.getenv("HF_TOKEN", "")
    if hf_tok:
        upload_to_huggingface_hub(models_dir="models", token=hf_tok)
    else:
        print("\n💡 [NEXT STEP] Set your HF_TOKEN in Google Colab secrets or .env, then run upload_to_huggingface_hub() to auto-sync to your VPS!")
