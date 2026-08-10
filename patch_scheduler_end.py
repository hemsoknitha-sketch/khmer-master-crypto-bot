import sys

filename = "scheduler_tasks.py"
with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find line containing "db.log_failed_pump(symbol)"
start_idx = -1
for i, line in enumerate(lines):
    if "db.log_failed_pump(symbol)" in line:
        start_idx = i
        break

if start_idx == -1:
    print("Could not find start index")
    sys.exit(1)

new_content = lines[:start_idx+1]
rest_of_code = """                
                # Unmute Insufficient Balance since we got USDT back
                if chat_id in GLOBAL_INSUFFICIENT_MUTE:
                    GLOBAL_INSUFFICIENT_MUTE[chat_id] = False
                
                emoji = '🟩' if profit_pct >= 0 else '🟥'
                status = "Profit Locked" if profit_pct >= 0 else "Stop Loss Hit"
                
                msg = (
                    f"🎯 **Trailing Stop Triggered! {status}!**\\n\\n"
                    f"🪙 **Symbol:** {symbol}\\n"
                    f"💰 **Sell Price:** ${current_price:,.4f}\\n"
                    f"📈 **Profit/Loss:** {profit_pct:+.2f}%\\n"
                    f"🛡️ **Reason:** Dropped {stop_loss_pct}% from highest peak (${current_highest:,.4f})\\n\\n"
                    f"_Apex AI protected your capital automatically._"
                )
                await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            else:
                print(f"⚠️ Binance Sell Failed for {symbol} Trailing Stop: {res}")
                if isinstance(res, dict) and res.get("code") == -2010:
                    print(f"🧹 Removed {symbol} from active trades (Insufficient Balance / Sold manually)")
                    db.remove_active_trade(trade_id, current_price, "INSUFFICIENT_BALANCE_REMOVED")

async def ai_order_execution_job(app: Application):
    import trading_engine
    import hft_inference
    import asyncio
    import dynamic_ranking
    
    auto_trade_users = db.get_auto_trade_users()
    if not auto_trade_users:
        return
        
    symbols_to_monitor = dynamic_ranking.get_top_500_coins()
    batch_signals = await asyncio.to_thread(hft_inference.hft_predictor.predict_batch, symbols_to_monitor)
    
    tasks = []
    for symbol, signals in batch_signals.items():
        if not signals.get("tp_signal", False):
            continue
            
        async def process_user(chat_id, sym):
            keys = db.get_user_api(chat_id)
            if not keys: return
            api_key, api_secret = keys
            
            base_coin = sym.replace("USDT", "")
            try:
                balance = await asyncio.to_thread(trading_engine.get_spot_balance, api_key, api_secret, base_coin)
                current_price = trading_engine.get_current_price(sym)
                
                if balance * current_price > 5.0:
                    max_sellable = await asyncio.to_thread(trading_engine.get_max_sellable_qty, sym, balance)
                    
                    if max_sellable > 0:
                        res = await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, sym, max_sellable)
                        
                        if "error" not in res and "code" not in res:
                            if chat_id in GLOBAL_INSUFFICIENT_MUTE:
                                GLOBAL_INSUFFICIENT_MUTE[chat_id] = False
                                
                            msg = (
                                f"🤖 **HFT AI TAKE PROFIT EXECUTED!**\\n\\n"
                                f"🪙 **Symbol:** {sym}\\n"
                                f"💰 **Sold Amount:** {max_sellable} {base_coin}\\n"
                                f"🎯 **Price:** ${current_price:,.4f}\\n\\n"
                                f"_The AI detected a market top and secured your profits automatically in milliseconds!_"
                            )
                            await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                        else:
                            print(f"HFT Take Profit rejected by Binance for {sym}: {res}")
            except Exception as e:
                print(f"HFT Auto-Trade TP failed for {chat_id} on {sym}: {e}")
                
        for chat_id in auto_trade_users:
            tasks.append(process_user(chat_id, symbol))
            
    if tasks:
        await asyncio.gather(*tasks)

async def smart_portfolio_rebalancer(app: Application, ai_engine):
    import database as db
    import binance_api as bapi
    import asyncio
    
    try:
        if not db.is_global_rebalance_enabled():
            return
            
        vip_users = db.get_vip_users_with_lang()
        if not vip_users: return
        
        for user_record in vip_users:
            user_id = user_record[0]
            if not db.is_auto_trade_enabled(user_id):
                continue
            if not db.is_user_opted_in_rebalance(user_id):
                continue
            if not db.can_user_rebalance(user_id):
                continue
                
            active_trades = db.get_active_trades_by_user(user_id)
            if not active_trades:
                continue
                
            for trade in active_trades:
                trade_id, symbol, qty, buy_price, _, _ = trade
                
                if buy_price <= 0: continue
                current_price = bapi.get_current_price(symbol)
                if not current_price: continue
                
                pnl_pct = ((current_price - buy_price) / buy_price) * 100
                if pnl_pct >= 0:
                    continue
                    
                trend_signal = "NEUTRAL"
                atr = current_price * 0.05
                try:
                    trend_signal = ai_engine.predict_trend(symbol)
                    if hasattr(ai_engine, "get_atr"):
                        atr_val = ai_engine.get_atr(symbol)
                        if atr_val: atr = atr_val
                except Exception:
                    pass
                    
                if trend_signal not in ["BEARISH", "STRONG_BEARISH"]:
                    continue
                    
                loss_threshold = (1.5 * atr / current_price) * 100
                if abs(pnl_pct) < loss_threshold:
                    continue
                
                import rvol_engine
                top_5 = []
                try:
                    top_5 = rvol_engine.get_top_rvol(limit=5)
                except Exception:
                    pass
                    
                best_candidate = None
                best_conf = 0.0
                
                for cand in top_5:
                    if cand == symbol: continue
                    try:
                        conf = ai_engine.predict_price_confidence(cand)
                        if conf > 65.0 and conf > best_conf:
                            best_candidate = cand
                            best_conf = conf
                    except Exception:
                        pass
                
                try:
                    sell_res = bapi.execute_sell(symbol, qty)
                    if not sell_res: continue
                    
                    db.remove_active_trade(trade_id, exit_price=current_price, pnl_pct=pnl_pct, reason="SMART_REBALANCE")
                    
                    if not best_candidate:
                        msg = f"🔄 <b>Smart Portfolio Rebalance</b>\\n\\n📉 កាត់ខាត <b>{symbol}</b> ({pnl_pct:.2f}%)\\n⚠️ មូលហេតុ: Loss > 1.5 ATR + <b>BEARISH</b> AI\\n💵 រក្សាទុនជា USDT សិន ព្រោះគ្មានកាក់ថ្មីដែល AI ជឿជាក់លើស 65%។"
                        await app.bot.send_message(user_id, text=msg, parse_mode="HTML")
                        db.increment_user_rebalance(user_id)
                        continue
                        
                    orderbook = bapi.get_order_book(best_candidate)
                    if not orderbook or not orderbook.get('bids'):
                        continue
                    best_bid = float(orderbook['bids'][0][0])
                    recovered_usdt = float(qty) * float(current_price) * 0.999
                    
                    buy_qty = recovered_usdt / best_bid
                    buy_qty = bapi.adjust_quantity(best_candidate, buy_qty)
                    
                    buy_res = bapi.execute_limit_buy(best_candidate, buy_qty, best_bid)
                    if buy_res:
                        db.add_active_trade(user_id, best_candidate, buy_qty, best_bid, current_highest=best_bid, stop_loss_pct=0.0)
                        msg = f"🔄 <b>Smart Portfolio Rebalance</b>\\n\\n📉 កាត់ខាត <b>{symbol}</b> ({pnl_pct:.2f}%)\\n🚀 ទិញចូលជំនួស <b>{best_candidate}</b> ចំនួន {buy_qty} នៅតម្លៃ <b>{best_bid}</b> (Limit)\\n🤖 AI Confidence: <b>{best_conf:.1f}%</b>\\n📊 ឱកាសស្រង់ដើម និងយកចំណេញលឿនពី RVOL Spike!"
                        await app.bot.send_message(user_id, text=msg, parse_mode="HTML")
                        db.increment_user_rebalance(user_id)
                        
                except Exception as e:
                    print(f"Rebalance Execution Error: {e}")
                    
    except Exception as e:
        print(f"Smart Rebalancer Error: {e}")

VPS_STRIKE_COUNT = 0

async def vps_health_monitor_job(app: Application):
    global VPS_STRIKE_COUNT
    try:
        import psutil
        import asyncio
        import gc
        
        cpu_usage = await asyncio.to_thread(psutil.cpu_percent, interval=0.1)
        ram = await asyncio.to_thread(psutil.virtual_memory)
        ram_percent = ram.percent
        
        if cpu_usage > 90 or ram_percent > 90:
            VPS_STRIKE_COUNT += 1
            print(f"⚠️ [VPS HEALTH] CPU: {cpu_usage}%, RAM: {ram_percent}%. Strike: {VPS_STRIKE_COUNT}/3. Initiating Self-Healing (GC)...")
            
            gc.collect()
            
            if VPS_STRIKE_COUNT >= 3:
                admin_id = "859271875"
                msg = (
                    f"🔴 **CRITICAL SYSTEM ALERT** 🔴\\n\\n"
                    f"⚠️ **VPS Load is exceeding safe limits for 15+ minutes!**\\n"
                    f"🧠 **CPU Usage:** `{cpu_usage}%`\\n"
                    f"📊 **RAM Usage:** `{ram_percent}%`\\n"
                    f"🛠️ _Self-healing attempted but failed. Manual intervention required._"
                )
                try:
                    await app.bot.send_message(chat_id=admin_id, text=msg, parse_mode="Markdown")
                except Exception as e:
                    print(f"Failed to send health alert to Admin: {e}")
                
                VPS_STRIKE_COUNT = 0
        else:
            if VPS_STRIKE_COUNT > 0:
                print(f"✅ [VPS HEALTH] System recovered. CPU: {cpu_usage}%, RAM: {ram_percent}%. Resetting strikes.")
                VPS_STRIKE_COUNT = 0
                
    except Exception as e:
        print(f"VPS Health Monitor Error: {e}")

async def database_backup_job(app: Application):
    import shutil
    import os
    import time
    from datetime import datetime
    
    try:
        db_path = "Apex_AI_Bot.db"
        backup_dir = "backups"
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        if not os.path.exists(db_path):
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H")
        backup_filename = f"Apex_AI_Bot_{timestamp}.db"
        backup_filepath = os.path.join(backup_dir, backup_filename)
        
        shutil.copy2(db_path, backup_filepath)
        print(f"💾 [AUTO-BACKUP] Database backed up to {backup_filename}")
        
        now = time.time()
        retention_seconds = 48 * 3600
        
        for filename in os.listdir(backup_dir):
            if filename.endswith(".db"):
                filepath = os.path.join(backup_dir, filename)
                file_age = now - os.path.getmtime(filepath)
                if file_age > retention_seconds:
                    try:
                        os.remove(filepath)
                        print(f"🗑️ [AUTO-BACKUP] Deleted old backup: {filename}")
                    except:
                        pass
                    
    except Exception as e:
        print(f"Database Backup Error: {e}")
"""

with open(filename, "w", encoding="utf-8") as f:
    f.writelines(new_content)
    f.write(rest_of_code)

print("Successfully patched scheduler_tasks.py")
