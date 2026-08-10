async def sweep_sniper_monitor(app):

    import database as db

    import market_data

    import trading_engine

    

    snipers = db.get_all_sweep_snipers()

    if not snipers: return

    

    # Get top 10 volatile coins to hunt sweeps

    volatile_coins = market_data.get_top_volatile_coins(limit=10)

    if not volatile_coins: return

    

    for coin_data in volatile_coins:

        symbol = coin_data['symbol']

        sweep_data = market_data.detect_liquidity_sweep(symbol)

        

        if sweep_data["type"] == "BULLISH":

            for sniper in snipers:

                chat_id = sniper["chat_id"]

                amount = sniper["amount"]

                

                keys = db.get_user_api(chat_id)

                if not keys: continue

                api_key, api_secret = keys

                

                # Check if we already have an active trade for this symbol to avoid spamming

                active_trades = db.get_active_trades(chat_id)

                if any(t[2] == symbol for t in active_trades): continue

                

                # LIQUIDITY GUARD

                available_usdt = trading_engine.get_spot_balance(api_key, api_secret, "USDT")

                actual_amount = min(amount, available_usdt)

                if actual_amount < 10.0:

                    continue

                

                try:

                    # Place Spot Buy at the bottom of the sweep

                    res = await asyncio.to_thread(trading_engine.place_market_buy, api_key, api_secret, symbol, quote_order_qty=actual_amount)

                    if "status" in res and res["status"] == "FILLED":

                        actual_spent = float(res.get("cummulativeQuoteQty", 0.0))

                        qty = float(res.get("executedQty", res.get("origQty", 0.0)))

                        buy_price = actual_spent / qty if qty > 0 else 0.0

                        actual_spent = float(res.get("cummulativeQuoteQty", buy_price * qty))

                        

                        # Set a tight 2% Trailing Stop-Loss

                        db.add_active_trade(chat_id, symbol, qty, buy_price, stop_loss_pct=2.0)

                        

                        downsize_warning = ""

                        if actual_spent < amount * 0.95:

                            downsize_warning = f"\n⚠️ **AI Auto-Resized:** Used remaining ${actual_spent:.2f} USDT"

                            

                        msg = f"🐋 **Whale Liquidity Sweep Caught!**\n\n🪙 **{symbol}**\n📉 **Sweep Type:** BULLISH (Bottom Hunted)\n🤖 **Confidence:** {sweep_data['confidence']}%\n💰 **Buy Amount:** ${actual_spent:.2f}{downsize_warning}\n🎯 **Entry Price:** ${buy_price:,.4f}\n\n_The AI has bought the dip right behind the whales with a tight Trailing Stop-Loss._"

                        await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

                except Exception as e:

                    print(f"Sweep Sniper buy failed for {chat_id}: {e}")

                    

        elif sweep_data["type"] == "BEARISH":

            for sniper in snipers:

                chat_id = sniper["chat_id"]

                amount = sniper["amount"]

                

                keys = db.get_user_api(chat_id)

                if not keys: continue

                api_key, api_secret = keys

                

                active_shorts = db.get_active_shorts(chat_id)

                if any(s[2] == symbol for s in active_shorts): continue

                

                try:

                    # Use AI Dynamic Leverage for safety

                    dynamic_lev = 10

                    if db.is_dynamic_leverage_enabled(chat_id):

                        dynamic_lev = await asyncio.to_thread(trading_engine.calculate_ai_dynamic_leverage, symbol, 20, 80.0)

                        

                    res = await asyncio.to_thread(trading_engine.place_futures_short, api_key, api_secret, symbol, margin_usdt=amount, leverage=dynamic_lev, vol_target=1500)

                    if "status" in res and res["status"] == "FILLED":

                        short_price = float(res["price"])

                        db.add_active_short(chat_id, symbol, amount, dynamic_lev, short_price)

                        

                        msg = f"🐋 **Whale Liquidity Sweep Caught!**\n\n🪙 **{symbol}**\n📈 **Sweep Type:** BEARISH (Top Hunted)\n🤖 **Confidence:** {sweep_data['confidence']}%\n🔴 **Short Margin:** ${amount:.2f} ({dynamic_lev}x Leverage)\n🎯 **Entry Price:** ${short_price:,.4f}\n\n_The AI has shorted the top right behind the whales._"

                        await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

                except Exception as e:

                    print(f"Sweep Sniper short failed for {chat_id}: {e}")


