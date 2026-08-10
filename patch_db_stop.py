import re

with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

funcs_to_add = '''
def deactivate_all_bots_by_symbol(chat_id: int, symbol: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    symbol = symbol.upper()
    
    # 1. Stop Infinity Grids
    cursor.execute("UPDATE infinity_grid_bots SET is_active = 0 WHERE chat_id = ? AND symbol = ?", (chat_id, symbol))
    # 2. Stop Scalpers
    cursor.execute("UPDATE ai_scalper SET is_active = 0 WHERE chat_id = ? AND symbol = ?", (chat_id, symbol))
    # 3. Stop Active Trades (Spot trailing stops)
    cursor.execute("DELETE FROM active_trades WHERE chat_id = ? AND symbol = ?", (chat_id, symbol))
    # 4. Stop Grid Bots
    cursor.execute("UPDATE grid_bots SET is_active = 0 WHERE chat_id = ? AND symbol = ?", (chat_id, symbol))
    # 5. Stop Shorts
    cursor.execute("DELETE FROM active_shorts WHERE chat_id = ? AND symbol = ?", (chat_id, symbol))
    
    conn.commit()
    conn.close()
'''

if 'deactivate_all_bots_by_symbol' not in content:
    with open('database.py', 'a', encoding='utf-8') as f:
        f.write(funcs_to_add)
    print("Added deactivate_all_bots_by_symbol to database.py")
else:
    print("Function already exists")
