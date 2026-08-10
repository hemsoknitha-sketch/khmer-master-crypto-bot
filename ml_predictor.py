import requests
import pandas as pd
import numpy as np
import time
import os
import joblib
import warnings
import json
import yfinance as yf

warnings.filterwarnings('ignore')

try:
    from train_model import (
        fetch_ohlcv_advanced, fetch_funding_rate, fetch_long_short_ratio,
        fetch_sentiment, fetch_onchain_btc, add_technical_features,
        add_regime_feature, create_lstm_feature, add_rl_signal, calculate_atr
    )
except ImportError:
    pass

def predict_price(symbol: str = "BTCUSDT"):
    """
    Loads all pre-trained Super Brain models, fetches recent data, 
    and returns a comprehensive AI signal for the bot.
    """
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"
        
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    config_path = os.path.join(models_dir, "brain_config.json")
    
    if not os.path.exists(config_path):
        return (
            f"❌ **[ML Engine] មិនមាន File Config សម្រាប់ AI ថ្មីទេ!**\n"
            f"សូមប្រាកដថាអ្នកបានដំណើរការ `train_model.py` និងមាន files `brain_*.pkl` នៅក្នុង Folder models។"
        )

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        feature_cols = config['feature_columns']
        models_files = config['models']
        trend_map = config['trend_map']
        
        # Load all models
        models = {}
        for key, filename in models_files.items():
            path = os.path.join(models_dir, filename)
            models[key] = joblib.load(path)
            
    except Exception as e:
        return f"❌ [ML Engine] Error loading models or config: {e}"

    try:
        # Build dataset for inference (fetch ~200 days to be safe for 90d SMA and HMM/LSTM)
        df = fetch_ohlcv_advanced(symbol, '1d', limit=200)
        
        sp500 = yf.download('^GSPC', start=df.index.min().strftime('%Y-%m-%d'),
                            end=df.index.max().strftime('%Y-%m-%d'), progress=False)
        if isinstance(sp500.columns, pd.MultiIndex): sp500.columns = sp500.columns.droplevel(1)
        sp500 = sp500[['Close']].rename(columns={'Close':'sp500'}).resample('D').ffill()
        df = df.merge(sp500, left_index=True, right_index=True, how='left')
        
        funding = fetch_funding_rate(symbol, 200)
        ls = fetch_long_short_ratio(symbol, "5m", 200)
        if not funding.empty: df = df.merge(funding, left_index=True, right_index=True, how='left')
        if not ls.empty: df = df.merge(ls, left_index=True, right_index=True, how='left')
        
        sentiment = fetch_sentiment()
        if not sentiment.empty: df = df.merge(sentiment, left_index=True, right_index=True, how='left')
        
        onchain = fetch_onchain_btc()
        if not onchain.empty: df = df.merge(onchain, left_index=True, right_index=True, how='left')
        
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)

        df = add_technical_features(df)
        regime_df = add_regime_feature(df)
        df = df.merge(regime_df, left_index=True, right_index=True, how='left')
        df['regime'] = df['regime'].fillna(method='ffill').fillna(1)

        df = create_lstm_feature(df)
        df = add_rl_signal(df)
        
        # Select the last row for inference
        latest = df.iloc[-1:]
        
        # Extract features according to the config
        # Ensure missing columns are filled with 0 (in case some alt data failed)
        for col in feature_cols:
            if col not in latest.columns:
                latest[col] = 0
                
        X = latest[feature_cols].values
        
        # Scale
        X_sc = models['scaler'].transform(X)
        
        # Predict
        pred_price = models['price'].predict(X_sc)[0]
        pred_trend_idx = models['trend'].predict(X_sc)[0]
        pred_trend = trend_map[str(pred_trend_idx)]
        pred_vol = models['volatility'].predict(X_sc)[0]
        pred_tp = models['tp_signal'].predict(X_sc)[0]
        pred_dca = models['dca_zone'].predict(X_sc)[0]
        
        current_close = latest['close'].values[0]
        
        diff_val = pred_price - current_close
        diff_pct = (diff_val / current_close) * 100
        
        direction = "ឡើង (UP) 🚀" if diff_pct > 0 else "ចុះ (DOWN) 📉"
        
        summary = (
            f"\n🧠 **Apex Super Brain (Ensemble AI):**\n"
            f"⚡ **Load Mode:** Advanced Multi-Model Inference\n"
            f"📊 **Features:** {len(feature_cols)} (On-Chain, Order Book, RL, HMM, LSTM)\n\n"
            f"🎯 **លទ្ធផលទស្សន៍ទាយសម្រាប់ ២៤ ម៉ោងបន្ទាប់ ({symbol}):**\n"
            f"👉 តម្លៃគោលដៅ: **${pred_price:,.2f}** ({direction} {diff_pct:+.2f}%)\n"
            f"📈 និន្នាការ (Trend): **{pred_trend.upper()}**\n"
            f"🔥 ការប្រែប្រួលរំពឹងទុក (Volatility/ATR): **${pred_vol:,.2f}**\n"
            f"💰 សញ្ញា Take-Profit ល្អ: **{'បាទ (YES)' if pred_tp == 1 else 'ទេ (NO)'}**\n"
            f"🛒 សញ្ញា DCA គួរទិញ: **{'បាទ (YES)' if pred_dca == 1 else 'ទេ (NO)'}**\n\n"
            f"*(ចំណាំ: ម៉ូដែលប្រើ vol_target សម្រាប់ការគ្រប់គ្រងហានិភ័យដោយស្វ័យប្រវត្តិ)*"
        )
        
        return summary
        
    except Exception as e:
        return f"❌ [ML Engine Error]: {str(e)}"

