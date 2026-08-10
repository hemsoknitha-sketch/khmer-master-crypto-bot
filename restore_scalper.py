import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_logic = """                        # Convert USDT amount to Token Quantity
                        qty_to_sell = round(amount / current_price, 4)
                        res = trading_engine.place_market_sell(keys[0], keys[1], symbol, qty_to_sell)
                        
                        if res.get("status") == "FILLED":
                            actual_profit = ((current_price - entry_price) / entry_price) * 100.0
                            msg = f"🏓 **AI SCALPER (SELL)** 🏓\\n\\n🪙 **{symbol}**\\n💵 លក់ចេញ: `${current_price:,.4f}`\\n🟩 ចំណេញ: `+{actual_profit:.2f}%`\\n\\n_Bot កំពុងរង់ចាំទិញចូលវិញនៅពេលវាធ្លាក់ចុះបន្តិច..._"
                            try:
                                await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                            except: pass
                            db.update_scalper_state(scalp_id, 'WAITING_TO_BUY', current_price)
                        else:
                            error_msg = res.get('error', res.get('msg', 'Unknown Error'))
                            msg = f"🏓 **AI SCALPER (SELL FAILED)** ❌\\nបរាជ័យក្នុងការលក់ {symbol}: {error_msg}\\nBot នឹងព្យាយាមម្តងទៀតនៅជុំក្រោយ។"
                            try:
                                await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                            except: pass\n"""

# Find the exact place to insert it
for i, line in enumerate(lines):
    if "if current_price >= target_sell_price:" in line:
        # found line 1319. Check lines after
        if "if keys:" in lines[i+2]:
            # we want to replace lines i+2 to i+6
            # currently it is:
            # 1321:                     if keys:
            # 1322:                     
            # 1323:                     db.update_scalper_state(scalp_id, 'WAITING_TO_BUY', current_price)
            del lines[i+3:i+5] # remove the empty line and the old update_scalper_state
            lines.insert(i+3, new_logic)
            break

with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Restored missing scalper sell logic.")
