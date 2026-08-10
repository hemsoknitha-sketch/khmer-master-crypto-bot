import requests
import time
import math

# List of common stablecoins to exclude
STABLECOINS = {
    "USDCUSDT", "FDUSDUSDT", "TUSDUSDT", "BUSDUSDT", "EURUSDT", 
    "USDPUSDT", "DAIUSDT", "AEURUSDT", "USDEUSDT", "USDDUSDT", "PYUSDUSDT",
    "USD1USDT"
}

# Cache to avoid hitting Binance API too often
# Structure: {"timestamp": 123456789, "coins": ["BTCUSDT", "ETHUSDT", ...]}
TOP_COINS_CACHE = {
    "timestamp": 0,
    "coins": []
}

CACHE_EXPIRY_SECONDS = 3600  # 1 hour cache

def fetch_top_volatile_coins(limit=500):
    """
    Fetches the top coins by 24h quoteVolume from Binance.
    Excludes stablecoins and leveraged tokens.
    Uses an in-memory cache to prevent API rate limits.
    """
    global TOP_COINS_CACHE
    
    current_time = time.time()
    
    # Check if cache is still valid
    if TOP_COINS_CACHE["coins"] and (current_time - TOP_COINS_CACHE["timestamp"]) < CACHE_EXPIRY_SECONDS:
        return TOP_COINS_CACHE["coins"][:limit]
        
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            
            # Filter and sort by 24h Absolute Volatility % (excluding low volatility assets like PAXG)
            valid_coins = []
            for item in data:
                symbol = item["symbol"]
                change_pct = abs(float(item.get("priceChangePercent", 0)))
                volume = float(item.get("quoteVolume", 0))
                
                # Only keep USDT pairs, exclude stablecoins, exclude PAXG (low volatility), exclude UP/DOWN leveraged tokens
                if symbol.endswith("USDT") and symbol not in STABLECOINS and "PAXG" not in symbol and not symbol.endswith("UPUSDT") and not symbol.endswith("DOWNUSDT"):
                    # Futures Trading Status Guard: Verify symbol is active and TRADING on Binance Futures
                    try:
                        import trading_engine
                        sym_info = trading_engine.get_futures_symbol_info(symbol)
                        if sym_info and sym_info.get("status") != "TRADING":
                            continue
                    except Exception:
                        pass

                    # High Volatility Score = Volatility % * 0.7 + Volume Weight * 0.3
                    volatility_score = (change_pct * 10.0) + (math.log10(max(1.0, volume)) if volume > 0 else 0)
                    valid_coins.append({
                        "symbol": symbol,
                        "change_pct": change_pct,
                        "volume": volume,
                        "score": volatility_score
                    })
                    
            # Sort by High Volatility Score descending
            valid_coins.sort(key=lambda x: x["score"], reverse=True)
            
            # Extract symbols
            top_symbols = [coin["symbol"] for coin in valid_coins]
            
            # Update cache
            TOP_COINS_CACHE["timestamp"] = current_time
            TOP_COINS_CACHE["coins"] = top_symbols
            
            print(f"🏆 Dynamic Rank Engine: Fetched top {len(top_symbols)} volatile coins.")
            
            return top_symbols[:limit]
    except Exception as e:
        print(f"❌ Error fetching top coins for dynamic ranking: {e}")
        
    # Fallback to previous cache or safe defaults if API fails
    if TOP_COINS_CACHE["coins"]:
        return TOP_COINS_CACHE["coins"][:limit]
        
    return ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]

def get_top_500_coins():
    # Changed to 10 to implement Hyper-Focus on the absolute most volatile coins
    return fetch_top_volatile_coins(limit=10)

def get_dynamic_coin_allocation(symbol: str) -> float:
    """
    Phase 2: Momentum Radar & 80/20 Capital Shift.
    Returns the percentage of capital to allocate (0.0 to 0.8) based on real-time volatility rank.
    """
    top_coins = get_top_500_coins()
    if symbol not in top_coins:
        return 0.0
        
    rank = top_coins.index(symbol) + 1
    
    if rank == 1:
        return 0.80  # 80% to the absolute hottest coin
    elif rank == 2:
        return 0.40  # 40% to the runner up
    elif rank <= 5:
        return 0.10  # 10% to the mid-tier
    else:
        return 0.0   # 0% to the bottom 5 (Cold)
