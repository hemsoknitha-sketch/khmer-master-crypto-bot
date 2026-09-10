import sys
sys.path.append('.')
import sqlite3
import database as db

conn = db.get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("Tables:", tables)

for t in ['strategy_pnl_attribution', 'trade_history', 'trades', 'active_trades', 'closed_trades']:
    if t in tables:
        cursor.execute(f"SELECT count(*) FROM {t}")
        print(f"{t} count:", cursor.fetchone()[0])
conn.close()
