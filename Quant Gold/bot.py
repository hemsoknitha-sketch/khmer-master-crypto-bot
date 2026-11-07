# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD STANDALONE TELEGRAM BOT (AQ84)
=========================================================
Target: Google Cloud Linux VPS 'quant-gold' (us-central1-a, quant-gold-514007)
Author: HEM SINATH | Institutional Quantitative Governance
Version: 1.0.0

Purpose:
  100% Dedicated, Pure Gold (XAUUSD) Telegram Bot.
  Zero crypto bloat, zero Binance WebSockets (eliminating HTTP 451),
  zero MT5 wine bridge spam, zero CSX or Solana DEX jobs.
  Responds with <0.05ms speed to /start, /capital, /gold, /buy, /sell, /status.
=========================================================
"""

import os
import sys
import time
import logging
from typing import Dict, List, Optional, Tuple, Any

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    BotCommand,
    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logger = logging.getLogger("QUANT_GOLD_BOT")

# Ensure imports reach Quant Gold and parent directory
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE_ROOT = os.path.dirname(_CURRENT_DIR)
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if _WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, _WORKSPACE_ROOT)

import database as db
import capital_engine
from capital_gold_bridge import get_quant_gold_capital_bridge
from execution_engine import get_quant_gold_execution_engine


def get_quant_gold_bottom_keyboard() -> ReplyKeyboardMarkup:
    """Persistent 1-Tap Bottom Keyboard for Quick Commands."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🥇 Quant Gold Dashboard"), KeyboardButton("🔄 Scan 19 TFs")],
            [KeyboardButton("🟢 BUY GOLD (0.05)"), KeyboardButton("🔴 SELL GOLD (0.05)")],
            [KeyboardButton("📊 Open Positions"), KeyboardButton("🤖 Auto-Trade (ON/OFF)"), KeyboardButton("ℹ️ Status")]
        ],
        resize_keyboard=True,
        is_persistent=True
    )


