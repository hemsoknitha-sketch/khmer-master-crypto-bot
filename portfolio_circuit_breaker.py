"""
Khmer Master Crypto - Global Portfolio Drawdown Circuit Breaker & Correlation Clamping (Pillar 5)
Document Version: 1.0.0 (Institutional Ground Truth)
Authority: Architectural Specification Lock

Protects entire account capital from catastrophic multi-asset Black Swan contagion:
1. Hard Daily Loss Ceiling (-2.5%): If cumulative realized losses across all engines
   in the last rolling 24 hours reach -2.5%, the system automatically engages an
   in-process Circuit Breaker, locking new position entries for 12 hours.
2. Cross-Asset Correlation Clamping: Prevents over-leveraging on correlated risk factors
   (e.g., Long US100 + Long BTC + Long NVDA). Automatically scales down size by 50%
   when holding highly correlated (> 0.85 beta) assets.
3. Automated Telegram Alert to Super Admin & Active VIP Users upon activation.
"""

import time
import datetime
import sqlite3
import logging
from typing import Dict, Any, Tuple, List, Optional
import ui_standards

logger = logging.getLogger("PortfolioCircuitBreaker")

# Hardcoded Risk Invariants
MAX_DAILY_DRAWDOWN_PCT = 2.5       # -2.5% maximum daily loss
LOCK_DURATION_SECONDS = 43200.0    # 12 Hours Lock
HIGH_BETA_GROUPS = [
    {"US100", "NASDAQ", "BTC", "BTCUSDT", "NVDA", "TSLA", "META", "GOOGL"}, # Risk-On Tech & Crypto
    {"OIL", "OIL_CRUDE", "GAS", "NATURALGAS"}                               # Energy Commodities
]

_CIRCUIT_BREAKER_LOCKED_UNTIL: float = 0.0
_LAST_ALERT_SENT_TS: float = 0.0


def calculate_rolling_24h_drawdown(capital_baseline: float = 10000.0) -> Dict[str, Any]:
    """
    Computes total realized PnL across all closed trades in the rolling 24 hours.
    Queries both crypto trade_history and TradFi capital_auto_trades in bot_database.db.
    """
    total_realized_pnl = 0.0
    cutoff_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)
    cutoff_str = cutoff_dt.strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect("bot_database.db", timeout=5.0)
        cursor = conn.cursor()

        # 1. Crypto closed trades
        try:
            cursor.execute(
                "SELECT SUM(pnl) FROM trade_history WHERE exit_time >= ?",
                (cutoff_str,)
            )
            crypto_sum = cursor.fetchone()[0]
            if crypto_sum is not None:
                total_realized_pnl += float(crypto_sum)
        except Exception:
            pass

        # 2. Capital.com closed trades
        try:
            cursor.execute(
                "SELECT SUM(pnl) FROM capital_auto_trades WHERE closed_at >= ? AND status = 'CLOSED'",
                (cutoff_str,)
            )
            cap_sum = cursor.fetchone()[0]
            if cap_sum is not None:
                total_realized_pnl += float(cap_sum)
        except Exception:
            pass

        conn.close()
    except Exception as e:
        logger.debug(f"Drawdown calculation DB query note: {e}")

    # Determine percentage loss relative to capital baseline
    loss_pct = round((total_realized_pnl / max(100.0, capital_baseline)) * 100.0, 2)
    is_tripped = (loss_pct <= -MAX_DAILY_DRAWDOWN_PCT)

    return {
        "total_pnl_usd": round(total_realized_pnl, 2),
        "loss_pct": loss_pct,
        "is_tripped": is_tripped,
        "capital_baseline": capital_baseline
    }


def is_portfolio_circuit_breaker_active() -> Tuple[bool, str, float]:
    """
    Verifies if the Global Portfolio Circuit Breaker is actively locking new entries.
    Returns (is_active: bool, reason: str, remaining_seconds: float).
    """
    global _CIRCUIT_BREAKER_LOCKED_UNTIL
    now = time.time()

    if _CIRCUIT_BREAKER_LOCKED_UNTIL > now:
        rem_sec = _CIRCUIT_BREAKER_LOCKED_UNTIL - now
        rem_hrs = rem_sec / 3600.0
        reason = f"Global 2.5% Daily Loss Circuit Breaker ACTIVE ({rem_hrs:.1f}h remaining). Anti-Tilt Protection."
        return True, reason, round(rem_sec, 0)

    return False, "Circuit Breaker Normal (No Drawdown Lock)", 0.0


