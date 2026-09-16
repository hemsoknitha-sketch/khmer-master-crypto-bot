# -*- coding: utf-8 -*-
"""
KHMER MASTER CRYPTO - AUTO SPOT PROFIT WEALTH HARVESTER (SUPER SMART OPTION B)
==============================================================================
Institutional Long-Term Wealth Accumulation & Profit Sweeper Engine:
- Automatically sweeps and transfers Futures profits >= $10.00 USDT into Spot Wallet.
- Automatically buys Physical Gold (PAXG) or Digital Gold (BTC) on Binance Spot.
- 0.00% Liquidation Risk on accumulated wealth.
- Fuses Dynamic Gold/BTC Valuation Ratio from gold_btc_rebalancer.py.
"""

import time
import asyncio
import database as db
import trading_engine
import gold_btc_rebalancer
from ui_standards import DIVIDER_DOUBLE, OFFICIAL_FOOTNOTE

HARVEST_THRESHOLD_USDT = 10.00


def get_user_harvest_config(chat_id: int) -> dict:
    """
    Retrieves user's Spot Profit Harvester configuration.
    Default: Enabled (1), Target Asset: DYNAMIC (Auto BTC/PAXG balance).
    """
    enabled = db.get_system_setting(f"spot_harvest_{chat_id}_enabled", "1") == "1"
    target_asset = db.get_system_setting(f"spot_harvest_{chat_id}_target_asset", "DYNAMIC").upper()
    unharvested_pool = float(db.get_system_setting(f"spot_harvest_{chat_id}_unharvested_pool", "0.0") or 0.0)
    total_harvested_usd = float(db.get_system_setting(f"spot_harvest_{chat_id}_total_harvested_usd", "0.0") or 0.0)
    
    return {
        "enabled": enabled,
        "target_asset": target_asset,
        "unharvested_pool": unharvested_pool,
        "total_harvested_usd": total_harvested_usd
    }


def set_user_harvest_config(chat_id: int, enabled: bool = None, target_asset: str = None) -> dict:
    """
    Updates user's Spot Profit Harvester configuration.
    """
    if enabled is not None:
        db.update_system_setting(f"spot_harvest_{chat_id}_enabled", "1" if enabled else "0")
    if target_asset is not None:
        target_asset = str(target_asset).upper().strip()
        if target_asset not in ["BTC", "PAXG", "GOLD", "DYNAMIC"]:
            target_asset = "DYNAMIC"
        db.update_system_setting(f"spot_harvest_{chat_id}_target_asset", target_asset)
    return get_user_harvest_config(chat_id)


def resolve_harvest_target_symbol(chat_id: int) -> tuple[str, str, str]:
    """
    Resolves target coin symbol and institutional rationale.
    Returns: (symbol, coin_name, reason)
    """
    cfg = get_user_harvest_config(chat_id)
    target_asset = cfg.get("target_asset", "DYNAMIC")
    
    if target_asset == "BTC":
        return "BTCUSDT", "Bitcoin (Digital Gold)", "User Preferred Asset: Bitcoin (BTC)"
    elif target_asset in ["PAXG", "GOLD"]:
        return "PAXGUSDT", "Physical LBMA Gold (PAXG)", "User Preferred Asset: Physical Gold (PAXG)"
    
    # Dynamic Valuation Selection using Gold/BTC Macro Ratio
    try:
        ratio_info = gold_btc_rebalancer.fetch_gold_btc_ratio()
        ratio = ratio_info.get("btc_gold_ratio", 26.5)
        if ratio > 35.0:
            return "PAXGUSDT", "Physical LBMA Gold (PAXG)", f"Macro Valuation Ratio {ratio:.1f}x > 35.0x (Gold is Undervalued -> HODL Gold!)"
        elif ratio < 20.0:
            return "BTCUSDT", "Bitcoin (Digital Gold)", f"Macro Valuation Ratio {ratio:.1f}x < 20.0x (BTC is Undervalued -> HODL BTC!)"
        else:
            return "BTCUSDT", "Bitcoin (Digital Gold)", f"Balanced Macro Ratio {ratio:.1f}x (Optimal Digital Gold Accumulation)"
    except Exception as e:
        print(f"⚠️ [SPOT HARVESTER] Macro ratio notice: {e}")
        return "BTCUSDT", "Bitcoin (Digital Gold)", "Default Institutional Wealth Anchor"


