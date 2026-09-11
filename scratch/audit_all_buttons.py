import os
import re
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def audit_all_buttons():
    print("======================================================================")
    print("🔍 COMPREHENSIVE REPOSITORY-WIDE INLINE BUTTON AUDIT")
    print("======================================================================")

    # 1. Read bot_thread.py
    with open("bot_thread.py", "r", encoding="utf-8") as f:
        bot_code = f.read()

    # 2. Scan all python files for callback_data
    all_buttons = {}
    py_files = [f for f in os.listdir(".") if f.endswith(".py")]

    for pf in py_files:
        with open(pf, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Match static callback_data="..."
        static_matches = re.findall(r'callback_data=["\']([^"\']+)["\']', content)
        for m in static_matches:
            if m not in all_buttons:
                all_buttons[m] = []
            all_buttons[m].append(pf)

        # Match dynamic callback_data=f"btn_report_..."
        dyn_matches = re.findall(r'callback_data=f["\']([^"\'{]+)', content)
        for d in dyn_matches:
            prefix = d.strip()
            if prefix and prefix not in all_buttons:
                all_buttons[prefix] = []
            all_buttons[prefix].append(f"{pf} (dynamic)")

    print(f"Total Unique Button Signatures Found Across Repository: {len(all_buttons)}")

    unhandled = []
    handled = []

    for b, files in sorted(all_buttons.items()):
        escaped_b = re.escape(b)
        patterns = [
            rf'data\s*==\s*["\']{escaped_b}["\']',
            rf'["\']{escaped_b}["\']\s*==\s*data',
            rf'["\']{escaped_b}["\']\s*in\s*data',
            rf'data\s*in\s*\[[^\]]*["\']{escaped_b}["\'][^\]]*\]',
            rf'data\s*in\s*\{{[^\}}]*["\']{escaped_b}["\'][^\}}]*\}}',
            rf'data\s*in\s*\([^\)]*["\']{escaped_b}["\'][^\)]*\)',
        ]
        found = False
        for p in patterns:
            if re.search(p, bot_code):
                found = True
                break
        
        if not found:
            # Check startswith
            for m in re.finditer(r'(?:data|query\.data)\.startswith\(["\']([^"\']+)["\']\)', bot_code):
                prefix = m.group(1)
                if b.startswith(prefix):
                    found = True
                    break
        
        if found:
            handled.append(b)
        else:
            unhandled.append((b, files))

    print(f"\n✅ Handled Buttons: {len(handled)}")
    if unhandled:
        print(f"❌ Unhandled / Dead Buttons ({len(unhandled)}):")
        for ub, fls in unhandled:
            print(f"   - '{ub}' in {set(fls)}")
    else:
        print("🎉 ALL BUTTONS IN ALL FILES ARE 100% ROUTED AND FUNCTIONAL!")

    return len(unhandled) == 0

if __name__ == "__main__":
    success = audit_all_buttons()
    sys.exit(0 if success else 1)
