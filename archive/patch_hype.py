import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'async def check_social_hype' not in content:
    hype_code = '''
async def check_social_hype(app: Application, ai_engine=None):
    """Fetches trending coins from CoinGecko, analyzes social hype via AI, and auto-buys if score >= 75%."""
    print("🧠 Checking AI Social Sentiment & Hype Predictor...")
    try:
        import time
        from datetime import datetime
        import requests
        import database as db
        import trading_engine
        import re
        
        url = "https://api.coingecko.com/api/v3/search/trending"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return
            data = response.json()
        except Exception:
            return
            
        vip_users_lang = db.get_vip_users_with_lang()
        if not vip_users_lang:
            return
            
        trending_coins = data.get("coins", [])
        if not trending_coins:
            return
            
        # Analyze top 3 trending coins
        for item in trending_coins[:3]:
            coin = item.get("item", {})
            symbol_raw = coin.get("symbol", "").upper()
            name = coin.get("name", "")
            
            if not symbol_raw:
                continue
                
            binance_symbol = f"{symbol_raw}USDT"
            
            # Check if this coin has been processed today
            today_str = datetime.now().strftime("%Y-%m-%d")
            alert_id = f"hype_{binance_symbol}_{today_str}"
            if db.is_economic_event_alerted(alert_id):
                continue
                
            # Verify it exists on Binance
            current_price = trading_engine.get_current_price(binance_symbol)
            if current_price <= 0:
                continue # Coin not on Binance
                
            db.mark_economic_event_alerted(alert_id)
            
            ai_analysis = ""
            score = 0
            if ai_engine:
                prompt = (f"The crypto token {name} ({symbol_raw}) is currently trending #1 globally in search volume and social mentions. "
                          f"The current price is ${current_price}. "
                          f"Based on market psychology and hype, give it a 'HYPE SCORE' from 0 to 100 on its potential to pump. "
                          f"Respond STRICTLY in this format: 'Score: XX% - [Reason in exactly 2 short sentences in Khmer language]'.")
                try:
                    ai_resp = ai_engine.analyze_opportunity(prompt)
                    # Extract score
                    match = re.search(r"Score:\s*(\d+)%", ai_resp, re.IGNORECASE)
                    if match:
                        score = int(match.group(1))
                    else:
                        score = 80 if "BULLISH" in ai_resp.upper() else 50
                        
                    # Extract reason
                    if "-" in ai_resp:
                        ai_analysis = ai_resp.split("-", 1)[1].strip()
                    else:
                        ai_analysis = ai_resp
                except Exception:
                    score = 0
                    ai_analysis = "⚠️ AI Analysis temporarily unavailable."
                    
            if score >= 75:
                print(f"🔥 HYPE DETECTED: {binance_symbol} Score={score}%! Executing Auto-Buys...")
                
                for row in vip_users_lang:
                    chat_id = row[0]
                    user_lang = row[1] if len(row) > 1 else 'khmer'
                    
                    config = db.get_auto_trade_config(chat_id)
                    action_taken = "No trade executed (Auto-Trade off)."
                    
                    if config and config.get("enabled"):
                        trade_amount = config.get("amount", 50.0)
                        trailing_pct = config.get("trailing_pct", 10.0)
                        
                        keys = db.get_user_api(chat_id)
                        if keys:
                            api_key, api_secret = keys[0], keys[1]
                            try:
                                qty = trade_amount / current_price
                                result = trading_engine.place_market_buy(api_key, api_secret, binance_symbol, qty)
                                if result.get("status") == "FILLED":
                                    db.add_active_trade(chat_id, binance_symbol, qty, current_price, trailing_pct)
                                    action_taken = f"✅ **Auto-Buy (Spot):** ទិញបាន {qty:.4f} {symbol_raw} @ ${current_price:,.4f}"
                                else:
                                    action_taken = f"❌ **Buy Failed:** {result.get('error')}"
                            except Exception as e:
                                action_taken = f"❌ **Execution Error:** {e}"
                                
                    alert_msg = (f"🧠 **AI SOCIAL HYPE PREDICTOR** 🧠\\n\\n"
                                 f"🔥 **Trending Coin:** #{name} ({symbol_raw})\\n"
                                 f"📊 **HYPE SCORE:** **{score}%**\\n"
                                 f"💰 **Current Price:** ${current_price:,.4f}\\n\\n"
                                 f"💡 **AI វិភាគ:** {ai_analysis}\\n\\n"
                                 f"⚡ **Bot Action:** {action_taken}")
                    
                    try:
                        await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                    except Exception:
                        pass
                        
    except Exception as e:
        print(f"Error checking social hype: {e}")
'''
    with open('scheduler_tasks.py', 'a', encoding='utf-8') as f:
        f.write(hype_code)
    print("Added check_social_hype to scheduler_tasks.py")
else:
    print("check_social_hype already exists")
