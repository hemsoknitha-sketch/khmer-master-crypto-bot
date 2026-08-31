import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ai_scalper_monitor (around line 1323)
target_scalper = '''                    if current_price >= sell_target:
                        # Take Profit
                        trading_engine.place_market_sell(keys[0], keys[1], symbol, amount)
                        db.deactivate_scalper(scalper_id)
                        
                        msg = f"🏓 **AI SCALPER (TAKE PROFIT)** ⚡\\n✅ លក់យកចំណេញសម្រាប់ {symbol} បានសម្រេច!\\n💵 តម្លៃទិញ: `${entry_price:,.4f}`\\n💰 តម្លៃលក់: `${current_price:,.4f}`\\n\\n_Bot បានបញ្ចប់ជុំនេះដោយជោគជ័យ!_"
                        try:
                            await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                        except: pass
                        print(f"⚡ SCALPER TP: {symbol} for {chat_id}")'''

replacement_scalper = '''                    if current_price >= sell_target:
                        # Take Profit
                        # amount is in USDT. Calculate quantity of tokens to sell
                        qty_to_sell = round(amount / current_price, 4)
                        res = trading_engine.place_market_sell(keys[0], keys[1], symbol, qty_to_sell)
                        
                        if res.get("status") == "FILLED":
                            db.deactivate_scalper(scalper_id)
                            msg = f"🏓 **AI SCALPER (TAKE PROFIT)** ⚡\\n✅ លក់យកចំណេញសម្រាប់ {symbol} បានសម្រេច!\\n💵 តម្លៃទិញ: `${entry_price:,.4f}`\\n💰 តម្លៃលក់: `${current_price:,.4f}`\\n\\n_Bot បានបញ្ចប់ជុំនេះដោយជោគជ័យ!_"
                        else:
                            error_msg = res.get('error', res.get('msg', 'Unknown Error'))
                            msg = f"🏓 **AI SCALPER (TAKE PROFIT FAILED)** ❌\\nបរាជ័យក្នុងការលក់ {symbol}: {error_msg}\\nBot នឹងព្យាយាមម្តងទៀតនៅជុំក្រោយ។"
                            
                        try:
                            await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                        except: pass
                        print(f"⚡ SCALPER TP: {symbol} for {chat_id} - Status: {res.get('status')}")'''

# Fix infinity_grid_monitor Sell (around line 1383)
target_grid_sell = '''            if current_price >= sell_target:
                # Sell condition met
                res = trading_engine.place_market_sell(api_key, api_secret, symbol, amount_per_layer)
                
                new_inv = max(0.0, current_investment - amount_per_layer)
                db.update_infinity_grid_state(grid_id, new_inv, current_price)
                
                msg = f"🕸️ **INFINITY GRID (SELL)** ⚡\\n✅ លក់យកចំណេញ 1 ជាន់សម្រាប់ {symbol}!\\n💵 តម្លៃលក់: `${current_price:,.4f}`\\n\\n_Bot រង់ចាំទិញចូលជាន់បន្ទាប់ពេលតម្លៃធ្លាក់ចុះ!_"
                try:
                    await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                except: pass
                print(f"⚡ INFINITY SELL: {symbol} at {current_price} for {chat_id}")'''

replacement_grid_sell = '''            if current_price >= sell_target:
                # Sell condition met
                # amount_per_layer is in USDT. Calculate quantity to sell
                qty_to_sell = round(amount_per_layer / current_price, 4)
                res = trading_engine.place_market_sell(api_key, api_secret, symbol, qty_to_sell)
                
                if res.get("status") == "FILLED":
                    new_inv = max(0.0, current_investment - amount_per_layer)
                    db.update_infinity_grid_state(grid_id, new_inv, current_price)
                    msg = f"🕸️ **INFINITY GRID (SELL)** ⚡\\n✅ លក់យកចំណេញ 1 ជាន់សម្រាប់ {symbol}!\\n💵 តម្លៃលក់: `${current_price:,.4f}`\\n\\n_Bot រង់ចាំទិញចូលជាន់បន្ទាប់ពេលតម្លៃធ្លាក់ចុះ!_"
                else:
                    error_msg = res.get('error', res.get('msg', 'Unknown Error'))
                    msg = f"🕸️ **INFINITY GRID (SELL FAILED)** ❌\\nបរាជ័យក្នុងការលក់ {symbol}: {error_msg}"
                
                try:
                    await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                except: pass
                print(f"⚡ INFINITY SELL: {symbol} at {current_price} for {chat_id} - Status: {res.get('status')}")'''

# Fix infinity_grid_monitor Buy (around line 1394)
target_grid_buy = '''            elif current_price <= buy_target:
                # Buy condition met
                if current_investment + amount_per_layer <= max_investment:
                    res = trading_engine.place_market_buy(api_key, api_secret, symbol, amount_per_layer)
                    
                    new_inv = current_investment + amount_per_layer
                    db.update_infinity_grid_state(grid_id, new_inv, current_price)
                    
                    msg = f"🕸️ **INFINITY GRID (BUY)** ⚡\\nទិញចូល 1 ជាន់សម្រាប់ {symbol}!\\n💵 តម្លៃទិញ: `${current_price:,.4f}`\\n\\n_Bot រង់ចាំលក់យកចំណេញពេលតម្លៃឡើងទៅវិញ!_"
                    try:
                        await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                    except: pass
                    print(f"⚡ INFINITY BUY: {symbol} at {current_price} for {chat_id}")'''

replacement_grid_buy = '''            elif current_price <= buy_target:
                # Buy condition met
                if current_investment + amount_per_layer <= max_investment:
                    res = trading_engine.place_market_buy(api_key, api_secret, symbol, amount_per_layer)
                    
                    if res.get("status") == "FILLED":
                        new_inv = current_investment + amount_per_layer
                        db.update_infinity_grid_state(grid_id, new_inv, current_price)
                        msg = f"🕸️ **INFINITY GRID (BUY)** ⚡\\nទិញចូល 1 ជាន់សម្រាប់ {symbol}!\\n💵 តម្លៃទិញ: `${current_price:,.4f}`\\n\\n_Bot រង់ចាំលក់យកចំណេញពេលតម្លៃឡើងទៅវិញ!_"
                    else:
                        error_msg = res.get('error', res.get('msg', 'Unknown Error'))
                        msg = f"🕸️ **INFINITY GRID (BUY FAILED)** ❌\\nបរាជ័យក្នុងការទិញ {symbol}: {error_msg}"
                    
                    try:
                        await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                    except: pass
                    print(f"⚡ INFINITY BUY: {symbol} at {current_price} for {chat_id} - Status: {res.get('status')}")'''


if 'qty_to_sell = round(amount' not in content:
    content = content.replace(target_scalper, replacement_scalper)
    content = content.replace(target_grid_sell, replacement_grid_sell)
    content = content.replace(target_grid_buy, replacement_grid_buy)
    
    with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched scheduler_tasks.py bugs")
else:
    print("Already patched")
