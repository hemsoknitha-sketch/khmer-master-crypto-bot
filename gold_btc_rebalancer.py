import requests
import json
import time
import asyncio

def fetch_gold_btc_ratio() -> dict:
    """
    Fetches real-time Binance BTC/USDT and PAXG/USDT prices.
    Calculates exact BTC/Gold Ratio (Ounces of Physical Gold required to purchase 1 Bitcoin).
    """
    ratio_data = {
        "btc_price": 64500.00,
        "paxg_price": 2425.00,
        "btc_gold_ratio": 26.60, # 26.6 oz Gold per 1 BTC
        "target_range": "20.0x - 35.0x",
        "allocation_btc_pct": 50.0,
        "allocation_gold_pct": 50.0,
        "rebalance_action": "🟢 HOLD OPTIMAL 50/50 BALANCED ALLOCATION",
        "status": "success"
    }
    
    try:
        # Fetch BTC/USDT
        url_btc = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        res_btc = requests.get(url_btc, timeout=5)
        if res_btc.status_code == 200:
            ratio_data["btc_price"] = float(res_btc.json().get("price", 64500.0))
            
        # Fetch PAXG/USDT
        url_paxg = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        res_paxg = requests.get(url_paxg, timeout=5)
        if res_paxg.status_code == 200:
            ratio_data["paxg_price"] = float(res_paxg.json().get("price", 2425.0))
            
        if ratio_data["paxg_price"] > 0:
            ratio = round(ratio_data["btc_price"] / ratio_data["paxg_price"], 2)
            ratio_data["btc_gold_ratio"] = ratio
            
            # Evaluate Rebalancing Boundaries
            if ratio > 35.0:
                ratio_data["allocation_btc_pct"] = 35.0
                ratio_data["allocation_gold_pct"] = 65.0
                ratio_data["rebalance_action"] = "🚨 BTC OVERVALUED (>35x): Trim BTC -> Accumulate PAXG Gold!"
            elif ratio < 20.0:
                ratio_data["allocation_btc_pct"] = 65.0
                ratio_data["allocation_gold_pct"] = 35.0
                ratio_data["rebalance_action"] = "🚀 BTC UNDERVALUED (<20x): Trim PAXG Gold -> Accumulate BTC!"
            else:
                ratio_data["allocation_btc_pct"] = 50.0
                ratio_data["allocation_gold_pct"] = 50.0
                ratio_data["rebalance_action"] = "🟢 OPTIMAL 50/50 BALANCED HOLD RANGE (20x - 35x)"
    except Exception as e:
        print(f"⚠️ [GOLD BTC REBALANCER] Fetch error: {e}")

    return ratio_data

