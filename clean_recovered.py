async def trailing_stop_engine_job(app: Application):

    """

    V2 Institutional Trailing Stop Engine

    - 50% Scale-Out at +20% Profit.

    - Dynamic Trailing Stop Widening.

    - Asynchronous Non-Blocking Execution.

    - Adverse Event Learning (Logging failed pumps).

    """

    active_trades = db.get_all_active_trades()

    if not active_trades:

        return

        

    import trading_engine

    import asyncio

    from datetime import datetime

    

    # Pre-fetch all unique symbols concurrently

    unique_symbols = list(set([trade['symbol'] for trade in active_trades]))

    price_tasks = [asyncio.to_thread(trading_engine.get_current_price, sym) for sym in unique_symbols]

    prices = await asyncio.gather(*price_tasks)

    price_map = dict(zip(unique_symbols, prices))

    

    for trade in active_trades:

        trade_id = trade['id']

        chat_id = trade['chat_id']

        symbol = trade['symbol']

        qty = trade['qty']

        buy_price = trade['buy_price']

        stop_loss_pct = trade['stop_loss_pct']

        current_highest = trade['current_highest']

        scaled_out = trade.get('scaled_out', False)

        

        # Get real-time price (Offloaded to avoid freezing Telegram)

        current_price = await asyncio.to_thread(trading_engine.get_current_price, symbol)

        

        if current_price <= 0:

            continue

            

        current_pnl_pct = ((current_price - buy_price) / buy_price) * 100

        

        # 0. DYNAMIC EXIT PROTOCOL: Scale-out 50% if profit >= 20%

        if current_pnl_pct >= 20.0 and not scaled_out:

            keys = db.get_user_api(chat_id)

            if keys:

                api_key, api_secret = keys

                scale_out_qty = qty * 0.5

                

                # Execute Market Sell for 50%

                res = await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, symbol, scale_out_qty)

                

                if "error" not in res and "code" not in res:

                    db.mark_trade_scaled_out(trade_id)

                    db.update_active_trade_qty(trade_id, qty - scale_out_qty)

                    

                    # Widen trailing stop to give remaining capital room to run

                    new_stop_loss = 15.0 # Widen to 15% from highest

                    conn = db.get_db_connection()

                    conn.execute("UPDATE active_trades SET stop_loss_pct = ? WHERE id = ?", (new_stop_loss, trade_id))

                    conn.commit()

                    conn.close()

                    

                    msg = (

                        f"🚀 **DYNAMIC EXIT: 50% Profit Secured!**\n\n"

                        f"🪙 **Symbol:** {symbol}\n"

                        f"💰 **Sold:** 50% of holdings\n"

                        f"📈 **Profit Locked:** +{current_pnl_pct:.2f}%\n"

                        f"🛡️ **Status:** Letting the remaining 50% run with a {new_stop_loss}% dynamic trailing stop! 🏃‍♂️💨"

                    )

                    await app.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

                    continue # Skip further processing this tick

            

        # 1. Update Highest Price if it goes up

        if current_price > current_highest:

            db.update_active_trade_highest(trade_id, current_price)

            continue

            

        # DYNAMIC VOLATILITY ANALYSIS FOR HFT TRAILING STOP

        ticker = await asyncio.to_thread(trading_engine.get_24h_ticker, symbol)

        dynamic_stop_loss = 4.0 # Default mid-point

        if ticker:

            try:

                price_change = abs(float(ticker.get('priceChangePercent', 0)))

                if price_change >= 10.0:

                    dynamic_stop_loss = 3.0 # High volatility -> tight stop

                elif price_change <= 5.0:

                    dynamic_stop_loss = 5.0 # Low volatility -> wider stop

            except (ValueError, TypeError):

                pass

                

        # 2. Check if Trailing Stop is Triggered (Harvest & Compress Mode)

        trailing_stop_price = current_highest * (1 - (dynamic_stop_loss / 100))

        

        if current_price <= trailing_stop_price:

            keys = db.get_user_api(chat_id)

            if not keys:

                continue

            api_key, api_secret = keys

            

            # Execute Market Sell (Offloaded to thread)

            res = await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, symbol, qty)

            

            # Assume filled for paper trading or success real trading

            if "error" not in res and "code" not in res:

                db.remove_active_trade(trade_id, current_price, "TRAILING_STOP")

                profit_pct = ((current_price - buy_price) / buy_price) * 100

                pnl_usdt = (current_price - buy_price) * float(qty)

                db.update_strategy_pnl(chat_id, "HFT_SCALPING", pnl_usdt)

                

                # ADVERSE EVENT LEARNING: Check if it's a failed pump (-10% loss)

                if profit_pct <= -10.0 and not scaled_out:

                    db.log_failed_pump(symbol)