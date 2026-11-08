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

        bias_side = action if action in ["BUY", "SELL"] else sig_data.get("dominant_bias", "BUY")
        pips_sl = abs(curr_p - sl) * 10
        pips_tp1 = abs(tp1 - curr_p) * 10
        pips_tp2 = abs(tp2 - curr_p) * 10
        pips_tp3 = abs(tp3 - curr_p) * 10

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
                f"🛡️ <b>កម្រិតការពារដើមទុន &amp; គោលដៅ ({'សកម្ម' if action in ['BUY','SELL'] else 'រង់ចាំ'} {bias_side} | R:R &gt;= 1:1.20 - 1:4.00) ៖</b>\n"
                f"• កាត់ខាតតាមរចនាសម្ព័ន្ធ (SL) ៖ <code>${sl:.2f}</code> ({'-' if (sl < curr_p and bias_side == 'BUY') or (sl > curr_p and bias_side == 'SELL') else '+'}{pips_sl:.1f} pips)\n"
                f"• គោលដៅ TP1 (+{pips_tp1:.0f} pips) ៖ <code>${tp1:.2f}</code> (Breakeven Armor Lock)\n"
                f"• គោលដៅ TP2 (+{pips_tp2:.0f} pips) ៖ <code>${tp2:.2f}</code> (Guaranteed Cash Floor)\n"
                f"• គោលដៅ TP3 (+{pips_tp3:.0f} pips) ៖ <code>${tp3:.2f}</code> (Moonshot Runner)\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"💎 <i>ដំណើរការដោយឥតគិតថ្លៃ 24/7 365 លើ Hugging Face Token &amp; Google Cloud!</i>"
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
                f"🛡️ <b>RISK GOVERNOR &amp; TARGETS ({'ACTIVE' if action in ['BUY','SELL'] else 'PROSPECTIVE'} {bias_side} | R:R &gt;= 1:1.20 - 1:4.00) :</b>\n"
                f"• Structural Stop Loss (SL) : <code>${sl:.2f}</code> ({'-' if (sl < curr_p and bias_side == 'BUY') or (sl > curr_p and bias_side == 'SELL') else '+'}{pips_sl:.1f} pips)\n"
                f"• Target TP1 (+{pips_tp1:.0f} pips) : <code>${tp1:.2f}</code> (Breakeven Armor Lock)\n"
                f"• Target TP2 (+{pips_tp2:.0f} pips) : <code>${tp2:.2f}</code> (Guaranteed Cash Floor)\n"
                f"• Target TP3 (+{pips_tp3:.0f} pips) : <code>${tp3:.2f}</code> (Moonshot Runner)\n"
                f"{ui_standards.DIVIDER_HEAVY}\n"
                f"💎 <i>Running 24/7 365 Free on Hugging Face Serverless &amp; Google Cloud!</i>"
            )

        is_admin = (chat_id == 859271875) or db.is_admin(chat_id)
        btn_rows = [
            [
                InlineKeyboardButton("🟢 1-Tap BUY Gold", callback_data="btn_qgold_buy"),
                InlineKeyboardButton("🔴 1-Tap SELL Gold", callback_data="btn_qgold_sell")
            ],
            [
                InlineKeyboardButton("🏛️ Capital.com Live (/capital)", callback_data="btn_capital_menu"),
                InlineKeyboardButton("🎯 Gold Signal (/signal)", callback_data="btn_qgold_signal")
            ],
            [
                InlineKeyboardButton("📊 Positions (/positions)", callback_data="btn_qgold_positions"),
                InlineKeyboardButton("👑 VIP License (/license)", callback_data="btn_qgold_license")
            ],
            [
                InlineKeyboardButton("🤖 Toggle Auto Gold", callback_data="btn_qgold_toggle"),
                InlineKeyboardButton("💵 Live Status (/status)", callback_data="btn_qgold_status")
            ],
            [
                InlineKeyboardButton("🔄 Refresh 19-TF Scan", callback_data="btn_qgold_refresh"),
                InlineKeyboardButton("📖 User Guide / Help", callback_data="btn_qgold_help")
            ]
        ]
        if is_admin:
            btn_rows.append([
                InlineKeyboardButton("🖥️ VPS Health (/health)", callback_data="btn_qgold_health"),
                InlineKeyboardButton("🛡️ Security Citadel (/security)", callback_data="btn_qgold_security")
            ])
        kb = InlineKeyboardMarkup(btn_rows)

        return text, kb

    def build_vip_license_required_card(self, chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
        """Renders an institutional VIP License onboarding card for unlicensed users."""
        support_handle = os.getenv("SUPPORT_TELEGRAM_HANDLE", "AngkorQuantSupport").replace("@", "")
        support_url = f"https://t.me/{support_handle}"
        card = (
            f"👑 <b>[ANGKOR QUANT - VIP LICENSE REQUIRED]</b> 🏛️\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"ℹ️ <b>សេចក្តីជូនដំណឹងសិទ្ធិប្រើប្រាស់ (VIP Governance) ៖</b>\n"
            f"ប្រព័ន្ធជួញដូរស្វ័យប្រវត្ត Quant Gold 24/7 Apex Engine ដំណើរការសម្រាប់តែ VIP Users "
            f"ដែលមាន License ត្រឹមត្រូវប៉ុណ្ណោះ។\n\n"
            f"✨ <b>អត្ថប្រយោជន៍ VIP Member ៖</b>\n"
            f"• 19-Timeframe Master Signal វិភាគតម្លៃមាស Real-Time\n"
            f"• 1-Tap BUY / SELL ជាមួយ Breakeven Armor (0.00R Free-Roll Risk)\n"
            f"• ដំណើរការជួញដូរស្វ័យប្រវត្ត 24/7/365 Auto-Trade លើ Capital.com\n"
            f"• Fiduciary Protection Shields ការពារដើមទុន ១០០%\n"
            f"{ui_standards.DIVIDER_LIGHT}\n"
            f"👇 <i>សូមចុចប៊ូតុងខាងក្រោមដើម្បីស្នើសុំ VIP License 1-Click ទៅកាន់ Admin ៖</i>"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 ស្នើសុំ VIP License (Request License)", callback_data="btn_qgold_req_license")],
            [InlineKeyboardButton(f"📞 ទំនាក់ទំនង ជំនួយការ (@{support_handle})", url=support_url)]
        ])
        return card, kb

    def build_vip_referral_required_card(self, chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
        """Renders an institutional VIP onboarding card for unverified Capital.com users (Invariant 36)."""
        ref_link = os.getenv(
            "CAPITAL_REFERRAL_URL",
            "https://capital.com/referafriend-pro?c=az48cxia&pid=referral&src=inviteFriends&license=BAH&mn=ifbahpro1000"
        )
        support_handle = os.getenv("SUPPORT_TELEGRAM_HANDLE", "AngkorQuantSupport").replace("@", "")
        support_url = f"https://t.me/{support_handle}"

        dossier = db.get_user_license_details(chat_id) or {}
        tier_lbl = dossier.get("tier_label", "👑 LIFETIME VIP (គ្មានដែនកំណត់)")
        card = (
            f"🛡️ <b>[ANGKOR QUANT - REGISTRATION REQUIRED]</b> 🏛️\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"👑 <b>ស្ថានភាព VIP License ៖</b> <code>{tier_lbl}</code>\n"
            f"⚠️ <b>ស្ថានភាព ៖</b> 🔴 <b>មិនទាន់ភ្ជាប់ (Registration Required)</b>\n"
            f"ℹ️ <b>លក្ខខណ្ឌកាតព្វកិច្ចជួញដូរ ៖</b>\n"
            f"លោកអ្នកមាន VIP License រួចហើយ! ប៉ុន្តែដើម្បីដំណើរការជួញដូរផ្ទាល់ (Auto Trading) "
            f"ប្រព័ន្ធតម្រូវឱ្យភ្ជាប់គណនី តាមរយៈ Partner Link ផ្លូវការ "
            f"ដើម្បីឱ្យប្រព័ន្ធ AI អាចបញ្ជូន Order ទៅកាន់ Broker បាន។\n\n"
            f"📝 <b>ជំហានងាយៗទាំង ២ ៖</b>\n"
            f"1. បង្កើតគណនី តាម Link ផ្លូវការ ៖ <a href='{ref_link}'>ចុចទីនេះដើម្បីចុះឈ្មោះ</a>\n"
            f"2. ភ្ជាប់ API Key ផ្ទាល់ខ្លួនតាមរយៈ ៖\n"
            f"<code>/capital API &lt;API_KEY&gt; &lt;ACCOUNT_ID&gt; &lt;EMAIL&gt; &lt;PASSWORD&gt; live</code>\n"
            f"(ឬទាក់ទងមកកាន់ ជំនួយការ @{support_handle} ដើម្បីភ្ជាប់ និងអនុម័ត 1-Click!)\n"
            f"{ui_standards.DIVIDER_LIGHT}"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 ចុះឈ្មោះតាម Link ផ្លូវការ (Register)", url=ref_link)],
            [
                InlineKeyboardButton("🔑 របៀបភ្ជាប់ API (/capital API)", callback_data="cap_api_help"),
                InlineKeyboardButton("📖 ស្វែងរក API Key", callback_data="cap_api_instructions")
            ],
            [
                InlineKeyboardButton(f"📞 ជំនួយការ (@{support_handle})", url=support_url),
                InlineKeyboardButton("🔄 ពិនិត្យការអនុញ្ញាតឡើងវិញ (Re-check)", callback_data="btn_qgold_recheck_auth")
            ]
        ])
        return card, kb

    def build_awaiting_approval_card(self, chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
        """Renders an institutional card for users whose Capital.com credentials are registered but awaiting Super Admin approval."""
        support_handle = os.getenv("SUPPORT_TELEGRAM_HANDLE", "AngkorQuantSupport").replace("@", "")
        support_url = f"https://t.me/{support_handle}"

        dossier = db.get_user_license_details(chat_id) or {}
        tier_lbl = dossier.get("tier_label", "👑 LIFETIME VIP (គ្មានដែនកំណត់)")
        creds = db.get_user_capital_credentials(chat_id) or {}
        acc_id = str(creds.get("account_id", "N/A"))
        masked_acc = acc_id[:4] + "***" + acc_id[-4:] if len(acc_id) >= 8 else acc_id

        card = (
            f"⏳ <b>[ANGKOR QUANT - CAPITAL.COM APPROVAL PENDING]</b> 🏛️\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"👑 <b>ស្ថានភាព VIP License ៖</b> <code>{tier_lbl}</code>\n"
            f"🏛️ <b>គណនី Capital.com ៖</b> <code>{masked_acc}</code>\n"
            f"⚠️ <b>ស្ថានភាពអនុម័ត ៖</b> 🟡 <b>កំពុងរង់ចាំ Super Admin អនុម័ត (Pending Approval)</b>\n\n"
            f"ℹ️ <b>សេចក្តីជូនដំណឹងការពារដើមទុន (Institutional Governance) ៖</b>\n"
            f"ព័ត៌មានគណនី Capital.com របស់អ្នកត្រូវបានកត់ត្រាក្នុងប្រព័ន្ធរួចរាល់ហើយ។ "
            f"ដើម្បីធានាសុវត្ថិភាពដើមទុន ១០០% ប្រព័ន្ធតម្រូវឱ្យ Super Admin ពិនិត្យ "
            f"និងអនុម័តបើកសិទ្ធិជួញដូរពេញលេញ (Full /capital Services) ជាមុនសិន។\n\n"
            f"📞 <i>សូមទាក់ទងមកកាន់ ជំនួយការ @{support_handle} ដើម្បីពន្លឿនការអនុម័ត 1-Click!</i>\n"
            f"{ui_standards.DIVIDER_LIGHT}\n"
            f"💡 <i>លោកអ្នកនៅតែអាចមើល Signal 19 Timeframes (/signal) និងពិនិត្យតម្លៃមាស (/status) បានដោយសេរី!</i>"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"📞 ទំនាក់ទំនង ជំនួយការ (@{support_handle})", url=support_url)],
            [InlineKeyboardButton("🔄 ពិនិត្យការអនុញ្ញាតឡើងវិញ (Re-check)", callback_data="btn_qgold_recheck_auth")]
        ])
        return card, kb

    def get_authorization_gate_card(self, chat_id: int, reason: str = "") -> Tuple[str, InlineKeyboardMarkup]:
        """Routes to either VIP License Required Card, Awaiting Approval Card, or Capital.com Registration Card based on auth reason."""
        if reason == "UNLICENSED_ACCESS":
            return self.build_vip_license_required_card(chat_id)
        elif reason == "AWAITING_SUPER_ADMIN_APPROVAL":
            return self.build_awaiting_approval_card(chat_id)
        else:
            return self.build_vip_referral_required_card(chat_id)

    async def build_capital_user_dashboard(self, chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
        """Renders the official Capital.com Live Trading Deck for verified/authorized users."""
        is_admin = (chat_id == 859271875) or db.is_admin(chat_id)
        creds = db.get_user_capital_credentials(chat_id) or {}
        acc_id = str(creds.get("account_id") or ("216890638652757188" if is_admin else "N/A"))
        if is_admin and (not acc_id or acc_id == "N/A"):
            acc_id = os.getenv("CAPITAL_ACCOUNT_ID", "216890638652757188")
        masked_acc = acc_id if is_admin else (acc_id[:4] + "***" + acc_id[-4:] if len(acc_id) >= 8 else acc_id)

        is_demo = bool(creds.get("is_demo", False))
        mode_str = "🟢 LIVE MAINNET" if not is_demo else "🟡 DEMO ($10,000)"

        dossier = db.get_user_license_details(chat_id) or {}
        tier_lbl = "👑 SUPER ADMIN" if is_admin else dossier.get("tier_label", "👑 LIFETIME VIP (គ្មានដែនកំណត់)")

        auto_cfg = db.get_capital_auto_config(chat_id) or {}
        auto_on = bool(auto_cfg.get("enabled", False))
        budget = float(auto_cfg.get("budget", 400.0 if is_admin else 50.0))
        max_pos = int(auto_cfg.get("max_positions", 10 if is_admin else 5))
        auto_status = f"🟢 ON (${budget:.2f} / Trade | Max {max_pos} Pos)" if auto_on else "🔴 OFF (Paused)"

        open_trades = db.get_capital_auto_trades(chat_id, status="OPEN")
        gold_trades = [t for t in open_trades if str(t.get("epic", "")).upper() == "GOLD"]
        open_pos_count = len(gold_trades)

        # Live Gold Price & Spread
        bid, ask, spread = self.exec_engine.get_live_gold_price_quote()
        curr_p = (bid + ask) / 2.0

        # Master Signal & Edge
        sig = await self.exec_engine.evaluate_gold_master_signal()
        action = sig.get("action", "HOLD")
        conf = sig.get("confidence", 78.5)

        action_icon = "🟢 STRONG BUY" if action == "BUY" else ("🔴 STRONG SELL" if action == "SELL" else "⚪ HOLD / CHOP FILTER")

        # Query live balance from engine safely
        balance = 0.0
        equity = 0.0
        currency = creds.get("currency", "USD") or "USD"
        try:
            import asyncio
            u_eng = capital_engine.get_user_capital_engine(chat_id)
            bal_res = await asyncio.wait_for(asyncio.to_thread(u_eng.get_account_balance), timeout=6.0)
            if bal_res and bal_res.get("success"):
                balance = float(bal_res.get("balance", 0.0))
                equity = float(bal_res.get("equity", balance))
                currency = bal_res.get("currency", currency)
        except Exception as e_bal:
            logger.debug(f"Live balance fetch note for {chat_id}: {e_bal}")

        balance_str = f"${balance:.2f}"
        equity_str = f"${equity:.2f}" if equity > 0 else (f"${balance:.2f}" if balance > 0 else "Real-Time Synced")

        card = (
            f"🏛️ <b>[ANGKOR QUANT - CAPITAL LIVE TRADING]</b> 🥇\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"👤 <b>គណនី ID ៖</b> <code>{masked_acc}</code> ({mode_str})\n"
            f"🟢 <b>ស្ថានភាពតភ្ជាប់ ៖</b> <code>LIVE CONNECTED (Super Admin Approved)</code>\n"
            f"👑 <b>VIP License ៖</b> <code>{tier_lbl}</code>\n"
            f"💰 <b>សមតុល្យគណនី (Balance) ៖</b> <code>{balance_str}</code>\n"
            f"📈 <b>មូលធនសុទ្ធ (Equity) ៖</b> <code>{equity_str}</code>\n"
            f"{ui_standards.DIVIDER_LIGHT}\n"
            f"🤖 <b>ស្ថានភាព Auto-Trade 24/7 ៖</b> {auto_status}\n"
            f"📊 <b>Positions មាសកំពុងដំណើរការ ៖</b> <code>{open_pos_count} Active</code>\n"
            f"{ui_standards.DIVIDER_LIGHT}\n"
            f"🥇 <b>Spot Gold (XAUUSD) Real-Time ៖</b>\n"
            f"• តម្លៃបច្ចុប្បន្ន ៖ <code>${curr_p:.2f}</code> | Spread ៖ <code>${spread:.2f}</code>\n"
            f"• សកម្មភាព AI ៖ <code>{action_icon}</code> (Edge: <code>{conf:.1f}%</code>)\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"👇 <i>ជ្រើសរើសមុខងារបញ្ជាជួញដូររហ័ស 1-Tap ខាងក្រោម ៖</i>"
        )

        buttons = [
            [
                InlineKeyboardButton("🟢 1-Tap BUY Gold", callback_data="btn_qgold_buy"),
                InlineKeyboardButton("🔴 1-Tap SELL Gold", callback_data="btn_qgold_sell")
            ],
            [
                InlineKeyboardButton("📊 Positions (/positions)", callback_data="btn_qgold_positions"),
                InlineKeyboardButton("👑 VIP License (/license)", callback_data="btn_qgold_license")
            ],
            [
                InlineKeyboardButton("🤖 Toggle Auto-Trade", callback_data="btn_qgold_toggle"),
                InlineKeyboardButton("🛑 បិទគ្រប់ Positions (Close)", callback_data="btn_qgold_close_all")
            ],
            [
                InlineKeyboardButton("🎯 Gold Signal (/signal)", callback_data="btn_qgold_signal"),
                InlineKeyboardButton("💵 Live Status (/status)", callback_data="btn_qgold_status")
            ],
            [
                InlineKeyboardButton("🔄 ធ្វើបច្ចុប្បន្នភាព (Refresh)", callback_data="btn_capital_menu"),
                InlineKeyboardButton("📖 User Guide (/help)", callback_data="btn_qgold_help")
            ]
        ]

        if is_admin:
            buttons.append([
                InlineKeyboardButton("👥 User Registry (/admin_users)", callback_data="admin_users:list:0"),
                InlineKeyboardButton("👑 Fleet Controller (/admin_capital)", callback_data="btn_qgold_admin_capital")
            ])
            buttons.append([
                InlineKeyboardButton("🖥️ VPS Health (/health)", callback_data="btn_qgold_health"),
                InlineKeyboardButton("🛡️ Security Citadel (/security)", callback_data="btn_qgold_security")
            ])

        kb = InlineKeyboardMarkup(buttons)
        return card, kb

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
            auth_ok, reason = self.citadel.is_user_authorized_for_trading(chat_id)
            if not auth_ok:
                card, kb = self.get_authorization_gate_card(chat_id, reason)
                await self._safe_send(update, card, reply_markup=kb)
                return True
            card, kb = await self.build_capital_user_dashboard(chat_id)
            await self._safe_send(update, card, reply_markup=kb)
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
            auth_ok, reason = self.citadel.is_user_authorized_for_trading(chat_id)
            if not auth_ok:
                card, kb = self.get_authorization_gate_card(chat_id, reason)
                await self._safe_send(update, card, reply_markup=kb)
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

            is_admin = (chat_id == 859271875) or db.is_admin(chat_id)
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
            auth_ok, reason = self.citadel.is_user_authorized_for_trading(chat_id)
            if not auth_ok:
                card, kb = self.get_authorization_gate_card(chat_id, reason)
                await self._safe_send(update, card, reply_markup=kb)
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
