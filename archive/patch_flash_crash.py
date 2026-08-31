import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
if 'async def flash_crash_defender' not in content:
    defender_code = '''
# In-memory buffer for BTCUSDT prices
price_buffer = []

async def flash_crash_defender(app: Application, ai_engine=None):
    """Monitors BTCUSDT for a rapid 5% drop in 60s. Auto-liquidates altcoins if triggered."""
    global price_buffer
    try:
        import time
        import database as db
        import trading_engine
        
        symbol = "BTCUSDT"
        current_price = trading_engine.get_current_price(symbol)
        
        if current_price <= 0:
            return
            
        current_time = time.time()
        price_buffer.append((current_time, current_price))
        
        # Remove prices older than 60 seconds
        price_buffer = [p for p in price_buffer if current_time - p[0] <= 60]
        
        if len(price_buffer) < 2:
            return
            
        max_price_in_window = max(p[1] for p in price_buffer)
        drop_pct = ((max_price_in_window - current_price) / max_price_in_window) * 100
        
        # Check if drop exceeds 5%
        if drop_pct >= 5.0:
            # Check if alerted recently (prevent spam)
            alert_id = f"flash_crash_{int(current_time // 3600)}" # Once per hour max
            if db.is_economic_event_alerted(alert_id):
                return
            db.mark_economic_event_alerted(alert_id)
            
            print(f"🚨 FLASH CRASH DETECTED: {drop_pct:.2f}% drop in 60s! Liquidating altcoins...")
            
            vip_users_lang = db.get_vip_users_with_lang()
            if not vip_users_lang:
                return
                
            safe_assets = ["BTC", "ETH", "USDT", "USDC", "FDUSD", "USDE"]
            
            ai_analysis = ""
            if ai_engine:
                prompt = f"Bitcoin just flash crashed by {drop_pct:.2f}% in the last 60 seconds. What is the best strategy for a crypto trader right now? Respond in 2 sentences in Khmer."
                try:
                    ai_analysis = ai_engine.analyze_opportunity(prompt)
                except:
                    ai_analysis = "ទីផ្សារកំពុងបាក់ស្រុត! ត្រូវចេះការពារដើមទុនជាចម្បង។"
            
            for row in vip_users_lang:
                chat_id = row[0]
                user_lang = row[1] if len(row) > 1 else 'khmer'
                
                config = db.get_auto_trade_config(chat_id)
                # We assume VIPs with auto_trade enabled want this protection.
                if config and config.get("enabled"):
                    keys = db.get_user_api(chat_id)
                    if keys:
                        api_key, api_secret = keys[0], keys[1]
                        balances = trading_engine.get_all_spot_balances(api_key, api_secret)
                        
                        liquidated_assets = []
                        for asset, amount in balances.items():
                            if asset not in safe_assets:
                                # We need to check if value > $5
                                asset_symbol = f"{asset}USDT"
                                asset_price = trading_engine.get_current_price(asset_symbol)
                                if asset_price > 0 and (amount * asset_price) >= 5.0:
                                    res = trading_engine.place_market_sell(api_key, api_secret, asset_symbol, amount)
                                    if res.get("status") == "FILLED":
                                        liquidated_assets.append(f"{amount:.2f} {asset}")
                        
                        action_taken = ""
                        if liquidated_assets:
                            action_taken = "\\n✅ **បានលក់:** " + ", ".join(liquidated_assets)
                        else:
                            action_taken = "\\n✅ គ្មាន Altcoins ណាដែលមានហានិភ័យទេ (Safe)."
                            
                        alert_msg = (f"🛡️ **FLASH CRASH DEFENDER** 🛡️\\n\\n"
                                     f"🚨 **Bitcoin ធ្លាក់ចុះ {drop_pct:.2f}% ក្នងពេល ៦០វិនាទី!**\\n"
                                     f"🔄 Bot បានទាញយកលុយចូល USDT ដោយស្វ័យប្រវត្តិដើម្បីការពារដើមទុន។\\n"
                                     f"{action_taken}\\n\\n"
                                     f"💡 **AI វិភាគ:** {ai_analysis}")
                        
                        try:
                            await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                        except Exception:
                            pass
    except Exception as e:
        print(f"Error in Flash Crash Defender: {e}")
'''
    with open('scheduler_tasks.py', 'a', encoding='utf-8') as f:
        f.write(defender_code)
    print("Added flash_crash_defender")
else:
    print("flash_crash_defender already exists")
