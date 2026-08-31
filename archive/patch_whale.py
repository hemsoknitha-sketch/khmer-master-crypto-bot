import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func_pattern = re.compile(r'async def order_book_sniper\(app: Application, ai_engine\):.*?except Exception as e:\s*pass', re.DOTALL)

new_func = '''async def order_book_sniper(app: Application, ai_engine):
    """
    Scans the top volatile coins' Order Books for massive Whale Walls (> $100k) 
    and simulates a front-running limit buy if found.
    """
    try:
        vip_users = db.get_vip_users_with_lang()
        if not vip_users: return
        
        import market_data
        
        # Fetch Top 15 volatile coins to ensure we catch whales without hitting API limits heavily
        volatile_coins = market_data.fetch_top_volatile_coins(limit=15, min_change_pct=3.0)
        if not volatile_coins: return
        
        if not hasattr(order_book_sniper, "last_walls"):
            order_book_sniper.last_walls = {}
            
        for coin in volatile_coins:
            symbol = coin['symbol']
            bids, asks = market_data.get_order_book_depth(symbol, limit=20)
            
            if not bids: continue
            
            whale_wall_found = False
            target_price = 0
            whale_usdt = 0
            
            for price, qty in bids:
                value = price * qty
                if value >= 100000: # $100k Whale Wall threshold
                    whale_wall_found = True
                    target_price = price
                    whale_usdt = value
                    break
                    
            if whale_wall_found:
                last_wall = order_book_sniper.last_walls.get(symbol, 0)
                # Check if it's a new wall (price differs by > 0.5%)
                if target_price > 0 and (last_wall == 0 or abs(last_wall - target_price) / target_price > 0.005):
                    order_book_sniper.last_walls[symbol] = target_price
                    
                    front_run_price = target_price * 1.0005 # Front-run by 0.05%
                    
                    print(f"🐋 WHALE WALL DETECTED: {symbol} at ${target_price:,.4f} (Value: ${whale_usdt:,.0f})")
                    
                    for row in vip_users:
                        chat_id = row[0]
                        
                        msg = f"🐋 **Whale Wall Detected!**\\nMassive buy wall on {symbol} at `${target_price:,.4f}`.\\n_Value:_ `${whale_usdt:,.0f}`\\n\\n_Bot simulating Front-Run Buy at `${front_run_price:,.4f}`..._"
                        try:
                            await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                        except Exception:
                            pass
    except Exception as e:
        print(f"Error in order_book_sniper: {e}")'''

new_content, count = old_func_pattern.subn(new_func, content)

if count > 0:
    with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patch applied successfully.")
else:
    print("Pattern not found. Did not patch.")
