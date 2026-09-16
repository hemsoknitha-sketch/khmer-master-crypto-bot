"""
Khmer Master Crypto / Apex TURBO AGI v13.00
ARBITRUM ONE FLASH LOAN SMART CONTRACT V2 DEPLOYMENT HELPER
================================================================================
Deploys SuperSmartFlashLoanArbitrageV2.sol to Arbitrum One Mainnet using Keeper Wallet.
Unlocks 0.00% fee flash loans via Balancer V2 Vault and Multi-DEX Routing (Uniswap, Camelot, SushiSwap).
================================================================================
"""

import os
import sys
import json
import time

# Ensure root project directory is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from dotenv import load_dotenv
    _env_f = os.path.join(root_dir, ".env")
    if os.path.exists(_env_f):
        load_dotenv(_env_f, override=True)
except Exception:
    pass

from web3 import Web3
import keeper_relayer

# Arbitrum One Verified Protocol Addresses
AAVE_V3_ADDRESSES_PROVIDER = "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb" # Aave V3 Arbitrum
BALANCER_V2_VAULT          = "0xBA12222222228d8Ba445958a75a0704d566BF2C8" # Balancer V2 Vault (0% Fee)
UNISWAP_V3_ROUTER          = "0xE592427A0AEce92De3Edee1F18E0157C05861564" # Uniswap V3 SwapRouter
CAMELOT_ROUTER_V2          = "0xc873fEcbd354f5A56E00E710B90EF4201db2448d" # Camelot V2 Router
SUSHISWAP_V3_ROUTER        = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506" # SushiSwap V3 Router
ARBITRUM_CHAIN_ID          = 42161

def save_contract_to_env(contract_addr: str):
    """Persists FLASH_LOAN_CONTRACT_ADDRESS to .env file."""
    env_path = os.path.join(root_dir, ".env")
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            if line.strip().startswith("FLASH_LOAN_CONTRACT_ADDRESS="):
                new_lines.append(f"FLASH_LOAN_CONTRACT_ADDRESS={contract_addr}\n")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"\n# SuperSmart Flash Loan Smart Contract V2 (Arbitrum One)\nFLASH_LOAN_CONTRACT_ADDRESS={contract_addr}\n")
        
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    else:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"FLASH_LOAN_CONTRACT_ADDRESS={contract_addr}\n")
            
    os.environ["FLASH_LOAN_CONTRACT_ADDRESS"] = contract_addr
    keeper_relayer.keeper_engine.contract_address = contract_addr

