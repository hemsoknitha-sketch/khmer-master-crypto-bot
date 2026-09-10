import sys
sys.path.append('.')
import database as db

def test_summary(chat_id=859271875):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    # Ensure trade_history exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            symbol TEXT,
            side TEXT,
            entry_price REAL,
            exit_price REAL,
            qty REAL,
            entry_time TEXT,
            exit_time TEXT,
            pnl REAL,
            pnl_percent REAL,
            exit_reason TEXT
        )
    """)
    conn.commit()

    tot_pnl = 0.0
    tot_trades = 0
    wins = 0

    try:
        cursor.execute("""
            SELECT SUM(pnl), COUNT(*),
                   SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END)
            FROM trade_history
            WHERE chat_id = ? AND exit_time >= datetime('now', '-24 hours')
        """, (chat_id,))
        row = cursor.fetchone()
        if row and row[0] is not None:
            tot_pnl += float(row[0])
            tot_trades += int(row[1])
            wins += int(row[2] or 0)
    except Exception as e:
        print("trade_history query err:", e)

    try:
        cursor.execute("""
            SELECT SUM(net_profit_usd), COUNT(*)
            FROM user_flash_loan_trades
            WHERE chat_id = ? AND status = 'COMPLETED' AND created_at >= datetime('now', '-24 hours')
        """, (chat_id,))
        row = cursor.fetchone()
        if row and row[0] is not None:
            tot_pnl += float(row[0])
            tot_trades += int(row[1])
            wins += int(row[1])
    except Exception as e:
        print("user_flash_loan_trades query err:", e)

    try:
        cursor.execute("""
            SELECT SUM(total_pnl_usdt), SUM(win_count), SUM(loss_count)
            FROM strategy_pnl_attribution
            WHERE chat_id = ? AND last_updated >= datetime('now', '-24 hours')
        """, (chat_id,))
        row = cursor.fetchone()
        if row and row[0] is not None:
            tot_pnl += float(row[0])
            tot_trades += int(row[1] or 0) + int(row[2] or 0)
            wins += int(row[1] or 0)
    except Exception as e:
        print("strategy_pnl_attribution query err:", e)

    conn.close()

    win_rate = round((wins / tot_trades * 100.0), 1) if tot_trades > 0 else 100.0
    res = {
        "total_pnl": round(tot_pnl, 2),
        "total_trades": tot_trades,
        "wins": wins,
        "losses": tot_trades - wins,
        "win_rate": win_rate
    }
    print("Result:", res)
    return res

test_summary()
