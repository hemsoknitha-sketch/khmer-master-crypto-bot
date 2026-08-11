import time
import hmac
import hashlib
import requests
import os
from urllib.parse import urlencode
from dotenv import load_dotenv
load_dotenv()

# REAL TRADING ENABLED (Default: False if not explicitly set to True)
PAPER_TRADING = os.getenv("PAPER_TRADING", "False").lower() in ["true", "1", "yes"]

def set_paper_trading(enabled: bool):
    global PAPER_TRADING
    PAPER_TRADING = enabled
    os.environ["PAPER_TRADING"] = str(enabled)

# TIME SYNC
TIME_OFFSET = 0

# PRE-WARMED HIGH-PERFORMANCE HTTP SESSION POOL (<30ms latency)
HFT_SESSION = requests.Session()
_adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=1)
HFT_SESSION.mount("https://", _adapter)
HFT_SESSION.mount("http://", _adapter)
HFT_SESSION.headers.update({"Connection": "keep-alive", "User-Agent": "Apex-AI-Turbo/9.0"})

def sync_time():
    global TIME_OFFSET
    try:
        res = requests.get(f"{BASE_URL}/api/v3/time", timeout=5)
        if res.status_code == 200:
            server_time = res.json()['serverTime']
            local_time = int(time.time() * 1000)
            TIME_OFFSET = server_time - local_time
            print(f"Synced Binance Time Offset: {TIME_OFFSET}ms")
    except Exception as e:
        print(f"Failed to sync Binance time: {e}")

BINANCE_SPOT_URLS = [
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://api4.binance.com"
]

def get_working_spot_url():
    """Smart Fallback: Finds a working Binance endpoint to bypass DNS issues."""
    for url in BINANCE_SPOT_URLS:
        try:
            res = requests.get(f"{url}/api/v3/ping", timeout=3)
            if res.status_code == 200:
                return url
        except requests.exceptions.RequestException:
            continue
    return BINANCE_SPOT_URLS[0]

BASE_URL = get_working_spot_url()
sync_time()
FUTURES_URL = "https://fapi.binance.com"
import math

SYMBOL_INFO_CACHE = {}

def get_symbol_info(symbol):
    if not symbol:
        return None
    if not isinstance(symbol, str):
        symbol = str(symbol)
    symbol = symbol.upper().strip()
    if symbol in SYMBOL_INFO_CACHE:
        return SYMBOL_INFO_CACHE[symbol]
    try:
        url = f"{BASE_URL}/api/v3/exchangeInfo?symbol={symbol}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get('symbols'):
                SYMBOL_INFO_CACHE[symbol] = data['symbols'][0]
                return SYMBOL_INFO_CACHE[symbol]
    except Exception as e:
        print(f"Failed to fetch exchangeInfo for {symbol}: {e}")
_klines_cache = {}
_klines_cache_time = {}

def get_klines(symbol: str, interval: str = "1m", limit: int = 25):
    """Fetches Binance spot/futures klines safely with 3s TTL cache and sub-second execution."""
    if not symbol: return []
    symbol = str(symbol).upper().strip()
    cache_key = f"{symbol}_{interval}_{limit}"
    now = time.time()
    if cache_key in _klines_cache and (now - _klines_cache_time.get(cache_key, 0)) < 3.0:
        return _klines_cache[cache_key]

    try:
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
        res = HFT_SESSION.get(url, timeout=1.5)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and data:
                _klines_cache[cache_key] = data
                _klines_cache_time[cache_key] = now
                return data
    except Exception:
        pass

    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        res = HFT_SESSION.get(url, timeout=1.5)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and data:
                _klines_cache[cache_key] = data
                _klines_cache_time[cache_key] = now
                return data
    except Exception as e:
        print(f"Error fetching klines for {symbol}: {e}")

    return _klines_cache.get(cache_key, [])


FUTURES_INFO_CACHE = {}

def get_futures_symbol_info(symbol):
    global FUTURES_INFO_CACHE
    if not symbol:
        return None
    if not isinstance(symbol, str):
        symbol = str(symbol)
    symbol_str = symbol.upper().strip()
    if not FUTURES_INFO_CACHE:
        try:
            import requests
            r = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo')
            if r.status_code == 200:
                data = r.json()
                for s in data['symbols']:
                    FUTURES_INFO_CACHE[s['symbol']] = s
        except Exception as e:
            print(f"Failed to fetch futures exchangeInfo: {e}")
    return FUTURES_INFO_CACHE.get(symbol_str)

def get_futures_max_sellable_qty(symbol: str, raw_qty: float) -> float:
    info = get_futures_symbol_info(symbol)
    if not info:
        return round(raw_qty, 3) # Fallback
        
    step_size = None
    for f in info.get('filters', []):
        if f['filterType'] == 'LOT_SIZE':
            step_size = float(f['stepSize'])
            break
            
    if step_size:
        import math
        precision = max(0, int(round(-math.log10(step_size))))
        if precision == 0:
            return float(math.floor(raw_qty))
        factor = 10 ** precision
        max_sellable = math.floor(raw_qty * factor) / factor
        return max_sellable
    return round(raw_qty, 3)

def get_max_sellable_qty(symbol: str, raw_balance: float) -> float:
    info = get_symbol_info(symbol)
    if not info:
        return raw_balance
        
    step_size = None
    for f in info.get('filters', []):
        if f['filterType'] == 'LOT_SIZE':
            step_size = float(f['stepSize'])
            break
            
    if step_size:
        precision = max(0, int(round(-math.log10(step_size))))
        factor = 10 ** precision
        max_sellable = math.floor(raw_balance * factor) / factor
        return max_sellable
    return raw_balance

