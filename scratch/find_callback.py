with open('bot_thread.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'data == "btn_balance_refresh"' in line or 'data == "btn_menu_portfolio"' in line:
            print(f"{i+1}: {line.strip()}")
