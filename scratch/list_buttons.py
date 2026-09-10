import re
with open('bot_thread.py', 'r', encoding='utf-8') as f:
    code = f.read()
buttons = re.findall(r'callback_data=["\']([^"\']+)["\']', code)
print('Smart/trade/auto buttons:', [b for b in set(buttons) if any(k in b for k in ['trade', 'smart', 'turbo', 'hedge', 'arb', 'menu', 'balance', 'portfolio'])])
