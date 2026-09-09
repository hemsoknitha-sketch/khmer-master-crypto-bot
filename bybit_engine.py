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

def validate_bybit_api_keys(api_key: str, api_secret: str) -> tuple[bool, str, dict]:
    """
    Validates Bybit API Key and Secret using official Bybit V5 user/query-api endpoint.
    Returns: (is_valid: bool, status_message: str, details: dict)
    """
    try:
        srv_time = int(time.time() * 1000)
        try:
            time_res = requests.get(f"{BYBIT_API_URL}/v5/market/time", timeout=5)
            if time_res.status_code == 200:
                srv_time = int(time_res.json().get("time", srv_time))
        except Exception:
            pass

        timestamp = str(srv_time)
        recv_window = "10000"
        params_str = ""
        
        sign_payload = timestamp + api_key + recv_window + params_str
        signature = hmac.new(
            bytes(api_secret, "utf-8"),
            bytes(sign_payload, "utf-8"),
            hashlib.sha256
        ).hexdigest()

        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "Content-Type": "application/json"
        }

        res = requests.get(f"{BYBIT_API_URL}/v5/user/query-api", headers=headers, timeout=8)
        if res.status_code != 200:
            return False, f"HTTP {res.status_code}: មិនអាចភ្ជាប់ទៅកាន់ Bybit API បានទេ ({res.text[:120]})", {}

        data = res.json()
        ret_code = data.get("retCode", -1)
        ret_msg = data.get("retMsg", "Unknown Error")

        if ret_code != 0:
            return False, f"Code {ret_code}: {ret_msg}", {}

        result = data.get("result", {})
        perms = result.get("permissions", {})
        
        spot_perms = perms.get("Spot", [])
        contract_perms = perms.get("ContractTrade", [])
        is_read_only = bool(result.get("readOnly", 0))

        spot_status = "🟢 ដំណើរការ (Enabled)" if spot_perms else "🟡 មិនទាន់បើក (Spot Not Selected)"
        contract_status = "🟢 ដំណើរការ (Enabled)" if contract_perms else "🟡 មិនទាន់បើក (ContractTrade Not Selected)"
        mode_status = "🔴 Read-Only (គ្មានសិទ្ធិ Trade)" if is_read_only else "🟢 Read-Write (ពេញលេញ)"

        msg = (
            "✅ **ភ្ជាប់ BYBIT API ជោគជ័យ! (Bybit V5 API Connected)**\n\n"
            "**មុខងារដែលបានបើកសិទ្ធិលើ Bybit:**\n"
            f" - Spot Trading: {spot_status}\n"
            f" - Derivatives/Futures Trading: {contract_status}\n"
            f" - API Permission Mode: {mode_status}\n\n"
            "*(ប្រព័ន្ធគាំទ្រ Sub-5ms Cross-Exchange Arbitrage & Bybit Futures Hedging ពេញលេញ!)*"
        )
        return True, msg, result
    except Exception as e:
        return False, f"កំហុសក្នុងការតភ្ជាប់ Bybit ៖ {str(e)}", {}

def get_bybit_wallet_balance(api_key: str, api_secret: str, account_type: str = "UNIFIED") -> dict:
    """
    Fetches Bybit wallet balance for Unified Trading or Contract account.
    """
    try:
        srv_time = int(time.time() * 1000)
        try:
            time_res = requests.get(f"{BYBIT_API_URL}/v5/market/time", timeout=5)
            if time_res.status_code == 200:
                srv_time = int(time_res.json().get("time", srv_time))
        except Exception:
            pass

        timestamp = str(srv_time)
        recv_window = "10000"
        params_str = f"accountType={account_type}"

        sign_payload = timestamp + api_key + recv_window + params_str
        signature = hmac.new(
            bytes(api_secret, "utf-8"),
            bytes(sign_payload, "utf-8"),
            hashlib.sha256
        ).hexdigest()

        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "Content-Type": "application/json"
        }

        url = f"{BYBIT_API_URL}/v5/account/wallet-balance?{params_str}"
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            data = res.json()
            if data.get("retCode") == 0:
                accts = data.get("result", {}).get("list", [])
                if accts:
                    acct = accts[0]
                    total_equity = float(acct.get("totalEquity", 0.0))
                    total_available = float(acct.get("totalAvailableBalance", 0.0))
                    usdt_balance = 0.0
                    for c in acct.get("coin", []):
                        if c.get("coin") == "USDT":
                            usdt_balance = float(c.get("walletBalance", 0.0))
                            break
                    return {
                        "total_equity": total_equity,
                        "total_available": total_available,
                        "usdt_balance": usdt_balance,
                        "account_type": account_type,
                        "success": True
                    }
        if account_type == "UNIFIED":
            return get_bybit_wallet_balance(api_key, api_secret, "CONTRACT")
        return {"success": False, "usdt_balance": 0.0, "total_equity": 0.0}
    except Exception as e:
        return {"success": False, "error": str(e), "usdt_balance": 0.0}

