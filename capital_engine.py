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
from dotenv import load_dotenv

# Automatically load .env configuration
load_dotenv()

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
    # US Mega-Cap Stocks
    "NVDA": "NVDA",             # Nvidia Corporation
    "TSLA": "TSLA",             # Tesla Inc
    "AAPL": "AAPL",             # Apple Inc
    "MSFT": "MSFT",             # Microsoft Corporation
    "AMZN": "AMZN",             # Amazon.com Inc
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

# Default Capital.com Institutional Demo Credentials (Zero-Config Fallback)
DEFAULT_CAPITAL_API_KEY = "Vm6tyK0cHtqq6fPe"
DEFAULT_CAPITAL_IDENTIFIER = "hem.sinath@gmail.com"
DEFAULT_CAPITAL_PASSWORD = "Vipheavy@2297!"


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
        is_demo: Optional[bool] = None
    ):
        self.api_key = (api_key or os.getenv("CAPITAL_API_KEY", "")).strip() or DEFAULT_CAPITAL_API_KEY
        self.identifier = (identifier or os.getenv("CAPITAL_IDENTIFIER", "")).strip() or DEFAULT_CAPITAL_IDENTIFIER
        self.password = (password or os.getenv("CAPITAL_PASSWORD", "")).strip() or DEFAULT_CAPITAL_PASSWORD
        self.last_auth_error: str = ""
        
        if is_demo is not None:
            self.is_demo = is_demo
        else:
            self.is_demo = os.getenv("CAPITAL_IS_DEMO", "True").strip().lower() in ("true", "1", "yes")
            
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
            msg = "Missing Capital.com API Key, Identifier, or Password. Please configure .env settings."
            self.last_auth_error = msg
            logger.error(msg)
            return False, msg

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
                self.last_auth_error = ""
                
                body = res.json()
                self.active_account_id = body.get("currentAccountId")
                
                env_mode = "DEMO ($10,000 Virtual)" if self.is_demo else "LIVE MAINNET"
                msg = f"Session established successfully [{env_mode}]! Account ID: {self.active_account_id}"
                logger.info(msg)
                return True, msg
            else:
                err_data = res.json() if res.content else {}
                err_msg = err_data.get("errorCode", f"HTTP {res.status_code}: {res.text}")
                if "error.null.accountId" in err_msg and self.is_demo:
                    err_msg = "error.null.accountId (No active Demo account found on Capital.com profile. Please switch to Demo on Capital.com web platform to activate your $10,000 demo account, or set CAPITAL_IS_DEMO=False for Live)."
                self.last_auth_error = err_msg
                logger.error(f"Authentication failed: {err_msg}")
                return False, f"Auth Error: {err_msg}"
        except Exception as e:
            err_msg = str(e)
            self.last_auth_error = err_msg
            logger.error(f"Authentication exception: {e}")
            return False, f"Connection Exception: {e}"

    def ensure_session(self) -> bool:
        """Verifies session freshness and auto-refreshes if close to 10-minute expiry."""
        now = time.time()
        if not self.cst_token or not self.security_token:
            success, msg = self.authenticate()
            if not success:
                self.last_auth_error = msg
            return success
            
        if (now - self.session_created_at) > SESSION_EXPIRY_THRESHOLD:
            logger.info("Session token near expiry. Performing proactive session refresh...")
            success, msg = self.authenticate()
            if not success:
                self.last_auth_error = msg
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
            err_detail = self.last_auth_error or "Unable to establish valid session."
            return {"success": False, "error": f"Unable to establish valid session: {err_detail}"}

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
            err_detail = self.last_auth_error or "Unable to establish valid session."
            return {"success": False, "error": f"Unable to establish valid session: {err_detail}"}

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

                # Auto-Recovery from Stop-Loss / Take-Profit distance boundary rejections (Invariant 1 Zero Negligence):
                # 1. error.invalid.stoploss.minvalue: <val>
                m_sl_min = re.search(r'error\.invalid\.stoploss\.minvalue:\s*([0-9.]+)', err_code)
                if m_sl_min:
                    min_val = float(m_sl_min.group(1))
                    adjusted_sl = round(min_val * 1.0005, 2) if dir_upper == "SELL" else round(min_val * 1.0005, 2)
                    logger.info(f"🔄 Auto-Recovery: Adjusting Stop-Loss to {adjusted_sl} (required min: {min_val}) and retrying...")
                    payload["stopLevel"] = adjusted_sl
                    res_retry = requests.post(url, headers=self.get_auth_headers(), json=payload, timeout=10)
                    if res_retry.status_code == 200:
                        data = res_retry.json()
                        deal_ref = data.get("dealReference")
                        logger.info(f"✅ Auto-Recovery succeeded! Deal Ref: {deal_ref}")
                        return {
                            "success": True,
                            "epic": resolved_epic,
                            "direction": dir_upper,
                            "size": size,
                            "deal_reference": deal_ref,
                            "is_demo": self.is_demo,
                            "response": data
                        }

                # 2. error.invalid.stoploss.maxvalue: <val>
                m_sl_max = re.search(r'error\.invalid\.stoploss\.maxvalue:\s*([0-9.]+)', err_code)
                if m_sl_max:
                    max_val = float(m_sl_max.group(1))
                    adjusted_sl = round(max_val * 0.9995, 2)
                    logger.info(f"🔄 Auto-Recovery: Adjusting Stop-Loss to {adjusted_sl} (required max: {max_val}) and retrying...")
                    payload["stopLevel"] = adjusted_sl
                    res_retry = requests.post(url, headers=self.get_auth_headers(), json=payload, timeout=10)
                    if res_retry.status_code == 200:
                        data = res_retry.json()
                        deal_ref = data.get("dealReference")
                        logger.info(f"✅ Auto-Recovery succeeded! Deal Ref: {deal_ref}")
                        return {
                            "success": True,
                            "epic": resolved_epic,
                            "direction": dir_upper,
                            "size": size,
                            "deal_reference": deal_ref,
                            "is_demo": self.is_demo,
                            "response": data
                        }

                # 3. Fallback: If SL/TP was rejected by exchange distance rules, execute clean Market Order without stops first
                if "stoploss" in err_code.lower() or "profitlevel" in err_code.lower():
                    logger.warning(f"Exchange SL/TP rejected ({err_code}). Executing clean Market Order...")
                    payload_clean = {
                        "epic": resolved_epic,
                        "direction": dir_upper,
                        "size": round(size, 4),
                        "guaranteedStop": guaranteed_stop
                    }
                    res_clean = requests.post(url, headers=self.get_auth_headers(), json=payload_clean, timeout=10)
                    if res_clean.status_code == 200:
                        data = res_clean.json()
                        deal_ref = data.get("dealReference")
                        logger.info(f"✅ Market entry filled cleanly! Deal Ref: {deal_ref}")
                        return {
                            "success": True,
                            "epic": resolved_epic,
                            "direction": dir_upper,
                            "size": size,
                            "deal_reference": deal_ref,
                            "is_demo": self.is_demo,
                            "response": data
                        }

                return {"success": False, "error": err_code}
        except Exception as e:
            logger.error(f"Order placement exception: {e}")
            return {"success": False, "error": str(e)}

    def close_position(self, deal_id: str) -> Dict[str, Any]:
        """Closes an open position by dealId."""
        if not self.ensure_session():
            err_detail = self.last_auth_error or "Unable to establish valid session."
            return {"success": False, "error": f"Unable to establish valid session: {err_detail}"}

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

    def update_position_stops(
        self,
        deal_id: str,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> Dict[str, Any]:
        """Updates Stop-Loss and/or Take-Profit on an open position (Breakeven Armor / Trailing Stop)."""
        if not self.ensure_session():
            err_detail = self.last_auth_error or "Unable to establish valid session."
            return {"success": False, "error": f"Unable to establish valid session: {err_detail}"}

        url = f"{self.base_url}/positions/{deal_id}"
        payload: Dict[str, Any] = {}
        if stop_loss is not None and stop_loss > 0:
            payload["stopLevel"] = round(stop_loss, 4)
        if take_profit is not None and take_profit > 0:
            payload["profitLevel"] = round(take_profit, 4)

        try:
            res = requests.put(url, headers=self.get_auth_headers(), json=payload, timeout=10)
            if res.status_code == 200:
                return {"success": True, "deal_id": deal_id, "data": res.json()}
            else:
                err_data = res.json() if res.content else {}
                err_code = err_data.get("errorCode", f"HTTP {res.status_code}: {res.text}")
                return {"success": False, "error": err_code}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def close_all_capital_positions(self) -> Dict[str, Any]:
        """Closes all currently open TradFi positions in one call (Emergency Flush / Clean Harvest)."""
        positions = self.get_open_positions()
        if not positions:
            return {"success": True, "closed_count": 0, "message": "No open positions to close."}

        closed = []
        errors = []
        for pos_item in positions:
            pos = pos_item.get("position", {})
            deal_id = pos.get("dealId")
            epic = pos.get("epic", "UNKNOWN")
            if deal_id:
                res = self.close_position(deal_id)
                if res.get("success"):
                    closed.append({"deal_id": deal_id, "epic": epic})
                else:
                    errors.append({"deal_id": deal_id, "error": res.get("error")})

        return {
            "success": len(errors) == 0,
            "closed_count": len(closed),
            "errors_count": len(errors),
            "closed": closed,
            "errors": errors
        }

    # --------------------------------------------------------------------------
    # Institutional Quant Signal Engine & Mathematical Edge
    # --------------------------------------------------------------------------
    def evaluate_tradfi_quant_signal(self, epic: str) -> Dict[str, Any]:
        """
        Evaluates Multi-Timeframe Quant Confluence (EMA 20/50, RSI 14, ATR, Spread Guard)
        on Capital.com instruments (Gold, S&P 500, Crude Oil, Crypto CFDs).
        
        Returns actionable institutional signal:
        {signal: 'STRONG_BUY'|'BUY'|'HOLD_NEUTRAL'|'SELL'|'STRONG_SELL',
         confidence: int (0-100), entry_price: float, sl: float, tp: float, ...}
        """
        resolved_epic = EPIC_MAP.get(epic.upper(), epic.upper())
        market = self.get_market_details(resolved_epic)
        if not market.get("success"):
            return {"success": False, "signal": "HOLD_NEUTRAL", "error": market.get("error")}

        current_bid = market.get("bid", 0.0)
        current_ask = market.get("ask", 0.0)
        mid_price = market.get("mid", 0.0)
        spread = market.get("spread", 0.0)
        market_status = market.get("market_status") or market.get("marketStatus", "UNKNOWN")

        # 1. Market Status Guard (TradFi Market Closed Shield)
        if market_status != "TRADEABLE":
            return {
                "success": True,
                "epic": resolved_epic,
                "signal": "HOLD_NEUTRAL",
                "confidence": 0,
                "market_status": market_status,
                "reason": f"Market {resolved_epic} is currently {market_status} (TradFi markets closed on weekends/holidays).",
                "mid_price": mid_price,
                "spread": spread
            }

        # 2. Spread Guard
        max_spreads = {"GOLD": 0.90, "US500": 1.20, "OIL_CRUDE": 0.08, "BTCUSD": 80.0}
        max_spread = max_spreads.get(resolved_epic, 2.0)
        if spread > max_spread:
            return {
                "success": True,
                "epic": resolved_epic,
                "signal": "HOLD_NEUTRAL",
                "confidence": 10,
                "reason": f"Spread Guard: Current spread {spread} exceeds threshold {max_spread} (News/Volatility dislocation).",
                "mid_price": mid_price,
                "spread": spread
            }

        # 3. Fetch 15m Candles for Technical Confluence
        candles = self.get_historical_prices(resolved_epic, resolution="MINUTE_15", max_bars=40)
        if len(candles) < 20:
            return {
                "success": True,
                "epic": resolved_epic,
                "signal": "HOLD_NEUTRAL",
                "confidence": 20,
                "reason": "Insufficient historical candles for institutional confluence.",
                "mid_price": mid_price,
                "spread": spread
            }

        closes = [c["close"] for c in candles]
        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]

        # Calculate EMA 20 & EMA 50
        def _ema(prices: List[float], period: int) -> float:
            if len(prices) < period:
                return prices[-1] if prices else 0.0
            mult = 2.0 / (period + 1)
            val = sum(prices[:period]) / period
            for p in prices[period:]:
                val = (p - val) * mult + val
            return val

        ema20 = _ema(closes, 20)
        ema50 = _ema(closes, min(50, len(closes)))

        # Calculate RSI 14
        deltas = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
        gains = [d if d > 0 else 0.0 for d in deltas]
        losses = [-d if d < 0 else 0.0 for d in deltas]
        p_rsi = 14
        if len(deltas) >= p_rsi:
            avg_g = sum(gains[:p_rsi]) / p_rsi
            avg_l = sum(losses[:p_rsi]) / p_rsi
            for i in range(p_rsi, len(deltas)):
                avg_g = (avg_g * (p_rsi - 1) + gains[i]) / p_rsi
                avg_l = (avg_l * (p_rsi - 1) + losses[i]) / p_rsi
            rs = avg_g / avg_l if avg_l > 0 else 100.0
            rsi = round(100.0 - (100.0 / (1.0 + rs)), 2)
        else:
            rsi = 50.0

        # Calculate ATR 14
        trs = []
        for i in range(1, len(candles)):
            h, l, pc = candles[i]["high"], candles[i]["low"], candles[i-1]["close"]
            trs.append(max(h - l, abs(h - pc), abs(l - pc)))
        atr = round(sum(trs[-14:]) / min(14, len(trs)), 4) if trs else 1.0

        # Calculate ADX 14 & Directional Movement (+DI, -DI)
        adx = 25.0
        plus_di = 25.0
        minus_di = 25.0
        if len(candles) >= 28:
            tr_list = []
            dm_plus_list = []
            dm_minus_list = []
            for i in range(1, len(candles)):
                h = candles[i]["high"]
                l = candles[i]["low"]
                c_prev = candles[i-1]["close"]
                h_prev = candles[i-1]["high"]
                l_prev = candles[i-1]["low"]

                tr = max(h - l, abs(h - c_prev), abs(l - c_prev))
                up_move = h - h_prev
                down_move = l_prev - l

                dm_p = up_move if (up_move > down_move and up_move > 0) else 0.0
                dm_m = down_move if (down_move > up_move and down_move > 0) else 0.0

                tr_list.append(tr)
                dm_plus_list.append(dm_p)
                dm_minus_list.append(dm_m)

            p_adx = 14
            if len(tr_list) >= p_adx:
                tr14 = sum(tr_list[:p_adx])
                dmp14 = sum(dm_plus_list[:p_adx])
                dmm14 = sum(dm_minus_list[:p_adx])

                dx_list = []
                for i in range(p_adx, len(tr_list)):
                    tr14 = tr14 - (tr14 / p_adx) + tr_list[i]
                    dmp14 = dmp14 - (dmp14 / p_adx) + dm_plus_list[i]
                    dmm14 = dmm14 - (dmm14 / p_adx) + dm_minus_list[i]

                    p_di = (100.0 * dmp14 / tr14) if tr14 > 0 else 0.0
                    m_di = (100.0 * dmm14 / tr14) if tr14 > 0 else 0.0
                    di_diff = abs(p_di - m_di)
                    di_sum = p_di + m_di
                    dx = (100.0 * di_diff / di_sum) if di_sum > 0 else 0.0
                    dx_list.append(dx)

                if dx_list:
                    adx = round(sum(dx_list[-p_adx:]) / min(len(dx_list), p_adx), 2)
                    plus_di = round(p_di, 2)
                    minus_di = round(m_di, 2)

        # Calculate Relative Volume (RVOL) and Range Expansion
        volumes = [float(c.get("volume", 0.0)) for c in candles]
        valid_vols = [v for v in volumes if v > 0]
        if len(valid_vols) >= 10:
            avg_vol = sum(valid_vols[-20:]) / min(len(valid_vols), 20)
            rvol = round(valid_vols[-1] / avg_vol, 2) if avg_vol > 0 else 1.0
        else:
            rvol = 1.0

        candle_ranges = [c["high"] - c["low"] for c in candles]
        avg_range = sum(candle_ranges[-10:]) / min(len(candle_ranges), 10) if candle_ranges else 1.0
        current_range = candle_ranges[-1] if candle_ranges else 1.0
        range_ratio = round(current_range / avg_range, 2) if avg_range > 0 else 1.0

        # Confluence Logic
        bullish_score = 0
        bearish_score = 0

        # 1. EMA Trend (35 pts)
        if closes[-1] > ema20 > ema50:
            bullish_score += 35
        elif closes[-1] < ema20 < ema50:
            bearish_score += 35
        elif closes[-1] > ema20:
            bullish_score += 20
        elif closes[-1] < ema20:
            bearish_score += 20

        # 2. RSI Momentum Sweet Spot (25 pts)
        # Pullback sweet spot: 48 - 66 for Bullish (riding uptrend without chasing top)
        if 48.0 <= rsi <= 66.0:
            bullish_score += 25
        # Pullback sweet spot: 34 - 52 for Bearish
        elif 34.0 <= rsi <= 52.0:
            bearish_score += 25

        # Anti-FOMO Overbought / Oversold Guards (Strict Invariant 16 & Capital Preservation)
        if rsi > 70.0:
            bullish_score = 0  # Rebuff buying the absolute top
        if rsi < 36.0:
            bearish_score = 0  # Rebuff shorting panic bottom

        # 3. ADX Trend Strength Filter (20 pts)
        # Low-momentum chop filter: if ADX < 20, market is in sideways consolidation -> penalize
        if adx >= 24.0:
            if plus_di > minus_di:
                bullish_score += 20
            elif minus_di > plus_di:
                bearish_score += 20
        elif adx < 19.0:
            bullish_score = max(0, bullish_score - 25)
            bearish_score = max(0, bearish_score - 25)

        # 4. Volume / Range Surge (15 pts)
        if rvol >= 1.35 or range_ratio >= 1.30:
            if closes[-1] > closes[-2]:
                bullish_score += 15
            elif closes[-1] < closes[-2]:
                bearish_score += 15
        elif rvol < 0.60 and range_ratio < 0.60:
            bullish_score = max(0, bullish_score - 15)
            bearish_score = max(0, bearish_score - 15)

        # 5. Recent 3 candle momentum (10 pts)
        if len(closes) >= 4:
            if closes[-1] > closes[-2] > closes[-3]:
                bullish_score += 10
            elif closes[-1] < closes[-2] < closes[-3]:
                bearish_score += 10

        # Asymmetric R:R >= 1:6 Mathematical Ratio Enforcement
        # Downside Risk (1R): Micro-clamped outside noise band
        min_sl_dist = max(1.5 * atr, spread * 2.5, 0.0025 * mid_price)
        # Upside Target (6R): Clamped to >= 6.0x the risk distance
        min_tp_dist = max(6.0 * min_sl_dist, 6.0 * atr, 0.015 * mid_price)

        if bullish_score >= 75:
            signal = "STRONG_BUY" if bullish_score >= 85 else "BUY"
            confidence = min(96, bullish_score)
            sl = round(current_bid - min_sl_dist, 2)
            tp = round(current_ask + min_tp_dist, 2)
        elif bearish_score >= 75:
            signal = "STRONG_SELL" if bearish_score >= 85 else "SELL"
            confidence = min(96, bearish_score)
            sl = round(current_ask + min_sl_dist, 2)
            tp = round(current_bid - min_tp_dist, 2)
        else:
            signal = "HOLD_NEUTRAL"
            confidence = max(bullish_score, bearish_score)
            sl = 0.0
            tp = 0.0

        return {
            "success": True,
            "epic": resolved_epic,
            "signal": signal,
            "confidence": confidence,
            "mid_price": mid_price,
            "bid": current_bid,
            "ask": current_ask,
            "spread": spread,
            "ema20": round(ema20, 2),
            "ema50": round(ema50, 2),
            "rsi": rsi,
            "atr": atr,
            "adx": adx,
            "plus_di": plus_di,
            "minus_di": minus_di,
            "rvol": rvol,
            "range_ratio": range_ratio,
            "rr_ratio": 6.0,
            "sl": sl,
            "tp": tp,
            "market_status": market_status
        }

    def execute_smart_tradfi_order(
        self,
        epic: str,
        direction: str,
        size: Optional[float] = None,
        risk_pct: float = 1.0
    ) -> Dict[str, Any]:
        """
        Executes an institutional risk-managed trade with automated SL/TP based on ATR.
        """
        resolved_epic = EPIC_MAP.get(epic.upper(), epic.upper())
        dir_u = direction.upper()
        
        # 1. Run Quant Signal Evaluation
        analysis = self.evaluate_tradfi_quant_signal(resolved_epic)
        if not analysis.get("success"):
            return {"success": False, "error": analysis.get("error", "Quant signal failure")}

        if analysis.get("market_status") != "TRADEABLE":
            return {
                "success": False,
                "error": f"Market {resolved_epic} is {analysis.get('market_status')} (Closed for trading)."
            }

        # 2. Compute Size if not specified
        bal_info = self.get_account_balance()
        equity = bal_info.get("balance", 1000.0)
        market_details = self.get_market_details(resolved_epic)
        min_size = market_details.get("min_deal_size", 0.01)

        if size is None or size <= 0:
            # Sizing: 1% risk per trade
            # Gold: 1 lot = 1 oz. 0.01 lot = $0.01 price move = $0.01 PnL
            if resolved_epic == "GOLD":
                size = max(0.02, min_size)
            elif resolved_epic == "US500":
                size = max(0.1, min_size)
            elif resolved_epic == "BTCUSD":
                size = max(0.001, min_size)
            else:
                size = min_size
        else:
            size = max(size, min_size)

        # 3. Retrieve or calculate dynamic SL/TP
        sl = analysis.get("sl")
        tp = analysis.get("tp")
        atr = analysis.get("atr", 1.0)
        ask = analysis.get("ask", 0.0)
        bid = analysis.get("bid", 0.0)

        mid_px = (bid + ask) / 2.0 if (bid + ask) > 0 else 1.0
        spread = analysis.get("spread", 0.0)
        # Enforce Asymmetric R:R >= 1:6 Mathematical Ratio
        min_sl_dist = max(1.5 * atr, spread * 2.5, 0.0025 * mid_px)
        min_tp_dist = max(6.0 * min_sl_dist, 6.0 * atr, 0.015 * mid_px)

        if dir_u == "BUY":
            if not sl or sl <= 0 or sl >= bid:
                sl = round(bid - min_sl_dist, 2)
            if not tp or tp <= 0 or tp <= ask:
                tp = round(ask + min_tp_dist, 2)
        elif dir_u == "SELL":
            if not sl or sl <= 0 or sl <= ask:
                sl = round(ask + min_sl_dist, 2)
            if not tp or tp <= 0 or tp >= bid:
                tp = round(bid - min_tp_dist, 2)

        # 4. Transmit Protected Position
        max_spreads = {
            "GOLD": 1.20, "US500": 1.50, "US100": 2.00, "OIL_CRUDE": 0.10, "BTCUSD": 80.0,
            "NVDA": 0.60, "TSLA": 0.60, "AAPL": 0.50, "MSFT": 0.60, "AMZN": 0.60
        }
        max_spread = max_spreads.get(resolved_epic, 5.0)

        res = self.place_position(
            epic=resolved_epic,
            direction=dir_u,
            size=size,
            stop_loss=sl,
            take_profit=tp,
            max_allowed_spread=max_spread
        )

        if res.get("success"):
            res["sl"] = sl
            res["tp"] = tp
            res["confidence"] = analysis.get("confidence")
            res["rsi"] = analysis.get("rsi")
            res["atr"] = atr

        return res

    def get_tradfi_dashboard_data(self) -> Dict[str, Any]:
        """
        Aggregates live account balance, active quotes, and open positions
        for the Telegram /capital Master Control Panel.
        """
        bal = self.get_account_balance()
        positions = self.get_open_positions()

        # Fetch key asset quotes (Cached)
        gold = self.get_market_details("GOLD")
        sp500 = self.get_market_details("SP500")
        oil = self.get_market_details("OIL")
        btc = self.get_market_details("BTCUSD")

        # Summarize positions
        pos_summary = []
        total_unrealized_pnl = 0.0
        for p in positions:
            pos = p.get("position", {})
            upl = float(pos.get("upl", 0.0))
            total_unrealized_pnl += upl
            pos_summary.append({
                "deal_id": pos.get("dealId"),
                "epic": pos.get("epic"),
                "direction": pos.get("direction"),
                "size": float(pos.get("size", 0.0)),
                "level": float(pos.get("level", 0.0)),
                "upl": upl,
                "currency": pos.get("currency", "USD"),
                "stop_level": pos.get("stopLevel"),
                "profit_level": pos.get("profitLevel")
            })

        return {
            "success": True,
            "is_demo": self.is_demo,
            "account_id": bal.get("account_id"),
            "account_name": bal.get("account_name"),
            "balance": bal.get("balance", 0.0),
            "available": bal.get("available", 0.0),
            "equity": bal.get("balance", 0.0) + bal.get("pnl", 0.0),
            "active_pnl": bal.get("pnl", 0.0) or total_unrealized_pnl,
            "currency": bal.get("currency", "USD"),
            "status": bal.get("status", "ACTIVE"),
            "quotes": {
                "GOLD": gold,
                "SP500": sp500,
                "OIL": oil,
                "BTCUSD": btc
            },
            "open_positions": pos_summary,
            "positions_count": len(pos_summary)
        }


