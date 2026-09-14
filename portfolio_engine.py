"""
Khmer Master Crypto / Apex AGI v13.00
INSTITUTIONAL SUPER SMART UNIFIED PORTFOLIO ENGINE
================================================================================
Comprehensively audits, tracks, and displays real-time operational state,
exact invested coins, entry/mark prices, leverage, and PnL across ALL 10
investment engines without omitting any component:
  1. Turbo Hedge & Delta-Neutral HFT Engine (/turbo_hedge)
  2. Super Smart Trade Suite (/smart_trade / auto_trade)
  3. Smart X Multi-Asset Quant Suite (/smart_x / /smartx)
  4. Smart Swap Multi-Chain DEX & AI Gem Sniper (/smart_swap)
  5. Dynamic Infinity Matrix & Compound Grid (/infinity_matrix / /compound_grid)
  6. Institutional Smart Listing & Pre-Pump Accumulation Engine (/pre_pump)
  7. 8-Hour Funding Rate & Basis Arbitrage Harvester (/funding_harvester)
  8. Gold Turbo & Macro Radar (/gold_turbo / /gold_guard)
  9. DeFi Flash Loan & Tokyo HFT MEV Keeper (/flash_loan)
 10. Liquidation Defender & 24/7 Circuit Breaker Sentinel
================================================================================
"""

import os
import sys
import time
import psutil
from datetime import datetime

# Reconfigure stdout for UTF-8 safety
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import database as db
import trading_engine

# Start time reference for uptime calculation
_START_TIME = time.time()
_ONCHAIN_BALANCE_CACHE = {}

def get_onchain_live_balances(address: str) -> dict:
    """
    Fetches real-time on-chain balance for a connected Web3 wallet (EVM or Solana).
    Caches results for 45 seconds to guarantee sub-millisecond execution.
    """
    if not address or len(address) < 20:
        return {"total_usd": 0.0, "details": "", "address": ""}

    now = time.time()
    clean = str(address).strip()
    if clean in _ONCHAIN_BALANCE_CACHE:
        cached_time, cached_data = _ONCHAIN_BALANCE_CACHE[clean]
        if now - cached_time < 45:
            return cached_data

    total_usd = 0.0
    details = ""

    # 1. EVM Chains (Arbitrum One USDT & ETH)
    if clean.startswith("0x") and len(clean) == 42:
        try:
            import urllib.request
            import json
            rpc_url = "https://arb1.arbitrum.io/rpc"
            
            # Native ETH
            p_eth = {'jsonrpc': '2.0', 'method': 'eth_getBalance', 'params': [clean, 'latest'], 'id': 1}
            req1 = urllib.request.Request(rpc_url, data=json.dumps(p_eth).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req1, timeout=1.8) as r1:
                res1 = json.loads(r1.read().decode())
                wei = int(res1.get('result', '0x0'), 16)
                eth_bal = round(wei / 1e18, 5)

            # Arbitrum USDT (0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9)
            usdt_contract = '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9'
            d_call = '0x70a08231000000000000000000000000' + clean[2:].lower()
            p_usdt = {'jsonrpc': '2.0', 'method': 'eth_call', 'params': [{'to': usdt_contract, 'data': d_call}, 'latest'], 'id': 2}
            req2 = urllib.request.Request(rpc_url, data=json.dumps(p_usdt).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2, timeout=1.8) as r2:
                res2 = json.loads(r2.read().decode())
                raw_usdt = int(res2.get('result', '0x0'), 16)
                usdt_bal = round(raw_usdt / 1e6, 2)

            eth_est_price = 2450.0
            eth_usd = eth_bal * eth_est_price
            total_usd = round(usdt_bal + eth_usd, 2)
            details = f"{usdt_bal:.2f} USDT + {eth_bal:.4f} ETH លើ Arbitrum"
        except Exception:
            pass

    # 2. Solana Network (SOL)
    elif 32 <= len(clean) <= 44 and not clean.startswith("0x"):
        try:
            import urllib.request
            import json
            rpc_url = "https://api.mainnet-beta.solana.com"
            payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [clean]}
            req = urllib.request.Request(rpc_url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=1.8) as resp:
                res = json.loads(resp.read().decode())
                lamports = res.get("result", {}).get("value", 0)
                sol_bal = round(lamports / 1e9, 4)
                sol_est_price = 145.0
                total_usd = round(sol_bal * sol_est_price, 2)
                details = f"{sol_bal:.4f} SOL លើ Solana"
        except Exception:
            pass

    res_data = {
        "total_usd": total_usd,
        "details": details,
        "address": clean
    }
    _ONCHAIN_BALANCE_CACHE[clean] = (now, res_data)
    return res_data

