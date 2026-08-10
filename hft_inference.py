import os
import time
import requests
import warnings
warnings.filterwarnings("ignore", module="hmmlearn")

import joblib
import pandas as pd
import numpy as np
import json
import asyncio
import threading
from pathlib import Path
import websocket_engine
import ml_predictor
import concurrent.futures

PREFETCH_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=2)

class BatchAIPredictor:
    def __init__(self):
        self.models = {}
        self.feature_cols = []
        self.trend_map = {}
        self.features_cache = {}  # { symbol: dict_of_features }
        self.prefetch_threads = {}
        self.failed_prefetch = {}
        self._load_models()
        
    def _load_models(self):
        models_dir = Path(os.path.dirname(__file__)) / "models"
        config_path = models_dir / "brain_config.json"
        
        if not config_path.exists():
            print("❌ [HFT Engine] brain_config.json not found! Cannot initialize HFT Engine.")
            return
            
        print("🧠 [HFT Engine] Pre-loading ML Models into RAM...")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            self.feature_cols = config['feature_columns']
            self.trend_map = config['trend_map']
            models_files = config['models']
            
            for key, filename in models_files.items():
                path = models_dir / filename
                self.models[key] = joblib.load(path)
                
            print(f"✅ [HFT Engine] Loaded {len(self.models)} models into RAM.")
        except Exception as e:
            print(f"❌ [HFT Engine] Failed to load models: {e}")

    def _fetch_historical_worker(self, symbol: str):
        try:
            from train_model import (
                fetch_ohlcv_advanced, fetch_funding_rate, fetch_long_short_ratio,
                fetch_sentiment, fetch_onchain_btc, add_technical_features,
                add_regime_feature, create_lstm_feature, add_rl_signal
            )
            import yfinance as yf
            
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
            
            if df.empty or len(df) == 0:
                raise ValueError("DataFrame is empty, not enough historical data.")
                
            latest = df.iloc[-1:]
            for col in self.feature_cols:
                if col not in latest.columns:
                    latest[col] = 0
                    
            self.features_cache[symbol] = latest[self.feature_cols].iloc[0].to_dict()
            print(f"✅ [HFT Engine] Cached baseline features for {symbol}")
        except Exception as e:
            err_msg = str(e)
            if "fetch_ohlcv_advanced" not in err_msg and "DLL load failed" not in err_msg:
                if "DataFrame is empty" in err_msg:
                    print(f"⚠️ [HFT Engine] Skipped {symbol} (Delisted or No Data).")
                else:
                    print(f"⚠️ [HFT Engine] Failed to pre-fetch features for {symbol}: {err_msg.split(chr(10))[0]}")
            import time
            self.failed_prefetch[symbol] = time.time()
        finally:
            self.prefetch_threads.pop(symbol, None)

    def trigger_prefetch(self, symbol: str):
        import time
        if symbol in self.failed_prefetch:
            if time.time() - self.failed_prefetch[symbol] < 3600:
                return
                
        if symbol not in self.features_cache and symbol not in self.prefetch_threads:
            self.prefetch_threads[symbol] = True
            PREFETCH_POOL.submit(self._fetch_historical_worker, symbol)

    def predict_batch(self, symbols: list) -> dict:
        """
        Predicts signals for a batch of symbols instantly using WebSockets + RAM.
        Returns: { 'BTCUSDT': {'tp_signal': True}, ... }
        """
        results = {}
        if not self.models:
            return results
            
        scaler = self.models.get('scaler')
        tp_model = self.models.get('tp_signal')
        
        if not scaler or not tp_model:
            return results
        
        for symbol in symbols:
            results[symbol] = {'tp_signal': False}
            
            if symbol not in self.features_cache:
                self.trigger_prefetch(symbol)
                continue
                
            raw_features = self.features_cache.get(symbol).copy()
            fast_price = websocket_engine.get_fast_price(symbol)
            
            if fast_price > 0:
                raw_features['close'] = fast_price
                
            X_raw = np.array([raw_features[col] for col in self.feature_cols]).reshape(1, -1)
            
            try:
                X_sc = scaler.transform(X_raw)
                pred_tp = tp_model.predict(X_sc)[0]
                tp_signal = bool(pred_tp == 1)
                
                # --- Order Book Imbalance Override ---
                import orderbook_engine
                imbalance = orderbook_engine.get_imbalance(symbol)
                
                if imbalance < 0.2:
                    # Emergency Exit: Sell Wall is 5x bigger than Buy Wall
                    print(f"⚠️ [OrderBook] Emergency Exit Override for {symbol}! Massive Sell Wall (Ratio: {imbalance:.2f})")
                    tp_signal = True
                elif imbalance > 5.0 and tp_signal:
                    # Profit Maximizer: AI says sell, but Buy Wall is 5x bigger than Sell Wall
                    print(f"🚀 [OrderBook] Profit Maximizer Override for {symbol}! Canceling Sell due to Massive Buy Wall (Ratio: {imbalance:.2f})")
                    tp_signal = False
                    
                results[symbol]['tp_signal'] = tp_signal
            except Exception:
                pass
                
        return results

# Global Singleton
hft_predictor = BatchAIPredictor()
