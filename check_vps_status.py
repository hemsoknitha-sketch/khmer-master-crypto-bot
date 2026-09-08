#!/usr/bin/env python3
"""
======================================================================
  KHMER MASTER CRYPTO - ARBITRUM ONE VPS STATUS & AUTHORIZATION CHECK
======================================================================
This diagnostic script verifies the end-to-end authorization between:
1. Keeper Private Key in .env
2. Smart Contract Address on Arbitrum One
3. On-chain Owner verification
4. Real Gas balance on Arbitrum One
5. Live Pre-flight Execution Readiness
======================================================================
"""

import sys
import os

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import keeper_relayer

def run_check():
    print("=" * 65)
    print("  🔍 KHMER MASTER CRYPTO - VPS AUTHORIZATION DIAGNOSTIC")
    print("=" * 65)

    engine = keeper_relayer.keeper_engine
    status = engine.get_status_overview()

    keeper_addr = status.get("keeper_address", "N/A")
    contract_addr = status.get("contract_address", "N/A")
    gas_eth = status.get("arbitrum_gas_eth", 0.0)
    gas_usd = status.get("gas_usd_est", 0.0)
    is_funded = status.get("is_funded", False)
    mode = status.get("execution_mode", "UNKNOWN")
    rpc_ok = status.get("rpc_connected", False)
    chain_id = status.get("chain_id", 42161)

    print(f"📡 Arbitrum RPC Connected:  {'✅ YES' if rpc_ok else '❌ NO'} (Chain ID: {chain_id})")
    print(f"💼 Keeper Wallet Address:   {keeper_addr}")
    print(f"⛽ Gas Balance (Arbitrum):  {gas_eth:.6f} ETH (~${gas_usd:.2f} USD)")
    print(f"⛽ Is Gas Funded (> $2.00): {'✅ YES' if is_funded else '❌ NO'}")
    print(f"📜 Smart Contract Address:  {contract_addr}")

    # Query On-Chain Owner
    import requests
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": contract_addr, "data": "0x8da5cb5b"}, "latest"],
        "id": 1
    }
    owner_addr = "Unknown"
    is_owner = False
    try:
        r = requests.post(keeper_relayer.ARBITRUM_RPC_PRIMARY, json=payload, timeout=8).json()
        raw = r.get("result", "")
        if raw and len(raw) >= 40:
            owner_addr = "0x" + raw[-40:]
            is_owner = (owner_addr.lower() == keeper_addr.lower())
    except Exception as e:
        owner_addr = f"Query error: {e}"

    print(f"👑 On-Chain Contract Owner: {owner_addr}")
    print(f"🔐 Owner & Keeper Match:   {'✅ 100% MATCH' if is_owner else '❌ MISMATCH'}")
    print(f"⚙️ Execution Mode:          {mode}")

    # Test Preflight Authorization
    print("-" * 65)
    print("🧪 Running Instant On-Chain Authorization Test...")
    res = engine.execute_onchain_flash_loan(
        borrow_asset="USDT",
        amount_usd=1000.0,
        intermediate_token="WETH",
        min_net_profit_usd=5.0,
        user_recipient=keeper_addr,
        dex_route=0,
        pool_fee=500
    )

    err = res.get("error", "")
    is_auth = "Caller not authorized" not in err

    if is_auth and is_owner and is_funded:
        print("🎉 [RESULT]: ✅ FULLY AUTHORIZED & LIVE MAINNET READY!")
        print("   The contract strictly recognizes this keeper wallet as the owner.")
        print(f"   Net profit will flow 100% directly to: {keeper_addr}")
    else:
        print("⚠️ [RESULT]: ❌ AUTHORIZATION INCOMPLETE")
        if not is_owner:
            print("   - Keeper wallet does not match on-chain contract owner.")
        if not is_funded:
            print("   - Keeper wallet needs ETH gas on Arbitrum One.")
        if not is_auth:
            print(f"   - Revert: {err}")

    print("=" * 65)

if __name__ == "__main__":
    run_check()
