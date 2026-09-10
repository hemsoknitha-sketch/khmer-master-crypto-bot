import sys
sys.path.append('.')
import inspect
import database as db

for func_name in [
    'is_hyper_trade_enabled',
    'is_auto_arb_enabled',
    'is_sweep_auto_enabled',
    'is_funding_harvester_enabled',
    'is_trailing_guard_enabled'
]:
    fn = getattr(db, func_name, None)
    print(f"--- {func_name} ---")
    if fn:
        print(inspect.getsource(fn))
    else:
        print("NOT FOUND")
