import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

engine_code = '''
async def smart_sniper_engine(app: Application, ai_engine):
    """Monitors the active Smart Listing Snipers every 5 seconds."""
    if not hasattr(smart_sniper_engine, "active_smart_snipers"):
        return
        
    from datetime import datetime
    import market_data
    import trading_engine
    
    # We need a copy of keys because we might delete or modify
    symbols = list(getattr(smart_sniper_engine, "active_smart_snipers", {}).keys())
    
    # Since active_smart_snipers is initialized in the command handler as an attribute 
    # of scheduler_tasks module, let's reference it correctly:
    import sys
    this_module = sys.modules[__name__]
    active_snipers = getattr(this_module, "active_smart_snipers", {})
    
    for symbol in list(active_snipers.keys()):
        sniper = active_snipers[symbol]
        state = sniper['state']
        chat_id = sniper['chat_id']
        invest_amount = sniper['invest_amount']
        
        try:
            if state == "WAITING_DUMP":
                # Ensure at least 1 minute has passed to let first 1m candle form
                if (datetime.now() - sniper['start_time']).total_seconds() < 60:
                    continue
                    
                df = market_data.get_historical_klines_1m(symbol, limit=20)
                if df is None or len(df) < 10:
                    continue
                    
                # Calculate EMA-9
                df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()
                
                curr = df.iloc[-1]
                prev = df.iloc[-2]
                
                # Check for Breakout & Volume Spike
                is_breakout = curr['close'] > curr['ema9'] and prev['close'] <= prev['ema9']
                is_volume_spike = curr['volume'] > (prev['volume'] * 1.5)
                
                if is_breakout and is_volume_spike:
                    # Time to buy!
                    res = trading_engine.execute_market_buy(symbol, invest_amount)
                    buy_price = curr['close']
                    if res.get('status') == 'success':
                        buy_price = res.get('price', buy_price)
                        
                    sniper['state'] = "TRAILING_SL"
                    sniper['buy_price'] = buy_price
                    sniper['max_price_seen'] = buy_price
                    
                    msg = f"🚀 **សញ្ញាទិញបានមកដល់! (Momentum Breakout)**\\n\\n🪙 កាក់: {symbol}\\n💵 តម្លៃទិញ: `${buy_price:.4f}`\\n🛡️ កំណត់ Stop-Loss ស្វ័យប្រវត្តិ: -5%\\n📈 Trailing Stop: +3%"
                    await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            
            elif state == "TRAILING_SL":
                # Check current price
                ticker = trading_engine.client.get_symbol_ticker(symbol=symbol)
                current_price = float(ticker['price'])
                
                buy_price = sniper['buy_price']
                max_seen = sniper['max_price_seen']
                
                if current_price > max_seen:
                    sniper['max_price_seen'] = current_price
                    max_seen = current_price
                    
                # Calculate dynamic stop price
                if max_seen > buy_price * 1.05:
                    # Profit is over 5%, trail by 3% from max
                    stop_price = max_seen * 0.97
                else:
                    # Hard stop at -5%
                    stop_price = buy_price * 0.95
                    
                if current_price <= stop_price:
                    # Trigger Sell
                    # Calculate held amount
                    held_qty = (invest_amount * 0.999) / buy_price # Roughly minus fees
                    res = trading_engine.execute_market_sell(symbol, held_qty)
                    sell_price = current_price
                    if res.get('status') == 'success':
                        sell_price = res.get('price', current_price)
                        
                    profit_pct = ((sell_price - buy_price) / buy_price) * 100
                    profit_usd = (invest_amount * profit_pct) / 100
                    
                    status_icon = "🟩 ចំណេញ" if profit_pct > 0 else "🟥 ខាត (Stop-Loss)"
                    msg = f"🚨 **បញ្ចប់ការជួញដូរ!**\\n\\n🪙 កាក់: {symbol}\\n💵 តម្លៃលក់: `${sell_price:.4f}`\\n📊 លទ្ធផល: {status_icon} `{profit_pct:.2f}%` (${profit_usd:.2f})"
                    await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                    
                    sniper['state'] = "SOLD"
                    
            elif state == "SOLD":
                del active_snipers[symbol]
                
        except Exception as e:
            print(f"[SMART SNIPER ERROR] {symbol}: {e}")

'''

content = content + "\n" + engine_code

with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied to scheduler_tasks.py")