def deploy_v2_arbitrum_contract() -> dict:
    """Deploys SuperSmartFlashLoanArbitrageV2 contract to Arbitrum One using Keeper wallet."""
    engine = keeper_relayer.keeper_engine
    status = engine.get_status_overview()

    print("=" * 75)
    print("  ARBITRUM ONE SUPERSMART FLASH LOAN V2 CONTRACT DEPLOYMENT")
    print("=" * 75)
    print(f"• Keeper Wallet:  {status['keeper_address']}")
    print(f"• Gas Balance:    {status['arbitrum_gas_eth']} ETH (~${status['gas_usd_est']} USD)")
    print(f"• Is Funded:      {status['is_funded']}")

    if not status["is_funded"] or status["arbitrum_gas_eth"] < 0.0001:
        msg = f"Insufficient gas: {status['arbitrum_gas_eth']} ETH. Need at least 0.0002 ETH."
        print(f"\n❌ {msg}")
        return {"success": False, "error": msg}

    json_path = os.path.join(os.path.dirname(__file__), "SuperSmartFlashLoanArbitrageV2.json")
    if not os.path.exists(json_path):
        msg = f"Artifact not found: {json_path}. Compiling now..."
        print(f"⚙️ {msg}")
        import solcx
        solcx.install_solc('0.8.20')
        sol_path = os.path.join(os.path.dirname(__file__), "SuperSmartFlashLoanArbitrageV2.sol")
        with open(sol_path, 'r', encoding='utf-8') as f:
            src = f.read()
        compiled = solcx.compile_source(src, output_values=['abi', 'bin'], solc_version='0.8.20', optimize=True, optimize_runs=200)
        c_data = compiled['<stdin>:SuperSmartFlashLoanArbitrageV2']
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({'contractName': 'SuperSmartFlashLoanArbitrageV2', 'abi': c_data['abi'], 'bytecode': c_data['bin']}, f, indent=2)

    with open(json_path, "r", encoding="utf-8") as f:
        artifact = json.load(f)

    abi = artifact["abi"]
    bytecode = artifact["bytecode"]

    w3 = engine.w3
    if not w3 or not w3.is_connected():
        msg = "Failed to connect to Arbitrum One RPC cluster."
        print(f"\n❌ {msg}")
        return {"success": False, "error": msg}

    keeper_addr = Web3.to_checksum_address(status["keeper_address"])
    keeper_privkey = engine.keeper_private_key
    if not keeper_privkey:
        msg = "Keeper private key not available for signing."
        print(f"\n❌ {msg}")
        return {"success": False, "error": msg}

    print("\n📦 Initializing Contract Factory with Constructor Parameters:")
    print(f"  1. Aave V3 Provider:     {AAVE_V3_ADDRESSES_PROVIDER}")
    print(f"  2. Balancer V2 Vault:    {BALANCER_V2_VAULT} (0% Flash Loan Fee)")
    print(f"  3. Uniswap V3 Router:    {UNISWAP_V3_ROUTER}")
    print(f"  4. Camelot V2 Router:    {CAMELOT_ROUTER_V2}")
    print(f"  5. SushiSwap V3 Router:  {SUSHISWAP_V3_ROUTER}")

    contract_factory = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(keeper_addr, "pending")
    gas_price = w3.eth.gas_price

    construct_txn = contract_factory.constructor(
        Web3.to_checksum_address(AAVE_V3_ADDRESSES_PROVIDER),
        Web3.to_checksum_address(BALANCER_V2_VAULT),
        Web3.to_checksum_address(UNISWAP_V3_ROUTER),
        Web3.to_checksum_address(CAMELOT_ROUTER_V2),
        Web3.to_checksum_address(SUSHISWAP_V3_ROUTER)
    ).build_transaction({
        'from': keeper_addr,
        'nonce': nonce,
        'gasPrice': int(gas_price * 1.15),
        'chainId': ARBITRUM_CHAIN_ID
    })

    try:
        est_gas = w3.eth.estimate_gas(construct_txn)
        construct_txn['gas'] = int(est_gas * 1.20)
    except Exception as e:
        print(f"⚠️ Gas estimate warning: {e}. Using fallback 2,500,000 gas limit.")
        construct_txn['gas'] = 2500000

    est_cost_eth = (construct_txn['gas'] * construct_txn['gasPrice']) / (10 ** 18)
    print(f"⚡ Estimated Gas Limit: {construct_txn['gas']}")
    print(f"⚡ Gas Price:          {construct_txn['gasPrice'] / 10**9:.3f} Gwei")
    print(f"⚡ Estimated Cost:       {est_cost_eth:.6f} ETH (~${est_cost_eth * 2420.0:.2f} USD)")

    print("\n🚀 Signing and broadcasting deployment transaction to Arbitrum One...")
    signed_txn = w3.eth.account.sign_transaction(construct_txn, private_key=keeper_privkey)
    raw_bytes = getattr(signed_txn, 'rawTransaction', getattr(signed_txn, 'raw_transaction', None))
    tx_hash = w3.eth.send_raw_transaction(raw_bytes)
    tx_hash_hex = tx_hash.hex()
    print(f"📡 Broadcasted! Tx Hash: {tx_hash_hex}")
    print(f"🔗 Arbiscan Pending: https://arbiscan.io/tx/{tx_hash_hex}")

    print("⏳ Waiting for Arbitrum One block inclusion receipt...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    if receipt.get("status") == 1:
        deployed_addr = Web3.to_checksum_address(receipt.contractAddress)
        gas_used = receipt.get("gasUsed", 0)
        actual_cost_eth = (gas_used * construct_txn['gasPrice']) / (10 ** 18)
        print("\n" + "🎉" * 35)
        print("  SUPER SMART FLASH LOAN V2 DEPLOYED SUCCESSFULLY ON ARBITRUM ONE!")
        print("🎉" * 35)
        print(f"• Contract Address: {deployed_addr}")
        print(f"• Transaction Hash: {tx_hash_hex}")
        print(f"• Gas Used:         {gas_used}")
        print(f"• Actual Cost:      {actual_cost_eth:.6f} ETH (~${actual_cost_eth * 2420.0:.2f} USD)")
        print(f"• Arbiscan Link:    https://arbiscan.io/address/{deployed_addr}")

        # Save to .env and deployed record
        save_contract_to_env(deployed_addr)
        print(f"💾 Updated FLASH_LOAN_CONTRACT_ADDRESS={deployed_addr} in .env!")

        deployed_record = {
            "contract_name": "SuperSmartFlashLoanArbitrageV2",
            "contract_address": deployed_addr,
            "tx_hash": tx_hash_hex,
            "deployer": keeper_addr,
            "gas_used": gas_used,
            "cost_eth": actual_cost_eth,
            "timestamp": int(time.time()),
            "network": "Arbitrum One",
            "chain_id": ARBITRUM_CHAIN_ID,
            "balancer_vault": BALANCER_V2_VAULT,
            "aave_provider": AAVE_V3_ADDRESSES_PROVIDER
        }
        rec_path = os.path.join(os.path.dirname(__file__), "SuperSmartFlashLoanArbitrageV2_deployed.json")
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(deployed_record, f, indent=2)

        return {
            "success": True,
            "contract_address": deployed_addr,
            "tx_hash": tx_hash_hex,
            "explorer_url": f"https://arbiscan.io/address/{deployed_addr}",
            "gas_used": gas_used,
            "cost_eth": actual_cost_eth
        }
    else:
        print(f"\n❌ Deployment transaction failed or reverted. Receipt: {receipt}")
        return {"success": False, "error": "Transaction reverted on Arbitrum One", "receipt": receipt}

if __name__ == "__main__":
    deploy_v2_arbitrum_contract()
