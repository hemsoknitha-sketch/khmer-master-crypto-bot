import asyncio
import time
import requests
import database as db

# Thresholds
CRASH_THRESHOLD_PCT = -0.03 # -3% drop
CHECK_INTERVAL_SEC = 60 # Check every 1 minute
SYMBOLS_TO_MONITOR = ["BTCUSDT", "ETHUSDT"]

class CircuitBreakerEngine:
    def __init__(self, bot_app=None):
        self.bot_app = bot_app # telegram.ext.Application to send messages
        self.is_running = False

    def get_price_change_5m(self, symbol: str) -> float:
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=2"
            res = requests.get(url, timeout=5)
            data = res.json()
            if len(data) >= 2:
                # data[0] is the previous 5m candle, data[1] is current active 5m candle
                open_price = float(data[0][1]) # open of the last 5m candle
                current_price = float(data[1][4]) # current close price
                pct_change = (current_price - open_price) / open_price
                return pct_change
        except Exception as e:
            print(f"Error fetching circuit breaker data for {symbol}: {e}")
        return 0.0

    async def trigger_circuit_breaker(self, symbol: str, drop_pct: float):
        # 1. Update Database
        db.set_circuit_breaker_status(True)
        print(f"🚨 CIRCUIT BREAKER ACTIVATED due to {symbol} drop of {drop_pct*100:.2f}%!")
        
        # 2. Get all VIP users
        vip_users = db.get_vip_users()
        
        # 3. Send Telegram Alerts and Engage Hedge Mode
        if self.bot_app:
            alert_msg = (
                f"🚨 **FLASH CRASH DETECTED!** 🚨\n\n"
                f"⚠️ `{symbol}` has dropped by **{drop_pct*100:.2f}%** in the last 5 minutes!\n"
                f"🛡️ **Market Circuit Breaker ACTIVATED**\n"
                f"⛔ All New Spot Buys Paused.\n"
                f"📉 Auto Hedge Mode Engaging...\n"
                f"*(Protecting your portfolio automatically)*"
            )
            import trading_engine
            
            for chat_id in vip_users:
                try:
                    await self.bot_app.bot.send_message(chat_id=chat_id, text=alert_msg, parse_mode="Markdown")
                    
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
                                    text=f"🚨 **SUPER SMART HEDGE ACTIVATED!** 🚨\n\n"
                                         f"🪙 **កាក់:** `{symbol}`\n"
                                         f"🛡️ **ទំហំការពារ:** ${actual_amount:.2f}{downsize_msg}\n"
                                         f"⚙️ **Dynamic Leverage:** {dynamic_leverage}x (AI Adjusted)\n\n"
                                         f"_(ប្រព័ន្ធបានបើកការ Short ស្វ័យប្រវត្តិដើម្បីទប់ទល់នឹងការធ្លាក់ចុះនៃទីផ្សារ!)_"
                                )
                except Exception as e:
                    print(f"Failed to alert/hedge user {chat_id}: {e}")

    async def run_loop(self):
        self.is_running = True
        print("🛡️ Market Circuit Breaker Engine Started.")
        
        while self.is_running:
            try:
                if not db.is_circuit_breaker_active():
                    for sym in SYMBOLS_TO_MONITOR:
                        change = self.get_price_change_5m(sym)
                        if change <= CRASH_THRESHOLD_PCT:
                            await self.trigger_circuit_breaker(sym, change)
                            break # Only trigger once
                            
            except Exception as e:
                print(f"Circuit Breaker Error: {e}")
                
            await asyncio.sleep(CHECK_INTERVAL_SEC)
            
    def stop(self):
        self.is_running = False

circuit_breaker = CircuitBreakerEngine()

async def start_circuit_breaker(app):
    circuit_breaker.bot_app = app
    await circuit_breaker.run_loop()
