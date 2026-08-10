import time
from datetime import datetime, timezone

# High Impact Macro Economic Events Registry
# Timestamps in Unix Seconds or ISO strings
REGISTERED_MACRO_EVENTS = [
    # Samples & Future Calendar Entries
    {"name": "FOMC Interest Rate Decision", "ts": 1785614400}, # Scheduled FOMC Event
    {"name": "US CPI Inflation Data Release", "ts": 1785009600}, # Scheduled CPI Event
    {"name": "Non-Farm Payrolls (NFP) Report", "ts": 1784404800} # Scheduled NFP Event
]

def add_macro_event(name: str, timestamp: float):
    """Registers a new upcoming macro economic event."""
    REGISTERED_MACRO_EVENTS.append({"name": name, "ts": timestamp})
    print(f"[MACRO GUARD] Registered upcoming event: {name} at {timestamp}")

def is_macro_event_active(window_hours: float = 2.0, current_ts: float = None) -> tuple[bool, str, int]:
    """
    Checks if current time is within +/- window_hours (default 2h) of any high-impact macro economic event.
    Returns: (is_active, event_name, remaining_mins)
    """
    now = current_ts if current_ts is not None else time.time()
    window_secs = window_hours * 3600.0
    
    for event in REGISTERED_MACRO_EVENTS:
        event_ts = event["ts"]
        diff = abs(now - event_ts)
        
        if diff <= window_secs:
            rem_secs = window_secs - diff
            rem_mins = int(rem_secs / 60) + 1
            return True, event["name"], rem_mins
            
    return False, "", 0
