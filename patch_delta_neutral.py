import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    code = f.read()

# The duplicates start with 'async def delta_neutral_monitor(app):'
# I will find all instances and only keep the first one, then patch it.
parts = code.split('async def delta_neutral_monitor(app):')

if len(parts) > 2:
    # There are duplicates!
    # parts[0] is everything before first
    # parts[1] is the first delta_neutral_monitor body (up to next def or next delta_neutral_monitor)
    # parts[2] is the second delta_neutral_monitor body
    
    # Actually, parts[2] goes all the way to sweep_sniper_monitor
    
    print(f"Found {len(parts)-1} delta_neutral_monitor instances. Removing duplicates...")
    
    # Just take parts[0] + parts[-1] (the last one) but wait, parts[1] might just be the exact same text.
    # Let's just do a clean regex replacement.
    pass

import sys

# Let's write a safer parser
with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
delta_count = 0

for line in lines:
    if line.startswith('async def delta_neutral_monitor(app):'):
        delta_count += 1
        if delta_count > 1:
            # We already have one, skip this duplicate block until the next 'async def'
            skip = True
            continue
            
    if skip and line.startswith('async def '):
        skip = False
        
    if not skip:
        new_lines.append(line)

code_no_dupes = "".join(new_lines)

# Now, we need to patch the single delta_neutral_monitor to use asyncio.to_thread and Liquidity Guard.
# I'll just find the entire delta_neutral_monitor block and replace it.

start_str = 'async def delta_neutral_monitor(app):'
next_def_idx = code_no_dupes.find('async def sweep_sniper_monitor(app):')

if next_def_idx == -1:
    print("Error: Could not find sweep_sniper_monitor!")
    sys.exit(1)

start_idx = code_no_dupes.find(start_str)

new_delta_neutral = """async def delta_neutral_monitor(app):
    \"\"\"
    Delta Neutral Strategy Monitor
    Maintains and closes active delta-neutral arbitrage bots.
    \"\"\"
    import database as db
    import market_data
    import trading_engine
    import asyncio
    
    # Check current active bots to close them if funding rate drops
    active_bots = db.get_active_delta_neutral_bots()
    if active_bots:
        for bot in active_bots:
            try:
                current_rate = await asyncio.to_thread(market_data.fetch_funding_rate, bot['symbol'])
                if current_rate < 0.0001:  # Drops below 0.01%, no longer profitable enough
                    keys = db.get_user_api(bot['chat_id'])
                    if keys:
                        api_key, api_secret = keys
                        await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, bot['symbol'], bot['spot_qty'])
                        await asyncio.to_thread(trading_engine.close_futures_short, api_key, api_secret, bot['symbol'], bot['futures_qty'])
                        db.stop_delta_neutral_bot(bot['id'])
                        
                        msg = f"💸 **Delta-Neutral Arbitrage Closed**\\n\\nSymbol: {bot['symbol']}\\nReason: Funding rate dropped below threshold.\\nBoth Spot and Futures positions have been successfully closed to lock in passive income."
                        await app.bot.send_message(chat_id=bot['chat_id'], text=msg, parse_mode="Markdown")
            except Exception as e:
                print(f"Error managing Delta Neutral for {bot['symbol']}: {e}")

    # Find new opportunities
    rates = await asyncio.to_thread(market_data.fetch_all_funding_rates)
    if not rates: return
    
    best_candidate = rates[0]
    if best_candidate['funding_rate'] < 0.0005:  # Require at least 0.05% per 8hr
        return
        
    symbol = best_candidate['symbol']
    rate_pct = best_candidate['funding_rate'] * 100
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id, delta_neutral_amount FROM users WHERE is_vip = 1 AND delta_neutral_enabled = 1')
    vips = cursor.fetchall()
    conn.close()
    
    for vip in vips:
        chat_id = vip[0]
        invest_amount = vip[1]
        
        # Check if already running a bot for this symbol
        existing = db.get_user_delta_neutral_bots(chat_id)
        if len(existing) >= 3: continue  # Max 3 concurrent arbitrage bots
        if any(b['symbol'] == symbol for b in existing): continue
        
        keys = db.get_user_api(chat_id)
        if not keys: continue
        api_key, api_secret = keys
        
        try:
            # LIQUIDITY GUARD
            available_usdt = await asyncio.to_thread(trading_engine.get_spot_balance, api_key, api_secret, "USDT")
            trade_amount = invest_amount / 2
            
            if available_usdt < trade_amount:
                trade_amount = available_usdt * 0.95  # Safe sizing if balance is short
                
            if trade_amount < 10.0:
                continue
            
            # 1. Spot Buy
            spot_res = await asyncio.to_thread(trading_engine.place_market_buy, api_key, api_secret, symbol, quote_order_qty=trade_amount)
            if "error" in spot_res:
                print(f"Spot buy failed for delta neutral {chat_id}: {spot_res['error']}")
                continue
                
            executed_qty = float(spot_res.get("executedQty", 0))
            if executed_qty <= 0: continue
            
            # 2. Short Futures (Exact same quantity, 1x leverage)
            fut_res = await asyncio.to_thread(trading_engine.place_futures_short_qty, api_key, api_secret, symbol, qty=executed_qty, leverage=1)
            if "error" in fut_res:
                # Emergency sell spot
                await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, symbol, qty=executed_qty)
                print(f"Futures short failed, reverted spot {chat_id}: {fut_res['error']}")
                continue
                
            db.add_delta_neutral_bot(chat_id, symbol, invest_amount, executed_qty, executed_qty)
            
            msg = f"💸 **Delta-Neutral Arbitrage Opened!**\\n\\n🪙 **{symbol}**\\n📈 **Funding Rate:** {rate_pct:.4f}%\\n💰 **Investment:** ${invest_amount:.2f}\\n⚖️ **Spot Buy:** {executed_qty} {symbol}\\n🔴 **Futures Short:** {executed_qty} {symbol} (1x Leverage)\\n\\n_You are now earning passive income every 8 hours without price risk!_"
            await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Error opening delta neutral for {chat_id}: {e}")

"""

final_code = code_no_dupes[:start_idx] + new_delta_neutral + code_no_dupes[next_def_idx:]

with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
    f.write(final_code)

print('Successfully refactored delta_neutral_monitor!')
