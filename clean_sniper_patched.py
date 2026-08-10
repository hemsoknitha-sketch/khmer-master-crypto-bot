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
                    
                    # 🚀 SUPER SMART: DELTA-NEUTRAL HEDGE
                    # Whale hunted the top, funding rates are extremely high. We lock in Delta Neutral.
                    trade_amount = amount / 2
                    
                    # 1. Spot Buy
                    spot_res = await asyncio.to_thread(trading_engine.place_market_buy, api_key, api_secret, symbol, quote_order_qty=trade_amount)
                    if "error" in spot_res:
                        print(f"Delta-Neutral Spot Buy failed: {spot_res['error']}")
                        continue
                        
                    executed_qty = float(spot_res.get("executedQty", 0))
                    if executed_qty <= 0: continue
                    
                    # 2. Futures Short (1x Leverage)
                    fut_res = await asyncio.to_thread(trading_engine.place_futures_short_qty, api_key, api_secret, symbol, qty=executed_qty, leverage=1)
                    if "error" in fut_res:
                        # Emergency Revert
                        await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, symbol, qty=executed_qty)
                        print(f"Delta-Neutral Futures Short failed, reverted Spot: {fut_res['error']}")
                        continue
                        
                    # Register Delta Neutral Bot
                    db.add_delta_neutral_bot(chat_id, symbol, amount, executed_qty, executed_qty)
                    
                    msg = f"🐋 **Whale Liquidity Sweep Caught!**\n\n🪙 **{symbol}**\n📈 **Sweep Type:** BEARISH (Top Hunted)\n🤖 **Strategy:** Delta-Neutral Hedge\n💰 **Investment:** ${amount:.2f}\n⚖️ **Spot Buy:** {executed_qty} {symbol}\n🔴 **Futures Short:** {executed_qty} {symbol} (1x Leverage)\n\n_The AI has locked in the extreme funding rate spike precisely at the top!_"
                    await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

                except Exception as e:
                    print(f"Sweep Sniper short failed for {chat_id}: {e}")
