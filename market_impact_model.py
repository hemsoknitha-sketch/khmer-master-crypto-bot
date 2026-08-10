import requests

def get_order_book(symbol: str, limit: int = 100):
    """Fetches the order book for a symbol from Binance Spot."""
    try:
        url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error fetching order book for {symbol}: {e}")
    return None

def estimate_slippage(symbol: str, order_qty_usdt: float, side: str = "BUY") -> float:
    """
    Estimates the slippage percentage for a market order of size order_qty_usdt.
    Returns: slippage percentage (e.g., 0.2 means 0.2%).
    Returns 0.0 if unable to estimate.
    """
    depth = get_order_book(symbol)
    if not depth or "bids" not in depth or "asks" not in depth:
        return 0.0

    if not depth["bids"] or not depth["asks"]:
        return 0.0

    best_bid = float(depth["bids"][0][0])
    best_ask = float(depth["asks"][0][0])
    mid_price = (best_bid + best_ask) / 2.0

    remaining_usdt = order_qty_usdt
    total_cost_usdt = 0.0
    total_qty_coin = 0.0

    # If BUY, we sweep the ASKS
    # If SELL, we sweep the BIDS
    levels = depth["asks"] if side.upper() == "BUY" else depth["bids"]

    for price_str, qty_str in levels:
        price = float(price_str)
        qty = float(qty_str)
        level_usdt = price * qty

        if remaining_usdt <= level_usdt:
            # This level fully absorbs the rest of the order
            level_qty = remaining_usdt / price
            total_qty_coin += level_qty
            total_cost_usdt += remaining_usdt
            remaining_usdt = 0
            break
        else:
            # Take the whole level
            total_qty_coin += qty
            total_cost_usdt += level_usdt
            remaining_usdt -= level_usdt

    # If order is so large it sweeps the entire 100-level order book limit
    if remaining_usdt > 0:
        return 10.0 # Extremely high slippage, definitely force slicing

    if total_qty_coin == 0:
        return 0.0

    vwap = total_cost_usdt / total_qty_coin
    
    if side.upper() == "BUY":
        slippage_pct = ((vwap - mid_price) / mid_price) * 100
    else:
        slippage_pct = ((mid_price - vwap) / mid_price) * 100

    return max(0.0, slippage_pct)

def get_best_bid_ask(symbol: str) -> tuple[float, float]:
    """Returns (best_bid, best_ask) for a symbol from order book depth."""
    depth = get_order_book(symbol, limit=5)
    if depth and "bids" in depth and "asks" in depth:
        if depth["bids"] and depth["asks"]:
            return float(depth["bids"][0][0]), float(depth["asks"][0][0])
    return 0.0, 0.0

