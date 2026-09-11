import asyncio
import os
import sys

# Ensure cwd in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import database as db
import scheduler_tasks

async def test_report():
    test_chat_id = 859271875

    print("=== 1. Testing Daily 24H Report ===")
    msg_daily, kb_daily = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily")
    print(f"Length: {len(msg_daily)} chars")
    assert "APEX VIP 24H DAILY AUDIT" in msg_daily
    assert "Khmer Master Crypto" in msg_daily
    assert "APEX SUPER BRAIN AI" in msg_daily
    assert "ដំណើរការការពារហានិភ័យ & កើបចំណេញ ២៤/៧!" in msg_daily
    assert "/turbo_hedge" in msg_daily
    assert "/smart_x" in msg_daily
    assert "/smart_trade" in msg_daily
    assert "/smart_swap" in msg_daily
    assert "NET PROFIT" in msg_daily
    assert "24h Growth" in msg_daily
    print("  [PASS] Daily Report verified!")

    print("\n=== 2. Testing Monthly 30D Report ===")
    msg_monthly, kb_monthly = await scheduler_tasks.build_executive_summary_report(test_chat_id, "monthly")
    assert "APEX VIP 30D MONTHLY AUDIT" in msg_monthly
    assert "30d Growth" in msg_monthly
    print("  [PASS] Monthly Report verified!")

    print("\n=== 3. Testing Yearly 1Y Report ===")
    msg_yearly, kb_yearly = await scheduler_tasks.build_executive_summary_report(test_chat_id, "yearly")
    assert "APEX VIP 1Y YEARLY AUDIT" in msg_yearly
    assert "1y Growth" in msg_yearly
    print("  [PASS] Yearly Report verified!")

    print("\n=== 4. Testing Lifetime Report ===")
    msg_lifetime, kb_lifetime = await scheduler_tasks.build_executive_summary_report(test_chat_id, "lifetime")
    assert "APEX VIP LIFETIME AUDIT" in msg_lifetime
    assert "All-Time Growth" in msg_lifetime
    print("  [PASS] Lifetime Report verified!")

    print("\n=== 5. Testing Engine Filter (turbo_hedge) ===")
    msg_hedge, kb_hedge = await scheduler_tasks.build_executive_summary_report(test_chat_id, "daily", "turbo_hedge")
    assert "TURBO_HEDGE" in msg_hedge
    print("  [PASS] Engine Filter verified!")

    print("\n=== 6. Checking Line Width for Mobile Separator Fit ===")
    for line in msg_daily.split("\n"):
        if "━━━" in line or "───" in line or "┈┈┈" in line:
            assert len(line) <= 24, f"Separator line too long: {len(line)} chars: {line}"
    print("  [PASS] Separator width <= 24 chars strictly enforced!")

    print("\n=== 7. Sample Rendered Card Output ===")
    print(msg_daily)
    print("\n" + "=" * 50)
    print(">>> ALL 7 REPORT SUITE TESTS PASSED 100%! <<<")

if __name__ == "__main__":
    asyncio.run(test_report())
