with open('trading_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

# We need to insert this near get_max_sellable_qty which is around line 68
insertion = '''
FUTURES_INFO_CACHE = {}

def get_futures_symbol_info(symbol: str):
    global FUTURES_INFO_CACHE
    if not FUTURES_INFO_CACHE:
        try:
            import requests
            r = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo')
            if r.status_code == 200:
                data = r.json()
                for s in data['symbols']:
                    FUTURES_INFO_CACHE[s['symbol']] = s
        except Exception as e:
            print(f"Failed to fetch futures exchangeInfo: {e}")
    return FUTURES_INFO_CACHE.get(symbol.upper())

def get_futures_max_sellable_qty(symbol: str, raw_qty: float) -> float:
    info = get_futures_symbol_info(symbol)
    if not info:
        return round(raw_qty, 3) # Fallback
        
    step_size = None
    for f in info.get('filters', []):
        if f['filterType'] == 'LOT_SIZE':
            step_size = float(f['stepSize'])
            break
            
    if step_size:
        import math
        precision = max(0, int(round(-math.log10(step_size))))
        if precision == 0:
            return float(math.floor(raw_qty))
        factor = 10 ** precision
        max_sellable = math.floor(raw_qty * factor) / factor
        return max_sellable
    return round(raw_qty, 3)
'''

target = 'def get_max_sellable_qty(symbol: str, raw_balance: float) -> float:'
new_code = code.replace(target, insertion + '\n' + target)

with open('trading_engine.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
print('Added futures quantity formatting to trading_engine.py!')
