import time
import asyncio
import database as db
import trading_engine
import rvol_engine
import orderbook_engine
from notification_manager import send_smart_notification

# 30-second Cache for Total Capital
_CAPITAL_CACHE = {}

def get_total_deployable_capital(user_id: int, ai_engine=None):
    """
    Fetches the total deployable capital (USDT value of all held assets + free USDT).
    Uses a 30s in-memory cache to prevent Binance API Weight bans.
    Returns: float (Total USDT Equivalent)
    """
    now = time.time()
    if user_id in _CAPITAL_CACHE:
        cached_val, timestamp = _CAPITAL_CACHE[user_id]
        if now - timestamp < 30:
            return cached_val
            
    # Connect to Binance
    api_key, api_secret = db.get_api_keys(user_id)
    if not api_key or not api_secret:
        return 0.0
        
    try:
        # Get account balances
        balances = trading_engine.get_all_spot_balances(api_key, api_secret)
        
        total_usdt = 0.0
        
        if balances:
            for asset, free_amt in balances.items():
                if free_amt <= 0: continue
                
                if asset == 'USDT':
                    total_usdt += free_amt
                else:
                    # Convert to USDT
                    symbol = f"{asset}USDT"
                    current_price = trading_engine.get_current_price(symbol)
                    if current_price:
                        total_usdt += free_amt * current_price
                        
        # Update Cache
        _CAPITAL_CACHE[user_id] = (total_usdt, now)
        return total_usdt
        
    except Exception as e:
        print(f"Error fetching capital for user {user_id}: {e}")
        return 0.0

def score_asset(symbol: str, ai_engine) -> float:
    """
    Scoring Engine for an asset (0-100).
    Combines Trend Classifier, Volatility, and Prediction Confidence.
    """
    score = 50.0 # Base score
    
    try:
        # 1. AI Trend (0 - 40 pts)
        trend = ai_engine.predict_trend(symbol)
        if trend == "STRONG_BULLISH": score += 20
        elif trend == "BULLISH": score += 10
        elif trend == "BEARISH": score -= 15
        elif trend == "STRONG_BEARISH": score -= 25
        
        # 2. Prediction Confidence (0 - 30 pts)
        conf = ai_engine.predict_price_confidence(symbol)
        if conf > 80: score += 15
        elif conf > 65: score += 10
        elif conf < 50: score -= 10
        
        # 3. Orderbook Imbalance (0 - 20 pts)
        imbalance = orderbook_engine.get_imbalance(symbol)
        if imbalance > 2.0: score += 10 # Strong Buy Wall
        elif imbalance > 1.2: score += 5
        elif imbalance < 0.5: score -= 15 # Strong Sell Wall
        elif imbalance < 0.2: score -= 25 # Massive Sell Wall
        
    except Exception:
        pass
        
    # Cap score between 0 and 100
    return max(0.0, min(100.0, score))


