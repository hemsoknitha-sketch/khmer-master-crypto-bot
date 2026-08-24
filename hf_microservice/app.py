"""
FastAPI + Gradio Microservice Server for Hugging Face Space: khmer-master-crypto-bot
Serves as the AI Super Brain Node for APEX AGI ENGINE v11.0.
Supports 100% Free Gradio Space SDK on Hugging Face!
"""

import os
import time
import json
import xml.etree.ElementTree as ET
from typing import Optional, List, Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
import gradio as gr

# ------------------------------------------------------------------------------
# Request & Response Models
# ------------------------------------------------------------------------------

class PredictRequest(BaseModel):
    symbol: str = Field(default="BTCUSDT", description="Target trading pair symbol")

class AnalyzeRequest(BaseModel):
    symbol: str = Field(default="BTCUSDT", description="Target trading pair symbol")
    prompt: Optional[str] = Field(default=None, description="Custom prompt or extra data")
    gemini_key: Optional[str] = Field(default=None, description="Optional Gemini API key")

class NewsRequest(BaseModel):
    symbol: Optional[str] = Field(default=None, description="Optional symbol filter")
    limit: int = Field(default=5, ge=1, le=20, description="Max news items")

class SentimentRequest(BaseModel):
    text: str = Field(..., description="Headline or tweet text to evaluate")

# ------------------------------------------------------------------------------
# Financial NLP Keywords & Sentiment Logic
# ------------------------------------------------------------------------------

BULLISH_KEYWORDS = ["surge", "jump", "soar", "gain", "bull", "breakout", "rally", "buy", "adoption", "approval", "record", "high", "upgrade", "partnership", "inflow", "boost", "soaring", "moon", "pump"]
BEARISH_KEYWORDS = ["drop", "fall", "plummet", "crash", "bear", "hack", "exploit", "ban", "lawsuit", "sec", "dump", "outflow", "decline", "crackdown", "risk", "warn", "threat", "rugpull"]

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cryptopotato.com/feed/",
    "https://news.bitcoin.com/feed/"
]

def evaluate_headline_sentiment(title: str) -> str:
    title_lower = title.lower()
    bull_count = sum(1 for kw in BULLISH_KEYWORDS if kw in title_lower)
    bear_count = sum(1 for kw in BEARISH_KEYWORDS if kw in title_lower)
    if bull_count > bear_count:
        return "BULLISH"
    elif bear_count > bull_count:
        return "BEARISH"
    return "NEUTRAL"

# ------------------------------------------------------------------------------
# Core Processing Functions
# ------------------------------------------------------------------------------

def process_health():
    return {
        "status": "online",
        "service": "khmer-master-crypto-bot-ai-brain",
        "version": "v11.0-super-brain",
        "timestamp": time.time(),
        "uptime": "24/7/365 Free Gradio SDK Active"
    }

def process_predict(symbol: str):
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"): symbol += "USDT"
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        res = requests.get(url, timeout=4).json()
        price = float(res.get("lastPrice", 0))
        pct = float(res.get("priceChangePercent", 0))
        volume = float(res.get("quoteVolume", 0))
        high = float(res.get("highPrice", 0))
        low = float(res.get("lowPrice", 0))

        if pct > 3.0:
            signal, action, conf = "STRONG_BULLISH", "BUY", 88.5
        elif pct > 0.5:
            signal, action, conf = "BULLISH", "BUY", 72.0
        elif pct < -3.0:
            signal, action, conf = "STRONG_BEARISH", "SELL / HEDGE", 85.0
        elif pct < -0.5:
            signal, action, conf = "BEARISH", "SELL", 68.0
        else:
            signal, action, conf = "NEUTRAL_SIDEWAYS", "HOLD / GRID", 55.0

        return {
            "success": True,
            "symbol": symbol,
            "last_price": price,
            "change_24h_pct": pct,
            "volume_24h_usdt": volume,
            "high_24h": high,
            "low_24h": low,
            "ai_signal": signal,
            "recommended_action": action,
            "confidence_score": conf,
            "timestamp": time.time()
        }
    except Exception as e:
        return {"success": False, "error": str(e), "symbol": symbol}

