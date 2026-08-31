import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

idx1 = content.find("await update.message.reply_text(loc.get_text(user_lang, 'hedge_mode_disabled'))")
idx2 = content.find("async def smart_dca_command", idx1)

if idx1 != -1 and idx2 != -1:
    part1 = content[:idx1 + len("await update.message.reply_text(loc.get_text(user_lang, 'hedge_mode_disabled'))")]
    part2 = content[idx2:]
    
    insertion = '''
                await delete_sensitive_message(context, chat_id, update.message.message_id, user_lang)
                self.log_signal.emit(f"🛡️ Hedge Mode DISABLED for {chat_id}")
            else:
                await update.message.reply_text(loc.get_text(user_lang, 'hedge_mode_usage'))

        '''
    
    new_content = part1 + insertion + part2
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed bot_thread.py successfully.")
else:
    print("Could not find patterns.")
