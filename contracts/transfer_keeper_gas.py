"""
Khmer Master Crypto - Arbitrum One Gas Sweeper / Transfer Engine
================================================================
Transfers ETH gas from Keeper Wallet (0x3D1eef...) to Owner Wallet (0xe3833d...)
Can run directly on Google Cloud VPS or on local machine.
"""

import os
import sys
import requests
from web3 import Web3
from eth_account import Account

sys.stdout.reconfigure(encoding='utf-8')

ARBITRUM_RPC = "https://arb1.arbitrum.io/rpc"
DEFAULT_TARGET_RECIPIENT = "0xe3833dDaf7fb92b3F0e0a57169C98bd9482e9560"

def get_candidate_keys():
    keys = []
    # 1. Check environment
    k = os.getenv("KEEPER_RELAYER_PRIVATE_KEY", "").strip()
    if k:
        keys.append(k if k.startswith("0x") else "0x" + k)
    
    # 2. Check .env in current directory or /opt/khmer-master-crypto-bot/.env
    env_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        os.path.join(os.getcwd(), ".env"),
        "/opt/khmer-master-crypto-bot/.env"
    ]
    for p in env_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("KEEPER_RELAYER_PRIVATE_KEY") and "=" in line:
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val and not val.startswith("PASTE_"):
                                fmt_v = val if val.startswith("0x") else "0x" + val
                                if fmt_v not in keys:
                                    keys.append(fmt_v)
            except Exception:
                pass
    return keys

def sweep_gas_to_owner(recipient: str = DEFAULT_TARGET_RECIPIENT, explicit_private_key: str = None):
    print("=" * 65)
    print("  KHMER MASTER CRYPTO - ARBITRUM GAS TRANSFER / SWEEPER")
    print("=" * 65)

    w3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC, request_kwargs={'timeout': 10}))
    if not w3.is_connected():
        print("❌ Cannot connect to Arbitrum One RPC.")
        return False

    recipient = Web3.to_checksum_address(recipient)
    print(f"🎯 Target Destination Wallet: {recipient}")

    keys_to_test = [explicit_private_key] if explicit_private_key else get_candidate_keys()

    target_sender = None
    target_key = None
    max_balance = 0

    for k in keys_to_test:
        if not k:
            continue
        try:
            acct = Account.from_key(k)
            bal = w3.eth.get_balance(acct.address)
            print(f"🔍 Checked Account: {acct.address} | Balance: {w3.from_wei(bal, 'ether'):.6f} ETH")
            if bal > max_balance:
                max_balance = bal
                target_sender = acct
                target_key = k
        except Exception:
            continue

    if not target_sender or max_balance == 0:
        print("\n❌ គ្មានកាបូបណាដែលមាន Gas ETH ត្រូវបានរកឃើញឡើយ!")
        print("💡 សូមប្រាកដថា Private Key នៃកាបូប 0x3D1eef... ត្រូវបានបញ្ចូលត្រឹមត្រូវ។")
        return False

    print("\n" + "-" * 65)
    print(f"💎 Selected Sender Wallet: {target_sender.address}")
    bal_eth = float(w3.from_wei(max_balance, 'ether'))
    print(f"💰 Current Gas Balance:   {bal_eth:.6f} ETH (~${bal_eth * 2550:.2f} USD)")

    if target_sender.address.lower() == recipient.lower():
        print("ℹ️ កាបូបប្រភព និងកាបូបគោលដៅ គឺជាកាបូបតែមួយ (0xe3833d...). មិនចាំបាច់ផ្ទេរទេ!")
        return True

    # Calculate gas cost
    gas_limit = 21000
    gas_price = w3.eth.gas_price
    tx_cost = gas_limit * gas_price

    transfer_amount = max_balance - tx_cost
    if transfer_amount <= 0:
        print("❌ សមតុល្យ ETH មិនគ្រប់គ្រាន់សម្រាប់បង់ថ្លៃ Gas ក្នុងការផ្ទេរឡើយ!")
        return False

    print(f"⛽ Gas Limit: 21,000 | Gas Price: {w3.from_wei(gas_price, 'gwei'):.4f} Gwei")
    print(f"💸 Sending Amount: {w3.from_wei(transfer_amount, 'ether'):.6f} ETH to {recipient}")

    nonce = w3.eth.get_transaction_count(target_sender.address, 'pending')
    tx = {
        'to': recipient,
        'value': transfer_amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': 42161
    }

    signed_tx = w3.eth.account.sign_transaction(tx, target_key)
    raw_tx = getattr(signed_tx, 'raw_transaction', None) or getattr(signed_tx, 'rawTransaction')

    print("🚀 Broadcasting transaction to Arbitrum One Mainnet...")
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    hex_hash = tx_hash.hex()
    if not hex_hash.startswith("0x"):
        hex_hash = "0x" + hex_hash

    print("\n" + "=" * 65)
    print("🎉 ជោគជ័យ! ប្រតិបត្តិការផ្ទេរ Gas ត្រូវបានបញ្ជូនទៅកាន់ Arbitrum One!")
    print(f"🔗 Tx Hash:      {hex_hash}")
    print(f"👉 Arbiscan URL: https://arbiscan.io/tx/{hex_hash}")
    print("=" * 65)

    print("⏳ Waiting for Arbitrum block confirmation (2-5 seconds)...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
    if receipt.status == 1:
        print("✅ BLOCK CONFIRMED! Gas ត្រូវបានផ្ទេរចូលកាបូប 0xe3833d... ដោយជោគជ័យ ១០០%!")
        return True
    else:
        print("❌ Transaction Reverted!")
        return False

if __name__ == "__main__":
    key_arg = sys.argv[1] if len(sys.argv) > 1 else None
    dest_arg = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_TARGET_RECIPIENT
    sweep_gas_to_owner(recipient=dest_arg, explicit_private_key=key_arg)
