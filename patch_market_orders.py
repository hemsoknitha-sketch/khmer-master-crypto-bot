import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. auto_trade (Line 326)
target1 = '''                                if sentiment == "BULLISH":
                                    result = trading_engine.place_market_buy(api_key, api_secret, symbol, qty)
                                    if result.get("status") == "FILLED":'''
replacement1 = '''                                if sentiment == "BULLISH":
                                    result = trading_engine.place_market_buy(api_key, api_secret, symbol, trade_amount)
                                    if result.get("status") == "FILLED":'''

# 2. smart_dca (Line 559)
target2 = '''                                    qty = buy_amount / current_price
                                    result = trading_engine.place_market_buy(api_key, api_secret, binance_symbol, qty)
                                    
                                    if result.get("status") == "FILLED":'''
replacement2 = '''                                    qty = buy_amount / current_price
                                    result = trading_engine.place_market_buy(api_key, api_secret, binance_symbol, buy_amount)
                                    
                                    if result.get("status") == "FILLED":'''

# 3. Sentiment Auto-Buy (Line 1822)
target3 = '''                                qty = trade_amount / current_price
                                result = trading_engine.place_market_buy(api_key, api_secret, binance_symbol, qty)
                                if result.get("status") == "FILLED":'''
replacement3 = '''                                qty = trade_amount / current_price
                                result = trading_engine.place_market_buy(api_key, api_secret, binance_symbol, trade_amount)
                                if result.get("status") == "FILLED":'''

# 4. ai_scalper_monitor Sell (Line 1323)
target4 = '''            if current_state == 'HOLDING':
                target_sell_price = entry_price * (1 + (profit_target_pct / 100.0))
                if current_price >= target_sell_price:
                    # SELL!
                    if keys:
                        # Paper trading simulated if set in engine, otherwise real market order
                        trading_engine.place_market_sell(keys[0], keys[1], symbol, amount)
                    
                    actual_profit = ((current_price - entry_price) / entry_price) * 100.0
                    msg = f"🏓 **AI SCALPER (SELL)** 🏓\\n\\n🪙 **{symbol}**\\n💵 លក់ចេញ: `${current_price:,.4f}`\\n🟩 ចំណេញ: `+{actual_profit:.2f}%`\\n\\n_Bot កំពុងរង់ចាំទិញចូលវិញនៅពេលវាធ្លាក់ចុះបន្តិច..._"
                    
                    try:
                        await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                    except: pass
                    
                    db.update_scalper_state(scalper_id, 'WAITING', current_price)'''
replacement4 = '''            if current_state == 'HOLDING':
                target_sell_price = entry_price * (1 + (profit_target_pct / 100.0))
                if current_price >= target_sell_price:
                    # SELL!
                    if keys:
                        # amount is in USDT. Calculate token quantity
                        qty_to_sell = round(amount / current_price, 4)
                        res = trading_engine.place_market_sell(keys[0], keys[1], symbol, qty_to_sell)
                        
                        if res.get("status") == "FILLED":
                            actual_profit = ((current_price - entry_price) / entry_price) * 100.0
                            msg = f"🏓 **AI SCALPER (SELL)** 🏓\\n\\n🪙 **{symbol}**\\n💵 លក់ចេញ: `${current_price:,.4f}`\\n🟩 ចំណេញ: `+{actual_profit:.2f}%`\\n\\n_Bot កំពុងរង់ចាំទិញចូលវិញនៅពេលវាធ្លាក់ចុះបន្តិច..._"
                            db.update_scalper_state(scalper_id, 'WAITING', current_price)
                        else:
                            error_msg = res.get('error', res.get('msg', 'Unknown Error'))
                            msg = f"🏓 **AI SCALPER (SELL FAILED)** ❌\\nបរាជ័យក្នុងការលក់ {symbol}: {error_msg}\\nBot នឹងព្យាយាមម្តងទៀតនៅជុំក្រោយ។"
                            
                        try:
                            await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                        except: pass'''


count = 0
if target1 in content:
    content = content.replace(target1, replacement1)
    count += 1
if target2 in content:
    content = content.replace(target2, replacement2)
    count += 1
if target3 in content:
    content = content.replace(target3, replacement3)
    count += 1
if target4 in content:
    content = content.replace(target4, replacement4)
    count += 1

with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Patched {count} locations in scheduler_tasks.py")
