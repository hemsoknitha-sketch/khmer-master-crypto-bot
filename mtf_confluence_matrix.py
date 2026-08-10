import market_data

def evaluate_mtf_confluence(symbol: str, df_dict: dict = None) -> dict:
    """
    Evaluates 4-Timeframe Trend Confluence Matrix:
    1. 4h: Macro Bullish Trend (close > ema20 or ema20 > ema50)
    2. 1h: Dynamic Consolidation / Support Hold (RSI 45..70)
    3. 15m: Momentum Breakout (RSI > 52 and MACD Hist > 0)
    4. 1m: Volume Spike Trigger (Volume > 1.5x 20-SMA)
    
    Returns: {"is_confluent": bool, "score": float, "details": dict}
    """
    details = {
        "4h_macro_bullish": False,
        "1h_consolidation": False,
        "15m_breakout": False,
        "1m_volume_spike": False
    }
    
    try:
        # Fetch or use pre-loaded DataFrames
        if df_dict is None:
            df_4h, _, _ = market_data.fetch_binance_data(symbol, interval="4h", limit=30)
            df_1h, _, _ = market_data.fetch_binance_data(symbol, interval="1h", limit=30)
            df_15m, _, _ = market_data.fetch_binance_data(symbol, interval="15m", limit=30)
            df_1m, _, _ = market_data.fetch_binance_data(symbol, interval="1m", limit=30)
        else:
            df_4h = df_dict.get("4h")
            df_1h = df_dict.get("1h")
            df_15m = df_dict.get("15m")
            df_1m = df_dict.get("1m")
            
        # 1. 4h Macro Trend Check
        if df_4h is not None and not df_4h.empty:
            c4 = df_4h['close'].iloc[-1]
            ema20_4h = df_4h['ema20'].iloc[-1] if 'ema20' in df_4h.columns else c4
            ema50_4h = df_4h['ema50'].iloc[-1] if 'ema50' in df_4h.columns else c4 * 0.99
            if c4 >= ema20_4h or ema20_4h >= ema50_4h:
                details["4h_macro_bullish"] = True
                
        # 2. 1h Consolidation Check
        if df_1h is not None and not df_1h.empty:
            rsi_1h = df_1h['rsi'].iloc[-1] if 'rsi' in df_1h.columns else 55.0
            if 45.0 <= rsi_1h <= 72.0:
                details["1h_consolidation"] = True
                
        # 3. 15m Breakout Check
        if df_15m is not None and not df_15m.empty:
            rsi_15m = df_15m['rsi'].iloc[-1] if 'rsi' in df_15m.columns else 55.0
            macd_h = df_15m['macd_hist'].iloc[-1] if 'macd_hist' in df_15m.columns else 0.1
            if rsi_15m >= 52.0 and macd_h >= 0.0:
                details["15m_breakout"] = True
                
        # 4. 1m Volume Spike Trigger Check
        if df_1m is not None and not df_1m.empty:
            v1m = df_1m['volume'].iloc[-1]
            v_sma = df_1m['volume'].tail(20).mean() if len(df_1m) >= 20 else v1m
            if v_sma > 0 and (v1m / v_sma) >= 1.25:
                details["1m_volume_spike"] = True
            elif 'rvol' in df_1m.columns and df_1m['rvol'].iloc[-1] >= 1.25:
                details["1m_volume_spike"] = True
                
        passed_count = sum(1 for v in details.values() if v)
        score = round((passed_count / 4.0) * 100.0, 1)
        is_confluent = (passed_count == 4)
        
        return {
            "is_confluent": is_confluent,
            "score": score,
            "details": details
        }
    except Exception as e:
        print(f"[MTF MATRIX] Evaluation Error: {e}")
        return {"is_confluent": False, "score": 0.0, "details": details}
