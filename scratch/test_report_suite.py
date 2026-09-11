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
    assert "Khmer Master Crypto" in msg_daily
    assert "APEX SUPER BRAIN AI" in msg_daily
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
    turbo_btn = kb_hedge.inline_keyboard[2][0].text
    assert "✅ Turbo Hedge" in turbo_btn
    print("  [PASS] Dedicated Turbo Hedge Audit verified!")

    print("\n=== 3. Testing Dedicated SmartX Audit ===")
    msg_smartx, kb_smartx = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "smart_x")
    assert "APEX VIP AUDIT — 🧠 SMARTX AI" in msg_smartx
    assert "SweetSpot High-Frequency" in msg_smartx
    assert "12 Wall Street ML" in msg_smartx
    smartx_btn = kb_smartx.inline_keyboard[2][1].text
    assert "✅ SmartX" in smartx_btn
    print("  [PASS] Dedicated SmartX Audit verified!")

    print("\n=== 4. Testing Dedicated Smart Trade Audit ===")
    msg_trade, kb_trade = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "smart_trade")
    assert "APEX VIP AUDIT — 📊 SMART TRADE" in msg_trade
    assert "Min $10.50 (Zero -1013)" in msg_trade
    trade_btn = kb_trade.inline_keyboard[3][1].text
    assert "✅ Smart Trade" in trade_btn
    print("  [PASS] Dedicated Smart Trade Audit verified!")

    print("\n=== 5. Testing Dedicated Smart Swap Audit ===")
    msg_swap, kb_swap = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "smart_swap")
    assert "APEX VIP AUDIT — ⚡ SMART SWAP" in msg_swap
    assert "Multi-Chain DEX & MEV Shield" in msg_swap
    swap_btn = kb_swap.inline_keyboard[3][0].text
    assert "✅ Smart Swap" in swap_btn
    print("  [PASS] Dedicated Smart Swap Audit verified!")

    print("\n=== 6. Checking Line Width for Mobile Separator Fit ===")
    for report_msg in [msg_daily, msg_hedge, msg_smartx, msg_trade, msg_swap]:
        for line in report_msg.split("\n"):
            if "━━━" in line or "───" in line or "┈┈┈" in line:
                assert len(line) <= 24, f"Separator line too long: {len(line)} chars: {line}"
    print("  [PASS] Separator width <= 24 chars strictly enforced across all engine views!")

    print("\n=== 7. Sample Rendered Turbo Hedge Card Output ===")
    print(msg_hedge)
    print("\n" + "=" * 50)
    print(">>> ALL 7 REPORT SUITE TESTS PASSED 100%! <<<")

if __name__ == "__main__":
    asyncio.run(test_report())
