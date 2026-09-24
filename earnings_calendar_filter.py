"""
Khmer Master Crypto - Corporate Earnings Blackout Shield (Pillar 2)
Document Version: 1.0.0 (Institutional Ground Truth)
Authority: Architectural Specification Lock

Protects trading accounts against catastrophic overnight gap risk on US Stock CFDs
(NVDA, TSLA, AAPL, GOOGL, META, MSFT, AMZN) caused by quarterly earnings calls.
- Enforces a 48-Hour Hard Blackout before corporate earnings release.
- Automatically bypasses individual stock setups while maintaining index & commodity trading.
"""

import time
import datetime
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("EarningsCalendarFilter")

# Cache mapping: symbol -> (cached_ts, earnings_datetime)
_EARNINGS_CACHE: Dict[str, Tuple[float, Any]] = {}
_CACHE_TTL_SECONDS = 86400.0  # 24 Hours TTL

EARNINGS_BLACKOUT_HOURS = 48.0

# Supported major US stock symbols on Capital.com
TRACKED_STOCKS = {"NVDA", "TSLA", "AAPL", "GOOGL", "META", "MSFT", "AMZN"}


def get_stock_next_earnings_date(symbol: str) -> Any:
    """
    Fetches the next corporate earnings date for a given stock symbol.
    Cached for 24 hours to eliminate redundant queries.
    """
    global _EARNINGS_CACHE
    now = time.time()
    sym_u = symbol.upper()

    if sym_u in _EARNINGS_CACHE:
        cached_ts, cached_date = _EARNINGS_CACHE[sym_u]
        if now - cached_ts < _CACHE_TTL_SECONDS:
            return cached_date

    earnings_dt = None
    try:
        import yfinance as yf
        t = yf.Ticker(sym_u)
        cal = t.calendar
        if cal and isinstance(cal, dict):
            ed_list = cal.get("Earnings Date")
            if ed_list and isinstance(ed_list, (list, tuple)) and len(ed_list) > 0:
                first_d = ed_list[0]
                if isinstance(first_d, datetime.date):
                    earnings_dt = datetime.datetime.combine(first_d, datetime.time(20, 0, tzinfo=datetime.timezone.utc))
                elif isinstance(first_d, datetime.datetime):
                    earnings_dt = first_d
    except Exception as e:
        logger.debug(f"Earnings lookup note for {symbol}: {e}")

    _EARNINGS_CACHE[sym_u] = (now, earnings_dt)
    return earnings_dt


def is_asset_in_earnings_blackout(epic: str) -> Tuple[bool, str, float]:
    """
    Verifies whether a tradable asset is an individual stock CFD currently within
    the 48-hour pre-earnings danger window.

    Returns:
    (in_blackout: bool, earnings_date_str: str, hours_remaining: float)
    """
    epic_u = epic.upper()

    # Identify if asset matches a tracked US single stock
    matched_sym = None
    for s in TRACKED_STOCKS:
        if s in epic_u:
            matched_sym = s
            break

    if not matched_sym:
        return False, "", 0.0

    earnings_dt = get_stock_next_earnings_date(matched_sym)
    if not earnings_dt:
        return False, "", 0.0

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    if earnings_dt.tzinfo is None:
        earnings_dt = earnings_dt.replace(tzinfo=datetime.timezone.utc)

    diff_sec = (earnings_dt - now_utc).total_seconds()
    diff_hours = diff_sec / 3600.0

    # 48-Hour Hard Shield Window (0 <= diff_hours <= 48.0)
    if 0.0 <= diff_hours <= EARNINGS_BLACKOUT_HOURS:
        ed_str = earnings_dt.strftime("%Y-%m-%d %H:%M UTC")
        logger.warning(
            f"🛡️ [EARNINGS BLACKOUT SHIELD] {matched_sym} blocked from entry! "
            f"Earnings call scheduled in {diff_hours:.1f} hours ({ed_str}). Anti-Gap Guard Active."
        )
        return True, ed_str, round(diff_hours, 1)

    return False, "", 0.0
