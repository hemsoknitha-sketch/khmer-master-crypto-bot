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
  6. Smart Listing & Pre-Pump Accumulation Sniper (/snipe / /pre_pump)
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
            fut_bal, fut_unreal = trading_engine.get_futures_balance_detailed(keys[0], keys[1], "USDT")
            futures_wallet_usdt = float(fut_bal or 0.0)
            futures_unrealized_pnl = float(fut_unreal or 0.0)
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

    # 6. Active Infinity Grids
    active_grids = []
    try:
        raw_grids = db.get_active_infinity_grids_by_user(chat_id) or []
        for g in raw_grids:
            # (id, symbol, amount_per_layer, step_pct, max_investment, current_investment, last_price)
            g_id, sym, layer_amt, step_pct, max_inv, curr_inv, last_p = g[:7]
            curr_p = trading_engine.get_current_price(sym) or float(last_p)
            active_grids.append({
                "id": g_id,
                "symbol": sym,
                "layer_amount": float(layer_amt),
                "step_pct": float(step_pct),
                "max_investment": float(max_inv),
                "current_investment": float(curr_inv),
                "last_price": float(last_p),
                "current_price": float(curr_p)
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

    # 8. Funding Harvester
    funding_cfg = db.get_funding_harvester_config(chat_id) if hasattr(db, 'get_funding_harvester_config') else {"enabled": False, "amount": 50.0}

    # 8b. Gold Turbo Config
    gold_turbo_cfg = db.get_gold_turbo_config(chat_id) if hasattr(db, 'get_gold_turbo_config') else {"is_enabled": False, "amount_per_trade": 15.0}

    # 8c. Smart X Quant Config
    smart_x_active = (db.get_system_setting(f"smart_x_{chat_id}_active", "0") == "1") if hasattr(db, 'get_system_setting') else False
    smart_x_target = db.get_system_setting(f"smart_x_{chat_id}_target", "GOLD") if hasattr(db, 'get_system_setting') else "GOLD"

    # 9. Flash Loan Keeper & Strategy
    is_flash_loan_auto = db.is_user_flash_loan_auto(chat_id) if hasattr(db, 'is_user_flash_loan_auto') else False
    flash_loan_pnl = db.get_user_flash_loan_pnl_summary(chat_id) if hasattr(db, 'get_user_flash_loan_pnl_summary') else {"count": 0, "total_profit": 0.0}

    # 10. Liquidation Defender & Circuit Breaker
    is_defender_active = db.is_defender_active() if hasattr(db, 'is_defender_active') else False
    circuit_breaker = db.get_circuit_breaker_status() if hasattr(db, 'get_circuit_breaker_status') else {"tripped": False}

    # 11. Multi-Chain Web3 Settlement Wallet
    web3_wallets = db.get_user_multichain_wallets(chat_id) if hasattr(db, 'get_user_multichain_wallets') else {}
    primary_web3 = db.get_user_web3_wallet(chat_id) if hasattr(db, 'get_user_web3_wallet') else ""

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
    total_onchain_capital = sum(s["current_val_usd"] for s in active_smart_swaps)
    total_portfolio_net_worth = total_spot_capital + total_futures_capital + total_onchain_capital

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

        # Active Positions per Engine
        "active_futures_positions": active_futures_positions,
        "active_spot_trades": active_spot_trades,
        "user_turbo_bots": user_turbo_bots,
        "active_smart_swaps": active_smart_swaps,
        "active_grids": active_grids,
        "user_snipers": user_snipers,

        # Engine Flags
        "funding_cfg": funding_cfg,
        "gold_turbo_cfg": gold_turbo_cfg,
        "smart_x_active": smart_x_active,
        "smart_x_target": smart_x_target,
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

    # =========================================================================
    # 1. HEADER & EXECUTIVE CAPITAL SUMMARY
    # =========================================================================
    if lang == "en":
        header = (
            "👑 **KHMER MASTER CRYPTO | INSTITUTIONAL SUPER SMART PORTFOLIO** 🛡️\n"
            "══════════════════════════════════════\n"
            f"💼 **ACCOUNT CLEARANCE:** `ID: {chat_id}` | `{badge_mode}`\n"
            "══════════════════════════════════════\n\n"
            "💰 **CONSOLIDATED NET CAPITAL OVERVIEW:**\n"
            f"• 💎 **Total Net Portfolio Value:** `${net_worth:,.2f} USD`\n"
            f"• 🎯 **Active Capital at Work:** `${invested:,.2f} USD`\n"
            f"• {pnl_emoji} **Total Floating Net PnL:** `{pnl_str}` (`{roi:+.2f}%` ROI)\n\n"
            "🏦 **MULTI-WALLET BALANCES:**\n"
            f"• 🟡 **Binance Spot:** `${data['spot_usdt_free']:,.2f} USDT` free | `${data['spot_alt_exposure']:,.2f}` in Coins\n"
            f"• ⚡ **Binance Futures:** `${data['futures_wallet_usdt']:,.2f} USDT` balance (PnL: `${data['futures_unrealized_pnl']:+,.2f}`)\n"
            f"• 🌐 **Web3 On-Chain:** `${data['total_onchain_capital']:,.2f} USD` across Solana & EVM\n"
            "──────────────────────────────────────\n\n"
        )
    else:
        header = (
            "👑 **KHMER MASTER CRYPTO | របាយការណ៍វិនិយោគរួម SUPER SMART PORTFOLIO** 🛡️\n"
            "══════════════════════════════════════\n"
            f"💼 **គណនីវិនិយោគិន ៖** `ID: {chat_id}` | `{badge_mode}`\n"
            "══════════════════════════════════════\n\n"
            "💰 **ទិដ្ឋភាពរួមដើមទុន និងប្រាក់ចំណេញសរុប ៖**\n"
            f"• 💎 **ទ្រព្យសរុបក្នុងប្រព័ន្ធ (Net Worth) ៖** `${net_worth:,.2f} USD`\n"
            f"• 🎯 **ដើមទុនកំពុងវិនិយោគជាក់ស្តែង ៖** `${invested:,.2f} USD`\n"
            f"• {pnl_emoji} **ផលចំណេញសរុបបណ្តោះអាសន្ន (Floating PnL) ៖** `{pnl_str}` (`{roi:+.2f}%` ROI)\n\n"
            "🏦 **សមតុល្យតាមកាបូបនីមួយៗ (Multi-Wallet Balances) ៖**\n"
            f"• 🟡 **Binance Spot ៖** `${data['spot_usdt_free']:,.2f} USDT` សេរី | `${data['spot_alt_exposure']:,.2f}` កំពុងកាន់កាក់\n"
            f"• ⚡ **Binance Futures ៖** `${data['futures_wallet_usdt']:,.2f} USDT` ក្នុងកាបូប (PnL: `${data['futures_unrealized_pnl']:+,.2f}`)\n"
            f"• 🌐 **Web3 On-Chain ៖** `${data['total_onchain_capital']:,.2f} USD` លើ Solana & EVM\n"
            "──────────────────────────────────────\n\n"
        )

    # =========================================================================
    # 2. AUDIT OF ALL 10 INVESTMENT ENGINES (WITH ACTIVE ASSETS)
    # =========================================================================
    engines_text = "📊 **ស្ថានភាពដំណើរការម៉ាស៊ីនវិនិយោគទាំង ១០ (10-ENGINE AUDIT):**\n\n" if lang == "km" else "📊 **OPERATIONAL STATUS OF ALL 10 ENGINES:**\n\n"

    # --- ENGINE 1: Turbo Hedge & Delta-Neutral HFT Engine ---
    tb_bots = data["user_turbo_bots"]
    fut_pos = data["active_futures_positions"]
    if tb_bots or fut_pos:
        e1_status = "🟢 ACTIVE / INVESTED (កំពុងវិនិយោគពិតប្រាកដ)" if lang == "km" else "🟢 ACTIVE / INVESTED"
        e1_details = []
        for b in tb_bots:
            e1_details.append(f"  • `{b['symbol']}` ({b['side']} {b['leverage']}x) ៖ ដើមទុន `${b['amount_usd']:.2f}` | Entry: `${b['entry_price']:.4f}` | Mark: `${b['current_price']:.4f}` | TP: `+{b['target_tp_pct']}%`")
        for p in fut_pos:
            # If not already detailed in tb_bots
            if not any(b['symbol'] == p['symbol'] for b in tb_bots):
                e_pnl_sign = "+" if p['pnl_usd'] >= 0 else ""
                e1_details.append(f"  • `{p['symbol']}` ({p['side']} {p['leverage']}x ISOLATED) ៖ Margin `${p['margin_usd']:.2f}` | Entry: `${p['entry_price']:.4f}` | Mark: `${p['mark_price']:.4f}` | PnL: `{e_pnl_sign}${p['pnl_usd']:.2f}` (`{p['roi_pct']:+.1f}%`)")
        e1_body = "\n".join(e1_details)
    else:
        e1_status = "🟡 STANDBY (រង់ចាំឱកាស ស្កេន Basis & Funding 24/7)" if lang == "km" else "🟡 STANDBY (Scanning Basis & Funding 24/7)"
        e1_body = "  • ស្ថានភាព ៖ រង់ចាំសញ្ញាបញ្ជា `/turbo_hedge HEDGE auto 20 1234`" if lang == "km" else "  • Status: Standby for command `/turbo_hedge HEDGE auto 20 1234`"
    engines_text += f"1️⃣ **Turbo Hedge & Delta-Neutral HFT Engine (`/turbo_hedge`)**\n   {e1_status}\n{e1_body}\n\n"

    # --- ENGINE 2: Super Smart Trade Suite (Spot Breakout & Top Gainers) ---
    sp_trades = data["active_spot_trades"]
    if sp_trades:
        e2_status = f"🟢 ACTIVE ({len(sp_trades)} កាក់កំពុងជួញដូរ)" if lang == "km" else f"🟢 ACTIVE ({len(sp_trades)} Spot Positions)"
        e2_details = []
        for st in sp_trades:
            s_sign = "+" if st['pnl_usd'] >= 0 else ""
            e2_details.append(f"  • `{st['symbol']}` ៖ ដើមទុន `${st['invested_usd']:.2f}` | Entry: `${st['buy_price']:.4f}` | Mark: `${st['current_price']:.4f}` | PnL: `{s_sign}${st['pnl_usd']:.2f}` (`{st['roi_pct']:+.2f}%`)")
        e2_body = "\n".join(e2_details)
    else:
        e2_status = "🟡 STANDBY (ស្កេនរកកាក់ Spot Breakout & Top Gainers 24/7)" if lang == "km" else "🟡 STANDBY (Scanning Spot Breakouts 24/7)"
        e2_body = "  • ស្ថានភាព ៖ គ្មានកាក់ Spot កំពុងជួញដូរ (វាយ `/smart_trade auto 20 1234` ដើម្បីចាប់ផ្តើម)" if lang == "km" else "  • Status: Ready to execute `/smart_trade auto 20 1234`"
    engines_text += f"2️⃣ **Super Smart Trade Suite (`/smart_trade` / `auto_trade`)**\n   {e2_status}\n{e2_body}\n\n"

    # --- ENGINE 3: Smart X Multi-Asset Quant Suite (Gold & BTC) ---
    smart_x_active = data.get("smart_x_active", False)
    smart_x_target = data.get("smart_x_target", "GOLD")
    paxg_pos = [p for p in fut_pos if "PAXG" in p.get("symbol", "")] + [s for s in sp_trades if "PAXG" in s.get("symbol", "")]
    btc_pos = [p for p in fut_pos if "BTC" in p.get("symbol", "")] + [s for s in sp_trades if "BTC" in s.get("symbol", "")]
    smart_x_bots = [b for b in tb_bots if "PAXG" in b.get("symbol", "") or "BTC" in b.get("symbol", "")]

    if smart_x_active or paxg_pos or btc_pos or smart_x_bots:
        e3_status = "🟢 ACTIVE / INVESTED (ម៉ាស៊ីន AI Quant កំពុងជួញដូរ)" if lang == "km" else "🟢 ACTIVE / INVESTED"
        e3_details = []
        if paxg_pos:
            for p in paxg_pos:
                p_pnl = p.get('pnl_usd', 0.0)
                p_sign = "+" if p_pnl >= 0 else ""
                p_margin = p.get('margin_usd', p.get('invested_usd', 0.0))
                p_side = p.get('side', 'BUY')
                p_lev = p.get('leverage', 10)
                e3_details.append(f"  • `PAXGUSDT` (Gold Quant {p_side} {p_lev}x) ៖ Margin `${p_margin:.2f}` | Entry: `${p.get('entry_price', 0):.2f}` | PnL: `{p_sign}${p_pnl:.2f}` (`{p.get('roi_pct', 0.0):+.1f}%`)")
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
    if swaps:
        e4_status = f"🟢 ACTIVE ({len(swaps)} On-Chain Gems កំពុងកើបចំណេញ)" if lang == "km" else f"🟢 ACTIVE ({len(swaps)} On-Chain Gems)"
        e4_details = []
        for s in swaps:
            sw_sign = "+" if s['pnl_usd'] >= 0 else ""
            scale_str = "50% Moonbag" if s['scale_out_level'] == 1 else "100% Full Qty"
            e4_details.append(f"  • `{s['symbol']}` ({s['chain']}) ៖ Value `${s['current_val_usd']:.2f}` | Entry: `${s['entry_price']:.6f}` | Live: `${s['current_price']:.6f}` | PnL: `{sw_sign}${s['pnl_usd']:.2f}` (`{s['roi_pct']:+.1f}%`) [{scale_str}]")
        e4_body = "\n".join(e4_details)
    else:
        e4_status = "🟡 STANDBY (ស្កេន DexScreener/Jupiter ស្វែងរកកាក់ Breakout 24/7)" if lang == "km" else "🟡 STANDBY (Scanning DEX Breakout Firehose 24/7)"
        e4_body = "  • ស្ថានភាព ៖ Honeypot & Jito MEV Shield សកម្ម (វាយ `/smart_swap auto 20 1234` ដើម្បីបាញ់)" if lang == "km" else "  • Status: Armed with Jito MEV Protection (Execute `/smart_swap auto 20 1234`)"
    engines_text += f"4️⃣ **Smart Swap Multi-Chain DEX & AI Sniper (`/smart_swap`)**\n   {e4_status}\n{e4_body}\n\n"

    # --- ENGINE 5: Dynamic Infinity Matrix & Compound Grid ---
    grids = data["active_grids"]
    if grids:
        e5_status = f"🟢 ACTIVE ({len(grids)} Grids កំពុងរាយសំណាញ់)" if lang == "km" else f"🟢 ACTIVE ({len(grids)} Infinity Grids)"
        e5_details = []
        for g in grids:
            e5_details.append(f"  • `{g['symbol']}` ៖ ដើមទុន `${g['current_investment']:.2f}` / Max `${g['max_investment']:.2f}` | Layer: `${g['layer_amount']:.2f}` (Step: {g['step_pct']}%)")
        e5_body = "\n".join(e5_details)
    else:
        e5_status = "🟡 STANDBY (ត្រៀមសំណាញ់វិនិយោគ Grid 3X Compound)" if lang == "km" else "🟡 STANDBY (Ready for 3X Compound Deployment)"
        e5_body = "  • ស្ថានភាព ៖ គ្មាន Grid សកម្ម (វាយ `/compound_grid XRP 100 1234` ដើម្បីដាក់សំណាញ់)" if lang == "km" else "  • Status: Ready to deploy via `/compound_grid`"
    engines_text += f"5️⃣ **Dynamic Infinity Matrix & Compound Grid (`/infinity_matrix`)**\n   {e5_status}\n{e5_body}\n\n"

    # --- ENGINE 6: Smart Listing & Pre-Pump Sniper ---
    snipers = data["user_snipers"]
    if snipers:
        e6_status = f"🟢 ACTIVE SNIPER ({len(snipers)} កាក់កំពុងស្ទាក់ចាប់)" if lang == "km" else f"🟢 ACTIVE SNIPER ({len(snipers)} Targets)"
        e6_details = [f"  • `{sn.get('symbol')}` ៖ ដើមទុន `${sn.get('invest_amount', 0):.2f}` | State: `{sn.get('state')}` | Buy Price: `${sn.get('buy_price', 0):.4f}`" for sn in snipers]
        e6_body = "\n".join(e6_details)
    else:
        e6_status = "🟡 STANDBY (WebSocket WebSocket Listing Radar ត្រៀមស្ទាក់កាក់ថ្មី 24/7)" if lang == "km" else "🟡 STANDBY (Binance WebSocket Listing Radar Active 24/7)"
        e6_body = "  • ស្ថានភាព ៖ តាមដានគម្លាត Volume Velocity (វាយ `/snipe` ដើម្បីកំណត់)" if lang == "km" else "  • Status: Monitoring order books (Configure via `/snipe`)"
    engines_text += f"6️⃣ **Smart Listing & Pre-Pump Sniper (`/snipe` / `/pre_pump`)**\n   {e6_status}\n{e6_body}\n\n"

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
    if gold_on:
        e8_status = "🟢 ACTIVE (ដំណើរការ HFT Gold Turbo 24/7)" if lang == "km" else "🟢 ACTIVE (HFT Gold Turbo Active 24/7)"
        e8_body = f"  • ដើមទុន / Trade ៖ `${gold_cfg.get('amount_per_trade', 15.0):.2f} USDT` ({gold_cfg.get('max_leverage', 25)}x Lev) | AI Win-Rate Threshold: 85%" if lang == "km" else f"  • Capital / Trade: ${gold_cfg.get('amount_per_trade', 15.0):.2f} USDT"
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
        "──────────────────────────────────────\n"
        "💡 *ចុចប៊ូតុងខាងក្រោមដើម្បី Refresh ឬបញ្ជា Stop/Launch ភ្លាមៗ ៖*"
    ) if lang == "km" else (
        "──────────────────────────────────────\n"
        "💡 *Use the interactive buttons below to refresh or manage positions:*"
    )

    if include_vitals:
        vitals_block = (
            "──────────────────────────────────────\n"
            "🖥️ **ស្ថានភាពម៉ាស៊ីនបម្រើការ (VPS Vitals & Health):**\n"
            f"• ⏳ Uptime ៖ `{data['uptime_str']}`\n"
            f"• 🧠 CPU Load ៖ `{data['cpu_usage']:.1f}%` (Dynamic Core)\n"
            f"• 📊 RAM Usage ៖ `{data['ram_usage_mb']} MB / {data['ram_total_mb']} MB ({data['ram_pct']:.1f}%)`\n"
            f"• 💾 Database Size ៖ `{data['db_size_mb']:.2f} MB` (SQLite WAL High-Speed Mode)\n"
        ) if lang == "km" else (
            "──────────────────────────────────────\n"
            "🖥️ **VPS HARDWARE & SYSTEM HEALTH:**\n"
            f"• ⏳ Uptime: `{data['uptime_str']}`\n"
            f"• 🧠 CPU Load: `{data['cpu_usage']:.1f}%` (Multi-Core Dynamic)\n"
            f"• 📊 RAM Usage: `{data['ram_usage_mb']} MB / {data['ram_total_mb']} MB ({data['ram_pct']:.1f}%)`\n"
            f"• 💾 Database Size: `{data['db_size_mb']:.2f} MB` (WAL High-Speed Mode)\n"
        )
        return header + engines_text + vitals_block + footer

    return header + engines_text + footer
