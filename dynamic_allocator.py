import database as db
from notification_manager import send_smart_notification

STRATEGIES = [
    "HFT_SCALPING",
    "COMPOUND_GRID",
    "INFINITY_GRID",
    "ARBITRAGE",
    "ICO_SMART_REBALANCE"
]

def get_max_allocation(chat_id: int, strategy_name: str) -> float:
    """
    Returns the maximum allowed percentage of total capital (5.0 to 50.0).
    """
    if strategy_name not in STRATEGIES:
        return 20.0 # Default for unknown
    
    alloc = db.get_strategy_allocation(chat_id, strategy_name)
    return max(5.0, min(50.0, alloc))

async def run_allocation_cycle(app):
    """
    Evaluates PnL for each strategy and dynamically shifts capital.
    Runs hourly.
    """
    vip_users = db.get_vip_users_with_lang()
    for user_record in vip_users:
        user_id = user_record[0]
        
        strategy_stats = db.get_all_strategy_pnls(user_id)
        if not strategy_stats:
            continue
            
        changes = []
        
        for stat in strategy_stats:
            # stat: (strategy_name, total_pnl_usdt, win_count, loss_count, allocation_pct)
            strat = stat[0]
            pnl = stat[1]
            win = stat[2]
            loss = stat[3]
            current_alloc = stat[4]
            
            total_trades = win + loss
            if total_trades < 5:
                continue # Not enough data to judge
                
            win_rate = (win / total_trades) * 100
            
            new_alloc = current_alloc
            
            # Winner Logic
            if win_rate >= 60.0 and pnl > 0:
                new_alloc += 5.0
            # Loser Logic
            elif win_rate < 40.0 and pnl < 0:
                new_alloc -= 5.0
                
            # Clamp limits
            new_alloc = max(5.0, min(50.0, new_alloc))
            
            if new_alloc != current_alloc:
                db.set_strategy_allocation(user_id, strat, new_alloc)
                trend = "📈 បង្កើនទុន" if new_alloc > current_alloc else "📉 កាត់បន្ថយទុន"
                changes.append(f"{trend} <b>{strat}</b>: {current_alloc}% ➡️ <b>{new_alloc}%</b> (Win Rate: {win_rate:.1f}%)")
                
        if changes:
            msg = "⚖️ <b>Dynamic Capital Allocation</b>\n\nប្រព័ន្ធបានវាយតម្លៃប្រសិទ្ធភាពយុទ្ធសាស្ត្រ និងបែងចែកទុនថ្មីដោយស្វ័យប្រវត្តិ៖\n\n"
            msg += "\n".join(changes)
            msg += "\n\n_Apex AI ធានាថារាល់ដុល្លារ ធ្វើការនៅកន្លែងដែលចំណេញបំផុត!_"
            
            try:
                await send_smart_notification(app, user_id, msg, category="INFO")
            except:
                pass
