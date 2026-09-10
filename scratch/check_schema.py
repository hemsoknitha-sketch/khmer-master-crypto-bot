import sys
sys.path.append('.')
import database as db

conn = db.get_db_connection()
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(trade_history)")
print("trade_history columns:", [c[1] for c in cursor.fetchall()])

cursor.execute("PRAGMA table_info(user_flash_loan_trades)")
print("user_flash_loan_trades columns:", [c[1] for c in cursor.fetchall()])

conn.close()
