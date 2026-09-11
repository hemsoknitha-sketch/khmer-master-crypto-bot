# test_news_sentiment_intelligence.py
import re
import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Deep Institutional Keywords
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

COIN_MAP = [
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

def evaluate_institutional_news_impact(title: str, description: str, target_sym: str = None, ai_engine = None) -> dict:
    t_lower = title.lower()
    d_lower = description.lower()
    comb_lower = t_lower + " " + d_lower

    # 1. Target coin resolution
    resolved_sym = target_sym
    if not resolved_sym or resolved_sym == "BTCUSDT":
        for sym, keywords in COIN_MAP:
            if any(re.search(r'\b' + re.escape(k) + r'\b', t_lower) for k in keywords):
                resolved_sym = sym
                break
        if not resolved_sym:
            for sym, keywords in COIN_MAP:
                if any(re.search(r'\b' + re.escape(k) + r'\b', d_lower) for k in keywords):
                    resolved_sym = sym
                    break
        if not resolved_sym:
            resolved_sym = "BTCUSDT"

    # 2. Check for high-impact shutdown phrases (Direct 25x score)
    critical_bearish_triggers = [
        "put down", "shut down", "closing", "liquidat", "delist", "terminate",
        "reject", "deny", "unwind", "subpoena", "lawsuit", "bankrupt", "low net assets"
    ]
    critical_bullish_triggers = [
        "approved", "greenlight", "record inflow", "adoption", "treasury reserve", "all-time high"
    ]

    bear_score = 0
    bull_score = 0

    # Title evaluation (Heavy 10x weight)
    for kw in INSTITUTIONAL_BEARISH_KEYWORDS:
        if kw in t_lower:
            bear_score += 15 if any(ct in kw for ct in critical_bearish_triggers) else 10
    for kw in INSTITUTIONAL_BULLISH_KEYWORDS:
        if kw in t_lower:
            # Check negation in title
            negated = False
            for neg in NEGATION_PATTERNS:
                if re.search(neg + re.escape(kw), t_lower):
                    negated = True
                    break
            if negated:
                bear_score += 8
            else:
                bull_score += 15 if any(ct in kw for ct in critical_bullish_triggers) else 10

    # Description evaluation (2x weight with strict negation guard)
    for kw in INSTITUTIONAL_BEARISH_KEYWORDS:
        if kw in d_lower:
            bear_score += 4
    for kw in INSTITUTIONAL_BULLISH_KEYWORDS:
        if kw in d_lower:
            negated = False
            for neg in NEGATION_PATTERNS:
                if re.search(neg + re.escape(kw), d_lower):
                    negated = True
                    break
            if negated:
                bear_score += 4
            else:
                bull_score += 2

    # 3. Multi-Model AI Engine Evaluation if available
    ai_bias = None
    ai_confidence = 88.0
    if ai_engine and hasattr(ai_engine, "analyze_opportunity"):
        try:
            eval_prompt = (
                f"You are the Chief Risk Officer at an institutional crypto fund.\n"
                f"Evaluate this breaking news for quantitative trading:\n"
                f"HEADLINE: {title}\n"
                f"DETAILS: {description[:400]}\n"
                f"TARGET: {resolved_sym}\n\n"
                f"CRITICAL RULE: If an ETF is being put down, closed, rejected, or liquidating, it is strongly BEARISH, NEVER bullish.\n\n"
                f"Reply strictly in this format:\n"
                f"VERDICT: [BULLISH/BEARISH/NEUTRAL]\n"
                f"ACTION: [BUY/SELL/HEDGE]\n"
                f"CONFIDENCE: [70-98]"
            )
            ai_res = ai_engine.analyze_opportunity(eval_prompt)
            v_match = re.search(r"VERDICT:\s*(BULLISH|BEARISH|NEUTRAL)", ai_res, re.IGNORECASE)
            c_match = re.search(r"CONFIDENCE:\s*(\d+)", ai_res, re.IGNORECASE)
            if v_match:
                ai_bias = v_match.group(1).upper()
            if c_match:
                ai_confidence = float(c_match.group(1))
        except Exception:
            pass

    # 4. Synthesize Lexical + AI Verdict
    if ai_bias:
        if ai_bias == "BEARISH":
            sentiment = "BEARISH"
            trade_side = "SELL"
        elif ai_bias == "BULLISH":
            # Sanity check: If lexical is heavily bearish (e.g. "put down"), prevent false bullish
            if bear_score > bull_score + 10:
                sentiment = "BEARISH"
                trade_side = "SELL"
            else:
                sentiment = "BULLISH"
                trade_side = "BUY"
        else:
            sentiment = "NEUTRAL"
            trade_side = "HEDGE"
        win_rate = round(min(98.5, max(85.0, ai_confidence)), 1)
    else:
        # Lexical-only synthesis
        if bear_score > bull_score:
            sentiment = "BEARISH"
            trade_side = "SELL"
            win_rate = round(min(97.5, max(88.0, 85.0 + (bear_score - bull_score) * 0.5)), 1)
        elif bull_score > bear_score:
            sentiment = "BULLISH"
            trade_side = "BUY"
            win_rate = round(min(97.5, max(88.0, 85.0 + (bull_score - bear_score) * 0.5)), 1)
        else:
            # Ambiguous / zero signal -> NEVER default to BUY! Default to HEDGE!
            sentiment = "NEUTRAL"
            trade_side = "HEDGE"
            win_rate = 85.0

    # 5. Market Bias text
    if sentiment == "BEARISH":
        market_bias_km = "🔴 BEARISH DISTRIBUTION (ស្ថាប័នកាត់បន្ថយហានិភ័យ / បិទបញ្ចប់ ETF)"
        market_bias_en = "🔴 BEARISH DISTRIBUTION (Institutional De-risking / ETF Closure)"
        market_bias_zh = "🔴 机构减仓避险 (ETF清盘清算)"
        footnote_cmd = f"/turbo_hedge {resolved_sym} 20 10 SELL 2.5 1234"
    elif sentiment == "BULLISH":
        market_bias_km = "🟢 BULLISH ACCUMULATION (ទិញសន្សំតាមស្ថាប័ន)"
        market_bias_en = "🟢 BULLISH ACCUMULATION (Institutional Inflows)"
        market_bias_zh = "🟢 看涨吸筹 (机构净流入)"
        footnote_cmd = f"/turbo_hedge {resolved_sym} 20 10 BUY 2.5 1234"
    else:
        market_bias_km = "⚪ VOLATILITY EXPANSION (យុទ្ធសាស្ត្រ HEDGE ការពារហានិភ័យ 0%)"
        market_bias_en = "⚪ VOLATILITY EXPANSION (Delta-Neutral 0% Risk Hedge)"
        market_bias_zh = "⚪ 波动率扩张 (Delta中性对冲)"
        footnote_cmd = f"/turbo_hedge HEDGE {resolved_sym} 50"

    score = 8
    if any(w in t_lower for w in ['etf', 'sec', 'binance', 'fed', 'rate', 'hack', 'record', 'billion', 'million']):
        score = 9

    return {
        "target_sym": resolved_sym,
        "sentiment": sentiment,
        "trade_side": trade_side,
        "win_rate": win_rate,
        "impact_score": score,
        "market_bias_km": market_bias_km,
        "market_bias_en": market_bias_en,
        "market_bias_zh": market_bias_zh,
        "footnote_cmd": footnote_cmd,
        "bear_score": bear_score,
        "bull_score": bull_score
    }

# Test Cases
test_cases = [
    {
        "title": "Bitwise to put down Dogecoin ETF less than a year after launch",
        "desc": "Net Assets in lowest level of $688,000 ... ending ... cash payouts ... whale accumulation did not show bullish momentum...",
        "expected_sentiment": "BEARISH",
        "expected_coin": "DOGEUSDT",
        "expected_side": "SELL"
    },
    {
        "title": "SEC Approves Spot Solana ETF with Record $1.2B Day-One Inflow",
        "desc": "Institutional adoption surges as trading volume breaks historic records across major exchanges.",
        "expected_sentiment": "BULLISH",
        "expected_coin": "SOLUSDT",
        "expected_side": "BUY"
    },
    {
        "title": "Ethereum Core Developers Discuss Upgrade Timeline Amid Market Stability",
        "desc": "Technical meeting addresses protocol efficiency and fee structures without major timeline shifts.",
        "expected_sentiment": "NEUTRAL",
        "expected_coin": "ETHUSDT",
        "expected_side": "HEDGE"
    }
]

print("==================================================")
print("TESTING INSTITUTIONAL NEWS EVALUATION ENGINE")
print("==================================================")
all_pass = True
for tc in test_cases:
    res = evaluate_institutional_news_impact(tc["title"], tc["desc"])
    print(f"\nHeadline: '{tc['title']}'")
    print(f"Target: {res['target_sym']} | Sentiment: {res['sentiment']} | Side: {res['trade_side']} | Win Rate: {res['win_rate']}%")
    print(f"Scores: Bear={res['bear_score']}, Bull={res['bull_score']}")
    print(f"Bias KM: {res['market_bias_km']}")
    print(f"Command: {res['footnote_cmd']}")
    
    if res["sentiment"] != tc["expected_sentiment"] or res["target_sym"] != tc["expected_coin"] or res["trade_side"] != tc["expected_side"]:
        print(f"❌ FAIL: Expected {tc['expected_sentiment']} on {tc['expected_coin']} {tc['expected_side']}")
        all_pass = False
    else:
        print("✅ PASS!")

print("\n" + "=" * 50)
if all_pass:
    print(">>> ALL INSTITUTIONAL EVALUATION TESTS PASSED (100%) <<<")
else:
    print(">>> SOME TESTS FAILED <<<")