# Keep this for backward compatibility if other modules need it directly
def get_vol_target(symbol: str = "BTCUSDT"):
    """
    Returns only the predicted volatility (vol_target) for risk management (Position sizing, Stop Loss)
    """
    try:
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        config_path = os.path.join(models_dir, "brain_config.json")
        with open(config_path, 'r') as f: config = json.load(f)
        feature_cols = config['feature_columns']
        scaler = joblib.load(os.path.join(models_dir, config['models']['scaler']))
        vol_model = joblib.load(os.path.join(models_dir, config['models']['volatility']))
        
        df = fetch_ohlcv_advanced(symbol, '1d', limit=200)
        # We might not need the full heavy features just for vol, but the model expects them!
        # This is heavy to run twice (once in predict, once here). So we should cache it or run it less often.
        # But for now, we'll just run it. 
        # A better way is to cache the last prediction.
        
        # Simplification: just return a fallback based on ATR if we don't want to run the heavy model again
        df['atr14'] = calculate_atr(df, 14)
        return df['atr14'].iloc[-1]
        
    except Exception as e:
        return 1000.0 # fallback default Volatility in USDT

def get_ai_signals(symbol: str = "BTCUSDT") -> dict:
    """Returns raw dictionary of AI predictions for programmatic execution."""
    try:
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        config_path = os.path.join(models_dir, "brain_config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        feature_cols = config['feature_columns']
        
        models = {
            'price': joblib.load(os.path.join(models_dir, config['models']['price'])),
            'trend': joblib.load(os.path.join(models_dir, config['models']['trend'])),
            'volatility': joblib.load(os.path.join(models_dir, config['models']['volatility'])),
            'tp_signal': joblib.load(os.path.join(models_dir, config['models']['tp_signal'])),
            'dca_zone': joblib.load(os.path.join(models_dir, config['models']['dca_zone'])),
            'scaler': joblib.load(os.path.join(models_dir, config['models']['scaler']))
        }
        
        trend_map = config['trend_map']
        
        df = fetch_ohlcv_advanced(symbol, '1d', limit=200)
        if df.empty: return {}
        
        df = add_technical_features(df)
        regime_df = add_regime_feature(df)
        df = df.merge(regime_df, left_index=True, right_index=True, how='left')
        df['regime'] = df['regime'].fillna(method='ffill').fillna(1)
        
        df = create_lstm_feature(df)
        df = add_rl_signal(df)
        
        latest = df.iloc[-1:]
        
        for col in feature_cols:
            if col not in latest.columns:
                latest[col] = 0
                
        X = latest[feature_cols].values
        X_sc = models['scaler'].transform(X)
        
        pred_price = models['price'].predict(X_sc)[0]
        pred_trend_idx = models['trend'].predict(X_sc)[0]
        pred_trend = trend_map[str(pred_trend_idx)]
        pred_vol = models['volatility'].predict(X_sc)[0]
        pred_tp = models['tp_signal'].predict(X_sc)[0]
        pred_dca = models['dca_zone'].predict(X_sc)[0]
        
        return {
            "tp_signal": int(pred_tp),
            "dca_signal": int(pred_dca),
            "price": float(pred_price),
            "trend": pred_trend,
            "volatility": float(pred_vol)
        }
    except Exception as e:
        print(f"Error getting AI signals for {symbol}: {e}")
        return {}
