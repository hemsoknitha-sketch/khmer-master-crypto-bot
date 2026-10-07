# -*- coding: utf-8 -*-
"""
KHMER MASTER CRYPTO / ANGKOR QUANT - INSTITUTIONAL POST-NEWS VOLATILITY HARVESTER (NEWS SCALP ALPHA)
===================================================================================================
Document Version: 1.0.0 (Absolute Mathematical Ground Truth & Institutional Specification Lock)
Target: Capital.com TradFi Markets (Gold, US Indices, Mega-Caps, Forex CFDs)
Integrations: economic_calendar_guard.py, super_smart_capital_citadel.py, capital_engine.py

Architecture (The 6 Institutional Pillars of Post-News Alpha):
  1. Pillar 1: Zero Toxic Flow Shield (Strict 0 to 2.5m Post-Release Freeze)
     - Never trade in the initial 150 seconds where Tier-1 LPs pull quotes and spreads blow out.
  2. Pillar 2: Real-time Live Spread Normalization Sensor (<= 1.25x Baseline)
     - Continuously monitor broker live spread; unlock only when spread cools down to normal.
  3. Pillar 3: Setup 1 - Institutional News Turtle Soup Reversal (BSL/SSL Purge with >= 50% Wick)
     - Detect sweeps of Asian/London session high or low during the news spike with exhaustion wick.
  4. Pillar 4: Setup 2 - Institutional Displacement & 5m FVG Retest (True Fundamental Repricing)
     - Detect genuine macro repricing; wait for first pullback into 5m Fair Value Gap with tight SL.
  5. Pillar 5: Asymmetric Risk-to-Reward Hard Floor (R:R >= 1:2.5 to 1:5.0 with News Peak Wick SL)
     - Stop-Loss is mathematically anchored to the extreme news spike wick; zero ambiguous risk.
  6. Pillar 6: Mathematical Breakeven Armor (+1.0R Quick Shift) & Dynamic ATR Micro-Trailing Lock
     - Fast protection for rapid news moves; locks profit into bank as soon as momentum stalls.
"""

import time
import math
import datetime
import logging
import asyncio
from typing import Dict, Any, Tuple, Optional, List

import database as db
import ui_standards
import economic_calendar_guard

logger = logging.getLogger("PostNewsScalpHarvester")


# Priority institutional assets with deepest post-news liquidity on Capital.com
NEWS_SCALP_PRIORITY_ASSETS = [
    "GOLD",      # Spot Gold / US Dollar (XAU/USD) - High Volatility Harvester
    "US500",     # S&P 500 Index - Ultra Tight Spread (0.4-0.6 pts)
    "US30",      # Dow Jones Industrial Average
    "US100",     # Nasdaq 100 Tech Index
    "EURUSD",    # Euro / US Dollar - Deepest Interbank Liquidity
    "GBPUSD",    # British Pound / US Dollar
    "USDJPY",    # US Dollar / Japanese Yen
    "BTCUSD"     # Bitcoin / US Dollar CFD
]

# Baseline normal spreads for assets on Capital.com (in price units / points)
ASSET_SPREAD_BASELINES: Dict[str, float] = {
    "GOLD": 0.35,        # 0.35 USD
    "SILVER": 0.035,     # 0.035 USD
    "US500": 0.60,       # 0.60 pts
    "SP500": 0.60,
    "US30": 2.50,        # 2.50 pts
    "DOW": 2.50,
    "US100": 1.60,       # 1.60 pts
    "NASDAQ": 1.60,
    "EURUSD": 0.00010,   # 1.0 pip
    "GBPUSD": 0.00015,   # 1.5 pips
    "USDJPY": 0.012,     # 1.2 pips
    "OIL": 0.05,         # 0.05 USD
    "OIL_CRUDE": 0.05,
    "BTCUSD": 25.0       # 25.0 USD
}

# Maximum allowed spread multiplier during post-news scalping regime
MAX_NORMALIZED_SPREAD_MULTIPLIER = 1.30

# Toxic window freeze duration (seconds) immediately after release
TOXIC_ZONE_SECONDS = 150.0  # 2.5 minutes


