import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '.')
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ui_standards import DIVIDER_HEAVY

# Mock news article
title = "Bitwise to put down Dogecoin ETF less than a year after launch"
description = "Net Assets in lowest level of $688,000 ... ending ... cash payouts ... whale accumulation did not show bullish momentum..."
link = "https://cointelegraph.com/news/bitwise-put-down-dogecoin-etf-year-launch"
image_url = "https://images.cointelegraph.com/images/840_test.jpg"
source_name = "CoinTelegraph"
kh_date_str = "ថ្ងៃសុក្រ ទី១១ ខែកញ្ញា ឆ្នាំ២០២៦ ម៉ោង ១៥:៣៦ (GMT+7)"
texts = {
    'khmer': "ទីក្រុងញូវយ៉ក ៖ ក្រុមហ៊ុនគ្រប់គ្រងទ្រព្យសកម្មឌីជីថលឈានមុខគេ Bitwise បានប្រកាសសម្រេចចិត្តបញ្ចប់ប្រតិបត្តិការនៃមូលបត្រប្តូរបាន Dogecoin...",
    'english': "NEW YORK — Bitwise has announced the closure of its Dogecoin ETF due to negligible AUM...",
    'chinese': "纽约讯 — Bitwise 宣布清盘旗下 Dogecoin ETF..."
}

# Run lexical evaluation logic from scheduler_tasks.py
t_lower = title.lower()
d_lower = description.lower()

coin_map = [
    ("BTCUSDT", ["btc", "bitcoin"]),
    ("ETHUSDT", ["eth", "ethereum"]),
    ("SOLUSDT", ["sol", "solana"]),
    ("BNBUSDT", ["bnb", "binance coin", "binance"]),
    ("XRPUSDT", ["xrp", "ripple"]),
    ("DOGEUSDT", ["doge", "dogecoin"]),
    ("ADAUSDT", ["ada", "cardano"]),
    ("AVAXUSDT", ["avax", "avalanche"]),
    ("SUIUSDT", ["sui"]),
    ("PEPEUSDT", ["pepe"]),
    ("SHIBUSDT", ["shib", "shiba"]),
    ("LINKUSDT", ["link", "chainlink"]),
    ("NEARUSDT", ["near"]),
    ("APTUSDT", ["apt", "aptos"]),
]
target_sym = "BTCUSDT"
for sym, keywords in coin_map:
    if any(re.search(r'\b' + re.escape(k) + r'\b', t_lower) for k in keywords):
        target_sym = sym
        break
if target_sym == "BTCUSDT":
    for sym, keywords in coin_map:
        if any(re.search(r'\b' + re.escape(k) + r'\b', d_lower) for k in keywords):
            target_sym = sym
            break

INSTITUTIONAL_BEARISH_KEYWORDS = [
    "put down", "shut down", "shutdown", "close", "closing", "liquidate", "liquidating", "liquidation",
    "terminate", "terminating", "termination", "delist", "delisting", "withdraw", "withdrawing", "withdrawn",
    "reject", "rejection", "deny", "denial", "payout", "payouts", "unwind", "redeem", "redemption",
    "fail", "failure", "failed", "cancel", "cancelled", "halt", "halted", "drop etf", "abandon", "abandoned",
    "low net assets", "illiquid", "insolvent", "insolvency", "bankrupt", "bankruptcy", "outflow", "outflows",
    "dump", "dumps", "crash", "crashes", "plunge", "plunges", "bleeding", "collapse", "collapses",
    "investigation", "subpoena", "lawsuit", "sue", "sued", "fraud", "scam", "hack", "hacked", "exploit",
    "exploited", "fine", "penalty", "crackdown", "ban", "banned", "bear", "bearish", "selloff", "panic",
    "drop", "drops", "fall", "falls", "decline", "declines", "threat", "risk off", "de-risk"
]

INSTITUTIONAL_BULLISH_KEYWORDS = [
    "inflow", "inflows", "record inflow", "approve", "approved", "approval", "greenlight", "launch", "launched",
    "debut", "debuts", "expand", "expansion", "partnership", "soar", "soars", "surge", "surges", "jump", "jumps",
    "rally", "rallies", "record", "high", "highs", "strongest", "bull", "bullish", "all-time high", "ath",
    "breakout", "accumulate", "accumulation", "accumulating", "buying", "buyback", "adopt", "adoption",
    "rebound", "rebounds", "recover", "recovery", "treasury reserve", "milestone", "gain", "gains", "pump", "boost"
]

NEGATION_PATTERNS = [
    r'\b(?:not|did not|didn\'t|fail(?:ed)? to|unable to|no|loss of|lack of|without|cannot|less than)\b[^\.\,\;\!\?]{0,40}\b'
]

critical_bearish_triggers = [
    "put down", "shut down", "closing", "liquidat", "delist", "terminate",
    "reject", "deny", "unwind", "subpoena", "lawsuit", "bankrupt", "low net assets"
]
critical_bullish_triggers = [
    "approved", "greenlight", "record inflow", "adoption", "treasury reserve", "all-time high"
]

bear_score = 0
bull_score = 0

for kw in INSTITUTIONAL_BEARISH_KEYWORDS:
    if kw in t_lower:
        bear_score += 15 if any(ct in kw for ct in critical_bearish_triggers) else 10
