import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            # --- SCALPERS ---
            for scalper in scalpers:
                scalper_id, sym, inv_amt, target_pct, stop_loss_pct, current_pos, entry_price = scalper
                current_price = trading_engine.get_current_price(sym)
                
                valid_trades_found = True
                
                pnl = 0.0
                if current_pos > 0 and entry_price > 0:
                    pnl_pct = ((current_price - entry_price) / entry_price) * 100
                    pnl = inv_amt * (pnl_pct / 100.0)'''

replacement = '''            # --- SCALPERS ---
            for scalper in scalpers:
                scalper_id, sym, inv_amt, target_pct, current_state, entry_price = scalper
                current_price = trading_engine.get_current_price(sym)
                
                valid_trades_found = True
                
                pnl = 0.0
                if current_state == 'BOUGHT' and entry_price > 0:
                    pnl_pct = ((current_price - entry_price) / entry_price) * 100
                    pnl = inv_amt * (pnl_pct / 100.0)'''

if 'current_state == \'BOUGHT\'' not in content:
    content = content.replace(target, replacement)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched bot_thread.py for scalper variables")
else:
    print("Already patched")
