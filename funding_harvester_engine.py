import requests
import json
import time
import asyncio
import trading_engine

def scan_top_funding_rates(min_funding_pct: float = 0.03) -> dict:
    """
    Scans Binance Futures Premium Index to identify coins with extreme funding rates (>= 0.03% per 8h).
    Returns top target coin details, settlement countdown, and top 3 yield opportunities.
    """
    result = {
        "opportunity_detected": False,
        "symbol": "",
        "funding_rate_pct": 0.0,
        "estimated_8h_yield_usdt": 0.0,
        "next_funding_time_ms": 0,
        "seconds_to_settlement": 0,
        "recommendation": "Scanning perpetual funding yields...",
        "top_opportunities": []
    }

    try:
        url = "https://fapi.binance.com/fapi/v1/premiumIndex"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if not isinstance(data, list):
                data = [data]

            now_ms = int(time.time() * 1000)
            parsed_items = []

            for item in data:
                symbol = item.get("symbol", "")
                if not symbol.endswith("USDT"):
                    continue

                funding_rate = float(item.get("lastFundingRate", 0.0)) * 100.0 # percentage
                next_time = int(item.get("nextFundingTime", 0))
                secs_left = max(0, int((next_time - now_ms) / 1000))
                parsed_items.append({
                    "symbol": symbol,
                    "funding_rate_pct": round(funding_rate, 4),
                    "abs_rate": abs(funding_rate),
                    "next_funding_time_ms": next_time,
                    "seconds_to_settlement": secs_left
                })

            parsed_items.sort(key=lambda x: x["abs_rate"], reverse=True)
            result["top_opportunities"] = parsed_items[:5]

            if parsed_items and parsed_items[0]["abs_rate"] >= min_funding_pct:
                best = parsed_items[0]
                result["opportunity_detected"] = True
                result["symbol"] = best["symbol"]
                result["funding_rate_pct"] = best["funding_rate_pct"]
                result["next_funding_time_ms"] = best["next_funding_time_ms"]
                result["seconds_to_settlement"] = best["seconds_to_settlement"]
                mins = best["seconds_to_settlement"] // 60
                secs = best["seconds_to_settlement"] % 60
                result["recommendation"] = f"🌾 Extreme 8h Funding Yield on {best['symbol']}: {best['funding_rate_pct']:+.4f}% (Settlement in {mins}m {secs}s)"

    except Exception as e:
        print(f"⚠️ [FUNDING HARVESTER SCAN ERROR]: {e}")

    return result

def is_pre_settlement_window(seconds_left: int) -> bool:
    """Returns True if within 10 minutes (600s) before 8-hour funding settlement."""
    return 10 <= seconds_left <= 600

def execute_funding_harvest_entry(api_key: str, api_secret: str, symbol: str, capital_usdt: float, funding_rate_pct: float) -> dict:
    """
    Executes a 1:1 Delta-Neutral Paired Entry:
    - Half capital Spot Buy
    - Half capital Futures 1x Short
    """
    try:
        spot_cap = round(capital_usdt * 0.5, 2)
        futures_cap = round(capital_usdt * 0.5, 2)

        print(f"[FUNDING HARVEST ENTRY] {symbol} | Spot: ${spot_cap} | Futures 1x Short: ${futures_cap} | Funding: {funding_rate_pct:+.4f}%")

        # Set 1x Leverage on Futures
        trading_engine.set_futures_leverage(api_key, api_secret, symbol, 1)

        # Place Spot Market Buy
        spot_res = trading_engine.place_market_buy(api_key, api_secret, symbol, spot_cap)

        # Place Futures 1x Short Entry (is_entry=True, without reduceOnly restriction)
        price = trading_engine.get_current_price(symbol) or 2650.0
        qty = round((spot_cap / price), 3) if price > 0 else 0.001
        futures_res = trading_engine.place_futures_short_qty(api_key, api_secret, symbol, qty, leverage=1)

        return {
            "status": "success",
            "symbol": symbol,
            "capital": capital_usdt,
            "spot_result": spot_res,
            "futures_result": futures_res
        }
    except Exception as e:
        print(f"[FUNDING HARVEST ENTRY ERROR]: {e}")
        return {"status": "error", "message": str(e)}

def execute_funding_harvest_exit(api_key: str, api_secret: str, symbol: str, capital_usdt: float) -> dict:
    """
    Closes the 1:1 Delta-Neutral Paired Position right after funding settlement.
    """
    try:
        print(f"[FUNDING HARVEST EXIT] Closing paired position for {symbol} after settlement...")

        price = trading_engine.get_current_price(symbol) or 2650.0
        qty = round(((capital_usdt * 0.5) / price), 3) if price > 0 else 0.001
        # Close Futures Short position (is_entry=False, with reduceOnly: true)
        trading_engine.smart_execute_futures_order(api_key, api_secret, symbol, "BUY", qty, leverage=1, is_entry=False)

        return {"status": "success", "symbol": symbol}
    except Exception as e:
        print(f"⚠️ [FUNDING HARVEST EXIT ERROR]: {e}")
        return {"status": "error", "message": str(e)}
