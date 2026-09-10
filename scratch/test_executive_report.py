import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scheduler_tasks import build_executive_summary_report

async def test_executive_report():
    print("Testing build_executive_summary_report(859271875)...")
    msg, kb = await build_executive_summary_report(859271875)
    assert msg is not None and len(msg) > 50
    assert kb is not None
    print("✅ Successfully generated executive report:")
    print(msg[:400])
    print("\n[ALL EXECUTIVE REPORT TESTS PASSED!]")

if __name__ == "__main__":
    asyncio.run(test_executive_report())