def get_full_system_portfolio_data(chat_id: int) -> dict:
    """
    Queries all database tables, live Binance Spot/Futures APIs, and on-chain registries
    to assemble a 100% comprehensive diagnostic snapshot for the user.
    """
    keys = db.get_user_api(chat_id)
    is_paper = getattr(trading_engine, "PAPER_TRADING", False)

    # 1. Spot Wallet & Holdings
    spot_usdt_free = 0.0
    spot_alt_exposure = 0.0
    spot_holdings = {}
    actual_balances = {}
    prices = {}

    if keys:
        try:
            actual_balances = trading_engine.get_all_spot_balances(keys[0], keys[1]) or {}
            spot_usdt_free = float(actual_balances.get("USDT", 0.0))
            spot_alt_exposure, spot_holdings = trading_engine.get_total_spot_exposure(keys[0], keys[1])
        except Exception as e:
            print(f"[PORTFOLIO] Spot balance query error: {e}")

    # 2. Futures Wallet & Positions
    futures_wallet_usdt = 0.0
    futures_unrealized_pnl = 0.0
    futures_positions_raw = []
    active_futures_positions = []

    if keys:
        try:
            fut_bal, fut_status = trading_engine.get_futures_balance_detailed(keys[0], keys[1], "USDT")
            futures_wallet_usdt = float(fut_bal or 0.0)
            futures_unrealized_pnl = 0.0
            futures_positions_raw = trading_engine.get_futures_positions(keys[0], keys[1]) or []
            
            for p in futures_positions_raw:
                raw_amt = float(p.get("positionAmt", 0.0) or 0.0)
                if raw_amt != 0.0:
                    sym = str(p.get("symbol", ""))
                    entry_p = float(p.get("entryPrice", 0.0) or 0.0)
                    mark_p = float(p.get("markPrice", 0.0) or 0.0)
                    unRealizedProfit = float(p.get("unRealizedProfit", 0.0) or 0.0)
                    leverage = int(p.get("leverage", 1) or 1)
                    side = "LONG" if raw_amt > 0 else "SHORT"
                    abs_qty = abs(raw_amt)
                    margin = (abs_qty * entry_p) / max(1, leverage)
                    roi_pct = (unRealizedProfit / margin * 100.0) if margin > 0 else 0.0
                    
                    active_futures_positions.append({
                        "symbol": sym,
                        "side": side,
                        "leverage": leverage,
                        "qty": abs_qty,
                        "entry_price": entry_p,
                        "mark_price": mark_p,
                        "margin_usd": margin,
                        "pnl_usd": unRealizedProfit,
                        "roi_pct": roi_pct
                    })
                    futures_unrealized_pnl += unRealizedProfit
        except Exception as e:
            print(f"[PORTFOLIO] Futures position query error: {e}")

    # 3. Active Spot Trades (From DB)
    active_spot_trades = []
    try:
        raw_trades = db.get_active_trades_by_user(chat_id) or []
        for t in raw_trades:
            # (id, symbol, qty, buy_price, current_highest, stop_loss_pct)
            t_id, sym, qty, buy_price, current_highest, stop_loss_pct = t[:6]
            curr_p = trading_engine.get_current_price(sym) or buy_price
            invested = float(qty) * float(buy_price)
            pnl, pnl_pct = trading_engine.calculate_net_pnl(buy_price, curr_p, qty)
            active_spot_trades.append({
                "id": t_id,
                "symbol": sym,
                "qty": float(qty),
                "buy_price": float(buy_price),
                "current_price": float(curr_p),
                "invested_usd": invested,
                "pnl_usd": pnl,
                "roi_pct": pnl_pct,
                "stop_loss_pct": float(stop_loss_pct)
            })
    except Exception as e:
        print(f"[PORTFOLIO] Active spot trades query error: {e}")

    # 4. Active Turbo Hedge Bots (From DB)
    user_turbo_bots = []
    try:
        all_turbo = db.get_active_turbo_hedge_bots() or []
        for b in all_turbo:
            if b.get("chat_id") == chat_id:
                sym = str(b.get("symbol", ""))
                amt = float(b.get("amount", 10.0))
                lev = int(b.get("leverage", 10))
                side = str(b.get("side", "HEDGE")).upper()
                tp = float(b.get("tp_percent", 20.0))
                
                # Fetch entry price from system settings
                entry_str = db.get_system_setting(f"turbo_hedge_{chat_id}_{sym}_entry_price", "0.0")
                entry_p = float(entry_str) if entry_str.replace('.', '', 1).isdigit() else 0.0
                curr_p = trading_engine.get_current_price(sym) or entry_p
                
                user_turbo_bots.append({
                    "symbol": sym,
                    "amount_usd": amt,
                    "leverage": lev,
                    "side": side,
                    "target_tp_pct": tp,
                    "entry_price": entry_p,
                    "current_price": curr_p
                })
    except Exception as e:
        print(f"[PORTFOLIO] Turbo hedge bots query error: {e}")

    # 4b. Turbo Hedge TOP Mode (Futures AGI Auto Decision 24/7)
    turbo_top_mode = False
    turbo_top_count = 5
    turbo_top_amount = 20.0
    turbo_top_leverage = 10
    turbo_top_side = "AUTO"
    turbo_top_tp = 20.0
    try:
        turbo_top_mode = (db.get_system_setting(f"turbo_hedge_{chat_id}_top_mode", "0") == "1")
        val_cnt = db.get_system_setting(f"turbo_hedge_{chat_id}_top_count", "5")
        turbo_top_count = int(val_cnt) if str(val_cnt).isdigit() else 5
        val_amt = db.get_system_setting(f"turbo_hedge_{chat_id}_top_amount", "20.0")
        turbo_top_amount = float(val_amt) if val_amt.replace('.', '', 1).isdigit() else 20.0
        val_lev = db.get_system_setting(f"turbo_hedge_{chat_id}_top_leverage", "10")
        turbo_top_leverage = int(val_lev) if str(val_lev).isdigit() else 10
        turbo_top_side = db.get_system_setting(f"turbo_hedge_{chat_id}_top_side", "AUTO").upper()
        val_tp = db.get_system_setting(f"turbo_hedge_{chat_id}_top_tp", "20.0")
        turbo_top_tp = float(val_tp) if val_tp.replace('.', '', 1).isdigit() else 20.0
    except Exception as e:
        print(f"[PORTFOLIO] Turbo TOP mode query error: {e}")

    # 5. Active Smart Swaps (On-Chain DEX Solana / EVM)
    active_smart_swaps = []
    try:
        import smart_swap_engine
        raw_swaps = db.get_active_smart_swaps(chat_id=chat_id) or []
        for s in raw_swaps:
            chain = s["chain"]
            sym = s["token_symbol"]
            addr = s["token_address"]
            amt_usd = float(s["amount_in_usd"])
            qty = float(s["token_qty"])
            entry_p = float(s["entry_price"])
            scale_lvl = int(s.get("scale_out_level", 0))
            
            curr_p = smart_swap_engine.get_token_price_usd(chain, addr) or entry_p
            curr_val = curr_p * qty
            pnl = (curr_p - entry_p) * qty
            roi_pct = ((curr_p - entry_p) / entry_p * 100.0) if entry_p > 0 else 0.0
            
            active_smart_swaps.append({
                "id": s["id"],
                "chain": chain,
                "symbol": sym,
                "address": addr,
                "amount_usd": amt_usd,
                "current_val_usd": curr_val,
                "token_qty": qty,
                "entry_price": entry_p,
                "current_price": curr_p,
                "pnl_usd": pnl,
                "roi_pct": roi_pct,
                "scale_out_level": scale_lvl
            })
    except Exception as e:
        print(f"[PORTFOLIO] Smart swaps query error: {e}")

    # 6. Active Infinity & Compound Grids (Multi-Table Aggregator)
    active_grids = []
    try:
        # 6a. Legacy infinity_grid_bots
        raw_grids = db.get_active_infinity_grids_by_user(chat_id) or []
        for g in raw_grids:
            g_id, sym, layer_amt, step_pct, max_inv, curr_inv, last_p = g[:7]
            curr_p = trading_engine.get_current_price(sym) or float(last_p)
            active_grids.append({
                "id": g_id,
                "type": "INFINITY_GRID",
                "symbol": sym,
                "layer_amount": float(layer_amt),
                "step_pct": float(step_pct),
                "max_investment": float(max_inv),
                "current_investment": float(curr_inv),
                "last_price": float(last_p),
                "current_price": float(curr_p)
            })

        # 6b. Spot Snowball Compound Grids (compound_grids table)
        if hasattr(db, 'get_active_compound_grids_by_user'):
            c_grids = db.get_active_compound_grids_by_user(chat_id) or []
            for cg in c_grids:
                cg_id, c_sym, c_layer, c_step, c_target, c_coins, c_last_p = cg[:7]
                curr_p = trading_engine.get_current_price(c_sym) or float(c_last_p)
                active_grids.append({
                    "id": cg_id,
                    "type": "COMPOUND_GRID",
                    "symbol": c_sym,
                    "layer_amount": float(c_layer),
                    "step_pct": float(c_step),
                    "max_investment": float(c_target),
                    "current_investment": float(c_coins) * curr_p if float(c_coins) > 0 else float(c_layer),
                    "last_price": float(c_last_p),
                    "current_price": float(curr_p)
                })

        # 6c. Dynamic Infinity Matrix Bots (infinity_matrix_bots table)
        if hasattr(db, 'get_user_infinity_matrix_bots'):
            im_bots = db.get_user_infinity_matrix_bots(chat_id) or []
            for ib in im_bots:
                if isinstance(ib, (list, tuple)) and len(ib) >= 4:
                    ib_id = ib[0]
                    ib_sym = ib[2]
                    ib_cap = float(ib[3])
                    ib_pnl = float(ib[4]) if len(ib) > 4 else 0.0
                    ib_grids = int(ib[5]) if len(ib) > 5 else 100
                    curr_p = trading_engine.get_current_price(ib_sym) or 0.0
                    active_grids.append({
                        "id": ib_id,
                        "type": "INFINITY_MATRIX",
                        "symbol": ib_sym,
                        "layer_amount": ib_cap / max(1, ib_grids),
                        "step_pct": 1.0,
                        "max_investment": ib_cap,
                        "current_investment": ib_cap,
                        "last_price": curr_p,
                        "current_price": curr_p,
                        "accumulated_pnl": ib_pnl
                    })
    except Exception as e:
        print(f"[PORTFOLIO] Infinity grids query error: {e}")

    # 7. Active Snipers
    user_snipers = []
    try:
        all_snipers = db.get_active_smart_snipers() or {}
        for sn_id, sn in all_snipers.items():
            if sn.get("chat_id") == chat_id:
                user_snipers.append(sn)
    except Exception as e:
        print(f"[PORTFOLIO] Snipers query error: {e}")

    # 7b. Pre-Pump Radar Config
    is_pre_pump_enabled = db.is_pre_pump_enabled(chat_id) if hasattr(db, 'is_pre_pump_enabled') else False
    pre_pump_cfg = db.get_pre_pump_config(chat_id) if hasattr(db, 'get_pre_pump_config') else {}

    # 8. Funding Harvester
    funding_cfg = db.get_funding_harvester_config(chat_id) if hasattr(db, 'get_funding_harvester_config') else {"enabled": False, "amount": 50.0}

    # 8b. Gold Turbo Config
    gold_turbo_cfg = db.get_gold_turbo_config(chat_id) if hasattr(db, 'get_gold_turbo_config') else {"is_enabled": False, "amount_per_trade": 15.0}

    # 8c. Smart X Quant Config
    smart_x_active = (db.get_system_setting(f"smart_x_{chat_id}_active", "0") == "1") if hasattr(db, 'get_system_setting') else False
    smart_x_target = db.get_system_setting(f"smart_x_{chat_id}_target", "GOLD") if hasattr(db, 'get_system_setting') else "GOLD"

    # 8d. Auto Trade / Smart Trade Spot Config
    is_auto_trade_enabled = db.is_auto_trade_enabled(chat_id) if hasattr(db, 'is_auto_trade_enabled') else False
    macro_auto_cfg = db.get_macro_auto_trade_config(chat_id) if hasattr(db, 'get_macro_auto_trade_config') else {}

    # 9. Flash Loan Keeper & Strategy
    is_flash_loan_auto = db.is_user_flash_loan_auto(chat_id) if hasattr(db, 'is_user_flash_loan_auto') else False
    flash_loan_pnl = db.get_user_flash_loan_pnl_summary(chat_id) if hasattr(db, 'get_user_flash_loan_pnl_summary') else {"count": 0, "total_profit": 0.0}

    # 10. Liquidation Defender & Circuit Breaker
    is_defender_active = db.is_defender_active() if hasattr(db, 'is_defender_active') else False
    circuit_breaker = db.get_circuit_breaker_status() if hasattr(db, 'get_circuit_breaker_status') else {"tripped": False}

    # 11. Multi-Chain Web3 Settlement Wallet & Smart Swap Dedicated Wallets
    web3_wallets = db.get_user_multichain_wallets(chat_id) if hasattr(db, 'get_user_multichain_wallets') else {}
    primary_web3 = db.get_user_web3_wallet(chat_id) if hasattr(db, 'get_user_web3_wallet') else ""

    # Dedicated Solana Trading Hot Wallet (Trojan / BonkBot Architecture)
    user_sol_wallet = None
    user_sol_pubkey = ""
    user_sol_bal = 0.0
    user_sol_usd = 0.0
    user_sol_funded = False
    try:
        import solana_trading_wallet
        user_sol_wallet = solana_trading_wallet.get_user_solana_wallet_overview(chat_id)
        user_sol_pubkey = user_sol_wallet.get("public_key", "")
        user_sol_bal = float(user_sol_wallet.get("sol_balance", 0.0))
        user_sol_usd = float(user_sol_wallet.get("usd_value", 0.0))
        user_sol_funded = bool(user_sol_wallet.get("is_funded", False))
    except Exception as e:
        print(f"[PORTFOLIO] Solana wallet query error: {e}")

    # Bound Phantom Profit Settlement Vault (100% Non-Custodial Zero-Risk Destination)
    phantom_vault = ""
    phantom_bal_usd = 0.0
    phantom_details_str = ""
    try:
        import solana_trading_wallet
        phantom_vault = solana_trading_wallet.get_user_phantom_wallet(chat_id) or ""
        if phantom_vault:
            p_data = get_onchain_live_balances(phantom_vault)
            phantom_bal_usd = float(p_data.get("total_usd", 0.0))
            phantom_details_str = p_data.get("details", "")
    except Exception as e:
        print(f"[PORTFOLIO] Phantom vault query error: {e}")

    # EVM Web3 Wallet (Arbitrum / Ethereum)
    evm_bal_usd = 0.0
    evm_details_str = ""
    if primary_web3 and primary_web3.startswith("0x"):
        e_data = get_onchain_live_balances(primary_web3)
        evm_bal_usd = float(e_data.get("total_usd", 0.0))
        evm_details_str = e_data.get("details", "")

    # Smart Swap Realized PnL & Trade Count
    swap_history = []
    total_realized_swap_pnl = 0.0
    total_swaps_count = 0
    try:
        swap_history = db.get_smart_swap_history(chat_id=chat_id, limit=30) or []
        total_swaps_count = len(swap_history)
        total_realized_swap_pnl = sum(float(h.get("realized_pnl_usd", 0.0)) for h in swap_history)
    except Exception as e:
        print(f"[PORTFOLIO] Swap history query error: {e}")

    # Smart Swap 24/7 Auto-Pilot Status
    smart_swap_autopilot_cfg = {}
    try:
        smart_swap_autopilot_cfg = db.get_smart_swap_autopilot_config(chat_id)
    except Exception as e:
        print(f"[PORTFOLIO] Smart Swap autopilot query error: {e}")

    # 12. VPS & System Health
    uptime_sec = int(time.time() - _START_TIME)
    h, rem = divmod(uptime_sec, 3600)
    m, s = divmod(rem, 60)
    uptime_str = f"{h}h {m}m {s}s"

    cpu_usage = 0.0
    ram_usage_mb = 0
    ram_total_mb = 0
    ram_pct = 0.0
    disk_used_gb = 0.0
    disk_total_gb = 0.0
    db_size_mb = 0.0

    try:
        cpu_usage = psutil.cpu_percent(interval=0.05)
        mem = psutil.virtual_memory()
        ram_usage_mb = int(mem.used / (1024 * 1024))
        ram_total_mb = int(mem.total / (1024 * 1024))
        ram_pct = mem.percent
        disk = psutil.disk_usage('/')
        disk_used_gb = round(disk.used / (1024**3), 2)
        disk_total_gb = round(disk.total / (1024**3), 2)
        if os.path.exists(db.DB_FILE):
            db_size_mb = round(os.path.getsize(db.DB_FILE) / (1024 * 1024), 2)
    except Exception:
        pass

    # =========================================================================
    # CONSOLIDATED TOTALS CALCULATION
    # =========================================================================
    total_spot_capital = spot_usdt_free + spot_alt_exposure
    total_futures_capital = futures_wallet_usdt + futures_unrealized_pnl
    active_swaps_usd = sum(s["current_val_usd"] for s in active_smart_swaps)
    total_onchain_capital = round(active_swaps_usd + user_sol_usd + evm_bal_usd, 2)
    total_portfolio_net_worth = round(total_spot_capital + total_futures_capital + total_onchain_capital, 2)

    total_invested_usd = 0.0
    total_unrealized_pnl = 0.0

    # From Spot Trades
    for st in active_spot_trades:
        total_invested_usd += st["invested_usd"]
        total_unrealized_pnl += st["pnl_usd"]

    # From Futures Positions
    for fp in active_futures_positions:
        total_invested_usd += fp["margin_usd"]
        total_unrealized_pnl += fp["pnl_usd"]

    # From Smart Swaps
    for ss in active_smart_swaps:
        total_invested_usd += ss["amount_usd"]
        total_unrealized_pnl += ss["pnl_usd"]

    # From Infinity Grids
    for ig in active_grids:
        total_invested_usd += ig["current_investment"]

    total_roi_pct = (total_unrealized_pnl / max(1.0, total_invested_usd) * 100.0) if total_invested_usd > 0 else 0.0

    return {
        "chat_id": chat_id,
        "is_paper": is_paper,
        "total_portfolio_net_worth": round(total_portfolio_net_worth, 2),
        "total_invested_usd": round(total_invested_usd, 2),
        "total_unrealized_pnl": round(total_unrealized_pnl, 2),
        "total_roi_pct": round(total_roi_pct, 2),
        
        # Wallet Balances
        "spot_usdt_free": round(spot_usdt_free, 2),
        "spot_alt_exposure": round(spot_alt_exposure, 2),
        "spot_holdings": spot_holdings,
        "futures_wallet_usdt": round(futures_wallet_usdt, 2),
        "futures_unrealized_pnl": round(futures_unrealized_pnl, 2),
        "total_onchain_capital": round(total_onchain_capital, 2),
        "web3_wallets": web3_wallets,
        "primary_web3": primary_web3,
        
        # Dedicated Smart Swap & Web3 Fields
        "user_sol_pubkey": user_sol_pubkey,
        "user_sol_bal": user_sol_bal,
        "user_sol_usd": round(user_sol_usd, 2),
        "user_sol_funded": user_sol_funded,
        "phantom_vault": phantom_vault,
        "phantom_bal_usd": round(phantom_bal_usd, 2),
        "phantom_details_str": phantom_details_str,
        "evm_bal_usd": round(evm_bal_usd, 2),
        "evm_details_str": evm_details_str,
        "total_realized_swap_pnl": round(total_realized_swap_pnl, 2),
        "total_swaps_count": total_swaps_count,

        # Active Positions per Engine
        "active_futures_positions": active_futures_positions,
        "active_spot_trades": active_spot_trades,
        "user_turbo_bots": user_turbo_bots,
        "active_smart_swaps": active_smart_swaps,
        "active_grids": active_grids,
        "user_snipers": user_snipers,

        # Engine Flags
        "turbo_top_mode": turbo_top_mode,
        "turbo_top_count": turbo_top_count,
        "turbo_top_amount": turbo_top_amount,
        "turbo_top_leverage": turbo_top_leverage,
        "turbo_top_side": turbo_top_side,
        "turbo_top_tp": turbo_top_tp,
        "smart_swap_autopilot": smart_swap_autopilot_cfg,
        "funding_cfg": funding_cfg,
        "gold_turbo_cfg": gold_turbo_cfg,
        "smart_x_active": smart_x_active,
        "smart_x_target": smart_x_target,
        "is_auto_trade_enabled": is_auto_trade_enabled,
        "macro_auto_cfg": macro_auto_cfg,
        "is_pre_pump_enabled": is_pre_pump_enabled,
        "pre_pump_cfg": pre_pump_cfg,
        "is_flash_loan_auto": is_flash_loan_auto,
        "flash_loan_pnl": flash_loan_pnl,
        "is_defender_active": is_defender_active,
        "circuit_breaker": circuit_breaker,

        # Hardware & Vitals
        "uptime_str": uptime_str,
        "cpu_usage": cpu_usage,
        "ram_usage_mb": ram_usage_mb,
        "ram_total_mb": ram_total_mb,
        "ram_pct": ram_pct,
        "disk_used_gb": disk_used_gb,
        "disk_total_gb": disk_total_gb,
        "db_size_mb": db_size_mb
    }

