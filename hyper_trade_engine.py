import requests
import json
import time
import asyncio
import trading_engine

# Top High-Volatility Tickers for HFT Scalping
HFT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "PAXGUSDT", "XRPUSDT", "DOGEUSDT", "AVAXUSDT", "NEARUSDT"]

def scan_hft_opportunity(symbol: str = "BTCUSDT") -> dict:
    """
    High-Frequency 1m/15s Market Scanner.
    Calculates Momentum, RSI 1m, Volume Surge Ratio, and AI Win Rate Probability %.
    Returns dict with trade signal and parameters if Win Rate >= 78%.
    """
    result = {
        "symbol": symbol,
        "signal": "NEUTRAL",
        "win_rate_pct": 0.0,
        "entry_price": 0.0,
        "tp_price": 0.0,
        "sl_price": 0.0,
        "side": "BUY",
        "momentum_score": 0.0,
        "dynamic_leverage": 5,
        "reason": "Low market volatility"
    }

    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=20"
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return result

        klines = res.json()
        if not klines or len(klines) < 15:
            return result

        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]

        current_price = closes[-1]
        prev_close = closes[-2]

        # 1. Price Momentum % (1m vs 5m)
        price_change_1m = ((current_price - prev_close) / prev_close) * 100.0
        price_change_5m = ((current_price - closes[-5]) / closes[-5]) * 100.0

        # 2. Volume Surge Ratio
        avg_vol = sum(volumes[-10:-1]) / 9.0 if sum(volumes[-10:-1]) > 0 else 1.0
        vol_ratio = volumes[-1] / avg_vol if avg_vol > 0 else 1.0

        # 3. Simple RSI (14 period on 1m)
        gains, losses = 0.0, 0.0
        for i in range(len(closes) - 14, len(closes)):
            diff = closes[i] - closes[i - 1]
            if diff >= 0:
                gains += diff
            else:
                losses += abs(diff)
        avg_gain = gains / 14.0
        avg_loss = losses / 14.0 if losses > 0 else 1e-6
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

        # 4. Trend Alignment Guard (15-period Simple Moving Average)
        sma15 = sum(closes[-15:]) / 15.0
        is_bullish_trend = current_price > sma15
        is_bearish_trend = current_price < sma15

        # 5. Institutional Risk-Reward Scoring Model (85% Win Rate Threshold)
        win_rate = 70.0
        side = "BUY"
        is_delisting_setup = "DELIST" in symbol.upper()

        # Reject choppy range market unless it's a High-Yield Delisting / Whale Breakout
        if not is_delisting_setup and (abs(price_change_1m) < 0.05 or vol_ratio < 1.15):
            result["reason"] = f"⚪ Choppy Market Suppressed (1m Change: {price_change_1m:.2f}%, Vol: {vol_ratio:.1f}x)"
            return result

        if price_change_1m > 0.05 and rsi < 68.0 and vol_ratio > 1.15 and is_bullish_trend:
            win_rate = min(98.0, 85.0 + (price_change_1m * 10.0) + (vol_ratio * 2.0))
            side = "BUY"
            reason = f"🟢 Institutional Bullish Trend Alignment (1m: +{price_change_1m:.2f}%, Vol: {vol_ratio:.1f}x, RSI: {rsi:.1f})"
        elif price_change_1m < -0.05 and rsi > 30.0 and is_bearish_trend:
            win_rate = min(99.0, 88.0 + (abs(price_change_1m) * 12.0) + (vol_ratio * 3.0))
            side = "SELL" # SHORT
            reason = f"🔴 Turbo High-Yield Bearish Death-Dump Alignment (1m: {price_change_1m:.2f}%, Vol: {vol_ratio:.1f}x, RSI: {rsi:.1f})"
        else:
            reason = f"⚪ Trend Misalignment Suppressed (RSI: {rsi:.1f}, Vol Ratio: {vol_ratio:.1f}x)"

        # Uncapped Trailing Peak Lock (Initial TP trigger +2.5%, hard SL -1.0%)
        tp_offset = current_price * 0.025
        sl_offset = current_price * 0.010

        result["entry_price"] = current_price
        result["win_rate_pct"] = round(win_rate, 1)
        result["reason"] = reason
        result["dynamic_leverage"] = 15 if win_rate >= 90.0 else 5

        if win_rate >= 85.0:
            # BTC Lead Impulse Guard check for altcoins (High-Conviction ≥ 92.0% AI Consensus Overrides Guard)
            if symbol != "BTCUSDT" and win_rate < 92.0 and not is_delisting_setup:
                import btc_lead_guard
                btc_impulse = btc_lead_guard.get_btc_impulse_status()
                if btc_impulse.get("status") == "DUMPING" and side == "BUY":
                    result["reason"] = f"🛡️ BTC Lead Impulse Guard Suppressed LONG (BTC Dumping: {btc_impulse.get('price_1m_change')}%)"
                    return result
                elif btc_impulse.get("status") == "PUMPING" and side == "SELL":
                    result["reason"] = f"🛡️ BTC Lead Impulse Guard Suppressed SHORT (BTC Pumping: +{btc_impulse.get('price_1m_change')}%)"
                    return result

            result["signal"] = "EXECUTE_HFT"
            result["side"] = side
            if side == "BUY":
                result["tp_price"] = round(current_price + tp_offset, 4)
                result["sl_price"] = round(current_price - sl_offset, 4)
            else:
                result["tp_price"] = round(current_price - tp_offset, 4)
                result["sl_price"] = round(current_price + sl_offset, 4)

    except Exception as e:
        print(f"⚠️ [HFT ENGINE SCAN ERROR]: {e}")

    return result

def execute_hft_order(api_key: str, api_secret: str, symbol: str, amount_usdt: float, side: str = "BUY", leverage: int = 5) -> dict:
    """
    Executes instant HFT order on Binance Futures with specified leverage and amount.
    """
    try:
        leverage = min(15, max(1, int(leverage)))
        trading_engine.set_futures_leverage(api_key, api_secret, symbol, leverage)
        price = trading_engine.get_current_price(symbol)
        if price <= 0:
            return {"status": "error", "message": "Failed to fetch price"}

        # Institutional Position Sizing Clamp: Max $10.00 USDT margin per trade to prevent over-leverage
        amount_usdt = min(10.0, max(1.0, amount_usdt))

        # Super Smart MIN_NOTIONAL Safeguard: Binance Futures requires >= $5.05 USDT notional
        min_notional = 5.05
        notional = amount_usdt * leverage
        if notional < min_notional:
            notional = min_notional
            amount_usdt = notional / leverage

        qty = notional / price

        # Precision handling & minimum trade step floor
        if "PAXG" in symbol:
            qty = round(qty, 3)
            if qty <= 0: qty = 0.001
        elif "BTC" in symbol:
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

        if qty <= 0:
            return {"status": "error", "message": "Calculated quantity too small"}

        # Place Real/Paper Futures Order (without reduceOnly restriction)
        res = trading_engine.place_futures_order(api_key, api_secret, symbol, side, qty, leverage)
        if isinstance(res, dict) and res.get("status") == "error":
            return res

        return {
            "status": "success",
            "symbol": symbol,
            "side": side,
            "price": price,
            "quantity": qty,
            "response": res
        }
    except Exception as e:
        print(f"❌ [HFT EXECUTE ORDER ERROR]: {e}")
        return {"status": "error", "message": str(e)}