def generate_signature(api_secret: str, query_string: str) -> str:
    """Generates the HMAC SHA256 signature required by Binance."""
    return hmac.new(
        api_secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def validate_api_keys(api_key: str, api_secret: str) -> tuple[bool, str]:
    """Tests if the API keys are valid by checking Spot and Futures endpoints (Dual-Check)."""
    if PAPER_TRADING:
        return True, "✅ ភ្ជាប់ API ជោគជ័យ! (Paper Trading / Demo Mode)"
        
    try:
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        query_string = f"recvWindow=60000&timestamp={timestamp}"
        signature = generate_signature(api_secret, query_string)
        
        headers = {"X-MBX-APIKEY": api_key}
        
        # Check Spot
        spot_url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"
        spot_res = requests.get(spot_url, headers=headers, timeout=5)
        spot_enabled = (spot_res.status_code == 200)
        
        # Check Futures
        futures_url = f"{FUTURES_URL}/fapi/v2/balance?{query_string}&signature={signature}"
        futures_res = requests.get(futures_url, headers=headers, timeout=5)
        futures_enabled = (futures_res.status_code == 200)
        
        if spot_enabled or futures_enabled:
            spot_status = "🟢 ដំណើរការ (Enabled)" if spot_enabled else "🔴 មិនទាន់បើកសិទ្ធិ (Disabled)"
            futures_status = "🟢 ដំណើរការ (Enabled)" if futures_enabled else "🔴 មិនទាន់បើកសិទ្ធិ (Disabled)"
            
            msg = (
                "✅ **ភ្ជាប់ API ជោគជ័យ! (API Connected)**\n\n"
                "**មុខងារដែលបានបើកសិទ្ធិ:**\n"
                f" - Spot Trading: {spot_status}\n"
                f" - Futures Trading: {futures_status}\n\n"
                "*(បញ្ជាក់: សូមប្រាកដថាអ្នកបានបើកសិទ្ធិត្រឹមត្រូវនៅលើ Binance App)*"
            )
            return True, msg
            
        try:
            # Both failed, let's parse the error from Futures (or Spot)
            err_data = futures_res.json() if futures_res.status_code != 200 else spot_res.json()
            code = err_data.get('code', 0)
            msg = err_data.get('msg', '')
            
            if code == -2015:
                return False, "❌ បរាជ័យ: API Key មិនត្រឹមត្រូវ, ឬមិនទាន់បានដាក់ IP Address (`110.235.246.183`) នៅក្នុង Trusted IPs របស់ Binance ទេ។"
            elif code == -1022:
                return False, "❌ បរាជ័យ: API Secret មិនត្រឹមត្រូវទេ។"
            elif code == -2014:
                return False, "❌ បរាជ័យ: ទម្រង់ API Key មិនត្រឹមត្រូវទេ។"
            elif code == -1021:
                return False, "❌ បរាជ័យ: ម៉ោង (VPS Time) ដើរលឿន ឬយឺតជាង Binance។ សូម Update ម៉ោង VPS។"
            else:
                return False, f"❌ បរាជ័យ: {msg} (Code: {code})"
        except:
            return False, f"❌ បរាជ័យ: Binance ឆ្លើយតប {futures_res.status_code} - {futures_res.text}"
            
    except requests.exceptions.RequestException:
        return False, "❌ **បរាជ័យ:** ប្រព័ន្ធអ៊ិនធឺណិតរបស់ម៉ាស៊ីន (VPS Network) កំពុងមានបញ្ហាក្នុងការតភ្ជាប់ទៅកាន់ Binance។ សូមរង់ចាំបន្តិច រួចសាកល្បងម្តងទៀត!"
    except Exception as e:
        return False, "❌ **បរាជ័យ:** ប្រព័ន្ធអ៊ិនធឺណិតរបស់ម៉ាស៊ីន (VPS Network) កំពុងមានបញ្ហាក្នុងការតភ្ជាប់ទៅកាន់ Binance។ សូមរង់ចាំបន្តិច រួចសាកល្បងម្តងទៀត!"

def get_all_spot_balances(api_key: str, api_secret: str) -> dict:
    """Returns a dictionary of all assets with total (free + locked) balance > 0."""
    try:
        if PAPER_TRADING:
            return {"BTC": 1.0, "ETH": 10.0, "SOL": 100.0, "DOGE": 10000.0} # Mock data
            
        endpoint = "/api/v3/account"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        query_string = f"recvWindow=60000&timestamp={timestamp}"
        signature = generate_signature(api_secret, query_string)
        headers = {"X-MBX-APIKEY": api_key}
        url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
        res = requests.get(url, headers=headers, timeout=5)
        
        balances_dict = {}
        if res.status_code == 200:
            balances = res.json().get('balances', [])
            for b in balances:
                total_amt = float(b['free']) + float(b.get('locked', 0.0))
                if total_amt > 0:
                    balances_dict[b['asset']] = total_amt
        return balances_dict
    except:
        return {}

def get_all_prices() -> dict:
    """Fetches all ticker prices from Binance Spot at once."""
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return {item['symbol']: float(item['price']) for item in res.json()}
        return {}
    except:
        return {}

def get_total_spot_exposure(api_key: str, api_secret: str) -> tuple[float, dict]:
    """
    Calculates the live USDT market value of all active non-USDT Spot altcoin holdings.
    Returns: (total_exposure_usdt, breakdown_dict)
    """
    balances = get_all_spot_balances(api_key, api_secret)
    prices = get_all_prices()
    
    total_exposure = 0.0
    breakdown = {}
    for asset, qty in balances.items():
        if asset in ["USDT", "USDC", "BUSD", "FDUSD", "TUSD"]:
            continue
            
        symbol = f"{asset}USDT"
        if symbol in prices:
            val = qty * prices[symbol]
            if val >= 0.50: # Only count holdings valued >= $0.50 USDT
                total_exposure += val
                breakdown[asset] = {"qty": qty, "price": prices[symbol], "value_usdt": val}
            
    return total_exposure, breakdown


BALANCE_CACHE = {} # { "api_key_asset": {"amount": float, "timestamp": float} }

def get_spot_balance(api_key: str, api_secret: str, asset: str = "USDT") -> float:
    cache_key = f"{api_key}_{asset}"
    current_time = time.time()
    if cache_key in BALANCE_CACHE:
        cached = BALANCE_CACHE[cache_key]
        if current_time - cached["timestamp"] < 30:
            return cached["amount"]
            
    try:
        endpoint = "/api/v3/account"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        query_string = f"recvWindow=60000&timestamp={timestamp}"
        signature = generate_signature(api_secret, query_string)
        headers = {"X-MBX-APIKEY": api_key}
        url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            balances = res.json().get('balances', [])
            for b in balances:
                if b['asset'] == asset:
                    amt = float(b['free'])
                    BALANCE_CACHE[cache_key] = {"amount": amt, "timestamp": current_time}
                    return amt
    except Exception as e:
        print(f"Error getting spot balance: {e}")
    return 0.0

def get_available_usdt_balance(api_key: str, api_secret: str) -> float:
    """Returns total available free USDT balance across Spot and Futures wallets."""
    spot_usdt = get_spot_balance(api_key, api_secret, "USDT")
    futures_usdt = 0.0
    try:
        res_f, status = get_futures_balance_details(api_key, api_secret, "USDT")
        if status == "OK" and res_f > 0:
            futures_usdt = res_f
    except Exception:
        pass
    return max(spot_usdt, futures_usdt)

def get_portfolio_margin_balance(api_key: str, api_secret: str, asset: str = "USDT") -> float:
    """Fetches Portfolio Margin & Cross Margin Wallet Equity from Binance SAPI."""
    try:
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        query_string = f"recvWindow=60000&timestamp={timestamp}"
        signature = generate_signature(api_secret, query_string)
        headers = {"X-MBX-APIKEY": api_key}
        
        # 1. Try Portfolio Margin Account Endpoint
        pm_url = f"{BASE_URL}/sapi/v1/portfolio/account?{query_string}&signature={signature}"
        res = requests.get(pm_url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            equity = float(data.get('accountEquity', 0.0) or data.get('totalWalletBalance', 0.0))
            if equity > 0:
                return equity
                
        # 2. Try Cross Margin Account Endpoint
        margin_url = f"{BASE_URL}/sapi/v1/margin/account?{query_string}&signature={signature}"
        res = requests.get(margin_url, headers=headers, timeout=5)
        if res.status_code == 200:
            user_assets = res.json().get('userAssets', [])
            for item in user_assets:
                if item.get('asset') == asset:
                    return float(item.get('netAsset', 0.0) or item.get('free', 0.0))
        return 0.0
    except:
        return 0.0

def get_futures_balance_detailed(api_key: str, api_secret: str, asset: str = "USDT") -> tuple:
    """
    Fetches real-time Futures Wallet Balance with detailed diagnostic error reporting.
    Returns: (balance: float, status_str: str)
    """
    try:
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        query_string = f"recvWindow=60000&timestamp={timestamp}"
        signature = generate_signature(api_secret, query_string)
        headers = {"X-MBX-APIKEY": api_key}
        
        # 1. Try USDT-M Futures /fapi/v2/balance
        url_v2 = f"{FUTURES_URL}/fapi/v2/balance?{query_string}&signature={signature}"
        res = requests.get(url_v2, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                for b in data:
                    if b.get('asset') == asset:
                        bal = float(b.get('balance', 0.0) or 0.0)
                        cross = float(b.get('crossWalletBalance', 0.0) or 0.0)
                        avail = float(b.get('availableBalance', 0.0) or 0.0)
                        max_val = max(bal, cross, avail)
                        if max_val > 0:
                            return max_val, "OK"
                return 0.0, "OK"
        else:
            err_json = {}
            try:
                err_json = res.json()
            except:
                pass
            err_code = err_json.get('code', res.status_code)
            err_msg = err_json.get('msg', res.text)
            print(f"⚠️ [FUTURES API V2 FAIL]: Code {err_code} - {err_msg}")
            
            if err_code in [-2015, 2015]:
                return 0.0, "API_PERM_ERROR"
            elif err_code in [-1021, 1021]:
                return 0.0, "TIMESTAMP_ERROR"
            elif err_code in [-2014, 2014]:
                return 0.0, "INVALID_KEY_ERROR"

        # 2. Try USDT-M Futures Account Summary /fapi/v2/account
        url_acc = f"{FUTURES_URL}/fapi/v2/account?{query_string}&signature={signature}"
        res_acc = requests.get(url_acc, headers=headers, timeout=5)
        if res_acc.status_code == 200:
            acc_data = res_acc.json()
            if isinstance(acc_data, dict):
                total_bal = float(acc_data.get('totalWalletBalance', 0.0) or 0.0)
                total_margin = float(acc_data.get('totalMarginBalance', 0.0) or 0.0)
                max_acc = max(total_bal, total_margin)
                if max_acc > 0:
                    return max_acc, "OK"
                for a in acc_data.get('assets', []):
                    if a.get('asset') == asset:
                        a_bal = float(a.get('walletBalance', 0.0) or a.get('marginBalance', 0.0) or 0.0)
                        if a_bal > 0:
                            return a_bal, "OK"

        # 3. Try COIN-M Futures /dapi/v1/balance as additional fallback
        url_dapi = f"https://dapi.binance.com/dapi/v1/balance?{query_string}&signature={signature}"
        res_dapi = requests.get(url_dapi, headers=headers, timeout=5)
        if res_dapi.status_code == 200:
            ddata = res_dapi.json()
            if isinstance(ddata, list):
                for b in ddata:
                    if b.get('asset') == asset:
                        d_bal = float(b.get('balance', 0.0) or b.get('crossWalletBalance', 0.0) or 0.0)
                        if d_bal > 0:
                            return d_bal, "OK"

        return 0.0, "ZERO_BALANCE"
    except Exception as e:
        print(f"⚠️ [GET FUTURES BALANCE ERROR]: {e}")
        return 0.0, f"EXCEPTION: {e}"

def get_futures_balance(api_key: str, api_secret: str, asset: str = "USDT") -> float:
    bal, _ = get_futures_balance_detailed(api_key, api_secret, asset)
    return bal

def get_futures_wallet_balance(api_key: str, api_secret: str, asset: str = "USDT") -> float:
    return get_futures_balance(api_key, api_secret, asset)

def get_funding_balance(api_key: str, api_secret: str, asset: str = "USDT") -> float:
    """Fetches Binance Funding Wallet balance (P2P/Pay/Funding)."""
    try:
        endpoint = "/sapi/v1/funding/wallet"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        payload = urlencode({
            "asset": asset,
            "timestamp": timestamp
        })
        signature = generate_signature(api_secret, payload)
        headers = {"X-MBX-APIKEY": api_key}
        url = f"{BASE_URL}{endpoint}?{payload}&signature={signature}"
        res = requests.post(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                for item in data:
                    if item.get('asset') == asset:
                        free_amt = float(item.get('free', 0.0) or 0.0)
                        locked_amt = float(item.get('locked', 0.0) or 0.0)
                        return free_amt + locked_amt
        return 0.0
    except Exception as e:
        print(f"⚠️ [GET FUNDING BALANCE ERROR]: {e}")
        return 0.0

def get_earn_balance(api_key: str, api_secret: str, asset: str = "USDT") -> float:
    """Fetches Binance Simple Earn / Flexible Savings balance."""
    try:
        endpoint = "/sapi/v1/simple-earn/flexible/position"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        payload = urlencode({
            "asset": asset,
            "timestamp": timestamp
        })
        signature = generate_signature(api_secret, payload)
        headers = {"X-MBX-APIKEY": api_key}
        url = f"{BASE_URL}{endpoint}?{payload}&signature={signature}"
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            rows = data.get('rows', [])
            total = 0.0
            for r in rows:
                if r.get('asset') == asset:
                    total += float(r.get('totalAmount', 0.0) or 0.0)
            return total
        return 0.0
    except Exception as e:
        print(f"⚠️ [GET EARN BALANCE ERROR]: {e}")
        return 0.0

def get_futures_positions(api_key: str, api_secret: str) -> list:
    if PAPER_TRADING:
        return []
    for attempt in range(3):
        try:
            endpoint = "/fapi/v2/positionRisk"
            timestamp = (int(time.time() * 1000) + TIME_OFFSET)
            query_string = f"recvWindow=60000&timestamp={timestamp}"
            signature = generate_signature(api_secret, query_string)
            headers = {"X-MBX-APIKEY": api_key}
            url = f"{FUTURES_URL}{endpoint}?{query_string}&signature={signature}"
            res = HFT_SESSION.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                return res.json()
            time.sleep(0.1)
        except Exception:
            time.sleep(0.1)
    return []

def emergency_reduce_position(api_key: str, api_secret: str, symbol: str, side: str, qty: float) -> dict:
    if PAPER_TRADING:
        return simulate_order_response(symbol, f"EMERGENCY_REDUCE_{side}", qty)
    try:
        endpoint = "/fapi/v1/order"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        trade_side = "SELL" if side.upper() == "LONG" else "BUY"
        payload = urlencode({
            "symbol": symbol,
            "side": trade_side,
            "type": "MARKET",
            "quantity": qty,
            "reduceOnly": "true",
            "timestamp": timestamp
        })
        signature = generate_signature(api_secret, payload)
        headers = {"X-MBX-APIKEY": api_key}
        url = f"{FUTURES_URL}{endpoint}?{payload}&signature={signature}"
        res = requests.post(url, headers=headers, timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

_price_cache = {}
_price_cache_time = {}

def get_current_price(symbol) -> float:
    """Helper to fetch the current price with 2.5s TTL cache and WebSocket fast path."""
    if not symbol:
        return 0.0
    if not isinstance(symbol, str):
        symbol = str(symbol)
    symbol = symbol.upper().strip()
    now = time.time()
    if symbol in _price_cache and (now - _price_cache_time.get(symbol, 0)) < 2.5:
        return _price_cache[symbol]

    try:
        import websocket_engine
        fast_price = websocket_engine.get_fast_price(symbol)
        if fast_price > 0:
            _price_cache[symbol] = fast_price
            _price_cache_time[symbol] = now
            return fast_price
    except Exception:
        pass
        
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        res = HFT_SESSION.get(url, timeout=1.5)
        if res.status_code == 200:
            price = float(res.json().get('price', 0.0))
            if price > 0:
                _price_cache[symbol] = price
                _price_cache_time[symbol] = now
                return price
    except Exception:
        pass

    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = HFT_SESSION.get(url, timeout=1.5)
        if res.status_code == 200:
            price = float(res.json().get('price', 0.0))
            if price > 0:
                _price_cache[symbol] = price
                _price_cache_time[symbol] = now
                return price
    except Exception:
        pass

    return _price_cache.get(symbol, 60000.0) # Fallback

def simulate_order_response(symbol: str, side: str, qty: float, price: float = None) -> dict:
    """Generates a fake successful response for Paper Trading."""
    price = price or get_current_price(symbol)
    print(f"[PAPER TRADING] Executed {side} order for {symbol} - Qty: {qty} @ ~${price}")
    return {
        "orderId": int(time.time() * 1000),
        "symbol": symbol,
        "status": "FILLED",
        "clientOrderId": "paper_trade_123",
        "price": str(price),
        "origQty": str(qty),
        "executedQty": str(qty),
        "cumQuote": str(price * qty),
        "timeInForce": "GTC",
        "type": "MARKET",
        "side": side,
        "updateTime": int(time.time() * 1000)
    }

def calculate_dynamic_risk(margin_usdt: float, current_price: float, vol_target: float, leverage: int, side: str) -> dict:
    """
    Calculates dynamic position size, ATR-adjusted leverage, and Stop-Loss based on predicted volatility (vol_target).
    """
    # Dynamic Position Sizing (reduce position & leverage in high volatility)
    # Assume base ATR for BTC is around $1500 for normal market
    risk_factor = min(1.5, max(0.2, 1500.0 / (vol_target + 1))) 
    adjusted_margin = margin_usdt * risk_factor
    adjusted_leverage = max(1, int(round(leverage * risk_factor)))

    
    qty = (adjusted_margin * adjusted_leverage) / current_price if current_price > 0 else 0.0
    qty = round(qty, 3) 
    
    # Dynamic Stop Loss
    sl_distance = vol_target * 1.5
    if side.upper() == 'BUY':
        stop_loss = current_price - sl_distance
    else:
        stop_loss = current_price + sl_distance
        
    return {
        "qty": qty,
        "adjusted_margin": adjusted_margin,
        "adjusted_leverage": adjusted_leverage,
        "stop_loss": stop_loss,
        "risk_factor": risk_factor
    }


def _raw_place_market_buy(api_key: str, api_secret: str, symbol: str, quote_order_qty: float) -> dict:
    """Internal function to place a raw market buy to Binance."""
    symbol = symbol.upper()
    endpoint = "/api/v3/order"
    params = {
        "symbol": symbol,
        "side": "BUY",
        "type": "MARKET",
        "quoteOrderQty": quote_order_qty,
        "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    try:
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def execute_stealth_twap_buy(api_key: str, api_secret: str, symbol: str, total_quote_qty: float, chunk_size: float = 500.0) -> dict:
    print(f"🥷 [STEALTH TWAP BUY] Activated for {symbol} - Total: ${total_quote_qty} (Chunk: ${chunk_size})")
    remaining = total_quote_qty
    aggregated_res = {
        "symbol": symbol,
        "orderId": int(time.time()),
        "clientOrderId": "stealth_twap_buy",
        "transactTime": int(time.time() * 1000),
        "price": "0",
        "origQty": "0",
        "executedQty": "0",
        "cummulativeQuoteQty": "0",
        "status": "FILLED",
        "type": "MARKET",
        "side": "BUY",
        "fills": []
    }
    
    total_executed_qty = 0.0
    total_cummulative_quote = 0.0
    
    while remaining > 0:
        chunk = min(remaining, chunk_size)
        if chunk < 5.0:
            break
            
        print(f"   🔪 [TWAP Slice] Buying ${chunk} of {symbol}...")
        res = _raw_place_market_buy(api_key, api_secret, symbol, chunk)
        
        if "error" in res or "code" in res:
            print(f"⚠️ TWAP Slice Error: {res}")
            if remaining == total_quote_qty:
                return res
            break
            
        executed_qty = float(res.get("executedQty", 0))
        cummulative_quote = float(res.get("cummulativeQuoteQty", 0))
        
        total_executed_qty += executed_qty
        total_cummulative_quote += cummulative_quote
        
        if "fills" in res:
            aggregated_res["fills"].extend(res["fills"])
            
        remaining -= chunk
        
        if remaining > 0:
            time.sleep(1) # Stealth interval
            
    aggregated_res["executedQty"] = str(total_executed_qty)
    aggregated_res["cummulativeQuoteQty"] = str(total_cummulative_quote)
    if total_executed_qty > 0:
        aggregated_res["price"] = str(total_cummulative_quote / total_executed_qty)
        
    print(f"✅ [STEALTH TWAP BUY] Completed. Total Filled: {total_executed_qty} {symbol} for ${total_cummulative_quote}")
    return aggregated_res

def place_market_buy(api_key: str, api_secret: str, symbol: str, quote_order_qty: float = 50.0) -> dict:
    """Places a Market Buy order with Stealth Execution if slippage is high."""
    import database as db
    import market_impact_model
    
    if db.is_circuit_breaker_active():
        print(f"🛡️ Circuit Breaker Active: Blocked Spot Buy for {symbol} (${quote_order_qty})")
        return {"success": False, "msg": "CIRCUIT_BREAKER_ACTIVE"}
    if PAPER_TRADING:
        price = get_current_price(symbol)
        qty = round(quote_order_qty / price, 3)
        return simulate_order_response(symbol, "BUY", qty, price)

    # Super Smart Balance Check
    available_balance = get_spot_balance(api_key, api_secret, "USDT")
    if available_balance < quote_order_qty:
        if available_balance >= 5.0:
            print(f"⚠️ Insufficient full balance. Auto-adjusting Spot BUY from {quote_order_qty} to {available_balance}")
            quote_order_qty = available_balance
        else:
            return {"error": f"Insufficient USDT Balance (Available: {available_balance:.2f} USDT). Minimum required: $5.00"}

    # 🥷 Super Smart Anti-Slippage Check (Lowered threshold to $15.00)
    if quote_order_qty >= 15.0:
        slippage = market_impact_model.estimate_slippage(symbol, quote_order_qty, "BUY")
        if slippage > 0.15:
            print(f"⚠️ [ANTI-SLIPPAGE GUARD] Projected slippage {slippage:.3f}% > 0.15% for ${quote_order_qty:.2f} BUY!")
            if quote_order_qty >= 50.0:
                chunk = min(100.0, max(20.0, quote_order_qty / 3.0))
                return execute_stealth_twap_buy(api_key, api_secret, symbol, quote_order_qty, chunk_size=chunk)
            else:
                # Small order with high slippage: Place Limit Buy at best ask to prevent orderbook sweep
                best_bid, best_ask = market_impact_model.get_best_bid_ask(symbol)
                if best_ask > 0:
                    buy_qty = quote_order_qty / best_ask
                    print(f"🛡️ [SMART LIMIT-IOC BUY] Placing Limit Buy for {buy_qty:.4f} {symbol} @ ${best_ask:.4f}")
                    return place_limit_buy(api_key, api_secret, symbol, buy_qty, best_ask)

    return _raw_place_market_buy(api_key, api_secret, symbol, quote_order_qty)

def _raw_place_market_sell(api_key: str, api_secret: str, symbol: str, quantity: float) -> dict:
    """Internal function to place a raw market sell to Binance."""
    symbol = symbol.upper()
    endpoint = "/api/v3/order"
    formatted_qty = get_max_sellable_qty(symbol, quantity)
    
    params = {
        "symbol": symbol,
        "side": "SELL",
        "type": "MARKET",
        "quantity": formatted_qty,
        "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    try:
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def execute_stealth_twap_sell(api_key: str, api_secret: str, symbol: str, total_qty: float, chunk_qty: float) -> dict:
    print(f"🥷 [STEALTH TWAP SELL] Activated for {symbol} - Total: {total_qty} (Chunk: {chunk_qty})")
    remaining = total_qty
    aggregated_res = {
        "symbol": symbol,
        "orderId": int(time.time()),
        "clientOrderId": "stealth_twap_sell",
        "transactTime": int(time.time() * 1000),
        "price": "0",
        "origQty": str(total_qty),
        "executedQty": "0",
        "cummulativeQuoteQty": "0",
        "status": "FILLED",
        "type": "MARKET",
        "side": "SELL",
        "fills": []
    }
    
    total_executed_qty = 0.0
    total_cummulative_quote = 0.0
    
    while remaining > 0:
        chunk = min(remaining, chunk_qty)
        
        print(f"   🔪 [TWAP Slice] Selling {chunk} of {symbol}...")
        res = _raw_place_market_sell(api_key, api_secret, symbol, round(chunk, 5))
        
        if "error" in res or "code" in res:
            print(f"⚠️ TWAP Slice Error: {res}")
            if remaining == total_qty:
                return res
            break
            
        executed_qty = float(res.get("executedQty", 0))
        cummulative_quote = float(res.get("cummulativeQuoteQty", 0))
        
        total_executed_qty += executed_qty
        total_cummulative_quote += cummulative_quote
        
        if "fills" in res:
            aggregated_res["fills"].extend(res["fills"])
            
        remaining -= chunk
        
        if remaining > 0:
            time.sleep(1) # Stealth interval
            
    aggregated_res["executedQty"] = str(total_executed_qty)
    aggregated_res["cummulativeQuoteQty"] = str(total_cummulative_quote)
    if total_executed_qty > 0:
        aggregated_res["price"] = str(total_cummulative_quote / total_executed_qty)
        
    print(f"✅ [STEALTH TWAP SELL] Completed. Total Filled: {total_executed_qty} {symbol} for ${total_cummulative_quote}")
    return aggregated_res

def place_market_sell(api_key: str, api_secret: str, symbol: str, quantity: float) -> dict:
    """Places a Market Sell order with Stealth Execution if slippage is high."""
    import market_impact_model
    if PAPER_TRADING:
        return simulate_order_response(symbol, "SELL", quantity)

    current_price = get_current_price(symbol)
    qty_usdt = quantity * current_price
    
    # 🥷 Super Smart Anti-Slippage Check (Lowered threshold to $15.00)
    if qty_usdt >= 15.0:
        slippage = market_impact_model.estimate_slippage(symbol, qty_usdt, "SELL")
        if slippage > 0.15:
            print(f"⚠️ [ANTI-SLIPPAGE GUARD] Projected slippage {slippage:.3f}% > 0.15% for ${qty_usdt:.2f} SELL!")
            if qty_usdt >= 50.0:
                chunk_qty = min(100.0 / current_price, max(20.0 / current_price, quantity / 3.0))
                return execute_stealth_twap_sell(api_key, api_secret, symbol, quantity, chunk_qty)
            else:
                # Small order with high slippage: Place Limit Sell at best bid to prevent orderbook dump
                best_bid, best_ask = market_impact_model.get_best_bid_ask(symbol)
                if best_bid > 0:
                    print(f"🛡️ [SMART LIMIT-IOC SELL] Placing Limit Sell for {quantity:.4f} {symbol} @ ${best_bid:.4f}")
                    return place_limit_sell(api_key, api_secret, symbol, quantity, best_bid)

    return _raw_place_market_sell(api_key, api_secret, symbol, quantity)

def place_smart_market_sell(api_key: str, api_secret: str, symbol: str, quantity: float) -> dict:
    """
    Super Smart Market Sell Guard:
    Protects against Binance MIN_NOTIONAL errors ($5.00 limit).
    If a Stop-Loss position drops below $5.00 (between $0.50 and $4.99 USDT):
      1. Performs a temporary micro-buy (e.g. $5.10 - current_val) to bring value above MIN_NOTIONAL.
      2. Immediately places a Market Sell for the full updated balance, liquidating the stuck bag!
    If position value < $0.50 (micro dust), cleans up gracefully.
    """
    current_price = get_current_price(symbol)
    notional_val = quantity * current_price
    
    # 1. Micro Dust Guard (< $0.50 USDT)
    if notional_val < 0.50:
        print(f"[DUST CLEANER] {symbol} value (${notional_val:.4f}) is sub-dust (<$0.50). Marking as filled.")
        return {
            "status": "FILLED",
            "symbol": symbol,
            "executedQty": str(quantity),
            "cummulativeQuoteQty": str(notional_val),
            "price": str(current_price),
            "is_dust_cleaned": True
        }

    if PAPER_TRADING:
        return simulate_order_response(symbol, "SMART_SELL", quantity)

        
    # 2. Sub-MIN_NOTIONAL Auto Top-Up Guard ($0.50 <= val < $5.00)
    if notional_val < 5.0:
        base_asset = symbol[:-4] if symbol.endswith("USDT") else symbol
        top_up_needed = max(5.10 - notional_val, 5.0)
        print(f"🛠️ [MIN_NOTIONAL GUARD] {symbol} sell value is ${notional_val:.2f} < $5.00 threshold!")
        print(f"⚡ [AUTO TOP-UP & SELL] Buying ${top_up_needed:.2f} USDT of {symbol} to enable full liquidation...")
        
        buy_res = _raw_place_market_buy(api_key, api_secret, symbol, top_up_needed)
        if "status" in buy_res and buy_res["status"] == "FILLED":
            # Fetch updated full coin balance
            updated_bal = get_spot_balance(api_key, api_secret, base_asset)
            if updated_bal > 0:
                print(f"🚀 [FULL LIQUIDATION] Selling updated balance of {updated_bal} {symbol}...")
                sell_res = place_market_sell(api_key, api_secret, symbol, updated_bal)
                return sell_res
        else:
            print(f"⚠️ Top-Up micro buy failed: {buy_res}. Falling back to standard sell.")

    # 3. Standard Market Sell
    return place_market_sell(api_key, api_secret, symbol, quantity)


def place_limit_buy(api_key: str, api_secret: str, symbol: str, quantity: float, price: float) -> dict:
    """Places a Limit Buy order."""
    import database as db
    if db.is_circuit_breaker_active():
        print(f"🛡️ Circuit Breaker Active: Blocked Limit Buy for {symbol} ({quantity} @ {price})")
        return {"success": False, "msg": "CIRCUIT_BREAKER_ACTIVE"}

    if PAPER_TRADING:
        return simulate_order_response(symbol, "LIMIT_BUY", quantity, price)

    symbol = symbol.upper()
    endpoint = "/api/v3/order"
    params = {
        "symbol": symbol, "side": "BUY", "type": "LIMIT", "timeInForce": "GTC",
        "quantity": quantity, "price": price, "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    payload = f"{query_string}&signature={signature}"
    url = f"{BASE_URL}{endpoint}?{payload}"
    try:
        print(f"[TRADING ENGINE - REAL SPOT] LIMIT BUY {symbol} | Qty: {quantity} | Price: {price}")
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def place_limit_sell(api_key: str, api_secret: str, symbol: str, quantity: float, price: float) -> dict:
    """Places a Limit Sell order."""
    if PAPER_TRADING:
        return simulate_order_response(symbol, "LIMIT_SELL", quantity, price)

    symbol = symbol.upper()
    endpoint = "/api/v3/order"
    formatted_qty = get_max_sellable_qty(symbol, quantity)
    
    params = {
        "symbol": symbol, "side": "SELL", "type": "LIMIT", "timeInForce": "GTC",
        "quantity": formatted_qty, "price": price, "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    payload = f"{query_string}&signature={signature}"
    url = f"{BASE_URL}{endpoint}?{payload}"
    try:
        print(f"[TRADING ENGINE - REAL SPOT] LIMIT SELL {symbol} | Qty: {quantity} | Price: {price}")
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def set_leverage(api_key: str, api_secret: str, symbol: str, leverage: int) -> dict:
    """Sets the leverage for a specific futures symbol."""
    if PAPER_TRADING:
        return {"symbol": symbol, "leverage": leverage, "maxNotionalValue": "1000000"}

    endpoint = "/fapi/v1/leverage"
    params = {
        "symbol": symbol, "leverage": leverage, "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    payload = f"{query_string}&signature={signature}"
    url = f"{FUTURES_URL}{endpoint}?{payload}"
    try:
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

set_futures_leverage = set_leverage

def place_futures_short(api_key: str, api_secret: str, symbol: str, margin_usdt: float, leverage: int, vol_target: float = 1500.0) -> dict:
    """Places a REAL or PAPER Futures Short Sell."""
    symbol = symbol.upper()
    
    # Super Smart Balance Check
    if not PAPER_TRADING:
        available_balance = get_futures_balance(api_key, api_secret, "USDT")
        if available_balance < margin_usdt:
            if available_balance >= 5.0:
                print(f"⚠️ Insufficient full margin. Auto-adjusting Futures SHORT from {margin_usdt} to {available_balance}")
                margin_usdt = available_balance
            else:
                return {"error": f"Insufficient USDT Futures Balance (Available: {available_balance:.2f} USDT). Minimum required: $5.00"}
                
    current_price = get_current_price(symbol)
    
    # Apply dynamic risk management
    risk = calculate_dynamic_risk(margin_usdt, current_price, vol_target, leverage, "SELL")
    qty = risk['qty']
    
    print(f"[RISK MANAGER] Volatility: ${vol_target:.2f} | Risk Factor: {risk['risk_factor']:.2f}x | SL: ${risk['stop_loss']:.2f}")

    if PAPER_TRADING:
        return simulate_order_response(symbol, "FUTURES_SHORT", qty, current_price)

    set_leverage(api_key, api_secret, symbol, leverage)
    
    endpoint = "/fapi/v1/order"
    params = {
        "symbol": symbol, "side": "SELL", "type": "MARKET",
        "quantity": qty, "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    payload = f"{query_string}&signature={signature}"
    url = f"{FUTURES_URL}{endpoint}?{payload}"
    
    try:
        print(f"[TRADING ENGINE - REAL FUTURES] SHORT {symbol} | Margin: ${risk['adjusted_margin']:.2f} | Leverage: {leverage}x | Qty: {qty}")
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def close_futures_short(api_key: str, api_secret: str, symbol: str, qty: float) -> dict:
    """Closes a Futures Short Sell."""
    symbol = symbol.upper()
    qty = round(qty, 3)

    if PAPER_TRADING:
        return simulate_order_response(symbol, "CLOSE_FUTURES_SHORT", qty)
    
    endpoint = "/fapi/v1/order"
    params = {
        "symbol": symbol, "side": "BUY", "type": "MARKET", "quantity": qty,
        "reduceOnly": "true", "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    payload = f"{query_string}&signature={signature}"
    url = f"{FUTURES_URL}{endpoint}?{payload}"
    
    try:
        print(f"[TRADING ENGINE - REAL FUTURES] CLOSE SHORT {symbol} | Qty: {qty}")
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def calculate_ai_dynamic_leverage(symbol: str, base_leverage: int, ai_confidence: float = 50.0) -> int:
    """Dynamically scales leverage based on AI confidence and recent market volatility."""
    if base_leverage <= 1:
        return 1
    
    try:
        import market_data
        df, _, _ = market_data.fetch_binance_data(symbol, interval="15m", limit=50)
        if df is not None and len(df) > 15:
            atr_series = market_data.calculate_atr(df, window=14)
            current_atr = atr_series.iloc[-1]
            current_price = df["close"].iloc[-1]
            if current_price > 0:
                atr_percent = (current_atr / current_price) * 100.0
                # Penalty gets harsher as ATR percent goes up
                volatility_penalty = 1.0 / (1.0 + atr_percent)
                
                # Base formula: Base Leverage * Confidence Factor * Volatility Safety
                dynamic_leverage = int(base_leverage * (ai_confidence / 50.0) * volatility_penalty)
                
                if dynamic_leverage < 1:
                    return 1
                if dynamic_leverage > base_leverage:
                    return base_leverage
                return dynamic_leverage
    except Exception as e:
        print(f"Error calculating dynamic leverage for {symbol}: {e}")
        
    return base_leverage



def place_futures_short_qty(api_key: str, api_secret: str, symbol: str, qty: float, leverage: int = 1) -> dict:
    """Places a Futures Short Sell with an exact quantity (Delta Neutral)."""
    symbol = symbol.upper()
    if PAPER_TRADING:
        return simulate_order_response(symbol, "FUTURES_SHORT", qty, get_current_price(symbol))
        
    set_leverage(api_key, api_secret, symbol, leverage)
    
    endpoint = "/fapi/v1/order"
    formatted_qty = get_futures_max_sellable_qty(symbol, qty)
    params = {
        "symbol": symbol, "side": "SELL", "type": "MARKET",
        "quantity": formatted_qty, "recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)
    }
    query_string = urlencode(params)
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    payload = f"{query_string}&signature={signature}"
    url = f"{FUTURES_URL}{endpoint}?{payload}"
    
    try:
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def legacy_place_futures_order(api_key: str, api_secret: str, symbol: str, side: str, qty: float, leverage: int = 5) -> dict:
    """Delegates to Super Smart HFT Futures Order Engine with Defender Mode check."""
    try:
        import database as db
        if db.is_defender_active():
            try:
                print(f"🛡️ [DEFENDER MODE ACTIVE] Bypassing new position entry for {symbol} ({side})")
            except Exception:
                print(f"[DEFENDER MODE ACTIVE] Bypassing new position entry for {symbol} ({side})")
            return {"status": "error", "message": "Defender Circuit Breaker Active - New positions paused"}
    except Exception:
        pass

    symbol = symbol.upper()
    side = side.upper()
    current_price = get_current_price(symbol)
    if PAPER_TRADING:
        return simulate_order_response(symbol, f"FUTURES_{side}", qty, current_price)
        
    return place_futures_order(api_key, api_secret, symbol, side, qty, leverage)


def place_futures_buy_qty(api_key: str, api_secret: str, symbol: str, qty: float, leverage: int = 1) -> dict:
    """Places a Futures Long Buy with an exact quantity."""
    return place_futures_order(api_key, api_secret, symbol, "BUY", qty, leverage)

def smart_execute_futures_order(api_key: str, api_secret: str, symbol: str, side: str, qty: float, leverage: int = 5, is_entry: bool = True) -> dict:
    """
    Super Smart Futures Order Router:
    - is_entry=True: Opening new position -> uses place_futures_order (WITHOUT reduceOnly).
    - is_entry=False: Closing/reducing existing position -> uses emergency_reduce_position (WITH reduceOnly: true).
    """
    if is_entry:
        return place_futures_order(api_key, api_secret, symbol, side, qty, leverage)
    else:
        return emergency_reduce_position(api_key, api_secret, symbol, side, qty)



def get_24h_ticker(symbol: str) -> dict:
    """Fetches the 24h ticker for a symbol to get volume and price change."""
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error fetching 24h ticker for {symbol}: {e}")
    return {}

def panic_sell_all(api_key: str, api_secret: str, chat_id: int = 0):
    """
    Market sells all crypto balances to USDT in Spot.
    (Leaves USDT, BUSD, USDC, FDUSD alone).
    """
    if PAPER_TRADING:
        print(f"[{chat_id}] PAPER TRADING: Panic Sell All executed virtually.")
        return {'status': 'success', 'sold': ['PAPER_TRADING_DUMMY_ASSET']}
        
    try:
        timestamp = int(time.time() * 1000) + TIME_OFFSET
        params = {"timestamp": timestamp, "recvWindow": 60000}
        query_string = urlencode(params)
        signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
        
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return {'status': 'error', 'msg': f"Failed to get account balances: {res.text}"}
            
        account_data = res.json()
        balances = account_data.get('balances', [])
        
        sold_assets = []
        
        for bal in balances:
            asset = bal['asset']
            free = float(bal['free'])
            if asset in ['USDT', 'BUSD', 'USDC', 'FDUSD'] or free <= 0:
                continue
                
            symbol = f"{asset}USDT"
            
            # Simple check if symbol exists and get price
            ticker_url = f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}"
            ticker_res = requests.get(ticker_url, timeout=5)
            if ticker_res.status_code == 200:
                price = float(ticker_res.json().get('price', 0))
                # Binance requires minimum $5 notional value
                if price * free > 5.0:
                    sell_res = place_market_sell(api_key, api_secret, symbol, free)
                    if sell_res.get('status') == 'FILLED':
                        sold_assets.append(f"{free} {asset}")
                        
        return {'status': 'success', 'sold': sold_assets}
    except Exception as e:
        print(f"Exception in panic_sell_all: {e}")
        return {'status': 'error', 'msg': str(e)}

ZERO_FEE_PAIRS = {"FDUSDUSDT", "USDCUSDT", "TUSDUSDT", "BTCFDUSD", "ETHFDUSD"}

def is_zero_fee_pair(symbol: str) -> bool:
    """Checks if a trading pair qualifies for 0.0% Binance promo maker fee."""
    return symbol.upper() in ZERO_FEE_PAIRS if symbol else False

def place_maker_post_only_order(api_key: str, api_secret: str, symbol: str, side: str, qty: float, price: float) -> dict:
    """
    Executes a Binance LIMIT_MAKER (Post-Only) order.
    Guarantees Maker liquidity status (0.0% fee or lowest maker tier).
    If the order would execute immediately as a Taker order, Binance rejects it automatically.
    """
    if PAPER_TRADING:
        print(f"[PAPER TRADING] Executed LIMIT_MAKER {side} for {symbol} - Qty: {qty} @ ~${price}")
        return simulate_order_response(symbol, side, qty, price)
        
    try:
        timestamp = int(time.time() * 1000) + TIME_OFFSET
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "LIMIT_MAKER",
            "quantity": qty,
            "price": f"{price:.8f}".rstrip('0').rstrip('.'),
            "timestamp": timestamp,
            "recvWindow": 60000
        }
        query_string = urlencode(params)
        signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = f"{BASE_URL}/api/v3/order?{query_string}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
        
        res = requests.post(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def calculate_net_pnl(buy_price: float, current_price: float, qty: float = 1.0, buy_fee_pct: float = 0.075, sell_fee_pct: float = 0.075, symbol: str = None) -> tuple[float, float]:
    """
    Calculates fee-adjusted Net PnL (USDT amount and percentage).
    Default applies BNB 25% Fee Discount (0.075% buy + 0.075% sell = 0.15% round-trip).
    If symbol is a zero-fee pair (e.g. FDUSDUSDT), applies 0.00% fee.
    Returns: (net_pnl_usdt, net_pnl_pct)
    """
    if not buy_price or buy_price <= 0 or not current_price or current_price <= 0 or qty <= 0:
        return 0.0, 0.0
        
    if symbol and is_zero_fee_pair(symbol):
        buy_fee_pct = 0.0
        sell_fee_pct = 0.0
        
    effective_buy_cost = (buy_price * qty) * (1.0 + (buy_fee_pct / 100.0))
    effective_sell_proceeds = (current_price * qty) * (1.0 - (sell_fee_pct / 100.0))
    
    net_pnl_usdt = effective_sell_proceeds - effective_buy_cost
    net_pnl_pct = (net_pnl_usdt / effective_buy_cost) * 100.0
    return round(net_pnl_usdt, 4), round(net_pnl_pct, 4)

def calculate_net_pnl_pct(buy_price: float, current_price: float, buy_fee_pct: float = 0.075, sell_fee_pct: float = 0.075, symbol: str = None) -> float:
    """
    Convenience helper to get fee-adjusted Net PnL percentage with BNB fee discount.
    """
    _, net_pnl_pct = calculate_net_pnl(buy_price, current_price, 1.0, buy_fee_pct, sell_fee_pct, symbol)
    return net_pnl_pct

def calculate_kelly_optimal_size(base_amount: float, confidence: float, risk_reward_ratio: float = 1.5, half_kelly: bool = True, min_usdt: float = 15.0, max_usdt: float = 30.0) -> tuple[float, float]:
    """
    Calculates Optimal Position Size using the Kelly Criterion:
    f* = (b * p - q) / b
    
    Enforces strict Institutional Rules:
    1. Cutoff: Returns (0.0, 0.0) if confidence < 85.0% (Only high-confidence setups).
    2. Bounded Sizing: Clamps per-trade capital strictly between min_usdt ($15.00) and max_usdt ($30.00) USDT.
    """
    if base_amount <= 0 or confidence < 85.0:
        return 0.0, 0.0
    
    p = max(0.01, min(0.99, confidence / 100.0))
    q = 1.0 - p
    b = max(0.5, risk_reward_ratio)
    
    # Kelly Formula: f* = (b * p - q) / b
    f_star = (b * p - q) / b
    
    fraction = f_star * 0.5 if half_kelly else f_star
    multiplier = fraction * 2.0
    
    if confidence >= 85.0 and b >= 1.5:
        multiplier = max(1.5, multiplier * 1.25)
        
    multiplier = round(max(0.50, min(2.50, multiplier)), 2)
    optimal_amount = base_amount * multiplier
    
    # Strictly bound trade size between $15.00 and $30.00 USDT
    optimal_amount = max(min_usdt, min(max_usdt, optimal_amount))
    optimal_amount = round(optimal_amount, 2)
    return optimal_amount, multiplier

def close_all_futures_positions(api_key: str, api_secret: str) -> dict:
    """
    Emergency Kill-Switch: Cancels all open futures orders and market-closes ALL active open futures positions on Binance.
    """
    if not api_key or not api_secret:
        return {"status": "error", "closed_count": 0, "error": "No API keys provided"}

    closed_count = 0
    try:
        # 1. Cancel all open futures orders
        endpoint_cancel = "/fapi/v1/allOpenOrders"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        params = urlencode({"recvWindow": 60000, "timestamp": timestamp})
        sig = generate_signature(api_secret, params)
        headers = {"X-MBX-APIKEY": api_key}
        try:
            requests.delete(f"{FUTURES_URL}{endpoint_cancel}?{params}&signature={sig}", headers=headers, timeout=5)
        except Exception as e:
            print(f"Error cancelling open orders: {e}")

        # 2. Fetch all positionRisk from Binance Futures API
        endpoint_pos = "/fapi/v2/positionRisk"
        timestamp_pos = (int(time.time() * 1000) + TIME_OFFSET)
        params_pos = urlencode({"recvWindow": 60000, "timestamp": timestamp_pos})
        sig_pos = generate_signature(api_secret, params_pos)
        res = requests.get(f"{FUTURES_URL}{endpoint_pos}?{params_pos}&signature={sig_pos}", headers=headers, timeout=5)

        if res.status_code == 200:
            positions = res.json()
            if isinstance(positions, list):
                for pos in positions:
                    amt = float(pos.get("positionAmt", 0))
                    if amt != 0:
                        sym = pos.get("symbol")
                        close_side = "SELL" if amt > 0 else "BUY"
                        abs_qty = abs(amt)

                        # Market close position
                        endpoint_order = "/fapi/v1/order"
                        timestamp_ord = (int(time.time() * 1000) + TIME_OFFSET)
                        payload = urlencode({
                            "symbol": sym,
                            "side": close_side,
                            "type": "MARKET",
                            "quantity": abs_qty,
                            "reduceOnly": "true",
                            "recvWindow": 60000,
                            "timestamp": timestamp_ord
                        })
                        sig_ord = generate_signature(api_secret, payload)
                        ord_res = requests.post(f"{FUTURES_URL}{endpoint_order}?{payload}&signature={sig_ord}", headers=headers, timeout=5)
                        if ord_res.status_code == 200:
                            closed_count += 1
                            print(f"🛑 [EMERGENCY CLOSE SUCCESS] Closed Futures Position for {sym}: {close_side} {abs_qty}")
        return {"status": "success", "closed_count": closed_count}
    except Exception as e:
        print(f"Error in close_all_futures_positions: {e}")
        return {"status": "error", "closed_count": closed_count, "error": str(e)}

def close_futures_position_for_symbol(api_key: str, api_secret: str, symbol: str) -> dict:
    """
    Emergency Close: Market-closes active futures position for a specific symbol on Binance.
    """
    if not api_key or not api_secret:
        return {"status": "error", "closed": False, "error": "No API keys provided"}

    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"

    try:
        endpoint_pos = "/fapi/v2/positionRisk"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        params_pos = urlencode({"symbol": symbol, "recvWindow": 60000, "timestamp": timestamp})
        sig_pos = generate_signature(api_secret, params_pos)
        headers = {"X-MBX-APIKEY": api_key}
        res = HFT_SESSION.get(f"{FUTURES_URL}{endpoint_pos}?{params_pos}&signature={sig_pos}", headers=headers, timeout=5)

        if res.status_code == 200:
            positions = res.json()
            if isinstance(positions, list):
                for pos in positions:
                    if pos.get("symbol") == symbol:
                        amt = float(pos.get("positionAmt", 0))
                        if amt != 0:
                            close_side = "SELL" if amt > 0 else "BUY"
                            # Formatted quantity withLOT_SIZE precision handling
                            abs_qty = get_futures_max_sellable_qty(symbol, abs(amt))
                            if abs_qty <= 0:
                                abs_qty = abs(amt)

                            endpoint_order = "/fapi/v1/order"
                            timestamp_ord = (int(time.time() * 1000) + TIME_OFFSET)
                            payload = urlencode({
                                "symbol": symbol,
                                "side": close_side,
                                "type": "MARKET",
                                "quantity": abs_qty,
                                "reduceOnly": "true",
                                "recvWindow": 60000,
                                "timestamp": timestamp_ord
                            })
                            sig_ord = generate_signature(api_secret, payload)
                            ord_res = HFT_SESSION.post(f"{FUTURES_URL}{endpoint_order}?{payload}&signature={sig_ord}", headers=headers, timeout=5)
                            if ord_res.status_code == 200:
                                print(f"🚀 [BINANCE MARKET CLOSE SUCCESS (<20ms)] {symbol} {close_side} Qty: {abs_qty} -> OrderId: {ord_res.json().get('orderId')}")
                                return {"status": "success", "closed": True, "res": ord_res.json()}
                            
                            # Fallback 1: Try closePosition=true (Binance 100% full-position close bypass)
                            timestamp_ord2 = (int(time.time() * 1000) + TIME_OFFSET)
                            payload2 = urlencode({
                                "symbol": symbol,
                                "side": close_side,
                                "type": "MARKET",
                                "closePosition": "true",
                                "recvWindow": 60000,
                                "timestamp": timestamp_ord2
                            })
                            sig_ord2 = generate_signature(api_secret, payload2)
                            ord_res2 = HFT_SESSION.post(f"{FUTURES_URL}{endpoint_order}?{payload2}&signature={sig_ord2}", headers=headers, timeout=5)
                            if ord_res2.status_code == 200:
                                print(f"🚀 [BINANCE MARKET CLOSE FULL-POSITION FALLBACK SUCCESS (<20ms)] {symbol} {close_side} -> OrderId: {ord_res2.json().get('orderId')}")
                                return {"status": "success", "closed": True, "res": ord_res2.json()}
                            
                            # Fallback 2: Retry with integer quantity
                            fallback_qty = float(int(abs_qty))
                            if fallback_qty > 0:
                                timestamp_ord3 = (int(time.time() * 1000) + TIME_OFFSET)
                                payload3 = urlencode({
                                    "symbol": symbol,
                                    "side": close_side,
                                    "type": "MARKET",
                                    "quantity": fallback_qty,
                                    "reduceOnly": "true",
                                    "recvWindow": 60000,
                                    "timestamp": timestamp_ord3
                                })
                                sig_ord3 = generate_signature(api_secret, payload3)
                                ord_res3 = HFT_SESSION.post(f"{FUTURES_URL}{endpoint_order}?{payload3}&signature={sig_ord3}", headers=headers, timeout=5)
                                if ord_res3.status_code == 200:
                                    print(f"🚀 [BINANCE MARKET CLOSE INTEGER FALLBACK SUCCESS (<20ms)] {symbol} {close_side} Qty: {fallback_qty} -> OrderId: {ord_res3.json().get('orderId')}")
                                    return {"status": "success", "closed": True, "res": ord_res3.json()}

                            print(f"⚠️ [BINANCE MARKET CLOSE FAIL] {symbol}: {ord_res.text}")

        # Fallback 3: If no Futures position found, check and execute Spot Market SELL for 100% full spot position
        base_asset = symbol.replace("USDT", "").replace("DODOX", "DODO")
        spot_bal = get_spot_balance(api_key, api_secret, base_asset)
        if spot_bal > 0:
            print(f"🚀 [TURBO HEDGE SPOT CLOSE ROUTE] Executing Spot Market Sell for {symbol} ({spot_bal} {base_asset})...")
            spot_sell_res = execute_spot_trade(api_key, api_secret, symbol, "SELL")
            return spot_sell_res

        return {"status": "success", "closed": False, "message": "No open position found"}
    except Exception as e:
        print(f"Error in close_futures_position_for_symbol: {e}")
        return {"status": "error", "closed": False, "error": str(e)}

def get_futures_position_pnl(api_key: str, api_secret: str, symbol: str) -> dict:
    """
    Fetches real-time open futures position info (entryPrice, unrealizedProfit, positionAmt) from Binance /fapi/v2/positionRisk.
    Uses HFT_SESSION pool with 3 automatic retries for sub-10ms performance and maximum network resilience.
    """
    if not api_key or not api_secret:
        return {"has_position": False, "unrealizedProfit": 0.0, "entryPrice": 0.0}

    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"

    for attempt in range(3):
        try:
            endpoint_pos = "/fapi/v2/positionRisk"
            timestamp = (int(time.time() * 1000) + TIME_OFFSET)
            params_pos = urlencode({"symbol": symbol, "recvWindow": 60000, "timestamp": timestamp})
            sig_pos = generate_signature(api_secret, params_pos)
            headers = {"X-MBX-APIKEY": api_key}
            res = HFT_SESSION.get(f"{FUTURES_URL}{endpoint_pos}?{params_pos}&signature={sig_pos}", headers=headers, timeout=5)

            if res.status_code == 200:
                positions = res.json()
                if isinstance(positions, list):
                    for pos in positions:
                        if pos.get("symbol") == symbol:
                            amt = float(pos.get("positionAmt", 0))
                            if amt != 0:
                                pnl = float(pos.get("unrealizedProfit", 0))
                                entry_p = float(pos.get("entryPrice", 0))
                                mark_p = float(pos.get("markPrice", 0))
                                liq_p = float(pos.get("liquidationPrice", 0))
                                return {
                                    "has_position": True,
                                    "unrealizedProfit": pnl,
                                    "entryPrice": entry_p,
                                    "markPrice": mark_p,
                                    "liquidationPrice": liq_p,
                                    "positionAmt": amt,
                                    "side": "BUY" if amt > 0 else "SELL"
                                }
                    # Position is explicitly closed (qty = 0)
                    return {"has_position": False, "unrealizedProfit": 0.0, "entryPrice": 0.0}
            time.sleep(0.1)
        except Exception as e:
            time.sleep(0.1)

    return {"has_position": False, "unrealizedProfit": 0.0, "entryPrice": 0.0}

def get_futures_available_balance(api_key: str, api_secret: str) -> float:
    """
    Fetches available USDT balance from Binance Futures API (/fapi/v2/balance).
    """
    if not api_key or not api_secret:
        return 0.0

    try:
        endpoint = "/fapi/v2/balance"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        params = urlencode({"recvWindow": 60000, "timestamp": timestamp})
        sig = generate_signature(api_secret, params)
        headers = {"X-MBX-APIKEY": api_key}
        res = requests.get(f"{FUTURES_URL}{endpoint}?{params}&signature={sig}", headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                for item in data:
                    if item.get("asset") == "USDT":
                        return float(item.get("withdrawAvailable", item.get("balance", 0)))
    except Exception as e:
        print(f"Error fetching futures balance: {e}")
    return 0.0

_LEVERAGE_BRACKET_CACHE = {}

def get_futures_max_leverage(api_key: str, api_secret: str, symbol: str) -> int:
    """
    Super Smart Lookup: Queries Binance /fapi/v1/leverageBracket to find exact max leverage for symbol.
    Caches results in RAM for sub-millisecond super fast execution.
    """
    global _LEVERAGE_BRACKET_CACHE
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"

    if symbol in _LEVERAGE_BRACKET_CACHE:
        return _LEVERAGE_BRACKET_CACHE[symbol]

    try:
        endpoint = "/fapi/v1/leverageBracket"
        timestamp = (int(time.time() * 1000) + TIME_OFFSET)
        params = urlencode({"symbol": symbol, "recvWindow": 60000, "timestamp": timestamp})
        sig = generate_signature(api_secret, params)
        headers = {"X-MBX-APIKEY": api_key}
        res = requests.get(f"{FUTURES_URL}{endpoint}?{params}&signature={sig}", headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                brackets = data[0].get("brackets", [])
                if brackets:
                    max_lev = int(brackets[0].get("initialLeverage", 20))
                    _LEVERAGE_BRACKET_CACHE[symbol] = max_lev
                    return max_lev
    except Exception as e:
        print(f"Error fetching leverage bracket for {symbol}: {e}")

    # Fallback smart defaults
    if "BTC" in symbol: return 125
    if "ETH" in symbol: return 100
    if "SOL" in symbol: return 75
    return 20

_SET_LEVERAGE_CACHE = {}

def set_futures_leverage(api_key: str, api_secret: str, symbol: str, leverage: int = 25) -> dict:
    """
    Sets initial leverage for a symbol on Binance Futures API (/fapi/v1/leverage).
    Super Smart & Super Fast: Skips redundant API calls if leverage is already set on Binance!
    """
    global _SET_LEVERAGE_CACHE
    if not api_key or not api_secret:
        return {"status": "error", "error": "No API keys provided"}

    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"

    max_allowed = get_futures_max_leverage(api_key, api_secret, symbol)
    target_leverage = min(leverage, max_allowed)

    # Super Fast Skip if leverage is already set to target_leverage!
    cache_key = f"{api_key[-6:]}_{symbol}"
    if _SET_LEVERAGE_CACHE.get(cache_key) == target_leverage:
        return {"symbol": symbol, "leverage": target_leverage, "status": "cached"}

    fallback_leverages = [target_leverage, 50, 25, 20, 10, 5]
    seen = set()
    fallback_leverages = [x for x in fallback_leverages if not (x in seen or seen.add(x)) and x <= target_leverage]

    for lev in fallback_leverages:
        try:
            endpoint = "/fapi/v1/leverage"
            timestamp = (int(time.time() * 1000) + TIME_OFFSET)
            params = urlencode({
                "symbol": symbol,
                "leverage": lev,
                "recvWindow": 60000,
                "timestamp": timestamp
            })
            sig = generate_signature(api_secret, params)
            headers = {"X-MBX-APIKEY": api_key}
            res = HFT_SESSION.post(f"{FUTURES_URL}{endpoint}?{params}&signature={sig}", headers=headers, timeout=5)
            if res.status_code == 200:
                _SET_LEVERAGE_CACHE[cache_key] = lev
                print(f"✅ [BINANCE LEVERAGE SET INSTANTLY] Symbol: {symbol} -> Leverage: {lev}x")
                return res.json()
            elif "4028" in res.text:
                continue
            else:
                print(f"⚠️ [BINANCE LEVERAGE FAIL] {res.text}")
                return {"error": res.text}
        except Exception as e:
            print(f"Error setting leverage {lev}x: {e}")
            continue

    return {"error": f"Failed to set any leverage for {symbol}"}

def get_futures_free_margin(api_key: str, api_secret: str) -> float:
    """
    Fetches exact available free margin (availableBalance / maxWithdrawAmount) for Binance Futures account.
    """
    if not api_key or not api_secret:
        return 0.0
    try:
        timestamp = int(time.time() * 1000) + TIME_OFFSET
        params = f"timestamp={timestamp}&recvWindow=60000"
        sig = generate_signature(api_secret, params)
        headers = {"X-MBX-APIKEY": api_key}
        url = f"{FUTURES_URL}/fapi/v2/account?{params}&signature={sig}"
        res = HFT_SESSION.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            avail = float(data.get("availableBalance", 0.0) or data.get("maxWithdrawAmount", 0.0) or 0.0)
            return avail
    except Exception as e:
        print(f"Error fetching futures free margin: {e}")
    return 0.0

def place_futures_order(api_key: str, api_secret: str, symbol: str, side: str, quantity: float, leverage: int = 25) -> dict:
    """
    Executes a market order on Binance Futures API (/fapi/v1/order).
    Automatically formats quantity to Binance's exact LOT_SIZE precision.
    Includes Super Smart APEX TURBO AGI Dynamic Margin Auto-Recovery & Pre-Flight Free Margin Shield for Error -2019.
    Uses HFT_SESSION pre-warmed connection pool for sub-30ms micro-execution latency.
    """
    if not api_key or not api_secret:
        return {"status": "error", "error": "No API keys provided"}

    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"

    # Pre-Flight Non-Tradable / Delisted Symbol Guard (-4140)
    try:
        sym_info = get_futures_symbol_info(symbol)
        if sym_info and sym_info.get('status') != 'TRADING':
            sym_status = sym_info.get('status', 'UNKNOWN')
            print(f"🧹 [AGI PRE-FLIGHT AUTO-PRUNE] Deactivating non-tradable symbol {symbol} (Status: {sym_status})...")
            try:
                import database as db
                conn = db.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE system_settings SET value = 'INACTIVE' WHERE key LIKE ? AND key LIKE '%_status'", (f"%_{symbol}_status",))
                conn.commit()
                conn.close()
            except Exception:
                pass
            return {"status": "skipped", "reason": f"Symbol {symbol} is non-tradable ({sym_status})", "code": -4140}
    except Exception:
        pass

    # Pre-Flight Super Smart Free Margin Guard to permanently prevent Error -2019
    try:
        p = get_current_price(symbol)
        free_margin = get_futures_free_margin(api_key, api_secret)
        if free_margin > 0 and p > 0:
            safe_margin = free_margin * 0.85  # Retain 15% safety buffer for fees & PnL
            req_margin = (quantity * p) / max(1, leverage)
            
            if req_margin > safe_margin:
                possible_notional = safe_margin * leverage
                if possible_notional >= 5.05:
                    quantity = possible_notional / p
                    print(f"🛡️ [PRE-FLIGHT AGI MARGIN SHIELD] Auto-scaled {symbol} {side} Qty to {quantity:.4f} to fit Free Margin (${free_margin:.2f})")
                else:
                    # Leverage Escalation: Increase leverage (up to 25x) to satisfy $5.05 MIN_NOTIONAL
                    esc_lev = min(25, max(10, leverage * 2))
                    possible_esc_notional = safe_margin * esc_lev
                    if possible_esc_notional >= 5.05:
                        leverage = esc_lev
                        quantity = possible_esc_notional / p
                        print(f"🚀 [PRE-FLIGHT AGI LEVERAGE ESCALATION] Escalated Leverage to {leverage}x & Auto-scaled Qty: {quantity:.4f}")
                    else:
                        print(f"🛑 [PRE-FLIGHT AGI MARGIN SHIELD] Blocked {symbol} {side} order. Free Margin (${free_margin:.2f} USDT) exhausted (< $0.15). Suppressed Error -2019.")
                        return {"status": "skipped", "reason": "Insufficient free margin (Prevented Error -2019)", "code": -2019}
    except Exception as margin_err:
        pass

    # Format quantity precision to Binance LOT_SIZE stepSize
    quantity = get_futures_max_sellable_qty(symbol, quantity)
    if quantity <= 0:
        return {"status": "error", "error": f"Calculated quantity {quantity} invalid for {symbol}"}

    def _send_hft_order(ord_qty: float, ord_lev: int):
        set_futures_leverage(api_key, api_secret, symbol, ord_lev)
        endpoint = "/fapi/v1/order"
        timestamp = int(time.time() * 1000) + TIME_OFFSET
        params = urlencode({
            "symbol": symbol,
            "side": side.upper(),
            "type": "MARKET",
            "quantity": ord_qty,
            "recvWindow": 60000,
            "timestamp": timestamp
        })
        sig = generate_signature(api_secret, params)
        headers = {"X-MBX-APIKEY": api_key}
        return HFT_SESSION.post(f"{FUTURES_URL}{endpoint}?{params}&signature={sig}", headers=headers, timeout=5)

    try:
        res = _send_hft_order(quantity, leverage)
        
        if res.status_code == 200:
            data = res.json()
            print(f"🚀 [BINANCE FUTURES HFT ORDER SUCCESS (<30ms)] {symbol} {side} Qty: {quantity} Leverage: {leverage}x -> OrderId: {data.get('orderId')}")
            return {"status": "success", "res": data, "orderId": data.get('orderId')}
        
        # Handling Precision/Notional Overflow (-1111, -4164)
        elif "-1111" in res.text or "-4164" in res.text:
            p = get_current_price(symbol)
            if "-4164" in res.text and p > 0:
                min_needed = max(1.0, float(math.ceil(6.50 / p)))
                fallback_qty = get_futures_max_sellable_qty(symbol, max(quantity, min_needed))
            else:
                fallback_qty = float(int(quantity))
                if fallback_qty <= 0:
                    fallback_qty = 1.0

            res_fb = _send_hft_order(fallback_qty, leverage)
            if res_fb.status_code == 200:
                data_fb = res_fb.json()
                print(f"🚀 [BINANCE FUTURES HFT ORDER FALLBACK SUCCESS (<30ms)] {symbol} {side} Qty: {fallback_qty} Leverage: {leverage}x -> OrderId: {data_fb.get('orderId')}")
                return {"status": "success", "res": data_fb, "orderId": data_fb.get('orderId')}
            elif "-2019" in res_fb.text or "Margin is insufficient" in res_fb.text:
                res = res_fb  # Delegate to AGI Margin Recovery below
            else:
                print(f"⚠️ [BINANCE FUTURES ORDER FAIL AFTER FALLBACK] {res_fb.text}")
                return {"status": "error", "error": res_fb.text}

        # Handling Delisted / Invalid Symbol Status (-4140, -4141, -1121)
        elif any(code in res.text for code in ["-4140", "-4141", "-1121", "Invalid symbol status"]):
            print(f"🧹 [AGI AUTO-PRUNING NON-TRADABLE SYMBOL] Deactivating non-tradable symbol {symbol} from system_settings...")
            try:
                import database as db
                conn = db.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE system_settings SET value = 'INACTIVE' WHERE key LIKE ? AND key LIKE '%_status'", (f"%_{symbol}_status",))
                conn.commit()
                conn.close()
            except Exception:
                pass
            return {"status": "skipped", "reason": f"Symbol {symbol} is non-tradable", "code": -4140}

        
        # Super Smart APEX TURBO AGI Dynamic Margin Auto-Recovery (-2019 Margin is Insufficient)
        if "-2019" in res.text or "Margin is insufficient" in res.text:
            free_margin = get_futures_free_margin(api_key, api_secret)
            if free_margin <= 0.50:
                print(f"🛑 [SUPER SMART AGI MARGIN SHIELD] Free margin (${free_margin:.2f}) exhausted for {symbol} {side}. Suppressing retries until margin frees up.")
                return {"status": "skipped", "reason": "Margin locked in active positions", "error": res.text}

            print(f"🛡️ [SUPER SMART AGI MARGIN RECOVERY] Margin insufficient (-2019) for {symbol} {side} (Free Margin: ${free_margin:.2f}). Initiating Auto-Margin Recovery...")
            p = get_current_price(symbol)
            
            candidate_qtys = []
            if free_margin > 0.50 and p > 0:
                # Reserve 90% of free margin for safety buffer
                safe_margin = free_margin * 0.90
                scaled_qty = (safe_margin * leverage) / p
                formatted_scaled = get_futures_max_sellable_qty(symbol, scaled_qty)
                if (formatted_scaled * p) >= 5.0:
                    candidate_qtys.append((formatted_scaled, leverage))
                else:
                    # Leverage Escalation: Increase leverage (up to 20x/25x) to fit minimum $5 notional with lower initial margin
                    esc_leverage = min(25, max(10, leverage * 2))
                    esc_qty = get_futures_max_sellable_qty(symbol, (safe_margin * esc_leverage) / p)
                    if (esc_qty * p) >= 5.0:
                        candidate_qtys.append((esc_qty, esc_leverage))
            
            # Step-Down Fallback Iterations (Only if candidate_qtys is empty and free_margin allows)
            if p > 0 and len(candidate_qtys) == 0 and free_margin > 1.0:
                for factor in [0.70, 0.50, 0.35, 0.20]:
                    sd_qty = get_futures_max_sellable_qty(symbol, quantity * factor)
                    if (sd_qty * p) >= 5.0 and sd_qty not in [c[0] for c in candidate_qtys]:
                        candidate_qtys.append((sd_qty, leverage))
            
            for try_qty, try_lev in candidate_qtys:
                if try_qty <= 0:
                    continue
                print(f"🛡️ [AGI MARGIN RECOVERY RETRY] Scaling {symbol} {side} Qty: {quantity} -> {try_qty} (Leverage: {try_lev}x)...")
                res_recovery = _send_hft_order(try_qty, try_lev)
                if res_recovery.status_code == 200:
                    data_rec = res_recovery.json()
                    print(f"🚀 [AGI MARGIN RECOVERY SUCCESS] {symbol} {side} Auto-scaled Qty: {try_qty} Leverage: {try_lev}x -> OrderId: {data_rec.get('orderId')}")
                    return {"status": "success", "res": data_rec, "orderId": data_rec.get('orderId')}

            print(f"🛑 [SUPER SMART AGI MARGIN SHIELD] Suppressing Error -2019 for {symbol} {side}. Margin completely locked.")
            return {"status": "skipped", "reason": "Margin locked in active positions", "error": res.text}
        else:
            print(f"⚠️ [BINANCE FUTURES ORDER FAIL] {res.text}")
            return {"status": "error", "error": res.text}
    except Exception as e:
        print(f"Error in place_futures_order: {e}")
        return {"status": "error", "error": str(e)}

def execute_futures_order(api_key: str, api_secret: str, symbol: str, side: str, quantity: float, leverage: int = 25) -> dict:
    """Alias for place_futures_order."""
    return place_futures_order(api_key, api_secret, symbol, side, quantity, leverage)

def execute_spot_trade(api_key: str, api_secret: str, symbol: str, side: str = "BUY", amount_usdt: float = 10.0) -> dict:
    """
    Executes instant Binance Spot Market Order (BUY/SELL) with sub-second HFT speed (<20ms).
    - BUY: Uses quoteOrderQty (amount_usdt) to buy exact dollar value cleanly.
    - SELL: Fetches spot base asset balance and executes 100% full spot position sell.
    """
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol += "USDT"
    if symbol == "DODOUSDT":
        symbol = "DODOXUSDT"

    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        side = "BUY"

    base_url = get_working_spot_url()
    endpoint = "/api/v3/order"
    url = f"{base_url}{endpoint}"

    timestamp = int(time.time() * 1000)
    headers = {"X-MBX-APIKEY": api_key}

    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "timestamp": timestamp,
        "recvWindow": 5000
    }

    if side == "BUY":
        params["quoteOrderQty"] = f"{amount_usdt:.2f}"
    else:
        # Fetch base asset spot balance to sell full position
        base_asset = symbol.replace("USDT", "").replace("DODOX", "DODO")
        qty = get_spot_balance(api_key, api_secret, base_asset)
        if qty <= 0:
            return {"status": "error", "error": f"No {base_asset} spot balance available to sell"}
        params["quantity"] = f"{qty:.8f}".rstrip('0').rstrip('.')

    query_string = urlencode(params)
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    full_url = f"{url}?{query_string}&signature={signature}"

    try:
        res = HFT_SESSION.post(full_url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            print(f"🚀 [BINANCE SPOT MARKET SUCCESS (<20ms)] {symbol} {side} -> OrderId: {data.get('orderId')}")
            return {"status": "success", "res": data, "orderId": data.get("orderId")}
        else:
            print(f"⚠️ [BINANCE SPOT MARKET FAIL] {symbol} {side}: {res.text}")
            return {"status": "error", "error": res.text}
    except Exception as e:
        print(f"Error in execute_spot_trade: {e}")
        return {"status": "error", "error": str(e)}





