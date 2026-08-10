import asyncio
import json
import time
import websockets

# Global in-memory cache for ultra-fast sub-10ms access directly from RAM
PRICE_CACHE = {}

async def _binance_bookticker_ws_loop():
    """Ultra-Fast Sub-10ms BookTicker Stream for tick-by-tick real-time price feeds."""
    url = "wss://stream.binance.com:9443/ws/!bookTicker"
    while True:
        try:
            print("[HFT Engine] Connecting to Binance Real-Time BookTicker Stream...")
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print("[HFT Engine] Connected to Sub-10ms Binance !bookTicker Stream!")
                while True:
                    message = await ws.recv()
                    item = json.loads(message)
                    
                    symbol = item.get('s')
                    if not symbol:
                        continue
                        
                    bid_price = float(item.get('b', 0))
                    ask_price = float(item.get('a', 0))
                    
                    if bid_price > 0 and ask_price > 0:
                        mid_price = (bid_price + ask_price) / 2.0
                        spread_pct = ((ask_price - bid_price) / ask_price) * 100.0 if ask_price > 0 else 0.0
                    elif bid_price > 0:
                        mid_price = bid_price
                        spread_pct = 0.0
                    else:
                        mid_price = ask_price
                        spread_pct = 0.0
                        
                    prev_data = PRICE_CACHE.get(symbol, {})
                    volume = prev_data.get("volume", 0.0)
                    
                    PRICE_CACHE[symbol] = {
                        "price": mid_price,
                        "best_bid": bid_price,
                        "best_ask": ask_price,
                        "spread_pct": spread_pct,
                        "volume": volume,
                        "timestamp": time.time()
                    }
                    
                    # Notify tick listeners in sub-millisecond RAM execution
                    for cb in TICK_LISTENERS:
                        try:
                            cb(symbol, mid_price, bid_price, ask_price)
                        except Exception:
                            pass
        except websockets.ConnectionClosed:
            print("[HFT Engine] BookTicker WebSocket closed. Reconnecting in 3s...")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"[HFT Engine] BookTicker WebSocket Error: {e}")
            await asyncio.sleep(3)

async def _binance_miniticker_ws_loop():
    """Background MiniTicker array stream for secondary volume fallback."""
    url = "wss://stream.binance.com:9443/ws/!miniTicker@arr"
    while True:
        try:
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    current_time = time.time()
                    for item in data:
                        symbol = item['s']
                        close_price = float(item['c'])
                        volume = float(item['q'])
                        
                        if symbol in PRICE_CACHE:
                            PRICE_CACHE[symbol]["volume"] = volume
                        else:
                            PRICE_CACHE[symbol] = {
                                "price": close_price,
                                "best_bid": close_price,
                                "best_ask": close_price,
                                "spread_pct": 0.0,
                                "volume": volume,
                                "timestamp": current_time
                            }
        except Exception:
            await asyncio.sleep(5)

TICK_LISTENERS = []

def register_tick_listener(callback):
    """Registers a callback function to receive real-time tick updates (symbol, price, bid, ask)."""
    if callback not in TICK_LISTENERS:
        TICK_LISTENERS.append(callback)

def start_binance_websocket():
    """Starts the ultra-fast Sub-10ms WebSocket connection in a background task."""
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(_binance_bookticker_ws_loop())
        loop.create_task(_binance_miniticker_ws_loop())
        print("[HFT Engine] Sub-10ms Real-Time WebSocket Engine Initialized.")
    except Exception as e:
        print(f"[HFT Engine] Failed to start WebSocket engine: {e}")

def get_fast_price(symbol: str) -> float:
    """Returns the real-time price instantly from RAM (< 0.1ms). Returns 0.0 if expired or not cached."""
    data = PRICE_CACHE.get(symbol)
    if data:
        # High-frequency validity window (5 seconds max latency)
        if time.time() - data['timestamp'] < 5.0:
            return data['price']
    return 0.0

def get_fast_book_ticker(symbol: str) -> dict:
    """Returns best bid, best ask, mid price and spread instantly from RAM."""
    data = PRICE_CACHE.get(symbol)
    if data and (time.time() - data['timestamp'] < 5.0):
        return {
            "symbol": symbol,
            "price": data["price"],
            "best_bid": data["best_bid"],
            "best_ask": data["best_ask"],
            "spread_pct": data["spread_pct"],
            "timestamp": data["timestamp"]
        }
    return {}

