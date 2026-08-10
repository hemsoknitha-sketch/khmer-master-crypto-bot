import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert Command Handler before infinity_grid_command
target_func = "        async def infinity_grid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):"

scan_cmd = '''        async def smart_listing_sniper_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            user_lang = db.get_user_language(chat_id)
            
            args = context.args
            if len(args) < 3:
                await update.message.reply_text("❌ ប្រើប្រាស់ខុស! ទម្រង់ត្រូវ: `/smart_listing_sniper <SYMBOL> <INVEST_AMOUNT> <PIN>`\\nឧទាហរណ៍: `/smart_listing_sniper TONUSDT 100 1234`", parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
                
            symbol = args[0].upper()
            if not symbol.endswith("USDT"): symbol += "USDT"
            
            try:
                invest_amount = float(args[1])
            except ValueError:
                await update.message.reply_text("❌ ចំនួនលុយមិនត្រឹមត្រូវ!")
                return
                
            pin = args[2]
            user = db.get_user(chat_id)
            if not user or user[4] != pin:
                await update.message.reply_text("❌ PIN Code មិនត្រឹមត្រូវ!")
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                return
                
            import scheduler_tasks
            if not hasattr(scheduler_tasks, "active_smart_snipers"):
                scheduler_tasks.active_smart_snipers = {}
                
            from datetime import datetime
            scheduler_tasks.active_smart_snipers[symbol] = {
                "chat_id": chat_id,
                "invest_amount": invest_amount,
                "state": "WAITING_DUMP",
                "buy_price": 0.0,
                "max_price_seen": 0.0,
                "start_time": datetime.now()
            }
            
            await update.message.reply_text(f"🧠 **Smart Listing Sniper ដំណើរការ!**\\n\\n🪙 **កាក់:** {symbol}\\n💰 **ទុនត្រៀម:** `${invest_amount}`\\n⏳ **ស្ថានភាព:** កំពុងរង់ចាំទីផ្សារបញ្ចេញកំហឹងលក់ (Airdrop Dump) ចប់សិន ទើបរកសញ្ញាទិញផ្អែកលើ EMA-9 Breakout...", parse_mode="Markdown")
            await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
            self.log_signal.emit(f"🧠 Smart Listing Sniper Activated for {chat_id}: {symbol} with ${invest_amount}")

'''

content = content.replace(target_func, scan_cmd + target_func)

# 2. Register Handler
handler_reg = 'self.app.add_handler(CommandHandler("infinity_grid", infinity_grid_command))'
content = content.replace(handler_reg, 'self.app.add_handler(CommandHandler("smart_listing_sniper", smart_listing_sniper_command))\n        ' + handler_reg)

with open('bot_thread.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied to bot_thread.py.")
