import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

target1 = '''            if amt_per_layer <= 0 or step_pct <= 0:
                await update.message.reply_text("⚠️ ទំហំទិញ/លក់ និង ភាគរយ ត្រូវតែធំជាង ០")
                return
                
            if max_inv < 10.0:
                await update.message.reply_text("⚠️ ដើមទុនអតិបរមាត្រូវតែធំជាង ឬស្មើ $10")
                return'''

replacement1 = '''            if amt_per_layer <= 0 or step_pct <= 0:
                await update.message.reply_text("⚠️ ទំហំទិញ/លក់ និង ភាគរយ ត្រូវតែធំជាង ០")
                return
                
            from trading_engine import PAPER_TRADING
            if not PAPER_TRADING and amt_per_layer < 5.0:
                await update.message.reply_text("⚠️ [Binance Rule] ទំហំទិញលក់ក្នុង១ជាន់ ត្រូវតែយ៉ាងតិច $5.0 ដើម្បីអាចទិញបាន (MIN_NOTIONAL)!")
                return
                
            if max_inv < 10.0:
                await update.message.reply_text("⚠️ ដើមទុនអតិបរមាត្រូវតែធំជាង ឬស្មើ $10")
                return'''

target2 = '''            if amount < 10:
                await update.message.reply_text("⚠️ ទំហំវិនិយោគត្រូវតែចាប់ពី $10 ឡើងទៅ")
                return'''

replacement2 = '''            from trading_engine import PAPER_TRADING
            if not PAPER_TRADING and amount < 5.0:
                await update.message.reply_text("⚠️ [Binance Rule] ទំហំវិនិយោគត្រូវតែយ៉ាងតិច $5.0 (MIN_NOTIONAL)!")
                return
                
            if amount < 10:
                await update.message.reply_text("⚠️ ទំហំវិនិយោគត្រូវតែចាប់ពី $10 ឡើងទៅ")
                return'''

if 'amt_per_layer < 5.0' not in content:
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched bot_thread.py for min notional")
else:
    print("Already patched")
