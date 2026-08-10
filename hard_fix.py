import codecs

with codecs.open('bot_thread.py', 'r', 'utf-8') as f:
    text = f.read()

start_idx = text.find('        async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):')
end_idx = text.find('        async def admin_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):')

if start_idx != -1 and end_idx != -1:
    before = text[:start_idx]
    after = text[end_idx:]
    
    fixed_middle = '''        async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            user_lang = db.get_user_language(chat_id)
            await context.bot.send_message(chat_id=chat_id, text=loc.get_text(user_lang, 'fetching_top'))
            import market_data
            top_gainers_summary = market_data.fetch_top_gainers()
            
            ai_prompt = f"Here are the top gaining coins in the last 24h:\\n{top_gainers_summary}\\nProvide a very brief 2-3 sentence analysis of what sector might be pumping or market sentiment."
            if user_lang != 'auto':
                ai_prompt += f"\\n\\n[CRITICAL INSTRUCTION: You MUST respond fluently in {user_lang.upper()}.]"
                
            analysis = self.ai_engine.analyze_opportunity(ai_prompt)
            
            header = loc.get_text(user_lang, 'ai_analysis_header')
            final_msg = f"{top_gainers_summary}\\n{header}{analysis}"
            await send_long_message(context, chat_id, final_msg)
            self.log_signal.emit(f"🚀 Sent top gainers to {chat_id}")

        async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            user_lang = db.get_user_language(chat_id)
            await context.bot.send_message(chat_id=chat_id, text=loc.get_text(user_lang, 'fetching_news'))
            ai_prompt = "What is the current global macroeconomic situation and overall sentiment for the cryptocurrency market? Summarize in 3-4 paragraphs."
            if user_lang != 'auto':
                ai_prompt += f"\\n\\n[CRITICAL INSTRUCTION: You MUST respond fluently in {user_lang.upper()}.]"
            analysis = self.ai_engine.analyze_opportunity(ai_prompt)
            await send_long_message(context, chat_id, analysis)
            self.log_signal.emit(f"📰 Sent macro news to {chat_id}")

        async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            current_lang = db.get_user_language(chat_id)
            if not context.args:
                await update.message.reply_text(loc.get_text(current_lang, 'language_current', lang=current_lang.upper()), parse_mode="Markdown")
                return
                
            new_lang = context.args[0].lower()
            valid_langs = ['khmer', 'english', 'chinese', 'auto']
            if new_lang not in valid_langs:
                await update.message.reply_text(loc.get_text(current_lang, 'language_invalid'), parse_mode="Markdown")
                return
                
            db.set_user_language(chat_id, new_lang)
            await update.message.reply_text(loc.get_text(new_lang, 'language_set', lang=new_lang.upper()), parse_mode="Markdown")
            self.log_signal.emit(f"🌐 User {chat_id} changed language to {new_lang}")

        async def delete_sensitive_message(context, chat_id, message_id, user_lang):
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                await context.bot.send_message(chat_id=chat_id, text=loc.get_text(user_lang, 'msg_auto_deleted'), parse_mode="Markdown")
            except Exception as e:
                self.log_signal.emit(f"⚠️ Failed to auto-delete message: {e}")

        async def add_api_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            user_lang = db.get_user_language(chat_id)
            
            if len(context.args) != 3:
                await update.message.reply_text(loc.get_text(user_lang, 'add_api_usage_pin'), parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
                
            api_key = context.args[0]
            api_secret = context.args[1]
            pin_input = context.args[2]
            
            stored_pin = db.get_user_pin(chat_id)
            if not stored_pin:
                await update.message.reply_text(loc.get_text(user_lang, 'pin_required'), parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
                
            import hashlib
            input_hash = hashlib.sha256(pin_input.encode()).hexdigest()
            if stored_pin != input_hash:
                await update.message.reply_text(loc.get_text(user_lang, 'pin_incorrect'), parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
            
            import trading_engine as te
            is_valid, reason = te.validate_api_keys(api_key, api_secret)
            if not is_valid:
                await update.message.reply_text(f"📊 **ស្ថានភាពភ្ជាប់ API:**\\n\\n{reason}", parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
            
            db.set_user_api(chat_id, api_key, api_secret)
            
            await update.message.reply_text(loc.get_text(user_lang, 'api_added'), parse_mode="Markdown")
            await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
            self.log_signal.emit(f"✅ VIP User {chat_id} updated their Binance API keys.")

'''
    
    with codecs.open('bot_thread.py', 'w', 'utf-8') as f:
        f.write(before + fixed_middle + after)
        
    print("Repaired bot_thread.py successfully.")
else:
    print("Could not find start or end index.")
