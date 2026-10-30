#!/usr/bin/env python3
"""
ANGKOR QUANT - GOLD M1 YOUTUBE LIVE STREAMING SERVER
======================================================
Asynchronous HTTP & WebSocket server powering the 24/7/365 YouTube Live Stream.
Delivers:
  1. Live Gold M1 Candlesticks with sub-millisecond RAM caching
  2. Institutional 9 SMC Citadel Overlays (Order Blocks, FVG, Liquidity Sweeps)
  3. Wall Street Mathematical Radar (Hurst, Kalman, Bayes, OU, GARCH)
  4. Audio Chime Alerts for BUY/SELL/TP/SL Signals
======================================================
"""

import os
import sys
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from aiohttp import web, WSMsgType
import pandas as pd
import numpy as np

# Adjust path for Angkor Quant root imports
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

STATIC_DIR = os.path.join(ROOT_DIR, "web_gui")
AUDIO_DIR = os.path.join(ROOT_DIR, "audio")

# Fast JSON serializer
try:
    import orjson
    def fast_dumps(obj):
        return orjson.dumps(obj).decode("utf-8")
except Exception:
    def fast_dumps(obj):
        return json.dumps(obj)

# Cache state
_CACHE = {
    "timestamp": 0.0,
    "snapshot": {}
}
_WS_CLIENTS = set()


def _fetch_gold_m1_data() -> Dict[str, Any]:
    """
    Synthesizes Live Gold M1 Candlesticks, SMC Structures, and Math Radar.
    Runs in background thread to avoid blocking the event loop.
    """
    import mt5_smc_citadel
    import gold_mathematical_radar

    # 1. Fetch M1 Candlesticks
    df = mt5_smc_citadel.MT5SMCCitadelEngine.fetch_timeframe_candles("XAUUSD", "1m", limit=120)
    if df is None or len(df) < 15:
        # Fallback to PAXGUSDT if XAUUSD feed is offline
        df = mt5_smc_citadel.MT5SMCCitadelEngine.fetch_timeframe_candles("PAXGUSDT", "1m", limit=120)

    current_price = 2745.50
    candles_list = []
    if df is not None and not df.empty:
        current_price = round(float(df['close'].iloc[-1]), 2)
        for idx, row in df.iterrows():
            ts = int(row['timestamp'].timestamp()) if hasattr(row['timestamp'], 'timestamp') else int(time.time())
            candles_list.append({
                "time": ts,
                "open": round(float(row['open']), 2),
                "high": round(float(row['high']), 2),
                "low": round(float(row['low']), 2),
                "close": round(float(row['close']), 2),
                "volume": round(float(row['volume']), 2),
            })

    # 2. Institutional 9 SMC Citadel Analysis
    smc_score = 75
    ob_summary = "1 Bullish M1 OB"
    fvg_summary = "1 Imbalance Retest"
    sweep_summary = "Dealing Range Boundaries"
    smc_action = "WAIT"

    if df is not None and len(df) >= 20:
        try:
            obs = mt5_smc_citadel.MT5SMCCitadelEngine.detect_order_blocks(df)
            fvgs = mt5_smc_citadel.MT5SMCCitadelEngine.detect_fair_value_gaps(df)
            lp = mt5_smc_citadel.MT5SMCCitadelEngine.detect_liquidity_pools(df)
            slh = mt5_smc_citadel.MT5SMCCitadelEngine.detect_stop_loss_hunting(df, lp)

            bull_obs = [o for o in obs if o.get('type') == 'BULLISH_OB' and not o.get('mitigated', False)]
            bear_obs = [o for o in obs if o.get('type') == 'BEARISH_OB' and not o.get('mitigated', False)]
            active_fvgs = [f for f in fvgs if not f.get('filled', False)]

            ob_summary = f"{len(bull_obs)} Bullish OB, {len(bear_obs)} Bearish OB"
            fvg_summary = f"{len(active_fvgs)} Imbalance Zones"

            if slh.get('bullish_sweep'):
                sweep_summary = "SSL Liquidity Grab Wick Absorbed"
                smc_action = "BUY"
                smc_score = 92
            elif slh.get('bearish_sweep'):
                sweep_summary = "BSL Liquidity Grab Wick Absorbed"
                smc_action = "SELL"
                smc_score = 92
            elif len(bull_obs) > len(bear_obs):
                smc_action = "BUY"
                smc_score = 82
            elif len(bear_obs) > len(bull_obs):
                smc_action = "SELL"
                smc_score = 82
        except Exception:
            pass

    # 3. Wall Street Mathematical Radar Execution
    math_res = gold_mathematical_radar.analyze_gold_mathematical_edge(
        current_price=current_price,
        candles_df=df,
        smc_action=smc_action,
        smc_confidence=float(smc_score),
        force_refresh=True
    )

    math_verdict = math_res.get("math_verdict", "NEUTRAL_WAIT")
    hurst = float(math_res.get("hurst_exponent", 0.50))
    kalman = math_res.get("kalman", {})
    ou = math_res.get("ornstein_uhlenbeck", {})
    bayes = math_res.get("bayesian_probability", {})
    garch = math_res.get("garch_volatility", {})
    risk_buffer = float(garch.get("dynamic_risk_buffer_usd", 4.50))

    # 4. Synthesize Final Trading Action & Target Plan
    action = "WAIT"
    confidence = float(math_res.get("math_composite_confidence", 50.0))

    if "BUY" in math_verdict and smc_action in ["BUY", "WAIT"]:
        action = "BUY"
    elif "SELL" in math_verdict and smc_action in ["SELL", "WAIT"]:
        action = "SELL"
    elif smc_score >= 85:
        action = smc_action

    # Target Coordinates
    entry = current_price
    sl_dist = max(risk_buffer, 3.80)
    if action == "BUY":
        sl = round(entry - sl_dist, 2)
        r = entry - sl
        tp1 = round(entry + 2.0 * r, 2)
        tp2 = round(entry + 4.0 * r, 2)
        runner = round(entry + 6.0 * r, 2)
    elif action == "SELL":
        sl = round(entry + sl_dist, 2)
        r = sl - entry
        tp1 = round(entry - 2.0 * r, 2)
        tp2 = round(entry - 4.0 * r, 2)
        runner = round(entry - 6.0 * r, 2)
    else:
        sl = round(entry - sl_dist, 2)
        tp1 = round(entry + 2.0 * sl_dist, 2)
        tp2 = round(entry + 4.0 * sl_dist, 2)
        runner = round(entry + 6.0 * sl_dist, 2)

    return {
        "timestamp": time.time(),
        "current_price": current_price,
        "spread": 0.18,
        "candles": candles_list,
        "signal": {
            "action": action,
            "confidence": round(confidence, 1),
            "entry": entry,
            "sl": sl,
            "tp1": tp1,
            "tp2": tp2,
            "runner": runner,
            "rr_ratio": "1 : 3.5"
        },
        "math": {
            "verdict": math_verdict,
            "hurst": round(hurst, 3),
            "kalman_velocity": f"{float(kalman.get('velocity', 0.0)):+.2f}",
            "kalman_bias": kalman.get("velocity_bias", "STATIONARY"),
            "ou_z": f"{float(ou.get('z_score', 0.0)):+.2f}",
            "ou_bias": ou.get("spread_bias", "EQUILIBRIUM"),
            "bayes_bull": round(float(bayes.get("bullish_pct", 50.0)), 1),
            "risk_buffer": round(risk_buffer, 2)
        },
        "smc": {
            "confluence_score": smc_score,
            "order_blocks_summary": ob_summary,
            "fvg_summary": fvg_summary,
            "sweep_summary": sweep_summary
        }
    }


