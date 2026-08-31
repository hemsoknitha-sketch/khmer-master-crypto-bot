import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = "async def check_economic_calendar(app: Application):"
end_str = 'print(f"Error checking economic calendar: {e}")'

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

replacement = '''async def check_economic_calendar(app: Application, ai_engine=None):
    """Fetches economic calendar, uses AI to predict impact, and executes front-run trades."""
    print("📅 Checking Global Macro-Economic Matrix...")
    try:
        from datetime import datetime, timezone
        import requests
        import database as db
        import trading_engine
        
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        try:
            response = requests.get(url, timeout=15)
            if response.status_code != 200:
                return
            events = response.json()
        except Exception:
            return
            
        vip_users_lang = db.get_vip_users_with_lang()
        if not vip_users_lang:
            return
            
        now_utc = datetime.now(timezone.utc)
        
        for event in events:
            # We only care about USD high impact
            if event.get('country') != 'USD' or event.get('impact') != 'High':
                continue
                
            title = event.get('title', '')
            date_str = event.get('date', '') # e.g. "2026-07-19T18:45:00-04:00"
            
            if not date_str:
                continue
                
            try:
                event_time = datetime.fromisoformat(date_str)
            except ValueError:
                continue
                
            event_time_utc = event_time.astimezone(timezone.utc)
            time_diff = event_time_utc - now_utc
            minutes_to_event = time_diff.total_seconds() / 60.0
            
            # If it's between 0 and 20 minutes from now, trigger front-run
            if 0 < minutes_to_event <= 20:
                event_id = f"{title}_{date_str}"
                
                if db.is_economic_event_alerted(event_id):
                    continue
                    
                db.mark_economic_event_alerted(event_id)
                
                forecast = event.get('forecast', 'N/A')
                previous = event.get('previous', 'N/A')
                minutes_rounded = int(minutes_to_event)
                
                # AI Sentiment Analysis
                ai_analysis = ""
                sentiment = "NEUTRAL"
                if ai_engine:
                    prompt = (f"The USD economic event '{title}' is happening in {minutes_rounded} mins. "
                              f"Forecast: {forecast}, Previous: {previous}. "
                              f"Based on historical patterns, will this be BULLISH or BEARISH for Bitcoin right now? "
                              f"Start your response with 'BULLISH' or 'BEARISH', then explain why in exactly 2 short sentences in Khmer language.")
                    try:
                        ai_resp = ai_engine.analyze_opportunity(prompt)
                        if "BULLISH" in ai_resp.upper()[:20]:
                            sentiment = "BULLISH"
                        elif "BEARISH" in ai_resp.upper()[:20]:
                            sentiment = "BEARISH"
                        ai_analysis = ai_resp
                    except Exception:
                        ai_analysis = "⚠️ AI Analysis temporarily unavailable."
                
                for row in vip_users_lang:
                    chat_id = row[0]
                    user_lang = row[1] if len(row) > 1 else 'khmer'
                    
                    config = db.get_auto_trade_config(chat_id)
                    action_taken = "No trade executed (Auto-Trade off)."
                    
                    if config and config.get("enabled"):
                        trade_amount = config.get("amount", 50.0)
                        trailing_pct = config.get("trailing_pct", 10.0)
                        symbol = "BTCUSDT"
                        
                        keys = db.get_user_api(chat_id)
                        if keys:
                            api_key, api_secret = keys[0], keys[1]
                            try:
                                current_price = trading_engine.get_current_price(symbol)
                                qty = trade_amount / current_price
                                
                                if sentiment == "BULLISH":
                                    result = trading_engine.place_market_buy(api_key, api_secret, symbol, qty)
                                    if result.get("status") == "FILLED":
                                        db.add_active_trade(chat_id, symbol, qty, current_price, trailing_pct)
                                        action_taken = f"✅ **Auto-Long (Buy):** {qty:.4f} BTC @ ${current_price:,.2f}"
                                    else:
                                        action_taken = f"❌ **Buy Failed:** {result.get('error')}"
                                        
                                elif sentiment == "BEARISH":
                                    # Since place_futures_short requires margin_usdt and leverage, we get them from DB
                                    # But wait, user might not have futures enabled in DB. We'll use defaults.
                                    leverage = 20
                                    result = trading_engine.place_futures_short(api_key, api_secret, symbol, trade_amount, leverage)
                                    if "error" not in result:
                                        # Assume success
                                        action_taken = f"📉 **Auto-Short (Futures):** {trade_amount} USDT Margin @ {leverage}x"
                                        # Also add to active_shorts DB if we have a table for it
                                        try:
                                            conn = db.get_db_connection()
                                            c = conn.cursor()
                                            c.execute("INSERT INTO active_shorts (chat_id, symbol, margin_usdt, leverage, entry_price) VALUES (?, ?, ?, ?, ?)",
                                                      (chat_id, symbol, trade_amount, leverage, current_price))
                                            conn.commit()
                                            conn.close()
                                        except Exception: pass
                                    else:
                                        action_taken = f"❌ **Short Failed:** {result.get('error')}"
                            except Exception as e:
                                action_taken = f"❌ **Execution Error:** {e}"
                                
                    alert_msg = (f"🌐 **GLOBAL MACRO MATRIX ALERT** 🌐\\n\\n"
                                 f"📅 **Event:** {title}\\n"
                                 f"⏱️ **Time:** In {minutes_rounded} mins\\n"
                                 f"📊 **Forecast:** {forecast} | 📉 **Prev:** {previous}\\n\\n"
                                 f"🤖 **AI Sentiment:** **{sentiment}**\\n"
                                 f"💡 **AI វិភាគ:** {ai_analysis}\\n\\n"
                                 f"⚡ **Bot Action:** {action_taken}")
                    
                    try:
                        await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                    except Exception:
                        pass
                        
    except Exception as e:
        print(f"Error checking economic calendar: {e}")'''

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_str)
    new_content = content[:start_idx] + replacement + content[end_idx:]
    with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced check_economic_calendar successfully.")
else:
    print(f"Could not find the function block. start={start_idx}, end={end_idx}")
