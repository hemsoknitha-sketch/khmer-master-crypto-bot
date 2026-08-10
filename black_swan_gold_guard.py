import requests
import json
import time
import asyncio

# Geopolitical Crisis & Black-Swan NLP Keyword Classifier
GEOPOLITICAL_CRISIS_KEYWORDS = [
    "war", "military strike", "missile attack", "invasion", "escalation",
    "banking panic", "bank failure", "sanctions", "taiwan conflict",
    "middle east crisis", "nuclear threat", "state of emergency", "flight to safety"
]

def scan_geopolitical_black_swan() -> dict:
    """
    Scans breaking news feeds for geopolitical crisis events using Real-Time NLP.
    Calculates Geopolitical Crisis Severity Index (0 - 100%).
    If Severity Index >= 75%, triggers CRITICAL FLIGHT-TO-SAFETY ALERT.
    """
    guard_data = {
        "crisis_severity_index": 25.0, # Baseline normal geopolitical risk
        "crisis_detected": False,
        "matched_keywords": [],
        "headline_sample": "Global markets trading in normal ranges.",
        "gold_impact": "+$0.00/oz (Baseline)",
        "recommendation": "MONITORING GLOBAL FEEDS (Normal Range)",
        "status": "success"
    }
    
    try:
        from ai_news_engine import fetch_live_news
        news_items = fetch_live_news()
        
        matched = []
        highest_match = ""
        for item in news_items:
            title_lower = item.get("title", "").lower()
            summary_lower = item.get("summary", "").lower()
            text = f"{title_lower} {summary_lower}"
            
            for kw in GEOPOLITICAL_CRISIS_KEYWORDS:
                if kw in text and kw not in matched:
                    matched.append(kw)
                    highest_match = item.get("title", "")
                    
        if matched:
            severity = min(98.0, 30.0 + (len(matched) * 22.5))
            guard_data["crisis_severity_index"] = round(severity, 1)
            guard_data["matched_keywords"] = matched
            guard_data["headline_sample"] = highest_match
            
            if severity >= 75.0:
                guard_data["crisis_detected"] = True
                guard_data["gold_impact"] = "+$30.00 to +$100.00/oz (Flight-to-Safety Spike)"
                guard_data["recommendation"] = "🚨 CRITICAL FLIGHT-TO-SAFETY ALERT: Confirm PAXG Gold Buy!"
            else:
                guard_data["recommendation"] = f"🟡 MODERATE GEOPOLITICAL RISK DETECTED (Index {severity:.1f}%)"
    except Exception as e:
        print(f"⚠️ [BLACK SWAN GUARD] News scan error: {e}")

    return guard_data

def generate_black_swan_report(user_lang: str = "khmer", ai_engine=None) -> str:
    """
    Generates Institutional Geopolitical Black-Swan Flight-to-Safety Guard Report in Khmer.
    Details real-time Crisis Severity Index %, matched NLP keywords, and Semi-Automatic Buy confirmation instructions.
    """
    guard_info = scan_geopolitical_black_swan()
    
    severity = guard_info["crisis_severity_index"]
    keywords = ", ".join(guard_info["matched_keywords"]) if guard_info["matched_keywords"] else "None (Normal Operations)"
    headline = guard_info["headline_sample"]
    impact = guard_info["gold_impact"]
    rec = guard_info["recommendation"]
    
    status_emoji = "🚨 CRITICAL CRISIS DETECTED" if guard_info["crisis_detected"] else "🟢 NORMAL GEOPOLITICAL CONDITIONS"
    
    ai_analysis = ""
    if ai_engine:
        prompt = (
            f"You are Supreme Head of Quantitative Strategy for Apex Institutional Fund.\n"
            f"Provide a 2-3 sentence Khmer Crisis Response Assessment based on:\n"
            f"Geopolitical Crisis Severity Index: {severity:.1f}%\n"
            f"Matched Crisis Keywords: {keywords}\n"
            f"Sample Headline: {headline}\n"
            f"Estimated Gold Price Impact: {impact}\n"
            f"Status: {status_emoji}\n\n"
            f"Explain how Real-Time NLP detection of geopolitical crises allows VIP investors to front-run the flight-to-safety capital flow into PAXG Gold in Khmer."
        )
        try:
            ai_analysis = ai_engine.analyze_opportunity(prompt)
        except Exception as e:
            ai_analysis = f"សន្ទស្សន៍ហានិភ័យភូមិសាស្ត្រនយោបាយ {severity:.1f}% បញ្ជាក់ថាយន្តការ Flight-to-Safety កំពុងការពារទ្រព្យសកម្ម និងប្រមូលទិញមាស PAXG មុនពេលទីផ្សារមាន Panic Sell។"
    else:
        ai_analysis = f"សន្ទស្សន៍ហានិភ័យភូមិសាស្ត្រនយោបាយ {severity:.1f}% បញ្ជាក់ថាយន្តការ Flight-to-Safety កំពុងការពារទ្រព្យសកម្ម និងប្រមូលទិញមាស PAXG មុនពេលទីផ្សារមាន Panic Sell។"

    if user_lang == 'khmer':
        report = (
            f"🛡️ **APEX SUPER BRAIN — GEOPOLITICAL BLACK-SWAN GUARD** 🛡️\n"
            f"*(ប្រព័ន្ធការពារសង្គ្រាម & វិបត្តិ Real-Time NLP Gold Accumulation)*\n\n"
            f"📊 **GEOPOLITICAL CRISIS SEVERITY INDEX:** `{severity:.1f}%`\n"
            f"🏛️ **STATUS:** {status_emoji}\n"
            f"🔍 **MATCHED NLP KEYWORDS:** `{keywords}`\n"
            f"📰 **SAMPLE HEADLINE:** _{headline}_\n\n"
            f"🌐 **ESTIMATED GOLD IMPACT:** `{impact}`\n"
            f"💡 **AI RECOMMENDATION:** {rec}\n\n"
            f"💡 **AI QUANTITATIVE ASSESSMENT (របាយការណ៍ស្ថាប័ន):**\n"
            f"{ai_analysis}\n\n"
            f"⚡ _ប្រើបញ្ជា `/scalp PAXGUSDT 100 1.5 <PIN>` ដើម្បីទិញមាសស្ទាក់មុនពេលមានវិបត្តិ!_"
        )
    else:
        report = (
            f"🛡️ **APEX SUPER BRAIN — GEOPOLITICAL BLACK-SWAN GUARD** 🛡️\n\n"
            f"📊 **GEOPOLITICAL CRISIS SEVERITY INDEX:** `{severity:.1f}%`\n"
            f"🏛️ **STATUS:** {status_emoji}\n"
            f"🔍 **MATCHED NLP KEYWORDS:** `{keywords}`\n"
            f"📰 **SAMPLE HEADLINE:** _{headline}_\n\n"
            f"🌐 **ESTIMATED GOLD IMPACT:** `{impact}`\n"
            f"💡 **AI RECOMMENDATION:** {rec}\n\n"
            f"💡 **AI QUANTITATIVE ASSESSMENT:**\n"
            f"{ai_analysis}\n\n"
            f"⚡ _Use `/scalp PAXGUSDT 100 1.5 <PIN>` to execute flight-to-safety gold buys!_"
        )

    return report