def check_and_harvest_futures_profit(
    chat_id: int, 
    api_key: str, 
    api_secret: str, 
    realized_pnl: float = 0.0, 
    app = None, 
    force: bool = False
) -> dict:
    """
    Evaluates cumulative realized profit. When unharvested profit >= $10.00 USDT:
    1. Transfers profit from Futures to Spot via Binance API.
    2. Executes Spot Market Buy for BTC or PAXG Gold.
    3. Records permanent wealth asset in SQLite database.
    4. Sends celebratory wealth accumulation notification to Telegram.
    """
    if not api_key or not api_secret:
        return {"status": "skipped", "reason": "MISSING_API_KEYS"}
    
    cfg = get_user_harvest_config(chat_id)
    if not cfg.get("enabled") and not force:
        return {"status": "skipped", "reason": "HARVEST_DISABLED"}
    
    # 1. Update unharvested profit pool
    current_pool = cfg.get("unharvested_pool", 0.0)
    if realized_pnl > 0:
        current_pool += realized_pnl
        db.update_system_setting(f"spot_harvest_{chat_id}_unharvested_pool", str(round(current_pool, 2)))
        print(f"🏦 [SPOT HARVEST POOL] User {chat_id}: Added +${realized_pnl:.2f} USDT -> Total Pool: ${current_pool:.2f} USDT (Target: >=${HARVEST_THRESHOLD_USDT:.2f})")
    
    if current_pool < HARVEST_THRESHOLD_USDT and not force:
        return {
            "status": "accumulating",
            "current_pool": current_pool,
            "threshold": HARVEST_THRESHOLD_USDT,
            "progress_pct": round((current_pool / HARVEST_THRESHOLD_USDT) * 100.0, 1)
        }
    
    harvest_amount = round(current_pool if not force else max(HARVEST_THRESHOLD_USDT, current_pool), 2)
    # Ensure MIN_NOTIONAL floor for Spot Buy (Min $10.50 to avoid -1013 Filter failure)
    harvest_amount = max(10.50, harvest_amount)
    
    # 2. Free Margin Safety Shield on Futures
    avail_fut = trading_engine.get_futures_available_balance(api_key, api_secret)
    if avail_fut < (harvest_amount + 5.0) and not trading_engine.PAPER_TRADING:
        print(f"🛡️ [SPOT HARVEST MARGIN GUARD] User {chat_id}: Futures free balance (${avail_fut:.2f}) is too tight to transfer ${harvest_amount:.2f} safely. Waiting for next cycle.")
        return {"status": "deferred", "reason": "INSUFFICIENT_FUTURES_MARGIN_BUFFER"}
    
    target_symbol, coin_name, rationale = resolve_harvest_target_symbol(chat_id)
    print(f"🚀 [SPOT WEALTH HARVEST INITIATED] User {chat_id}: Transferring ${harvest_amount:.2f} USDT to Spot to buy {target_symbol} ({rationale})...")
    
    # 3. Transfer from Futures to Spot
    transfer_res = trading_engine.transfer_futures_to_spot(api_key, api_secret, harvest_amount, asset="USDT")
    if not transfer_res.get("success", False) and not trading_engine.PAPER_TRADING:
        err_msg = transfer_res.get("error", "Unknown transfer error")
        print(f"⚠️ [SPOT HARVEST TRANSFER FAILED] User {chat_id}: {err_msg}")
        return {"status": "error", "stage": "TRANSFER", "error": err_msg}
    
    tran_id = transfer_res.get("tranId", "LOCAL_TX")
    time.sleep(0.5) # Brief buffer for Spot wallet balance synchronization
    
    # 4. Execute Spot Market Buy
    spot_buy_res = trading_engine.execute_spot_trade(api_key, api_secret, target_symbol, "BUY", harvest_amount)
    if isinstance(spot_buy_res, dict) and (spot_buy_res.get("status") in ["success", "FILLED"] or spot_buy_res.get("orderId")):
        # Calculate executed qty and price
        exec_price = trading_engine.get_current_price(target_symbol)
        if exec_price <= 0:
            exec_price = 68000.0 if "BTC" in target_symbol else 2700.0
            
        c_fills = spot_buy_res.get("fills", [])
        if c_fills:
            total_qty = sum(float(f.get("qty", 0.0)) for f in c_fills)
            weighted_price = sum(float(f.get("price", 0.0)) * float(f.get("qty", 0.0)) for f in c_fills) / max(0.00001, total_qty)
            qty_bought = total_qty
            exec_price = weighted_price
        else:
            qty_bought = harvest_amount / exec_price
            
        # 5. Persist Wealth Accumulation in Database
        db.record_spot_wealth_harvest(chat_id, target_symbol, harvest_amount, qty_bought, exec_price, str(tran_id))
        
        # Reset unharvested pool and update cumulative stats
        db.update_system_setting(f"spot_harvest_{chat_id}_unharvested_pool", "0.0")
        tot_harvested = cfg.get("total_harvested_usd", 0.0) + harvest_amount
        db.update_system_setting(f"spot_harvest_{chat_id}_total_harvested_usd", str(round(tot_harvested, 2)))
        
        totals = db.get_total_spot_wealth_harvested(chat_id)
        
        print(f"✅ [SPOT WEALTH HARVEST ACCOMPLISHED] User {chat_id}: Successfully accumulated {qty_bought:.6f} {target_symbol} (${harvest_amount:.2f} USDT)!")
        
        # 6. Telegram Rich Notification
        if app and hasattr(app, "bot"):
            try:
                asset_tag = "🪙 Bitcoin" if "BTC" in target_symbol else "🏆 Physical Gold"
                msg_text = (
                    f"🏦 **APEX AUTO SPOT PROFIT HARVEST COMPLETED!** 💎\n"
                    f"{DIVIDER_DOUBLE}\n\n"
                    f"💵 **ប្រាក់ចំណេញ Futures បានផ្ទេរ ៖** `+${harvest_amount:,.2f} USDT`\n"
                    f"🪙 **ទ្រព្យសន្សំ Spot (០% Liquidation) ៖** `+{qty_bought:.6f} {target_symbol.replace('USDT', '')}`\n"
                    f"📈 **តម្លៃទិញជាមធ្យម ៖** `${exec_price:,.2f} USDT`\n"
                    f"🎯 **មូលហេតុបង្វែរទុន ៖** _{rationale}_\n\n"
                    f"📊 **ស្ថានភាពទ្រព្យសម្បត្តិ Spot សរុប (HODL) ៖**\n"
                    f" • 🥇 **សរុប Bitcoin ៖** `{totals.get('btc_qty', 0):.6f} BTC`\n"
                    f" • 🏆 **សរុប Physical Gold ៖** `{totals.get('paxg_qty', 0):.4f} PAXG`\n"
                    f" • 💰 **សរុបតម្លៃដុល្លារ ៖** `${totals.get('total_usd', 0):,.2f} USDT`\n"
                    f" • 🔄 **ចំនួនដង Harvested ៖** `{totals.get('harvest_count', 1)} ដង`\n\n"
                    f"🛡️ _ប្រាក់ចំណេញពី Futures ត្រូវបានចាក់សោរចូលកាបូប Spot ដោយស្វ័យប្រវត្តិតាមយុទ្ធសាស្ត្រ Wealth Preservation ដើម្បីកសាងទ្រព្យសម្បត្តិយូរអង្វែង!_\n\n"
                    f"{OFFICIAL_FOOTNOTE}"
                )
                asyncio.create_task(app.bot.send_message(chat_id=chat_id, text=msg_text, parse_mode="Markdown", read_timeout=5, write_timeout=5, connect_timeout=5))
            except Exception as notify_err:
                print(f"⚠️ [SPOT HARVEST NOTIFY ERROR] {notify_err}")
                
        return {
            "status": "success",
            "symbol": target_symbol,
            "harvest_amount": harvest_amount,
            "qty_bought": qty_bought,
            "price": exec_price,
            "totals": totals
        }
    else:
        err = spot_buy_res.get("error", "Unknown spot buy error") if isinstance(spot_buy_res, dict) else str(spot_buy_res)
        print(f"⚠️ [SPOT BUY FAILED] User {chat_id}: {err}")
        return {"status": "error", "stage": "SPOT_BUY", "error": err}
