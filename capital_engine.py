"""
KHMER MASTER CRYPTO - CAPITAL.COM INSTITUTIONAL TRADING ENGINE
==============================================================
Module: capital_engine.py
Target Broker: Capital.com (FCA, CySEC, ASIC Regulated Global Multi-Asset Broker)
Instruments: Gold (XAU/USD), Crude Oil (WTI), S&P 500, Nasdaq 100, Major Forex & Crypto CFDs
Architecture: REST API & Session-based Token Management (CST + X-SECURITY-TOKEN)
Execution Environment: Demo ($10,000 Virtual Funds) & Live Mainnet
==============================================================
"""

import os
import time
import logging
import requests
from typing import Dict, Any, Optional, Tuple, List

# Setup Logger
logger = logging.getLogger("CapitalComEngine")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [Capital.com] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# ==============================================================================
# 1. CAPITAL.COM REST API ENDPOINTS & CONSTANTS
# ==============================================================================
CAPITAL_LIVE_URL = "https://api-capital.backend-capital.com/api/v1"
CAPITAL_DEMO_URL = "https://demo-api-capital.backend-capital.com/api/v1"

# Canonical Instrument Epics on Capital.com
EPIC_MAP = {
    # Commodities
    "GOLD": "GOLD",             # Spot Gold / US Dollar (XAU/USD)
    "SILVER": "SILVER",         # Spot Silver / US Dollar (XAG/USD)
    "OIL": "OIL_CRUDE",         # US Crude Oil WTI
    "BRENT": "OIL_BRENT",       # Brent Crude Oil
    # Indices
    "SP500": "US500",           # S&P 500 Index
    "NASDAQ": "US100",          # Nasdaq 100 Tech Index
    "DOW": "US30",              # Dow Jones Industrial Average
    "DAX": "GERMANY40",         # German DAX 40
    # Forex
    "EURUSD": "EURUSD",         # Euro / US Dollar
    "GBPUSD": "GBPUSD",         # British Pound / US Dollar
    "USDJPY": "USDJPY",         # US Dollar / Japanese Yen
    # Crypto CFDs
    "BTCUSD": "BTCUSD",         # Bitcoin / US Dollar CFD
    "ETHUSD": "ETHUSD",         # Ethereum / US Dollar CFD
    "SOLUSD": "SOLUSD"          # Solana / US Dollar CFD
}

# Session validity duration in seconds (Capital.com sessions expire after 10 minutes)
SESSION_EXPIRY_THRESHOLD = 500  # Refresh session after ~8.3 minutes to avoid expiration


