import codecs

with codecs.open('trading_engine.py', 'r', 'utf-8') as f:
    text = f.read()

# Replace the block that incorrectly placed sync_logic before BASE_URL
# Currently it looks like:
# # TIME SYNC...
# sync_time()
# BASE_URL = "https://api.binance.com"

# Let's remove the sync_time() call from there
text = text.replace('sync_time()\n\nBASE_URL = "https://api.binance.com"', 'BASE_URL = "https://api.binance.com"\n\n# Call it once on module load\nsync_time()')
text = text.replace('sync_time()\nBASE_URL = "https://api.binance.com"', 'BASE_URL = "https://api.binance.com"\n\n# Call it once on module load\nsync_time()')

with codecs.open('trading_engine.py', 'w', 'utf-8') as f:
    f.write(text)

print("Fixed BASE_URL initialization order in trading_engine.py.")
