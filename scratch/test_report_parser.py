import asyncio
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

import scheduler_tasks
import database as db

async def test_suite():
    print("Testing all engines and timeframes...")
    chat_id = 859271875

    mock_trade = {
        "id": "#10849204",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET / TRAIL_TP",
        "qty": "0.150 BTC",
        "entry_price": 65000.0,
        "exit_price": 66200.0,
        "time": "2026-09-11 10:30:00",
        "pnl": 180.0,
        "roi": 12.5,
        "commission": 1.20,
        "funding": 0.50,
        "net_pnl": 179.30,
        "engine": "turbo_hedge"
    }

    old_get_data = db.get_user_multi_timeframe_report_data
    def mock_data(cid, tf, eng):
        res = old_get_data(cid, tf, eng)
        res['recent_trades'] = [mock_trade]
        return res

    db.get_user_multi_timeframe_report_data = mock_data

    engines = [None, "turbo_hedge", "smart_x", "smart_trade", "smart_swap"]
    timeframes = ["daily", "monthly", "yearly", "lifetime"]

    for eng in engines:
        for tf in timeframes:
            msg, kb = await scheduler_tasks.build_executive_summary_report(chat_id, timeframe=tf, engine_filter=eng)
            without_code = re.sub(r"`[^`]*`", "", msg)
            underscores = [i for i, c in enumerate(without_code) if c == '_']
            asterisks = [i for i, c in enumerate(without_code) if c == '*']

            # Check parity
            u_odd = len(underscores) % 2 != 0
            a_odd = len(asterisks) % 2 != 0
            
            if u_odd or a_odd:
                print(f"[FAIL] eng={eng}, tf={tf} -> Underscores: {len(underscores)}, Asterisks: {len(asterisks)}")
                print(msg)
                sys.exit(1)
            else:
                print(f"[PASS] eng={eng or 'ALL'}, tf={tf} -> _ : {len(underscores)} (even), * : {len(asterisks)} (even)")

    print("\n>>> ALL REPORT CONFIGURATIONS PASSED MARKDOWN PARITY TEST! <<<")

if __name__ == "__main__":
    asyncio.run(test_suite())
