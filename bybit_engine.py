import time
import hmac
import hashlib
import requests
import asyncio
from typing import Dict, Any, Optional

BYBIT_API_URL = "https://api.bybit.com"

def get_bybit_headers(api_key: str, api_secret: str, params_str: str) -> Dict[str, str]:
    """Generates required headers for Bybit API."""
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    
    sign_payload = timestamp + api_key + recv_window + params_str
    signature = hmac.new(
        bytes(api_secret, "utf-8"),
        bytes(sign_payload, "utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    return {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "Content-Type": "application/json"
    }

def get_current_price(symbol: str) -> float:
    """Fetches current price of a symbol on Bybit Spot."""
    try:
        url = f"{BYBIT_API_URL}/v5/market/tickers"
        params = {"category": "spot", "symbol": symbol}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get("retCode") == 0:
            return float(data["result"]["list"][0]["lastPrice"])
        return 0.0
    except Exception as e:
        print(f"[Bybit] Error fetching price for {symbol}: {e}")
        return 0.0

def place_market_order(api_key: str, api_secret: str, symbol: str, side: str, qty: float) -> Dict[str, Any]:
    """Places a Spot Market order on Bybit."""
    try:
        url = f"{BYBIT_API_URL}/v5/order/create"
        import json
        payload = {
            "category": "spot",
            "symbol": symbol,
            "side": side.capitalize(),
            "orderType": "Market",
            "qty": str(qty)
        }
        payload_str = json.dumps(payload)
        
        headers = get_bybit_headers(api_key, api_secret, payload_str)
        response = requests.post(url, headers=headers, data=payload_str, timeout=10)
        return response.json()
    except Exception as e:
        return {"retCode": -1, "retMsg": str(e)}

def place_market_buy(api_key: str, api_secret: str, symbol: str, quote_qty: float) -> Dict[str, Any]:
    """Places a market buy order using Quote Currency (e.g. USDT) amount."""
    price = get_current_price(symbol)
    if price <= 0:
        return {"retCode": -1, "retMsg": "Could not fetch price to calculate qty."}
    qty = quote_qty / price
    qty = round(qty, 4) 
    return place_market_order(api_key, api_secret, symbol, "Buy", qty)

def place_market_sell(api_key: str, api_secret: str, symbol: str, qty: float) -> Dict[str, Any]:
    """Places a market sell order."""
    qty = round(qty, 4)
    return place_market_order(api_key, api_secret, symbol, "Sell", qty)
