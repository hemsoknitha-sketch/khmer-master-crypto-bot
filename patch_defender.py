import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_logic = '''
                if diff_pct < 0.05:
                    side = "LONG" if amt > 0 else "SHORT"
                    reduce_qty = abs(amt) * 0.25
                    reduce_qty = round(reduce_qty, 3)
                    
                    if reduce_qty > 0:
                        res = await asyncio.to_thread(trading_engine.emergency_reduce_position, api_key, api_secret, symbol, side, reduce_qty)
'''

new_logic = '''
                # 🚀 SUPER SMART: AI-Powered Liquidation Defender
                if diff_pct < 0.08: # Widened trigger zone to 8% for earlier defense
                    side = "LONG" if amt > 0 else "SHORT"
                    
                    # 1. Consult AI Engine for immediate market direction
                    prediction = await asyncio.to_thread(ai_engine.predict, symbol)
                    
                    reduction_ratio = 0.25 # Default 25% reduction
                    ai_action = "កាត់បន្ថយធម្មតា (25%)"
                    
                    if prediction:
                        pred_dir = prediction.get('prediction', '')
                        conf = prediction.get('confidence', 50)
                        
                        # If we are LONG but AI predicts BEARISH dump
                        if side == "LONG" and pred_dir == "BEARISH":
                            if conf >= 75:
                                reduction_ratio = 1.0
                                ai_action = "បិទចោលទាំងស្រុង (100%) ព្រោះ AI ព្យាករណ៍ថាទីផ្សារនឹងបន្តធ្លាក់កប់!"
                            else:
                                reduction_ratio = 0.50
                                ai_action = "កាត់បន្ថយពាក់កណ្តាល (50%) ព្រោះ AI ឃើញសញ្ញាធ្លាក់ចុះបន្ត។"
                                
                        # If we are SHORT but AI predicts BULLISH pump
                        elif side == "SHORT" and pred_dir == "BULLISH":
                            if conf >= 75:
                                reduction_ratio = 1.0
                                ai_action = "បិទចោលទាំងស្រុង (100%) ព្រោះ AI ព្យាករណ៍ថាទីផ្សារនឹងបន្តហោះឡើង!"
                            else:
                                reduction_ratio = 0.50
                                ai_action = "កាត់បន្ថយពាក់កណ្តាល (50%) ព្រោះ AI ឃើញសញ្ញាហោះឡើងបន្ត។"
                    
                    raw_reduce_qty = abs(amt) * reduction_ratio
                    # 2. Format with exact Binance Futures Lot Size precision
                    reduce_qty = await asyncio.to_thread(trading_engine.get_futures_max_sellable_qty, symbol, raw_reduce_qty)
                    
                    if reduce_qty > 0:
                        res = await asyncio.to_thread(trading_engine.emergency_reduce_position, api_key, api_secret, symbol, side, reduce_qty)
'''

new_code = code.replace(old_logic.strip(), new_logic.strip())

# Also update the telegram message to include the AI action
old_msg = '''
                        msg = (f"🚨 **LIQUIDATION DEFENDER TRIGGERED!** 🚨\\n\\n"
                               f"🪙 **កាក់:** `{symbol}`\\n"
                               f"⚠️ **ហានិភ័យ:** តម្លៃទីផ្សារ (${mark_price}) ខិតជិតតម្លៃ Liquidation (${liq_price}) ណាស់!\\n"
                               f"🛡️ **សកម្មភាពសង្គ្រោះ:** ប្រព័ន្ធទើបតែកាត់បន្ថយ Position ចំនួន 25% ({reduce_qty} គ្រាប់) ដោយស្វ័យប្រវត្តិ ដើម្បីជៀសវាងការឆេះគណនីទាំងមូល。\\n\\n"
                               f"_(សូមពិនិត្យមើលគណនី Futures របស់អ្នកជាបន្ទាន់!)_")
'''

new_msg = '''
                        msg = (f"🚨 **SUPER SMART DEFENDER TRIGGERED!** 🚨\\n\\n"
                               f"🪙 **កាក់:** `{symbol}`\\n"
                               f"⚠️ **ហានិភ័យ:** តម្លៃទីផ្សារ (${mark_price}) ខិតជិតតម្លៃ Liquidation (${liq_price}) ណាស់!\\n"
                               f"🧠 **សកម្មភាព AI:** {ai_action}\\n"
                               f"🛡️ **កាត់បន្ថយ:** {reduce_qty} {symbol}\\n\\n"
                               f"_(សូមពិនិត្យមើលគណនី Futures របស់អ្នកជាបន្ទាន់!)_")
'''

new_code = new_code.replace(old_msg.strip(), new_msg.strip())

with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print('Updated liquidation defender!')
