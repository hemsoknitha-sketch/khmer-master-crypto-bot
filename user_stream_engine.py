import asyncio
import json
import aiohttp
import websockets
import time

import database as db

# Global memory cache for all users' spot balances
# Format: { chat_id: { "USDT": 100.5, "BTC": 0.1 } }
USER_BALANCES = {}

class UserStreamEngine:
    def __init__(self):
        self.active_tasks = {}
        self.listen_keys = {}

    async def get_listen_key(self, api_key: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.binance.com/api/v3/userDataStream"
                headers = {"X-MBX-APIKEY": api_key}
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('listenKey')
                    return None
        except Exception as e:
            print(f"Error getting listen key: {e}")
            return None

    async def keep_alive_listen_key(self, api_key: str, listen_key: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.binance.com/api/v3/userDataStream?listenKey={listen_key}"
                headers = {"X-MBX-APIKEY": api_key}
                async with session.put(url, headers=headers) as resp:
                    return resp.status == 200
        except Exception as e:
            print(f"Error keeping listen key alive: {e}")
            return False

    async def _keep_alive_loop(self, chat_id, api_key, listen_key):
        try:
            while True:
                await asyncio.sleep(30 * 60) # Ping every 30 minutes
                success = await self.keep_alive_listen_key(api_key, listen_key)
                if not success:
                    print(f"⚠️ Failed to keep-alive listenKey for {chat_id}, reconnecting...")
                    break # Break out to let the main WS loop reconnect
                else:
                    print(f"✅ User Data Stream Keep-Alive successful for {chat_id}")
        except asyncio.CancelledError:
            pass

    async def handle_event(self, chat_id, data):
        event_type = data.get('e')
        
        if event_type == 'outboundAccountPosition':
            if chat_id not in USER_BALANCES:
                USER_BALANCES[chat_id] = {}
            for bal in data.get('B', []):
                asset = bal['a']
                free = float(bal['f'])
                USER_BALANCES[chat_id][asset] = free
                
        elif event_type == 'executionReport':
            status = data.get('X')
            if status == 'FILLED':
                sym = data.get('s')
                qty = float(data.get('z', 0))
                quote_qty = float(data.get('Z', 0))
                
                if qty > 0:
                    entry_price = quote_qty / qty
                    print(f"⚡ [WS Execution] {chat_id} | {sym} FILLED at {entry_price}")
                    # Update database entry if the trade was stored with 0.0 buy_price
                    try:
                        await asyncio.to_thread(db.update_trade_entry_price, chat_id, sym, entry_price)
                    except Exception as e:
                        print(f"Failed to update entry price for {sym}: {e}")

    async def _ws_task(self, chat_id, api_key):
        while True:
            try:
                listen_key = await self.get_listen_key(api_key)
                if not listen_key:
                    await asyncio.sleep(60)
                    continue
                    
                self.listen_keys[chat_id] = listen_key
                url = f"wss://stream.binance.com:9443/ws/{listen_key}"
                
                print(f"✅ User Data Stream Connected: {chat_id}")
                
                async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                    keep_alive_task = asyncio.create_task(self._keep_alive_loop(chat_id, api_key, listen_key))
                    
                    try:
                        async for message in ws:
                            data = json.loads(message)
                            await self.handle_event(chat_id, data)
                    except websockets.exceptions.ConnectionClosed:
                        pass
                    except Exception as e:
                        print(f"⚠️ WS Error for {chat_id}: {e}")
                    finally:
                        keep_alive_task.cancel()
                        
            except Exception as e:
                print(f"⚠️ UserStream Task Exception for {chat_id}: {e}")
                
            await asyncio.sleep(5)

    async def start(self):
        try:
            # We only track auto trade users or VIP users. Since Auto Trade users are the ones
            # placing orders frequently, we track them.
            users = await asyncio.to_thread(db.get_auto_trade_users)
            count = 0
            for chat_id in users:
                api = await asyncio.to_thread(db.get_user_api, chat_id)
                if api:
                    api_key, api_secret = api
                    if api_key:
                        task = asyncio.create_task(self._ws_task(chat_id, api_key))
                        self.active_tasks[chat_id] = task
                        count += 1
            print(f"🚀 Initialized Binance User Data Streams for {count} users.")
        except Exception as e:
            print(f"Error starting user streams: {e}")

engine = UserStreamEngine()

async def start_user_streams():
    await engine.start()
