import re

def parse_turbo_hedge_args(args):
    raw_args = [a.strip() for a in args]
    is_spot_prefix = (raw_args[0].upper() == "SPOT")
    is_hedge_prefix = (raw_args[0].upper() == "HEDGE")
    if is_spot_prefix or is_hedge_prefix:
        raw_args.pop(0)

    if not raw_args or len(raw_args) < 2:
        return {"error": "insufficient_args"}

    symbol_raw = raw_args[0].upper().strip()
    pin = str(raw_args[-1]).strip()
    inner_args = raw_args[1:-1]

    if symbol_raw in ["AUTO", "SCAN", "TOP", "ON", "START", "RUN"]:
        symbol = "TOP"
    elif symbol_raw.replace('.', '', 1).isdigit():
        symbol = "TOP"
        inner_args = [symbol_raw] + list(inner_args)
    elif not symbol_raw.endswith("USDT"):
        symbol = symbol_raw + "USDT"
    else:
        symbol = symbol_raw

    user_side_input = "SPOT" if is_spot_prefix else ("HEDGE" if is_hedge_prefix else "AUTO")
    target_tp = 2.5
    amount = 5.0
    leverage = 1 if (is_spot_prefix or is_hedge_prefix) else 10
    top_count = 20

    if is_spot_prefix:
        leverage = 1
        user_side_input = "SPOT"
        spot_nums = []
        for tok in inner_args:
            u = tok.upper()
            if u in ["AUTO", "BUY", "BREAKOUT"]:
                pass
            else:
                try:
                    spot_nums.append(float(tok))
                except ValueError:
                    pass
        if spot_nums:
            amount = spot_nums[0]
            if len(spot_nums) >= 2:
                target_tp = spot_nums[1]
        else:
            amount = 50.0
    elif is_hedge_prefix:
        leverage = 1
        user_side_input = "HEDGE"
        if inner_args:
            try: amount = float(inner_args[0])
            except ValueError: amount = 100.0
    else:
        # FUTURES MODE
        if symbol == "TOP":
            # Check if side token is embedded in inner_args
            side_idx = -1
            for i, tok in enumerate(inner_args):
                if tok.upper() in ["BUY", "SELL", "AUTO", "SPOT"]:
                    user_side_input = tok.upper()
                    side_idx = i
                    break
            
            if side_idx != -1:
                before_tokens = inner_args[:side_idx]
                after_tokens = inner_args[side_idx+1:]
                before_nums = []
                for t in before_tokens:
                    try: before_nums.append(float(t))
                    except ValueError: pass
                after_nums = []
                for t in after_tokens:
                    try: after_nums.append(float(t))
                    except ValueError: pass

                if len(before_nums) >= 2:
                    top_count = int(before_nums[0])
                    leverage = int(before_nums[1])
                elif len(before_nums) == 1:
                    top_count = int(before_nums[0])

                if len(after_nums) >= 2:
                    amount = float(after_nums[0])
                    target_tp = float(after_nums[1])
                elif len(after_nums) == 1:
                    amount = float(after_nums[0])
            else:
                nums = []
                for tok in inner_args:
                    try: nums.append(float(tok))
                    except ValueError: pass
                if len(nums) >= 4:
                    top_count = int(nums[0])
                    leverage = int(nums[1])
                    amount = float(nums[2])
                    target_tp = float(nums[3])
                elif len(nums) == 3:
                    if nums[0] > 15:
                        top_count = int(nums[0])
                        leverage = int(nums[1])
                        amount = float(nums[2])
                    else:
                        amount = float(nums[0])
                        leverage = int(nums[1])
                        target_tp = float(nums[2])
                        top_count = 10
                elif len(nums) == 2:
                    if nums[0] > 15:
                        top_count = int(nums[0])
                        leverage = int(nums[1])
                    else:
                        amount = float(nums[0])
                        leverage = int(nums[1])
                elif len(nums) == 1:
                    amount = float(nums[0])

    return {
        "symbol": symbol,
        "user_side_input": user_side_input,
        "top_count": top_count,
        "leverage": leverage,
        "amount": amount,
        "target_tp": target_tp,
        "pin": pin
    }

# Test Cases
t1 = parse_turbo_hedge_args(["TOP", "20", "10", "AUTO", "5", "1234"])
print("Test 1 /smart_trade TOP 20 10 AUTO 5 1234:", t1)
assert t1["symbol"] == "TOP"
assert t1["top_count"] == 20
assert t1["leverage"] == 10
assert t1["user_side_input"] == "AUTO"
assert t1["amount"] == 5.0
assert t1["pin"] == "1234"

t2 = parse_turbo_hedge_args(["SPOT", "TOP", "AUTO", "50", "1234"])
print("Test 2 /smart_trade SPOT TOP AUTO 50 1234:", t2)
assert t2["symbol"] == "TOP"
assert t2["user_side_input"] == "SPOT"
assert t2["leverage"] == 1
assert t2["amount"] == 50.0
assert t2["pin"] == "1234"

t3 = parse_turbo_hedge_args(["SPOT", "50", "1234"])
print("Test 3 /smart_trade SPOT 50 1234:", t3)
assert t3["symbol"] == "TOP"
assert t3["user_side_input"] == "SPOT"
assert t3["amount"] == 50.0

t4 = parse_turbo_hedge_args(["SPOT", "SOL", "50", "1234"])
print("Test 4 /smart_trade SPOT SOL 50 1234:", t4)
assert t4["symbol"] == "SOLUSDT"
assert t4["user_side_input"] == "SPOT"
assert t4["amount"] == 50.0

t5 = parse_turbo_hedge_args(["TOP", "20", "10", "BUY", "5", "1234"])
print("Test 5 /smart_trade TOP 20 10 BUY 5 1234:", t5)
assert t5["top_count"] == 20
assert t5["leverage"] == 10
assert t5["user_side_input"] == "BUY"
assert t5["amount"] == 5.0

print("\nALL PARSER UNIT TESTS PASSED 100%!")
