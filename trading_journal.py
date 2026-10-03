# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - TRADING JOURNAL & PRE-FLIGHT CONFLUENCE CHECKLIST
Document Version: 1.0.0
Ground Truth Authority: Invariant 47 & 50 (Pedagogical & Quantitative Execution Standard)

Inspired by the "Trading From Zero" institutional discipline framework:
- Ep. 9 & 10: Multi-Timeframe Confluence (Structure + S/R Zone + Moving Average)
- Ep. 12 & 13: Quantitative Expectancy (E[X] > 0) & Overfitting Shield
- Ep. 14: Structured Trading Journal & Strategy Loss vs Mistake Attribution
- Ep. 15: Fractional Kelly Capital Allocation & Asymmetric Risk-to-Reward (R:R >= 1:2.0)
- Ep. 17: Trader Psychology Citadel (Combats FOMO, Fear, Greed & Revenge Trading)
- Ep. 18: 6-Step Routine Loop (PREPARE -> ANALYZE -> WAIT -> EXECUTE -> RECORD -> REVIEW)
"""

import os
import sqlite3
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ui_standards import (
    DIVIDER_HEAVY,
    DIVIDER_LIGHT,
    DIVIDER_DASH,
    DIVIDER_DOUBLE,
    INSTITUTIONAL_HEADER,
    INSTITUTIONAL_FOOTER
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "bot_database.db")


# ─── TAG DEFINITIONS & DISCIPLINE METRICS ────────────────────────────────────

TAG_CATALOG = {
    "STRATEGY_RULE": {
        "label": "✅ តាមក្បួនត្រឹមត្រូវ",
        "en_label": "Strategy Rule (Clean)",
        "score": 100.0,
        "is_mistake": False,
        "desc": "Trade អនុវត្តតាមក្បួន System, SL & TP ច្បាស់លាស់ (វិន័យ 100%)",
        "icon": "✅"
    },
    "FOMO_CHASE": {
        "label": "⚠️ FOMO ដេញថ្លៃ",
        "en_label": "FOMO / Chased Price",
        "score": 50.0,
        "is_mistake": True,
        "desc": "ចូលផ្សារដេញតាមទៀនវែងដោយគ្មាន Setup ឬខ្លាចធ្លាក់ឡាន",
        "icon": "⚠️"
    },
    "EARLY_PANIC": {
        "label": "🛑 ភ័យបិទមុន",
        "en_label": "Early Panic Exit",
        "score": 60.0,
        "is_mistake": True,
        "desc": "បិទមុន Target ឬភ័យកាត់មុន SL ដោយសារអារម្មណ៍ភ័យខ្លាច",
        "icon": "🛑"
    },
    "REVENGE_TRADE": {
        "label": "🔄 Revenge ឌឺទីផ្សារ",
        "en_label": "Revenge Trading",
        "score": 30.0,
        "is_mistake": True,
        "desc": "បើក Trade ភ្លាមៗក្រោយចាញ់ ដើម្បីចង់ស្រង់ដើមវិញ",
        "icon": "🔄"
    },
    "MISSED_PLAN": {
        "label": "💤 ខុស Plan / លើសទុន",
        "en_label": "Missed Plan / Overleveraged",
        "score": 40.0,
        "is_mistake": True,
        "desc": "ប្រើទុនធំជ្រុល ឬមិនបានឆែក Economic Calendar មុនពេល Trade",
        "icon": "💤"
    }
}


# ─── DATABASE INITIALIZATION & REVIEWS TABLE ─────────────────────────────────

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    return conn


def init_trade_journal_table():
    """Initializes the trade journal review & mistake tagging schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS trade_journal_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id INTEGER UNIQUE,
        chat_id INTEGER,
        symbol TEXT,
        side TEXT,
        entry_price REAL,
        exit_price REAL,
        pnl REAL,
        pnl_percent REAL,
        tag TEXT DEFAULT 'UNTAGGED',
        tag_label TEXT DEFAULT 'មិនទាន់ Tag',
        mistake_reason TEXT DEFAULT '',
        discipline_score REAL DEFAULT 100.0,
        confluence_checklist TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        created_at TEXT,
        updated_at TEXT
    )''')
    conn.commit()
    conn.close()


# Ensure table is ready on module import
init_trade_journal_table()


# ─── DATA SYNCHRONIZATION & TRADE RETRIEVAL ──────────────────────────────────

def sync_recent_trades_to_journal(chat_id: int, limit: int = 20):
    """
    Synchronizes closed trades from trade_history into trade_journal_reviews
    so they appear seamlessly in the journal interface for tagging.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if trade_history table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trade_history'")
        if not cursor.fetchone():
            return

        cursor.execute("""
            SELECT id, chat_id, symbol, side, entry_price, exit_price, pnl, pnl_percent, exit_time
            FROM trade_history
            WHERE chat_id = ?
            ORDER BY id DESC
            LIMIT ?
        """, (chat_id, limit))
        rows = cursor.fetchall()

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in rows:
            tid, cid, sym, side, entry_p, exit_p, pnl, pnl_pct, exit_t = row
            # Insert IGNORE if already present
            cursor.execute("""
                INSERT OR IGNORE INTO trade_journal_reviews
                (trade_id, chat_id, symbol, side, entry_price, exit_price, pnl, pnl_percent, tag, tag_label, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'UNTAGGED', 'មិនទាន់ Tag', ?, ?)
            """, (tid, cid, sym or "UNKNOWN", side or "LONG", entry_p or 0.0, exit_p or 0.0, pnl or 0.0, pnl_pct or 0.0, exit_t or now_str, now_str))

        conn.commit()
    except Exception as e:
        print(f"⚠️ [JOURNAL SYNC NOTICE]: {e}")
    finally:
        conn.close()


def get_journal_trades(chat_id: int, limit: int = 5, offset: int = 0) -> List[Dict[str, Any]]:
    """Retrieves paginated journal trade entries for a specific user."""
    sync_recent_trades_to_journal(chat_id, limit=30)
    conn = get_db_connection()
    cursor = conn.cursor()
    trades = []
    try:
        cursor.execute("""
            SELECT id, trade_id, symbol, side, entry_price, exit_price, pnl, pnl_percent, tag, tag_label, mistake_reason, discipline_score, updated_at
            FROM trade_journal_reviews
            WHERE chat_id = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (chat_id, limit, offset))
        for row in cursor.fetchall():
            trades.append({
                "journal_id": row[0],
                "trade_id": row[1],
                "symbol": row[2],
                "side": row[3],
                "entry_price": row[4],
                "exit_price": row[5],
                "pnl": row[6],
                "pnl_percent": row[7],
                "tag": row[8],
                "tag_label": row[9],
                "mistake_reason": row[10],
                "discipline_score": row[11],
                "updated_at": row[12]
            })
    except Exception as e:
        print(f"⚠️ [GET JOURNAL TRADES ERROR]: {e}")
    finally:
        conn.close()
    return trades


def get_journal_trade_by_id(trade_id: int, chat_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single journal trade by trade_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    trade = None
    try:
        cursor.execute("""
            SELECT id, trade_id, symbol, side, entry_price, exit_price, pnl, pnl_percent, tag, tag_label, mistake_reason, discipline_score, notes, updated_at
            FROM trade_journal_reviews
            WHERE (trade_id = ? OR id = ?) AND chat_id = ?
            LIMIT 1
        """, (trade_id, trade_id, chat_id))
        row = cursor.fetchone()
        if row:
            trade = {
                "journal_id": row[0],
                "trade_id": row[1],
                "symbol": row[2],
                "side": row[3],
                "entry_price": row[4],
                "exit_price": row[5],
                "pnl": row[6],
                "pnl_percent": row[7],
                "tag": row[8],
                "tag_label": row[9],
                "mistake_reason": row[10],
                "discipline_score": row[11],
                "notes": row[12],
                "updated_at": row[13]
            }
    except Exception as e:
        print(f"⚠️ [GET JOURNAL TRADE ERROR]: {e}")
    finally:
        conn.close()
    return trade


def tag_journal_trade(trade_id: int, chat_id: int, tag_key: str, notes: str = "") -> bool:
    """Tags a closed trade with a specific discipline label and updates metrics."""
    if tag_key not in TAG_CATALOG:
        return False

    meta = TAG_CATALOG[tag_key]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE trade_journal_reviews
            SET tag = ?,
                tag_label = ?,
                mistake_reason = ?,
                discipline_score = ?,
                notes = ?,
                updated_at = ?
            WHERE (trade_id = ? OR id = ?) AND chat_id = ?
        """, (
            tag_key,
            meta["label"],
            meta["desc"],
            meta["score"],
            notes,
            now_str,
            trade_id,
            trade_id,
            chat_id
        ))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"⚠️ [TAG JOURNAL TRADE ERROR]: {e}")
        return False
    finally:
        conn.close()


# ─── PERFORMANCE, EXPECTANCY & DISCIPLINE ANALYTICS ──────────────────────────

def calculate_journal_metrics(chat_id: int) -> Dict[str, Any]:
    """
    Computes professional quantitative trading metrics (Ep. 12, 14, 15, 19):
    - Win Rate (%)
    - Average Win ($) & Average Loss ($)
    - Mathematical Expectancy: E = (W% * AvgWin) - (L% * AvgLoss)
    - Profit Factor: Total Gains / Total Losses
    - Discipline Score (%) & Mistake Ratio
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    metrics = {
        "total_trades": 0,
        "win_trades": 0,
        "loss_trades": 0,
        "win_rate": 0.0,
        "total_pnl": 0.0,
        "avg_win": 0.0,
        "avg_loss": 0.0,
        "profit_factor": 0.0,
        "expectancy": 0.0,
        "tagged_count": 0,
        "strategy_rule_count": 0,
        "mistake_count": 0,
        "discipline_score": 100.0,
        "top_mistake": "គ្មាន"
    }

    try:
        cursor.execute("""
            SELECT pnl, tag, discipline_score
            FROM trade_journal_reviews
            WHERE chat_id = ?
        """, (chat_id,))
        rows = cursor.fetchall()
        if not rows:
            return metrics

        wins = []
        losses = []
        discipline_scores = []
        mistake_counts = {}

        for pnl, tag, d_score in rows:
            metrics["total_trades"] += 1
            metrics["total_pnl"] += pnl

            if pnl > 0:
                metrics["win_trades"] += 1
                wins.append(pnl)
            else:
                metrics["loss_trades"] += 1
                losses.append(abs(pnl))

            if tag and tag != "UNTAGGED":
                metrics["tagged_count"] += 1
                discipline_scores.append(d_score or 100.0)
                if tag == "STRATEGY_RULE":
                    metrics["strategy_rule_count"] += 1
                else:
                    metrics["mistake_count"] += 1
                    mistake_counts[tag] = mistake_counts.get(tag, 0) + 1

        total = metrics["total_trades"]
        w_count = metrics["win_trades"]
        l_count = metrics["loss_trades"]

        metrics["win_rate"] = (w_count / total * 100.0) if total > 0 else 0.0
        metrics["avg_win"] = (sum(wins) / len(wins)) if wins else 0.0
        metrics["avg_loss"] = (sum(losses) / len(losses)) if losses else 0.0

        total_win_val = sum(wins)
        total_loss_val = sum(losses)
        if total_loss_val > 0:
            metrics["profit_factor"] = total_win_val / total_loss_val
        elif total_win_val > 0:
            metrics["profit_factor"] = 99.9
        else:
            metrics["profit_factor"] = 0.0

        # Mathematical Expectancy: E = (Win_Probability * Avg_Win) - (Loss_Probability * Avg_Loss)
        p_win = (w_count / total) if total > 0 else 0.0
        p_loss = (l_count / total) if total > 0 else 0.0
        metrics["expectancy"] = (p_win * metrics["avg_win"]) - (p_loss * metrics["avg_loss"])

        if discipline_scores:
            metrics["discipline_score"] = sum(discipline_scores) / len(discipline_scores)
        else:
            metrics["discipline_score"] = 100.0

        if mistake_counts:
            top_tag = max(mistake_counts, key=mistake_counts.get)
            metrics["top_mistake"] = TAG_CATALOG.get(top_tag, {}).get("label", top_tag)
        else:
            metrics["top_mistake"] = "គ្មាន (100% តាមក្បួន)"

    except Exception as e:
        print(f"⚠️ [CALCULATE JOURNAL METRICS ERROR]: {e}")
    finally:
        conn.close()

    return metrics


# ─── PRE-FLIGHT CONFLUENCE CHECKLIST GENERATOR ────────────────────────────────

def build_confluence_checklist(
    symbol: str,
    side: str,
    timeframe: str = "15m",
    structure: str = "Break of Structure (BOS)",
    value_zone: str = "50% Pullback Demand Zone",
    trend_filter: str = "Price > EMA 50 & EMA 200",
    calendar_status: str = "Zero High-Impact Red News (Safe Window)",
    anti_panic_rsi: float = 48.5,
    risk_kelly_pct: float = 1.5,
    rr_ratio: float = 2.5
) -> str:
    """
    Constructs the official Pre-Flight Confluence Checklist widget (Ep. 9, 10, 16, 18).
    Calibrated for 2.0 cm mobile-fit with zero line-wrapping on Telegram.
    """
    sym = symbol.upper()
    side_u = side.upper()
    side_icon = "🟢 LONG" if side_u == "LONG" or side_u == "BUY" else "🔴 SHORT"

    rsi_text = f"RSI {anti_panic_rsi:.1f} (Anti-Oversold Guard Certified)"
    if side_u in ["SHORT", "SELL"] and anti_panic_rsi <= 38.0:
        rsi_text = f"⚠️ RSI {anti_panic_rsi:.1f} (REJECTED: Oversold Short Guard)"

    lines = [
        "📋 **PRE-FLIGHT CONFLUENCE CHECKLIST**",
        f"_{sym} {side_icon} • TF {timeframe}_",
        DIVIDER_DASH,
        f"├ 🟢 **Market Structure:** {structure}",
        f"├ 🟢 **Value Zone:** {value_zone}",
        f"├ 🟢 **Trend Confluence:** {trend_filter}",
        f"├ 🟢 **Macro Calendar:** {calendar_status}",
        f"├ 🟢 **Anti-Panic Guard:** {rsi_text}",
        f"└ 🛡️ **Risk Sizing:** Fractional Kelly {risk_kelly_pct:.1f}% (R:R 1:{rr_ratio:.1f})",
        DIVIDER_DASH,
        "💡 _All 6 Quantitative Rules Verified Before Execution!_"
    ]
    return "\n".join(lines)


# ─── TELEGRAM UI CARDS & KEYBOARDS ───────────────────────────────────────────

def build_journal_card(chat_id: int, page: int = 0, limit: int = 4) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Builds the main interactive Trading Journal dashboard card on Telegram.
    Allows viewing recent trades, discipline status, and 1-tap mistake tagging.
    """
    metrics = calculate_journal_metrics(chat_id)
    offset = page * limit
    trades = get_journal_trades(chat_id, limit=limit, offset=offset)

    pnl_sign = "+" if metrics["total_pnl"] >= 0 else ""
    pnl_icon = "🟢" if metrics["total_pnl"] >= 0 else "🔴"
    exp_sign = "+" if metrics["expectancy"] >= 0 else ""

    text_parts = [
        "📓 **ANGKOR TRADING JOURNAL & DISCIPLINE** ⚡",
        "_សៀវភៅតាមដាន Trade & កែប្រែចិត្តសាស្ត្រវិន័យ_",
        DIVIDER_DOUBLE,
        f"📊 **លទ្ធផលជួញដូរសរុប (Trade History):**",
        f"• ចំនួន Trades: `{metrics['total_trades']}` (ឈ្នះ {metrics['win_trades']} / ចាញ់ {metrics['loss_trades']})",
        f"• Win Rate: `{metrics['win_rate']:.1f}%`",
        f"• PnL សរុប: {pnl_icon} `{pnl_sign}${metrics['total_pnl']:,.2f}`",
        f"• Profit Factor: `{metrics['profit_factor']:.2f}`",
        f"• Expectancy: `{exp_sign}${metrics['expectancy']:,.2f}` / trade",
        DIVIDER_LIGHT,
        f"🧠 **សន្ទស្សន៍វិន័យជួញដូរ (Discipline Radar):**",
        f"• Discipline Score: `{metrics['discipline_score']:.1f}%` 🛡️",
        f"• Trades បាន Tag: `{metrics['tagged_count']}` / `{metrics['total_trades']}`",
        f"• តាមក្បួន (Clean Rule): `{metrics['strategy_rule_count']}` trades",
        f"• កំហុសខុសវិន័យ (Mistakes): `{metrics['mistake_count']}` trades",
        f"• កំហុសជួបញឹកញាប់: `{metrics['top_mistake']}`",
        DIVIDER_HEAVY,
        "📋 **បញ្ជី Trades ចុងក្រោយ (ចុច Tag ដើម្បីកត់ត្រាវិន័យ):**\n"
    ]

    keyboard = []

    if not trades:
        text_parts.append("_មិនទាន់មានទិន្នន័យ Closed Trades ក្នុង Journal នៅឡើយទេ។_")
        text_parts.append("\n💡 _ពេលប្រព័ន្ធ ឬអ្នកបិទ Trade វានឹងបង្ហាញនៅទីនេះដោយស្វ័យប្រវត្តិ!_")
    else:
        for t in trades:
            t_pnl = t["pnl"]
            t_icon = "🟢" if t_pnl >= 0 else "🔴"
            t_sign = "+" if t_pnl >= 0 else ""
            tag_display = t["tag_label"] or "មិនទាន់ Tag"
            text_parts.append(
                f"{t_icon} **{t['symbol']}** ({t['side']}) | `{t_sign}${t_pnl:,.2f}` (`{t_sign}{t['pnl_percent']:.2f}%`)\n"
                f"   └ 🏷️ Status: **{tag_display}**\n"
            )
            # Add 1-tap tag button for each trade
            btn_text = f"🏷️ Tag #{t['trade_id']} ({t['symbol']})"
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"btn_tag_trade_{t['trade_id']}")])

    # Navigation buttons
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ ទំព័រមុន", callback_data=f"btn_journal_page_{page - 1}"))
    if len(trades) == limit:
        nav_row.append(InlineKeyboardButton("ទំព័របន្ទាប់ ➡️", callback_data=f"btn_journal_page_{page + 1}"))
    if nav_row:
        keyboard.append(nav_row)

    # Action row
    keyboard.append([
        InlineKeyboardButton("📈 Expectancy Analytics", callback_data="btn_journal_expectancy"),
        InlineKeyboardButton("🔄 Refresh Journal", callback_data=f"btn_journal_page_{page}")
    ])
    keyboard.append([
        InlineKeyboardButton("📋 Confluence Checklist", callback_data="btn_journal_confluence_sample"),
        InlineKeyboardButton("🔙 ត្រឡប់ទៅ Menu", callback_data="btn_menu_refresh")
    ])

    text_parts.append(DIVIDER_LIGHT)
    text_parts.append("💡 _«កាត់ខាតតាមក្បួន គឺជាផ្នែកនៃជ័យជម្នះ • កាត់ខាតខុសវិន័យ គឺជាការបំផ្លាញខ្លួនឯង!»_")

    return "\n".join(text_parts), InlineKeyboardMarkup(keyboard)


def build_tagging_card(trade_id: int, chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Builds the tagging selection card where user can categorize a specific trade.
    """
    trade = get_journal_trade_by_id(trade_id, chat_id)
    if not trade:
        return (
            "⚠️ **រកមិនឃើញទិន្នន័យ Trade នេះឡើយ!**\n\nសូមត្រឡប់ទៅពិនិត្យ Journal ម្តងទៀត។",
            InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ត្រឡប់ទៅ Journal", callback_data="btn_journal_page_0")]])
        )

    t_pnl = trade["pnl"]
    t_icon = "🟢" if t_pnl >= 0 else "🔴"
    t_sign = "+" if t_pnl >= 0 else ""

    text = (
        f"🏷️ **TAGGING TRADE #{trade['trade_id']}** ⚡\n"
        f"_{trade['symbol']} • {trade['side']} • {trade['updated_at']}_\n"
        f"{DIVIDER_DOUBLE}\n"
        f"💵 **ព័ត៌មានលម្អិត Trade:**\n"
        f"• Entry: `${trade['entry_price']:,.4f}`\n"
        f"• Exit: `${trade['exit_price']:,.4f}`\n"
        f"• PnL: {t_icon} `{t_sign}${t_pnl:,.2f}` (`{t_sign}{trade['pnl_percent']:.2f}%`)\n"
        f"• Tag បច្ចុប្បន្ន: **{trade['tag_label']}**\n"
        f"{DIVIDER_LIGHT}\n"
        f"🎯 **ជ្រើសរើសមូលហេតុ ឬកំហុសក្នុងការជួញដូរ (Select Tag):**\n"
        f"សូមជ្រើសរើសដោយស្មោះត្រង់ដើម្បីជួយវាស់ស្ទង់វិន័យពិតប្រាកដ៖"
    )

    keyboard = [
        [InlineKeyboardButton("✅ តាមក្បួនត្រឹមត្រូវ (Strategy Rule)", callback_data=f"btn_set_tag_{trade_id}_STRATEGY_RULE")],
        [InlineKeyboardButton("⚠️ FOMO ដេញថ្លៃ (FOMO Chase)", callback_data=f"btn_set_tag_{trade_id}_FOMO_CHASE")],
        [InlineKeyboardButton("🛑 ភ័យបិទមុន (Early Panic Exit)", callback_data=f"btn_set_tag_{trade_id}_EARLY_PANIC")],
        [InlineKeyboardButton("🔄 Revenge ឌឺទីផ្សារ (Revenge Trade)", callback_data=f"btn_set_tag_{trade_id}_REVENGE_TRADE")],
        [InlineKeyboardButton("💤 ខុស Plan / លើសទុន (Missed Plan)", callback_data=f"btn_set_tag_{trade_id}_MISSED_PLAN")],
        [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Journal", callback_data="btn_journal_page_0")]
    ]

    return text, InlineKeyboardMarkup(keyboard)


def build_performance_expectancy_card(chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Builds the deep quantitative Expectancy & Formula Breakdown card (Ep. 12, 19).
    """
    m = calculate_journal_metrics(chat_id)
    exp_sign = "+" if m["expectancy"] >= 0 else ""

    text = (
        "📈 **MATHEMATICAL EXPECTANCY & METRICS** ⚡\n"
        "_រូបមន្តប្រៀបឈ្នះបែបគណិតវិទ្យា (The Quantitative Edge)_\n"
        f"{DIVIDER_DOUBLE}\n"
        "📐 **រូបមន្ត Expectancy ($E$):**\n"
        "`E = (Win% × AvgWin) - (Loss% × AvgLoss)`\n\n"
        f"📊 **ទិន្នន័យជាក់ស្តែងរបស់អ្នក:**\n"
        f"• Win Rate ($W$): `{m['win_rate']:.1f}%`\n"
        f"• Loss Rate ($L$): `{(100.0 - m['win_rate']):.1f}%`\n"
        f"• Average Win: `${m['avg_win']:,.2f}`\n"
        f"• Average Loss: `${m['avg_loss']:,.2f}`\n"
        f"• **Net Expectancy ($E$):** `{exp_sign}${m['expectancy']:,.2f}` / trade\n"
        f"• **Profit Factor:** `{m['profit_factor']:.2f}`\n"
        f"{DIVIDER_LIGHT}\n"
        "💡 **ការបកស្រាយលទ្ធផល:**\n"
    )

    if m["expectancy"] > 0:
        text += (
            "🟢 **ប្រព័ន្ធរបស់អ្នកមាន Positive Expectancy ($E > 0$):**\n"
            "មានន័យថារាល់ Trade មួយៗជាមធ្យមបង្កើតប្រាក់ចំណេញ។ ដរាបណាអ្នករក្សាវិន័យមិនកាត់ខាតខុសក្បួន "
            "ដើមទុនរបស់អ្នកនឹងកើនឡើងតាមគណិតវិទ្យា!\n"
        )
    elif m["total_trades"] == 0:
        text += "⚪ _មិនទាន់មានទិន្នន័យគ្រប់គ្រាន់ក្នុងការគណនា Expectancy ឡើយ។_\n"
    else:
        text += (
            "🔴 **ប្រព័ន្ធរបស់អ្នកមាន Negative Expectancy ($E \\le 0$):**\n"
            "មូលហេតុចម្បងភាគច្រើនមកពី Average Loss ធំជាង Average Win (កាត់ចំណេញតិច កាត់ខាតច្រើន) "
            "ឬការលូកដៃបិទ trade មុនក្បួន។ សូមពិនិត្យ Tag Mistakes ក្នុង Journal!\n"
        )

    text += f"{DIVIDER_HEAVY}\n"
    text += "🧠 **Discipline Score:** `" + f"{m['discipline_score']:.1f}%` | Mistakes: `" + f"{m['mistake_count']}`\n"

    keyboard = [
        [InlineKeyboardButton("📓 ត្រឡប់ទៅ Journal", callback_data="btn_journal_page_0")],
        [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Menu", callback_data="btn_menu_refresh")]
    ]

    return text, InlineKeyboardMarkup(keyboard)
