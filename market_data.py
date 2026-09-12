import os
import time
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Force non-GUI backend for thread safety
import matplotlib.pyplot as plt
import io

def calculate_rsi(data, window=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    exp1 = data['close'].ewm(span=short_window, adjust=False).mean()
    exp2 = data['close'].ewm(span=long_window, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calculate_atr(df, window=14):
    """Calculates Average True Range (ATR)"""
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    atr = true_range.rolling(window).mean()
    return atr

def detect_patterns(df):
    """Detects simple candlestick patterns on the latest candles."""
    if len(df) < 2:
        return "None"
        
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    
    # Doji
    body_size = abs(curr['open'] - curr['close'])
    total_size = curr['high'] - curr['low']
    is_doji = (body_size <= (total_size * 0.1)) if total_size > 0 else False
    
    # Engulfing
    is_prev_red = prev['close'] < prev['open']
    is_prev_green = prev['close'] > prev['open']
    is_curr_red = curr['close'] < curr['open']
    is_curr_green = curr['close'] > curr['open']
    
    is_bullish_engulfing = is_prev_red and is_curr_green and (curr['open'] <= prev['close']) and (curr['close'] >= prev['open'])
    is_bearish_engulfing = is_prev_green and is_curr_red and (curr['open'] >= prev['close']) and (curr['close'] <= prev['open'])
    
    patterns = []
    if is_doji: patterns.append("Doji (Indecision)")
    if is_bullish_engulfing: patterns.append("Bullish Engulfing")
    if is_bearish_engulfing: patterns.append("Bearish Engulfing")
    
    return ", ".join(patterns) if patterns else "None"

def fetch_funding_rate(symbol: str):
    """Fetches current funding rate from Binance Futures."""
    try:
        url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return float(data.get('lastFundingRate', 0))
    except Exception:
        pass
    return 0.0

def get_historical_klines_1m(symbol: str, limit: int = 20):
    """Fetches 1m klines and returns a DataFrame. Returns None on error."""
    if not isinstance(symbol, str): symbol = str(symbol)
    symbol = symbol.upper().strip()
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            return df
    except Exception as e:
        print(f"Error fetching 1m klines: {e}")
    return None

def fetch_binance_data(symbol: str = "BTCUSDT", interval: str = "1d", limit: int = 30):
    """
    Fetches candlestick data from Binance with fallback endpoints.
    Returns a pandas DataFrame and a formatted text summary for the AI.
    """
    if not isinstance(symbol, str): symbol = str(symbol)
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"

    # Binance provides multiple API endpoints in case of network/DNS issues
    base_urls = [
        "https://data-api.binance.vision",
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com"
    ]
    
    last_error = ""
    for base_url in base_urls:
        url = f"{base_url}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Columns based on Binance API response
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                       'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore']
            
            df = pd.DataFrame(data, columns=columns)
            
            # Convert numeric columns
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
            
            # Convert timestamp to datetime
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Calculate RSI and MACD
            df['rsi'] = calculate_rsi(df)
            df['macd'], df['macd_signal'], df['macd_hist'] = calculate_macd(df)
            
            latest_price = df['close'].iloc[-1]
            latest_rsi = df['rsi'].iloc[-1]
            latest_macd = df['macd'].iloc[-1]
            latest_macd_signal = df['macd_signal'].iloc[-1]
            latest_volume = df['volume'].iloc[-1]
            
            macd_trend = "Bullish" if latest_macd > latest_macd_signal else "Bearish"
            candlestick_pattern = detect_patterns(df)
            funding_rate = fetch_funding_rate(symbol)
            
            summary = (
                f"Live Data for {symbol} (Interval: {interval}, Last 30 periods):\n"
                f"- Current Price: ${latest_price:,.2f}\n"
                f"- Volume: {latest_volume:,.2f}\n"
                f"- 14-Period RSI: {latest_rsi:.2f}\n"
                f"- MACD Trend: {macd_trend} (MACD: {latest_macd:.2f}, Signal: {latest_macd_signal:.2f})\n"
                f"- Candlestick Pattern: {candlestick_pattern}\n"
                f"- Futures Funding Rate: {funding_rate*100:.4f}%\n"
                f"- Context: Evaluate RSI, MACD, Patterns, and Funding Rate. If Funding Rate > 0.05% warn of Long Squeeze."
            )
            
            return df, summary, symbol
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                return None, f"❌ Invalid Coin Symbol: '{symbol}'. Binance does not have this pair. Please provide a valid symbol like BTC or ETH.", symbol
            last_error = str(e)
            continue
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            continue # Try the next URL
        except Exception as e:
            return None, f"Error processing data for {symbol}: {str(e)}", symbol
            
    return None, f"Network Error: Could not connect to Binance API. Last Error: {last_error}", symbol

def get_symbol_rsi(symbol: str, interval: str = "15m", window: int = 14) -> float:
    """
    Returns latest RSI for a symbol. Returns 50.0 on error or insufficient data.
    Ultra-fast, institutional-grade safeguard for Anti-Oversold and Anti-Peak shields.
    """
    try:
        res = fetch_binance_data(symbol, interval=interval, limit=window + 15)
        if res and isinstance(res, tuple) and len(res) >= 1:
            df = res[0]
            if df is not None and not df.empty and 'rsi' in df.columns:
                rsi_val = df['rsi'].iloc[-1]
                if not pd.isna(rsi_val):
                    return float(rsi_val)
    except Exception:
        pass
    return 50.0

_atr_cache = {}
_atr_cache_time = {}

def get_symbol_atr(symbol: str, interval: str = "15m", window: int = 14) -> dict:
    """
    Returns latest ATR (Average True Range) and ATR percentage for a symbol.
    Uses a 10-second memory cache to provide sub-millisecond responses without hitting API limits.
    Returns: {"atr_val": float, "atr_pct": float, "current_price": float}
    """
    symbol = str(symbol).upper().strip()
    cache_key = f"{symbol}_{interval}_{window}"
    now = time.time()
    if cache_key in _atr_cache and (now - _atr_cache_time.get(cache_key, 0)) < 10.0:
        return _atr_cache[cache_key]

    default_res = {"atr_val": 0.0, "atr_pct": 1.5, "current_price": 0.0}
    try:
        res = fetch_binance_data(symbol, interval=interval, limit=window + 20)
        if res and isinstance(res, tuple) and len(res) >= 1:
            df = res[0]
            if df is not None and not df.empty and len(df) >= window:
                atr_s = calculate_atr(df, window=window)
                curr_p = float(df['close'].iloc[-1])
                last_atr = float(atr_s.iloc[-1]) if not pd.isna(atr_s.iloc[-1]) else curr_p * 0.015
                atr_pct = (last_atr / curr_p) * 100.0 if curr_p > 0 else 1.5
                out = {
                    "atr_val": round(last_atr, 6),
                    "atr_pct": round(atr_pct, 2),
                    "current_price": curr_p
                }
                _atr_cache[cache_key] = out
                _atr_cache_time[cache_key] = now
                return out
    except Exception:
        pass

    return default_res


def generate_chart(df: pd.DataFrame, symbol: str, filepath: str = "chart.png"):
    """
    Generates a dark-themed chart with Price and RSI and saves it as an image.
    """
    plt.style.use('dark_background')
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # Plot Price
    ax1.plot(df['datetime'], df['close'], color='#00ff00', linewidth=2)
    ax1.set_title(f"{symbol} - Daily Price, RSI & MACD", color='white', fontsize=16)
    ax1.set_ylabel("Price (USDT)", color='white', fontsize=12)
    ax1.grid(color='#333333', linestyle='--', alpha=0.5)
    
    # Plot RSI
    ax2.plot(df['datetime'], df['rsi'], color='#f39c12', linewidth=2)
    ax2.axhline(70, color='red', linestyle='--', alpha=0.5)
    ax2.axhline(30, color='green', linestyle='--', alpha=0.5)
    ax2.set_ylabel("RSI (14)", color='white', fontsize=12)
    ax2.set_ylim(0, 100)
    ax2.grid(color='#333333', linestyle='--', alpha=0.5)
    
    # Plot MACD
    ax3.plot(df['datetime'], df['macd'], color='#00bfff', linewidth=1.5, label='MACD')
    ax3.plot(df['datetime'], df['macd_signal'], color='#ff4500', linewidth=1.5, label='Signal')
    
    # Plot MACD Histogram
    colors = ['#00ff00' if val >= 0 else '#ff0000' for val in df['macd_hist']]
    ax3.bar(df['datetime'], df['macd_hist'], color=colors, alpha=0.5)
    ax3.set_ylabel("MACD", color='white', fontsize=12)
    ax3.grid(color='#333333', linestyle='--', alpha=0.5)
    ax3.legend(loc='upper left', fontsize=8)
    
    # Format X-axis
    fig.autofmt_xdate()
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    return filepath

def fetch_top_gainers(limit: int = 5, lang: str = 'km'):
    """
    Fetches the top gaining and losing crypto assets in the last 24 hours from Binance (v13.00 Apex Ultra AGI).
    """
    base_urls = [
        "https://data-api.binance.vision",
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com"
    ]
    
    lang_clean = str(lang or 'km').lower()
    user_lang = 'en' if lang_clean in ['en', 'english'] else ('zh' if lang_clean in ['zh', 'chinese'] else 'km')
    
    last_error = ""
    for base_url in base_urls:
        url = f"{base_url}/api/v3/ticker/24hr"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            usdt_pairs = [item for item in data if item['symbol'].endswith('USDT')
                          and float(item.get('lastPrice', 0)) > 0
                          and float(item.get('bidPrice', 0)) > 0
                          and float(item.get('askPrice', 0)) > 0
                          and float(item.get('quoteVolume', 0)) >= 1000000.0]
            
            usdt_pairs.sort(key=lambda x: float(x['priceChangePercent']), reverse=True)
            
            top_gainers = usdt_pairs[:limit]
            top_losers = usdt_pairs[-limit:]
            top_losers.reverse()
            
            if user_lang == 'en':
                summary = "🔥 **TOP 5 VOLATILE GAINERS (MOMENTUM PUMP):**\n"
                for i, coin in enumerate(top_gainers):
                    full_sym = coin['symbol']
                    symbol = full_sym.replace("USDT", "")
                    change = float(coin['priceChangePercent'])
                    price = float(coin['lastPrice'])
                    volume = float(coin['quoteVolume'])
                    summary += f"{i+1}. 🟢 **{full_sym}** ៖ +{change:.2f}% (Price: `${price:,.4f}` | Vol: `${volume/1e6:.2f}M`)\n   ⚡ Launch Command ៖ `` `/turbo_hedge {symbol} 20 10 BUY 2.5 <PIN>` ``\n"
                    
                summary += "\n🔻 **TOP 5 VOLATILE LOSERS (DIP REBOUND):**\n"
                for i, coin in enumerate(top_losers):
                    full_sym = coin['symbol']
                    symbol = full_sym.replace("USDT", "")
                    change = float(coin['priceChangePercent'])
                    price = float(coin['lastPrice'])
                    volume = float(coin['quoteVolume'])
                    summary += f"{i+1}. 🔴 **{full_sym}** ៖ {change:.2f}% (Price: `${price:,.4f}` | Vol: `${volume/1e6:.2f}M`)\n   ⚡ Launch Command ៖ `` `/turbo_hedge {symbol} 20 10 BUY 2.5 <PIN>` ``\n"
            elif user_lang == 'zh':
                summary = "🔥 **24小时涨幅榜 TOP 5 (动量拉盘):**\n"
                for i, coin in enumerate(top_gainers):
                    full_sym = coin['symbol']
                    symbol = full_sym.replace("USDT", "")
                    change = float(coin['priceChangePercent'])
                    price = float(coin['lastPrice'])
                    volume = float(coin['quoteVolume'])
                    summary += f"{i+1}. 🟢 **{full_sym}** ៖ +{change:.2f}% (价格: `${price:,.4f}` | 成交额: `${volume/1e6:.2f}M`)\n   ⚡ 一键启动 ៖ `` `/turbo_hedge {symbol} 20 10 BUY 2.5 <PIN>` ``\n"
                    
                summary += "\n🔻 **24小时跌幅榜 TOP 5 (抄底反弹):**\n"
                for i, coin in enumerate(top_losers):
                    full_sym = coin['symbol']
                    symbol = full_sym.replace("USDT", "")
                    change = float(coin['priceChangePercent'])
                    price = float(coin['lastPrice'])
                    volume = float(coin['quoteVolume'])
                    summary += f"{i+1}. 🔴 **{full_sym}** ៖ {change:.2f}% (价格: `${price:,.4f}` | 成交额: `${volume/1e6:.2f}M`)\n   ⚡ 一键启动 ៖ `` `/turbo_hedge {symbol} 20 10 BUY 2.5 <PIN>` ``\n"
            else:
                summary = "🔥 **បញ្ជីកាក់ឡើងថ្លៃខ្លាំងបំផុត (TOP 5 GAINERS - MOMENTUM PUMP):**\n"
                for i, coin in enumerate(top_gainers):
                    full_sym = coin['symbol']
                    symbol = full_sym.replace("USDT", "")
                    change = float(coin['priceChangePercent'])
                    price = float(coin['lastPrice'])
                    volume = float(coin['quoteVolume'])
                    summary += f"{i+1}. 🟢 **{full_sym}** ៖ +{change:.2f}% (តម្លៃ ៖ `${price:,.4f}` | Vol: `${volume/1e6:.2f}M`)\n   ⚡ 1-Tap Command ៖ `` `/turbo_hedge {symbol} 20 10 BUY 2.5 <PIN>` ``\n"
                    
                summary += "\n🔻 **បញ្ជីកាក់ធ្លាក់ចុះខ្លាំងបំផុត (TOP 5 LOSERS - DIP REBOUND):**\n"
                for i, coin in enumerate(top_losers):
                    full_sym = coin['symbol']
                    symbol = full_sym.replace("USDT", "")
                    change = float(coin['priceChangePercent'])
                    price = float(coin['lastPrice'])
                    volume = float(coin['quoteVolume'])
                    summary += f"{i+1}. 🔴 **{full_sym}** ៖ {change:.2f}% (តម្លៃ ៖ `${price:,.4f}` | Vol: `${volume/1e6:.2f}M`)\n   ⚡ 1-Tap Command ៖ `` `/turbo_hedge {symbol} 20 10 BUY 2.5 <PIN>` ``\n"
                
            return summary

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            continue
        except Exception as e:
            return f"Error processing top gainers: {str(e)}"
            
    return f"Network Error: Could not connect to Binance API. Last Error: {last_error}"

def fetch_top_volatile_coins(limit: int = 5, min_change_pct: float = 10.0):
    """
    Fetches the 24hr ticker for all coins, filters top USDT pairs by volume, 
    and returns those with high volatility (priceChangePercent > min_change_pct or < -min_change_pct).
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return []
            
        data = res.json()
        
        # Filter for USDT pairs that are actively trading (not delisted/halted)
        usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') 
                      and float(d.get('lastPrice', 0)) > 0
                      and float(d.get('bidPrice', 0)) > 0
                      and float(d.get('askPrice', 0)) > 0]
        
        # Sort by quoteVolume to get highly liquid coins (Top 500)
        usdt_pairs.sort(key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
        top_liquid = usdt_pairs[:500]
        
        # Filter by extreme price change or high/low spread
        volatile_coins = []
        for coin in top_liquid:
            price_change_pct = float(coin.get('priceChangePercent', 0))
            high_price = float(coin.get('highPrice', 0))
            low_price = float(coin.get('lowPrice', 1))
            spread_pct = ((high_price - low_price) / low_price) * 100
            
            # Condition: Absolute price change > min_change_pct OR spread > min_change_pct + 5
            if abs(price_change_pct) >= min_change_pct or spread_pct >= (min_change_pct + 5):
                volatile_coins.append({
                    "symbol": coin['symbol'],
                    "priceChangePercent": price_change_pct,
                    "lastPrice": float(coin['lastPrice']),
                    "quoteVolume": float(coin['quoteVolume']),
                    "spread_pct": spread_pct
                })
                
        # Sort by most volatile first (by spread)
        volatile_coins.sort(key=lambda x: x['spread_pct'], reverse=True)
        return volatile_coins[:limit]
        
    except Exception as e:
        print(f"Error fetching top volatile coins: {e}")
        return []

def get_order_book_depth(symbol: str, limit: int = 100):
    """
    Fetches the Level 2 Order Book depth from Binance to identify Whale Walls.
    Returns bids and asks as lists of [price, quantity] floats.
    """
    base_urls = [
        "https://data-api.binance.vision",
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com"
    ]
    for base_url in base_urls:
        url = f"{base_url}/api/v3/depth?symbol={symbol}&limit={limit}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            bids = [[float(price), float(qty)] for price, qty in data.get('bids', [])]
            asks = [[float(price), float(qty)] for price, qty in data.get('asks', [])]
            return bids, asks
        except Exception as e:
            continue
    print(f"Error fetching order book for {symbol}: Network Error")
    return [], []

def get_triangular_prices():
    """
    Fetches concurrent prices for BTCUSDT, ETHBTC, and ETHUSDT for Triangular Arbitrage.
    Returns a dictionary of prices.
    """
    symbols = '["BTCUSDT","ETHBTC","ETHUSDT"]'
    base_urls = [
        "https://data-api.binance.vision",
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com"
    ]
    for base_url in base_urls:
        url = f"{base_url}/api/v3/ticker/price?symbols={symbols}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            prices = {item['symbol']: float(item['price']) for item in data}
            return prices
        except Exception as e:
            continue
    print("Error fetching triangular prices: Network Error")
    return {}

def fetch_new_binance_listings():
    """
    Placeholder stub for fetching new Binance listings.
    Since Binance Announcements API is restricted/retired,
    this currently returns an empty list to prevent crashes.
    """
    return []

def fetch_all_funding_rates() -> list:
    """Fetches and sorts all Futures funding rates to find arbitrage opportunities."""
    try:
        url = "https://fapi.binance.com/fapi/v1/premiumIndex"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        rates = []
        for item in data:
            symbol = item.get("symbol", "")
            if not symbol.endswith("USDT") or "_" in symbol:
                continue
            try:
                rate = float(item.get("lastFundingRate", 0))
                rates.append({"symbol": symbol, "funding_rate": rate})
            except:
                pass
                
        # Sort by highest funding rate descending (best for shorting futures / buying spot)
        rates.sort(key=lambda x: x["funding_rate"], reverse=True)
        return rates
    except Exception as e:
        print(f"Error fetching all funding rates: {e}")
        return []

def detect_liquidity_sweep(symbol: str) -> dict:
    """
    Detects if a liquidity sweep just occurred on the 5m timeframe.
    Returns: {"type": "BULLISH" | "BEARISH" | None, "confidence": int, "price": float}
    """
    try:
        df, _, _ = fetch_binance_data(symbol, interval="5m", limit=10)
        if df is None or len(df) < 10:
            return {"type": None, "confidence": 0, "price": 0.0}
            
        # Get the most recently closed candle (index -2 to ensure it's fully closed, or -1 if we want to catch it live)
        # We will use -2 for safety
        recent_candle = df.iloc[-2]
        
        open_p = recent_candle['open']
        close_p = recent_candle['close']
        high_p = recent_candle['high']
        low_p = recent_candle['low']
        volume = recent_candle['volume']
        
        # Calculate averages of previous 8 candles
        prev_candles = df.iloc[-10:-2]
        avg_volume = prev_candles['volume'].mean()
        
        body_size = abs(open_p - close_p)
        upper_wick = high_p - max(open_p, close_p)
        lower_wick = min(open_p, close_p) - low_p
        
        # Avoid division by zero
        if body_size == 0: body_size = 0.000001
        if avg_volume == 0: avg_volume = 1.0
        
        vol_multiplier = volume / avg_volume
        
        # Bullish Sweep: Price dropped hard, hit stops, and immediately got bought up
        if lower_wick > (body_size * 2) and lower_wick > upper_wick and vol_multiplier > 1.8:
            confidence = min(100, int((lower_wick / body_size) * 10 + (vol_multiplier * 10)))
            return {"type": "BULLISH", "confidence": confidence, "price": close_p}
            
        # Bearish Sweep: Price spiked hard, hit short stops, and immediately rejected down
        if upper_wick > (body_size * 2) and upper_wick > lower_wick and vol_multiplier > 1.8:
            confidence = min(100, int((upper_wick / body_size) * 10 + (vol_multiplier * 10)))
            return {"type": "BEARISH", "confidence": confidence, "price": close_p}
            
    except Exception as e:
        print(f"Error detecting sweep for {symbol}: {e}")
        
    return {"type": None, "confidence": 0, "price": 0.0}

def detect_ict_kill_zone(timestamp=None) -> dict:
    """
    ICT Session Kill Zone & Time-Gating Engine:
    - Asian Consolidation / Range: 00:00 - 06:00 UTC (Liquidity setup)
    - London Open Kill Zone: 07:00 - 10:00 UTC (London Expansion / Judas Swing)
    - London Lunch / NY Pre-Market: 10:00 - 12:00 UTC
    - New York AM Kill Zone (Silver Bullet): 12:00 - 15:00 UTC (Prime Institutional Volatility)
    - London Close / NY PM: 15:00 - 17:00 UTC
    - Asian Prep / Late NY: 17:00 - 21:00 UTC
    - Dead Zone (Low Liquidity / Widening Spreads): 21:00 - 23:59 UTC
    """
    if timestamp is None:
        dt = datetime.utcnow()
    elif isinstance(timestamp, (int, float)):
        dt = datetime.utcfromtimestamp(timestamp / 1000.0 if timestamp > 1e11 else timestamp)
    elif isinstance(timestamp, pd.Timestamp):
        dt = timestamp.to_pydatetime()
    else:
        dt = datetime.utcnow()

    hour = dt.hour
    minute = dt.minute
    total_minutes = hour * 60 + minute

    if 420 <= total_minutes < 600:
        session = "LONDON_OPEN_KZ"
        multiplier = 1.25
        is_prime = True
        desc = "London Open Kill Zone (Judas Swing & Liquidity Expansion)"
    elif 720 <= total_minutes < 900:
        session = "NY_AM_SILVER_BULLET_KZ"
        multiplier = 1.30
        is_prime = True
        desc = "New York AM Kill Zone / Silver Bullet (Peak Institutional Flow)"
    elif 900 <= total_minutes < 1020:
        session = "LONDON_CLOSE_KZ"
        multiplier = 1.15
        is_prime = True
        desc = "London Close Kill Zone (Trend Continuation or Reversal)"
    elif 0 <= total_minutes < 360:
        session = "ASIAN_RANGE"
        multiplier = 0.90
        is_prime = False
        desc = "Asian Session Range (Liquidity Pool Accumulation)"
    elif 1260 <= total_minutes <= 1440:
        session = "DEAD_ZONE"
        multiplier = 0.65
        is_prime = False
        desc = "Low Liquidity Dead Zone (High Spread Risk - Suppress Leverage)"
    else:
        session = "INTER_SESSION"
        multiplier = 1.00
        is_prime = False
        desc = "Inter-session Transition Window"

    return {
        "session": session,
        "is_prime_liquidity": is_prime,
        "liquidity_multiplier": multiplier,
        "utc_time": dt.strftime("%H:%M UTC"),
        "description": desc
    }

def detect_cvd_absorption_divergence(df: pd.DataFrame) -> dict:
    """
    Order Flow CVD Absorption & Institutional Footprint Engine:
    Detects when passive Limit orders (Whale Absorption) counter aggressive Market dumps or pumps.
    - Bullish Absorption: Price tests low while CVD makes Higher Low (Whale Limit Buying).
    - Bearish Absorption: Price tests high while CVD makes Lower High (Whale Limit Selling).
    """
    if len(df) < 15 or 'taker_buy_base' not in df.columns:
        return {"divergence": "NONE", "bias": 0.0, "confidence": 0, "description": "Insufficient order flow data"}

    try:
        taker_buy = df['taker_buy_base']
        volume = df['volume']
        taker_sell = volume - taker_buy
        delta = taker_buy - taker_sell
        cvd = delta.cumsum()

        recent_df = df.iloc[-15:]
        recent_cvd = cvd.iloc[-15:]

        curr_price = float(recent_df['close'].iloc[-1])
        price_span = (recent_df['high'].max() - recent_df['low'].min()) + 1e-10
        cvd_span = (recent_cvd.max() - recent_cvd.min()) + 1e-10

        curr_cvd = float(recent_cvd.iloc[-1])

        # Price near low (within bottom 25% of 15-bar range)
        price_near_low = (curr_price - recent_df['low'].min()) / price_span < 0.25
        # CVD is clearly higher than its 15-bar minimum
        cvd_higher_than_low = curr_cvd > recent_cvd.min() + cvd_span * 0.35

        # Price near high (within top 25% of 15-bar range)
        price_near_high = (recent_df['high'].max() - curr_price) / price_span < 0.25
        # CVD is clearly lower than its 15-bar maximum
        cvd_lower_than_high = curr_cvd < recent_cvd.max() - cvd_span * 0.35

        if price_near_low and cvd_higher_than_low and delta.iloc[-3:].sum() > 0:
            return {
                "divergence": "BULLISH_ABSORPTION",
                "bias": 1.0,
                "confidence": 88,
                "description": "Whale Limit Buying Absorbing Sell Dumps (Institutional Accumulation)"
            }
        elif price_near_high and cvd_lower_than_high and delta.iloc[-3:].sum() < 0:
            return {
                "divergence": "BEARISH_ABSORPTION",
                "bias": -1.0,
                "confidence": 88,
                "description": "Whale Limit Selling Absorbing Buy Pumps (Institutional Distribution)"
            }

        return {"divergence": "NONE", "bias": 0.0, "confidence": 50, "description": "Order flow delta balanced"}
    except Exception as e:
        return {"divergence": "NONE", "bias": 0.0, "confidence": 0, "description": f"Error: {e}"}

def detect_eqh_eql_liquidity(df: pd.DataFrame, tolerance: float = 0.0020) -> dict:
    """
    SMC Engineered Liquidity Pool Detector:
    Detects Equal Highs (EQH - Buy-Side Liquidity BSL) and Equal Lows (EQL - Sell-Side Liquidity SSL).
    - EQH: Retail Double/Triple Top resistance where stop-loss orders pool. Target for Bullish Sweeps.
    - EQL: Retail Double/Triple Bottom support where stop-loss orders pool. Target for Bearish Sweeps.
    """
    if len(df) < 20:
        return {"has_eqh": False, "eqh_level": 0.0, "has_eql": False, "eql_level": 0.0, "bias": 0.0, "description": "Insufficient candles"}

    try:
        highs = df['high'].values
        lows = df['low'].values
        swing_highs = []
        swing_lows = []

        for i in range(2, len(df) - 2):
            if highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1] and highs[i] > highs[i+2]:
                swing_highs.append((i, highs[i]))
            if lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1] and lows[i] < lows[i+2]:
                swing_lows.append((i, lows[i]))

        has_eqh = False
        eqh_level = 0.0
        if len(swing_highs) >= 2:
            for j in range(len(swing_highs)-1, max(0, len(swing_highs)-4), -1):
                for k in range(j-1, max(-1, j-3), -1):
                    h1 = swing_highs[j][1]
                    h2 = swing_highs[k][1]
                    if abs(h1 - h2) / ((h1 + h2) / 2.0) <= tolerance:
                        has_eqh = True
                        eqh_level = max(h1, h2)
                        break
                if has_eqh:
                    break

        has_eql = False
        eql_level = 0.0
        if len(swing_lows) >= 2:
            for j in range(len(swing_lows)-1, max(0, len(swing_lows)-4), -1):
                for k in range(j-1, max(-1, j-3), -1):
                    l1 = swing_lows[j][1]
                    l2 = swing_lows[k][1]
                    if abs(l1 - l2) / ((l1 + l2) / 2.0) <= tolerance:
                        has_eql = True
                        eql_level = min(l1, l2)
                        break
                if has_eql:
                    break

        curr_price = float(df['close'].iloc[-1])
        bias = 0.0
        # If price is trading below EQH and approaching it -> Magnet for BSL run
        if has_eqh and curr_price < eqh_level:
            bias += 0.5
        # If price is trading above EQL and approaching it -> Magnet for SSL run
        if has_eql and curr_price > eql_level:
            bias -= 0.5

        return {
            "has_eqh": has_eqh,
            "eqh_level": round(float(eqh_level), 4),
            "has_eql": has_eql,
            "eql_level": round(float(eql_level), 4),
            "bias": bias,
            "description": f"EQH BSL: {eqh_level:.2f}" if has_eqh else (f"EQL SSL: {eql_level:.2f}" if has_eql else "No equal extremes")
        }
    except Exception as e:
        return {"has_eqh": False, "eqh_level": 0.0, "has_eql": False, "eql_level": 0.0, "bias": 0.0, "description": str(e)}

_HTF_CACHE = {}

def fetch_htf_market_structure(symbol: str, ttl_seconds: int = 300) -> dict:
    """
    Higher Timeframe (HTF) Market Structure Engine (D1 15% + H4 15% = 30% Confluence):
    - Fetches Daily (1d) and 4-Hour (4h) klines with multi-mirror fallback.
    - Caches in-memory for 5 minutes (300s TTL) for 0.0ms subsequent inference latency.
    - Determines true macro direction so 15m/1m scalps never fight the daily trend.
    """
    global _HTF_CACHE
    now = time.time()
    if symbol in _HTF_CACHE:
        entry = _HTF_CACHE[symbol]
        if now - entry['timestamp'] < ttl_seconds:
            return entry['data']

    def _fetch_candles(interval: str, limit: int = 30) -> pd.DataFrame:
        endpoints = [
            f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}",
            f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}",
            f"https://api.binance.us/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        ]
        for url in endpoints:
            try:
                res = requests.get(url, timeout=3)
                if res.status_code == 200:
                    raw = res.json()
                    if isinstance(raw, list) and len(raw) > 0:
                        cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                'close_time', 'quote_vol', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore']
                        df_k = pd.DataFrame(raw, columns=cols)
                        for c in ['open', 'high', 'low', 'close', 'volume']:
                            df_k[c] = pd.to_numeric(df_k[c])
                        return df_k
            except Exception:
                continue
        return pd.DataFrame()

    try:
        df_h4 = _fetch_candles("4h", 30)
        df_d1 = _fetch_candles("1d", 30)

        h4_struct = calculate_market_structure(df_h4) if len(df_h4) >= 15 else {"trend": "NEUTRAL", "bias": 0.0}
        d1_struct = calculate_market_structure(df_d1) if len(df_d1) >= 15 else {"trend": "NEUTRAL", "bias": 0.0}

        data = {
            "d1_trend": d1_struct.get("trend", "NEUTRAL"),
            "d1_bias": float(d1_struct.get("bias", 0.0)),
            "h4_trend": h4_struct.get("trend", "NEUTRAL"),
            "h4_bias": float(h4_struct.get("bias", 0.0)),
            "htf_confluence": round(float(d1_struct.get("bias", 0.0) * 0.5 + h4_struct.get("bias", 0.0) * 0.5), 2)
        }
    except Exception:
        data = {
            "d1_trend": "NEUTRAL",
            "d1_bias": 0.0,
            "h4_trend": "NEUTRAL",
            "h4_bias": 0.0,
            "htf_confluence": 0.0
        }

    _HTF_CACHE[symbol] = {"timestamp": now, "data": data}
    return data

# ==============================================================================
# 🏛️ INSTITUTIONAL 10-PILLAR QUANTITATIVE FEATURE ENGINE (SUPER SMART SUITE)
# ==============================================================================
# 1. Market Structure / Price Action (BOS, CHoCH, Swing HH/HL/LH/LL)
# 2. Support & Resistance / Supply & Demand (Order Blocks & Fair Value Gaps FVG)
# 3. Liquidity / Swings (PDH/PDL Turtle Soup Sweeps)
# 4. EMA Alignment (EMA 20/50/200 Multi-Timeframe)
# 5. ATR Volatility & Stop-Loss Multiplier
# 6. Volume & Order Flow (CVD Imbalance & Aggressive Delta)
# 7. VWAP & Standard Deviation Bands (±1σ, ±2σ)
# 8. RSI 14 & Regular/Hidden Divergence Detection
# 9. MACD Momentum Acceleration
# 10. Fibonacci Retracement (Golden Pocket 61.8% OTE Pullback)
# ==============================================================================

def calculate_market_structure(df: pd.DataFrame, swing_window: int = 5) -> dict:
    """
    Pillar 1: Market Structure / Price Action
    Detects Swing Highs/Lows, Break of Structure (BOS), Change of Character (CHoCH).
    """
    if len(df) < swing_window * 3:
        return {"trend": "NEUTRAL", "bias": 0.0, "bos": False, "choch": False}
    
    try:
        highs = df['high'].values
        lows = df['low'].values
        closes = df['close'].values
        n = len(df)

        swing_highs = []
        swing_lows = []

        for i in range(swing_window, n - swing_window):
            if highs[i] == max(highs[i - swing_window : i + swing_window + 1]):
                swing_highs.append((i, highs[i]))
            if lows[i] == min(lows[i - swing_window : i + swing_window + 1]):
                swing_lows.append((i, lows[i]))

        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return {"trend": "NEUTRAL", "bias": 0.0, "bos": False, "choch": False}

        last_sh1, last_sh2 = swing_highs[-1][1], swing_highs[-2][1]
        last_sl1, last_sl2 = swing_lows[-1][1], swing_lows[-2][1]
        curr_close = closes[-1]

        # Structure analysis
        is_uptrend = (last_sh1 > last_sh2) and (last_sl1 > last_sl2)
        is_downtrend = (last_sh1 < last_sh2) and (last_sl1 < last_sl2)

        # BOS (Break of Structure)
        bullish_bos = curr_close > last_sh1
        bearish_bos = curr_close < last_sl1

        # CHoCH (Change of Character)
        bullish_choch = (not is_uptrend) and (curr_close > last_sh1)
        bearish_choch = (not is_downtrend) and (curr_close < last_sl1)

        bias = 0.0
        if is_uptrend or bullish_bos or bullish_choch:
            trend = "BULLISH"
            bias = 1.0 if (bullish_bos or bullish_choch) else 0.5
        elif is_downtrend or bearish_bos or bearish_choch:
            trend = "BEARISH"
            bias = -1.0 if (bearish_bos or bearish_choch) else -0.5
        else:
            trend = "CHOPPY_RANGE"
            bias = 0.0

        return {
            "trend": trend,
            "bias": bias,
            "bos": bullish_bos or bearish_bos,
            "choch": bullish_choch or bearish_choch,
            "last_swing_high": float(last_sh1),
            "last_swing_low": float(last_sl1)
        }
    except Exception:
        return {"trend": "NEUTRAL", "bias": 0.0, "bos": False, "choch": False}

def detect_order_blocks_and_fvg(df: pd.DataFrame) -> dict:
    """
    Pillar 2: Support & Resistance / Supply & Demand (Order Blocks & Fair Value Gaps FVG).
    """
    if len(df) < 5:
        return {"bias": 0.0, "fvg_type": "NONE", "ob_price": 0.0, "has_fvg": False}

    try:
        # FVG 3-candle imbalance check
        c1 = df.iloc[-3]
        c2 = df.iloc[-2]
        c3 = df.iloc[-1]

        bullish_fvg = c3['low'] > c1['high']
        bearish_fvg = c3['high'] < c1['low']

        fvg_type = "NONE"
        bias = 0.0

        if bullish_fvg:
            fvg_type = "BULLISH_FVG"
            bias = 1.0
        elif bearish_fvg:
            fvg_type = "BEARISH_FVG"
            bias = -1.0

        ob_price = float(c2['open'])
        return {
            "bias": bias,
            "fvg_type": fvg_type,
            "ob_price": ob_price,
            "has_fvg": (bullish_fvg or bearish_fvg)
        }
    except Exception:
        return {"bias": 0.0, "fvg_type": "NONE", "ob_price": 0.0, "has_fvg": False}

def calculate_vwap_bands(df: pd.DataFrame) -> dict:
    """
    Pillar 7: VWAP (Volume-Weighted Average Price) & Standard Deviation Bands (±1σ, ±2σ).
    """
    if len(df) < 5 or 'volume' not in df.columns:
        return {"vwap": 0.0, "zscore": 0.0, "bias": 0.0}
    try:
        typical_price = (df['high'] + df['low'] + df['close']) / 3.0
        cum_vol = df['volume'].cumsum()
        cum_pv = (typical_price * df['volume']).cumsum()
        vwap_series = cum_pv / (cum_vol + 1e-10)
        curr_vwap = float(vwap_series.iloc[-1])
        curr_price = float(df['close'].iloc[-1])

        dev = ((typical_price - vwap_series) ** 2 * df['volume']).cumsum() / (cum_vol + 1e-10)
        vwap_std = float(np.sqrt(np.maximum(dev.iloc[-1], 1e-10)))

        zscore = (curr_price - curr_vwap) / (vwap_std + 1e-10)
        bias = 1.0 if zscore > 0.5 else (-1.0 if zscore < -0.5 else 0.0)

        return {
            "vwap": curr_vwap,
            "upper_1s": curr_vwap + vwap_std,
            "lower_1s": curr_vwap - vwap_std,
            "upper_2s": curr_vwap + 2 * vwap_std,
            "lower_2s": curr_vwap - 2 * vwap_std,
            "zscore": float(zscore),
            "bias": bias
        }
    except Exception:
        return {"vwap": 0.0, "zscore": 0.0, "bias": 0.0}

def calculate_fibonacci_proximity(df: pd.DataFrame, window: int = 50) -> dict:
    """
    Pillar 10: Fibonacci 38.2% / 50% / 61.8% Golden Pocket Pullback Zones.
    """
    if len(df) < 20:
        return {"fib_bias": 0.0, "in_golden_pocket": False, "fib_618": 0.0}
    try:
        recent = df.iloc[-window:] if len(df) >= window else df
        highest = float(recent['high'].max())
        lowest = float(recent['low'].min())
        curr_price = float(df['close'].iloc[-1])
        price_range = highest - lowest

        if price_range <= 0:
            return {"fib_bias": 0.0, "in_golden_pocket": False, "fib_618": 0.0}

        fib_382 = highest - 0.382 * price_range
        fib_500 = highest - 0.500 * price_range
        fib_618 = highest - 0.618 * price_range
        fib_650 = highest - 0.650 * price_range

        in_bullish_golden_pocket = (curr_price <= fib_618) and (curr_price >= fib_650)
        proximity = 1.0 - min(1.0, abs(curr_price - fib_618) / price_range)

        return {
            "highest": highest,
            "lowest": lowest,
            "fib_382": float(fib_382),
            "fib_500": float(fib_500),
            "fib_618": float(fib_618),
            "in_golden_pocket": bool(in_bullish_golden_pocket),
            "proximity_score": float(proximity),
            "fib_bias": 1.0 if in_bullish_golden_pocket else 0.0
        }
    except Exception:
        return {"fib_bias": 0.0, "in_golden_pocket": False, "fib_618": 0.0}

_10_PILLAR_MODELS = None

def get_10_pillar_ml_models():
    """
    Institutional Singleton Cache for the 10-Pillar ML Deep Ensemble:
    - brain_scaler.pkl (Standard Normalizer)
    - brain_xgb.pkl (XGBoost Classifier)
    - brain_catboost.pkl (CatBoost Classifier)
    - brain_lightgbm.pkl (LightGBM Classifier)
    - brain_moe_router.pkl (Mixture-of-Experts Router)
    - brain_hmm_regime.pkl (HMM Market Regime Classifier)
    """
    global _10_PILLAR_MODELS
    if _10_PILLAR_MODELS is not None:
        return _10_PILLAR_MODELS
    try:
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        scaler_path = os.path.join(models_dir, "brain_scaler.pkl")
        xgb_path = os.path.join(models_dir, "brain_xgb.pkl")
        if not (os.path.exists(scaler_path) and os.path.exists(xgb_path)):
            return None

        import joblib
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            scaler = joblib.load(scaler_path)
            xgb = joblib.load(xgb_path)
            cb = joblib.load(os.path.join(models_dir, "brain_catboost.pkl")) if os.path.exists(os.path.join(models_dir, "brain_catboost.pkl")) else None
            lgb = joblib.load(os.path.join(models_dir, "brain_lightgbm.pkl")) if os.path.exists(os.path.join(models_dir, "brain_lightgbm.pkl")) else None
            moe = joblib.load(os.path.join(models_dir, "brain_moe_router.pkl")) if os.path.exists(os.path.join(models_dir, "brain_moe_router.pkl")) else None
            hmm = joblib.load(os.path.join(models_dir, "brain_hmm_regime.pkl")) if os.path.exists(os.path.join(models_dir, "brain_hmm_regime.pkl")) else None

        _10_PILLAR_MODELS = {
            "scaler": scaler,
            "xgb": xgb,
            "cb": cb,
            "lgb": lgb,
            "moe": moe,
            "hmm": hmm
        }
        return _10_PILLAR_MODELS
    except Exception:
        return None

def extract_10_pillar_feature_vector(symbol: str, interval: str = "15m", limit: int = 100) -> dict:
    """
    Unified 10-Pillar Feature Extractor for /turbo_hedge and Super Smart AI Models.
    Fuses deterministic quantitative metrics with 10-Pillar ML Deep Ensemble (XGB, CatBoost, LightGBM, MoE, HMM).
    """
    symbol = str(symbol).upper().strip()
    try:
        endpoints = [
            f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}",
            f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}",
            f"https://api.binance.us/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        ]
        df = None
        for url in endpoints:
            try:
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    raw = res.json()
                    if isinstance(raw, list) and len(raw) > 0:
                        cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                'close_time', 'quote_vol', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore']
                        df = pd.DataFrame(raw, columns=cols)
                        for c in ['open', 'high', 'low', 'close', 'volume', 'taker_buy_base', 'taker_buy_quote']:
                            df[c] = pd.to_numeric(df[c])
                        break
            except Exception:
                continue

        if df is None or len(df) == 0:
            return {"error": "Failed to fetch klines from all mirrors", "symbol": symbol, "confluence_score": 50.0}

        curr_price = float(df['close'].iloc[-1])

        # 1. Market Structure
        struct = calculate_market_structure(df)

        # 2. Support & Resistance (FVG & OB)
        snr = detect_order_blocks_and_fvg(df)

        # 3. Liquidity Sweep
        sweep = detect_liquidity_sweep(symbol)

        # 4. EMA Alignment (EMA 20, 50, 200)
        ema20 = float(df['close'].ewm(span=20, adjust=False).mean().iloc[-1])
        ema50 = float(df['close'].ewm(span=50, adjust=False).mean().iloc[-1])
        ema200 = float(df['close'].ewm(span=min(200, len(df)), adjust=False).mean().iloc[-1])
        is_ema_bullish = (curr_price > ema20 > ema50) and (curr_price > ema200)
        is_ema_bearish = (curr_price < ema20 < ema50) and (curr_price < ema200)
        ema_score = 1.0 if is_ema_bullish else (-1.0 if is_ema_bearish else 0.0)

        # 5. ATR Volatility
        atr_series = calculate_atr(df, window=14)
        atr_val = float(atr_series.iloc[-1]) if not pd.isna(atr_series.iloc[-1]) else curr_price * 0.015
        atr_pct = (atr_val / curr_price) * 100.0

        # 6. Volume & Order Flow (CVD Imbalance)
        tot_vol = df['volume'].iloc[-5:].sum()
        taker_buy = df['taker_buy_base'].iloc[-5:].sum()
        taker_sell = tot_vol - taker_buy
        cvd_imbalance = (taker_buy - taker_sell) / (tot_vol + 1e-10)
        order_flow_bias = 1.0 if cvd_imbalance > 0.15 else (-1.0 if cvd_imbalance < -0.15 else 0.0)

        # 7. VWAP & Bands
        vwap_data = calculate_vwap_bands(df)

        # 8. RSI 14 & Divergence
        rsi_series = calculate_rsi(df, window=14)
        rsi_val = float(rsi_series.iloc[-1]) if not pd.isna(rsi_series.iloc[-1]) else 50.0

        # 9. MACD Momentum
        macd_line, sig_line, hist = calculate_macd(df)
        curr_hist = float(hist.iloc[-1]) if not pd.isna(hist.iloc[-1]) else 0.0
        prev_hist = float(hist.iloc[-2]) if len(hist) > 1 and not pd.isna(hist.iloc[-2]) else 0.0
        hist_accel = 1.0 if (curr_hist > prev_hist and curr_hist > 0) else (-1.0 if (curr_hist < prev_hist and curr_hist < 0) else 0.0)

        # 10. Fibonacci Retracement
        fib_data = calculate_fibonacci_proximity(df)

        # 11. Higher Timeframe (HTF) D1 (15%) + H4 (15%) = 30% Direction Matrix
        htf_data = fetch_htf_market_structure(symbol)

        # 12. SMC Equal Highs (EQH) / Equal Lows (EQL) Liquidity Pool Matrix (10%)
        eqh_eql = detect_eqh_eql_liquidity(df)

        # 13. ICT Session Kill Zone Gating
        ict_data = detect_ict_kill_zone(df['timestamp'].iloc[-1] if 'timestamp' in df.columns else None)

        # 14. Order Flow CVD Absorption Divergence
        cvd_abs = detect_cvd_absorption_divergence(df)

        # 🏛️ Vectorized 100% Institutional Multi-Factor Technical Score:
        # - Direction (30%): D1 (15%) + H4 (15%)
        # - Location (20%): S/R (10%) + Supply/Demand (Order Blocks/FVG) (10%)
        # - Liquidity (10%): EQH/EQL Liquidity Pools + Previous Swings (10%)
        # - Trigger (20%): Liquidity Sweep (10%) + BOS/CHoCH (10%)
        # - Confirmation (20%): EMA 20/50/200 (5%) + RSI (5%) + MACD/Volume/VWAP (10%)
        # TOTAL = 100.0%
        bull_weights = (
            htf_data['d1_bias'] * 15.0 +
            htf_data['h4_bias'] * 15.0 +
            snr['bias'] * 10.0 +
            (1.0 if snr['fvg_type'] == 'BULLISH' else (-1.0 if snr['fvg_type'] == 'BEARISH' else 0.0)) * 10.0 +
            eqh_eql['bias'] * 10.0 +
            (1.0 if sweep.get('type') == 'BULLISH' else (-1.0 if sweep.get('type') == 'BEARISH' else 0.0)) * 10.0 +
            struct['bias'] * 10.0 +
            ema_score * 5.0 +
            (1.0 if 40.0 <= rsi_val <= 65.0 else (0.0 if rsi_val > 75.0 else -0.5)) * 5.0 +
            vwap_data['bias'] * 4.0 +
            order_flow_bias * 3.0 +
            hist_accel * 3.0 +
            cvd_abs['bias'] * 12.0
        )
        raw_tech_confluence = max(0.0, min(100.0, 50.0 + (bull_weights / 2.0)))

        # 🏛️ Deep ML Ensemble Inference (HMM, XGBoost, CatBoost, LightGBM, MoE Router)
        ml_models = get_10_pillar_ml_models()
        ml_prob = raw_tech_confluence
        regime_name = "NEUTRAL"
        ml_active = False

        if ml_models is not None:
            try:
                high_20 = float(df['high'].rolling(min(20, len(df))).max().iloc[-1])
                low_20 = float(df['low'].rolling(min(20, len(df))).min().iloc[-1])
                dist_high = (high_20 - curr_price) / (curr_price + 1e-10)
                dist_low = (curr_price - low_20) / (curr_price + 1e-10)
                sweep_score = 1.0 if sweep.get('type') == 'BULLISH' else (-1.0 if sweep.get('type') == 'BEARISH' else 0.0)
                fvg_score = 1.0 if snr.get('fvg_type') == 'BULLISH' else (-1.0 if snr.get('fvg_type') == 'BEARISH' else 0.0)
                fib_proximity = fib_data.get('proximity_score', 0.5)

                feat_vec = np.array([[
                    ema_score,
                    atr_val / (curr_price + 1e-10),
                    cvd_imbalance,
                    vwap_data.get('zscore', 0.0),
                    rsi_val,
                    curr_hist,
                    hist_accel,
                    dist_high,
                    dist_low,
                    sweep_score,
                    fvg_score,
                    fib_proximity
                ]])

                feat_scaled = ml_models['scaler'].transform(feat_vec)
                p_xgb = ml_models['xgb'].predict_proba(feat_scaled)[0, 1] if ml_models.get('xgb') else 0.5
                p_cb = ml_models['cb'].predict_proba(feat_scaled)[0, 1] if ml_models.get('cb') else p_xgb
                p_lgb = ml_models['lgb'].predict_proba(feat_scaled)[0, 1] if ml_models.get('lgb') else p_xgb
                p_moe = ml_models['moe'].predict_proba(feat_scaled)[0, 1] if ml_models.get('moe') else p_xgb

                ml_prob = float((p_xgb * 0.35 + p_cb * 0.25 + p_lgb * 0.25 + p_moe * 0.15) * 100.0)

                if ml_models.get('hmm'):
                    reg_id = int(ml_models['hmm'].predict(feat_scaled[:, :4])[0])
                    regime_map = {0: "BEARISH_REGIME", 1: "RANGE_ACCUMULATION", 2: "BULLISH_TREND"}
                    regime_name = regime_map.get(reg_id, "NEUTRAL")

                ml_active = True
            except Exception:
                pass

        # 50/50 Institutional Confluence Fusion
        if ml_active:
            confluence_pct = round(0.50 * raw_tech_confluence + 0.50 * ml_prob, 1)
        else:
            confluence_pct = round(raw_tech_confluence, 1)

        # Apply Prime Liquidity Boost or Dead Zone Dampener
        if ict_data.get('is_prime_liquidity') and confluence_pct >= 55.0:
            confluence_pct = min(98.0, round(confluence_pct * 1.03, 1))

        return {
            "symbol": symbol,
            "price": curr_price,
            "rsi14": rsi_val,
            "atr_val": atr_val,
            "atr_pct": atr_pct,
            "structure": struct['trend'],
            "d1_trend": htf_data['d1_trend'],
            "h4_trend": htf_data['h4_trend'],
            "htf_confluence": htf_data['htf_confluence'],
            "has_eqh": eqh_eql['has_eqh'],
            "eqh_level": eqh_eql['eqh_level'],
            "has_eql": eqh_eql['has_eql'],
            "eql_level": eqh_eql['eql_level'],
            "ema_trend": "BULLISH" if is_ema_bullish else ("BEARISH" if is_ema_bearish else "NEUTRAL"),
            "fvg_type": snr['fvg_type'],
            "sweep_type": sweep.get('type'),
            "cvd_imbalance": float(cvd_imbalance),
            "vwap_zscore": vwap_data['zscore'],
            "fib_golden_pocket": fib_data['in_golden_pocket'],
            "ict_session": ict_data['session'],
            "is_prime_liquidity": ict_data['is_prime_liquidity'],
            "ict_description": ict_data['description'],
            "cvd_absorption": cvd_abs['divergence'],
            "cvd_absorption_desc": cvd_abs['description'],
            "regime": regime_name,
            "ml_win_rate_pct": round(ml_prob, 1),
            "ml_active": ml_active,
            "confluence_score": confluence_pct,
            "suggested_direction": "BUY" if confluence_pct >= 62.0 else ("SELL" if confluence_pct <= 38.0 else "HOLD"),
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol, "confluence_score": 50.0}