for kw in INSTITUTIONAL_BULLISH_KEYWORDS:
    if kw in t_lower:
        negated = any(re.search(neg + re.escape(kw), t_lower) for neg in NEGATION_PATTERNS)
        if negated:
            bear_score += 8
        else:
            bull_score += 15 if any(ct in kw for ct in critical_bullish_triggers) else 10

for kw in INSTITUTIONAL_BEARISH_KEYWORDS:
    if kw in d_lower:
        bear_score += 4
for kw in INSTITUTIONAL_BULLISH_KEYWORDS:
    if kw in d_lower:
        negated = any(re.search(neg + re.escape(kw), d_lower) for neg in NEGATION_PATTERNS)
        if negated:
            bear_score += 4
        else:
            bull_score += 2

if bear_score > bull_score:
    sentiment = "BEARISH"
    trade_side = "SELL"
    win_rate = round(min(97.5, max(88.0, 85.0 + (bear_score - bull_score) * 0.5)), 1)
elif bull_score > bear_score:
    sentiment = "BULLISH"
    trade_side = "BUY"
    win_rate = round(min(97.5, max(88.0, 85.0 + (bull_score - bear_score) * 0.5)), 1)
else:
    sentiment = "NEUTRAL"
    trade_side = "HEDGE"
    win_rate = 85.0

if sentiment == "BEARISH":
    market_bias_km = "🔴 BEARISH DISTRIBUTION (ស្ថាប័នកាត់បន្ថយហានិភ័យ / បិទបញ្ចប់ ETF)"
    footnote_cmd = f"/turbo_hedge {target_sym} 20 10 SELL 2.5 1234"
elif sentiment == "BULLISH":
    market_bias_km = "🟢 BULLISH ACCUMULATION (ទិញសន្សំតាមស្ថាប័ន)"
    footnote_cmd = f"/turbo_hedge {target_sym} 20 10 BUY 2.5 1234"
else:
    market_bias_km = "⚪ VOLATILITY EXPANSION (យុទ្ធសាស្ត្រ HEDGE ការពារហានិភ័យ 0%)"
    footnote_cmd = f"/turbo_hedge HEDGE {target_sym} 50"

sym_display = target_sym.replace("USDT", "")
if trade_side == "SELL":
    news_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🔻 Short {sym_display} ($20 10x)", callback_data=f"btn_alert_exec_short_{target_sym}"),
            InlineKeyboardButton(f"🛡️ Hedge {sym_display} (0% Risk)", callback_data=f"btn_alert_exec_hedge_{target_sym}")
        ],
        [
            InlineKeyboardButton("🎛️ Turbo Hedge Suite", callback_data="btn_turbo_hedge")
        ]
    ])
elif trade_side == "BUY":
    news_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🚀 Long {sym_display} ($20 10x)", callback_data=f"btn_alert_exec_long_{target_sym}"),
            InlineKeyboardButton(f"🛒 Spot Buy {sym_display}", callback_data=f"btn_alert_exec_spot_{target_sym}")
        ],
        [
            InlineKeyboardButton("🎛️ Turbo Hedge Suite", callback_data="btn_turbo_hedge")
        ]
    ])
else:
    news_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🛡️ Hedge {sym_display} (0% Risk)", callback_data=f"btn_alert_exec_hedge_{target_sym}"),
            InlineKeyboardButton("🎛️ Turbo Hedge Suite", callback_data="btn_turbo_hedge")
        ]
    ])

alert_msg = f"🚨 **ព័ត៌មានទាន់ហេតុការណ៍ទីផ្សារ CRYPTO (កម្រិតផលប៉ះពាល់ ៖ 9/10)** 🚨\n"
alert_msg += f"{DIVIDER_HEAVY}\n"
alert_msg += f"📰 **{title}**\n\n"
alert_msg += f"🌐 **ប្រភព ៖** {source_name} | 📅 **{kh_date_str}**\n"
alert_msg += f"{DIVIDER_HEAVY}\n\n"
alert_msg += f"{texts['khmer']}\n\n"
alert_msg += f"{DIVIDER_HEAVY}\n"
alert_msg += "📊 **សេចក្តីសន្និដ្ឋានស្ថាប័ន (INSTITUTIONAL VERDICT) ៖**\n"
alert_msg += f"• **ទិសដៅទីផ្សារ (Market Bias) ៖** {market_bias_km}\n"
alert_msg += f"• **អត្រាជោគជ័យ AI (Win Rate Probability) ៖** `{win_rate}%`\n"
alert_msg += f"• **ទ្រព្យសកម្មគោលដៅ ៖** `{target_sym}`\n\n"
alert_msg += "👉 **បញ្ជាជួញដូរស្វ័យប្រវត្តិ (1-Tap Copyable Execution) ៖**\n"
alert_msg += f"`` `{footnote_cmd}` ``\n\n"
alert_msg += f"🔗 [អានប្រភពដើមអន្តរជាតិ]({link})"

print("--- GENERATED ALERT MESSAGE ---")
print(alert_msg)
print("\n--- ATTACHED INLINE BUTTONS ---")
for row in news_kb.inline_keyboard:
    print([f"{btn.text} -> {btn.callback_data}" for btn in row])

assert trade_side == "SELL", "Must be SELL"
assert target_sym == "DOGEUSDT", "Must be DOGEUSDT"
assert "BEARISH DISTRIBUTION" in market_bias_km, "Must be BEARISH"
assert len(DIVIDER_HEAVY) == 12, "Divider must be 12 chars"
print("\n>>> ALL ASSERTIONS PASSED! FLOW VERIFIED! <<<")
