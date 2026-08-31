import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            try:
                import market_data
                volatile_coins = market_data.fetch_top_volatile_coins(limit=1, min_change_pct=5.0)
                
                if not volatile_coins:
                    await update.message.reply_text("មិនមានកាក់ណាដែលកំពុងប្រែប្រួលខ្លាំងគួរឲ្យកត់សម្គាល់នៅពេលនេះទេ។")
                    return
                    
                coin = volatile_coins[0]
                symbol = coin['symbol']'''

replacement = '''            try:
                import market_data
                import random
                # Get top 10 volatile coins and pick one randomly so it changes on each /scan
                volatile_coins = market_data.fetch_top_volatile_coins(limit=10, min_change_pct=5.0)
                
                if not volatile_coins:
                    await update.message.reply_text("មិនមានកាក់ណាដែលកំពុងប្រែប្រួលខ្លាំងគួរឲ្យកត់សម្គាល់នៅពេលនេះទេ។")
                    return
                    
                coin = random.choice(volatile_coins)
                symbol = coin['symbol']'''

if 'import random' not in target and 'random.choice' not in content:
    content = content.replace(target, replacement)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched bot_thread.py scan_command")
else:
    print("Already patched or target not found")
