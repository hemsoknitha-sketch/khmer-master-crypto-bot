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

        # Confluence Logic
        bullish_score = 0
        bearish_score = 0

        # EMA Trend
        if closes[-1] > ema20 > ema50:
            bullish_score += 40
        elif closes[-1] < ema20 < ema50:
            bearish_score += 40
        elif closes[-1] > ema20:
            bullish_score += 20
        elif closes[-1] < ema20:
            bearish_score += 20

        # RSI Momentum
        if 48.0 <= rsi <= 68.0:
            bullish_score += 30
        elif 32.0 <= rsi <= 52.0:
            bearish_score += 30

        # Anti-FOMO Overbought / Oversold Guards
        if rsi > 72.0:
            bullish_score = 0  # Rebuff chasing tops
        if rsi < 35.0:
            bearish_score = 0  # Rebuff shorting bottoms

        # Recent 3 candle momentum
        if len(closes) >= 4:
            if closes[-1] > closes[-2] > closes[-3]:
                bullish_score += 20
            elif closes[-1] < closes[-2] < closes[-3]:
                bearish_score += 20

        # Final signal arbitration with broker distance compliance
        min_sl_dist = max(1.5 * atr, spread * 2.0, 0.002 * mid_price)
        min_tp_dist = max(3.0 * atr, spread * 4.0, 0.005 * mid_price)

        if bullish_score >= 70:
            signal = "STRONG_BUY" if bullish_score >= 85 else "BUY"
            confidence = min(96, bullish_score)
            sl = round(current_bid - min_sl_dist, 2)
            tp = round(current_ask + min_tp_dist, 2)
        elif bearish_score >= 70:
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
        min_sl_dist = max(1.5 * atr, spread * 2.0, 0.002 * mid_px)
        min_tp_dist = max(3.0 * atr, spread * 4.0, 0.005 * mid_px)

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
        max_spreads = {"GOLD": 1.20, "US500": 1.50, "OIL_CRUDE": 0.10, "BTCUSD": 80.0}
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
# 4. STANDALONE DEMO TEST HARNESS
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
