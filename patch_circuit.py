import re

with open('circuit_breaker.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_logic = '''
                    # Engage Hedge Mode if user has futures enabled
                    hedge_config = db.get_hedge_mode_config(chat_id)
                    api = db.get_user_api(chat_id)
                    if hedge_config and api:
                        enabled, amount, leverage = hedge_config
                        api_key, api_secret = api
                        
                        if enabled:
                            # Execute short
                            res = await asyncio.to_thread(trading_engine.place_futures_short, api_key, api_secret, symbol, amount, leverage, 1500.0)
                            if res and res.get('success'):
                                await self.bot_app.bot.send_message(chat_id=chat_id, text=f"✅ Hedge Mode Activated: Shorting {symbol} at {leverage}x with ${amount}")
'''

new_logic = '''
                    # 🚀 SUPER SMART: AI-Powered Hedge Mode
                    hedge_config = db.get_hedge_mode_config(chat_id)
                    api = db.get_user_api(chat_id)
                    
                    if hedge_config and api:
                        enabled = hedge_config.get("enabled", False)
                        amount = hedge_config.get("amount", 50.0)
                        base_leverage = hedge_config.get("leverage", 5)
                        api_key, api_secret = api
                        
                        if enabled:
                            # 1. AI Dynamic Leverage (Consult AI for real-time volatility)
                            # Dynamic Leverage takes over if market is highly volatile to prevent liquidation of the hedge itself
                            dynamic_leverage = await asyncio.to_thread(trading_engine.calculate_ai_dynamic_leverage, symbol, int(base_leverage), 80.0)
                            
                            # 2. USDT Liquidity Guard (Ensure we have enough balance to execute the hedge)
                            available_usdt = await asyncio.to_thread(trading_engine.get_futures_balance, api_key, api_secret, "USDT")
                            actual_amount = min(amount, available_usdt)
                            
                            if actual_amount < 5.0:
                                await self.bot_app.bot.send_message(chat_id=chat_id, text=f"⚠️ Hedge Mode Failed: Insufficient Futures USDT (${available_usdt:.2f})")
                                continue
                                
                            # 3. Execute Hedge Short
                            res = await asyncio.to_thread(trading_engine.place_futures_short, api_key, api_secret, symbol, margin_usdt=actual_amount, leverage=dynamic_leverage, vol_target=1500.0)
                            
                            if res and res.get('success'):
                                downsize_msg = f" (Auto-Resized to available balance)" if actual_amount < amount else ""
                                
                                await self.bot_app.bot.send_message(
                                    chat_id=chat_id, 
                                    text=f"🚨 **SUPER SMART HEDGE ACTIVATED!** 🚨\\n\\n"
                                         f"🪙 **កាក់:** `{symbol}`\\n"
                                         f"🛡️ **ទំហំការពារ:** ${actual_amount:.2f}{downsize_msg}\\n"
                                         f"⚙️ **Dynamic Leverage:** {dynamic_leverage}x (AI Adjusted)\\n\\n"
                                         f"_(ប្រព័ន្ធបានបើកការ Short ស្វ័យប្រវត្តិដើម្បីទប់ទល់នឹងការធ្លាក់ចុះនៃទីផ្សារ!)_"
                                )
'''

new_code = code.replace(old_logic.strip(), new_logic.strip())

with open('circuit_breaker.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print('Patched circuit_breaker.py hedge mode!')
