import asyncio
import json
import time
import requests
import websockets
from collections import deque
import dynamic_ranking
import database as db
import trading_engine
import os

# RVOL Threshold (3.0 means 300% volume spike)
RVOL_THRESHOLD = 3.0


# Store recent 1m candle volumes for each symbol
# Structure: { "BTCUSDT": deque([1000, 1500, 1200, ...], maxlen=15) }
VOLUME_HISTORY = {}

# Cooldown to prevent spam buying the same coin
COOLDOWN_CACHE = {}
COOLDOWN_SECONDS = 3600  # 1 hour cooldown per coin

def send_telegram_alert(chat_id, text):
    """Sends a Telegram message using REST API to avoid passing app instance around."""
    if "Insufficient USDT Balance" in text or ("Balance" in text and "Insufficient" in text) or "Insufficient Balance" in text:
        from notification_manager import logger
        logger.info(f"SILENCED RVOL [User {chat_id}]: {text}")
        return
        
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token or bot_token == "your_telegram_bot_token_here":
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to send RVOL Telegram alert: {e}")

async def _process_rvol_spike(symbol, rvol_multiplier, projected_vol, taker_ratio):
    """Executes the Auto-Buy and sends alerts when an RVOL spike is detected."""
    print(f"🔥 [RVOL Engine] SPIKE DETECTED! {symbol} | Spike: {rvol_multiplier:.2f}x | Toxicity: {taker_ratio*100:.0f}%")
    
    import database as db
    import orderbook_engine
    import trading_engine
# import asyncio # removed local shadowing
    
    # --- INSTITUTIONAL FILTER 1: Adverse Event Learning ---
    failed_count = db.get_failed_pump_count(symbol)
    if failed_count > 0:
        print(f"🚫 [RVOL] Skipped {symbol}: In Failed Pump DB ({failed_count} fails).")
        return

    # --- INSTITUTIONAL FILTER 2: Macro Risk-Off Check ---
    btc_ticker = await asyncio.to_thread(trading_engine.get_24h_ticker, 'BTCUSDT')
    if btc_ticker:
        btc_change = float(btc_ticker.get('priceChangePercent', 0))
        if btc_change < -2.0: # If BTC dropped more than 2% today, it's risk-off.
            print(f"🚫 [RVOL] Skipped {symbol}: Macro Risk-Off (BTC down {btc_change:.2f}%).")
            return

    # --- INSTITUTIONAL FILTER 3: Orderbook Wash-Trade Check ---
    imbalance = await asyncio.to_thread(orderbook_engine.get_imbalance, symbol)
    if imbalance < 0.5:
        print(f"🚫 [RVOL] Skipped {symbol}: Wash-Trade detected (Heavy Sell Wall, Imbalance: {imbalance}).")
        return
        
    # --- INSTITUTIONAL FILTER 4: Liquidity-Calibrated Sizing ---
    ticker = await asyncio.to_thread(trading_engine.get_24h_ticker, symbol)
    if not ticker: return
    vol_24h = float(ticker.get('quoteVolume', 0))
    current_price = float(ticker.get('lastPrice', 0))
    if current_price <= 0: return
    
    max_buy_amount = vol_24h * 0.01 # Max 1% of 24h volume
    
    auto_trade_users = db.get_auto_trade_users()
    if not auto_trade_users:
        return
        
    tasks = []
    
    # Async Auto-Buy for VIPs
    async def process_user(chat_id):
        keys = db.get_user_api(chat_id)
        if not keys: return
        api_key, api_secret = keys
        
        try:
            # Fixed $15 USDT amount for RVOL auto-buy (Safety feature) but capped by liquidity
            buy_amount = min(15.0, max_buy_amount)
            
            if buy_amount < 5.0:
                print(f"🚫 [RVOL] Skipped {symbol} for {chat_id}: Liquidity too low for minimum order size.")
                return
            
            res = await asyncio.to_thread(trading_engine.place_market_buy, api_key, api_secret, symbol, quote_order_qty=buy_amount)
            if "status" in res and res["status"] == "FILLED":
                actual_spent = float(res.get("cummulativeQuoteQty", 0.0))
                qty = float(res.get("executedQty", res.get("origQty", 0.0)))
                buy_price = actual_spent / qty if qty > 0 else 0.0
                
                # Add Trailing Stop (Ultra-tight 1.5% for RVOL momentum spikes)
                db.add_active_trade(chat_id, symbol, qty, buy_price, stop_loss_pct=1.5)

                
                downsize_warning = ""
                if actual_spent < 15.0:
                    downsize_warning = f"\n⚠️ **Liquidity Calibrated:** Resized to ${actual_spent:.2f} USDT (Max 1% of 24h Vol)"
                
                msg = (
                    f"🔥 **RVOL SPIKE AUTO-BUY!**\n\n"
                    f"🪙 **Symbol:** {symbol}\n"
                    f"📊 **Volume Spike:** {rvol_multiplier*100:.0f}%\n"
                    f"🔥 **Aggressive Buys:** {taker_ratio*100:.0f}% (Toxicity)\n"
                    f"💰 **Bought Amount:** ${actual_spent:.2f}{downsize_warning}\n"
                    f"🎯 **Entry Price:** ${buy_price:,.4f}\n\n"
                    f"_The AI verified genuine volume and bought to front-run the pump!_"
                )
                await asyncio.to_thread(send_telegram_alert, chat_id, msg)
            elif "error" in res:
                err = res.get('error', '')
                if "Insufficient" in err:
                    import scheduler_tasks
                    if not scheduler_tasks.GLOBAL_INSUFFICIENT_MUTE.get(chat_id, False):
                        msg = f"❌ **RVOL Buy Failed:** {err}\n\n⚠️ **ទុនបម្រុង USDT របស់អ្នកបានអស់ហើយ! ប្រព័ន្ធ AI នឹងផ្អាកការបញ្ជូនសាររំខានបណ្តោះអាសន្ន។ វានឹងរង់ចាំដោយស្ងៀមស្ងាត់។**"
                        await asyncio.to_thread(send_telegram_alert, chat_id, msg)
                        scheduler_tasks.GLOBAL_INSUFFICIENT_MUTE[chat_id] = True
                    else:
                        print(f"⏸️ RVOL Auto-Buy skipped for {chat_id} (Insufficient Balance - Muted)")
                else:
                    print(f"❌ RVOL Auto-Buy failed for {chat_id} on {symbol}: {err}")
                    
        except Exception as e:
            print(f"❌ RVOL Auto-Buy failed (Exception) for {chat_id} on {symbol}: {e}")
            
    for chat_id in auto_trade_users:
        tasks.append(process_user(chat_id))
        
    if tasks:
        await asyncio.gather(*tasks)

