import codecs

with codecs.open('bot_thread.py', 'r', 'utf-8') as f:
    text = f.read()

start_marker = 'self.log_signal.emit(f"✅ VIP User returned. Chat ID: {chat_id}")\n                return\n'
end_marker = '        async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):'

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found!")
    exit(1)

start_idx += len(start_marker)

correct_code = '''            
            keyboard = [[KeyboardButton("Share Phone Number 📱", request_contact=True)]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            await context.bot.send_message(
                chat_id=chat_id, 
                text="🤖 Welcome to Apex AI Bot!\\n\\nFor high-security verification, please share your phone number by clicking the button below.", 
                reply_markup=reply_markup
            )
            self.log_signal.emit(f"✅ User started bot. Chat ID: {chat_id}. Requested contact.")

        async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            contact = update.message.contact
            if contact:
                chat_id = update.effective_chat.id
                phone_number = contact.phone_number
                db.update_user_phone(chat_id, phone_number)
                self.log_signal.emit(f"📱 Phone number received for Chat ID: {chat_id}: {phone_number}")
                await context.bot.send_message(chat_id=chat_id, text="✅ Phone number verified securely. You may now wait for Admin approval or use /help.")

        async def send_long_message(context, chat_id, text):
            """Helper to send messages longer than 4096 chars and handle Markdown parsing errors."""
            if len(text) <= 4000:
                try:
                    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
                except Exception:
                    await context.bot.send_message(chat_id=chat_id, text=text) # Fallback without markdown
                return

            paragraphs = text.split('\\n')
            current_msg = ""
            for p in paragraphs:
                if len(current_msg) + len(p) + 1 > 4000:
                    try:
                        await context.bot.send_message(chat_id=chat_id, text=current_msg, parse_mode="Markdown")
                    except Exception:
                        await context.bot.send_message(chat_id=chat_id, text=current_msg)
                    current_msg = p + "\\n"
                else:
                    current_msg += p + "\\n"
            if current_msg.strip():
                try:
                    await context.bot.send_message(chat_id=chat_id, text=current_msg, parse_mode="Markdown")
                except Exception:
                    await context.bot.send_message(chat_id=chat_id, text=current_msg)

        async def execute_auto_trade_if_applicable(context, chat_id, user_lang, symbol, analysis_result):
            if "🟢 BUY" in analysis_result:
                config = db.get_auto_trade_config(chat_id)
                if config["enabled"]:
                    import security
                    keys = db.get_user_api(chat_id)
                    if keys:
                        await context.bot.send_message(chat_id=chat_id, text=loc.get_text(user_lang, 'auto_buy_start', symbol=symbol), parse_mode="Markdown")
                        import trading_engine
                        res = trading_engine.place_market_buy(keys[0], keys[1], symbol, config["amount"])
                        if "error" not in res and res.get("status") == "FILLED":
                            db.add_active_trade(chat_id, symbol, res['origQty'], res['price'], config['trailing_pct'])
                            sl_price = float(res['price']) * (1 - (float(config['trailing_pct'])/100.0))
                            msg = loc.get_text(user_lang, 'auto_buy_success', symbol=symbol, buy_price=res['price'], initial_stop_loss=sl_price)
                            await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                            self.log_signal.emit(f"🤖 Auto-Trade Executed for {chat_id}: BUY {symbol}")
                        else:
                            error_msg = res.get("error", "Unknown error")
                            msg = loc.get_text(user_lang, 'auto_buy_fail', error=error_msg)
                            await context.bot.send_message(chat_id=chat_id, text=msg)
            elif "🔴 SELL" in analysis_result or "BEARISH" in analysis_result.upper():
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
                            await context.bot.send_message(chat_id=chat_id, text=msg)

'''

new_text = text[:start_idx] + correct_code + text[end_idx:]

with codecs.open('bot_thread.py', 'w', 'utf-8') as f:
    f.write(new_text)

print("bot_thread.py fully restored successfully.")
