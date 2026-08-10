import codecs
with codecs.open('bot_thread.py', 'r', 'utf-8') as f:
    text = f.read()

broken_target = '''        async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            
            if len(context.args) != 1:
                await update.message.reply_text("Please provide language code: kh, en, or cn")
                return
                
            new_lang = context.args[0].lower()
            if new_lang not in ['kh', 'en', 'cn']:
                await update.message.reply_text("Invalid language. Use: kh, en, or cn")
                return
                
            db.update_user_language(chat_id, new_lang)
            await update.message.reply_text(loc.get_text(new_lang, 'language_set', lang=new_lang.upper()), parse_mode="Markdown")
            self.log_signal.emit(f"🌐 User {chat_id} changed language to {new_lang}")

            pin_input = context.args[2]'''

fixed_replacement = '''        async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            
            if len(context.args) != 1:
                await update.message.reply_text("Please provide language code: kh, en, or cn")
                return
                
            new_lang = context.args[0].lower()
            if new_lang not in ['kh', 'en', 'cn']:
                await update.message.reply_text("Invalid language. Use: kh, en, or cn")
                return
                
            db.update_user_language(chat_id, new_lang)
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
            pin_input = context.args[2]'''

text = text.replace(broken_target, fixed_replacement)

# Now fix the validate_api_keys which the tool failed to replace properly
bad_validate = '''            import trading_engine as te
            if not te.validate_api_keys(api_key, api_secret):
                await update.message.reply_text(loc.get_text(user_lang, 'api_invalid'), parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return'''

good_validate = '''            import trading_engine as te
            is_valid, reason = te.validate_api_keys(api_key, api_secret)
            if not is_valid:
                await update.message.reply_text(f"📊 **ស្ថានភាពភ្ជាប់ API:**\\n\\n{reason}", parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return'''

text = text.replace(bad_validate, good_validate)

with codecs.open('bot_thread.py', 'w', 'utf-8') as f:
    f.write(text)

print('File restored and patched.')