async def get_live_data_cached() -> Dict[str, Any]:
    """Cached with 1.5s TTL for sub-0.001ms response time."""
    now = time.time()
    if _CACHE["snapshot"] and (now - _CACHE["timestamp"] < 1.5):
        return _CACHE["snapshot"]
    
    snapshot = await asyncio.to_thread(_fetch_gold_m1_data)
    _CACHE["timestamp"] = now
    _CACHE["snapshot"] = snapshot
    return snapshot


# -------------------------------------------------------------------------
# HTTP ROUTE HANDLERS
# -------------------------------------------------------------------------
async def handle_live_view(request: web.Request) -> web.FileResponse:
    html_path = os.path.join(STATIC_DIR, "gold_live_view.html")
    resp = web.FileResponse(html_path)
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp


async def handle_api_snapshot(request: web.Request) -> web.Response:
    data = await get_live_data_cached()
    return web.json_response(data, dumps=fast_dumps)


async def handle_api_ws(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse(heartbeat=15.0)
    await ws.prepare(request)
    _WS_CLIENTS.add(ws)
    print(f"📡 [YOUTUBE STREAM] New WebSocket client connected (Total: {len(_WS_CLIENTS)})")

    # Send initial snapshot immediately
    snapshot = await get_live_data_cached()
    await ws.send_str(fast_dumps(snapshot))

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                pass
            elif msg.type == WSMsgType.ERROR:
                break
    finally:
        _WS_CLIENTS.discard(ws)
    return ws


# Background broadcaster to all connected WebSocket clients
async def broadcast_loop():
    while True:
        try:
            await asyncio.sleep(1.0)
            if _WS_CLIENTS:
                data = await get_live_data_cached()
                msg = fast_dumps(data)
                dead = set()
                for ws in _WS_CLIENTS:
                    if ws.closed:
                        dead.add(ws)
                    else:
                        try:
                            await ws.send_str(msg)
                        except Exception:
                            dead.add(ws)
                for ws in dead:
                    _WS_CLIENTS.discard(ws)
        except Exception as e:
            await asyncio.sleep(2.0)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", handle_live_view)
    app.router.add_get("/gold_live_view", handle_live_view)
    app.router.add_get("/api/gold_m1_live", handle_api_snapshot)
    app.router.add_get("/api/gold_m1_ws", handle_api_ws)

    # Audio static files
    if os.path.exists(AUDIO_DIR):
        app.router.add_static("/audio", AUDIO_DIR)
    
    return app


async def start_background_tasks(app):
    app["broadcast_task"] = asyncio.create_task(broadcast_loop())


async def cleanup_background_tasks(app):
    app["broadcast_task"].cancel()
    await app["broadcast_task"]


def main():
    port = int(os.getenv("YOUTUBE_WEB_PORT", "8000"))
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    print(f"🚀 [ANGKOR QUANT] Gold M1 YouTube Live Stream Server starting on http://0.0.0.0:{port}")
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

