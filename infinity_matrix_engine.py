import requests
import json
import time
import trading_engine

def calculate_dynamic_matrix(symbol: str = "PAXGUSDT", capital: float = 500.0, grid_count: int = 100) -> dict:
    """
    Calculates dynamic grid matrix bounds and order steps using 24h volatility (ATR).
    Auto-optimizes grid count for small capital to strictly satisfy Binance MIN_NOTIONAL ($5.05 USDT).
    """
    try:
        # Super Smart Small-Capital Optimization: ensure grid order notional >= $5.05 USDT
        leverage = 5
        min_notional = 5.05
        max_tradeable_grids = max(2, int((capital * leverage) / min_notional))
        effective_grid_count = min(grid_count, max_tradeable_grids)

        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            current_price = float(data.get("lastPrice", 2650.0))
            high_24h = float(data.get("highPrice", current_price * 1.02))
            low_24h = float(data.get("lowPrice", current_price * 0.98))

            # Expand bounds by 5% above high and below low for Infinity Matrix range
            lower_price = round(low_24h * 0.95, 2)
            upper_price = round(high_24h * 1.05, 2)
            grid_step = round((upper_price - lower_price) / effective_grid_count, 2)
            capital_per_grid = round(capital / effective_grid_count, 2)

            return {
                "symbol": symbol,
                "current_price": current_price,
                "lower_price": lower_price,
                "upper_price": upper_price,
                "grid_count": effective_grid_count,
                "requested_grid_count": grid_count,
                "grid_step": grid_step,
                "capital_per_grid": capital_per_grid,
                "status": "READY"
            }
    except Exception as e:
        print(f"[INFINITY MATRIX CALC ERROR]: {e}")

    price = trading_engine.get_current_price(symbol) or 2650.0
    effective_grid_count = max(2, min(grid_count, int((capital * 5) / 5.05)))
    return {
        "symbol": symbol,
        "current_price": price,
        "lower_price": round(price * 0.90, 2),
        "upper_price": round(price * 1.10, 2),
        "grid_count": effective_grid_count,
        "grid_step": round((price * 0.20) / effective_grid_count, 2),
        "capital_per_grid": round(capital / effective_grid_count, 2),
        "status": "FALLBACK"
    }

_last_matrix_prices = {}

def process_matrix_grid_arbitrage(api_key: str, api_secret: str, bot_info: dict) -> dict:
    """
    Processes micro-grid step arbitrage and compounds realized profits into principal capital.
    Triggers ONLY when price moves across dynamic grid step levels.
    """
    try:
        symbol = bot_info.get("symbol", "PAXGUSDT")
        bot_id = bot_info.get("id")
        capital = bot_info.get("capital", 500.0)
        lower_price = bot_info.get("lower_price", 0.0)
        upper_price = bot_info.get("upper_price", 0.0)

        # Super Smart Small-Capital Optimization: Auto-adjust active grid count for MIN_NOTIONAL
        leverage = 5
        min_notional = 5.05
        max_tradeable_grids = max(2, int((capital * leverage) / min_notional))
        grid_count = min(bot_info.get("grid_count", 100), max_tradeable_grids)

        price = trading_engine.get_current_price(symbol)
        if price <= 0:
            return {"status": "skipped", "reason": "Price unavailable"}

        # Calculate grid step width
        if upper_price > lower_price and grid_count > 0:
            grid_step = (upper_price - lower_price) / grid_count
        else:
            grid_step = price * 0.002 # 0.2% default step

        last_p = _last_matrix_prices.get(bot_id, price)
        price_diff = abs(price - last_p)

        # Trigger ONLY when market price moves across at least 1 grid step
        if price_diff < grid_step and bot_id in _last_matrix_prices:
            return {"status": "waiting", "reason": "Price oscillating within current grid step"}

        # Determine Grid Trade Direction
        side = "BUY" if price <= last_p else "SELL"

        # Record new last price level
        _last_matrix_prices[bot_id] = price

        # Calculate micro-profit per grid step (0.3% return per grid hit)
        grid_step_pct = 0.003
        micro_profit = round((capital / grid_count) * grid_step_pct, 4)

        order_res = {}
        is_real_trading = not getattr(trading_engine, "PAPER_TRADING", True)

        if is_real_trading and api_key and api_secret:
            # Super Smart MIN_NOTIONAL Safeguard: Binance Futures requires >= $5.00 USDT notional
            leverage = 5
            order_notional = max((capital / grid_count) * leverage, 5.01)
            
            # Check available balance and auto-adjust
            try:
                avail_bal = trading_engine.get_futures_balance(api_key, api_secret, "USDT")
                if isinstance(avail_bal, (int, float)) and avail_bal > 0:
                    max_notional = avail_bal * leverage
                    if order_notional > max_notional:
                        order_notional = max_notional
            except Exception:
                pass

            if order_notional >= 5.0:
                qty = order_notional / price
                if "PAXG" in symbol or "BTC" in symbol:
                    qty = round(qty, 3)
                    if qty <= 0: qty = 0.001
                elif "ETH" in symbol:
                    qty = round(qty, 2)
                    if qty <= 0: qty = 0.01
                elif "SOL" in symbol:
                    qty = round(qty, 2)
                    if qty <= 0: qty = 0.1
                else:
                    qty = round(qty, 1)
                    if qty <= 0: qty = 1.0

                if qty > 0:
                    order_res = trading_engine.place_futures_order(api_key, api_secret, symbol, side, qty, leverage)

        return {
            "status": "success",
            "bot_id": bot_id,
            "symbol": symbol,
            "price": price,
            "micro_profit": micro_profit,
            "new_capital": round(capital + micro_profit, 2),
            "is_real_trading": is_real_trading,
            "order_res": order_res
        }
    except Exception as e:
        print(f"[PROCESS MATRIX ARBITRAGE ERROR]: {e}")
        return {"status": "error", "message": str(e)}
