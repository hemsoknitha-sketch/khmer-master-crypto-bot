import time
import requests
import asyncio

BINANCE_HOT_WALLET = "0x28C6c06298d514Db089934071355E5743bf21d60"

# Memory state for dumping risk lockouts (symbol -> expire_timestamp)
WHALE_DUMPING_RISK_LOCKOUTS = {}

def set_dumping_risk_lockout(symbol: str, duration_mins: int = 30):
    """Sets a Dumping Risk Lockout for a symbol when massive exchange deposit is detected."""
    expire_ts = time.time() + (duration_mins * 60)
    WHALE_DUMPING_RISK_LOCKOUTS[symbol.upper()] = expire_ts
    print(f"[WHALE RADAR] Dumping Risk Lockout activated for {symbol} for {duration_mins}m!")


def is_dumping_risk_active(symbol: str) -> tuple[bool, int]:
    """
    Checks if Dumping Risk Lockout is active for a symbol.
    Returns: (is_active, remaining_mins)
    """
    now = time.time()
    expire_ts = WHALE_DUMPING_RISK_LOCKOUTS.get(symbol.upper(), 0)
    if now < expire_ts:
        rem_mins = int((expire_ts - now) / 60) + 1
        return True, rem_mins
    return False, 0

def process_token_transfer(symbol: str, value_usdt: float, is_deposit: bool) -> dict:
    """
    Processes an On-Chain Whale Token Transfer.
    Inflow >= $1M -> Inflow Dump Risk (Auto-Trades Paused for 30m)
    Outflow >= $1M -> Outflow Accumulation (+15% AI Confidence Boost)
    """
    symbol_clean = symbol.upper()
    if is_deposit and value_usdt >= 1_000_000:
        set_dumping_risk_lockout(symbol_clean, 30)
        return {
            "action": "INFLOW_DUMP_RISK",
            "symbol": symbol_clean,
            "value_usdt": value_usdt,
            "lockout_mins": 30
        }
    elif not is_deposit and value_usdt >= 1_000_000:
        return {
            "action": "OUTFLOW_ACCUMULATION",
            "symbol": symbol_clean,
            "value_usdt": value_usdt,
            "confidence_boost": 15.0
        }
    else:
        return {
            "action": "NEUTRAL",
            "symbol": symbol_clean,
            "value_usdt": value_usdt
        }
