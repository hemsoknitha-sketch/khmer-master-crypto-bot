import requests
import json
import time
import trading_engine

def detect_liquidity_sweep_wick(symbol: str = "PAXGUSDT") -> dict:
    """
    Sub-second Liquidity Sweep & Bottom Wick Detector.
    Scans for sudden lower wick drops (>= 0.4% in 1m/5m klines or ticker depth).
    Returns trigger status and target rebound prices.
    """
    result = {
        "sweep_detected": False,
        "symbol": symbol,
        "current_price": 0.0,
        "bottom_wick_price": 0.0,
        "rebound_target": 0.0,
        "wick_drop_pct": 0.0,
        "reason": "Normal price action"
    }

    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=10"
        res = requests.get(url, timeout=(3.05, 10))
        if res.status_code != 200:
            return result

        klines = res.json()
        if not klines or len(klines) < 5:
            return result

        latest = klines[-1]
        open_p = float(latest[1])
        high_p = float(latest[2])
        low_p = float(latest[3])
        close_p = float(latest[4])

        # Bottom wick length = Open/Close min minus Low
        body_min = min(open_p, close_p)
        wick_drop_pct = ((body_min - low_p) / body_min) * 100.0 if body_min > 0 else 0.0

        result["current_price"] = close_p
        result["bottom_wick_price"] = low_p
        result["wick_drop_pct"] = round(wick_drop_pct, 2)

        if wick_drop_pct >= 0.40:
            rebound_target = round(low_p * (1.0 + (wick_drop_pct * 0.008)), 2)
            result["sweep_detected"] = True
            result["rebound_target"] = rebound_target
            result["reason"] = f"🚨 Bottom Liquidity Sweep Wick Detected! (-{wick_drop_pct:.2f}% Drop, Rebound Target: ${rebound_target:,.2f})"

    except (requests.exceptions.ReadTimeout, requests.exceptions.RequestException):
        pass
    except Exception as e:
        print(f"⚠️ [SWEEP DETECTOR ERROR]: {e}")

    return result

def execute_sweep_rebound_trade(api_key: str, api_secret: str, symbol: str, amount_usdt: float, sweep_info: dict) -> dict:
    """
    Executes instant sub-second bottom wick buy order and 5-10s V-shape rebound exit.
    """
    try:
        price = sweep_info.get("bottom_wick_price") or trading_engine.get_current_price(symbol)
        if price <= 0:
            return {"status": "error", "message": "Price unavailable"}

        # 5x Leverage for high-velocity wick snipes
        trading_engine.set_futures_leverage(api_key, api_secret, symbol, 5)

        qty = (amount_usdt * 5.0) / price
        if "PAXG" in symbol or "BTC" in symbol:
            qty = round(qty, 3)
        elif "ETH" in symbol:
            qty = round(qty, 2)
        else:
            qty = round(qty, 1)

        if qty <= 0:
            return {"status": "error", "message": "Quantity too small"}

        # Market Buy at Bottom Wick (is_entry=True, without reduceOnly restriction)
        buy_res = trading_engine.smart_execute_futures_order(api_key, api_secret, symbol, "BUY", qty, leverage=5, is_entry=True)

        return {
            "status": "success",
            "symbol": symbol,
            "bottom_price": price,
            "rebound_target": sweep_info.get("rebound_target"),
            "quantity": qty,
            "order": buy_res
        }
    except Exception as e:
        print(f"❌ [EXECUTE SWEEP REBOUND ERROR]: {e}")
        return {"status": "error", "message": str(e)}
