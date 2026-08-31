import codecs
import re

with codecs.open('trading_engine.py', 'r', 'utf-8') as f:
    text = f.read()

# Add TIME_OFFSET and sync_time() at the top after imports
sync_logic = """
# TIME SYNC
TIME_OFFSET = 0

def sync_time():
    global TIME_OFFSET
    try:
        res = requests.get(f"{BASE_URL}/api/v3/time", timeout=5)
        if res.status_code == 200:
            server_time = res.json()['serverTime']
            local_time = int(time.time() * 1000)
            TIME_OFFSET = server_time - local_time
            print(f"✅ Synced Binance Time Offset: {TIME_OFFSET}ms")
    except Exception as e:
        print(f"⚠️ Failed to sync Binance time: {e}")

# Call it once on module load
sync_time()
"""

# Check if we already injected it
if "def sync_time():" not in text:
    # Insert it right before BASE_URL
    text = text.replace('BASE_URL = "https://api.binance.com"', sync_logic + '\nBASE_URL = "https://api.binance.com"')

# Replace int(time.time() * 1000) with (int(time.time() * 1000) + TIME_OFFSET)
text = text.replace('int(time.time() * 1000)', '(int(time.time() * 1000) + TIME_OFFSET)')
# Fix if we accidentally replaced it twice
text = text.replace('((int(time.time() * 1000) + TIME_OFFSET) + TIME_OFFSET)', '(int(time.time() * 1000) + TIME_OFFSET)')

with codecs.open('trading_engine.py', 'w', 'utf-8') as f:
    f.write(text)

print("trading_engine.py patched with time sync logic.")