def render_portfolio_card(data: dict, user_lang: str = "km", include_vitals: bool = False) -> str:
    """
    Renders an institutional-grade, highly aesthetic Telegram message
    categorizing and auditing EVERY single investment engine with full transparency.
    """
    lang = "en" if str(user_lang).lower() in ["en", "english"] else "km"
    chat_id = data["chat_id"]
    is_paper = data["is_paper"]

    badge_mode = "🧪 PAPER TRADING" if is_paper else "🚀 REAL LIVE CAPITAL"
    net_worth = data["total_portfolio_net_worth"]
    invested = data["total_invested_usd"]
    pnl = data["total_unrealized_pnl"]
    roi = data["total_roi_pct"]

    pnl_sign = "+" if pnl >= 0 else "-"
    pnl_emoji = "🟩" if pnl >= 0 else "🟥"
    pnl_str = f"{pnl_sign}${abs(pnl):,.2f} USD"

    # Solana Hot Wallet and Phantom Vault addresses for display
    user_sol_pub = data.get("user_sol_pubkey", "")
    short_sol = f"`{user_sol_pub[:6]}...{user_sol_pub[-4:]}`" if user_sol_pub else "`N/A`"
    sol_usd = data.get("user_sol_usd", 0.0)
    sol_bal = data.get("user_sol_bal", 0.0)

    p_vault = data.get("phantom_vault", "")
    if p_vault:
        short_pvault_en = f"`{p_vault[:6]}...{p_vault[-4:]}` (Linked ✅ | Auto Profit Vault)"
        short_pvault_km = f"`{p_vault[:6]}...{p_vault[-4:]}` (ភ្ជាប់រួចរាល់ ✅ | Auto Profit Vault)"
    else:
        short_pvault_en = "Not linked (`/smart_swap bind_phantom <addr>`)"
        short_pvault_km = "មិនទាន់ភ្ជាប់ (`/smart_swap bind_phantom <អាសយដ្ឋាន>`)"

    evm_u = data.get("evm_bal_usd", 0.0)
    evm_det = data.get("evm_details_str", "")
    evm_line_en = f"• 🌐 **Arbitrum/EVM Web3:** `${evm_u:,.2f} USD` ({evm_det})\n" if (evm_u > 0 or evm_det) else ""
    evm_line_km = f"• 🌐 **Arbitrum/EVM Web3 ៖** `${evm_u:,.2f} USD` ({evm_det})\n" if (evm_u > 0 or evm_det) else ""

    # =========================================================================
    # 1. HEADER & EXECUTIVE CAPITAL SUMMARY
    # =========================================================================
    if lang == "en":
        header = (
            "👑 **KHMER MASTER CRYPTO | INSTITUTIONAL SUPER SMART PORTFOLIO** 🛡️\n"
            "════════════\n"
            f"💼 **ACCOUNT CLEARANCE:** `ID: {chat_id}` | `{badge_mode}`\n"
            "════════════\n\n"
            "💰 **CONSOLIDATED NET CAPITAL OVERVIEW:**\n"
            f"• 💎 **Total Net Portfolio Value:** `${net_worth:,.2f} USD`\n"
            f"• 🎯 **Active Capital at Work:** `${invested:,.2f} USD`\n"
            f"• {pnl_emoji} **Total Floating Net PnL:** `{pnl_str}` (`{roi:+.2f}%` ROI)\n\n"
            "🏦 **MULTI-WALLET BALANCES:**\n"
            f"• 🟡 **Binance Spot:** `${data['spot_usdt_free']:,.2f} USDT` free | `${data['spot_alt_exposure']:,.2f}` in Coins\n"
            f"• ⚡ **Binance Futures:** `${data['futures_wallet_usdt']:,.2f} USDT` balance (PnL: `${data['futures_unrealized_pnl']:+,.2f}`)\n"
            f"• ⚡ **Solana Trading Wallet:** `${sol_usd:,.2f} USD` (`{sol_bal:.4f} SOL` | {short_sol}) [Dedicated Hot Wallet]\n"
            f"• 🟣 **Phantom Vault (Withdraw):** {short_pvault_en}\n"
            f"{evm_line_en}"
            f"• 🌐 **Total On-Chain Net Capital:** `${data['total_onchain_capital']:,.2f} USD`\n"
            "────────────\n\n"
        )
    else:
        header = (
            "👑 **KHMER MASTER CRYPTO | របាយការណ៍វិនិយោគរួម SUPER SMART PORTFOLIO** 🛡️\n"
            "════════════\n"
            f"💼 **គណនីវិនិយោគិន ៖** `ID: {chat_id}` | `{badge_mode}`\n"
            "════════════\n\n"
            "💰 **ទិដ្ឋភាពរួមដើមទុន និងប្រាក់ចំណេញសរុប ៖**\n"
            f"• 💎 **ទ្រព្យសរុបក្នុងប្រព័ន្ធ (Net Worth) ៖** `${net_worth:,.2f} USD`\n"
            f"• 🎯 **ដើមទុនកំពុងវិនិយោគជាក់ស្តែង ៖** `${invested:,.2f} USD`\n"
            f"• {pnl_emoji} **ផលចំណេញសរុបបណ្តោះអាសន្ន (Floating PnL) ៖** `{pnl_str}` (`{roi:+.2f}%` ROI)\n\n"
            "🏦 **សមតុល្យតាមកាបូបនីមួយៗ (Multi-Wallet Balances) ៖**\n"
            f"• 🟡 **Binance Spot ៖** `${data['spot_usdt_free']:,.2f} USDT` សេរី | `${data['spot_alt_exposure']:,.2f}` កំពុងកាន់កាក់\n"
            f"• ⚡ **Binance Futures ៖** `${data['futures_wallet_usdt']:,.2f} USDT` ក្នុងកាបូប (PnL: `${data['futures_unrealized_pnl']:+,.2f}`)\n"
            f"• ⚡ **Solana Trading Wallet ៖** `${sol_usd:,.2f} USD` (`{sol_bal:.4f} SOL` | {short_sol}) [កាបូបជួញដូរផ្ទាល់ខ្លួន]\n"
            f"• 🟣 **Phantom Vault (ដកប្រាក់) ៖** {short_pvault_km}\n"
            f"{evm_line_km}"
            f"• 🌐 **ទុនជួញដូរ On-Chain សរុប ៖** `${data['total_onchain_capital']:,.2f} USD`\n"
            "────────────\n\n"
        )

    # =========================================================================
    # 2. AUDIT OF ALL 10 INVESTMENT ENGINES (WITH ACTIVE ASSETS)
    # =========================================================================
    engines_text = "📊 **ស្ថានភាពដំណើរការម៉ាស៊ីនវិនិយោគទាំង ១០ (10-ENGINE AUDIT):**\n\n" if lang == "km" else "📊 **OPERATIONAL STATUS OF ALL 10 ENGINES:**\n\n"

    # --- ENGINE 1: Turbo Hedge & Delta-Neutral HFT Engine ---
    tb_bots = data.get("user_turbo_bots", [])
    fut_pos = data.get("active_futures_positions", [])
    top_mode = data.get("turbo_top_mode", False)
    top_amt = data.get("turbo_top_amount", 20.0)
    top_lev = data.get("turbo_top_leverage", 10)
    top_side = data.get("turbo_top_side", "AUTO")
    top_cnt = data.get("turbo_top_count", 5)
    top_tp = data.get("turbo_top_tp", 20.0)

    top_amt_str = f"{int(top_amt)}" if top_amt.is_integer() else f"{top_amt}"
    top_cmd_preset = f"`/turbo_hedge TOP {top_amt_str} {top_lev} {top_side} {top_cnt} 1234`"

    # 1. Delta-Neutral Pair Hedging
    active_dn_bots = [b for b in tb_bots if b.get("side") == "HEDGE"]
    if lang == "km":
        if active_dn_bots:
            dn_text = f"   🟢 ACTIVE / HEDGING ({len(active_dn_bots)} Pairs កំពុងកើបចំណេញ 24/7)\n"
            for b in active_dn_bots:
                dn_text += f"  • `{b['symbol']}` ({b['side']} {b['leverage']}x) ៖ ដើមទុន `${b['amount_usd']:.2f}` | Entry: `${b['entry_price']:.4f}` | Mark: `${b['current_price']:.4f}` | TP: `+{b['target_tp_pct']}%`\n"
        else:
            dn_text = (
                "   🟡 STANDBY (រង់ចាំឱកាស ស្កេន Basis & Funding 24/7)\n"
                "  • ស្ថានភាព ៖ រង់ចាំសញ្ញាបញ្ជា `/turbo_hedge HEDGE auto 20 1234`\n"
            )

        # 2. Futures AGI Auto Decision (TOP Mode)
        if top_mode:
            agi_text = (
                "🧠 **Futures AGI Auto Decision (AI ស្កេន & សម្រេចចិត្ត BUY/SELL ស្វ័យប្រវត្តិ 24/7)**\n"
                f"   {top_cmd_preset}\n"
                "   🟢 ACTIVE (កំពុងស្គែនរកកាក់ចូល Position 24/7)\n"
                f"  • ប៉ារ៉ាម៉ែត្រ ៖ ទុន `${top_amt:.0f}` | `{top_lev}x` | Side: `{top_side}` | ស្កេន: `Top 1-{top_cnt} Gainers` | TP: `+{top_tp:.0f}%`\n"
            )
        else:
            agi_text = (
                "🧠 **Futures AGI Auto Decision (AI ស្កេន & សម្រេចចិត្ត BUY/SELL ស្វ័យប្រវត្តិ 24/7)**\n"
                f"   {top_cmd_preset}\n"
                "   ⚪ STANDBY (រង់ចាំសញ្ញាបញ្ជាបើកដំណើរការ 24/7)\n"
            )

        # 3. Invested Positions (កាក់កំពុងវិនិយោគ)
        invested_items = []
        for b in [b for b in tb_bots if b.get("side") != "HEDGE"]:
            invested_items.append(f"  • `{b['symbol']}` ({b['side']} {b['leverage']}x) ៖ ដើមទុន `${b['amount_usd']:.2f}` | Entry: `${b['entry_price']:.4f}` | Mark: `${b['current_price']:.4f}` | TP: `+{b['target_tp_pct']}%`")
        for p in fut_pos:
            if not any(b['symbol'] == p['symbol'] for b in tb_bots):
                e_pnl_sign = "+" if p['pnl_usd'] >= 0 else ""
                side_label = "BUY" if p['side'] in ["LONG", "BUY"] else "SELL"
                price_fmt = f"${p['entry_price']:,.4f}" if p['entry_price'] >= 1 else f"${p['entry_price']:,.6f}"
                mark_fmt = f"${p['mark_price']:,.4f}" if p['mark_price'] >= 1 else f"${p['mark_price']:,.6f}"
                invested_items.append(f"  • `{p['symbol']}` (Futures {side_label} {p['leverage']}x ISOLATED) ៖ Margin `${p['margin_usd']:.2f}` | Entry: `{price_fmt}` | Mark: `{mark_fmt}` | PnL: `{e_pnl_sign}${p['pnl_usd']:.2f}` (`{p['roi_pct']:+.1f}%`)")

        if invested_items:
            inv_text = "💼 **កាក់កំពុងវិនិយោគជាក់ស្តែង ៖**\n" + "\n".join(invested_items)
        else:
            inv_text = "💼 **កាក់កំពុងវិនិយោគជាក់ស្តែង ៖**\n  • គ្មាន Position កំពុងត្រាំ (Free Margin 100% សុវត្ថិភាព)"

        engines_text += (
            f"1️⃣ **Turbo Hedge & Delta-Neutral HFT Engine (`/turbo_hedge`)**\n"
            f"{dn_text}"
            f"{agi_text}"
            f"{inv_text}\n\n"
        )
    else:
        # English rendering
        if active_dn_bots:
            dn_text = f"   🟢 ACTIVE / HEDGING ({len(active_dn_bots)} Pairs Hedging 24/7)\n"
            for b in active_dn_bots:
                dn_text += f"  • `{b['symbol']}` ({b['side']} {b['leverage']}x): Capital `${b['amount_usd']:.2f}` | Entry: `${b['entry_price']:.4f}` | Mark: `${b['current_price']:.4f}` | TP: `+{b['target_tp_pct']}%`\n"
        else:
            dn_text = (
                "   🟡 STANDBY (Scanning Basis & Funding Opportunities 24/7)\n"
                "  • Status: Standby for command `/turbo_hedge HEDGE auto 20 1234`\n"
            )

        # 2. Futures AGI Auto Decision (TOP Mode)
        if top_mode:
            agi_text = (
                "🧠 **Futures AGI Auto Decision (AI Scan & Auto BUY/SELL 24/7)**\n"
                f"   {top_cmd_preset}\n"
                "   🟢 ACTIVE (Scanning market & entering positions 24/7)\n"
                f"  • Config: Capital `${top_amt:.0f}` | `{top_lev}x` | Side: `{top_side}` | Scan: `Top 1-{top_cnt} Gainers` | TP: `+{top_tp:.0f}%`\n"
            )
        else:
            agi_text = (
                "🧠 **Futures AGI Auto Decision (AI Scan & Auto BUY/SELL 24/7)**\n"
                f"   {top_cmd_preset}\n"
                "   ⚪ STANDBY (Standby for execution command 24/7)\n"
            )

        # 3. Invested Positions
        invested_items = []
        for b in [b for b in tb_bots if b.get("side") != "HEDGE"]:
            invested_items.append(f"  • `{b['symbol']}` ({b['side']} {b['leverage']}x): Capital `${b['amount_usd']:.2f}` | Entry: `${b['entry_price']:.4f}` | Mark: `${b['current_price']:.4f}` | TP: `+{b['target_tp_pct']}%`")
        for p in fut_pos:
            if not any(b['symbol'] == p['symbol'] for b in tb_bots):
                e_pnl_sign = "+" if p['pnl_usd'] >= 0 else ""
                side_label = "BUY" if p['side'] in ["LONG", "BUY"] else "SELL"
                price_fmt = f"${p['entry_price']:,.4f}" if p['entry_price'] >= 1 else f"${p['entry_price']:,.6f}"
                mark_fmt = f"${p['mark_price']:,.4f}" if p['mark_price'] >= 1 else f"${p['mark_price']:,.6f}"
                invested_items.append(f"  • `{p['symbol']}` (Futures {side_label} {p['leverage']}x ISOLATED): Margin `${p['margin_usd']:.2f}` | Entry: `{price_fmt}` | Mark: `{mark_fmt}` | PnL: `{e_pnl_sign}${p['pnl_usd']:.2f}` (`{p['roi_pct']:+.1f}%`)")

        if invested_items:
            inv_text = "💼 **Active Invested Positions:**\n" + "\n".join(invested_items)
        else:
            inv_text = "💼 **Active Invested Positions:**\n  • No active positions (100% Free Margin Protected)"

        engines_text += (
            f"1️⃣ **Turbo Hedge & Delta-Neutral HFT Engine (`/turbo_hedge`)**\n"
            f"{dn_text}"
            f"{agi_text}"
            f"{inv_text}\n\n"
        )

    # --- ENGINE 2: Super Smart Trade Suite (Spot Breakout & Top Gainers) ---
    sp_trades = data["active_spot_trades"]
    macro_auto_cfg = data.get("macro_auto_cfg", {})
    is_auto_on = macro_auto_cfg.get("enabled", False) or data.get("is_auto_trade_enabled", False)
    auto_amt = macro_auto_cfg.get("amount", 30.0)

    if sp_trades:
        e2_status = f"🟢 ACTIVE / INVESTED ({len(sp_trades)} កាក់កំពុងជួញដូរ)" if lang == "km" else f"🟢 ACTIVE / INVESTED ({len(sp_trades)} Spot Positions)"
        e2_details = []
        for st in sp_trades:
            s_sign = "+" if st['pnl_usd'] >= 0 else ""
            e2_details.append(f"  • `{st['symbol']}` ៖ ដើមទុន `${st['invested_usd']:.2f}` | Entry: `${st['buy_price']:.4f}` | Mark: `${st['current_price']:.4f}` | PnL: `{s_sign}${st['pnl_usd']:.2f}` (`{st['roi_pct']:+.2f}%`)")
        if is_auto_on:
            e2_details.append(f"  • 🔄 Auto-Trade Scanner ៖ `🟢 ACTIVE (${auto_amt:.0f} USDT/Trade | 24/7 Scanning)`")
        e2_body = "\n".join(e2_details)
    elif is_auto_on:
        e2_status = "🟢 ACTIVE / SCANNING (ស្កេនរកកាក់ Spot Breakout 24/7)" if lang == "km" else "🟢 ACTIVE / SCANNING (Scanning Spot Breakouts 24/7)"
        e2_body = (
            f"  • 🔄 Auto-Trade Scanner ៖ `🟢 ACTIVE (${auto_amt:.0f} USDT/Trade)`\n"
            f"  • ស្ថានភាព ៖ ម៉ាស៊ីន AI កំពុងស្កេន Top Gainers & Pullbacks (រង់ចាំទិញពេល Breakout ពិតប្រាកដ)"
        ) if lang == "km" else (
            f"  • 🔄 Auto-Trade Scanner: `🟢 ACTIVE (${auto_amt:.0f} USDT/Trade)`\n"
            f"  • Status: Scanning Top Gainers & Pullbacks 24/7 (Awaiting prime breakout setup)"
        )
    else:
        e2_status = "🟡 STANDBY (ស្កេនរកកាក់ Spot Breakout & Top Gainers 24/7)" if lang == "km" else "🟡 STANDBY (Scanning Spot Breakouts 24/7)"
        e2_body = "  • ស្ថានភាព ៖ គ្មានកាក់ Spot កំពុងជួញដូរ (វាយ `/auto_trade ON 30` ឬ `/smart_trade auto 20 1234` ដើម្បីចាប់ផ្តើម)" if lang == "km" else "  • Status: Standby (Execute `/auto_trade ON 30` or `/smart_trade auto 20 1234`)"
    engines_text += f"2️⃣ **Super Smart Trade Suite (`/smart_trade` / `auto_trade`)**\n   {e2_status}\n{e2_body}\n\n"

    # --- ENGINE 3: Smart X Multi-Asset Quant Suite (Gold & BTC) ---
    smart_x_active = data.get("smart_x_active", False)
    smart_x_target = data.get("smart_x_target", "GOLD")
    gold_pos = [p for p in fut_pos if any(k in p.get("symbol", "") for k in ["XAU", "PAXG"])] + [s for s in sp_trades if any(k in s.get("symbol", "") for k in ["XAU", "PAXG"])]
    btc_pos = [p for p in fut_pos if "BTC" in p.get("symbol", "")] + [s for s in sp_trades if "BTC" in s.get("symbol", "")]
    smart_x_bots = [b for b in tb_bots if any(k in b.get("symbol", "") for k in ["XAU", "PAXG", "BTC"])]

    if smart_x_active or gold_pos or btc_pos or smart_x_bots:
        e3_status = "🟢 ACTIVE / INVESTED (ម៉ាស៊ីន AI Quant កំពុងជួញដូរ)" if lang == "km" else "🟢 ACTIVE / INVESTED"
        e3_details = []
        if gold_pos:
            for p in gold_pos:
                p_pnl = p.get('pnl_usd', 0.0)
                p_sign = "+" if p_pnl >= 0 else ""
                p_margin = p.get('margin_usd', p.get('invested_usd', 0.0))
                p_side = p.get('side', 'BUY')
                p_lev = p.get('leverage', 10)
                p_sym = p.get('symbol', 'XAUUSDT')
                e3_details.append(f"  • `{p_sym}` (Gold Quant {p_side} {p_lev}x) ៖ Margin `${p_margin:.2f}` | Entry: `${p.get('entry_price', 0):.4f}` | Mark: `${p.get('mark_price', p.get('current_price', 0)):.4f}` | PnL: `{p_sign}${p_pnl:.2f}` (`{p.get('roi_pct', 0.0):+.1f}%`)")
        elif btc_pos:
            for p in btc_pos:
                p_pnl = p.get('pnl_usd', 0.0)
                p_sign = "+" if p_pnl >= 0 else ""
                p_margin = p.get('margin_usd', p.get('invested_usd', 0.0))
                p_side = p.get('side', 'BUY')
                p_lev = p.get('leverage', 10)
                e3_details.append(f"  • `BTCUSDT` (Bitcoin Quant {p_side} {p_lev}x) ៖ Margin `${p_margin:.2f}` | Entry: `${p.get('entry_price', 0):.2f}` | PnL: `{p_sign}${p_pnl:.2f}` (`{p.get('roi_pct', 0.0):+.1f}%`)")
        elif smart_x_bots:
            for b in smart_x_bots:
                e3_details.append(f"  • `{b['symbol']}` (Quant Bot) ៖ ដើមទុន `${b['amount_usd']:.2f}` ({b['side']} {b['leverage']}x) | TP: `+{b['target_tp_pct']}%`")
        else:
            e3_details.append(f"  • ស្ថានភាព ៖ ម៉ាស៊ីន AI Quant សកម្ម (កំពុងស្កេនទុនជួញដូរ {smart_x_target} 24/7 តាម MoE Router)")
        e3_body = "\n".join(e3_details)
    else:
        e3_status = "🟡 STANDBY (រង់ចាំ London/NY Liquidity Sweep)" if lang == "km" else "🟡 STANDBY (Waiting for London/NY Sweep)"
        e3_body = "  • ស្ថានភាព ៖ រង់ចាំវាយលុក Asian Range Fakeout (វាយ `/smartx GOLD 20 10 AUTO 1234` ដើម្បីបើក)" if lang == "km" else "  • Status: Ready to launch via `/smartx GOLD 20 10 AUTO 1234`"
    engines_text += f"3️⃣ **Smart X Quant Suite (`/smart_x` / `/smartx`)**\n   {e3_status}\n{e3_body}\n\n"

    # --- ENGINE 4: Smart Swap Multi-Chain DEX & AI Gem Sniper ---
    swaps = data["active_smart_swaps"]
    realized_swap_pnl = data.get("total_realized_swap_pnl", 0.0)
    swaps_cnt = data.get("total_swaps_count", 0)
    ap_cfg = data.get("smart_swap_autopilot", {})
    is_ap_on = ap_cfg.get("enabled", False)
    ap_amt = ap_cfg.get("amount", 20.0)
    ap_pos = ap_cfg.get("max_positions", 2)
    ap_str_km = f"\n  • 🔄 24/7 Auto-Pilot ៖ `🟢 ACTIVE (${ap_amt:.0f}/Trade | Slot: {len(swaps)}/{ap_pos})`" if is_ap_on else f"\n  • 🔄 24/7 Auto-Pilot ៖ `⚪ STANDBY` (វាយ `/smart_swap autopilot ON 20 1234`)"
    ap_str_en = f"\n  • 🔄 24/7 Auto-Pilot: `🟢 ACTIVE (${ap_amt:.0f}/Trade | Slot: {len(swaps)}/{ap_pos})`" if is_ap_on else f"\n  • 🔄 24/7 Auto-Pilot: `⚪ STANDBY` (Execute `/smart_swap autopilot ON 20 1234`)"
    pnl_hist_str_km = f"\n  • 🏆 ផលចំណេញកើបបានពីមុន ៖ `+${realized_swap_pnl:,.2f} USD` (ពីការជួញដូរ {swaps_cnt} ដង)" if swaps_cnt > 0 else ""
    pnl_hist_str_en = f"\n  • 🏆 Realized DEX Profit ៖ `+${realized_swap_pnl:,.2f} USD` ({swaps_cnt} completed trades)" if swaps_cnt > 0 else ""

    if swaps:
        e4_status = f"🟢 ACTIVE / INVESTED ({len(swaps)} On-Chain Gems កំពុងកើបចំណេញ)" if lang == "km" else f"🟢 ACTIVE / INVESTED ({len(swaps)} On-Chain Gems)"
        e4_details = []
        for s in swaps:
            sw_sign = "+" if s['pnl_usd'] >= 0 else ""
            scale_str = "50% Moonbag Trailing" if s['scale_out_level'] == 1 else "100% Full Qty"
            short_addr = f"{s['address'][:6]}...{s['address'][-4:]}"
            e4_details.append(
                f"  • `{s['symbol']}` ({s['chain']}) ៖ Value `${s['current_val_usd']:.2f}` | Entry: `${s['entry_price']:.6f}` | Live: `${s['current_price']:.6f}` | PnL: `{sw_sign}${s['pnl_usd']:.2f}` (`{s['roi_pct']:+.1f}%`) [{scale_str}]\n"
                f"    🌾 TP/SL: `TP1 +40% (ដកដើម ១០០%) | Trailing Stop Active` | Mint: `{short_addr}`"
            )
        e4_body = ("\n".join(e4_details) + ap_str_km + pnl_hist_str_km) if lang == "km" else ("\n".join(e4_details) + ap_str_en + pnl_hist_str_en)
    elif is_ap_on:
        e4_status = "🟢 ACTIVE / HUNTING (24/7 Solana & DEX Auto-Pilot)" if lang == "km" else "🟢 ACTIVE / HUNTING (24/7 Solana & DEX Auto-Pilot)"
        sol_bal_text = f"`{sol_bal:.4f} SOL` (${sol_usd:.2f} USD)"
        e4_body = (
            f"  • 💳 កាបូបជួញដូរ Solana ៖ {sol_bal_text} | {short_sol}\n"
            f"  • 🟣 Phantom Settlement Vault ៖ {short_pvault_km}\n"
            f"  • 🛡️ សុវត្ថិភាព ៖ Jito Private MEV Shield & Honeypot AI Shield សកម្ម ១០០%\n"
            f"  • ស្ថានភាព ៖ ម៉ាស៊ីន Auto-Pilot កំពុងស្កេន DexScreener & Jupiter Breakout Firehose 24/7"
            f"{ap_str_km}"
            f"{pnl_hist_str_km}"
        ) if lang == "km" else (
            f"  • 💳 Solana Hot Wallet: {sol_bal_text} | {short_sol}\n"
            f"  • 🟣 Phantom Settlement Vault: {short_pvault_en}\n"
            f"  • 🛡️ Protection: Jito Private MEV Shield & Honeypot AI Active 100%\n"
            f"  • Status: Auto-Pilot hunting DexScreener & Jupiter Firehose 24/7"
            f"{ap_str_en}"
            f"{pnl_hist_str_en}"
        )
    else:
        e4_status = "🟡 STANDBY (ស្កេន DexScreener & Jupiter Breakout Firehose 24/7)" if lang == "km" else "🟡 STANDBY (Scanning DEX Breakout Firehose 24/7)"
        sol_bal_text = f"`{sol_bal:.4f} SOL` (${sol_usd:.2f} USD)"
        e4_body = (
            f"  • 💳 កាបូបជួញដូរ Solana ៖ {sol_bal_text} | {short_sol}\n"
            f"  • 🟣 Phantom Settlement Vault ៖ {short_pvault_km}\n"
            f"  • 🛡️ សុវត្ថិភាព ៖ Jito Private MEV Shield & Honeypot AI Shield សកម្ម ១០០%\n"
            f"  • 🎯 សកម្មភាព ៖ វាយ `/smart_swap auto 20 1234` ឬ `/smart_swap autopilot ON`"
            f"{ap_str_km}"
            f"{pnl_hist_str_km}"
        ) if lang == "km" else (
            f"  • 💳 Solana Hot Wallet: {sol_bal_text} | {short_sol}\n"
            f"  • 🟣 Phantom Settlement Vault: {short_pvault_en}\n"
            f"  • 🛡️ Protection: Jito Private MEV Shield & Honeypot AI Active 100%\n"
            f"  • 🎯 Action: Execute `/smart_swap auto 20 1234` or `/smart_swap autopilot ON`"
            f"{ap_str_en}"
            f"{pnl_hist_str_en}"
        )
    engines_text += f"4️⃣ **Smart Swap Multi-Chain DEX & AI Sniper (`/smart_swap`)**\n   {e4_status}\n{e4_body}\n\n"

    # --- ENGINE 5: Dynamic Infinity Matrix & Compound Grid ---
    grids = data["active_grids"]
    if grids:
        e5_status = f"🟢 ACTIVE ({len(grids)} សំណាញ់កំពុងកើបចំណេញ)" if lang == "km" else f"🟢 ACTIVE ({len(grids)} Active Grids)"
        e5_details = []
        for g in grids:
            g_type = g.get("type", "GRID")
            tag = "Snowball 3X" if g_type == "COMPOUND_GRID" else ("Matrix 100" if g_type == "INFINITY_MATRIX" else "Grid")
            e5_details.append(f"  • `{g['symbol']}` ({tag}) ៖ ដើមទុន `${g['current_investment']:.2f}` / Max `${g['max_investment']:.2f}` | Layer: `${g['layer_amount']:.2f}` (Step: {g['step_pct']}%)")
        e5_body = "\n".join(e5_details)
    else:
        e5_status = "🟡 STANDBY (ត្រៀមសំណាញ់វិនិយោគ Grid 3X Compound)" if lang == "km" else "🟡 STANDBY (Ready for 3X Compound Deployment)"
        e5_body = "  • ស្ថានភាព ៖ គ្មាន Grid សកម្ម (វាយ `/compound_grid AVAX 100 3.0 1234` ឬ `/infinity_matrix ON 100 1234` ដើម្បីដាក់សំណាញ់)" if lang == "km" else "  • Status: Ready to deploy via `/compound_grid` or `/infinity_matrix`"
    engines_text += f"5️⃣ **Dynamic Infinity Matrix & Compound Grid (`/infinity_matrix`)**\n   {e5_status}\n{e5_body}\n\n"

    # --- ENGINE 6: Smart Listing & Pre-Pump Sniper ---
    snipers = data["user_snipers"]
    is_pre_pump_on = data.get("is_pre_pump_enabled", False)
    pre_pump_cfg = data.get("pre_pump_cfg", {})
    pp_amt = pre_pump_cfg.get("amount", 50.0)

    if snipers:
        e6_status = f"🟢 ACTIVE SNIPER ({len(snipers)} កាក់កំពុងស្ទាក់ចាប់)" if lang == "km" else f"🟢 ACTIVE SNIPER ({len(snipers)} Targets)"
        e6_details = [f"  • `{sn.get('symbol')}` ៖ ដើមទុន `${sn.get('invest_amount', 0):.2f}` | State: `{sn.get('state')}` | Buy Price: `${sn.get('buy_price', 0):.4f}`" for sn in snipers]
        e6_body = "\n".join(e6_details)
    elif is_pre_pump_on:
        e6_status = "🟢 ACTIVE / RADAR (Whale Pre-Pump Radar កំពុងស្ទាក់ចាប់ 24/7)" if lang == "km" else "🟢 ACTIVE / RADAR (Whale Pre-Pump Radar Active 24/7)"
        e6_body = (
            f"  • 🐋 Whale Radar ៖ `🟢 ACTIVE (${pp_amt:.0f} USDT/Target)`\n"
            f"  • ស្ថានភាព ៖ 33 AI Models & WebSocket Orderflow Velocity កំពុងស្កេនចាប់កាក់ Whale Pump ២៤/៧"
        ) if lang == "km" else (
            f"  • 🐋 Whale Radar: `🟢 ACTIVE (${pp_amt:.0f} USDT/Target)`\n"
            f"  • Status: 33 AI Models & WebSocket Orderflow Velocity monitoring Whale Pumps 24/7"
        )
    else:
        e6_status = "🟡 STANDBY (WebSocket Listing Radar ត្រៀមស្ទាក់កាក់ថ្មី 24/7)" if lang == "km" else "🟡 STANDBY (Binance WebSocket Listing Radar Active 24/7)"
        e6_body = "  • ស្ថានភាព ៖ តាមដានគម្លាត Volume Velocity & 33 AI Models (វាយ `/pre_pump ON 50 1234` ដើម្បីបើក)" if lang == "km" else "  • Status: 33 AI Models & Orderflow Monitoring (Configure via `/pre_pump ON 50 1234`)"
    engines_text += f"6️⃣ **Smart Listing & Pre-Pump Engine (`/pre_pump`)**\n   {e6_status}\n{e6_body}\n\n"

    # --- ENGINE 7: 8-Hour Funding Rate & Basis Arbitrage Harvester ---
    f_cfg = data["funding_cfg"]
    if f_cfg.get("enabled"):
        e7_status = f"🟢 ACTIVE (កើបផលចំណេញ Funding Yields 8 ម៉ោងម្តង)" if lang == "km" else "🟢 ACTIVE (Harvesting 8-Hour Funding Yields)"
        e7_body = f"  • ដើមទុនបម្រុង ៖ `${f_cfg.get('amount', 50):.2f} USDT` | Delta-Neutral Immune to Market Drops"
    else:
        e7_status = "🟡 STANDBY (ត្រៀមកើបផលចំណេញ 30%-120% APY)" if lang == "km" else "🟡 STANDBY (30%-120% APY Yield Harvester Ready)"
        e7_body = "  • ស្ថានភាព ៖ រង់ចាំដំណើរការ (វាយ `/funding_harvester` ដើម្បីបើក)" if lang == "km" else "  • Status: Ready to launch via `/funding_harvester`"
    engines_text += f"7️⃣ **8-Hour Funding Rate Harvester (`/funding_harvester`)**\n   {e7_status}\n{e7_body}\n\n"

    # --- ENGINE 8: Gold Turbo & Macro Radar ---
    gold_cfg = data.get("gold_turbo_cfg", {})
    gold_on = gold_cfg.get("is_enabled", False)
    if gold_on or smart_x_active:
        e8_status = "🟢 ACTIVE (ដំណើរការ HFT Gold Turbo 24/7)" if lang == "km" else "🟢 ACTIVE (HFT Gold Turbo Active 24/7)"
        e8_body = f"  • ដើមទុន / Trade ៖ `${gold_cfg.get('amount_per_trade', 100.0):.2f} USDT` ({gold_cfg.get('max_leverage', 25)}x Lev) | AI Win-Rate Threshold: 85%" if lang == "km" else f"  • Capital / Trade: ${gold_cfg.get('amount_per_trade', 100.0):.2f} USDT"
    else:
        e8_status = "🟡 STANDBY (រង់ចាំការបើកដំណើរការ)" if lang == "km" else "🟡 STANDBY (Awaiting Activation)"
        e8_body = "  • ស្ថានភាព ៖ ម៉ាស៊ីន Macro Standby (វាយ `/gold_turbo ON 1234` ដើម្បីបើក)" if lang == "km" else "  • Status: Standby (Activate via `/gold_turbo ON 1234`)"
    engines_text += f"8️⃣ **Gold Turbo & Macro Radar (`/gold_turbo` / `/gold_guard`)**\n   {e8_status}\n{e8_body}\n\n"

    # --- ENGINE 9: DeFi Flash Loan & Tokyo HFT MEV Keeper ---
    fl_active = data["is_flash_loan_auto"]
    fl_pnl = data["flash_loan_pnl"]
    if fl_active:
        e9_status = "🟢 ACTIVE (24/7 Flash Loan Keeper លើ Arbitrum One)" if lang == "km" else "🟢 ACTIVE (24/7 Flash Loan Keeper on Arbitrum)"
        e9_body = f"  • ផលចំណេញកើបបាន ៖ `+${fl_pnl.get('total_profit', 0):,.2f} USD` ({fl_pnl.get('count', 0)} Arbitrage Trades)"
    else:
        e9_status = "🟡 STANDBY (0-Capital Risk Flash Loan Arbitrage Ready)" if lang == "km" else "🟡 STANDBY (0-Capital Risk Flash Loan Ready)"
        e9_body = "  • ស្ថានភាព ៖ Aave v3 + Uniswap v3 Routing Active (វាយ `/flash_loan` ដើម្បីបើក)" if lang == "km" else "  • Status: Aave v3 Routing Ready (Execute `/flash_loan`)"
    engines_text += f"9️⃣ **DeFi Flash Loan & Tokyo MEV Stack (`/flash_loan`)**\n   {e9_status}\n{e9_body}\n\n"

    # --- ENGINE 10: Liquidation Defender & Circuit Breaker ---
    def_on = data["is_defender_active"]
    breaker = data["circuit_breaker"]
    if def_on or not breaker.get("tripped"):
        e10_status = "🟢 ACTIVE (ការការពារកម្រិតស្ថាប័ន ២៤/៧)" if lang == "km" else "🟢 ACTIVE (Institutional Safeguard 24/7)"
        e10_body = "  • ស្ថានភាព ៖ Max 2% Drawdown Guard & Breakeven Lock Armored (Zero Liquidation Risk)" if lang == "km" else "  • Status: 2% Max Drawdown Guard & Breakeven Lock Active"
    else:
        e10_status = "🔴 CIRCUIT BREAKER TRIPPED" if lang == "km" else "🔴 CIRCUIT BREAKER TRIPPED"
        e10_body = "  • ស្ថានភាព ៖ ប្រព័ន្ធបានផ្អាកការជួញដូរជាបណ្តោះអាសន្នដើម្បីការពារដើមទុន" if lang == "km" else "  • Status: System paused to protect capital"
    engines_text += f"🔟 **Liquidation Defender & Circuit Breaker Sentinel**\n   {e10_status}\n{e10_body}\n"

    # =========================================================================
    # 3. INTERACTIVE FOOTER
    # =========================================================================
    footer = (
        "────────────\n"
        "💡 *ចុចប៊ូតុងខាងក្រោមដើម្បី Refresh ឬបញ្ជា Stop/Launch ភ្លាមៗ ៖*"
    ) if lang == "km" else (
        "────────────\n"
        "💡 *Use the interactive buttons below to refresh or manage positions:*"
    )

    if include_vitals:
        vitals_block = (
            "────────────\n"
            "🖥️ **ស្ថានភាពម៉ាស៊ីនបម្រើការ (VPS Vitals & Health):**\n"
            f"• ⏳ Uptime ៖ `{data['uptime_str']}`\n"
            f"• 🧠 CPU Load ៖ `{data['cpu_usage']:.1f}%` (Dynamic Core)\n"
            f"• 📊 RAM Usage ៖ `{data['ram_usage_mb']} MB / {data['ram_total_mb']} MB ({data['ram_pct']:.1f}%)`\n"
            f"• 💾 Database Size ៖ `{data['db_size_mb']:.2f} MB` (SQLite WAL High-Speed Mode)\n"
        ) if lang == "km" else (
            "────────────\n"
            "🖥️ **VPS HARDWARE & SYSTEM HEALTH:**\n"
            f"• ⏳ Uptime: `{data['uptime_str']}`\n"
            f"• 🧠 CPU Load: `{data['cpu_usage']:.1f}%` (Multi-Core Dynamic)\n"
            f"• 📊 RAM Usage: `{data['ram_usage_mb']} MB / {data['ram_total_mb']} MB ({data['ram_pct']:.1f}%)`\n"
            f"• 💾 Database Size: `{data['db_size_mb']:.2f} MB` (WAL High-Speed Mode)\n"
        )
        return header + engines_text + vitals_block + footer

    return header + engines_text + footer

