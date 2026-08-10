import re

# 1. Update bot_thread.py
with open('bot_thread.py', 'r', encoding='utf-8') as f:
    bt_content = f.read()

bt_target = '''    def _handle_direct_message(self, chat_id: int, text: str):
        if self.loop and self.app:
            asyncio.run_coroutine_threadsafe(
                self.app.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown"), 
                self.loop
            )'''

bt_replacement = '''    def _handle_direct_message(self, chat_id: int, text: str):
        if self.loop and self.app:
            async def _send():
                try:
                    await self.app.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
                except Exception as e:
                    print(f"Direct message Markdown error: {e}, falling back to plain text.")
                    try:
                        await self.app.bot.send_message(chat_id=chat_id, text=text)
                    except Exception as e2:
                        print(f"Failed to send direct message completely: {e2}")
            asyncio.run_coroutine_threadsafe(_send(), self.loop)'''

if 'falling back to plain text' not in bt_content:
    bt_content = bt_content.replace(bt_target, bt_replacement)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(bt_content)
    print("Patched bot_thread.py for direct messages")

# 2. Update main.py prompt
with open('main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

main_target = '''        prompt = f"You are an expert customer success AI. Look at this user's activity and chat history:\\n\\n{profile_data}\\n\\nDraft a perfect, personalized, and encouraging response to this user in their preferred language (or Khmer by default). Sound very professional. Output ONLY the message text you want to send."'''

main_replacement = '''        prompt = (f"You are the Apex AI Bot's Lead Customer Success Expert and a highly skilled Crypto Arbitrage Specialist. "
                  f"Look at this user's activity and chat history:\\n\\n{profile_data}\\n\\n"
                  f"Draft a highly persuasive, confident, and personalized response to this user in Khmer. "
                  f"Provide expert advice on using our High-Volatility Arbitrage systems like /infinity_grid and /scalp. "
                  f"Don't mention internal technical details, just sound like a billionaire-tier professional helping them win. "
                  f"Output ONLY the message text you want to send.")'''

if 'Billionaire-tier' not in main_content and 'Lead Customer Success Expert' not in main_content:
    main_content = main_content.replace(main_target, main_replacement)
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)
    print("Patched main.py for AI Draft Prompt")