def generate_rebalancer_report(user_lang: str = "khmer", ai_engine=None) -> str:
    """
    Generates Institutional Gold / BTC Multi-Asset Dynamic Rebalancer Report in Khmer.
    Details real-time BTC/Gold Ratio, target portfolio allocation %, and rebalance signals.
    """
    ratio_info = fetch_gold_btc_ratio()
    
    btc = ratio_info["btc_price"]
    paxg = ratio_info["paxg_price"]
    ratio = ratio_info["btc_gold_ratio"]
    action = ratio_info["rebalance_action"]
    alloc_btc = ratio_info["allocation_btc_pct"]
    alloc_gold = ratio_info["allocation_gold_pct"]
    
    ai_analysis = ""
    if ai_engine:
        prompt = (
            f"You are Supreme Head of Quantitative Strategy for Apex Institutional Fund.\n"
            f"Provide a 2-3 sentence Khmer Multi-Asset Rebalancing Strategy Report based on:\n"
            f"Bitcoin (BTC/USDT): ${btc:,.2f}\n"
            f"Physical Gold (PAXG/USDT): ${paxg:,.2f}\n"
            f"BTC/Gold Ratio: {ratio:.2f}x (Ounces of Gold per 1 BTC)\n"
            f"Optimal Allocation: {alloc_btc:.0f}% BTC / {alloc_gold:.0f}% PAXG Gold\n"
            f"Rebalance Action: {action}\n\n"
            f"Explain how rebalancing between Digital Gold (BTC) and Physical Gold (PAXG) based on BTC/Gold ratio preserves multi-generational wealth in Khmer."
        )
        try:
            ai_analysis = ai_engine.analyze_opportunity(prompt)
        except Exception as e:
            ai_analysis = f"ផលធៀប BTC/Gold Ratio គឺ {ratio:.2f}x (អោនស៍មាសក្នុង ១ BTC)។ ការបែងចែកទុន {alloc_btc:.0f}% BTC និង {alloc_gold:.0f}% PAXG ធានានូវការកើនឡើងនៃដើមទុនជាពហុគុណទាំងមាស និង Bitcoin!"
    else:
        ai_analysis = f"ផលធៀប BTC/Gold Ratio គឺ {ratio:.2f}x (អោនស៍មាសក្នុង ១ BTC)។ ការបែងចែកទុន {alloc_btc:.0f}% BTC និង {alloc_gold:.0f}% PAXG ធានានូវការកើនឡើងនៃដើមទុនជាពហុគុណទាំងមាស និង Bitcoin!"

    if user_lang == 'khmer':
        report = (
            f"💎 **APEX SUPER BRAIN — GOLD / BTC DYNAMIC REBALANCER** 💎\n"
            f"*(ការបែងចែកទុនរវាងមាសរូបវន្ត PAXG និងមាសឌីជីថល BTC)*\n\n"
            f"🪙 **Bitcoin (BTC/USDT):** `${btc:,.2f}`\n"
            f"🏆 **Physical Gold (PAXG/USDT):** `${paxg:,.2f}`\n"
            f"📐 **BTC / Gold Ratio:** `{ratio:.2f}x` *(អោនស៍មាសក្នុង 1 BTC)*\n\n"
            f"📊 **OPTIMAL PORTFOLIO ALLOCATION:**\n"
            f" 🟡 **Bitcoin Weight:** `{alloc_btc:.0f}%`\n"
            f" 🟡 **Physical Gold Weight:** `{alloc_gold:.0f}%`\n"
            f" 🎯 **TARGET RANGE:** `20.0x - 35.0x`\n"
            f" ⚡ **REBALANCE ACTION:** `{action}`\n\n"
            f"💡 **AI QUANTITATIVE REPORT (របាយការណ៍ស្ថាប័ន):**\n"
            f"{ai_analysis}\n\n"
            f"⚡ _វាយបញ្ជា `/gold_btc_rebalance` ឬ `/scalp PAXGUSDT 100 1.5 <PIN>` ដើម្បី Rebalance ទ្រព្យសកម្ម!_"
        )
    else:
        report = (
            f"💎 **APEX SUPER BRAIN — GOLD / BTC DYNAMIC REBALANCER** 💎\n\n"
            f"🪙 **Bitcoin (BTC/USDT):** `${btc:,.2f}`\n"
            f"🏆 **Physical Gold (PAXG/USDT):** `${paxg:,.2f}`\n"
            f"📐 **BTC / Gold Ratio:** `{ratio:.2f}x` *(Ounces per 1 BTC)*\n\n"
            f"📊 **OPTIMAL PORTFOLIO ALLOCATION:**\n"
            f" 🟡 **Bitcoin Weight:** `{alloc_btc:.0f}%`\n"
            f" 🟡 **Physical Gold Weight:** `{alloc_gold:.0f}%`\n"
            f" 🎯 **TARGET RANGE:** `20.0x - 35.0x`\n"
            f" ⚡ **REBALANCE ACTION:** `{action}`\n\n"
            f"💡 **AI QUANTITATIVE REPORT:**\n"
            f"{ai_analysis}\n\n"
            f"⚡ _Use `/gold_btc_rebalance` or `/scalp PAXGUSDT 100 1.5 <PIN>` to optimize your multi-asset portfolio!_"
        )

    return report
