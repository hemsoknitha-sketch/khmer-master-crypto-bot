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


# ==============================================================================
# CAPITAL.COM 360° SKY NET DAILY CAPITAL GOVERNOR & TARGET LOCK (INVARIANT 52)
# ==============================================================================

class CapitalDailyAGIGovernor:
    """
    🏛️ Sky Net 360° Daily Capital Governance Citadel (Invariant 52).
    Enforces Daily Profit Target Lock (+5.0% Daily Win Cap) & Capital Loss Floor (-2.5%).
    
    Axioms:
    1. Daily Baseline Equity Snapshot: Captured at 00:00 UTC / 07:00 ICT daily.
    2. +5.0% Daily Win Cap: When cumulative realized + unrealized gains reach >= +5.0%,
       trading is PUSHED/LOCKED for 24h to prevent overtrading and bank 100% of profits.
    3. -2.5% Daily Capital Loss Floor: If daily drawdown hits -2.5%, entries are locked
       for 12-24h to preserve 97.5% of principal capital.
    4. Anti-Greed & Zero Recklessness: Preemptively exits upon target attainment.
    """

    DAILY_PROFIT_TARGET_PCT = 5.0   # +5% Target Lock (Daily Win Cap)
    DAILY_LOSS_FLOOR_PCT = 2.5      # -2.5% Loss Floor (Capital Shield)

    @classmethod
    def get_today_str(cls) -> str:
        """Returns UTC date string for daily tracking."""
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    @classmethod
    def get_daily_starting_capital(cls, chat_id: int, current_balance: float = 0.0) -> float:
        """
        Retrieves starting equity baseline for today.
        If missing or 0, sets current_balance as today's starting baseline.
        """
        import database as db
        today_str = cls.get_today_str()
        key = f"cap_daily_start_eq_{chat_id}_{today_str}"
        val = db.get_system_setting(key)
        if val:
            try:
                start_eq = float(val)
                if start_eq > 0:
                    return start_eq
            except Exception:
                pass
        
        # Initialize starting equity for today
        if current_balance > 0:
            db.update_system_setting(key, str(round(current_balance, 2)))
            return current_balance
        return 1000.0  # Safe fallback

    @classmethod
    def evaluate_and_check_daily_lock(
        cls,
        chat_id: int,
        current_balance: float,
        app=None,
        is_demo: bool = False
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Evaluates daily capital status against the +5.0% Target Lock & -2.5% Loss Floor.
        Returns: (is_locked: bool, reason: str, telemetry: dict)
        """
        import database as db
        today_str = cls.get_today_str()
        baseline = cls.get_daily_starting_capital(chat_id, current_balance)
        daily_pnl_usd = round(current_balance - baseline, 2)
        daily_pnl_pct = round((daily_pnl_usd / max(1.0, baseline)) * 100.0, 2)

        lock_key = f"cap_daily_lock_{chat_id}_{today_str}"
        existing_lock = db.get_system_setting(lock_key)

        telemetry = {
            "today": today_str,
            "starting_capital": baseline,
            "current_balance": current_balance,
            "daily_pnl_usd": daily_pnl_usd,
            "daily_pnl_pct": daily_pnl_pct,
            "target_pct": cls.DAILY_PROFIT_TARGET_PCT,
            "floor_pct": cls.DAILY_LOSS_FLOOR_PCT,
            "is_target_locked": False,
            "is_loss_locked": False,
            "can_trade": True,
            "status": "NORMAL_TRADING"
        }

        # Check if user has enabled 24/7 Citadel Continuous Mode (Invariant 53)
        # Removes +5% profit freeze to allow 24/7 compounding and widens loss floor to -10% catastrophe floor
        user_auto_cfg = db.get_capital_auto_config(chat_id) if hasattr(db, "get_capital_auto_config") else {}
        is_24_7_continuous = (
            db.get_system_setting(f"cap_24_7_citadel_unlocked_{chat_id}", "0") == "1" or
            db.get_system_setting(f"cap_continuous_trading_{chat_id}", "0") == "1" or
            db.get_system_setting("capital_global_24_7_unlocked", "0") == "1" or
            user_auto_cfg.get("schedule_mode") in ["24/7", "247", "RESET", "ALWAYS_ON"]
        )

        # Check existing locks
        if existing_lock == "TARGET_5PCT_LOCKED":
            if is_24_7_continuous:
                telemetry["can_trade"] = True
                telemetry["status"] = "24_7_CITADEL_COMPOUNDING"
            else:
                telemetry["is_target_locked"] = True
                telemetry["can_trade"] = False
                telemetry["status"] = "TARGET_5PCT_LOCKED"
                reason = f"Daily +5.0% Profit Target LOCKED (+{daily_pnl_pct:.2f}%). Trading paused to bank 100% of profits."
                return True, reason, telemetry

        if existing_lock == "LOSS_FLOOR_LOCKED":
            active_loss_floor = 10.0 if is_24_7_continuous else cls.DAILY_LOSS_FLOOR_PCT
            if is_24_7_continuous and daily_pnl_pct > -active_loss_floor:
                telemetry["can_trade"] = True
                telemetry["status"] = "24_7_CITADEL_COMPOUNDING"
            elif daily_pnl_pct > -active_loss_floor:
                # Self-healing: If current equity is safely above the loss floor (e.g. false trigger from used margin dip),
                # automatically clear the stale lock and permit normal trading!
                db.update_system_setting(lock_key, "NORMAL")
                telemetry["is_loss_locked"] = False
                telemetry["can_trade"] = True
                telemetry["status"] = "NORMAL_TRADING"
            else:
                telemetry["is_loss_locked"] = True
                telemetry["can_trade"] = False
                telemetry["status"] = "LOSS_FLOOR_LOCKED"
                reason = f"Daily -{active_loss_floor:.1f}% Loss Floor ENGAGED ({daily_pnl_pct:.2f}%). Trading paused for capital preservation."
                return True, reason, telemetry

        # 1. Target Lock Trigger (+5.0%)
        if daily_pnl_pct >= cls.DAILY_PROFIT_TARGET_PCT:
            if is_24_7_continuous:
                telemetry["is_target_locked"] = False
                telemetry["can_trade"] = True
                telemetry["status"] = "24_7_CITADEL_COMPOUNDING"
                logger.info(f"💎 [24/7 CITADEL UNLOCKED] Daily Target +{daily_pnl_pct}% hit for User {chat_id}. Compounding 24/7 without halting!")
            else:
                db.update_system_setting(lock_key, "TARGET_5PCT_LOCKED")
                telemetry["is_target_locked"] = True
                telemetry["can_trade"] = False
                telemetry["status"] = "TARGET_5PCT_LOCKED"
                reason = f"Daily +5.0% Target Reached (+{daily_pnl_pct:.2f}% / +${daily_pnl_usd:.2f}). Trading Locked."

                logger.info(f"🏆 [CAPITAL.COM 360° SKY NET] Target hit for user {chat_id}: +{daily_pnl_pct}% (${daily_pnl_usd}). PUSHED & LOCKED.")

            # Send Telegram Victory Alert
            if app and hasattr(app, "bot") and chat_id:
                env_lbl = "DEMO ($10,000)" if is_demo else "LIVE MAINNET"
                msg = (
                    f"🏆 **[360° SKY NET: +5% DAILY TARGET LOCKED]** 👑\n"
                    f"{ui_standards.DIVIDER_HEAVY}\n"
                    f"⚙️ **គណនី ៖** `{env_lbl}`\n"
                    f"💵 **ទុនដើមថ្ងៃ (Baseline) ៖** `${baseline:,.2f}`\n"
                    f"📊 **សមតុល្យបច្ចុប្បន្ន ៖** `${current_balance:,.2f}`\n"
                    f"💰 **ប្រាក់ចំណេញសុទ្ធថ្ងៃនេះ ៖** `+${daily_pnl_usd:,.2f} USD` (`+{daily_pnl_pct:.2f}%`)\n"
                    f"🎯 **ផែនការប្រចាំថ្ងៃ ៖** `+5.0% Target Achieved (សម្រេចបាន ១០០%)`\n"
                    f"🛑 **ចំណាត់ការ AGI ៖** `PUSHED ផ្អាកការបើក Position ថ្មី ២៤ ម៉ោង!`\n"
                    f"🛡️ **វិន័យការពារ ៖** `ចាក់សោរប្រាក់ចំណេញ មិនលោភលន់ និងមិនប្រថុយប្រថានដាច់ខាត!`\n"
                    f"{ui_standards.DIVIDER_HEAVY}\n"
                    f"✨ _ប្រព័ន្ធនឹងដំណើរការឡើងវិញស្វ័យប្រវត្តនៅថ្ងៃស្អែក ឬវាយបញ្ជា_ `` `/capital RESET_DAILY` ``"
                )
                try:
                    asyncio.create_task(app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown"))
                except Exception as e_msg:
                    logger.debug(f"Failed to send target lock message: {e_msg}")

            return True, reason, telemetry

        # 2. Loss Floor Trigger (-2.5% standard vs -10.0% catastrophe in 24/7 Citadel)
        active_loss_floor = 10.0 if is_24_7_continuous else cls.DAILY_LOSS_FLOOR_PCT
        if daily_pnl_pct <= -active_loss_floor:
            db.update_system_setting(lock_key, "LOSS_FLOOR_LOCKED")
            telemetry["is_loss_locked"] = True
            telemetry["can_trade"] = False
            telemetry["status"] = "LOSS_FLOOR_LOCKED"
            reason = f"Daily -{active_loss_floor:.1f}% Loss Floor Hit ({daily_pnl_pct:.2f}% / ${daily_pnl_usd:.2f}). Trading Paused."

            logger.warning(f"🛡️ [CAPITAL.COM 360° SKY NET] Loss Floor hit for user {chat_id}: {daily_pnl_pct}% (${daily_pnl_usd}). PUSHED & LOCKED.")

            # Send Telegram Preservation Alert
            if app and hasattr(app, "bot") and chat_id:
                env_lbl = "DEMO ($10,000)" if is_demo else "LIVE MAINNET"
                msg = (
                    f"🛡️ **[360° SKY NET: CAPITAL PRESERVATION ENGAGED]** 🚨\n"
                    f"{ui_standards.DIVIDER_HEAVY}\n"
                    f"⚙️ **គណនី ៖** `{env_lbl}`\n"
                    f"💵 **ទុនដើមថ្ងៃ (Baseline) ៖** `${baseline:,.2f}`\n"
                    f"📊 **សមតុល្យបច្ចុប្បន្ន ៖** `${current_balance:,.2f}`\n"
                    f"⚠️ **ការខាតបង់ថ្ងៃនេះ ៖** `-${abs(daily_pnl_usd):,.2f} USD` (`{daily_pnl_pct:.2f}%`)\n"
                    f"🛑 **ចំណាត់ការ AGI ៖** `ផ្អាកការបើក Position ថ្មី ១២ ម៉ោង`\n"
                    f"🛡️ **វិន័យការពារ ៖** `ការពារដើមទុន ៩៧.៥% ដែលនៅសល់ មិនឱ្យផុងខ្លួនបន្តិចម្តងៗឡើយ!`\n"
                    f"{ui_standards.DIVIDER_HEAVY}\n"
                    f"✨ _ប្រព័ន្ធនឹងដំណើរការឡើងវិញស្វ័យប្រវត្តនៅថ្ងៃស្អែក ឬវាយបញ្ជា_ `` `/capital RESET_DAILY` ``"
                )
                try:
                    asyncio.create_task(app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown"))
                except Exception as e_msg:
                    logger.debug(f"Failed to send loss floor message: {e_msg}")

            return True, reason, telemetry

        return False, "Normal Trading Allowed", telemetry

    @classmethod
    def reset_daily_governor(cls, chat_id: int, current_balance: Optional[float] = None) -> bool:
        """Resets today's lock and recalibrates baseline equity."""
        import database as db
        today_str = cls.get_today_str()
        lock_key = f"cap_daily_lock_{chat_id}_{today_str}"
        db.update_system_setting(lock_key, "NORMAL")
        if current_balance is not None and current_balance > 0:
            key = f"cap_daily_start_eq_{chat_id}_{today_str}"
            db.update_system_setting(key, str(round(current_balance, 2)))
        logger.info(f"🔄 [CAPITAL GOVERNOR] Reset daily lock for user {chat_id}.")
        return True

    @classmethod
    def set_daily_baseline(cls, chat_id: int, starting_capital: float) -> None:
        """Explicitly sets today's starting capital baseline."""
        import database as db
        today_str = cls.get_today_str()
        key = f"cap_daily_start_eq_{chat_id}_{today_str}"
        db.update_system_setting(key, str(round(starting_capital, 2)))

    @classmethod
    def update_and_check(cls, chat_id: int, current_balance: float) -> Dict[str, Any]:
        """Convenience method checking lock and returning telemetry."""
        is_locked, reason, telemetry = cls.evaluate_and_check_daily_lock(chat_id, current_balance)
        telemetry["is_locked"] = is_locked
        telemetry["reason"] = reason
        if telemetry.get("is_target_locked"):
            telemetry["state"] = "TARGET_LOCKED"
        elif telemetry.get("is_loss_locked"):
            telemetry["state"] = "FLOOR_HIT"
        else:
            telemetry["state"] = "NORMAL"
        return telemetry

    @classmethod
    def get_daily_telemetry(cls, chat_id: int, current_balance: float = 0.0) -> Dict[str, Any]:
        """Returns read-only status for UI dashboards."""
        _, reason, data = cls.evaluate_and_check_daily_lock(chat_id, current_balance, app=None)
        data["reason"] = reason
        return data

    @classmethod
    def get_user_status(cls, chat_id: int, current_balance: float = 0.0) -> Dict[str, Any]:
        """Convenience alias for get_daily_telemetry with state mapping."""
        t = cls.get_daily_telemetry(chat_id, current_balance)
        if t.get("is_target_locked"):
            t["state"] = "TARGET_LOCKED"
        elif t.get("is_loss_locked"):
            t["state"] = "FLOOR_HIT"
        else:
            t["state"] = "NORMAL"
        return t


def is_capital_daily_locked(chat_id: int, current_balance: float = 0.0) -> Tuple[bool, str, Dict[str, Any]]:
    """Helper shortcut for CapitalDailyAGIGovernor.evaluate_and_check_daily_lock."""
    return CapitalDailyAGIGovernor.evaluate_and_check_daily_lock(chat_id, current_balance)


CAPITAL_DAILY_GOVERNOR = CapitalDailyAGIGovernor


def get_capital_daily_governor():
    """Singleton getter for CapitalDailyAGIGovernor."""
    return CapitalDailyAGIGovernor


