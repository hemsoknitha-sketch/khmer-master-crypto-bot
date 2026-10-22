# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - EXECUTION SLIPPAGE & TRANSACTION FRICTION AUDITOR
================================================================
Document Version: 1.0.0 (AQ84 Standard)
Author: HEM SINATH | Institutional Quantitative Governance

Calculates empirical slippage metrics from data/capital_execution_audit.csv:
  1. Mean and Median Slippage (Points & Basis Points)
  2. Adverse Selection Drag (% of trades filled worse than expected)
  3. Execution Latency Distribution (P50, P90, P99)
  4. Cost Drag Impact on Net Expectancy E[R]
"""

import os
import sys
import logging
from typing import Dict, Any
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("ExecutionSlippageAudit")


class ExecutionSlippageAuditor:
    """
    Analyzes historical trade executions from the live and demo broker audit logs.
    """

    DEFAULT_LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "capital_execution_audit.csv")

    @classmethod
    def analyze_execution_frictions(cls, log_path: str = DEFAULT_LOG_PATH) -> Dict[str, Any]:
        """
        Parses execution audit ledger and returns statistical distribution of slippage and latency.
        """
        if not os.path.exists(log_path):
            return {
                "total_logged_executions": 0,
                "mean_slippage_bps": 0.0,
                "median_slippage_bps": 0.0,
                "adverse_slippage_ratio": 0.0,
                "p95_latency_ms": 0.0,
                "fill_rate_pct": 100.0,
                "status": "NO_AUDIT_LOG_FOUND"
            }

        try:
            df = pd.read_csv(log_path)
            if df.empty or len(df) == 0:
                return {
                    "total_logged_executions": 0,
                    "mean_slippage_bps": 0.0,
                    "median_slippage_bps": 0.0,
                    "adverse_slippage_ratio": 0.0,
                    "p95_latency_ms": 0.0,
                    "fill_rate_pct": 100.0,
                    "status": "EMPTY_LOG"
                }

            filled = df[df["status"] == "FILLED"]
            total_orders = len(df)
            filled_orders = len(filled)
            fill_rate = (filled_orders / max(1, total_orders)) * 100.0

            if filled_orders == 0:
                return {
                    "total_logged_executions": total_orders,
                    "fill_rate_pct": round(fill_rate, 2),
                    "mean_slippage_bps": 0.0,
                    "status": "NO_FILLED_ORDERS"
                }

            # Slippage in basis points
            slippage_pct = pd.to_numeric(filled["slippage_pct"], errors="coerce").dropna()
            slippage_bps = slippage_pct * 100.0  # 1% = 100 bps

            latency = pd.to_numeric(filled["latency_ms"], errors="coerce").dropna()

            # Adverse slippage: trade executed at worse price than expected
            # For BUY, filled > expected (slippage > 0); for SELL, filled < expected
            adverse_count = len(slippage_bps[slippage_bps > 0])
            adverse_ratio = (adverse_count / max(1, filled_orders)) * 100.0

            return {
                "total_logged_executions": total_orders,
                "filled_orders": filled_orders,
                "fill_rate_pct": round(fill_rate, 2),
                "mean_slippage_bps": round(float(np.mean(slippage_bps)), 2),
                "median_slippage_bps": round(float(np.median(slippage_bps)), 2),
                "std_slippage_bps": round(float(np.std(slippage_bps)), 2),
                "p95_slippage_bps": round(float(np.percentile(slippage_bps, 95)), 2),
                "adverse_slippage_ratio": round(adverse_ratio, 2),
                "mean_latency_ms": round(float(np.mean(latency)), 1),
                "p95_latency_ms": round(float(np.percentile(latency, 95)), 1),
                "status": "VALID_AUDIT"
            }
        except Exception as exc:
            logger.error(f"Error analyzing slippage log: {exc}")
            return {
                "error": str(exc),
                "status": "PARSE_ERROR"
            }