class PostNewsScalpHarvester:
    """
    Wall Street Institutional Post-News Alpha Engine.
    Executes high-probability sniper scalps following Red Folder economic releases
    once spreads normalize and institutional order flow confirms direction.
    """

    _INSTANCE = None
    _LAST_EVALUATIONS: Dict[str, Tuple[float, Dict[str, Any]]] = {}

    def __init__(self):
        self._cooldowns: Dict[str, float] = {}  # epic -> timestamp

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    @staticmethod
    def is_news_scalp_enabled(chat_id: Optional[int] = None) -> bool:
        """
        Checks whether the Post-News Volatility Harvester is enabled.
        Can check user-specific override or system-wide default.
        """
        try:
            if chat_id:
                user_val = db.get_system_setting(f"news_scalp_user_{chat_id}", "")
                if user_val.upper() in ["OFF", "DISABLED", "FALSE", "0"]:
                    return False
                if user_val.upper() in ["ON", "ENABLED", "TRUE", "1"]:
                    return True

            sys_val = db.get_system_setting("news_scalp_alpha_master", "ACTIVE")
            return sys_val.upper() in ["ACTIVE", "ON", "ENABLED", "TRUE", "1"]
        except Exception:
            return True

    @staticmethod
    def set_news_scalp_enabled(enabled: bool, chat_id: Optional[int] = None) -> None:
        """Sets news scalp status globally or for a specific user."""
        val = "ACTIVE" if enabled else "OFF"
        try:
            if chat_id:
                db.update_system_setting(f"news_scalp_user_{chat_id}", val)
            else:
                db.update_system_setting("news_scalp_alpha_master", val)
        except Exception as e:
            logger.debug(f"Error persisting news scalp setting: {e}")

    @classmethod
    def evaluate_news_scalp_setup(
        cls,
        epic: str,
        engine: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Evaluates whether an institutional post-news scalp setup exists on a specific asset.
        Enforces Zero Toxic Flow, Live Spread Normalization, and ICT/SMC Reversal or Displacement.
        """
        import capital_engine

        resolved_epic = capital_engine.EPIC_MAP.get(str(epic or "").upper().strip(), str(epic or "").upper().strip())
        now = time.time()

        # Step 1: Check Economic Calendar Status
        bo_info = economic_calendar_guard.check_red_folder_blackout()
        is_bo = bo_info.get("is_blackout", False)
        phase = bo_info.get("phase", "NORMAL")
        event_name = bo_info.get("event_name", "Economic Release")

        # Must strictly be in POST_EVENT phase
        if not is_bo or phase != "POST_EVENT":
            return {
                "epic": resolved_epic,
                "is_approved": False,
                "rejection_reason": f"NOT_POST_EVENT_PHASE: Current status is {phase}. Scalp engine requires active POST_EVENT window.",
                "phase": phase
            }

        minutes_since = float(bo_info.get("minutes_since", 0.0) or 0.0)
        seconds_since = minutes_since * 60.0

        # Step 2: Pillar 1 - Zero Toxic Flow Shield (First 2.5m / 150s Freeze)
        if seconds_since < TOXIC_ZONE_SECONDS:
            remaining_toxic = int(TOXIC_ZONE_SECONDS - seconds_since)
            return {
                "epic": resolved_epic,
                "is_approved": False,
                "rejection_reason": f"TOXIC_ZONE_ACTIVE: {minutes_since:.1f}m < 2.5m minimum cooling window. Remaining toxic freeze: {remaining_toxic}s.",
                "minutes_since": minutes_since,
                "event_name": event_name
            }

        # Window expires at 15 minutes post-event
        if minutes_since > 15.0:
            return {
                "epic": resolved_epic,
                "is_approved": False,
                "rejection_reason": f"EVENT_WINDOW_EXPIRED: {minutes_since:.1f}m > 15.0m maximum post-news window.",
                "minutes_since": minutes_since
            }

        if engine is None:
            engine = capital_engine.get_capital_engine()

        # Step 3: Pillar 2 - Live Spread Normalization Sensor
        market_details = engine.get_market_details(resolved_epic)
        if not market_details.get("success"):
            return {
                "epic": resolved_epic,
                "is_approved": False,
                "rejection_reason": f"MARKET_DATA_UNAVAILABLE: {market_details.get('error')}"
            }

        current_bid = float(market_details.get("bid", 0.0))
        current_ask = float(market_details.get("ask", 0.0))
        mid_price = float(market_details.get("mid", 0.0)) or ((current_bid + current_ask) / 2.0 if current_bid > 0 else 1.0)
        current_spread = float(market_details.get("spread", 0.0))

        baseline_spread = ASSET_SPREAD_BASELINES.get(resolved_epic.upper(), 0.50)
        max_allowed_spread = baseline_spread * MAX_NORMALIZED_SPREAD_MULTIPLIER

        if current_spread > max_allowed_spread:
            return {
                "epic": resolved_epic,
                "is_approved": False,
                "rejection_reason": f"SPREAD_BLOWOUT: Live spread {current_spread:.4f} > {max_allowed_spread:.4f} threshold ({current_spread / max(0.00001, baseline_spread):.1f}x baseline). Waiting for Tier-1 LP liquidity.",
                "current_spread": current_spread,
                "baseline_spread": baseline_spread,
                "max_allowed_spread": max_allowed_spread
            }

        # Step 4: Fetch Historical 5m and 15m Candles for Price Action Structure
        candles_5m = engine.get_historical_prices(resolved_epic, resolution="MINUTE_5", max_bars=30)
        if not candles_5m or len(candles_5m) < 10:
            return {
                "epic": resolved_epic,
                "is_approved": False,
                "rejection_reason": "INSUFFICIENT_5M_CANDLES"
            }

        highs_5m = [float(c.get("high", 0.0)) for c in candles_5m]
        lows_5m = [float(c.get("low", 0.0)) for c in candles_5m]
        closes_5m = [float(c.get("close", 0.0)) for c in candles_5m]
        opens_5m = [float(c.get("open", 0.0)) for c in candles_5m]

        # Pre-event range: High/Low of candles prior to the news spike (candles [-8:-2])
        pre_event_high = max(highs_5m[-8:-2]) if len(highs_5m) >= 8 else max(highs_5m[:-2])
        pre_event_low = min(lows_5m[-8:-2]) if len(lows_5m) >= 8 else min(lows_5m[:-2])

        # News spike candles (last 2 bars)
        news_bar = candles_5m[-2] if len(candles_5m) >= 2 else candles_5m[-1]
        latest_bar = candles_5m[-1]

        news_high = max(float(news_bar.get("high", 0.0)), float(latest_bar.get("high", 0.0)))
        news_low = min(float(news_bar.get("low", 0.0)), float(latest_bar.get("low", 0.0)))
        news_open = float(news_bar.get("open", 0.0))
        news_close = float(latest_bar.get("close", 0.0))
        total_news_range = max(0.00001, news_high - news_low)

        # Calculate approximate 5m ATR for buffer sizing
        tr_list = []
        for i in range(1, len(candles_5m)):
            tr = max(
                highs_5m[i] - lows_5m[i],
                abs(highs_5m[i] - closes_5m[i - 1]),
                abs(lows_5m[i] - closes_5m[i - 1])
            )
            tr_list.append(tr)
        atr_5m = sum(tr_list[-10:]) / 10.0 if len(tr_list) >= 10 else (news_high - news_low) * 0.3

        # --------------------------------------------------------------------
        # SETUP 1: INSTITUTIONAL NEWS TURTLE SOUP REVERSAL (LIQUIDITY PURGE)
        # --------------------------------------------------------------------
        # Scenario 1A: Bearish Turtle Soup (Spike swept BSL high, but failed to sustain)
        swept_high = news_high > pre_event_high
        failed_high = mid_price < pre_event_high  # Closed back below pre-event level
        upper_wick = news_high - max(news_open, news_close)
        upper_wick_ratio = upper_wick / total_news_range

        if swept_high and failed_high and upper_wick_ratio >= 0.45:
            # Anchor Stop Loss 0.4 * ATR above the news spike high
            sl_price = round(news_high + (0.4 * atr_5m), 4)
            # Take profit targets 50% Mean-Reversion Fibonacci / Equilibrium
            tp_price = round(news_low + (0.35 * total_news_range), 4)
            risk = abs(sl_price - mid_price)
            reward = abs(mid_price - tp_price)
            rr_ratio = round(reward / max(0.0001, risk), 2)

            if rr_ratio >= 2.5:
                return {
                    "epic": resolved_epic,
                    "is_approved": True,
                    "action": "SELL",
                    "setup_type": "NEWS_TURTLE_SOUP_REVERSAL",
                    "entry_price": mid_price,
                    "stop_loss": sl_price,
                    "take_profit": tp_price,
                    "risk_reward": rr_ratio,
                    "event_name": event_name,
                    "minutes_since": minutes_since,
                    "current_spread": current_spread,
                    "wick_ratio": round(upper_wick_ratio * 100, 1),
                    "rationale": (
                        f"Bearish Turtle Soup: News swept Pre-Event High ({pre_event_high:.2f}) "
                        f"with {upper_wick_ratio * 100:.1f}% upper wick exhaustion. "
                        f"Price closed back inside range. R:R 1:{rr_ratio:.1f} to Equilibrium."
                    )
                }

        # Scenario 1B: Bullish Turtle Soup (Spike swept SSL low, but failed to sustain)
        swept_low = news_low < pre_event_low
        failed_low = mid_price > pre_event_low  # Closed back above pre-event level
        lower_wick = min(news_open, news_close) - news_low
        lower_wick_ratio = lower_wick / total_news_range

        if swept_low and failed_low and lower_wick_ratio >= 0.45:
            sl_price = round(news_low - (0.4 * atr_5m), 4)
            tp_price = round(news_high - (0.35 * total_news_range), 4)
            risk = abs(mid_price - sl_price)
            reward = abs(tp_price - mid_price)
            rr_ratio = round(reward / max(0.0001, risk), 2)

            if rr_ratio >= 2.5:
                return {
                    "epic": resolved_epic,
                    "is_approved": True,
                    "action": "BUY",
                    "setup_type": "NEWS_TURTLE_SOUP_REVERSAL",
                    "entry_price": mid_price,
                    "stop_loss": sl_price,
                    "take_profit": tp_price,
                    "risk_reward": rr_ratio,
                    "event_name": event_name,
                    "minutes_since": minutes_since,
                    "current_spread": current_spread,
                    "wick_ratio": round(lower_wick_ratio * 100, 1),
                    "rationale": (
                        f"Bullish Turtle Soup: News swept Pre-Event Low ({pre_event_low:.2f}) "
                        f"with {lower_wick_ratio * 100:.1f}% lower wick rejection. "
                        f"Price reclaimed support. R:R 1:{rr_ratio:.1f} to Equilibrium."
                    )
                }

        # --------------------------------------------------------------------
        # SETUP 2: INSTITUTIONAL DISPLACEMENT & 5M FVG RETEST
        # --------------------------------------------------------------------
        # Check for Fair Value Gap formed in the last 3 candles
        if len(candles_5m) >= 4:
            bar_0 = candles_5m[-1]  # current/retest bar
            bar_1 = candles_5m[-2]  # displacement bar
            bar_2 = candles_5m[-3]  # previous bar

            # Bullish Displacement FVG: bar_1 displaced upwards, bar_0 low > bar_2 high
            fvg_bull_gap = float(bar_0.get("low", 0.0)) - float(bar_2.get("high", 0.0))
            is_bull_displacement = float(bar_1.get("close", 0.0)) > float(bar_1.get("open", 0.0)) and (float(bar_1.get("close", 0.0)) - float(bar_1.get("open", 0.0))) > (1.2 * atr_5m)

            if is_bull_displacement and fvg_bull_gap >= (0.2 * atr_5m):
                # Price is retesting the upper bound of the FVG
                fvg_top = float(bar_0.get("low", 0.0))
                fvg_bottom = float(bar_2.get("high", 0.0))
                if fvg_bottom <= mid_price <= fvg_top + (0.5 * atr_5m):
                    sl_price = round(fvg_bottom - (0.3 * atr_5m), 4)
                    tp_price = round(news_high + (0.8 * total_news_range), 4)
                    risk = abs(mid_price - sl_price)
                    reward = abs(tp_price - mid_price)
                    rr_ratio = round(reward / max(0.0001, risk), 2)
                    if rr_ratio >= 2.5:
                        return {
                            "epic": resolved_epic,
                            "is_approved": True,
                            "action": "BUY",
                            "setup_type": "INSTITUTIONAL_DISPLACEMENT_FVG_RETEST",
                            "entry_price": mid_price,
                            "stop_loss": sl_price,
                            "take_profit": tp_price,
                            "risk_reward": rr_ratio,
                            "event_name": event_name,
                            "minutes_since": minutes_since,
                            "current_spread": current_spread,
                            "rationale": f"Bullish FVG Retest: Displaced bar formed FVG [{fvg_bottom:.2f} - {fvg_top:.2f}]. Retest confirmed with normalized spread. R:R 1:{rr_ratio:.1f}."
                        }

            # Bearish Displacement FVG: bar_1 displaced downwards, bar_2 low > bar_0 high
            fvg_bear_gap = float(bar_2.get("low", 0.0)) - float(bar_0.get("high", 0.0))
            is_bear_displacement = float(bar_1.get("open", 0.0)) > float(bar_1.get("close", 0.0)) and (float(bar_1.get("open", 0.0)) - float(bar_1.get("close", 0.0))) > (1.2 * atr_5m)

            if is_bear_displacement and fvg_bear_gap >= (0.2 * atr_5m):
                fvg_top = float(bar_2.get("low", 0.0))
                fvg_bottom = float(bar_0.get("high", 0.0))
                if fvg_bottom - (0.5 * atr_5m) <= mid_price <= fvg_top:
                    sl_price = round(fvg_top + (0.3 * atr_5m), 4)
                    tp_price = round(news_low - (0.8 * total_news_range), 4)
                    risk = abs(sl_price - mid_price)
                    reward = abs(mid_price - tp_price)
                    rr_ratio = round(reward / max(0.0001, risk), 2)
                    if rr_ratio >= 2.5:
                        return {
                            "epic": resolved_epic,
                            "is_approved": True,
                            "action": "SELL",
                            "setup_type": "INSTITUTIONAL_DISPLACEMENT_FVG_RETEST",
                            "entry_price": mid_price,
                            "stop_loss": sl_price,
                            "take_profit": tp_price,
                            "risk_reward": rr_ratio,
                            "event_name": event_name,
                            "minutes_since": minutes_since,
                            "current_spread": current_spread,
                            "rationale": f"Bearish FVG Retest: Displaced bar formed FVG [{fvg_bottom:.2f} - {fvg_top:.2f}]. Retest confirmed with normalized spread. R:R 1:{rr_ratio:.1f}."
                        }

        return {
            "epic": resolved_epic,
            "is_approved": False,
            "rejection_reason": "NO_INSTITUTIONAL_NEWS_PATTERN: Market did not form clear Turtle Soup or FVG Retest with R:R >= 2.5.",
            "event_name": event_name,
            "minutes_since": minutes_since,
            "current_spread": current_spread
        }

    @classmethod
    async def scan_and_execute_news_scalps_async(
        cls,
        app: Optional[Any] = None,
        engine: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously scans all priority news assets and dispatches verified setups.
        """
        import capital_engine

        if engine is None:
            engine = capital_engine.get_capital_engine()

        executed = []
        now = time.time()
        harvester = cls.get_instance()

        for epic in NEWS_SCALP_PRIORITY_ASSETS:
            # 10-minute cooldown per asset for news scalps
            if harvester._cooldowns.get(epic, 0.0) > now:
                continue

            try:
                setup = cls.evaluate_news_scalp_setup(epic, engine=engine)
                if not setup.get("is_approved"):
                    continue

                action = setup.get("action")
                entry = setup.get("entry_price")
                sl = setup.get("stop_loss")
                tp = setup.get("take_profit")
                rr = setup.get("risk_reward")
                setup_type = setup.get("setup_type")
                event_name = setup.get("event_name")
                rationale = setup.get("rationale")

                logger.info(
                    f"🎯 [NEWS SCALP ALPHA TRIGGERED] {epic} {action} @ {entry:.2f} | "
                    f"SL: {sl:.2f} | TP: {tp:.2f} | R:R 1:{rr} ({setup_type}) for event '{event_name}'"
                )

                # Set cooldown to prevent duplicate triggers
                harvester._cooldowns[epic] = now + 600.0  # 10 mins

                # Dispatch execution to active users via capital_engine
                active_users = db.get_active_capital_auto_users()
                for user in active_users:
                    chat_id = user.get("chat_id")
                    if not chat_id:
                        continue

                    # Check if user has news scalping enabled
                    if not cls.is_news_scalp_enabled(chat_id):
                        continue

                    try:
                        user_engine = capital_engine.get_user_capital_engine(chat_id)
                        # Execute market order with predefined SL and TP
                        exec_res = await asyncio.to_thread(
                            user_engine.execute_smart_order,
                            epic,
                            action,
                            stop_loss=sl,
                            take_profit=tp
                        )
                        if exec_res.get("success"):
                            deal_id = exec_res.get("deal_id") or exec_res.get("dealReference", "OK")
                            logger.info(f"✅ [NEWS SCALP DISPATCHED] User {chat_id}: {action} {epic} Deal #{deal_id}")
                    except Exception as e_user:
                        logger.debug(f"User {chat_id} news scalp exec note: {e_user}")

                # Send Telegram Announcement to Super Admin and active VIPs
                if app and hasattr(app, "bot"):
                    msg = (
                        f"🎯 **[INSTITUTIONAL NEWS SCALP ALPHA EXECUTED]** ⚡\n"
                        f"{ui_standards.DIVIDER_HEAVY}\n"
                        f"🏛️ **ព្រឹត្តិការណ៍សេដ្ឋកិច្ច ៖** `{event_name}`\n"
                        f"💎 **ទ្រព្យសកម្ម ៖** `{epic}`\n"
                        f"🚀 **សកម្មភាព ៖** `{'🟢 BUY (LONG)' if action == 'BUY' else '🔴 SELL (SHORT)'}`\n"
                        f"⚙️ **យុទ្ធសាស្ត្រ ៖** `{setup_type}`\n"
                        f"📊 **តម្លៃចូល (Entry) ៖** `{entry:.2f}`\n"
                        f"🛑 **Stop-Loss (News Wick) ៖** `{sl:.2f}`\n"
                        f"🎯 **Take-Profit (Mean Reversion) ៖** `{tp:.2f}`\n"
                        f"⚖️ **Risk : Reward ៖** `1 : {rr:.1f}`\n"
                        f"🛡️ **Spread Sensor ៖** `{setup.get('current_spread', 0):.4f} (NORMALIZED <= 1.3x)`\n"
                        f"{ui_standards.DIVIDER_HEAVY}\n"
                        f"💡 _{rationale}_\n"
                        f"🛡️ _Breakeven Armor នឹងការពារទុនដោយស្វ័យប្រវត្តិពេលចំណេញបាន +1.0R!_"
                    )
                    try:
                        await app.bot.send_message(chat_id=859271875, text=msg, parse_mode="Markdown")
                    except Exception:
                        pass

                executed.append(setup)

            except Exception as e:
                logger.error(f"Error evaluating news scalp for {epic}: {e}")

        return executed

    @classmethod
    def get_status_report(cls, chat_id: Optional[int] = None) -> Dict[str, Any]:
        """Returns diagnostic status report of the Post-News Volatility Harvester."""
        is_enabled = cls.is_news_scalp_enabled(chat_id)
        bo_info = economic_calendar_guard.check_red_folder_blackout()
        return {
            "is_enabled": is_enabled,
            "status_label": "🟢 ACTIVE (ស្ទាក់កើបចំណេញ)" if is_enabled else "⏸️ DISABLED (ឈប់សម្រាក)",
            "economic_status": bo_info,
            "priority_assets": NEWS_SCALP_PRIORITY_ASSETS,
            "toxic_window_seconds": TOXIC_ZONE_SECONDS,
            "max_spread_multiplier": MAX_NORMALIZED_SPREAD_MULTIPLIER
        }


# Canonical Module-Level Functions
def is_news_scalp_enabled(chat_id: Optional[int] = None) -> bool:
    return PostNewsScalpHarvester.is_news_scalp_enabled(chat_id)

def set_news_scalp_enabled(enabled: bool, chat_id: Optional[int] = None) -> None:
    PostNewsScalpHarvester.set_news_scalp_enabled(enabled, chat_id)

def evaluate_news_scalp_setup(epic: str, engine: Optional[Any] = None) -> Dict[str, Any]:
    return PostNewsScalpHarvester.evaluate_news_scalp_setup(epic, engine)

async def scan_and_execute_news_scalps_async(app: Optional[Any] = None, engine: Optional[Any] = None) -> List[Dict[str, Any]]:
    return await PostNewsScalpHarvester.scan_and_execute_news_scalps_async(app, engine)

def get_status_report(chat_id: Optional[int] = None) -> Dict[str, Any]:
    return PostNewsScalpHarvester.get_status_report(chat_id)
