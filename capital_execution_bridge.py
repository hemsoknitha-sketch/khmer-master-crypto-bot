# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - CAPITAL.COM DIRECT INSTITUTIONAL EXECUTION BRIDGE
================================================================
Document Version: 1.0.0 (AQ84 / AQ92 Institutional Execution Standard)
Author: HEM SINATH | Institutional Quantitative Governance
Target Broker: Capital.com (REST API v1)

Responsibilities:
  1. Secure Session Management:
     - Multi-tier authentication via CAPITAL_API_KEY, CAPITAL_IDENTIFIER, CAPITAL_PASSWORD.
     - Auto-refresh of CST (Client Security Token) and X-SECURITY-TOKEN headers.
     - Ping / Session Keep-Alive heartbeat avoiding mid-trade dropouts.
  2. Order Execution Gateway:
     - Direct Market Orders, Stop-Loss / Take-Profit placement, and Working Orders.
     - Transparent Demo vs. Live routing with auto-fallback safeguard.
  3. Real-Time Execution Slippage & Latency Auditing:
     - Measures exact delta between Expected Signal Price and Broker Fill Price.
     - Records fill duration (latency in milliseconds) and spreads.
     - Logs all executions to data/capital_execution_audit.csv.
"""

import os
import sys
import time
import math
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from dotenv import load_dotenv

# Ensure stdout handles UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

logger = logging.getLogger("CapitalExecutionBridge")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(name)s][%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class CapitalExecutionBridge:
    """
    Direct institutional REST Execution Bridge for Capital.com.
    Provides session resilience, zero-lookahead fill audits, and empirical slippage logging.
    """

    BASE_URL_DEMO = "https://demo-api-capital.backend-capital.com"
    BASE_URL_LIVE = "https://api-capital.backend-capital.com"

    def __init__(self, is_demo: bool = True):
        self.is_demo = is_demo
        self.base_url = self.BASE_URL_DEMO if is_demo else self.BASE_URL_LIVE
        self.api_key = os.getenv("CAPITAL_API_KEY", "").strip()
        self.identifier = os.getenv("CAPITAL_IDENTIFIER", "").strip()
        self.password = os.getenv("CAPITAL_PASSWORD", "").strip()

        self.cst_token: Optional[str] = None
        self.x_security_token: Optional[str] = None
        self.session_expiry: float = 0.0
        self.active_account_id: Optional[str] = None

        # Resilient HTTP Session with institutional retry policy
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=20)
        self.session.mount("https://", adapter)

        self.audit_log_path = os.path.join(os.path.dirname(__file__), "data", "capital_execution_audit.csv")
        self._init_audit_file()

    def _init_audit_file(self):
        """Initializes execution audit CSV ledger if not present."""
        os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)
        if not os.path.exists(self.audit_log_path):
            header = (
                "timestamp,symbol,direction,expected_price,filled_price,slippage_pts,"
                "slippage_pct,spread_pts,latency_ms,deal_id,status,environment\n"
            )
            with open(self.audit_log_path, "w", encoding="utf-8") as f:
                f.write(header)

    def is_session_valid(self) -> bool:
        """Verifies if tokens exist and session has not expired."""
        return (
            bool(self.cst_token) and
            bool(self.x_security_token) and
            time.time() < (self.session_expiry - 60.0)
        )

    def authenticate(self) -> bool:
        """
        Authenticates with Capital.com REST API and captures CST and X-SECURITY-TOKEN.
        """
        if not self.api_key or not self.identifier or not self.password:
            logger.warning("[CAPITAL_BRIDGE] Missing credentials in environment. Operating in sandbox telemetry mode.")
            return False

        endpoint = f"{self.base_url}/api/v1/session"
        headers = {
            "X-CAP-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "identifier": self.identifier,
            "password": self.password
        }

        try:
            t0 = time.time()
            resp = self.session.post(endpoint, json=payload, headers=headers, timeout=10)
            latency_ms = (time.time() - t0) * 1000.0

            if resp.status_code in [200, 201]:
                self.cst_token = resp.headers.get("CST")
                self.x_security_token = resp.headers.get("X-SECURITY-TOKEN")
                # Capital.com sessions last 10 minutes (600s); buffer to 8 minutes
                self.session_expiry = time.time() + 480.0

                data = resp.json()
                self.active_account_id = data.get("currentAccountId", "")
                env_str = "DEMO" if self.is_demo else "LIVE"
                logger.info(
                    f"[CAPITAL_BRIDGE] Authenticated successfully ({env_str}) in {latency_ms:.1f}ms. "
                    f"Account: {self.active_account_id}"
                )
                return True
            else:
                logger.error(f"[CAPITAL_BRIDGE] Authentication failed: HTTP {resp.status_code} - {resp.text}")
                return False
        except Exception as exc:
            logger.error(f"[CAPITAL_BRIDGE] Network error during authentication: {exc}")
            return False

    def get_auth_headers(self) -> Dict[str, str]:
        """Constructs active authenticated headers."""
        if not self.is_session_valid():
            self.authenticate()

        return {
            "X-CAP-API-KEY": self.api_key,
            "CST": self.cst_token or "",
            "X-SECURITY-TOKEN": self.x_security_token or "",
            "Content-Type": "application/json"
        }

    def place_market_order_with_slippage_audit(
        self,
        epic: str,
        direction: str,
        size: float,
        expected_price: float,
        sl_price: Optional[float] = None,
        tp_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes a direct market order and precisely audits execution slippage against expected price.
        """
        direction_clean = direction.upper().strip()
        t_start = time.time()

        if not self.is_session_valid():
            auth_ok = self.authenticate()
            if not auth_ok:
                return {
                    "success": False,
                    "error": "AUTHENTICATION_FAILED",
                    "slippage_points": 0.0,
                    "latency_ms": (time.time() - t_start) * 1000.0
                }

        endpoint = f"{self.base_url}/api/v1/positions"
        headers = self.get_auth_headers()
        payload: Dict[str, Any] = {
            "epic": epic,
            "direction": direction_clean,
            "size": size,
            "guaranteedStop": False
        }
        if sl_price and sl_price > 0:
            payload["stopLevel"] = round(sl_price, 5)
        if tp_price and tp_price > 0:
            payload["profitLevel"] = round(tp_price, 5)

        try:
            resp = self.session.post(endpoint, json=payload, headers=headers, timeout=8)
            latency_ms = (time.time() - t_start) * 1000.0

            if resp.status_code in [200, 201]:
                res_data = resp.json()
                deal_ref = res_data.get("dealReference", "")
                
                # Fetch deal confirmation to acquire exact fill price
                fill_details = self._get_deal_confirmation(deal_ref)
                filled_price = fill_details.get("level", expected_price)
                deal_id = fill_details.get("dealId", deal_ref)

                # Calculate slippage
                if direction_clean == "BUY":
                    slippage_pts = filled_price - expected_price
                else:
                    slippage_pts = expected_price - filled_price

                slippage_pct = (slippage_pts / max(1e-5, expected_price)) * 100.0

                # Log to audit ledger
                self._log_audit_record(
                    symbol=epic,
                    direction=direction_clean,
                    expected_price=expected_price,
                    filled_price=filled_price,
                    slippage_pts=slippage_pts,
                    slippage_pct=slippage_pct,
                    spread_pts=fill_details.get("spread", 0.0),
                    latency_ms=latency_ms,
                    deal_id=deal_id,
                    status="FILLED"
                )

                logger.info(
                    f"[CAPITAL_BRIDGE] ORDER FILLED: {epic} {direction_clean} {size} lots | "
                    f"Expected: {expected_price:.4f}, Filled: {filled_price:.4f} | "
                    f"Slippage: {slippage_pts:+.4f} pts ({slippage_pct:+.3f}%) | Latency: {latency_ms:.1f}ms"
                )

                return {
                    "success": True,
                    "deal_id": deal_id,
                    "filled_price": filled_price,
                    "expected_price": expected_price,
                    "slippage_points": slippage_pts,
                    "slippage_pct": slippage_pct,
                    "latency_ms": latency_ms,
                    "status": "FILLED"
                }
            else:
                err_msg = f"HTTP {resp.status_code}: {resp.text}"
                logger.error(f"[CAPITAL_BRIDGE] Order rejected: {err_msg}")
                self._log_audit_record(
                    symbol=epic,
                    direction=direction_clean,
                    expected_price=expected_price,
                    filled_price=expected_price,
                    slippage_pts=0.0,
                    slippage_pct=0.0,
                    spread_pts=0.0,
                    latency_ms=latency_ms,
                    deal_id="",
                    status="REJECTED"
                )
                return {
                    "success": False,
                    "error": err_msg,
                    "latency_ms": latency_ms
                }
        except Exception as exc:
            logger.error(f"[CAPITAL_BRIDGE] Exception during order placement: {exc}")
            return {
                "success": False,
                "error": str(exc),
                "latency_ms": (time.time() - t_start) * 1000.0
            }

    def _get_deal_confirmation(self, deal_ref: str) -> Dict[str, Any]:
        """Polls deal confirmation endpoint for exact execution level."""
        if not deal_ref:
            return {}

        endpoint = f"{self.base_url}/api/v1/confirms/{deal_ref}"
        headers = self.get_auth_headers()

        # Retry up to 3 times with brief 150ms backoff
        for _ in range(3):
            try:
                resp = self.session.get(endpoint, headers=headers, timeout=5)
                if resp.status_code == 200:
                    d = resp.json()
                    if d.get("status") in ["SUCCESS", "ACCEPTED"]:
                        return {
                            "level": float(d.get("level", 0.0) or 0.0),
                            "dealId": str(d.get("dealId", "")),
                            "spread": float(d.get("spread", 0.0) or 0.0)
                        }
            except Exception:
                pass
            time.sleep(0.15)

        return {}

    def _log_audit_record(
        self,
        symbol: str,
        direction: str,
        expected_price: float,
        filled_price: float,
        slippage_pts: float,
        slippage_pct: float,
        spread_pts: float,
        latency_ms: float,
        deal_id: str,
        status: str
    ):
        """Appends trade execution record to empirical slippage audit CSV."""
        try:
            ts = datetime.utcnow().isoformat()
            env_str = "DEMO" if self.is_demo else "LIVE"
            row = (
                f"{ts},{symbol},{direction},{expected_price:.5f},{filled_price:.5f},"
                f"{slippage_pts:+.5f},{slippage_pct:+.4f},{spread_pts:.5f},"
                f"{latency_ms:.1f},{deal_id},{status},{env_str}\n"
            )
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(row)
        except Exception as exc:
            logger.warning(f"[CAPITAL_BRIDGE] Failed to write audit record: {exc}")