async def check_and_enforce_portfolio_circuit_breaker(app=None, capital_baseline: float = 10000.0) -> bool:
    """
    Evaluates rolling 24h PnL. If loss exceeds -2.5%, activates the 12-hour lock
    and sends urgent Telegram alert to Super Admin and active VIP users.
    Returns True if breaker tripped or active.
    """
    global _CIRCUIT_BREAKER_LOCKED_UNTIL, _LAST_ALERT_SENT_TS
    now = time.time()

    is_active, _, rem_s = is_portfolio_circuit_breaker_active()
    if is_active:
        return True

    res = calculate_rolling_24h_drawdown(capital_baseline=capital_baseline)
    if res.get("is_tripped"):
        _CIRCUIT_BREAKER_LOCKED_UNTIL = now + LOCK_DURATION_SECONDS
        loss_val = res.get("loss_pct", 0.0)
        pnl_usd = res.get("total_pnl_usd", 0.0)

        logger.critical(
            f"🚨 [PORTFOLIO CIRCUIT BREAKER TRIPPED] 24h Drawdown: {loss_val}% (${pnl_usd}). "
            f"Locking all new entries for 12 hours (Anti-Compounding Tilt Guard)."
        )

        # Send Telegram Alert if app provided
        if app and hasattr(app, "bot") and (now - _LAST_ALERT_SENT_TS > 3600.0):
            _LAST_ALERT_SENT_TS = now
            msg = (
                f"🚨 **[PORTFOLIO CIRCUIT BREAKER ENGAGED]** 🛡️\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"⚠️ **ការខាតបង់ ២៤ ម៉ោង ៖** `{loss_val}%` (`${pnl_usd:,.2f}`)\n"
                f"🛑 **ចំណាត់ការ ៖** `ផ្អាកការបើក Position ថ្មីគ្រប់ម៉ាស៊ីន (Lock ១២ ម៉ោង)`\n"
                f"⏱️ **រយៈពេលដោះសោ ៖** ១២ ម៉ោងក្រោយ\n"
                f"🛡️ **គោលបំណងការពារ ៖** បញ្ឈប់ការខាតបង់បន្តបន្ទាប់ (Anti-Compounding Tilt Guard)\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"💡 _ប្រព័ន្ធនឹងត្រួតពិនិត្យ និងបើកដំណើរការឡើងវិញដោយស្វ័យប្រវត្តិតាមវិន័យគណិតវិទ្យា!_"
            )
            try:
                await app.bot.send_message(chat_id=859271875, text=msg, parse_mode="Markdown")
            except Exception:
                pass

            try:
                import database as db
                for u in db.get_active_capital_auto_users():
                    uid = u.get("chat_id")
                    if uid and uid != 859271875:
                        try:
                            await app.bot.send_message(chat_id=uid, text=msg, parse_mode="Markdown")
                        except Exception:
                            pass
            except Exception:
                pass

        return True

    return False


def apply_cross_asset_correlation_clamp(proposed_epic: str, base_size: float, open_epics: List[str]) -> Tuple[float, str]:
    """
    Clamps proposed lot size by 50% if the account already holds an asset
    in the same high-beta correlation group (> 0.85 correlation).
    """
    prop_u = proposed_epic.upper()
    existing_u = [e.upper() for e in open_epics]

    for grp in HIGH_BETA_GROUPS:
        # Check if proposed asset belongs to group
        is_in_grp = any(x in prop_u for x in grp)
        if not is_in_grp:
            continue

        # Check if user already holds another asset in the same group
        for held in existing_u:
            if any(x in held for x in grp) and not any(x in held and x in prop_u for x in grp):
                clamped = round(base_size * 0.50, 4)
                clamped = max(0.01, clamped)
                reason = f"Correlation Clamp Active (Holding {held}). Size clamped 50% ({base_size} -> {clamped}) to eliminate beta contagion."
                logger.info(f"🛡️ [CORRELATION CLAMP] {prop_u}: {reason}")
                return clamped, reason

    return base_size, "Normal sizing (No systemic correlation overlap)"
