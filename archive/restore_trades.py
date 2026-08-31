import sqlite3

def restore_trades():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Get the trades deleted today
    cursor.execute('''
        SELECT chat_id, symbol, qty, entry_price, entry_time 
        FROM trade_history 
        WHERE exit_time LIKE '2026-07-30%' AND exit_reason = 'TRAILING_STOP'
    ''')
    deleted_trades = cursor.fetchall()

    for trade in deleted_trades:
        chat_id, symbol, qty, entry_price, entry_time = trade
        # insert back into active_trades
        cursor.execute('''
            INSERT INTO active_trades (chat_id, symbol, qty, buy_price, current_highest, stop_loss_pct, timestamp, initial_qty, scale_out_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (chat_id, symbol, qty, entry_price, entry_price, 5.0, entry_time, qty, 0))
        print(f"Restored {symbol}")

    # Delete them from trade_history so they don't show as closed
    cursor.execute('''
        DELETE FROM trade_history 
        WHERE exit_time LIKE '2026-07-30%' AND exit_reason = 'TRAILING_STOP'
    ''')
    
    conn.commit()
    conn.close()
    print(f"Successfully restored {len(deleted_trades)} trades to active_trades!")

if __name__ == "__main__":
    restore_trades()
