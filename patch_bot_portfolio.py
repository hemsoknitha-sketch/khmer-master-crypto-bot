import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            trades = db.get_active_trades_by_user(chat_id)
            if not trades:
                await update.message.reply_text('🤷‍♂️ អ្នកមិនមានប្រតិបត្តិការ (Trades) កំពុងដំណើរការទេ។' if user_lang == 'khmer' else '🤷‍♂️ You have no active trades.')
                return
                
            import trading_engine
            msg = '📊 **ការវិនិយោគរបស់អ្នក (PORTFOLIO):**\\n\\n' if user_lang == 'khmer' else '📊 **YOUR PORTFOLIO:**\\n\\n'
            total_profit = 0.0
            total_invested = 0.0
            valid_trades_found = False
            
            for trade in trades:
                trade_id, sym, qty, buy_price, current_highest, stop_loss_pct = trade'''

replacement = '''            trades = db.get_active_trades_by_user(chat_id)
            infinity_grids = db.get_active_infinity_grids_by_user(chat_id)
            scalpers = db.get_active_scalpers_by_user(chat_id)
            
            if not trades and not infinity_grids and not scalpers:
                await update.message.reply_text('🤷‍♂️ អ្នកមិនមានប្រតិបត្តិការ (Trades) កំពុងដំណើរការទេ។' if user_lang == 'khmer' else '🤷‍♂️ You have no active trades.')
                return
                
            import trading_engine
            msg = '📊 **ការវិនិយោគរបស់អ្នក (PORTFOLIO):**\\n\\n' if user_lang == 'khmer' else '📊 **YOUR PORTFOLIO:**\\n\\n'
            total_profit = 0.0
            total_invested = 0.0
            valid_trades_found = False
            
            # --- STANDARD SPOT TRADES ---
            for trade in trades:
                trade_id, sym, qty, buy_price, current_highest, stop_loss_pct = trade'''

if 'infinity_grids = db.get_active_infinity_grids_by_user' not in content:
    content = content.replace(target, replacement)
    
    # Also append Infinity Grid info right before "if not valid_trades_found:"
    target2 = '''            if not valid_trades_found:
                await update.message.reply_text('🤷‍♂️ អ្នកមិនមានប្រតិបត្តិការ (Trades) កំពុងដំណើរការទេ។' if user_lang == 'khmer' else '🤷‍♂️ You have no active trades.')
                return'''
                
    replacement2 = '''            # --- INFINITY GRIDS ---
            for grid in infinity_grids:
                grid_id, sym, amt_per_layer, step_pct, max_inv, current_inv, last_price = grid
                current_price = trading_engine.get_current_price(sym)
                
                valid_trades_found = True
                
                pnl = 0.0 # Simplify PnL calculation for Grid for display
                if current_price > 0 and last_price > 0:
                    pnl_pct = ((current_price - last_price) / last_price) * 100
                    pnl = current_inv * (pnl_pct / 100.0)
                
                total_invested += current_inv
                total_profit += pnl
                
                emoji = '🟩' if pnl >= 0 else '🟥'
                msg += f'🕸️ **Infinity Grid: {sym}**\\n'
                msg += f'💰 ដើមទុន: `${current_inv:,.2f}` / `${max_inv:,.2f}`\\n'
                msg += f'📈 តម្លៃបច្ចុប្បន្ន: `${current_price:,.4f}`\\n'
                msg += f'{emoji} ស្ថានភាព (Status): ដំណើរការ 24/7\\n\\n'
                
            # --- SCALPERS ---
            for scalper in scalpers:
                scalper_id, sym, inv_amt, target_pct, stop_loss_pct, current_pos, entry_price = scalper
                current_price = trading_engine.get_current_price(sym)
                
                valid_trades_found = True
                
                pnl = 0.0
                if current_pos > 0 and entry_price > 0:
                    pnl_pct = ((current_price - entry_price) / entry_price) * 100
                    pnl = inv_amt * (pnl_pct / 100.0)
                
                total_invested += inv_amt
                total_profit += pnl
                
                emoji = '🟩' if pnl >= 0 else '🟥'
                msg += f'⚡ **AI Scalper: {sym}**\\n'
                msg += f'💰 ដើមទុន: `${inv_amt:,.2f}`\\n'
                msg += f'💵 តម្លៃទិញ: `${entry_price:,.4f}`\\n'
                msg += f'📈 តម្លៃបច្ចុប្បន្ន: `${current_price:,.4f}`\\n'
                msg += f'{emoji} ប្រាក់ចំណេញ (PnL): `{pnl:+.2f}$`\\n\\n'

            if not valid_trades_found:
                await update.message.reply_text('🤷‍♂️ អ្នកមិនមានប្រតិបត្តិការ (Trades) កំពុងដំណើរការទេ។' if user_lang == 'khmer' else '🤷‍♂️ You have no active trades.')
                return'''
                
    content = content.replace(target2, replacement2)
    
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched bot_thread.py portfolio_command")
else:
    print("Already patched")
