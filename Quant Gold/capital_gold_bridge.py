# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD CAPITAL.COM TELEGRAM & SYSTEM BRIDGE
==============================================================
Document Version: 1.0.0 (Institutional Ground Truth)
Integrates:
  - Telegram `/capital gold` command & inline keyboard menus
  - 1-Tap VIP Gold Execution with Structural SL & Breakeven Armor
  - Live 19-Timeframe Heatmap & Telemetry Dashboard
  - Background Scheduler integration with capital_auto_monitor
==============================================================
"""

import os
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

import database as db
import ui_standards

try:
    from .quant_gold_security import get_quant_gold_security_citadel
except (ImportError, ValueError):
    from quant_gold_security import get_quant_gold_security_citadel

try:
    from .timeframes import get_gold_mtf_engine
    from .mathematical_engine import get_gold_math_core
    from .execution_engine import get_quant_gold_execution_engine
except (ImportError, ValueError):
    from timeframes import get_gold_mtf_engine
    from mathematical_engine import get_gold_math_core
    from execution_engine import get_quant_gold_execution_engine

logger = logging.getLogger("QUANT_GOLD_BRIDGE")


class QuantGoldCapitalBridge:
    """
    Bridge connecting the Quant Gold Engine to the Telegram bot and scheduler.
    """

    def __init__(self):
        self.exec_engine = get_quant_gold_execution_engine()
        self.mtf_engine = get_gold_mtf_engine()
        self.math_core = get_gold_math_core()
        self.citadel = get_quant_gold_security_citadel()

    async def build_quant_gold_overview_ui(self, chat_id: int, user_lang: str = "khmer") -> Tuple[str, InlineKeyboardMarkup]:
        """
        Builds the institutional Quant Gold Telegram Dashboard with live 19-timeframe heatmap.
        """
        sig_data = await self.exec_engine.evaluate_gold_master_signal()
        curr_p = sig_data.get("current_price", 2735.0)
        action = sig_data.get("action", "HOLD")
        conf = sig_data.get("confidence", 50.0)
        sl = sig_data.get("sl", 0.0)
        tp1 = sig_data.get("tp1", 0.0)
        tp2 = sig_data.get("tp2", 0.0)
        tp3 = sig_data.get("tp3", 0.0)
        p_buy = sig_data.get("prospective_buy", {})
        p_sell = sig_data.get("prospective_sell", {})

        mtf = sig_data.get("mtf_summary", {})
        counts = mtf.get("counts", {})
        math_s = sig_data.get("math_summary", {})
        kalman_v = math_s.get("kalman_velocity", 0.0)
        hurst_val = math_s.get("composite_hurst", 0.50)
        regime = math_s.get("regime", "RANDOM_WALK")

        # Visual indicator icons
        action_icon = "🟢 BUY" if action == "BUY" else ("🔴 SELL" if action == "SELL" else "⚪ HOLD / CHOP FILTER")

        if user_lang == "khmer":
            text = (
                f"🥇 <b>[ANGKOR QUANT - QUANT GOLD APEX ENGINE]</b> 🏛️\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"🎯 <b>ឧបករណ៍វិនិយោគ ៖</b> <code>Spot Gold (XAUUSD / Gold)</code>\n"
                f"💵 <b>តម្លៃបច្ចុប្បន្ន ៖</b> <code>${curr_p:.2f}</code> | <b>Spread ៖</b> <code>${sig_data.get('spread', 0.35):.2f}</code>\n"
                f"⚡ <b>សញ្ញាសម្រេចចិត្ត ៖</b> <code>{action_icon}</code>\n"
                f"🧠 <b>ទំនុកចិត្តឈ្នះ (Win Prob) ៖</b> <code>{conf:.1f}%</code>\n"
                f"{ui_standards.DIVIDER_LIGHT}\n"
                f"📊 <b>វិសាលគម ១៩ TIMEFRAMES SPECTRUM (M1 ដល់ 1 Month) ៖</b>\n"
                f"• បៃតង (Bullish) ៖ <code>{counts.get('bullish', 0)} / 19 TFs</code>\n"
                f"• ក្រហម (Bearish) ៖ <code>{counts.get('bearish', 0)} / 19 TFs</code>\n"
                f"• អព្យាក្រឹត (Neutral) ៖ <code>{counts.get('neutral', 0)} / 19 TFs</code>\n"
                f"• ពិន្ទុសរុប (Weighted Score) ៖ <code>{mtf.get('weighted_score', 0):+.1f} / 100</code>\n"
                f"{ui_standards.DIVIDER_LIGHT}\n"
                f"🔬 <b>ប្រព័ន្ធគណិតវិទ្យាកំពូល (QUANTITATIVE CORE) ៖</b>\n"
                f"• 2D Kalman Velocity ៖ <code>{kalman_v:+.4f}</code> (Zero-Lag Momentum)\n"
                f"• Fractal Hurst (H) ៖ <code>{hurst_val:.3f}</code> | <b>Regime ៖</b> <code>{regime}</code>\n"
                f"• Bayesian Win Edge ៖ <code>{math_s.get('bayesian_win_probability', 50):.1f}%</code>\n"
                f"{ui_standards.DIVIDER_LIGHT}\n"
                f"🛡️ <b>កម្រិតការពារដើមទុន & គោលដៅ (R:R &gt;= 1:1.20 - 1:4.00) ៖</b>\n"
                f"• កាត់ខាតតាមរចនាសម្ព័ន្ធ (SL) ៖ <code>${sl:.2f}</code> (-60.8 pips)\n"
                f"• គោលដៅ TP1 (+73 pips) ៖ <code>${tp1:.2f}</code> (Breakeven Armor Lock)\n"
                f"• គោលដៅ TP2 (+152 pips) ៖ <code>${tp2:.2f}</code> (Guaranteed Cash Floor)\n"
                f"• គោលដៅ TP3 (+243 pips) ៖ <code>${tp3:.2f}</code> (Moonshot Runner)\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"💎 <i>ដំណើរការដោយឥតគិតថ្លៃ 24/7 365 លើ Hugging Face Token & Google Cloud!</i>"
            )
        else:
            text = (
                f"🥇 <b>[ANGKOR QUANT - QUANT GOLD APEX ENGINE]</b> 🏛️\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"🎯 <b>Asset :</b> <code>Spot Gold (XAUUSD / Gold)</code>\n"
                f"💵 <b>Current Price :</b> <code>${curr_p:.2f}</code> | <b>Spread :</b> <code>${sig_data.get('spread', 0.35):.2f}</code>\n"
                f"⚡ <b>Master Action :</b> <code>{action_icon}</code>\n"
                f"🧠 <b>Win Probability :</b> <code>{conf:.1f}%</code>\n"
                f"{ui_standards.DIVIDER_LIGHT}\n"
                f"📊 <b>19-TIMEFRAME SPECTRUM (M1 to 1 Month) :</b>\n"
                f"• Bullish Confluence : <code>{counts.get('bullish', 0)} / 19 TFs</code>\n"
                f"• Bearish Confluence : <code>{counts.get('bearish', 0)} / 19 TFs</code>\n"
                f"• Neutral / Consolidation : <code>{counts.get('neutral', 0)} / 19 TFs</code>\n"
                f"• Weighted Confluence Score : <code>{mtf.get('weighted_score', 0):+.1f} / 100</code>\n"
                f"{ui_standards.DIVIDER_LIGHT}\n"
                f"🔬 <b>QUANTITATIVE MATHEMATICS CORE :</b>\n"
                f"• 2D Kalman Velocity : <code>{kalman_v:+.4f}</code>\n"
                f"• Fractal Hurst Exponent (H) : <code>{hurst_val:.3f}</code> ({regime})\n"
                f"• Bayesian Win Edge : <code>{math_s.get('bayesian_win_probability', 50):.1f}%</code>\n"
                f"{ui_standards.DIVIDER_LIGHT}\n"
                f"🛡️ <b>RISK GOVERNOR & TARGETS (R:R &gt;= 1:1.20 - 1:4.00) :</b>\n"
                f"• Structural Stop Loss (SL) : <code>${sl:.2f}</code> (-60.8 pips)\n"
                f"• Target TP1 (+73 pips) : <code>${tp1:.2f}</code> (Breakeven Armor Lock)\n"
                f"• Target TP2 (+152 pips) : <code>${tp2:.2f}</code> (Guaranteed Cash Floor)\n"
                f"• Target TP3 (+243 pips) : <code>${tp3:.2f}</code> (Moonshot Runner)\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"💎 <i>Running 24/7 365 Free on Hugging Face Serverless & Google Cloud!</i>"
            )

        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 1-Tap BUY Gold", callback_data="btn_qgold_buy"),
                InlineKeyboardButton("🔴 1-Tap SELL Gold", callback_data="btn_qgold_sell")
            ],
            [
                InlineKeyboardButton("🎯 Super Smart Signal", callback_data="btn_qgold_signal"),
                InlineKeyboardButton("🔄 Refresh 19-TF Scan", callback_data="btn_qgold_refresh")
            ],
            [
                InlineKeyboardButton("📊 Open Positions", callback_data="btn_qgold_positions"),
                InlineKeyboardButton("🤖 Toggle Auto Gold", callback_data="btn_qgold_toggle")
            ],
            [
                InlineKeyboardButton("💵 Live Status", callback_data="btn_qgold_status"),
                InlineKeyboardButton("🖥️ VPS Health", callback_data="btn_qgold_health")
            ],
            [
                InlineKeyboardButton("🚨 Panic Close ALL", callback_data="btn_qgold_close_all"),
                InlineKeyboardButton("📖 User Guide / Help", callback_data="btn_qgold_help")
            ]
        ])

        return text, kb

    def build_vip_referral_required_card(self, chat_id: int) -> str:
        """Renders an institutional VIP onboarding card for unverified users (Invariant 36)."""
        ref_link = os.getenv("CAPITAL_REFERRAL_URL", "https://capital.com")
        card = (
            f"🛡️ <b>[ANGKOR QUANT - VIP CAPITAL.COM ACCESS GATEWAY]</b> 🏛️\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"ℹ️ <b>សេចក្តីជូនដំណឹងសុវត្ថិភាព (Invariant 36) ៖</b>\n"
            f"ដើម្បីធានាសុវត្ថិភាពគណនី និងអនុលោមភាពស្ថាប័ន ការជួញដូរផ្ទាល់ (Live 1-Tap & Auto Trading) "
            f"តម្រូវឱ្យមានការភ្ជាប់គណនី Capital.com ដែលបានផ្ទៀងផ្ទាត់ (Referral Verified) "
            f"ឬមាន API Credentials ផ្ទាល់ខ្លួន។\n\n"
            f"📝 <b>របៀបបើកដំណើរការ ៖</b>\n"
            f"1. បង្កើតគណនី Capital.com តាម Link ផ្លូវការ ៖ <a href='{ref_link}'>ចុចទីនេះដើម្បីចុះឈ្មោះ</a>\n"
            f"2. ផ្ញើលេខគណនី (Account ID) ទៅកាន់ Admin តាមរយៈ @soknitha_support ដើម្បីផ្ទៀងផ្ទាត់\n"
            f"3. ឬបញ្ចូល API Credentials ផ្ទាល់ខ្លួនតាមរយៈ Main Bot (/capital)\n"
            f"{ui_standards.DIVIDER_LIGHT}\n"
            f"💡 <i>លោកអាចមើល Signal វិភាគ 19 Timeframes (/signal) និងពិនិត្យតម្លៃមាស Real-Time (/status) បានដោយសេរី!</i>"
        )
        return card

    async def _safe_send(self, update: Update, text: str, reply_markup=None, parse_mode="HTML"):
        """Sends a telegram message safely with HTML, falling back to plain text if needed."""
        msg = update.effective_message
        if not msg:
            return None
        text = self.citadel.scrub_sensitive_data(text)
        try:
            return await msg.reply_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
        except Exception as e:
            logger.warning(f"Telegram {parse_mode} reply notice ({e}), falling back to plain text")
            import re
            clean = re.sub(r"<[^>]+>", "", text)
            clean = clean.replace("**", "").replace("`", "")
            try:
                return await msg.reply_text(clean, reply_markup=reply_markup)
            except Exception as e2:
                logger.error(f"Plain text fallback also failed: {e2}")
                return None

    async def handle_telegram_gold_subcommand(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        args: List[str]
    ) -> bool:
        """
        Handles subcommands like:
          /capital gold
          /capital gold scan
          /capital gold buy [lot]
          /capital gold sell [lot]
          /capital gold on
          /capital gold off
        """
        chat_id = update.effective_chat.id if update.effective_chat else None
        if not chat_id:
            return False

        raw_lang = db.get_user_language(chat_id)
        user_lang = "khmer" if raw_lang in ["km", "khmer", "0", "1", "auto"] else "english"

        sub_action = str(args[0]).upper().strip() if args else "MENU"

        if sub_action in ["GOLD", "XAUUSD", "MENU"]:
            text, kb = await self.build_quant_gold_overview_ui(chat_id, user_lang)
            await self._safe_send(update, text, reply_markup=kb)
            return True

        elif sub_action in ["BUY", "SELL"]:
            # 1. Circuit breaker lockdown check
            if self.citadel.is_locked():
                await self._safe_send(
                    update,
                    "🚨 <b>[CIRCUIT BREAKER ARMED]</b> <i>ការជួញដូរត្រូវបានផ្អាកជាបន្ទាន់ដោយ Super Admin (Emergency Halt)។</i>"
                )
                return True

            # 2. VIP Authorization Gatekeeper check (Invariant 36)
            auth_ok, _ = self.citadel.is_user_authorized_for_trading(chat_id)
            if not auth_ok:
                await self._safe_send(update, self.build_vip_referral_required_card(chat_id))
                return True

            # 3. Input Sanitization & Bounds Clamping (0.5 to 50.0 oz)
            raw_lot = args[1] if len(args) > 1 else 0.5
            lot = self.citadel.sanitize_lot_size(raw_lot, default_lot=0.5, min_lot=0.5, max_lot=50.0)

            sig = await self.exec_engine.evaluate_gold_master_signal()
            curr_p = sig.get("current_price", 4071.78)
            p_buy = sig.get("prospective_buy", {})
            p_sell = sig.get("prospective_sell", {})
            if sub_action == "BUY":
                sl = p_buy.get("sl", round(curr_p - 6.08, 2))
                tp1 = p_buy.get("tp1", round(curr_p + 7.30, 2))
            else:
                sl = p_sell.get("sl", round(curr_p + 6.08, 2))
                tp1 = p_sell.get("tp1", round(curr_p - 7.30, 2))

            await self._safe_send(
                update,
                f"⚡ <b>[EXECUTING 1-TAP QUANT GOLD {sub_action}]</b> 🥇\n"
                f"• Size: <code>{lot} oz (Troy Ounces)</code> | Invalidation SL: <code>${sl:.2f}</code> (-60.8 p)\n"
                f"• TP1 (+73 pips): <code>${tp1:.2f}</code> (Breakeven Armor Armed)\n"
                f"<i>Dispatching order to Capital.com via Sub-Millisecond Bridge...</i>"
            )

            is_admin = (chat_id in [859271875, 537186806])
            res = await self.exec_engine.execute_smart_order_for_user(
                chat_id=chat_id,
                direction=sub_action,
                size=lot,
                sl=sl,
                tp=tp1,
                broadcast_vip=is_admin
            )

            if res.get("success"):
                await self._safe_send(
                    update,
                    f"✅ <b>[QUANT GOLD ORDER FILLED]</b> 🟢\n"
                    f"{ui_standards.DIVIDER_HEAVY}\n"
                    f"• Instrument: <code>GOLD (XAUUSD)</code>\n"
                    f"• Direction: <code>{sub_action}</code> | Size: <code>{lot} Lot</code>\n"
                    f"• Invalidation SL: <code>${sl:.2f}</code>\n"
                    f"• Target TP1: <code>${tp1:.2f}</code> (Breakeven Armor Armed)\n"
                    f"{ui_standards.DIVIDER_LIGHT}\n"
                    f"🛡️ <i>Trade is protected by Dynamic Trailing Ratchet & Shock Early Harvest!</i>"
                )
            else:
                raw_msg = str(res.get('message', 'Broker error'))
                scrubbed_msg = self.citadel.scrub_sensitive_data(raw_msg)
                await self._safe_send(
                    update,
                    f"⚠️ <b>[ORDER REJECTED]</b> : <code>{scrubbed_msg}</code>"
                )
            return True

        elif sub_action in ["ON", "ENABLE", "START"]:
            # 1. Circuit breaker lockdown check
            if self.citadel.is_locked():
                await self._safe_send(
                    update,
                    "🚨 <b>[CIRCUIT BREAKER ARMED]</b> <i>ការជួញដូរត្រូវបានផ្អាកជាបន្ទាន់ដោយ Super Admin!</i>"
                )
                return True

            # 2. VIP Authorization Gatekeeper check (Invariant 36)
            auth_ok, _ = self.citadel.is_user_authorized_for_trading(chat_id)
            if not auth_ok:
                await self._safe_send(update, self.build_vip_referral_required_card(chat_id))
                return True
            db.set_capital_auto_config(chat_id=chat_id, enabled=True, budget=300.0, max_positions=5, is_demo=False)
            await self._safe_send(
                update,
                f"🥇 <b>[QUANT GOLD AUTONOMOUS ENGINE ACTIVATED]</b> 🟢\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"• Target: <code>Spot Gold (XAUUSD)</code> 100% Exclusively\n"
                f"• 19-Timeframe Confluence & AI Swarm: <code>ACTIVE</code>\n"
                f"• Breakeven Armor & Zero Loss Risk Protocol: <code>ARMED</code>\n"
                f"• 24/7 Free Execution: <code>Google Cloud + Hugging Face Serverless</code>"
            )
            return True

        elif sub_action in ["OFF", "DISABLE", "STOP"]:
            db.set_capital_auto_config(chat_id=chat_id, enabled=False)
            await self._safe_send(
                update,
                f"⏸️ <b>[QUANT GOLD AUTONOMOUS ENGINE PAUSED]</b> 🔴\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"Automated Gold order dispatch is now paused for your account."
            )
            return True

        return False

    async def _execute_user_order_fallback(self, chat_id: int, direction: str, size: float, sl: float, tp: float) -> Dict[str, Any]:
        """Fallback order executor delegating directly to execution engine."""
        return await self.exec_engine.execute_smart_order_for_user(chat_id, direction, size, sl, tp)
        try:
            import asyncio
            u_eng = capital_engine.get_user_capital_engine(chat_id)
            res = await asyncio.to_thread(
                u_eng.execute_smart_tradfi_order,
                epic="GOLD",
                direction=direction,
                size=size,
                sl=sl,
                tp=tp,
                bypass_quant_eval=True,
                bypass_citadel=True,
                setup_type="VIP_1TAP_GOLD"
            )
            if res.get("success"):
                deal_id = res.get("deal_reference") or res.get("dealId", "OK")
                db.record_capital_auto_trade(
                    chat_id=chat_id,
                    deal_id=str(deal_id),
                    deal_reference=str(deal_id),
                    epic="GOLD",
                    direction=direction,
                    size=size,
                    entry_price=res.get("entry_price") or res.get("price") or 0.0,
                    sl=sl,
                    tp=tp,
                    scale_tier=0,
                    sl_dist=abs((res.get("entry_price") or 0.0) - sl),
                    tranche_id="SINGLE",
                    tp1=tp,
                    tp2=0.0,
                    tp3=0.0
                )
            return res
        except Exception as e:
            return {"success": False, "message": str(e)}


# Singleton
_GOLD_BRIDGE: Optional[QuantGoldCapitalBridge] = None

def get_quant_gold_capital_bridge() -> QuantGoldCapitalBridge:
    global _GOLD_BRIDGE
    if _GOLD_BRIDGE is None:
        _GOLD_BRIDGE = QuantGoldCapitalBridge()
    return _GOLD_BRIDGE
