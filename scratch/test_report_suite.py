import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import database as db
import scheduler_tasks

async def test_report():
    test_chat_id = 859271875

    print("=== 1. Testing Daily 24H Overview Report ===")
    msg_daily, kb_daily = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily")
    assert "APEX VIP 24H DAILY AUDIT" in msg_daily
    assert "Angkor Quant" in msg_daily
    assert "Binance Spot/Fut + Capital.com + GTC PAMM" in msg_daily
    assert "BINANCE CRYPTO" in msg_daily
    assert "CAPITAL.COM TRADFI" in msg_daily
    assert "GTC PAMM / MT5" in msg_daily
    assert "ដំណើរការការពារហានិភ័យ & កើបចំណេញ ២៤/៧!" in msg_daily
    assert "NET PROFIT" in msg_daily
    assert "24h Growth" in msg_daily
    # Check button active indicators
    daily_btn_text = kb_daily.inline_keyboard[0][0].text
    assert "✅ 24H Daily" in daily_btn_text
    print("  [PASS] Daily Report & Active Indicators verified!")

    print("\n=== 2. Testing Dedicated Turbo Hedge Audit ===")
    msg_hedge, kb_hedge = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "turbo_hedge")
    assert "APEX VIP AUDIT — 🚀 TURBO HEDGE" in msg_hedge
    assert "Dual-Side Delta-Neutral HFT" in msg_hedge
    assert "ISOLATED" in msg_hedge
    assert "HEDGE MODE (Long + Short)" in msg_hedge
    assert "+0.12% Net Fee Offset" in msg_hedge
    # Check that Turbo Hedge button has checkmark
    turbo_btn = kb_hedge.inline_keyboard[2][1].text
    assert "✅ Turbo Hedge" in turbo_btn
    print("  [PASS] Dedicated Turbo Hedge Audit verified!")

    print("\n=== 3. Testing Dedicated SmartX Audit ===")
    msg_smartx, kb_smartx = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "smart_x")
    assert "APEX VIP AUDIT — 🥇 SMARTX GOLD QUANT" in msg_smartx
    smartx_btn = kb_smartx.inline_keyboard[3][0].text
    assert "✅ SmartX" in smartx_btn
    print("  [PASS] Dedicated SmartX Audit verified!")

    print("\n=== 4. Testing Dedicated Capital.com Audit ===")
    msg_cap, kb_cap = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "capital")
    assert "APEX VIP AUDIT — 🏛️ CAPITAL.COM TRADFI" in msg_cap
    cap_btn = kb_cap.inline_keyboard[5][0].text
    assert "✅ TradFi Capital" in cap_btn
    print("  [PASS] Dedicated Capital.com Audit verified!")

    print("\n=== 5. Testing Dedicated GTC PAMM Audit ===")
    msg_pamm, kb_pamm = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "pamm")
    assert "APEX VIP AUDIT — 🏦 GTC PAMM / MT5 MASTER FUND" in msg_pamm
    pamm_btn = kb_pamm.inline_keyboard[5][1].text
    assert "✅ GTC PAMM" in pamm_btn
    print("  [PASS] Dedicated GTC PAMM Audit verified!")

    print("\n🎉 ALL 5 REPORT SUITE AUDITS PASSED WITH FLYING COLORS!")

if __name__ == "__main__":
    asyncio.run(test_report())
