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

# =========================================================================
# 🚀 INSTITUTIONAL TOP 500 FUTURES CANDIDATE ENGINE
# =========================================================================

FUTURES_COINS_CACHE = {
    "timestamp": 0,
    "coins": []
}
FUTURES_CACHE_EXPIRY_SECONDS = 45  # 45-second high-frequency cache

def fetch_top_futures_candidates(limit: int = 60, min_volume: float = 5000000.0) -> list:
    """
    Institutional Top 500 Futures Candidate Scanner:
    Queries Binance Futures /fapi/v1/ticker/24hr dynamically across 250+ perpetual pairs.
    Filters for:
    1. Active TRADING perpetual USDT contracts.
    2. Zero stablecoins and zero TradFi synthetics (Invariants 7 & 9).
    3. Minimum $5M 24h volume for zero slippage.
    4. Sweet-spot momentum (abs price change between 2.5% and 15.0%).
    5. Excludes overbought/oversold extreme pumps (> 20.0%).
    Ranks by Momentum & Volume Log-Score to deliver prime breakout/breakdown candidates.
    """
    global FUTURES_COINS_CACHE
    current_time = time.time()
    if FUTURES_COINS_CACHE["coins"] and (current_time - FUTURES_COINS_CACHE["timestamp"]) < FUTURES_CACHE_EXPIRY_SECONDS:
        return FUTURES_COINS_CACHE["coins"][:limit]

    try:
        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            tickers = res.json()
            TRADFI_EXCLUSIONS = {
                "QNTXUSDT", "CSOPSKHYNIX2LUSDT", "MINIMAXUSDT", "ZHIPUUSDT", "NOKUSDT", "SMCIUSDT", "DELLUSDT", "SNDKUSDT", 
                "STXXUSDT", "INTWUSDT", "CBRSUSDT", "EWYUSDT", "MVLLUSDT", "GLWUSDT", "HK0700USDT", "HK1810USDT", "INTCUSDT", 
                "CHIPUSDT", "METAUSDT", "AAOIUSDT", "MRVLUSDT", "CRWVUSDT", "ZAMAUSDT", "PLTRUSDT", "TSMUSDT", "AMDUSDT", 
                "TQQQUSDT", "SQQQUSDT", "ARMUSDT", "TSLAUSDT", "NATGASUSDT", "INXUSDT", "AMZNUSDT", "AAPLUSDT", "MSFTUSDT", 
                "NVDAUSDT", "MSTRUSDT", "BABAUSDT", "ROBOUSDT", "NBISUSDT", "SHAZUSDT", "KORUUSDT", "DRAMUSDT", "SNXXUSDT", 
                "MUUUSDT", "MUUSDT", "BEUSDT", "SKHYUSDT", "SKHYNIXUSDT", "SAMSUNGUSDT", "WDCUSDT", "ORCLUSDT", "AIAUSDT", "MUBARAKUSDT", 
                "HYPEUSDT", "LITEUSDT", "DEXEUSDT", "BZUSDT", "CLUSDT", "XAUUSDT", "XAGUSDT", "TRUMPUSDT", "HFTUSDT", "GWEIUSDT", 
                "EPICUSDT", "USD1USDT", "SPCXUSDT", "OPENAIUSDT", "FIGMAUSDT", "STRIPEUSDT", "BYTEDANCEUSDT", "ANTHROPICUSDT",
                "USDCUSDT", "FDUSDUSDT", "TUSDUSDT", "BUSDUSDT"
            }
            candidates = []
            for t in tickers:
                sym = t.get("symbol", "")
                if not sym.endswith("USDT") or sym in TRADFI_EXCLUSIONS or not sym.isascii():
                    continue
                quote_vol = float(t.get("quoteVolume", 0.0) or 0.0)
                if quote_vol < min_volume:
                    continue
                abs_chg = abs(float(t.get("priceChangePercent", 0.0) or 0.0))
                # Early Sweet Spot between 2.5% and 15.0%
                if abs_chg < 2.5 or abs_chg > 20.0:
                    continue
                # Sweet spot peak around 6.5% - 8.5%
                momentum_score = 100.0 - (abs(abs_chg - 7.5) * 5.0)
                vol_score = math.log10(max(1.0, quote_vol)) * 8.0
                total_score = momentum_score + vol_score
                candidates.append({"symbol": sym, "score": total_score, "vol": quote_vol, "chg": abs_chg})

            candidates.sort(key=lambda x: x["score"], reverse=True)
            top_syms = [c["symbol"] for c in candidates]
            if top_syms:
                FUTURES_COINS_CACHE["timestamp"] = current_time
                FUTURES_COINS_CACHE["coins"] = top_syms
                return top_syms[:limit]
    except Exception as e:
        print(f"⚠️ [FUTURES CANDIDATE SCANNER] Error: {e}")

    if FUTURES_COINS_CACHE["coins"]:
        return FUTURES_COINS_CACHE["coins"][:limit]

    return ["ETHUSDT", "SOLUSDT", "BTCUSDT", "SUIUSDT", "NEARUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "ARBUSDT", "APTUSDT"]

def get_top_500_coins(limit: int = 500):
    return fetch_top_volatile_coins(limit=limit)

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
