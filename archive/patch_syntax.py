with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 1: process_economic_trade
code = code.replace('def process_economic_trade(chat_id, lang):', 'async def process_economic_trade(chat_id, lang):')

# Fix 2: execute_trade_logic
code = code.replace('def execute_trade_logic():', 'async def execute_trade_logic():')
code = code.replace('trade_msgs = await asyncio.to_thread(execute_trade_logic)', 'trade_msgs = await execute_trade_logic()')

with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed await outside async!")