def process_analyze(symbol: str, prompt: str = None, gemini_key: str = None):
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"): symbol += "USDT"
    key = gemini_key or os.getenv("GEMINI_API_KEY")

    if key and len(key) > 5:
        try:
            import google.generativeai as genai
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt_text = (
                f"You are the Apex AGI Super Brain financial advisor for {symbol}.\n"
                f"Data Context: {prompt or 'Analyze current market structure'}\n"
                f"Provide a concise, professional financial analysis report in Khmer language with clear BUY/SELL/HOLD advice, target prices, and risk management stop loss."
            )
            response = model.generate_content(prompt_text)
            return {
                "success": True,
                "symbol": symbol,
                "engine": "Gemini-2.5-Flash (Hugging Face Microservice)",
                "analysis": response.text
            }
        except Exception as e:
            print(f"Gemini call notice: {e}")

    try:
        res = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}", timeout=4).json()
        price = float(res.get("lastPrice", 0))
        pct = float(res.get("priceChangePercent", 0))
        advice = "🚀 BUY / LONG" if pct > 0 else "📉 SELL / SHORT"
        trend = "Bullish Uptrend 🟢" if pct > 0 else "Bearish Downtrend 🔴"

        report = (
            f"🧠 **[APEX AGI SUPER BRAIN - HF MICROSERVICE ANALYSIS]**\n\n"
            f"🪙 **កាក់ ៖** {symbol}\n"
            f"💵 **តម្លៃបច្ចុប្បន្ន ៖** ${price:,.4f}\n"
            f"📊 **ការប្រែប្រួល 24h ៖** {pct:+.2f}%\n"
            f"📈 **និន្នាការទីផ្សារ ៖** {trend}\n\n"
            f"🎯 **ការវិភាគ និងការណែនាំ AI ៖** {advice}\n"
            f"🛡️ **ការគ្រប់គ្រងហានិភ័យ ៖** ដាក់ Stop Loss ត្រឹម -1.5% និង Take Profit ត្រឹម +3.5%។\n\n"
            f"⚡ *ដំណើរការដោយ Hugging Face Microservice (khmer-master-crypto-bot)*"
        )
        return {"success": True, "symbol": symbol, "engine": "Quantitative AI Rule Engine (HF Fallback)", "analysis": report}
    except Exception as e:
        return {"success": False, "error": str(e), "symbol": symbol}

def process_news(symbol: str = None, limit: int = 5):
    news_items = []
    symbol_filter = symbol.upper().replace("USDT", "").strip() if symbol else None

    for feed_url in RSS_FEEDS:
        if len(news_items) >= limit * 2: break
        try:
            res = requests.get(feed_url, timeout=4, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                for item in root.findall("./channel/item"):
                    title = item.findtext("title")
                    link = item.findtext("link")
                    pub_date = item.findtext("pubDate")

                    if not title or (symbol_filter and symbol_filter not in title.upper()):
                        continue

                    sentiment = evaluate_headline_sentiment(title)
                    news_items.append({
                        "title": title.strip(),
                        "link": link.strip() if link else "https://coindesk.com",
                        "pub_date": pub_date.strip() if pub_date else "Recently",
                        "sentiment": sentiment
                    })
                    if len(news_items) >= limit: break
        except Exception:
            continue

    if not news_items:
        news_items = [{
            "title": f"No recent headlines found for {symbol_filter or 'Crypto'}. Market remains in consolidation.",
            "link": "https://binance.com",
            "pub_date": "Now",
            "sentiment": "NEUTRAL"
        }]

    return {"success": True, "symbol": symbol, "count": len(news_items), "news": news_items}

# ------------------------------------------------------------------------------
# Gradio Interface Definition
# ------------------------------------------------------------------------------

with gr.Blocks(title="APEX AGI Super Brain Microservice") as demo:
    gr.Markdown("# ⚡ APEX AGI ENGINE v11.0 - AI SUPER BRAIN MICROSERVICE 🚀")
    gr.Markdown("🟢 **STATUS: ONLINE 24/7/365** | Microservice Node for Khmer Master Crypto Bot")
    
    with gr.Row():
        sym_input = gr.Textbox(label="Trading Pair Symbol", value="BTCUSDT")
        btn = gr.Button("Analyze Symbol")
    
    out_md = gr.Markdown()

    def run_ui(s):
        res = process_predict(s)
        if res.get("success"):
            return (
                f"🪙 **Symbol**: `{res.get('symbol')}`\n"
                f"💵 **Price**: `${res.get('last_price'):,.4f}` (`{res.get('change_24h_pct'):+.2f}%`)\n"
                f"🎯 **AI Signal**: `{res.get('ai_signal')}` (`{res.get('recommended_action')}`)\n"
                f"⚡ **Confidence**: `{res.get('confidence_score')}%`"
            )
        return f"❌ Error: {res.get('error')}"

    btn.click(fn=run_ui, inputs=[sym_input], outputs=[out_md])

# ------------------------------------------------------------------------------
# Attach REST API Endpoints directly to Gradio's underlying FastAPI App
# ------------------------------------------------------------------------------

@demo.app.get("/health")
def api_health():
    return process_health()

@demo.app.post("/predict")
def api_predict(req: PredictRequest):
    return process_predict(req.symbol)

@demo.app.post("/analyze")
def api_analyze(req: AnalyzeRequest):
    return process_analyze(req.symbol, req.prompt, req.gemini_key)

@demo.app.post("/news")
def api_news(req: NewsRequest):
    return process_news(req.symbol, req.limit)

@demo.app.post("/hft_sentiment")
def api_sentiment(req: SentimentRequest):
    return {
        "success": True,
        "text": req.text,
        "sentiment": evaluate_headline_sentiment(req.text),
        "timestamp": time.time()
    }

# ------------------------------------------------------------------------------
# Launch Gradio Server on Hugging Face's Target Python Port (7861)
# Respects Hugging Face Node.js SSR reverse proxy running on Port 7860
# ------------------------------------------------------------------------------

target_port = int(os.environ.get("GRADIO_SERVER_PORT", os.environ.get("PORT", 7861)))
demo.launch(server_name="0.0.0.0", server_port=target_port)
