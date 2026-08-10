import time

# Rolling depth snapshots per symbol (symbol -> list of snapshots)
# Each snapshot: {"timestamp": float_ms, "bids": list, "asks": list}
DEPTH_SNAPSHOTS = {}

def record_snapshot(symbol: str, bids: list, asks: list, timestamp_ms: float = None):
    """Records an Orderbook Depth Snapshot for anti-spoofing analysis."""
    symbol_clean = symbol.upper()
    now_ms = timestamp_ms if timestamp_ms is not None else (time.time() * 1000.0)
    
    if symbol_clean not in DEPTH_SNAPSHOTS:
        DEPTH_SNAPSHOTS[symbol_clean] = []
        
    snapshots = DEPTH_SNAPSHOTS[symbol_clean]
    snapshots.append({"timestamp": now_ms, "bids": bids, "asks": asks})
    
    # Keep only last 30 snapshots
    if len(snapshots) > 30:
        DEPTH_SNAPSHOTS[symbol_clean] = snapshots[-30:]

def detect_spoofing(symbol: str, bids: list, asks: list, wall_threshold_usdt: float = 50000.0, max_lifetime_ms: float = 500.0, timestamp_ms: float = None) -> dict:
    """
    Detects Orderbook Spoofing / Fake Liquidity:
    Identifies massive Bid/Ask walls (>= $50k) that appeared and were cancelled in < 500ms.
    Returns: {"is_spoofing": bool, "fake_wall_type": "BID"|"ASK"|None, "spoof_usdt": float}
    """
    symbol_clean = symbol.upper()
    now_ms = timestamp_ms if timestamp_ms is not None else (time.time() * 1000.0)
    
    record_snapshot(symbol_clean, bids, asks, now_ms)
    snapshots = DEPTH_SNAPSHOTS.get(symbol_clean, [])
    
    if len(snapshots) < 2:
        return {"is_spoofing": False, "fake_wall_type": None, "spoof_usdt": 0.0}
        
    # Look back at snapshots within max_lifetime_ms (< 500ms ago)
    curr_bid_prices = set(float(b[0]) for b in bids)
    curr_ask_prices = set(float(a[0]) for a in asks)
    
    for snap in reversed(snapshots[:-1]):
        age_ms = now_ms - snap["timestamp"]
        if age_ms > max_lifetime_ms:
            break
            
        # Check previous Bid walls >= $50k that suddenly vanished in current snapshot
        for price_str, qty_str in snap["bids"]:
            price = float(price_str)
            qty = float(qty_str)
            val = price * qty
            
            if val >= wall_threshold_usdt:
                # If this $50k+ wall is missing from current bids -> Spoofing Fake Wall
                if price not in curr_bid_prices:
                    print(f"[ANTI-SPOOFING] Fake Bid Wall Detected on {symbol_clean}: ${val:,.0f} at ${price:,.4f} vanished in {age_ms:.0f}ms!")
                    return {
                        "is_spoofing": True,
                        "fake_wall_type": "BID",
                        "spoof_usdt": round(val, 2)
                    }
                    
        # Check previous Ask walls >= $50k that suddenly vanished in current snapshot
        for price_str, qty_str in snap["asks"]:
            price = float(price_str)
            qty = float(qty_str)
            val = price * qty
            
            if val >= wall_threshold_usdt:
                if price not in curr_ask_prices:
                    print(f"[ANTI-SPOOFING] Fake Ask Wall Detected on {symbol_clean}: ${val:,.0f} at ${price:,.4f} vanished in {age_ms:.0f}ms!")
                    return {
                        "is_spoofing": True,
                        "fake_wall_type": "ASK",
                        "spoof_usdt": round(val, 2)
                    }
                    
    return {"is_spoofing": False, "fake_wall_type": None, "spoof_usdt": 0.0}
