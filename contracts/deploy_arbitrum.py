"""
Khmer Master Crypto / Apex TURBO AGI v13.00
ARBITRUM ONE FLASH LOAN CONTRACT DEPLOYMENT HELPER
================================================================================
Deploys AaveFlashLoanArbitrage.sol to Arbitrum One Mainnet using the Keeper Wallet.
================================================================================
"""

import os
import sys

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

import json
import time
from web3 import Web3
import keeper_relayer

# Arbitrum One Constants
AAVE_V3_ADDRESSES_PROVIDER = "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb" # Aave V3 Arbitrum
UNISWAP_V3_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"          # Uniswap V3 SwapRouter
CAMELOT_ROUTER_V2 = "0xc873fEcbd354f5A56E00E710B90EF4201db2448d"          # Camelot V2 Router
ARBITRUM_CHAIN_ID = 42161

def save_contract_to_env(contract_addr: str):
    """Persists FLASH_LOAN_CONTRACT_ADDRESS to .env file."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
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
            new_lines.append(f"\n# Aave V3 Flash Loan Smart Contract (Arbitrum One)\nFLASH_LOAN_CONTRACT_ADDRESS={contract_addr}\n")
        
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    else:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"FLASH_LOAN_CONTRACT_ADDRESS={contract_addr}\n")
            
    os.environ["FLASH_LOAN_CONTRACT_ADDRESS"] = contract_addr
    keeper_relayer.keeper_engine.contract_address = contract_addr

def deploy_arbitrum_contract() -> dict:
    """Deploys AaveFlashLoanArbitrage contract to Arbitrum One using Keeper wallet."""
    engine = keeper_relayer.keeper_engine
    status = engine.get_status_overview()

    print("=" * 70)
    print("  ARBITRUM ONE AAVE V3 FLASH LOAN CONTRACT DEPLOYMENT")
    print("=" * 70)
    print(f"• Keeper Wallet:  {status['keeper_address']}")
    print(f"• Gas Balance:    {status['arbitrum_gas_eth']} ETH (~${status['gas_usd_est']} USD)")
    print(f"• Is Funded:      {status['is_funded']}")

    if not status["is_funded"] or status["arbitrum_gas_eth"] < 0.0008:
        msg = f"Insufficient gas: {status['arbitrum_gas_eth']} ETH. Need at least 0.001 ETH."
        print(f"\n❌ {msg}")
        return {"success": False, "error": msg}

    # Load compiled JSON artifact
    json_path = os.path.join(os.path.dirname(__file__), "AaveFlashLoanArbitrage.json")
    if not os.path.exists(json_path):
        msg = f"Artifact not found: {json_path}. Please compile contract first."
        print(f"\n❌ {msg}")
        return {"success": False, "error": msg}

    with open(json_path, "r", encoding="utf-8") as f:
        artifact = json.load(f)

    abi = artifact["abi"]
    bytecode = artifact["bytecode"]

    w3 = engine.w3
    if not w3 or not w3.is_connected():
        w3 = Web3(Web3.HTTPProvider(keeper_relayer.ARBITRUM_RPC_PRIMARY))

    print("\n📡 Connected to Arbitrum One RPC. Preparing deployment transaction...")
    contract_factory = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(engine.keeper_address)
    gas_price = w3.eth.gas_price

    tx = contract_factory.constructor(
        Web3.to_checksum_address(AAVE_V3_ADDRESSES_PROVIDER),
        Web3.to_checksum_address(UNISWAP_V3_ROUTER),
        Web3.to_checksum_address(CAMELOT_ROUTER_V2)
    ).build_transaction({
        'from': engine.keeper_address,
        'nonce': nonce,
        'gasPrice': int(gas_price * 1.25),
        'chainId': ARBITRUM_CHAIN_ID
    })

    print(f"⛽ Estimated Gas Price: {gas_price / 10**9:.3f} Gwei | Nonce: {nonce}")
    print("✍️ Signing deployment transaction with Keeper Private Key...")
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=engine.keeper_private_key)

    print("🚀 Broadcasting deployment transaction to Arbitrum One...")
    raw_tx = getattr(signed_tx, 'raw_transaction', getattr(signed_tx, 'rawTransaction', None))
    tx_hash_bytes = w3.eth.send_raw_transaction(raw_tx)
    tx_hash = w3.to_hex(tx_hash_bytes)
    print(f"🔗 Tx Hash: {tx_hash}")
    print(f"👉 Explorer: https://arbiscan.io/tx/{tx_hash}")

    print("⏳ Waiting for Arbitrum block confirmation (usually 2-5 seconds)...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    receipt_status = getattr(receipt, 'status', None) or receipt.get('status')
    if receipt_status == 1:
        deployed_addr = getattr(receipt, 'contractAddress', None) or receipt.get('contractAddress')
        gas_used = getattr(receipt, 'gasUsed', None) or receipt.get('gasUsed')
        print("\n" + "=" * 70)
        print("  🎉 SMART CONTRACT DEPLOYED SUCCESSFULLY TO ARBITRUM ONE! 🎉")
        print("=" * 70)
        print(f"• Contract Address: {deployed_addr}")
        print(f"• Arbiscan URL:     https://arbiscan.io/address/{deployed_addr}")
        print(f"• Gas Used:         {gas_used}")
        print("=" * 70)
        
        save_contract_to_env(deployed_addr)
        print("💾 Saved contract address to .env successfully!")
        return {
            "success": True,
            "contract_address": deployed_addr,
            "tx_hash": tx_hash,
            "arbiscan_url": f"https://arbiscan.io/address/{deployed_addr}",
            "gas_used": receipt.gasUsed
        }
    else:
        print("\n❌ Deployment transaction reverted on Arbitrum One!")
        return {"success": False, "error": "Transaction reverted by network", "tx_hash": tx_hash}

if __name__ == "__main__":
    deploy_arbitrum_contract()
