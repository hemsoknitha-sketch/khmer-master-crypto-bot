import requests
import time

_btc_cache = {"price_1m_change": 0.0, "status": "STABLE", "timestamp": 0}

def get_btc_impulse_status() -> dict:
    """
    BTC Lead Indicator Engine.
    BTC leads Altcoins (SOL, AVAX, DOGE, NEAR, XRP) by 15-30 seconds.
    Tracks 1m BTC price impulse rate to prevent trading altcoins against BTC market shocks.
    """
    global _btc_cache
    now = time.time()
    if now - _btc_cache["timestamp"] < 3:
        return _btc_cache

    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=5"
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            klines = res.json()
            if klines and len(klines) >= 2:
                current_price = float(klines[-1][4])
                prev_price = float(klines[-2][4])
                change_1m = ((current_price - prev_price) / prev_price) * 100.0
                
                status = "STABLE"
                if change_1m <= -0.35:
                    status = "DUMPING"
                elif change_1m >= 0.35:
                    status = "PUMPING"

                _btc_cache = {
                    "price_1m_change": round(change_1m, 3),
                    "status": status,
                    "timestamp": now
                }
                return _btc_cache
    except Exception as e:
        print(f"⚠️ [BTC LEAD GUARD ERROR]: {e}")

    return _btc_cache