async def run_ico_cycle(app, ai_engine):
    """
    The Core Engine of ICO.
    Evaluates current holdings, cuts bleeders, reallocates to highly scored RVOL targets.
    """
    if not db.is_global_rebalance_enabled(): return
    
    vip_users = db.get_vip_users_with_lang()
    for user_record in vip_users:
        user_id = user_record[0]
        if not db.is_auto_trade_enabled(user_id) or not db.is_user_opted_in_rebalance(user_id):
            continue
        if not db.can_user_rebalance(user_id):
            continue
            
        active_trades = db.get_active_trades_by_user(user_id)
        if not active_trades: continue
        
        # Determine total capital
        total_capital = await asyncio.to_thread(get_total_deployable_capital, user_id, ai_engine)
        if total_capital <= 0: continue
        
        import dynamic_allocator
        alloc_pct = dynamic_allocator.get_max_allocation(user_id, "ICO_SMART_REBALANCE")
        max_position_size = total_capital * (alloc_pct / 100.0)
        
        candidates_to_liquidate = []
        
        # Step 2: Evaluate Holdings
        for trade in active_trades:
            trade_id, symbol, db_qty, buy_price, _, _ = trade
            if buy_price <= 0: continue
            
            score = await asyncio.to_thread(score_asset, symbol, ai_engine)
            if score < 30: # Bearish/Weak
                current_price = await asyncio.to_thread(trading_engine.get_current_price, symbol)
                if current_price:
                    pnl_pct = ((current_price - buy_price) / buy_price) * 100
                    if pnl_pct < 0:
                        candidates_to_liquidate.append((trade_id, symbol, pnl_pct, current_price))
                        
        if not candidates_to_liquidate: continue # Nothing to liquidate
        
        # Step 4: Find Targets
        top_rvol = []
        try:
            top_rvol = await asyncio.to_thread(rvol_engine.get_top_rvol, limit=5)
        except Exception: pass
        
        best_target = None
        best_target_score = 0
        
        for cand in top_rvol:
            cand_score = await asyncio.to_thread(score_asset, cand, ai_engine)
            if cand_score > 70 and cand_score > best_target_score:
                best_target = cand
                best_target_score = cand_score
                
        api_key, api_secret = db.get_api_keys(user_id)
        if not api_key or not api_secret: continue
        
        # Step 5: Execute Liquidations Concurrently & Completely (Zero Dust)
        async def liquidate_task(cand):
            trade_id, symbol, pnl_pct, current_price = cand
            try:
                base_coin = symbol.replace("USDT", "")
                # Get absolute real spot balance to leave 0 dust
                raw_balance = await asyncio.to_thread(trading_engine.get_spot_balance, api_key, api_secret, base_coin)
                
                # Format to exact lot size (100% dust-free)
                max_sellable = await asyncio.to_thread(trading_engine.get_max_sellable_qty, symbol, raw_balance)
                
                if max_sellable * current_price < 5.0:
                    return 0.0 # Min notional
                    
                sell_res = await asyncio.to_thread(trading_engine.place_market_sell, api_key, api_secret, symbol, max_sellable)
                if "error" in sell_res:
                    raise Exception(sell_res['error'])
                    
                db.remove_active_trade(trade_id, exit_price=current_price, pnl_pct=pnl_pct, reason="ICO_LIQUIDATION")
                
                msg_liquidate = f"⚖️ <b>ICO: Asset Liquidation</b>\n\n📉 កាត់ខាតអស់ 100% {symbol} ({pnl_pct:.2f}%) ព្រោះពិន្ទុ AI ធ្លាក់ក្រោម 30។"
                await send_smart_notification(app, user_id, msg_liquidate, category="ACTION")
                
                return float(max_sellable) * float(current_price) * 0.999
            except Exception as e:
                await send_smart_notification(app, user_id, f"ICO Liquidation Failed for {symbol}: {e}", category="CRITICAL")
                return 0.0
                
        # Run all liquidations in parallel for Zero-Second execution
        liquidation_results = await asyncio.gather(*(liquidate_task(c) for c in candidates_to_liquidate))
        total_recovered_usdt = sum(liquidation_results)
        
        # Step 6: Buy Target instantly with all recovered funds
        if total_recovered_usdt > 5.0 and best_target:
            try:
                # Enforce 20% Max Position Rule
                buy_usdt = min(total_recovered_usdt, max_position_size)
                
                buy_res = await asyncio.to_thread(trading_engine.place_market_buy, api_key, api_secret, best_target, quote_order_qty=buy_usdt)
                if "error" in buy_res:
                    raise Exception(buy_res['error'])
                    
                buy_price = float(buy_res.get('price', trading_engine.get_current_price(best_target)))
                buy_qty = float(buy_res.get('origQty', buy_usdt / buy_price))
                
                db.add_active_trade(user_id, best_target, buy_qty, buy_price, current_highest=buy_price, stop_loss_pct=0.0)
                msg_realloc = f"⚖️ <b>ICO: Capital Reallocation</b>\n\n🚀 ប្តូរទុនសរុប ${buy_usdt:.2f} ទៅ {best_target} ភ្លាមៗ (Zero Seconds)\n🤖 ពិន្ទុ AI ខ្ពស់: {best_target_score:.1f}"
                await send_smart_notification(app, user_id, msg_realloc, category="ACTION")
                db.increment_user_rebalance(user_id)
            except Exception as e:
                await send_smart_notification(app, user_id, f"ICO Reallocation Failed: {e}", category="CRITICAL")
