"""
Khmer Master Crypto - Economic Calendar Blackout Guard (Pillar 1)
Document Version: 1.0.0 (Institutional Ground Truth)
Authority: Architectural Specification Lock

Protects trading engines against extreme spread blowouts and violent slippage
during Red Folder US High-Impact economic releases (CPI, NFP, FOMC, Core PCE):
- 30-minute Pre-Event Blackout: Freeze new entries (FORCED_WAIT)
- 15-minute Post-Event Blackout: Allow spreads and volatility to normalize
- Instant Telegram Alert to Super Admin & Active VIP Users
"""

import time
import datetime
import logging
import requests
from typing import Dict, Any, Optional, List, Tuple
import ui_standards

logger = logging.getLogger("EconomicCalendarGuard")

_CALENDAR_CACHE: Dict[str, Any] = {}
_CACHE_TTL_SECONDS = 3600.0  # 1 hour TTL
_LAST_ALERT_SENT_TS: float = 0.0
_LAST_ALERTED_EVENT: str = ""

# High-impact USD keywords
RED_FOLDER_KEYWORDS = [
    "CPI", "CONSUMER PRICE", "NON-FARM", "NFP", "FOMC", "FEDERAL FUNDS",
    "INTEREST RATE", "PCE", "UNEMPLOYMENT RATE", "GDP", "POWELL",
    "JACKSON HOLE", "CORE INFLATION"
]

PRE_EVENT_MINUTES = 30.0
POST_EVENT_MINUTES = 15.0


def fetch_usd_economic_events(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Fetches High-Impact USD economic events for the current week.
    Caches results in memory for 1 hour.
    """
    global _CALENDAR_CACHE
    now = time.time()

    if not force_refresh and "events" in _CALENDAR_CACHE:
        cache_time, cached_list = _CALENDAR_CACHE["events"]
        if now - cache_time < _CACHE_TTL_SECONDS:
            return cached_list

    events = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            raw_data = res.json()
            for item in raw_data:
                country = item.get("country", "")
                impact = item.get("impact", "")
                title = item.get("title", "")
                date_str = item.get("date", "")

                if country != "USD":
                    continue

                is_red = (impact in ["High", "Holiday"]) or any(kw in title.upper() for kw in RED_FOLDER_KEYWORDS)
                if not is_red:
                    continue

                try:
                    # ISO format parsing (e.g. 2026-09-24T08:30:00-04:00)
                    dt = datetime.datetime.fromisoformat(date_str)
                    dt_utc = dt.astimezone(datetime.timezone.utc)
                    events.append({
                        "title": title,
                        "impact": impact,
                        "datetime_utc": dt_utc,
                        "timestamp": dt_utc.timestamp(),
                        "date_str": date_str
                    })
                except Exception:
                    continue
    except Exception as e:
        logger.debug(f"Calendar fetch note: {e}")

    _CALENDAR_CACHE["events"] = (now, events)
    return events


def check_red_folder_blackout() -> Dict[str, Any]:
    """
    Evaluates current time against high-impact USD economic events.
    Returns blackout status, phase, event name, and remaining minutes.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_ts = now_utc.timestamp()

    events = fetch_usd_economic_events()
    for ev in events:
        ev_ts = ev["timestamp"]
        diff_sec = ev_ts - now_ts
        diff_min = diff_sec / 60.0

        # Phase 1: Pre-event blackout (30 mins before)
        if 0.0 <= diff_min <= PRE_EVENT_MINUTES:
            return {
                "is_blackout": True,
                "phase": "PRE_EVENT",
                "event_name": ev["title"],
                "minutes_remaining": round(diff_min, 1),
                "event_time_utc": ev["datetime_utc"].strftime("%H:%M UTC"),
                "reason": f"Red Folder Event '{ev['title']}' scheduled in {int(diff_min)}m"
            }

        # Phase 2: Post-event blackout (15 mins after)
        if -POST_EVENT_MINUTES <= diff_min < 0.0:
            since_min = abs(diff_min)
            return {
                "is_blackout": True,
                "phase": "POST_EVENT",
                "event_name": ev["title"],
                "minutes_since": round(since_min, 1),
                "event_time_utc": ev["datetime_utc"].strftime("%H:%M UTC"),
                "reason": f"Red Folder Event '{ev['title']}' released {int(since_min)}m ago (Cooling spread)"
            }

    return {
        "is_blackout": False,
        "phase": "NORMAL",
        "event_name": "",
        "minutes_remaining": 0.0,
        "reason": "Normal trading regime (No Red Folder economic events active)"
    }


async def notify_economic_blackout_if_needed(app, blackout_info: Dict[str, Any]) -> None:
    """
    Sends actionable, reassuring notification to Super Admin and active VIP users
    when a Red Folder economic blackout initiates.
    Throttled to at most once per distinct event.
    """
    global _LAST_ALERT_SENT_TS, _LAST_ALERTED_EVENT

    if not blackout_info.get("is_blackout") or not app or not hasattr(app, "bot"):
        return

    event_name = blackout_info.get("event_name", "Major USD Economic Release")
    now = time.time()

    # Throttling: Alert once per 3 hours or per unique event
    if event_name == _LAST_ALERTED_EVENT and (now - _LAST_ALERT_SENT_TS) < 10800.0:
        return

    _LAST_ALERTED_EVENT = event_name
    _LAST_ALERT_SENT_TS = now

    phase = blackout_info.get("phase", "PRE_EVENT")
    phase_str = "មុនពេលប្រកាស (៣០ នាទី)" if phase == "PRE_EVENT" else "ក្រោយពេលប្រកាស (១៥ នាទី)"

    msg = (
        f"🏛️ **[RED FOLDER ECONOMIC BLACKOUT GUARD ACTIVE]** ⚡\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"⚠️ **ព្រឹត្តិការណ៍សេដ្ឋកិច្ចសំខាន់ ៖** `{event_name}`\n"
        f"⏳ **ដំណាក់កាល ៖** `{phase_str}`\n"
        f"🛑 **ចំណាត់ការ ៖** `ផ្អាកការបើក Trade ថ្មី (FORCED WAIT)`\n"
        f"⏱️ **ច្បាប់ការពារ ៖** ៣០ នាទីមុន និង ១៥ នាទីក្រោយព័ត៌មាន\n"
        f"🛡️ **គោលបំណងការពារ ៖** ទប់ស្កាត់ការកើនឡើង Spread និង Slippage ដ៏គ្រោះថ្នាក់បំផុត!\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"💡 _ប្រព័ន្ធនឹងដំណើរការ Trade ដោយស្វ័យប្រវត្តិតាមធម្មតាភ្លាមៗក្រោយពេលទីផ្សារមានស្ថេរភាពឡើងវិញ!_"
    )

    try:
        # Alert Super Admin (859271875)
        await app.bot.send_message(chat_id=859271875, text=msg, parse_mode="Markdown")
        logger.info(f"🚨 [ECONOMIC GUARD] Sent Red Folder Blackout notification for {event_name}")
    except Exception as e:
        logger.debug(f"Failed to send admin economic guard alert: {e}")

    # Alert active VIP Capital auto users
    try:
        import database as db
        active_users = db.get_active_capital_auto_users()
        for u in active_users:
            uid = u.get("chat_id")
            if uid and uid != 859271875:
                try:
                    await app.bot.send_message(chat_id=uid, text=msg, parse_mode="Markdown")
                except Exception:
                    pass
    except Exception:
        pass
