import requests
import pandas as pd
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
            
    # If all URLs fail
    return None, f"Network Error: Could not connect to Binance API. Last Error: {last_error}", symbol

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

def fetch_top_gainers(limit: int = 5):
    """
    Fetches the top gaining crypto assets in the last 24 hours from Binance.
    """
    base_urls = [
        "https://data-api.binance.vision",
        "https://api.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com"
    ]
    
    last_error = ""
    for base_url in base_urls:
        url = f"{base_url}/api/v3/ticker/24hr"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Filter for active USDT pairs with liquid 24h volume (>= $1M USDT)
            usdt_pairs = [item for item in data if item['symbol'].endswith('USDT')
                          and float(item.get('lastPrice', 0)) > 0
                          and float(item.get('bidPrice', 0)) > 0
                          and float(item.get('askPrice', 0)) > 0
                          and float(item.get('quoteVolume', 0)) >= 1000000.0]
            
            usdt_pairs.sort(key=lambda x: float(x['priceChangePercent']), reverse=True)
            
            top_gainers = usdt_pairs[:limit]
            top_losers = usdt_pairs[-limit:]
            top_losers.reverse()
            
            summary = "🔥 **24H MARKET VOLATILITY RADAR** 🔥\n\n"
            summary += "🚀 **Top Gainers (Momentum Pump Radar):**\n"
            for i, coin in enumerate(top_gainers):
                full_sym = coin['symbol']
                symbol = full_sym.replace("USDT", "")
                change = float(coin['priceChangePercent'])
                price = float(coin['lastPrice'])
                volume = float(coin['quoteVolume'])
                summary += f"{i+1}. **{full_sym}**: +{change:.2f}% (${price:,.4f} | Vol: ${volume/1e6:.2f}M)\n   ⚡ `/scalp {full_sym} 100 1.5 <PIN>`\n"
                
            summary += "\n🔻 **Top Losers (Dip Rebound Radar):**\n"
            for i, coin in enumerate(top_losers):
                full_sym = coin['symbol']
                symbol = full_sym.replace("USDT", "")
                change = float(coin['priceChangePercent'])
                price = float(coin['lastPrice'])
                volume = float(coin['quoteVolume'])
                summary += f"{i+1}. **{full_sym}**: {change:.2f}% (${price:,.4f} | Vol: ${volume/1e6:.2f}M)\n   ⚡ `/infinity_grid {full_sym} 10 1.0 100 <PIN>`\n"
                
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
