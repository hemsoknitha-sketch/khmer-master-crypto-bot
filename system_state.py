# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - SYSTEM STATE & TELEMETRY REGISTRY
=================================================
Breaks circular dependencies between orchestration (bot_thread),
persistence (database), and background task workers.
Thread-safe singleton registry for system-wide execution loops and flags.
"""

import threading
from typing import Optional, Any
import asyncio

_lock = threading.Lock()
_MAIN_BOT_LOOP: Optional[asyncio.AbstractEventLoop] = None
_SYSTEM_METRICS = {
    "total_orders_routed": 0,
    "total_risk_vetoes": 0,
    "is_operational_247": True,
}


def set_main_loop(loop: Optional[asyncio.AbstractEventLoop]) -> None:
    """Sets the active asyncio event loop for the Telegram bot thread."""
    global _MAIN_BOT_LOOP
    with _lock:
        _MAIN_BOT_LOOP = loop


def get_main_loop() -> Optional[asyncio.AbstractEventLoop]:
    """Retrieves the active asyncio event loop safely without upward imports."""
    with _lock:
        return _MAIN_BOT_LOOP


def record_risk_veto() -> None:
    """Atomically records a risk sizer trade veto."""
    with _lock:
        _SYSTEM_METRICS["total_risk_vetoes"] += 1


def get_system_telemetry() -> dict:
    """Returns a snapshot of core operational telemetry."""
    with _lock:
        return dict(_SYSTEM_METRICS)