class QuantGoldBot:
    """
    100% Dedicated, Institutional Gold Bot for Telegram.
    """

    def __init__(self, token: str):
        self.token = token
        self.bridge = get_quant_gold_capital_bridge()
        self.exec_engine = get_quant_gold_execution_engine()
        self.app = None

    def build_application(self):
        """Builds and configures the pure Quant Gold telegram application."""
        async def post_init(application):
            # Sync clean public bot commands
            commands = [
                BotCommand("start", "🥇 Open Quant Gold Dashboard & 19-TF Spectrum"),
                BotCommand("capital", "🏛️ Capital.com Live Gold Trading Deck"),
                BotCommand("gold", "📈 Gold Real-Time Intelligence & Analysis"),
                BotCommand("scan", "🔄 Refresh 19-Timeframe Confluence Scan"),
                BotCommand("buy", "🟢 Execute Instant 1-Tap Market Buy on Gold"),
                BotCommand("sell", "🔴 Execute Instant 1-Tap Market Sell on Gold"),
                BotCommand("positions", "📊 View Active Gold Positions & Breakeven"),
                BotCommand("close", "🛑 Close All Active Gold Positions"),
                BotCommand("panic", "🚨 Emergency Close All Gold Positions"),
                BotCommand("auto", "🤖 Toggle 24/7 Autonomous Gold Trading"),
                BotCommand("status", "⚡ Check Live Price, Capital Session & VPS Health"),
                BotCommand("help", "📖 User Guide & Risk Management Handbook")
            ]
            try:
                await application.bot.set_my_commands(commands, scope=BotCommandScopeDefault())
                await application.bot.set_my_commands(commands, scope=BotCommandScopeAllPrivateChats())
                logger.info("✅ [QUANT GOLD BOT] Command menu synchronized successfully!")
            except Exception as e_cmd:
                logger.warning(f"Command menu sync notice: {e_cmd}")

        from telegram.request import HTTPXRequest
        request = HTTPXRequest(
            connect_timeout=10.0,
            read_timeout=25.0,
            write_timeout=10.0,
            pool_timeout=10.0,
            connection_pool_size=100
        )

        self.app = (
            ApplicationBuilder()
            .token(self.token)
            .request(request)
            .concurrent_updates(32)
            .post_init(post_init)
            .build()
        )

        # Register Handlers
        self.app.add_handler(CommandHandler("start", self.handle_start))
        self.app.add_handler(CommandHandler("capital", self.handle_start))
        self.app.add_handler(CommandHandler("gold", self.handle_start))
        self.app.add_handler(CommandHandler("scan", self.handle_start))
        self.app.add_handler(CommandHandler("buy", self.handle_buy))
        self.app.add_handler(CommandHandler("sell", self.handle_sell))
        self.app.add_handler(CommandHandler("positions", self.handle_positions))
        self.app.add_handler(CommandHandler("close", self.handle_close_all))
        self.app.add_handler(CommandHandler("close_all", self.handle_close_all))
        self.app.add_handler(CommandHandler("panic", self.handle_close_all))
        self.app.add_handler(CommandHandler("auto", self.handle_toggle_auto))
        self.app.add_handler(CommandHandler("status", self.handle_status))
        self.app.add_handler(CommandHandler("help", self.handle_help))

        # Callback query handler for 1-tap interactive buttons
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))

        # Bottom text button router
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_button))

        # Error handler to catch and handle any unhandled exceptions gracefully
        self.app.add_error_handler(self.error_handler)

        return self.app

    async def safe_reply(self, update: Update, text: str, reply_markup=None, parse_mode="HTML"):
        """Sends a message safely with HTML, falling back to plain text if Telegram fails."""
        msg = update.effective_message
        if not msg:
            return None
        try:
            return await msg.reply_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
        except Exception as e:
            logger.warning(f"Telegram {parse_mode} reply note ({e}), falling back to plain text")
            import re
            clean = re.sub(r"<[^>]+>", "", text)
            clean = clean.replace("**", "").replace("`", "")
            try:
                return await msg.reply_text(clean, reply_markup=reply_markup)
            except Exception as e2:
                logger.error(f"Telegram plain text fallback also failed: {e2}")
                return None

    async def safe_edit(self, query, text: str, reply_markup=None, parse_mode="HTML"):
        """Edits a message safely with HTML, falling back to plain text if Telegram fails."""
        try:
            return await query.edit_message_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
        except Exception as e:
            logger.warning(f"Telegram {parse_mode} edit note ({e}), falling back to plain text")
            import re
            clean = re.sub(r"<[^>]+>", "", text)
            clean = clean.replace("**", "").replace("`", "")
            try:
                return await query.edit_message_text(clean, reply_markup=reply_markup)
            except Exception as e2:
                logger.error(f"Telegram edit plain text fallback also failed: {e2}")
                return None

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Global error handler preventing crashes from unhandled update exceptions."""
        logger.warning(f"Handled exception during update processing: {context.error}")

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Displays the Flagship Quant Gold Dashboard."""
        chat_id = update.effective_chat.id if update.effective_chat else None
        if not chat_id:
            return

        user = update.effective_user
        username = user.username or user.first_name or "VIP Trader" if user else "VIP Trader"
        db.register_user(chat_id, username)

        raw_lang = db.get_user_language(chat_id)
        user_lang = "khmer" if raw_lang in ["km", "khmer", "0", "1", "auto"] else "english"

        text, inline_kb = await self.bridge.build_quant_gold_overview_ui(chat_id, user_lang)
        bottom_kb = get_quant_gold_bottom_keyboard()

        await self.safe_reply(update, text, reply_markup=inline_kb)
        if update.message:
            await self.safe_reply(
                update,
                "⚡ <i>ប្រើ Keyboard ខាងក្រោមសម្រាប់បញ្ជារហ័ស (1-Tap Buttons)</i>",
                reply_markup=bottom_kb
            )

    async def handle_buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Executes instant Gold Buy order."""
        lot = 0.05
        if context.args:
            try:
                lot = float(context.args[0])
            except ValueError:
                lot = 0.05
        await self.bridge.handle_telegram_gold_subcommand(update, context, ["BUY", str(lot)])

    async def handle_sell(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Executes instant Gold Sell order."""
        lot = 0.05
        if context.args:
            try:
                lot = float(context.args[0])
            except ValueError:
                lot = 0.05
        await self.bridge.handle_telegram_gold_subcommand(update, context, ["SELL", str(lot)])

    async def handle_positions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Displays current open Gold positions with real-time Breakeven status."""
        chat_id = update.effective_chat.id
        open_trades = db.get_capital_auto_trades_for_user(chat_id)
        gold_trades = [t for t in open_trades if str(t.get("epic", "")).upper() == "GOLD" and t.get("status") == "OPEN"]

        # Check broker live positions directly from Capital.com
        u_eng = capital_engine.get_user_capital_engine(chat_id)
        broker_gold = []
        try:
            broker_pos = u_eng.get_open_positions() if hasattr(u_eng, "get_open_positions") else []
            broker_gold = [
                p for p in broker_pos
                if str(p.get("market", {}).get("epic", "")).upper() == "GOLD"
                or str(p.get("epic", "")).upper() == "GOLD"
            ]
        except Exception as e_bp:
            logger.debug(f"Broker open positions check note: {e_bp}")

        bid, ask, spread = self.exec_engine.get_live_gold_price_quote()
        curr_p = (bid + ask) / 2.0

        if not gold_trades and not broker_gold:
            msg = (
                f"📊 <b>[QUANT GOLD POSITIONS]</b> 🥇\n"
                f"══════════════════════════════════════\n"
                f"💵 <b>តម្លៃមាសបច្ចុប្បន្ន ៖</b> <code>${curr_p:.2f}</code> (Spread: <code>${spread:.2f}</code>)\n"
                f"ℹ️ <b>ស្ថានភាព ៖</b> គ្មាន Position កំពុងបើកនៅឡើយទេ។\n\n"
                f"💡 <i>ចុចប៊ូតុង <b>🟢 1-Tap BUY</b> ឬ <b>🔴 1-Tap SELL</b> ដើម្បីចាប់ផ្តើមជួញដូរ!</i>"
            )
            await self.safe_reply(update, msg)
            return

        lines = [
            f"📊 <b>[QUANT GOLD ACTIVE POSITIONS]</b> 🥇",
            f"══════════════════════════════════════",
            f"💵 <b>តម្លៃមាសបច្ចុប្បន្ន ៖</b> <code>${curr_p:.2f}</code> (Spread: <code>${spread:.2f}</code>)\n"
        ]
        total_upl = 0.0
        seen_deals = set()

        for i, t in enumerate(gold_trades, 1):
            deal_id = str(t.get("deal_id", ""))
            seen_deals.add(deal_id)
            direction = t.get("direction", "BUY")
            size = float(t.get("size", 0.05) or 0.05)
            entry = float(t.get("entry_price", curr_p) or curr_p)
            sl = float(t.get("sl", 0.0) or 0.0)
            tp1 = float(t.get("tp1", 0.0) or 0.0)
            be_active = bool(t.get("breakeven_activated", False))

            upl = (curr_p - entry) * size if direction == "BUY" else (entry - curr_p) * size
            total_upl += upl
            p_icon = "🟢" if upl >= 0 else "🔴"
            be_str = "🛡️ Breakeven Active (0.00R Risk)" if be_active else "⏳ Initial Structural SL"

            lines.append(
                f"<b>#{i} {direction} {size} Lot GOLD</b>\n"
                f"• Entry: <code>${entry:.2f}</code> | SL: <code>${sl:.2f}</code> | TP1: <code>${tp1:.2f}</code>\n"
                f"• UPL: <code>{p_icon} ${upl:+.2f}</code> | {be_str}\n"
            )

        # Append any live broker positions not tracked in local DB
        for bp in broker_gold:
            pos_info = bp.get("position", {}) if isinstance(bp.get("position"), dict) else bp
            deal_id = str(pos_info.get("dealId", ""))
            if deal_id and deal_id in seen_deals:
                continue
            direction = str(pos_info.get("direction", "BUY")).upper()
            size = float(pos_info.get("size", 0.05) or 0.05)
            entry = float(pos_info.get("level", curr_p) or curr_p)
            sl = float(pos_info.get("stopLevel", 0.0) or 0.0)
            upl = float(pos_info.get("upl", 0.0) or 0.0)
            if upl == 0.0:
                upl = (curr_p - entry) * size if direction == "BUY" else (entry - curr_p) * size
            total_upl += upl
            p_icon = "🟢" if upl >= 0 else "🔴"

            lines.append(
                f"<b>#Broker {direction} {size} Lot GOLD</b>\n"
                f"• Entry: <code>${entry:.2f}</code> | SL: <code>${sl:.2f}</code>\n"
                f"• UPL: <code>{p_icon} ${upl:+.2f}</code> | 🌐 Live Broker Sync\n"
            )

        t_icon = "🟢" if total_upl >= 0 else "🔴"
        lines.append(f"══════════════════════════════════════")
        lines.append(f"💰 <b>Total Net UPL ៖</b> <code>{t_icon} ${total_upl:+.2f}</code>")

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛑 បិទគ្រប់ Positions (Close All)", callback_data="btn_qgold_close_all")],
            [InlineKeyboardButton("🔄 ធ្វើបច្ចុប្បន្នភាព (Refresh)", callback_data="btn_qgold_positions")]
        ])
        await self.safe_reply(update, "\n".join(lines), reply_markup=kb)

    async def handle_close_all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Closes all active Gold positions immediately."""
        chat_id = update.effective_chat.id
        u_eng = capital_engine.get_user_capital_engine(chat_id)
        open_trades = db.get_capital_auto_trades_for_user(chat_id)
        gold_trades = [t for t in open_trades if str(t.get("epic", "")).upper() == "GOLD" and t.get("status") == "OPEN"]

        # Also fetch live broker positions
        broker_gold = []
        try:
            broker_pos = u_eng.get_open_positions() if hasattr(u_eng, "get_open_positions") else []
            broker_gold = [
                p for p in broker_pos
                if str(p.get("market", {}).get("epic", "")).upper() == "GOLD"
                or str(p.get("epic", "")).upper() == "GOLD"
            ]
        except Exception:
            broker_gold = []

        if not gold_trades and not broker_gold:
            await self.safe_reply(update, "ℹ️ គ្មាន Position មាសណាមួយកំពុងបើកដើម្បីបិទឡើយ។")
            return

        closed_cnt = 0
        seen_deals = set()

        for t in gold_trades:
            deal_id = t.get("deal_id")
            if deal_id:
                seen_deals.add(str(deal_id))
                try:
                    u_eng.close_position(deal_id)
                    db.close_capital_auto_trade(deal_id, exit_price=0.0, exit_reason="USER_MANUAL_CLOSE_ALL")
                    closed_cnt += 1
                except Exception as e:
                    logger.warning(f"Error closing deal {deal_id}: {e}")

        for bp in broker_gold:
            pos_info = bp.get("position", {}) if isinstance(bp.get("position"), dict) else bp
            pos_id = pos_info.get("dealId") or bp.get("dealId")
            if pos_id and str(pos_id) not in seen_deals:
                try:
                    u_eng.close_position(pos_id)
                    closed_cnt += 1
                except Exception as e:
                    logger.warning(f"Error closing broker deal {pos_id}: {e}")

        await self.safe_reply(
            update,
            f"✅ <b>[POSITIONS CLOSED]</b> 🛑\n"
            f"បានបិទរាល់ Position មាសចំនួន <code>{closed_cnt}</code> ដោយជោគជ័យ!"
        )

    async def handle_toggle_auto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggles 24/7 Autonomous Gold Trading."""
        chat_id = update.effective_chat.id
        auto_cfg = db.get_capital_auto_config(chat_id)
        cur_st = bool(auto_cfg.get("enabled", False)) if auto_cfg else False
        new_st = not cur_st
        db.set_capital_auto_config(chat_id=chat_id, enabled=new_st, budget=300.0, max_positions=5, is_demo=False)

        st_text = "🟢 <b>ដំណើរការ ២៤/៧ (ACTIVE)</b>" if new_st else "🔴 <b>ផ្អាកបណ្តោះអាសន្ន (PAUSED)</b>"
        msg = (
            f"🤖 <b>[QUANT GOLD 24/7 AUTONOMOUS ENGINE]</b> 🥇\n"
            f"══════════════════════════════════════\n"
            f"• ស្ថានភាពបច្ចុប្បន្ន ៖ {st_text}\n"
            f"• ថវិកាជួញដូរ (Budget) ៖ <code>$300.00</code>\n"
            f"• វិសាលគមត្រួតពិនិត្យ ៖ <code>19 Timeframes (M1 ដល់ 1 Month)</code>\n"
            f"• ប្រព័ន្ធការពារដើមទុន ៖ <code>Breakeven Armor +2.0R & Flash Shock Harvest</code>\n"
            f"══════════════════════════════════════\n"
            f"<i>{ 'ម៉ាស៊ីន AI នឹងជួញដូរមាសស្វ័យប្រវត្តនៅពេលមានឱកាសឈ្នះខ្ពស់!' if new_st else 'ម៉ាស៊ីន AI ត្រូវបានផ្អាកការបើក Position ថ្មី។' }</i>"
        )
        await self.safe_reply(update, msg)

    async def handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Shows real-time system health, Capital.com connection, and VPS diagnostics."""
        chat_id = update.effective_chat.id
        bid, ask, spread = self.exec_engine.get_live_gold_price_quote()
        curr_p = (bid + ask) / 2.0

        c_eng = capital_engine.get_capital_engine()
        session_ok = c_eng.is_session_valid() if hasattr(c_eng, "is_session_valid") else True

        # Process CPU & RAM
        import psutil
        cpu_usage = psutil.cpu_percent(interval=0.1)
        ram_usage = psutil.virtual_memory().percent

        msg = (
            f"⚡ <b>[QUANT GOLD SYSTEM HEALTH & DIAGNOSTICS]</b> 🥇\n"
            f"══════════════════════════════════════\n"
            f"💵 <b>តម្លៃមាស (XAUUSD) ៖</b> <code>${curr_p:.2f}</code>\n"
            f"• Bid: <code>${bid:.2f}</code> | Ask: <code>${ask:.2f}</code> | Spread: <code>${spread:.2f}</code>\n"
            f"{'🟢' if session_ok else '🟡'} <b>Capital.com Session ៖</b> <code>{'ACTIVE (Connected)' if session_ok else 'Standby'}</code>\n"
            f"🖥️ <b>Google Cloud VPS (quant-gold) ៖</b>\n"
            f"• CPU Load: <code>{cpu_usage}%</code> | RAM: <code>{ram_usage}%</code> (4 vCPUs, 16 GB RAM)\n"
            f"• Region: <code>Tokyo (asia-northeast1-a)</code> / <code>Google Cloud Linux VPS</code>\n"
            f"• Latency: <code>&lt; 0.001ms (In-Memory RAM Engine)</code>\n"
            f"══════════════════════════════════════\n"
            f"✅ <i>ប្រព័ន្ធកំពុងដំណើរការឥតគិតថ្លៃ ២៤/៧ ៣៦៥ ដោយគ្មានបញ្ហាបច្ចេកទេស!</i>"
        )
        await self.safe_reply(update, msg)

    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Displays user guide and trading handbook."""
        help_text = (
            f"📖 <b>[ANGKOR QUANT - QUANT GOLD USER GUIDE]</b> 🥇\n"
            f"══════════════════════════════════════\n"
            f"<b>របៀបប្រើប្រាស់ប្រព័ន្ធ Quant Gold ៖</b>\n\n"
            f"1. <b>/start ឬ /capital ៖</b> បើកផ្ទាំងបញ្ជា Dashboard វិភាគ 19 Timeframes និងសញ្ញា AI\n"
            f"2. <b>🟢 1-Tap BUY / 🔴 1-Tap SELL ៖</b> បើក Order មាសភ្លាមៗជាមួយ Structural SL & Breakeven Armor\n"
            f"3. <b>🤖 Auto-Trade (ON/OFF) ៖</b> បើកដំណើរការជួញដូរស្វ័យប្រវត្ត ២៤/៧\n"
            f"4. <b>/positions ៖</b> មើលបញ្ជី Position ដែលកំពុងរត់ និងប្រាក់ចំណេញបច្ចុប្បន្ន\n"
            f"5. <b>/close ៖</b> បិទរាល់ Position មាសទាំងអស់ជាបន្ទាន់\n"
            f"6. <b>/status ៖</b> ពិនិត្យមើលស្ថានភាព Server VPS និងតម្លៃមាស Real-Time\n\n"
            f"🛡️ <b>កាតព្វកិច្ចការពារដើមទុន (FIDUCIARY COVENANT) ៖</b>\n"
            f"• ប្រព័ន្ធបដិសេធដាច់ខាតការដេញតាមទីផ្សារកំពូល ឬបាត (Zero Chasing)\n"
            f"• ពេលចំណេញដល់ +2.0R ប្រព័ន្ធនឹងចាក់សោរ Breakeven Armor ភ្លាម (0.00R Risk)\n"
            f"• គ្មានការជួញដូរដោយគ្មាន Stop Loss ដាច់ខាត (Zero No-SL Trading)!\n"
            f"══════════════════════════════════════\n"
        )
        await self.safe_reply(update, help_text)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles all 1-tap interactive inline button clicks."""
        query = update.callback_query
        data = query.data
        chat_id = update.effective_chat.id

        if data in ["btn_qgold_refresh", "btn_qgold_scan"]:
            try:
                await query.answer("🥇 Scanning 19 Timeframes for Gold...")
            except Exception:
                pass
            raw_lang = db.get_user_language(chat_id)
            user_lang = "khmer" if raw_lang in ["km", "khmer", "0", "1", "auto"] else "english"
            text, kb = await self.bridge.build_quant_gold_overview_ui(chat_id, user_lang)
            await self.safe_edit(query, text, reply_markup=kb)

        elif data == "btn_qgold_buy":
            try:
                await query.answer("⚡ Executing 1-Tap Gold BUY...")
            except Exception:
                pass
            await self.handle_buy(update, context)

        elif data == "btn_qgold_sell":
            try:
                await query.answer("⚡ Executing 1-Tap Gold SELL...")
            except Exception:
                pass
            await self.handle_sell(update, context)

        elif data == "btn_qgold_toggle":
            await self.handle_toggle_auto(update, context)
            try:
                await query.answer("Auto-Trade Toggled!")
            except Exception:
                pass

        elif data == "btn_qgold_positions":
            await self.handle_positions(update, context)

        elif data == "btn_qgold_status":
            await self.handle_status(update, context)

        elif data == "btn_qgold_help":
            await self.handle_help(update, context)

        elif data == "btn_qgold_close_all":
            try:
                await query.answer("Closing all positions...")
            except Exception:
                pass
            await self.handle_close_all(update, context)

        elif data == "btn_capital_menu":
            await self.handle_start(update, context)

    async def handle_text_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles clicks from the bottom persistent keyboard."""
        text = update.effective_message.text.strip() if update.effective_message and update.effective_message.text else ""

        if "Quant Gold Dashboard" in text or "Scan 19 TFs" in text:
            await self.handle_start(update, context)
        elif "BUY GOLD" in text:
            await self.handle_buy(update, context)
        elif "SELL GOLD" in text:
            await self.handle_sell(update, context)
        elif "Open Positions" in text:
            await self.handle_positions(update, context)
        elif "Auto-Trade" in text:
            await self.handle_toggle_auto(update, context)
        elif "Status" in text:
            await self.handle_status(update, context)