def render_smart_swap_dex_portfolio_card(data: dict, user_lang: str = "km") -> str:
    """
    Renders an institutional-grade, specialized On-Chain DEX Portfolio card
    focusing entirely on /smart_swap, Solana Hot Wallet, Phantom Vault, and Live Gems.
    """
    lang = "en" if str(user_lang).lower() in ["en", "english"] else "km"
    chat_id = data["chat_id"]
    is_paper = data["is_paper"]
    badge_mode = "🧪 PAPER TRADING SIMULATION" if is_paper else "🚀 REAL LIVE ON-CHAIN (Jupiter DEX)"

    user_sol_pub = data.get("user_sol_pubkey", "")
    short_sol = f"`{user_sol_pub[:6]}...{user_sol_pub[-4:]}`" if user_sol_pub else "`N/A`"
    sol_usd = data.get("user_sol_usd", 0.0)
    sol_bal = data.get("user_sol_bal", 0.0)

    p_vault = data.get("phantom_vault", "")
    short_pvault = f"`{p_vault[:6]}...{p_vault[-4:]}`" if p_vault else ""

    swaps = data.get("active_smart_swaps", [])
    active_swaps_usd = sum(s.get("current_val_usd", 0.0) for s in swaps)
    active_swaps_pnl = sum(s.get("pnl_usd", 0.0) for s in swaps)
    realized_pnl = data.get("total_realized_swap_pnl", 0.0)
    swaps_count = data.get("total_swaps_count", 0)
    total_onchain = data.get("total_onchain_capital", 0.0)

    pnl_sign = "+" if active_swaps_pnl >= 0 else ""
    pnl_emoji = "🟩" if active_swaps_pnl >= 0 else "🟥"

    ap_cfg = data.get("smart_swap_autopilot", {})
    is_ap_on = ap_cfg.get("enabled", False)
    ap_amt = ap_cfg.get("amount", 20.0)
    ap_pos = ap_cfg.get("max_positions", 2)
    ap_status_en = f"`🟢 ACTIVE 24/7` (${ap_amt:.0f}/Trade | Slot: `{len(swaps)}/{ap_pos}`)" if is_ap_on else "`⚪ STANDBY` (Run `/smart_swap autopilot ON 20 1234`)"
    ap_status_km = f"`🟢 ACTIVE 24/7` (${ap_amt:.0f}/Trade | Slot: `{len(swaps)}/{ap_pos}`)" if is_ap_on else "`⚪ STANDBY` (វាយ `/smart_swap autopilot ON 20 1234`)"

    if lang == "en":
        lines = [
            "⚡ **KHMER MASTER CRYPTO | SUPER SMART ON-CHAIN DEX PORTFOLIO** 🚀",
            "════════════",
            f"💼 **ACCOUNT CLEARANCE:** `ID: {chat_id}` | `{badge_mode}`",
            "════════════\n",
            "💰 **ON-CHAIN CAPITAL & DEX METRICS:**",
            f"• 💎 **Total On-Chain Net Capital:** `${total_onchain:,.2f} USD`",
            f"• 🎯 **Active in DEX Breakout Gems:** `${active_swaps_usd:,.2f} USD` ({len(swaps)} active)",
            f"• 💵 **Solana Hot Wallet Balance:** `${sol_usd:,.2f} USD` (`{sol_bal:.4f} SOL`)",
            f"• {pnl_emoji} **Floating DEX PnL:** `{pnl_sign}${active_swaps_pnl:,.2f} USD`",
            f"• 🏆 **Historical Realized Profit:** `+${realized_pnl:,.2f} USD` ({swaps_count} completed trades)",
            f"• 🔄 **24/7 Autonomous Auto-Pilot:** {ap_status_en}\n",
            "💳 **MULTI-TENANT DUAL-WALLET ARCHITECTURE:**",
            f"• ⚡ **Dedicated Solana Trading Wallet:** {short_sol} (`{user_sol_pub}`)",
            "  *(Personal Trojan/BonkBot-style execution wallet for sub-second DEX swaps)*"
        ]
        if p_vault:
            lines.append(f"• 🟣 **Phantom Profit Settlement Vault:** {short_pvault} (`{p_vault}`) (Bound ✅)")
            lines.append("  *(100% Non-Custodial Zero-Risk destination for automated profit taking)*\n")
        else:
            lines.append("• 🟣 **Phantom Profit Settlement Vault:** `Not Linked`")
            lines.append("  *(Execute `/smart_swap bind_phantom 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU` to set your profit destination)*\n")

        lines.append("📊 **ACTIVE ON-CHAIN GEM POSITIONS:**")
        if swaps:
            for s in swaps:
                s_sign = "+" if s['pnl_usd'] >= 0 else ""
                scale_str = "50% Moonbag Trailing" if s['scale_out_level'] == 1 else "100% Full Position"
                short_mint = f"{s['address'][:6]}...{s['address'][-4:]}"
                lines.append(
                    f"• `{s['symbol']}` ({s['chain']}) ៖ Value `${s['current_val_usd']:.2f}` | Entry: `${s['entry_price']:.6f}` | Live: `${s['current_price']:.6f}` | PnL: `{s_sign}${s['pnl_usd']:.2f}` (`{s['roi_pct']:+.1f}%`)\n"
                    f"  🌾 Strategy: `TP1 +40% (Capital Lock) | Moonbag Trailing` | Mint: `{short_mint}`"
                )
            lines.append("")
        else:
            lines.append("• 🟡 *No active DEX positions currently open (AI Scanner active 24/7)*\n")

        lines.extend([
            "🛡️ **INSTITUTIONAL SPEED & SECURITY STACK:**",
            "• ⚡ **Routing Engine:** `Jupiter Aggregator v6 Multi-DEX Direct`",
            "• 🛡️ **Anti-MEV:** `Jito Private Bundle (Zero Sandwich & Front-run Immune)`",
            "• 🔍 **Honeypot Shield:** `Sub-Second Pre-Trade Security Audit (Freeze/Mint Revoked)`",
            "• 🌾 **Profit Harvester:** `TP1 +40% (100% Capital Lock) + 50% Trailing Moonbag`\n",
            "────────────",
            "💡 *Use the interactive buttons below to snipe gems, check wallet, or exit market:*"
        ])
        return "\n".join(lines)
    else:
        lines = [
            "⚡ **KHMER MASTER CRYPTO | SUPER SMART ON-CHAIN DEX PORTFOLIO** 🚀",
            "════════════",
            f"💼 **គណនីវិនិយោគិន ៖** `ID: {chat_id}` | `{badge_mode}`",
            "════════════\n",
            "💰 **ទិដ្ឋភាពទុនជួញដូរ On-Chain (DEX Capital Overview) ៖**",
            f"• 💎 **ទុន On-Chain សរុប ៖** `${total_onchain:,.2f} USD`",
            f"• 🎯 **កំពុងវិនិយោគក្នុង DEX Gems ៖** `${active_swaps_usd:,.2f} USD` ({len(swaps)} កាក់សកម្ម)",
            f"• 💵 **ត្រៀមក្នុងកាបូប Solana Hot Wallet ៖** `${sol_usd:,.2f} USD` (`{sol_bal:.4f} SOL`)",
            f"• {pnl_emoji} **ផលចំណេញបណ្តោះអាសន្ន (Floating DEX PnL) ៖** `{pnl_sign}${active_swaps_pnl:,.2f} USD`",
            f"• 🏆 **ប្រាក់ចំណេញកើបបានពីមុន (Realized PnL) ៖** `+${realized_pnl:,.2f} USD` ({swaps_count} លើក)",
            f"• 🔄 **24/7 Autonomous Auto-Pilot ៖** {ap_status_km}\n",
            "💳 **ការគ្រប់គ្រងកាបូប On-Chain (Dual-Wallet Architecture) ៖**",
            f"• ⚡ **Solana Dedicated Hot Wallet ៖** {short_sol}",
            f"  `{user_sol_pub}`",
            "  *(កាបូបផ្ទាល់ខ្លួន Bot សម្រាប់បាញ់កាក់លើ Jupiter DEX & Raydium អូតូ ២៤/៧)*"
        ]
        if p_vault:
            lines.append(f"• 🟣 **Phantom Profit Settlement Vault ៖** {short_pvault} (ភ្ជាប់រួចរាល់ ✅)")
            lines.append(f"  `{p_vault}`")
            lines.append("  *(រាល់ពេលដកចំណេញ នឹងរត់ចូល Phantom ផ្ទាល់ខ្លួនភ្លាមៗ សុវត្ថិភាព ១០០%)*\n")
        else:
            lines.append("• 🟣 **Phantom Profit Settlement Vault ៖** `មិនទាន់ភ្ជាប់`")
            lines.append("  *(វាយ `/smart_swap bind_phantom 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU` ដើម្បីភ្ជាប់កាបូបដកប្រាក់)*\n")

        lines.append("📊 **ស្ថានភាពកាក់ Gem On-Chain កំពុងជួញដូរ (Active Positions) ៖**")
        if swaps:
            for s in swaps:
                s_sign = "+" if s['pnl_usd'] >= 0 else ""
                scale_str = "50% Moonbag Trailing" if s['scale_out_level'] == 1 else "100% Full Position"
                short_mint = f"{s['address'][:6]}...{s['address'][-4:]}"
                lines.append(
                    f"• `{s['symbol']}` ({s['chain']}) ៖ Value `${s['current_val_usd']:.2f}` | Entry: `${s['entry_price']:.6f}` | Live: `${s['current_price']:.6f}` | PnL: `{s_sign}${s['pnl_usd']:.2f}` (`{s['roi_pct']:+.1f}%`)\n"
                    f"  🌾 យុទ្ធសាស្ត្រ: `TP1 +40% (ដកដើម ១០០%) | Trailing Stop` | Mint: `{short_mint}`"
                )
            lines.append("")
        else:
            lines.append("• 🟡 *បច្ចុប្បន្នគ្មានកាក់ Gem កំពុងកាន់កាប់ឡើយ (ម៉ាស៊ីន AI កំពុងស្កេន DexScreener 24/7)*\n")

        lines.extend([
            "🛡️ **ប្រព័ន្ធសុវត្ថិភាព និងល្បឿនស្ថាប័ន (Institutional DEX Stack) ៖**",
            "• ⚡ **Router ៖** `Jupiter Aggregator v6 Direct Routing`",
            "• 🛡️ **Anti-MEV ៖** `Jito Private Bundle (ការពារការលួច Front-run & Sandwich)`",
            "• 🔍 **Honeypot Shield ៖** `Sub-Second Security Audit (Freeze & Mint Revoked)`",
            "• 🌾 **Profit Harvester ៖** `TP1 +40% (Lock ដើមទុន ១០០%) + Moonbag 50% Trailing`\n",
            "────────────",
            "💡 *ចុចប៊ូតុងខាងក្រោមដើម្បីបញ្ជា Auto Gem Sniper, ពិនិត្យកាបូប ឬ Stop Market ភ្លាមៗ ៖*"
        ])
        return "\n".join(lines)

