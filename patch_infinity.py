import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Menu
content = content.replace(
    'BotCommand("grid_bot", "បើកប្រព័ន្ធ Grid Bot"),',
    'BotCommand("infinity_grid", "🕸️ Infinity Grid (សំណាញ់ចាប់ចំណេញ)"),'
)

# 2. Insert Command Handler before grid_bot_command
grid_cmd_start = "        async def grid_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):"

infinity_cmd = '''        async def infinity_grid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            user_lang = db.get_user_language(chat_id)
            
            args = context.args
            if len(args) != 5:
                usage = "⚠️ **របៀបប្រើប្រាស់ Infinity Grid:**\\n\\n`/infinity_grid <កាក់> <ទំហំលុយ១ជាន់> <ភាគរយគម្លាត> <Max_Invest> <PIN>`\\n\\nឧទាហរណ៍៖ `/infinity_grid XRP 10 1.0 100 1234`\\n(វិនិយោគសរុប $100, ទិញ/លក់ ម្តង $10 រាល់ពេលខុសគ្នា 1.0%)"
                await update.message.reply_text(usage, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
                
            symbol = args[0].upper()
            if not symbol.endswith("USDT"):
                symbol += "USDT"
                
            try:
                amt_per_layer = float(args[1])
                step_pct = float(args[2])
                max_inv = float(args[3])
                pin = args[4]
            except (ValueError, IndexError):
                await update.message.reply_text("❌ សូមបញ្ចូលចំនួនលុយ និងភាគរយជាលេខឲ្យបានត្រឹមត្រូវ។")
                return
                
            stored_pin = db.get_user_pin(chat_id)
            import hashlib
            if not stored_pin or hashlib.sha256(pin.encode()).hexdigest() != stored_pin:
                await update.message.reply_text("❌ លេខកូដ PIN មិនត្រឹមត្រូវ។")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
                
            import requests
            try:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
                res = requests.get(url, timeout=5)
                entry_price = float(res.json()['price'])
            except:
                await update.message.reply_text(f"❌ បរាជ័យក្នុងការទាញយកតម្លៃសម្រាប់ {symbol}")
                return
                
            # Initially buy the first layer
            keys = db.get_user_api(chat_id)
            if keys:
                import trading_engine
                trading_engine.place_market_buy(keys[0], keys[1], symbol, amt_per_layer)
                
            db.add_infinity_grid(chat_id, symbol, amt_per_layer, step_pct, max_inv, entry_price)
            
            msg = f"✅ **Infinity Grid បានបើកដំណើរការ!** 🕸️\\n\\n🪙 កាក់: **{symbol}**\\n💵 លុយទិញ/លក់១ជាន់: **${amt_per_layer}**\\n🎯 គម្លាតសំណាញ់: **{step_pct}%**\\n💰 ដើមទុនអតិបរមា: **${max_inv}**\\n\\n_Bot នឹងប្រមូលចំណេញគ្មានដែនកំណត់ 24/7!_"
            await update.message.reply_text(msg, parse_mode="Markdown")
            await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
            self.log_signal.emit(f"🕸️ Infinity Grid Activated for {chat_id}: {symbol}")

'''

content = content.replace(grid_cmd_start, infinity_cmd + grid_cmd_start)

# 3. Register Handler
handler_reg = 'self.app.add_handler(CommandHandler("grid_bot", grid_bot_command))'
content = content.replace(handler_reg, 'self.app.add_handler(CommandHandler("infinity_grid", infinity_grid_command))\n        ' + handler_reg)

# 4. Add to scheduler
scheduler_reg = 'scheduler_tasks.ai_scalper_monitor,'
infinity_job = '''        # 17. Infinity Grid Monitor
        self.scheduler.add_job(
            scheduler_tasks.infinity_grid_monitor,
            "interval",
            seconds=10,
            args=[self.app, self.ai_engine],
            id="infinity_grid_monitor"
        )
        
'''

scheduler_target = '''        # 16. AI Scalper Monitor (Ping-Pong)'''
if scheduler_target in content:
    content = content.replace(scheduler_target, infinity_job + scheduler_target)
else:
    print("Warning: Scheduler insertion point not found.")

with open('bot_thread.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied.")
