import sys

filename = "database.py"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert the CREATE TABLE statement
target_str = "CREATE TABLE IF NOT EXISTS compound_grids ("
insert_idx = content.find(target_str)

if insert_idx == -1:
    print("Could not find insertion point for table schema")
    sys.exit(1)

table_schema = """CREATE TABLE IF NOT EXISTS strategy_pnl_attribution (
            chat_id INTEGER,
            strategy_name TEXT,
            total_pnl_usdt REAL DEFAULT 0.0,
            win_count INTEGER DEFAULT 0,
            loss_count INTEGER DEFAULT 0,
            allocation_pct REAL DEFAULT 20.0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (chat_id, strategy_name)
        )
    ''')
    
    cursor.execute('''
        """

new_content = content[:insert_idx] + table_schema + content[insert_idx:]

# 2. Append the new functions
new_functions = """

def update_strategy_pnl(chat_id: int, strategy_name: str, pnl_usdt: float):
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT total_pnl_usdt, win_count, loss_count FROM strategy_pnl_attribution WHERE chat_id = ? AND strategy_name = ?", (chat_id, strategy_name))
        row = cursor.fetchone()
        
        is_win = 1 if pnl_usdt > 0 else 0
        is_loss = 1 if pnl_usdt < 0 else 0
        
        if row:
            total_pnl = row[0] + pnl_usdt
            win_count = row[1] + is_win
            loss_count = row[2] + is_loss
            cursor.execute('''
                UPDATE strategy_pnl_attribution 
                SET total_pnl_usdt = ?, win_count = ?, loss_count = ?, last_updated = CURRENT_TIMESTAMP
                WHERE chat_id = ? AND strategy_name = ?
            ''', (total_pnl, win_count, loss_count, chat_id, strategy_name))
        else:
            cursor.execute('''
                INSERT INTO strategy_pnl_attribution (chat_id, strategy_name, total_pnl_usdt, win_count, loss_count)
                VALUES (?, ?, ?, ?, ?)
            ''', (chat_id, strategy_name, pnl_usdt, is_win, is_loss))
        conn.commit()
    except Exception as e:
        print(f"Error update_strategy_pnl: {e}")
    finally:
        conn.close()

def get_strategy_allocation(chat_id: int, strategy_name: str) -> float:
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    cursor = conn.cursor()
    alloc = 20.0 # Default
    try:
        cursor.execute("SELECT allocation_pct FROM strategy_pnl_attribution WHERE chat_id = ? AND strategy_name = ?", (chat_id, strategy_name))
        row = cursor.fetchone()
        if row:
            alloc = row[0]
        else:
            # Initialize with default if not found
            cursor.execute('''
                INSERT OR IGNORE INTO strategy_pnl_attribution (chat_id, strategy_name, allocation_pct)
                VALUES (?, ?, ?)
            ''', (chat_id, strategy_name, alloc))
            conn.commit()
    except Exception as e:
        print(f"Error get_strategy_allocation: {e}")
    finally:
        conn.close()
    return alloc

def set_strategy_allocation(chat_id: int, strategy_name: str, alloc_pct: float):
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE strategy_pnl_attribution 
            SET allocation_pct = ?, last_updated = CURRENT_TIMESTAMP
            WHERE chat_id = ? AND strategy_name = ?
        ''', (alloc_pct, chat_id, strategy_name))
        
        # if row didn't exist, insert it
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO strategy_pnl_attribution (chat_id, strategy_name, allocation_pct)
                VALUES (?, ?, ?)
            ''', (chat_id, strategy_name, alloc_pct))
            
        conn.commit()
    except Exception as e:
        print(f"Error set_strategy_allocation: {e}")
    finally:
        conn.close()

def get_all_strategy_pnls(chat_id: int):
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    cursor = conn.cursor()
    res = []
    try:
        cursor.execute("SELECT strategy_name, total_pnl_usdt, win_count, loss_count, allocation_pct FROM strategy_pnl_attribution WHERE chat_id = ?", (chat_id,))
        res = cursor.fetchall()
    except Exception as e:
        print(f"Error get_all_strategy_pnls: {e}")
    finally:
        conn.close()
    return res
"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(new_content)
    f.write(new_functions)

print("Successfully patched database.py for PnL Attribution")