async def _rvol_ws_loop():
    while True:
        try:
            # 1. Get Top 500 Coins
            top_coins = dynamic_ranking.get_top_500_coins()
            if not top_coins:
                await asyncio.sleep(10)
                continue
                
            # Create streams string (e.g., btcusdt@kline_1m/ethusdt@kline_1m)
            streams = "/".join([f"{sym.lower()}@kline_1m" for sym in top_coins])
            url = f"wss://stream.binance.com:9443/stream?streams={streams}"
            
            print(f"🔗 [RVOL Engine] Connecting to Binance Multiplex Stream for {len(top_coins)} coins...")
            
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print("✅ [RVOL Engine] Connected to 1m Kline Streams")
                
                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    
                    if "data" in data and "k" in data["data"]:
                        kline = data["data"]["k"]
                        symbol = kline["s"]
                        is_closed = kline["x"]
                        quote_volume = float(kline["q"])  # Volume in USDT
                        taker_buy_volume = float(kline["Q"]) # Taker Buy Volume in USDT
                        
                        # Handle closed candle
                        if is_closed:
                            if symbol not in VOLUME_HISTORY:
                                VOLUME_HISTORY[symbol] = deque(maxlen=15)
                            VOLUME_HISTORY[symbol].append(quote_volume)
                            continue
                            
                        # Handle live forming candle
                        if symbol in VOLUME_HISTORY and len(VOLUME_HISTORY[symbol]) >= 5:
                            avg_vol = sum(VOLUME_HISTORY[symbol]) / len(VOLUME_HISTORY[symbol])
                            if avg_vol > 0:
                                # If the *partial* minute volume is ALREADY 5x the average of full minutes, it's a guaranteed massive spike.
                                rvol = quote_volume / avg_vol
                                
                                if rvol >= RVOL_THRESHOLD:
                                    # Order Flow Toxicity check
                                    taker_ratio = (taker_buy_volume / quote_volume) if quote_volume > 0 else 0
                                    
                                    if taker_ratio >= 0.70:

                                        # Check Cooldown
                                        current_time = time.time()
                                        if symbol not in COOLDOWN_CACHE or (current_time - COOLDOWN_CACHE[symbol]) > COOLDOWN_SECONDS:
                                            COOLDOWN_CACHE[symbol] = current_time
                                            # Trigger Async Auto-Buy Task!
                                            asyncio.create_task(_process_rvol_spike(symbol, rvol, quote_volume, taker_ratio))

        except websockets.ConnectionClosed:
            print("⚠️ [RVOL Engine] WebSocket closed. Reconnecting...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ [RVOL Engine] WebSocket Error: {e}")
            await asyncio.sleep(5)

def start_rvol_engine():
    """Starts the RVOL WebSocket connection in a background task."""
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(_rvol_ws_loop())
    except Exception as e:
        print(f"❌ [RVOL Engine] Failed to start: {e}")
