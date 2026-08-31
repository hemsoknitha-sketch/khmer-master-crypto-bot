import re

with open('scheduler_tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = "async def check_smart_money(app: Application):"
end_str = 'print(f"Error in Smart Money Tracker: {e}")'

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

replacement = '''async def check_smart_money(app: Application, ai_engine=None):
    """Tracks Whale wallets using Blockscout API (tokentx) and executes Mirror Trading."""
    print("🕵️‍♂️ Checking Smart Money Tracker (Whales) for Copy Trades...")
    try:
        import database as db
        vip_users_lang = db.get_vip_users_with_lang()
        if not vip_users_lang:
            return
            
        wallets = {
            "Vitalik Buterin": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
            "Justin Sun": "0x3DdfA8eC3052539b6C9549F12cEA2C295cfF5296",
            "Wintermute": "0xdbF5E9c5206d0dB70a90108bf936DA60221dC080",
            "Jump Trading": "0x0000000000000000000000000000000000000000" # Just an example, let's keep it 3 for now
        }
        del wallets["Jump Trading"]
        
        import requests
        import trading_engine
        
        for whale_name, wallet_address in wallets.items():
            url = f"https://eth.blockscout.com/api?module=account&action=tokentx&address={wallet_address}&page=1&offset=5&sort=desc"
            
            try:
                res = requests.get(url, timeout=10)
                if res.status_code != 200:
                    continue
                data = res.json()
            except Exception:
                continue
                
            if data.get("status") != "1" or not data.get("result"):
                continue
                
            txs = data["result"]
            
            for tx in txs:
                tx_hash = tx.get("hash")
                if not tx_hash: continue
                
                # Check if we already processed this tx
                if db.is_tx_alerted(tx_hash):
                    continue
                    
                db.mark_tx_alerted(tx_hash)
                
                # Only trigger on incoming tokens
                to_addr = tx.get("to", "").lower()
                if to_addr != wallet_address.lower():
                    continue
                    
                token_symbol = tx.get("tokenSymbol", "")
                if not token_symbol or token_symbol in ["USDT", "USDC", "WETH", "ETH", "USDe"]:
                    continue # Ignore stablecoins
                    
                decimals = int(tx.get("tokenDecimal", 18))
                value = float(tx.get("value", 0)) / (10 ** decimals)
                
                # Filter out tiny dust amounts. Whales move big money.
                if value < 1000:
                    continue
                    
                binance_symbol = f"{token_symbol}USDT".upper()
                
                # Use AI Engine to analyze
                ai_analysis = ""
                if ai_engine:
                    prompt = f"The billionaire whale '{whale_name}' just accumulated {value:,.0f} of '{token_symbol}' token on-chain. Why would a whale buy this now? Explain the potential impact on {binance_symbol} in exactly 2 short sentences in Khmer language."
                    try:
                        ai_analysis = ai_engine.analyze_opportunity(prompt)
                    except Exception:
                        ai_analysis = "🚀 មានលំហូរទុនធំចូលទីផ្សារ! (AI Analysis Temporarily Unavailable)"
                
                for row in vip_users_lang:
                    chat_id = row[0]
                    user_lang = row[1] if len(row) > 1 else 'khmer'
                    
                    # Check auto-trade config
                    config = db.get_auto_trade_config(chat_id)
                    
                    if config and config.get("enabled"):
                        trade_amount = config.get("amount", 50.0)
                        trailing_pct = config.get("trailing_pct", 10.0)
                        
                        try:
                            current_price = trading_engine.get_current_price(binance_symbol)
                            if current_price > 0:
                                qty = trade_amount / current_price
                                keys = db.get_user_api(chat_id)
                                if keys:
                                    api_key, api_secret = keys[0], keys[1]
                                    result = trading_engine.place_market_buy(api_key, api_secret, binance_symbol, qty)
                                    if "status" in result and result["status"] == "FILLED":
                                        db.add_active_trade(chat_id, binance_symbol, qty, current_price, trailing_pct)
                                        alert_msg = (f"🐋 **WHALE COPY-TRADE SUCCESS!**\\n"
                                                     f"👤 **Whale:** {whale_name}\\n"
                                                     f"🪙 **Token:** {value:,.0f} {token_symbol}\\n"
                                                     f"🤖 **Bot Action:** Bought {qty:.4f} {binance_symbol} @ ${current_price}\\n\\n"
                                                     f"💡 **AI វិភាគ:**\\n{ai_analysis}")
                                        await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                                    elif "error" in result:
                                        error_msg = f"❌ ទិញបរាជ័យ (Mirror Trade - {binance_symbol}): {result['error']}"
                                        await app.bot.send_message(chat_id=chat_id, text=error_msg)
                        except Exception as e:
                            print(f"Error mirroring trade for {chat_id}: {e}")
                    else:
                        # Standard alert if auto-trade is disabled
                        alert_msg = (f"🚨 **SMART MONEY ALERT** 🚨\\n\\n"
                                     f"👤 **មហាសេដ្ឋី:** {whale_name}\\n"
                                     f"📥 **ប្រមូលទិញ:** **{value:,.0f} {token_symbol}**\\n"
                                     f"🔗 [View on Blockscout](https://eth.blockscout.com/tx/{tx_hash})\\n\\n"
                                     f"🧠 **ការវិភាគពី AI:**\\n{ai_analysis}\\n\\n"
                                     f"⚡ ប្រើបញ្ជា `/infinity_grid {binance_symbol} 10 1.0 100 <PIN>` ដើម្បីចាប់ឱកាសនេះ!")
                        try:
                            await app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown", disable_web_page_preview=True)
                        except Exception:
                            pass
                            
    except Exception as e:
        print(f"Error in Smart Money Tracker: {e}")'''

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_str)
    new_content = content[:start_idx] + replacement + content[end_idx:]
    with open('scheduler_tasks.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced check_smart_money successfully.")
else:
    print(f"Could not find the function block. start={start_idx}, end={end_idx}")
