import re

with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

funcs_to_add = '''
def get_active_infinity_grids_by_user(chat_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, symbol, amount_per_layer, step_pct, max_investment, current_investment, last_price FROM infinity_grid_bots WHERE chat_id = ? AND is_active = 1", (chat_id,))
    res = cursor.fetchall()
    conn.close()
    return res

def get_active_scalpers_by_user(chat_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, symbol, invest_amount, target_pct, stop_loss_pct, current_position, entry_price FROM ai_scalper WHERE chat_id = ? AND is_active = 1", (chat_id,))
    res = cursor.fetchall()
    conn.close()
    return res
'''

if 'get_active_infinity_grids_by_user' not in content:
    with open('database.py', 'a', encoding='utf-8') as f:
        f.write(funcs_to_add)
    print("Added user-specific getters to database.py")
else:
    print("Getters already exist")
