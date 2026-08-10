import os

file_path = "scheduler_tasks.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Find trailing_stop_monitor
start_idx = content.find("async def trailing_stop_monitor(app: Application, ai_engine):")
end_idx = content.find("async def smart_dca_monitor(app: Application, ai_engine):")

if start_idx != -1 and end_idx != -1:
    new_code = """
# ==========================================
# RE-ENTRY CACHE
# ==========================================
RECENTLY_SOLD_CACHE = {}  # { "BTCUSDT": {"sell_time": 12345, "sell_price": 50000, "chat_id": 123, "capital": 50.0} }
REENTRY_COOLDOWN = 1800  # 30 minutes
REENTRY_LOCKOUT_CACHE = {} # { "BTCUSDT": lockout_timestamp } (60-minute lockout on loss)
REENTRY_LOCKOUT_COOLDOWN = 3600 # 60 minutes

async def process_single_trailing_stop(app, ai_engine, trade):
    import trading_engine
    import database as db
    import security
    import localization as loc
    import asyncio
    import time
    
    trade_id = trade.get('id')
    chat_id = trade.get('chat_id')
    symbol = trade.get('symbol')
    qty = trade.get('qty')
    buy_price = trade.get('buy_price')
    current_highest = trade.get('current_highest')
    stop_loss_pct = trade.get('stop_loss_pct')
    scale_out_level = trade.get('scale_out_level', 0)
    initial_qty = trade.get('initial_qty', qty)
    
    current_price = await asyncio.to_thread(trading_engine.get_current_price, symbol)
    if not current_price or current_price <= 0:
        return
        
    # --- Scale-Out Logic (Fee-Adjusted Net PnL) ---
    profit_pct = trading_engine.calculate_net_pnl_pct(buy_price, current_price) if buy_price and buy_price > 0 else 0.0
    
    if profit_pct >= 5.0 and scale_out_level == 0:
        prompt = f"We are holding {symbol} and it's currently up {profit_pct:.2f}%. Should we take 20% profit now (SCALE OUT) or HOLD for more gains based on current momentum? Answer exactly 'SCALE OUT' or 'HOLD'."
        ai_resp = await asyncio.to_thread(ai_engine.analyze_opportunity, prompt)
        if "HOLD" in ai_resp.upper():
            print(f"AI decided to HOLD {symbol} at {profit_pct:.2f}% profit instead of scaling out early.")
            return
            
        sell_qty = initial_qty * 0.20
        if sell_qty <= qty:
            keys = await asyncio.to_thread(db.get_user_api, chat_id)
            if keys:
                api_key, api_secret = keys[0], keys[1]
                base_asset = symbol[:-4]
                actual_coin_balance = await asyncio.to_thread(trading_engine.get_spot_balance, api_key, api_secret, base_asset)
                actual_sell_qty = min(sell_qty, actual_coin_balance)
                
                if actual_sell_qty > 0:
                    result = await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, symbol, actual_sell_qty)
                else:
                    result = {"error": "Insufficient Coin Balance (Asset Guard)"}
                    
                if "status" in result and result["status"] == "FILLED":
                    new_qty = qty - sell_qty
                    await asyncio.to_thread(db.update_trade_qty_and_scale, trade_id, new_qty, 1)
                    qty = new_qty
                    user_lang = await asyncio.to_thread(db.get_user_language, chat_id)
                    alert_msg = loc.get_text(user_lang, 'scale_out_success', level=1, symbol=symbol, price=current_price, profit_pct=profit_pct, sold_qty=sell_qty, remaining_qty=qty)
                    try: await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                    except: pass
                elif "error" in result or "code" in result:
                    err_code = result.get("code")
                    if err_code in [-2010, -1013, -1111, -2015, -2014, -2011, -1021]:
                        await asyncio.to_thread(db.update_trade_qty_and_scale, trade_id, qty, 1)
                        try: await app.bot.send_message(chat_id=chat_id, text=f"⚠️ រំលងការលក់ Scale Out កម្រិត 1 សម្រាប់ {symbol} ដោយសារកំហុស។")
                        except: pass

    elif profit_pct >= 10.0 and scale_out_level == 1:
        prompt = f"We are holding {symbol} and it's currently up {profit_pct:.2f}%. Should we take another 30% profit now (SCALE OUT) or HOLD for more gains? Answer exactly 'SCALE OUT' or 'HOLD'."
        ai_resp = await asyncio.to_thread(ai_engine.analyze_opportunity, prompt)
        if "HOLD" in ai_resp.upper():
            return
            
        sell_qty = initial_qty * 0.30
        if sell_qty <= qty:
            keys = await asyncio.to_thread(db.get_user_api, chat_id)
            if keys:
                api_key, api_secret = keys[0], keys[1]
                base_asset = symbol[:-4]
                actual_coin_balance = await asyncio.to_thread(trading_engine.get_spot_balance, api_key, api_secret, base_asset)
                actual_sell_qty = min(sell_qty, actual_coin_balance)
                
                if actual_sell_qty > 0:
                    result = await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, symbol, actual_sell_qty)
                else:
                    result = {"error": "Insufficient Coin Balance (Asset Guard)"}
                    
                if "status" in result and result["status"] == "FILLED":
                    new_qty = qty - sell_qty
                    await asyncio.to_thread(db.update_trade_qty_and_scale, trade_id, new_qty, 2)
                    qty = new_qty
                    user_lang = await asyncio.to_thread(db.get_user_language, chat_id)
                    alert_msg = loc.get_text(user_lang, 'scale_out_success', level=2, symbol=symbol, price=current_price, profit_pct=profit_pct, sold_qty=sell_qty, remaining_qty=qty)
                    try: await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                    except: pass
                elif "error" in result or "code" in result:
                    err_code = result.get("code")
                    if err_code in [-2010, -1013, -1111, -2015, -2014, -2011, -1021]:
                        await asyncio.to_thread(db.update_trade_qty_and_scale, trade_id, qty, 2)

    # --- Trailing Stop-Loss Logic ---
    if current_price > current_highest:
        await asyncio.to_thread(db.update_active_trade_highest, trade_id, current_price)
        current_highest = current_price
        
    # ⚡ Sub-Second 0.1% Retracement Trailing Take-Profit Peak Lock:
    net_profit_pct = trading_engine.calculate_net_pnl_pct(buy_price, current_price) if buy_price and buy_price > 0 else 0.0
    trailing_peak_lock = (net_profit_pct > 1.0) and (current_price <= current_highest * 0.999)
    
    stop_loss_price = current_highest * (1 - (stop_loss_pct / 100.0))
    
    if (current_price <= stop_loss_price or trailing_peak_lock) and qty > 0:

        execute_sell = True
        
        # --- AI Wave Rider Safety Logic ---
        net_profit_pct = trading_engine.calculate_net_pnl_pct(buy_price, current_price) if buy_price and buy_price > 0 else 0.0
        wave_rider_enabled = await asyncio.to_thread(db.is_wave_rider_enabled, chat_id)
        
        if wave_rider_enabled and net_profit_pct > 1.0:
            import market_data
            df, _, _ = await asyncio.to_thread(market_data.fetch_binance_data, symbol, interval="15m", limit=30)
            if df is not None and not df.empty:
                latest_rsi = df['rsi'].iloc[-1]
                latest_macd = df['macd'].iloc[-1]
                latest_signal = df['macd_signal'].iloc[-1]
                if latest_rsi > 55 and latest_macd > latest_signal:
                    execute_sell = False
                    user_lang = await asyncio.to_thread(db.get_user_language, chat_id)
                    msg = f"🌊 **AI Wave Rider Active!**\\n\\n🪙 **{symbol}**\\n📈 **Momentum:** Strong (RSI: {latest_rsi:.1f})\\n🛡️ **Profit Secured:** +{net_profit_pct:.2f}%\\n🤖 **Action:** Letting position consolidate in profit."
                    try: await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                    except: pass

                    
        if not execute_sell:
            return
            
        keys = await asyncio.to_thread(db.get_user_api, chat_id)
        if keys:
            api_key, api_secret = keys[0], keys[1]
            base_asset = symbol[:-4]
            actual_coin_balance = await asyncio.to_thread(trading_engine.get_spot_balance, api_key, api_secret, base_asset)
            actual_sell_qty = min(qty, actual_coin_balance)
            
            if actual_sell_qty > 0:
                result = await asyncio.to_thread(trading_engine.place_smart_market_sell, api_key, api_secret, symbol, actual_sell_qty)
            else:
                result = {"error": "Insufficient Coin Balance (Asset Guard)"}
                
            if "status" in result and result["status"] == "FILLED":
                await asyncio.to_thread(db.remove_active_trade, trade_id, current_price, "TRAILING_STOP")
                _, pl_pct = trading_engine.calculate_net_pnl(buy_price, current_price, actual_sell_qty)
                
                # Caching for Re-entry if profit > 1.0%
                if pl_pct > 1.0:
                    sold_usdt = actual_sell_qty * current_price
                    RECENTLY_SOLD_CACHE[symbol] = {
                        "sell_time": time.time(),
                        "sell_price": current_price,
                        "chat_id": chat_id,
                        "capital": sold_usdt
                    }
                    print(f"🔄 Added {symbol} to Auto-Reentry Cache for 30 minutes.")
                else:
                    REENTRY_LOCKOUT_CACHE[symbol] = time.time()
                    print(f"🔒 [LOCKOUT GUARD] Added {symbol} to 60-minute Re-entry Lockout Cache (loss/breakeven trade).")
                
                user_lang = await asyncio.to_thread(db.get_user_language, chat_id)
                emoji = "🤑" if pl_pct > 0 else "🛡️"
                result_msg = loc.get_text(user_lang, 'profit') if pl_pct > 0 else loc.get_text(user_lang, 'break_even')
                alert_msg = loc.get_text(user_lang, 'trailing_stop_triggered', symbol=symbol, current_price=current_price, highest=current_highest, emoji=emoji, result_msg=result_msg, pl_pct=pl_pct)
                try: await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                except: pass
            elif "error" in result or "code" in result:
                err_code = result.get("code")
                if err_code in [-2010, -1013, -1111, -2015, -2014, -2011, -1021]:
                    await asyncio.to_thread(db.remove_active_trade, trade_id, 0.0, f"API_ERROR_{err_code}")

async def trailing_stop_monitor(app: Application, ai_engine):
    import database as db
    import asyncio
    try:
        active_trades = await asyncio.to_thread(db.get_all_active_trades)
        if not active_trades:
            return
            
        tasks = [process_single_trailing_stop(app, ai_engine, trade) for trade in active_trades]
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error in trailing stop monitor: {e}")

async def auto_reentry_monitor(app: Application):
    import time
    import asyncio
    import trading_engine
    import market_data
    import database as db
    
    try:
        current_time = time.time()
        to_remove = []
        for symbol, data in RECENTLY_SOLD_CACHE.items():
            if current_time - data["sell_time"] > REENTRY_COOLDOWN:
                to_remove.append(symbol)
                continue
                
            # 🛡️ 1. Anti-Whipsaw Guard: Check Lockout
            if symbol in REENTRY_LOCKOUT_CACHE:
                if current_time - REENTRY_LOCKOUT_CACHE[symbol] < REENTRY_LOCKOUT_COOLDOWN:
                    print(f"🔒 [ANTI-WHIPSAW GUARD] {symbol} is locked out for 60m due to recent loss. Skipping re-entry.")
                    to_remove.append(symbol)
                    continue
                else:
                    del REENTRY_LOCKOUT_CACHE[symbol]
                
            # Check 5m candle momentum & breakout
            df_5m, _, _ = await asyncio.to_thread(market_data.fetch_binance_data, symbol, interval="5m", limit=30)
            if df_5m is not None and not df_5m.empty:
                latest_macd = df_5m['macd'].iloc[-1]
                latest_signal = df_5m['macd_signal'].iloc[-1]
                prev_macd = df_5m['macd'].iloc[-2]
                prev_signal = df_5m['macd_signal'].iloc[-2]
                current_price = df_5m['close'].iloc[-1]
                sell_price = data.get("sell_price", 0)
                
                # 🛡️ 2. Price Breakout Guard: Must break above previous sell price (>= sell_price * 1.002)
                if sell_price > 0 and current_price < sell_price * 1.002:
                    continue
                
                # Bullish Cross Detection on 5m
                if prev_macd <= prev_signal and latest_macd > latest_signal:
                    # 🛡️ 3. Multi-Timeframe Confirmation: Check 15m RSI > 50
                    df_15m, _, _ = await asyncio.to_thread(market_data.fetch_binance_data, symbol, interval="15m", limit=30)
                    if df_15m is not None and not df_15m.empty:
                        rsi_15m = df_15m['rsi'].iloc[-1]
                        if rsi_15m < 50.0:
                            print(f"⚠️ [ANTI-WHIPSAW GUARD] Re-entry rejected for {symbol}: 15m RSI is {rsi_15m:.1f} (<50). Weak trend.")
                            continue

                    # Valid Re-entry!

                    chat_id = data["chat_id"]
                    capital = data["capital"]
                    
                    print(f"🚀 AUTO-REENTRY TRIGGERED FOR {symbol}!")
                    
                    keys = await asyncio.to_thread(db.get_user_api, chat_id)
                    if keys:
                        api_key, api_secret = keys[0], keys[1]
                        buy_res = await asyncio.to_thread(trading_engine.place_market_buy, api_key, api_secret, symbol, capital)
                        if "status" in buy_res and buy_res["status"] == "FILLED":
                            executed_qty = float(buy_res.get("executedQty", 0))
                            avg_price = float(buy_res.get("fills", [{}])[0].get("price", 0))
                            if avg_price > 0:
                                await asyncio.to_thread(db.add_active_trade, chat_id, symbol, executed_qty, avg_price)
                                try:
                                    msg = f"🚀 **AUTO RE-ENTRY EXECUTED!**\\n\\n🪙 **{symbol}** has regained bullish momentum.\\n💰 Re-invested: **${capital:.2f}**\\n🎯 Entry Price: **${avg_price}**\\n\\n*Trailing stop is now active.*"
                                    await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                                except: pass
                    
                    to_remove.append(symbol)
                    
        for sym in to_remove:
            if sym in RECENTLY_SOLD_CACHE:
                del RECENTLY_SOLD_CACHE[sym]
                
    except Exception as e:
        print(f"Error in auto re-entry monitor: {e}")

"""
    
    content = content[:start_idx] + new_code + "\n" + content[end_idx:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find start or end index.")
