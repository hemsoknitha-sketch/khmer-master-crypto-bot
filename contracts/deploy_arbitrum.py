"""
Khmer Master Crypto / Apex TURBO AGI v13.00
ARBITRUM ONE FLASH LOAN CONTRACT DEPLOYMENT HELPER
================================================================================
Deploys AaveFlashLoanArbitrage.sol to Arbitrum One Mainnet using the Keeper Wallet.
================================================================================
"""

import os
import sys
from web3 import Web3
import keeper_relayer

# Arbitrum One Constants
AAVE_V3_ADDRESSES_PROVIDER = "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb" # Aave V3 Arbitrum
UNISWAP_V3_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"          # Uniswap V3 SwapRouter
CAMELOT_ROUTER_V2 = "0xc873fEcbd354f5A56E00E710B90EF4201db2448d"          # Camelot V2 Router

def check_deployment_prerequisites():
    status = keeper_relayer.keeper_engine.get_status_overview()
    print("=" * 70)
    print("  ARBITRUM ONE AAVE V3 FLASH LOAN CONTRACT DEPLOYMENT STATUS")
    print("=" * 70)
    print(f"• Keeper Wallet Address: {status['keeper_address']}")
    print(f"• Arbitrum Gas Balance:  {status['arbitrum_gas_eth']} ETH (~${status['gas_usd_est']} USD)")
    print(f"• Is Funded with Gas:    {status['is_funded']}")
    print(f"• RPC Connection Live:   {status['rpc_connected']}")
    print(f"• Active Contract:       {status['contract_address']}")
    print("-" * 70)

    if not status["is_funded"]:
        print("\n⚠️ DEPLOYMENT NOTICE:")
        print(f"Please deposit at least 0.002 to 0.005 ETH (~$5 to $12 USD) on ARBITRUM ONE network")
        print(f"to the Keeper Wallet address above:")
        print(f"  👉 {status['keeper_address']}")
        print("\nOnce funded, run this script to deploy AaveFlashLoanArbitrage.sol to Arbitrum One!")
        return False
    
    print("\n✅ Keeper Wallet is FUNDED and ready for deployment!")
    return True

if __name__ == "__main__":
    check_deployment_prerequisites()
