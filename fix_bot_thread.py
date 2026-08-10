import codecs
with codecs.open('bot_thread.py', 'r', 'utf-8') as f: lines = f.readlines()

new_lines = []
for line in lines:
    if 'elif "🔴 SELL" in analysis_result or "BEARISH" in analysis_result.upper():' in line:
        new_lines.append(line)
        new_lines.append('                config = db.get_hedge_mode_config(chat_id)\n')
        new_lines.append('                if config["enabled"]:\n')
        new_lines.append('                    keys = db.get_user_api(chat_id)\n')
        new_lines.append('                    if keys:\n')
        new_lines.append('                        await context.bot.send_message(chat_id=chat_id, text=loc.get_text(user_lang, "hedge_short_start", symbol=symbol), parse_mode="Markdown")\n')
        new_lines.append('                        import trading_engine\n')
        new_lines.append('                        import ml_predictor\n')
        new_lines.append('                        vol_tgt = ml_predictor.get_vol_target(symbol)\n')
        new_lines.append('                        res = trading_engine.place_futures_short(keys[0], keys[1], symbol, config["amount"], config["leverage"], vol_target=vol_tgt)\n')
        new_lines.append('                        if "error" not in res and res.get("status") == "FILLED":\n')
        new_lines.append('                            db.add_active_short(chat_id, symbol, config["amount"], config["leverage"], res["price"])\n')
        new_lines.append('                            msg = loc.get_text(user_lang, "hedge_short_success", symbol=symbol, price=res["price"], leverage=config["leverage"])\n')
        new_lines.append('                            await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")\n')
        new_lines.append('                            self.log_signal.emit(f"🤖 Hedge Mode Executed for {chat_id}: SHORT {symbol}")\n')
    elif 'else:' in line and 'error_msg = res.get("error"' in lines[lines.index(line)+1] if lines.index(line)+1 < len(lines) else False:
        if "elif" not in lines[lines.index(line)-1] and "elif" not in lines[lines.index(line)-2] and "elif" not in lines[lines.index(line)-3]:
            new_lines.append(line)
        # Skip the broken else block right after elif
        pass
    else:
        new_lines.append(line)

# Let's do a much simpler fix. We know exactly which lines to replace.
with codecs.open('bot_thread.py', 'r', 'utf-8') as f: text = f.read()

broken_text = '''            elif "🔴 SELL" in analysis_result or "BEARISH" in analysis_result.upper():
                        else:
                            error_msg = res.get("error", "Unknown error")
                            msg = loc.get_text(user_lang, 'hedge_short_fail', error=error_msg)
                            await context.bot.send_message(chat_id=chat_id, text=msg)'''

fixed_text = '''            elif "🔴 SELL" in analysis_result or "BEARISH" in analysis_result.upper():
                config = db.get_hedge_mode_config(chat_id)
                if config["enabled"]:
                    keys = db.get_user_api(chat_id)
                    if keys:
                        await context.bot.send_message(chat_id=chat_id, text=loc.get_text(user_lang, 'hedge_short_start', symbol=symbol), parse_mode="Markdown")
                        import trading_engine
                        import ml_predictor
                        vol_tgt = ml_predictor.get_vol_target(symbol)
                        res = trading_engine.place_futures_short(keys[0], keys[1], symbol, config["amount"], config["leverage"], vol_target=vol_tgt)
                        if "error" not in res and res.get("status") == "FILLED":
                            db.add_active_short(chat_id, symbol, config["amount"], config["leverage"], res['price'])
                            msg = loc.get_text(user_lang, 'hedge_short_success', symbol=symbol, price=res['price'], leverage=config['leverage'])
                            await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                            self.log_signal.emit(f"🤖 Hedge Mode Executed for {chat_id}: SHORT {symbol}")
                        else:
                            error_msg = res.get("error", "Unknown error")
                            msg = loc.get_text(user_lang, 'hedge_short_fail', error=error_msg)
                            await context.bot.send_message(chat_id=chat_id, text=msg)'''

text = text.replace(broken_text, fixed_text)

with codecs.open('bot_thread.py', 'w', 'utf-8') as f: f.write(text)
print("bot_thread.py fixed.")
