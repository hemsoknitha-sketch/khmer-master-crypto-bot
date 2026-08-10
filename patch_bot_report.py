import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix infinity_grid_command
target_grid = '''            # Initially buy the first layer
            keys = db.get_user_api(chat_id)
            if keys:
                import trading_engine
                trading_engine.place_market_buy(keys[0], keys[1], symbol, amt_per_layer)
                
            db.add_infinity_grid(chat_id, symbol, amt_per_layer, step_pct, max_inv, entry_price)
            
            msg = f"✅ **Infinity Grid បានបើកដំណើរការ!** 🕸️\\n\\n🪙 កាក់: **{symbol}**\\n💵 លុយទិញ/លក់១ជាន់: **${amt_per_layer}**\\n🎯 គម្លាតសំណាញ់: **{step_pct}%**\\n💰 ដើមទុនអតិបរមា: **${max_inv}**\\n\\n_Bot នឹងប្រមូលចំណេញគ្មានដែនកំណត់ 24/7!_"'''

replacement_grid = '''            # Initially buy the first layer
            trade_status = "⚠️ មិនមាន API សម្រាប់ធ្វើការទិញទេ (Demo Mode)"
            keys = db.get_user_api(chat_id)
            if keys:
                import trading_engine
                res = trading_engine.place_market_buy(keys[0], keys[1], symbol, amt_per_layer)
                if res.get("status") == "FILLED":
                    trade_status = f"✅ **អនុម័តដោយ Binance:** បានទិញ {res.get('executedQty')} {symbol} រួចរាល់!"
                else:
                    trade_status = f"❌ **បរាជ័យ:** {res.get('error', 'Unknown Error')} (Bot នៅតែរត់ និងរង់ចាំទិញនៅជុំក្រោយ)"
                
            db.add_infinity_grid(chat_id, symbol, amt_per_layer, step_pct, max_inv, entry_price)
            
            msg = f"✅ **Infinity Grid បានបើកដំណើរការ!** 🕸️\\n\\n🪙 កាក់: **{symbol}**\\n💵 លុយទិញ/លក់១ជាន់: **${amt_per_layer}**\\n🎯 គម្លាតសំណាញ់: **{step_pct}%**\\n💰 ដើមទុនអតិបរមា: **${max_inv}**\\n\\n{trade_status}\\n\\n_Bot នឹងប្រមូលចំណេញគ្មានដែនកំណត់ 24/7!_"'''

# Fix scalp_command
target_scalp = '''            # Initially buy the asset
            keys = db.get_user_api(chat_id)
            if keys:
                import trading_engine
                trading_engine.place_market_buy(keys[0], keys[1], symbol, amount)
                
            db.add_scalper(chat_id, symbol, amount, profit_tgt, entry_price)
            
            msg = f"✅ **AI Scalper បានបើកដំណើរការ!** 🏓\\n\\n🪙 កាក់: **{symbol}**\\n💵 ទំហំលុយ: **${amount}**\\n🎯 គោលដៅចំណេញ (Take Profit): **{profit_tgt}%**\\n\\n_Bot នឹងទិញលក់វិលជុំយកចំណេញដោយស្វ័យប្រវត្តិ!_"'''

replacement_scalp = '''            # Initially buy the asset
            trade_status = "⚠️ មិនមាន API សម្រាប់ធ្វើការទិញទេ (Demo Mode)"
            keys = db.get_user_api(chat_id)
            if keys:
                import trading_engine
                res = trading_engine.place_market_buy(keys[0], keys[1], symbol, amount)
                if res.get("status") == "FILLED":
                    trade_status = f"✅ **អនុម័តដោយ Binance:** បានទិញ {res.get('executedQty')} {symbol} រួចរាល់!"
                else:
                    trade_status = f"❌ **បរាជ័យ:** {res.get('error', 'Unknown Error')} (Bot នៅតែរត់ និងរង់ចាំតម្លៃល្អ)"
                
            db.add_scalper(chat_id, symbol, amount, profit_tgt, entry_price)
            
            msg = f"✅ **AI Scalper បានបើកដំណើរការ!** 🏓\\n\\n🪙 កាក់: **{symbol}**\\n💵 ទំហំលុយ: **${amount}**\\n🎯 គោលដៅចំណេញ (Take Profit): **{profit_tgt}%**\\n\\n{trade_status}\\n\\n_Bot នឹងទិញលក់វិលជុំយកចំណេញដោយស្វ័យប្រវត្តិ!_"'''

if 'អនុម័តដោយ Binance' not in content:
    content = content.replace(target_grid, replacement_grid)
    content = content.replace(target_scalp, replacement_scalp)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched bot_thread.py with trade reporting")
else:
    print("Already patched")
