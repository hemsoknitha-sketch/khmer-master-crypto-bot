import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to command list
target1 = '''                BotCommand("balance", "💳 ឆែកលុយក្នុងកាបូប Binance ផ្ទាល់"),
                BotCommand("scalp", "🏓 យុទ្ធសាស្រ្ត AI Scalper (Ping-Pong)"),'''

replacement1 = '''                BotCommand("balance", "💳 ឆែកលុយក្នុងកាបូប Binance ផ្ទាល់"),
                BotCommand("scalp", "🏓 យុទ្ធសាស្រ្ត AI Scalper (Ping-Pong)"),
                BotCommand("stop", "🛑 បញ្ឈប់ Bot ដែលកំពុងដើរ (ឧ. /stop BTCUSDT)"),'''

target2 = '''                        BotCommand("set_pin", "🔒 កំណត់លេខកូដ PIN សម្ងាត់"),
                        BotCommand("portfolio", "📊 ពិនិត្យមើលប្រាក់ចំណេញ និងកាក់ដែលកំពុងកាន់ (PnL)"),'''

replacement2 = '''                        BotCommand("set_pin", "🔒 កំណត់លេខកូដ PIN សម្ងាត់"),
                        BotCommand("portfolio", "📊 ពិនិត្យមើលប្រាក់ចំណេញ និងកាក់ដែលកំពុងកាន់ (PnL)"),
                        BotCommand("stop", "🛑 បញ្ឈប់ Bot ដែលកំពុងដើរ (ឧ. /stop BTCUSDT)"),'''

# Add command handler
target3 = '''        async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):'''

replacement3 = '''        async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            chat_id = update.effective_chat.id
            if not await verify_user(update): return
            user_lang = db.get_user_language(chat_id)
            
            if len(context.args) == 0:
                await update.message.reply_text("⚠️ របៀបប្រើប្រាស់: `/stop <កាក់>`\\nឧទាហរណ៍: `/stop BTCUSDT`", parse_mode="Markdown")
                return
                
            symbol = context.args[0].upper()
            
            # Deactivate from DB
            db.deactivate_all_bots_by_symbol(chat_id, symbol)
            
            msg = f"🛑 **បានបញ្ឈប់ដោយជោគជ័យ!**\\n\\nរាល់ប្រព័ន្ធ Infinity Grid, AI Scalper, និង Auto-Trades សម្រាប់កាក់ **{symbol}** ត្រូវបានផ្តាច់ និងបិទដំណើរការ។"
            if user_lang != 'khmer':
                msg = f"🛑 **Successfully Stopped!**\\n\\nAll Infinity Grid, AI Scalper, and Auto-Trades for **{symbol}** have been deactivated."
                
            await update.message.reply_text(msg, parse_mode="Markdown")

        async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):'''

# Register handler
target4 = '''        self.app.add_handler(CommandHandler("portfolio", portfolio_command))'''

replacement4 = '''        self.app.add_handler(CommandHandler("portfolio", portfolio_command))
        self.app.add_handler(CommandHandler("stop", stop_command))'''

if 'stop_command(update: Update' not in content:
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    content = content.replace(target3, replacement3)
    content = content.replace(target4, replacement4)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched bot_thread.py with stop command")
else:
    print("Already patched")
