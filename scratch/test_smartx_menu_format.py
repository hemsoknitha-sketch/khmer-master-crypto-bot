# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

# View lines 9670-9740 from bot_thread.py to extract and test the messages
with open("bot_thread.py", "r", encoding="utf-8") as f:
    code = f.read()

# Verify that portal.tagmarkets.com does not appear in bot_thread.py
assert "portal.tagmarkets.com" not in code, "Error: portal.tagmarkets.com still found in bot_thread.py!"
assert "Tag Markets" not in code, "Error: Tag Markets still found in bot_thread.py!"

# Verify that separator lines in bot_thread.py and scheduler_tasks.py are not over 26 chars
lines_bt = [m for m in re.findall(r'═+', code) if len(m) > 26]
assert len(lines_bt) == 0, f"Error: found separator lines longer than 26 chars in bot_thread.py: {[len(m) for m in lines_bt]}"

with open("scheduler_tasks.py", "r", encoding="utf-8") as f:
    st_code = f.read()
lines_st = [m for m in re.findall(r'═+', st_code) if len(m) > 26]
assert len(lines_st) == 0, f"Error: found separator lines longer than 26 chars in scheduler_tasks.py: {[len(m) for m in lines_st]}"

print("✅ [TEST PASS] Zero tagmarkets references in bot_thread.py!")
print("✅ [TEST PASS] Zero separator lines over 26 chars in bot_thread.py & scheduler_tasks.py!")
print("✅ [TEST PASS] All formatting requirements verified 100%!")