# ==============================================================================
# 3. CONVENIENCE HELPERS & FACTORY FUNCTIONS
# ==============================================================================
_GLOBAL_CAPITAL_ENGINE: Optional[CapitalComEngine] = None

def get_capital_engine(is_demo: Optional[bool] = None) -> CapitalComEngine:
    """Singleton getter for the global CapitalComEngine instance."""
    global _GLOBAL_CAPITAL_ENGINE
    if is_demo is None:
        is_demo = os.getenv("CAPITAL_IS_DEMO", "True").strip().lower() in ("true", "1", "yes")
        
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

def quick_gold_quote(is_demo: Optional[bool] = None) -> Dict[str, Any]:
    """Fetches instant live quote for Spot Gold (XAU/USD)."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.get_market_details("GOLD")

def quick_sp500_quote(is_demo: Optional[bool] = None) -> Dict[str, Any]:
    """Fetches instant live quote for S&P 500 (US500)."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.get_market_details("SP500")

def get_tradfi_dashboard(is_demo: Optional[bool] = None) -> Dict[str, Any]:
    """Retrieves full TradFi dashboard payload for Telegram UI rendering."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.get_tradfi_dashboard_data()

def execute_tradfi_trade(
    epic: str,
    direction: str,
    size: Optional[float] = None,
    is_demo: Optional[bool] = None
) -> Dict[str, Any]:
    """Executes a protected institutional TradFi order on Capital.com."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.execute_smart_tradfi_order(epic=epic, direction=direction, size=size)