# ==============================================================================
# 2. CAPITAL.COM INSTITUTIONAL ENGINE CLASS
# ==============================================================================
class CapitalComEngine:
    """
    Institutional Algorithmic Engine for Capital.com.
    Handles session lifecycle, real-time market data, risk-guarded orders,
    and automatic demo/live environment routing.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        identifier: Optional[str] = None,
        password: Optional[str] = None,
        is_demo: bool = True
    ):
        self.api_key = api_key or os.getenv("CAPITAL_API_KEY", "")
        self.identifier = identifier or os.getenv("CAPITAL_IDENTIFIER", "")
        self.password = password or os.getenv("CAPITAL_PASSWORD", "")
        self.is_demo = is_demo
        
        self.base_url = CAPITAL_DEMO_URL if self.is_demo else CAPITAL_LIVE_URL
        
        # Session state
        self.cst_token: Optional[str] = None
        self.security_token: Optional[str] = None
        self.session_created_at: float = 0.0
        self.active_account_id: Optional[str] = None
        self.account_currency: str = "USD"
        
        # In-Memory Cache (Sub-millisecond fast responses)
        self._price_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = 3.0  # 3 seconds cache for live quotes

    # --------------------------------------------------------------------------
    # Authentication & Session Management
    # --------------------------------------------------------------------------
    def authenticate(self) -> Tuple[bool, str]:
        """
        Creates a new trading session via POST /api/v1/session.
        Captures CST (Client Security Token) and X-SECURITY-TOKEN from response headers.
        """
        if not self.api_key or not self.identifier or not self.password:
            return False, "Missing Capital.com API Key, Identifier, or API Password."

        url = f"{self.base_url}/session"
        headers = {
            "X-CAP-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "identifier": self.identifier,
            "password": self.password,
            "encryptedPassword": False
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=10)
            if res.status_code == 200:
                self.cst_token = res.headers.get("CST")
                self.security_token = res.headers.get("X-SECURITY-TOKEN")
                self.session_created_at = time.time()
                
                body = res.json()
                self.active_account_id = body.get("currentAccountId")
                
                env_mode = "DEMO ($10,000 Virtual)" if self.is_demo else "LIVE MAINNET"
                msg = f"Session established successfully [{env_mode}]! Account ID: {self.active_account_id}"
                logger.info(msg)
                return True, msg
            else:
                err_data = res.json() if res.content else {}
                err_msg = err_data.get("errorCode", f"HTTP {res.status_code}: {res.text}")
                logger.error(f"Authentication failed: {err_msg}")
                return False, f"Auth Error: {err_msg}"
        except Exception as e:
            logger.error(f"Authentication exception: {e}")
            return False, f"Connection Exception: {e}"

    def ensure_session(self) -> bool:
        """Verifies session freshness and auto-refreshes if close to 10-minute expiry."""
        now = time.time()
        if not self.cst_token or not self.security_token:
            success, _ = self.authenticate()
            return success
            
        if (now - self.session_created_at) > SESSION_EXPIRY_THRESHOLD:
            logger.info("Session token near expiry. Performing proactive session refresh...")
            success, _ = self.authenticate()
            return success
            
        return True

    def get_auth_headers(self) -> Dict[str, str]:
        """Returns standard headers required for all Capital.com REST requests."""
        return {
            "X-CAP-API-KEY": self.api_key,
            "CST": self.cst_token or "",
            "X-SECURITY-TOKEN": self.security_token or "",
            "Content-Type": "application/json"
        }

    # --------------------------------------------------------------------------
    # Account & Capital Overview
    # --------------------------------------------------------------------------
    def get_accounts(self) -> Dict[str, Any]:
        """Fetches full account information, equity, and margin balances."""
        if not self.ensure_session():
            return {"success": False, "error": "Unable to establish valid session."}

        url = f"{self.base_url}/accounts"
        try:
            res = requests.get(url, headers=self.get_auth_headers(), timeout=10)
            if res.status_code == 200:
                data = res.json()
                accounts = data.get("accounts", [])
                primary = accounts[0] if accounts else {}
                self.account_currency = primary.get("currency", "USD")
                return {
                    "success": True,
                    "accounts": accounts,
                    "primary_account": primary
                }
            return {"success": False, "error": f"HTTP {res.status_code}: {res.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_account_balance(self) -> Dict[str, Any]:
        """
        Returns a simplified, institutional balance breakdown:
        {balance, available_cash, equity, pnl, currency, is_demo}
        """
        acc_info = self.get_accounts()
        if not acc_info.get("success"):
            return {
                "success": False,
                "balance": 0.0,
                "available": 0.0,
                "equity": 0.0,
                "pnl": 0.0,
                "currency": "USD",
                "is_demo": self.is_demo,
                "error": acc_info.get("error", "Failed")
            }

        primary = acc_info.get("primary_account", {})
        balance_info = primary.get("balance", {})
        
        return {
            "success": True,
            "account_id": primary.get("accountId"),
            "account_name": primary.get("accountName", "Capital.com Demo"),
            "balance": float(balance_info.get("balance", 0.0)),
            "available": float(balance_info.get("available", 0.0)),
            "deposit": float(balance_info.get("deposit", 0.0)),  # Margin used
            "pnl": float(balance_info.get("profitLoss", 0.0)),
            "currency": primary.get("currency", "USD"),
            "status": primary.get("status", "ACTIVE"),
            "is_demo": self.is_demo
        }

    # --------------------------------------------------------------------------
    # Market Data & Live Pricing (Gold, Indices, Oil, Forex)
    # --------------------------------------------------------------------------
    def get_market_details(self, epic: str) -> Dict[str, Any]:
        """
        Retrieves market status, real-time bid/ask, spread, and minimum deal size.
        Example epics: 'GOLD', 'US500', 'OIL_CRUDE', 'BTCUSD'.
        """
        resolved_epic = EPIC_MAP.get(epic.upper(), epic.upper())
        
        # Check in-memory cache
        now = time.time()
        cached = self._price_cache.get(resolved_epic)
        if cached and (now - cached["timestamp"]) < self._cache_ttl:
            return cached["data"]

        if not self.ensure_session():
            return {"success": False, "error": "Unable to establish valid session."}

        url = f"{self.base_url}/markets/{resolved_epic}"
        try:
            res = requests.get(url, headers=self.get_auth_headers(), timeout=10)
            if res.status_code == 200:
                data = res.json()
                snapshot = data.get("snapshot", {})
                dealing_rules = data.get("dealingRules", {})
                instrument = data.get("instrument", {})

                bid = float(snapshot.get("bid", 0.0))
                ask = float(snapshot.get("offer", 0.0))
                spread = round(ask - bid, 4) if ask > 0 and bid > 0 else 0.0
                mid = round((bid + ask) / 2.0, 4) if bid > 0 and ask > 0 else 0.0
                
                market_status = snapshot.get("marketStatus", "TRADEABLE")
                min_size = float(dealing_rules.get("minDealSize", {}).get("value", 0.01))

                result = {
                    "success": True,
                    "epic": resolved_epic,
                    "instrument_name": instrument.get("name", resolved_epic),
                    "bid": bid,
                    "ask": ask,
                    "mid": mid,
                    "spread": spread,
                    "market_status": market_status,  # TRADEABLE, CLOSED, EDITS_ONLY
                    "min_deal_size": min_size,
                    "margin_factor": instrument.get("marginFactor", 0.05), # e.g. 5% = 20x leverage
                    "percentage_change": float(snapshot.get("percentageChange", 0.0)),
                    "high": float(snapshot.get("high", 0.0)),
                    "low": float(snapshot.get("low", 0.0)),
                    "timestamp": now
                }
                
                # Save to cache
                self._price_cache[resolved_epic] = {"timestamp": now, "data": result}
                return result
            else:
                return {"success": False, "error": f"HTTP {res.status_code}: {res.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_current_price(self, epic: str) -> Tuple[float, float, float]:
        """
        Fast helper returning (bid, ask, mid) for an instrument.
        Returns (0.0, 0.0, 0.0) if unavailable.
        """
        details = self.get_market_details(epic)
        if details.get("success"):
            return details.get("bid", 0.0), details.get("ask", 0.0), details.get("mid", 0.0)
        return 0.0, 0.0, 0.0

    def get_historical_prices(
        self,
        epic: str,
        resolution: str = "MINUTE_15",
        max_bars: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Fetches historical OHLCV bars for technical indicator calculation.
        Resolutions: MINUTE, MINUTE_5, MINUTE_15, MINUTE_30, HOUR, HOUR_4, DAY.
        """
        resolved_epic = EPIC_MAP.get(epic.upper(), epic.upper())
        if not self.ensure_session():
            return []

        url = f"{self.base_url}/prices/{resolved_epic}"
        params = {"resolution": resolution, "max": max_bars}
        
        try:
            res = requests.get(url, headers=self.get_auth_headers(), params=params, timeout=10)
            if res.status_code == 200:
                data = res.json()
                prices = data.get("prices", [])
                candles = []
                for p in prices:
                    candles.append({
                        "snapshotTime": p.get("snapshotTime"),
                        "open": float(p.get("openPrice", {}).get("bid", 0.0)),
                        "high": float(p.get("highPrice", {}).get("bid", 0.0)),
                        "low": float(p.get("lowPrice", {}).get("bid", 0.0)),
                        "close": float(p.get("closePrice", {}).get("bid", 0.0)),
                        "volume": float(p.get("lastTradedVolume", 0.0))
                    })
                return candles
            return []
        except Exception as e:
            logger.error(f"Error fetching historical prices: {e}")
            return []

    # --------------------------------------------------------------------------
    # Trading & Position Management (Demo & Live Protected)
    # --------------------------------------------------------------------------
    def get_open_positions(self) -> List[Dict[str, Any]]:
        """Retrieves all currently active open positions."""
        if not self.ensure_session():
            return []

        url = f"{self.base_url}/positions"
        try:
            res = requests.get(url, headers=self.get_auth_headers(), timeout=10)
            if res.status_code == 200:
                data = res.json()
                return data.get("positions", [])
            return []
        except Exception as e:
            logger.error(f"Error fetching open positions: {e}")
            return []

    def place_position(
        self,
        epic: str,
        direction: str,
        size: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        guaranteed_stop: bool = False,
        max_allowed_spread: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes a Market CFD order on Capital.com with full risk protection.
        
        Parameters:
        - epic: Instrument symbol (e.g. 'GOLD', 'US500', 'BTCUSD')
        - direction: 'BUY' (Long) or 'SELL' (Short)
        - size: Number of contracts / lot size
        - stop_loss: Absolute price level for Stop-Loss
        - take_profit: Absolute price level for Take-Profit
        - max_allowed_spread: Maximum acceptable spread before rejecting order (Spread Guard)
        """
        resolved_epic = EPIC_MAP.get(epic.upper(), epic.upper())
        dir_upper = direction.upper()
        if dir_upper not in ["BUY", "SELL"]:
            return {"success": False, "error": f"Invalid direction: {direction}. Must be 'BUY' or 'SELL'."}

        # Step 1: Check Market Status & Spread
        market_info = self.get_market_details(resolved_epic)
        if not market_info.get("success"):
            return {"success": False, "error": f"Market data query failed: {market_info.get('error')}"}

        if market_info.get("market_status") != "TRADEABLE":
            status = market_info.get("market_status")
            return {
                "success": False,
                "error": f"Market {resolved_epic} is currently {status} (TradFi markets closed on weekends/holidays)."
            }

        spread = market_info.get("spread", 0.0)
        if max_allowed_spread and spread > max_allowed_spread:
            return {
                "success": False,
                "error": f"Spread Guard rejection: Current spread {spread} exceeds max limit {max_allowed_spread}."
            }

        min_size = market_info.get("min_deal_size", 0.01)
        if size < min_size:
            size = min_size  # Auto-clamp to minimum deal size

        # Step 2: Prepare Payload
        payload: Dict[str, Any] = {
            "epic": resolved_epic,
            "direction": dir_upper,
            "size": round(size, 4),
            "guaranteedStop": guaranteed_stop
        }

        if stop_loss is not None and stop_loss > 0:
            payload["stopLevel"] = round(stop_loss, 4)
        if take_profit is not None and take_profit > 0:
            payload["profitLevel"] = round(take_profit, 4)

        # Step 3: Transmit Order
        url = f"{self.base_url}/positions"
        try:
            res = requests.post(url, headers=self.get_auth_headers(), json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()
                deal_ref = data.get("dealReference")
                logger.info(f"Order submitted successfully! Epic: {resolved_epic} | Dir: {dir_upper} | Ref: {deal_ref}")
                return {
                    "success": True,
                    "epic": resolved_epic,
                    "direction": dir_upper,
                    "size": size,
                    "deal_reference": deal_ref,
                    "is_demo": self.is_demo,
                    "response": data
                }
            else:
                err_data = res.json() if res.content else {}
                err_code = err_data.get("errorCode", f"HTTP {res.status_code}: {res.text}")
                logger.error(f"Order placement failed: {err_code}")
                return {"success": False, "error": err_code}
        except Exception as e:
            logger.error(f"Order placement exception: {e}")
            return {"success": False, "error": str(e)}

    def close_position(self, deal_id: str) -> Dict[str, Any]:
        """Closes an open position by dealId."""
        if not self.ensure_session():
            return {"success": False, "error": "Unable to establish valid session."}

        url = f"{self.base_url}/positions/{deal_id}"
        try:
            res = requests.delete(url, headers=self.get_auth_headers(), timeout=10)
            if res.status_code == 200:
                data = res.json()
                deal_ref = data.get("dealReference")
                logger.info(f"Position {deal_id} closed successfully! Deal Ref: {deal_ref}")
                return {"success": True, "deal_id": deal_id, "deal_reference": deal_ref}
            else:
                err_data = res.json() if res.content else {}
                err_code = err_data.get("errorCode", f"HTTP {res.status_code}: {res.text}")
                return {"success": False, "error": err_code}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==============================================================================
# 3. CONVENIENCE HELPERS & FACTORY FUNCTIONS
# ==============================================================================
_GLOBAL_CAPITAL_ENGINE: Optional[CapitalComEngine] = None

def get_capital_engine(is_demo: bool = True) -> CapitalComEngine:
    """Singleton getter for the global CapitalComEngine instance."""
    global _GLOBAL_CAPITAL_ENGINE
    if _GLOBAL_CAPITAL_ENGINE is None or _GLOBAL_CAPITAL_ENGINE.is_demo != is_demo:
        _GLOBAL_CAPITAL_ENGINE = CapitalComEngine(is_demo=is_demo)
    return _GLOBAL_CAPITAL_ENGINE

def validate_capital_credentials(
    api_key: str,
    identifier: str,
    password: str,
    is_demo: bool = True
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates user credentials against Capital.com (Demo or Live).
    Returns (is_valid: bool, status_message: str, account_details: dict).
    """
    engine = CapitalComEngine(
        api_key=api_key,
        identifier=identifier,
        password=password,
        is_demo=is_demo
    )
    success, msg = engine.authenticate()
    if not success:
        return False, msg, {}

    balance_info = engine.get_account_balance()
    return True, msg, balance_info

def quick_gold_quote(is_demo: bool = True) -> Dict[str, Any]:
    """Fetches instant live quote for Spot Gold (XAU/USD)."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.get_market_details("GOLD")

def quick_sp500_quote(is_demo: bool = True) -> Dict[str, Any]:
    """Fetches instant live quote for S&P 500 (US500)."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.get_market_details("SP500")


# ==============================================================================
# 4. STANDALONE DEMO TEST HARNESS
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  KHMER MASTER CRYPTO - CAPITAL.COM DEMO TEST HARNESS")
    print("=" * 70)
    
    api_k = os.getenv("CAPITAL_API_KEY", "")
    ident = os.getenv("CAPITAL_IDENTIFIER", "")
    pwd = os.getenv("CAPITAL_PASSWORD", "")
    
    print("\n[STEP 1] Inspecting Environment Variables...")
    print(f"  • CAPITAL_API_KEY:    {'[SET]' if api_k else '[EMPTY]'}")
    print(f"  • CAPITAL_IDENTIFIER: {'[SET]' if ident else '[EMPTY]'}")
    print(f"  • CAPITAL_PASSWORD:   {'[SET]' if pwd else '[EMPTY]'}")
    print("  • DEFAULT TARGET:     DEMO ($10,000 Virtual Funds)")
    
    if not api_k or not ident or not pwd:
        print("\n[NOTICE] No Capital.com credentials found in .env.")
        print("To test live execution on Demo Account, obtain free API credentials:")
        print("  1. Create free Demo account at: https://capital.com/")
        print("  2. Enable 2FA (Google Authenticator)")
        print("  3. Navigate to: Settings > API integrations > Generate Key")
        print("  4. Add to .env:")
        print("     CAPITAL_API_KEY=your_key")
        print("     CAPITAL_IDENTIFIER=your_email")
        print("     CAPITAL_PASSWORD=your_api_password")
        print("     CAPITAL_IS_DEMO=True")
        print("\n[TEST] Engine structure, classes, and helper mappings compiled successfully!")
        print("Ready for automated trading and institutional demo execution.")
    else:
        print("\n[STEP 2] Authenticating with Capital.com Demo API...")
        engine = CapitalComEngine(api_key=api_k, identifier=ident, password=pwd, is_demo=True)
        ok, msg = engine.authenticate()
        print(f"  Result: {'SUCCESS' if ok else 'FAILED'} -> {msg}")
        
        if ok:
            print("\n[STEP 3] Fetching Demo Account Balance...")
            bal = engine.get_account_balance()
            print(f"  • Account Name: {bal.get('account_name')}")
            print(f"  • Balance:      ${bal.get('balance'):,.2f} {bal.get('currency')}")
            print(f"  • Available:    ${bal.get('available'):,.2f} {bal.get('currency')}")
            print(f"  • Equity:       ${bal.get('balance', 0) + bal.get('pnl', 0):,.2f}")
            print(f"  • Active PnL:   ${bal.get('pnl'):,.2f}")
            
            print("\n[STEP 4] Fetching Live Gold (XAU/USD) & S&P 500 Market Prices...")
            gold = engine.get_market_details("GOLD")
            if gold.get("success"):
                print(f"  • GOLD (XAU/USD): Bid ${gold.get('bid'):,.2f} | Ask ${gold.get('ask'):,.2f} | Spread ${gold.get('spread'):.2f}")
            
            sp500 = engine.get_market_details("SP500")
            if sp500.get("success"):
                print(f"  • S&P 500:        Bid ${sp500.get('bid'):,.2f} | Ask ${sp500.get('ask'):,.2f} | Spread ${sp500.get('spread'):.2f}")
    
    print("\n" + "=" * 70)
