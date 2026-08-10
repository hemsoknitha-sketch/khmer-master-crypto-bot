import asyncio
import json
import time
import websockets
import dynamic_ranking

# Cache to store Orderbook Data
# Structure: { "BTCUSDT": {"bid_price": 100, "bid_qty": 2, "ask_price": 101, "ask_qty": 1, "timestamp": 1234} }
ORDERBOOK_CACHE = {}

async def _orderbook_ws_chunk_loop(coins_chunk):
    while True:
        try:
            streams = "/".join([f"{sym.lower()}@bookTicker" for sym in coins_chunk])
            url = f"wss://stream.binance.com:9443/stream?streams={streams}"
            
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print(f"✅ [OrderBook Engine] Connected to @bookTicker Streams for {len(coins_chunk)} coins")
                
                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    
                    if "data" in data and "s" in data["data"]:
                        tick = data["data"]
                        symbol = tick["s"]
                        
                        ORDERBOOK_CACHE[symbol] = {
                            "bid_price": float(tick["b"]),
                            "bid_qty": float(tick["B"]),
                            "ask_price": float(tick["a"]),
                            "ask_qty": float(tick["A"]),
                            "timestamp": time.time()
                        }
        except websockets.ConnectionClosed:
            # Silent reconnect to avoid spam
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ [OrderBook Engine] WebSocket Error: {e}")
            await asyncio.sleep(5)

async def _orderbook_ws_manager():
    while True:
        top_coins = dynamic_ranking.get_top_500_coins()
        if not top_coins:
            await asyncio.sleep(10)
            continue
            
        print(f"🔗 [OrderBook Engine] Connecting to Binance Multiplex Stream for {len(top_coins)} coins in chunks...")
        
        # Chunk into groups of 100
        tasks = []
        for i in range(0, len(top_coins), 100):
            chunk = top_coins[i:i+100]
            tasks.append(asyncio.create_task(_orderbook_ws_chunk_loop(chunk)))
            
        # Wait until tasks fail/close (which they do internally and retry)
        # However, to refresh coins every hour, we could cancel and restart.
        # But for now, just let it run. We sleep for 1 hour then refresh list.
        await asyncio.sleep(3600)
        
        for t in tasks:
            t.cancel()

def start_orderbook_engine():
    """Starts the OrderBook WebSocket connection in a background task."""
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(_orderbook_ws_manager())
    except Exception as e:
        print(f"❌ [OrderBook Engine] Failed to start: {e}")

def get_imbalance(symbol: str) -> float:
    """
    Calculates the OrderBook Imbalance Ratio (Bid USDT / Ask USDT).
    Returns a float > 1.0 if Bids are stronger (Buy Wall).
    Returns a float < 1.0 if Asks are stronger (Sell Wall).
    Returns 1.0 if no data or perfectly balanced.
    """
    data = ORDERBOOK_CACHE.get(symbol)
    if not data:
        return 1.0
        
    # Check if data is stale (> 30 seconds)
    if time.time() - data["timestamp"] > 30.0:
        return 1.0
        
    bid_usdt = data["bid_price"] * data["bid_qty"]
    ask_usdt = data["ask_price"] * data["ask_qty"]
    
    if ask_usdt == 0:
        return 10.0 # Return arbitrarily high imbalance if no asks
        
    return bid_usdt / ask_usdt

def check_micro_imbalance_signal(symbol: str, min_ratio: float = 3.0, max_spread_pct: float = 0.15) -> dict:
    """
    Checks if a symbol has a micro-imbalance signal (Bid USDT / Ask USDT >= min_ratio).
    Also checks that spread % <= max_spread_pct to prevent illiquid slippage.
    """
    data = ORDERBOOK_CACHE.get(symbol)
    if not data or (time.time() - data.get("timestamp", 0) > 10.0):
        return {"signal": "NONE", "ratio": 1.0, "reason": "No real-time data"}
        
    bid_p = data.get("bid_price", 0.0)
    ask_p = data.get("ask_price", 0.0)
    bid_q = data.get("bid_qty", 0.0)
    ask_q = data.get("ask_qty", 0.0)
    
    if bid_p <= 0 or ask_p <= 0 or ask_q <= 0:
        return {"signal": "NONE", "ratio": 1.0, "reason": "Invalid quotes"}
        
    bid_usdt = bid_p * bid_q
    ask_usdt = ask_p * ask_q
    ratio = bid_usdt / ask_usdt if ask_usdt > 0 else 10.0
    spread_pct = ((ask_p - bid_p) / ask_p) * 100.0
    
    if ratio >= min_ratio and spread_pct <= max_spread_pct:
        return {
            "signal": "BUY",
            "symbol": symbol,
            "ratio": ratio,
            "bid_usdt": bid_usdt,
            "ask_usdt": ask_usdt,
            "spread_pct": spread_pct,
            "target_profit_pct": 0.5,
            "stop_loss_pct": 0.5
        }
        
    return {"signal": "NONE", "ratio": ratio, "spread_pct": spread_pct}