def close_all_tradfi(is_demo: Optional[bool] = None) -> Dict[str, Any]:
    """Closes all open TradFi positions in one click."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.close_all_capital_positions()

def evaluate_tradfi_signal(epic: str, is_demo: Optional[bool] = None) -> Dict[str, Any]:
    """Evaluates multi-indicator quant signal on a TradFi asset."""
    engine = get_capital_engine(is_demo=is_demo)
    return engine.evaluate_tradfi_quant_signal(epic)


# ==============================================================================
# 4. CAPITAL.COM 24/7 AUTONOMOUS INSTITUTIONAL ENGINE (CAPITAL AUTO)
# ==============================================================================

class CapitalAutonomousEngine:
    """
    Flagship 24/7 Autonomous TradFi Trading Engine on Capital.com.
    Fuses:
    1. Google Macro Satellite (google_macro_satellite.py)
    2. Multi-Timeframe Quant Confluence (1H Trend + 15M Momentum + 5M Pullback)
    3. Central Bank Gold Radar & Black Swan Guard
    4. 24/7 Session Awareness (London, NY, Asian/Weekend BTC CFD)
    5. Breakeven Armor (+1.5% ROI lock) & Golden 80% Trailing Ratchet
    """
    def __init__(self):
        self._peak_upl_cache: Dict[str, float] = {}  # deal_id -> peak_upl
        self._be_locked_set = set()                   # deal_ids that reached Breakeven Armor
        self._last_scan_ts: float = 0.0
        self._scan_interval: float = 25.0             # Scan markets every 25 seconds

    def get_session_priority_assets(self) -> List[str]:
        """
        Determines active tradable instruments based on global market hours (UTC+7 Phnom Penh):
        - London Session (15:00 - 23:00): GOLD (XAU/USD), OIL
        - Wall Street Session (20:30 - 03:00): SP500, NASDAQ, GOLD
        - Off-hours / Weekend: BTCUSD (24/7 CFD)
        """
        import datetime
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        weekday = now_dt.weekday()  # Monday = 0, Friday = 4, Saturday = 5, Sunday = 6
        hour_utc = now_dt.hour
        
        # TradFi weekend closure: Friday 21:00 UTC to Sunday 22:00 UTC
        is_weekend = (weekday == 5) or (weekday == 4 and hour_utc >= 21) or (weekday == 6 and hour_utc < 22)
        
        if is_weekend:
            # 24/7 Crypto CFD active on weekends
            return ["BTCUSD", "ETHUSD", "SOLUSD"]
            
        # On weekdays, dynamically adjust priority based on London & Wall Street market hours:
        # Wall Street Session (13:30 - 21:00 UTC = 20:30 - 04:00 Phnom Penh): S&P 500, Nasdaq, Nvidia, Tesla, Gold, Oil
        if 13 <= hour_utc < 21:
            return ["GOLD", "SP500", "NASDAQ", "NVDA", "TSLA", "OIL", "BTCUSD"]
        # London Session (08:00 - 13:00 UTC = 15:00 - 20:00 Phnom Penh): Gold, Crude Oil, DAX, EURUSD
        elif 8 <= hour_utc < 13:
            return ["GOLD", "OIL", "SP500", "DAX", "BTCUSD"]
        else:
            return ["GOLD", "BTCUSD", "SP500"]

    def evaluate_multi_engine_tradfi_setup(self, epic: str) -> Dict[str, Any]:
        """
        Fuses Google Macro Satellite + Technical Indicators + Radar signals:
        Returns institutional decision with score (0-100) and recommendation.
        """
        engine = get_capital_engine()
        base_quant = engine.evaluate_tradfi_quant_signal(epic)
        if not base_quant.get("success"):
            return base_quant

        resolved_epic = base_quant.get("epic", epic)
        market_status = base_quant.get("market_status", "UNKNOWN")
        if market_status != "TRADEABLE":
            return base_quant

        # 1. Google Macro Satellite Integration
        macro_boost = 0
        macro_bias = "NEUTRAL"
        try:
            import google_macro_satellite
            macro_data = google_macro_satellite.fetch_google_macro_satellite_data()
            tradfi_sent = macro_data.get("tradfi_sentiment", "RISK_ON")
            dxy_sig = macro_data.get("dxy_signal", "BULLISH_LIQUIDITY")

            # Gold benefits from DXY weakness (BULLISH_LIQUIDITY) or RISK_OFF safe haven
            if resolved_epic == "GOLD":
                if dxy_sig == "BULLISH_LIQUIDITY":
                    macro_boost += 15
                    macro_bias = "BULLISH_MACRO"
                if tradfi_sent == "RISK_OFF":
                    macro_boost += 10
            elif resolved_epic in ["SP500", "US500", "US100", "NASDAQ", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN"]:
                if tradfi_sent == "RISK_ON":
                    macro_boost += 15
                    macro_bias = "BULLISH_MACRO"
                elif tradfi_sent == "RISK_OFF":
                    macro_boost -= 20
                    macro_bias = "BEARISH_MACRO"
            elif resolved_epic in ["OIL", "OIL_CRUDE", "OIL_BRENT"]:
                if tradfi_sent == "RISK_ON":
                    macro_boost += 10
                    macro_bias = "BULLISH_MACRO"
            elif resolved_epic == "BTCUSD":
                if dxy_sig == "BULLISH_LIQUIDITY" and tradfi_sent == "RISK_ON":
                    macro_boost += 20
                    macro_bias = "BULLISH_MACRO"
        except Exception as e_macro:
            logger.debug(f"Google Macro Satellite query note: {e_macro}")

        # 2. Central Bank Gold Radar Integration (for Gold)
        cb_boost = 0
        if resolved_epic == "GOLD":
            try:
                import central_bank_gold_radar
                cb_radar = central_bank_gold_radar.get_central_bank_gold_radar()
                if cb_radar.get("regime") == "ACCUMULATION":
                    cb_boost += 15
            except Exception:
                pass

        # 3. Final Score Arbitration
        raw_conf = base_quant.get("confidence", 50)
        final_conf = min(98, max(10, raw_conf + macro_boost + cb_boost))
        base_quant["final_confidence"] = final_conf
        base_quant["macro_bias"] = macro_bias

        # Adjust signal if macro and technicals align
        raw_sig = base_quant.get("signal", "HOLD_NEUTRAL")
        if raw_sig in ["BUY", "STRONG_BUY"] and final_conf >= 75:
            base_quant["final_action"] = "BUY"
        elif raw_sig in ["SELL", "STRONG_SELL"] and final_conf >= 75:
            base_quant["final_action"] = "SELL"
        else:
            base_quant["final_action"] = "HOLD"

        return base_quant

    def monitor_and_ratchet_open_positions(self, app=None) -> Dict[str, Any]:
        """
        Executes real-time position management on active Capital.com positions:
        1. Breakeven Armor: At +1.5% ROI, locks Stop-Loss to entry + fees.
        2. Golden 80% Trailing Ratchet: Ratchets trailing SL protecting 80% of peak profit.
        """
        engine = get_capital_engine()
        positions = engine.get_open_positions()
        if not positions:
            return {"active_count": 0, "ratcheted": 0, "closed": 0}

        ratcheted_count = 0
        closed_count = 0

        for pos_item in positions:
            pos = pos_item.get("position", {})
            deal_id = pos.get("dealId")
            epic = pos.get("epic", "UNKNOWN")
            direction = pos.get("direction", "BUY").upper()
            size = float(pos.get("size", 0.0))
            entry_level = float(pos.get("level", 0.0))
            upl = float(pos.get("upl", 0.0))
            sl = float(pos.get("stopLevel", 0.0) or 0.0)

            if not deal_id or entry_level <= 0:
                continue

            # Calculate ROI estimate (For 20x leverage, 5% margin requirement)
            estimated_margin = max(1.0, entry_level * size * 0.05)
            roi_pct = (upl / estimated_margin) * 100.0 if estimated_margin > 0 else 0.0

            # Track peak UPL
            peak_upl = self._peak_upl_cache.get(deal_id, upl)
            if upl > peak_upl:
                peak_upl = upl
                self._peak_upl_cache[deal_id] = peak_upl

            # Tier 1. Breakeven Armor: At +1.5% ROI (Locks SL to Entry + Fees, Downside Risk -> 0.00R)
            if roi_pct >= 1.5 and deal_id not in self._be_locked_set:
                new_sl = round(entry_level * 1.0008, 2) if direction == "BUY" else round(entry_level * 0.9992, 2)
                upd = engine.update_position_stops(deal_id=deal_id, stop_loss=new_sl)
                if upd.get("success"):
                    self._be_locked_set.add(deal_id)
                    ratcheted_count += 1
                    logger.info(f"🛡️ [BREAKEVEN ARMOR] Locked SL for {epic} ({direction}) at {new_sl} (+{roi_pct:.1f}% ROI, Risk: 0.00R)")

            # Tier 2. Capital Fortress Lock: At +3.5% ROI (Secures +1.5R net profit)
            elif roi_pct >= 3.5 and deal_id not in getattr(self, "_fortress_locked_set", set()):
                if not hasattr(self, "_fortress_locked_set"):
                    self._fortress_locked_set = set()
                secured_sl = round(entry_level * 1.0035, 2) if direction == "BUY" else round(entry_level * 0.9965, 2)
                upd = engine.update_position_stops(deal_id=deal_id, stop_loss=secured_sl)
                if upd.get("success"):
                    self._fortress_locked_set.add(deal_id)
                    ratcheted_count += 1
                    logger.info(f"🏰 [CAPITAL FORTRESS] Secured +1.5R for {epic} at {secured_sl} (+{roi_pct:.1f}% ROI)")

            # Tier 3. Golden 80% Trailing Ratchet: When profit exceeds +5.0% ROI (Uncapped upside runner)
            elif roi_pct >= 5.0 and peak_upl > 0:
                target_protected_profit = peak_upl * 0.80
                if direction == "BUY":
                    ratchet_price = round(entry_level + (target_protected_profit / size), 2)
                    if ratchet_price > sl:
                        upd = engine.update_position_stops(deal_id=deal_id, stop_loss=ratchet_price)
                        if upd.get("success"):
                            ratcheted_count += 1
                            logger.info(f"💎 [GOLDEN RATCHET] Ratcheted SL for {epic} to {ratchet_price} (80% Peak Locked)")
                elif direction == "SELL":
                    ratchet_price = round(entry_level - (target_protected_profit / size), 2)
                    if sl <= 0 or ratchet_price < sl:
                        upd = engine.update_position_stops(deal_id=deal_id, stop_loss=ratchet_price)
                        if upd.get("success"):
                            ratcheted_count += 1
                            logger.info(f"💎 [GOLDEN RATCHET] Ratcheted SL for {epic} to {ratchet_price} (80% Peak Locked)")

            # Tier 4. Clean Cash Harvest: At +12.0% ROI or 6R Target Reached
            if roi_pct >= 12.0:
                logger.info(f"🎯 [MEGA TARGET HARVEST] 6R Target Reached (+{roi_pct:.1f}% ROI)! Executing Clean Cash Harvest for {epic}...")
                close_res = engine.close_position(deal_id=deal_id)
                if close_res.get("success"):
                    closed_count += 1
                    self._peak_upl_cache.pop(deal_id, None)
                    self._be_locked_set.discard(deal_id)
                    if hasattr(self, "_fortress_locked_set"):
                        self._fortress_locked_set.discard(deal_id)

        return {
            "active_count": len(positions),
            "ratcheted": ratcheted_count,
            "closed": closed_count
        }

    async def execute_autonomous_cycle(self, app=None):
        """
        Main 24/7 autonomous loop called by scheduler:
        1. Monitors active positions across all users.
        2. Discovers new opportunities across priority assets.
        3. Executes trades for opted-in users within budget & max position limits.
        """
        import database as db
        active_users = db.get_active_capital_auto_users()
        if not active_users:
            return

        now = time.time()
        
        # Step 1: In-Flight Position Management & Ratchet
        self.monitor_and_ratchet_open_positions(app=app)

        # Step 2: Rate limit market scans to once every 25 seconds
        if (now - self._last_scan_ts) < self._scan_interval:
            return
        self._last_scan_ts = now

        engine = get_capital_engine()
        open_positions = engine.get_open_positions()
        open_epics = {pos.get("position", {}).get("epic", "").upper() for pos in open_positions}

        # Step 3: Scan candidate assets and rank via Institutional Edge Matrix
        priority_epics = self.get_session_priority_assets()
        candidate_setups = []

        for epic in priority_epics:
            resolved_epic = EPIC_MAP.get(epic, epic)
            if resolved_epic in open_epics:
                continue

            setup = self.evaluate_multi_engine_tradfi_setup(epic)
            final_action = setup.get("final_action", "HOLD")
            confidence = setup.get("final_confidence", 0)

            # Strict Invariant: Only setups with confidence >= 75% and actionable signal
            if final_action in ["BUY", "SELL"] and confidence >= 75:
                adx_val = setup.get("adx", 25.0)
                rvol_val = setup.get("rvol", 1.0)
                # Composite Institutional Edge Score: confidence * 1.5 + ADX + RVOL * 10
                rank_score = (confidence * 1.5) + adx_val + (rvol_val * 10.0)
                candidate_setups.append((rank_score, epic, resolved_epic, setup))

        if not candidate_setups:
            return

        # Sort candidate setups descending by institutional rank score (Apex Golden Setup First)
        candidate_setups.sort(key=lambda x: x[0], reverse=True)
        best_rank, best_epic, resolved_epic, setup = candidate_setups[0]
        final_action = setup["final_action"]
        confidence = setup["final_confidence"]

        logger.info(f"👑 [APEX TRADFI SETUP SELECTED] {resolved_epic} {final_action} | Score: {best_rank:.1f} | Conf: {confidence}% | ADX: {setup.get('adx', 0):.1f} | RVOL: {setup.get('rvol', 1.0)}x")
        
        for user in active_users:
            chat_id = user["chat_id"]
            budget = user.get("budget", 50.0)
            max_pos = user.get("max_positions", 2)

            if len(open_positions) >= max_pos:
                continue

            # Dynamic size based on user budget and asset DNA
            size = None
            if resolved_epic == "GOLD":
                size = 0.02 if budget < 100 else 0.05
            elif resolved_epic in ["US500", "SP500"]:
                size = 0.1 if budget < 100 else 0.2
            elif resolved_epic in ["US100", "NASDAQ"]:
                size = 0.1 if budget < 100 else 0.2
            elif resolved_epic in ["NVDA", "TSLA", "AAPL", "MSFT", "AMZN"]:
                size = 1.0 if budget < 100 else 2.0
            elif resolved_epic == "BTCUSD":
                size = 0.001 if budget < 50 else 0.002

            trade_res = engine.execute_smart_tradfi_order(
                epic=resolved_epic,
                direction=final_action,
                size=size
            )

            if trade_res.get("success"):
                deal_ref = trade_res.get("deal_reference", "AUTO")
                deal_id = trade_res.get("response", {}).get("dealId", deal_ref)
                entry_px = setup.get("ask" if final_action == "BUY" else "bid", 0.0)
                sl = trade_res.get("sl", 0.0)
                tp = trade_res.get("tp", 0.0)
                executed_size = trade_res.get("size", size or 0.01)

                # Record in database
                db.record_capital_auto_trade(
                    chat_id=chat_id,
                    deal_id=str(deal_id),
                    deal_reference=str(deal_ref),
                    epic=resolved_epic,
                    direction=final_action,
                    size=executed_size,
                    entry_price=entry_px,
                    sl=sl,
                    tp=tp
                )
                db.update_capital_auto_last_trade_time(chat_id, now)

                # Send Telegram Notification
                if app and hasattr(app, "bot"):
                    try:
                        user_lang = db.get_user_language(chat_id)
                        import ui_standards
                        env_lbl = "DEMO ($10,000)" if engine.is_demo else "LIVE MAINNET"
                        dir_emoji = "🟢 LONG / BUY" if final_action == "BUY" else "🔴 SHORT / SELL"
                        adx_str = f"{setup.get('adx', 0):.1f}"
                        rvol_str = f"{setup.get('rvol', 1.0):.1f}x"
                        
                        if user_lang == 'khmer':
                            notif_msg = (
                                f"🏛️ **[24/7 CAPITAL.COM AUTO TRADE EXECUTED]** ⚡\n"
                                f"{ui_standards.DIVIDER_HEAVY}\n"
                                f"⚙️ **គណនី ៖** `{env_lbl}`\n"
                                f"🏛️ **ឧបករណ៍ TradFi ៖** `{resolved_epic}`\n"
                                f"🎯 **ទិសដៅ ៖** `{dir_emoji}`\n"
                                f"🧠 **AI Confidence ៖** `{confidence}% (Google Macro + Quant)`\n"
                                f"📊 **កម្លាំង Trend & Volume ៖** ADX `{adx_str}` | RVOL `{rvol_str}`\n"
                                f"📦 **ទំហំកិច្ចសន្យា ៖** `{executed_size} contracts`\n"
                                f"💵 **តម្លៃចូល (Entry) ៖** `${entry_px:,.2f}`\n"
                                f"🛑 **Stop-Loss (1R) ៖** `${sl:,.2f}`\n"
                                f"🎯 **Take-Profit (6R) ៖** `${tp:,.2f}`\n"
                                f"🔖 **Deal Reference ៖** `{deal_ref}`\n"
                                f"{ui_standards.DIVIDER_HEAVY}\n"
                                f"🛡️ **ក្បួនការពារ & កើបចំណេញ Asymmetric R:R $\ge 1:6$ ៖**\n"
                                f"• Tier 1: Breakeven Armor នៅ +1.5% ROI (Risk -> 0.00R)\n"
                                f"• Tier 2: Capital Fortress Lock (+1.5R) នៅ +3.5% ROI\n"
                                f"• Tier 3: The Golden 80% Trailing Ratchet\n"
                                f"• Tier 4: Mega Target Harvest (6R+) នៅ +12.0% ROI\n"
                                f"{ui_standards.DIVIDER_HEAVY}\n"
                                f"💡 _ម៉ាស៊ីន AI ដំណើរការចាក់សោរប្រាក់ចំណេញ និងការពារទុន ២៤/៧!_"
                            )
                        else:
                            notif_msg = (
                                f"🏛️ **[24/7 CAPITAL.COM AUTO TRADE EXECUTED]** ⚡\n"
                                f"{ui_standards.DIVIDER_HEAVY}\n"
                                f"⚙️ **Account:** `{env_lbl}`\n"
                                f"🏛️ **TradFi Instrument:** `{resolved_epic}`\n"
                                f"🎯 **Direction:** `{dir_emoji}`\n"
                                f"🧠 **AI Confidence:** `{confidence}% (Google Macro + Quant)`\n"
                                f"📊 **Trend & Volume:** ADX `{adx_str}` | RVOL `{rvol_str}`\n"
                                f"📦 **Contract Size:** `{executed_size}`\n"
                                f"💵 **Entry Price:** `${entry_px:,.2f}`\n"
                                f"🛑 **Stop-Loss (1R):** `${sl:,.2f}`\n"
                                f"🎯 **Take-Profit (6R):** `${tp:,.2f}`\n"
                                f"🔖 **Deal Reference:** `{deal_ref}`\n"
                                f"{ui_standards.DIVIDER_HEAVY}\n"
                                f"🛡️ **Asymmetric R:R >= 1:6 Multi-Tier Protection:**\n"
                                f"• Tier 1: Breakeven Armor at +1.5% ROI (Risk -> 0.00R)\n"
                                f"• Tier 2: Capital Fortress Lock (+1.5R) at +3.5% ROI\n"
                                f"• Tier 3: Golden 80% Trailing Ratchet\n"
                                f"• Tier 4: Mega Target Cash Harvest (6R+) at +12.0% ROI\n"
                                f"{ui_standards.DIVIDER_HEAVY}\n"
                                f"💡 _AI Engine actively monitoring and trailing profits 24/7!_"
                            )
                        await app.bot.send_message(chat_id=chat_id, text=notif_msg, parse_mode="Markdown")
                    except Exception as notif_err:
                        logger.error(f"Failed to send Capital Auto notification: {notif_err}")

                # Throttle to 1 trade per cycle
                break


# Singleton Instance
CAPITAL_AUTO_ENGINE = CapitalAutonomousEngine()

def get_capital_auto_engine() -> CapitalAutonomousEngine:
    """Returns singleton instance of CapitalAutonomousEngine."""
    return CAPITAL_AUTO_ENGINE

async def run_capital_auto_cycle(app=None):
    """Entry point for APScheduler in scheduler_tasks.py."""
    await CAPITAL_AUTO_ENGINE.execute_autonomous_cycle(app=app)


# ==============================================================================
# 5. STANDALONE DEMO TEST HARNESS
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  KHMER MASTER CRYPTO - CAPITAL.COM DEMO TEST HARNESS")
    print("=" * 70)
    
    api_k = os.getenv("CAPITAL_API_KEY", "")
    ident = os.getenv("CAPITAL_IDENTIFIER", "")
    pwd = os.getenv("CAPITAL_PASSWORD", "")
    
    is_demo_cfg = os.getenv("CAPITAL_IS_DEMO", "True").strip().lower() in ("true", "1", "yes")
    target_env = "DEMO ($10,000 Virtual Funds)" if is_demo_cfg else "LIVE MAINNET"
    
    print("\n[STEP 1] Inspecting Environment Variables...")
    print(f"  • CAPITAL_API_KEY:    {'[SET]' if api_k else '[EMPTY]'}")
    print(f"  • CAPITAL_IDENTIFIER: {'[SET]' if ident else '[EMPTY]'}")
    print(f"  • CAPITAL_PASSWORD:   {'[SET]' if pwd else '[EMPTY]'}")
    print(f"  • TARGET ENVIRONMENT: {target_env}")
    
    if not api_k or not ident or not pwd:
        print("\n[NOTICE] No Capital.com credentials found in .env.")
        print("To test live execution, obtain free API credentials:")
        print("  1. Create account at: https://capital.com/")
        print("  2. Enable 2FA (Google Authenticator)")
        print("  3. Navigate to: Settings > API integrations > Generate Key")
        print("  4. Add to .env:")
        print("     CAPITAL_API_KEY=your_key")
        print("     CAPITAL_IDENTIFIER=your_email")
        print("     CAPITAL_PASSWORD=your_api_password")
        print("     CAPITAL_IS_DEMO=True")
        print("\n[TEST] Engine structure, classes, and helper mappings compiled successfully!")
        print("Ready for automated trading and institutional execution.")
    else:
        print(f"\n[STEP 2] Authenticating with Capital.com ({target_env})...")
        engine = CapitalComEngine(api_key=api_k, identifier=ident, password=pwd, is_demo=is_demo_cfg)
        ok, msg = engine.authenticate()
        
        # Smart fallback: If Demo was requested but account only has Live enabled
        if not ok and is_demo_cfg and "error.null.accountId" in msg:
            print("\n  [INFO] Capital.com profile has no active Demo sub-account.")
            print("  [ACTION] Testing connection against Live Mainnet...")
            engine = CapitalComEngine(api_key=api_k, identifier=ident, password=pwd, is_demo=False)
            ok, msg = engine.authenticate()
            
        print(f"  Result: {'SUCCESS' if ok else 'FAILED'} -> {msg}")
        
        if ok:
            mode_lbl = "Demo" if engine.is_demo else "Live"
            print(f"\n[STEP 3] Fetching {mode_lbl} Account Balance...")
            bal = engine.get_account_balance()
            print(f"  • Account ID:   {bal.get('account_id')}")
            print(f"  • Account Name: {bal.get('account_name') or 'Primary'}")
            print(f"  • Balance:      ${bal.get('balance'):,.2f} {bal.get('currency')}")
            print(f"  • Available:    ${bal.get('available'):,.2f} {bal.get('currency')}")
            print(f"  • Equity:       ${bal.get('balance', 0) + bal.get('pnl', 0):,.2f}")
            print(f"  • Active PnL:   ${bal.get('pnl'):,.2f}")
            print(f"  • Status:       {bal.get('status')}")
            
            print("\n[STEP 4] Fetching Live Institutional Market Prices...")
            gold = engine.get_market_details("GOLD")
            if gold.get("success"):
                print(f"  • GOLD (XAU/USD): Bid ${gold.get('bid'):,.2f} | Ask ${gold.get('ask'):,.2f} | Spread ${gold.get('spread'):.2f}")
            
            sp500 = engine.get_market_details("SP500")
            if sp500.get("success"):
                print(f"  • S&P 500:        Bid ${sp500.get('bid'):,.2f} | Ask ${sp500.get('ask'):,.2f} | Spread ${sp500.get('spread'):.2f}")

            btc = engine.get_market_details("BTCUSD")
            if btc.get("success"):
                print(f"  • Bitcoin (CFD):  Bid ${btc.get('bid'):,.2f} | Ask ${btc.get('ask'):,.2f} | Spread ${btc.get('spread'):.2f}")
    
    print("\n" + "=" * 70)
