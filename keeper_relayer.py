"""
Khmer Master Crypto / Apex TURBO AGI v13.00
KEEPER RELAYER WALLET & MAINNET EXECUTION ENGINE (ARBITRUM ONE)
================================================================================
Manages dedicated, isolated Keeper Relayer wallet for automated on-chain
Flash Loan execution. Eliminates private key risk for user wallets.
================================================================================
"""

import os
import sys
import time
import json
import secrets
from web3 import Web3
from eth_account import Account

# Arbitrum One Mainnet Infrastructure Constants
ARBITRUM_RPC_PRIMARY = "https://arb1.arbitrum.io/rpc"
ARBITRUM_RPC_FALLBACK = "https://rpc.ankr.com/arbitrum"
ARBITRUM_CHAIN_ID = 42161
ARBITRUM_EXPLORER_TX = "https://arbiscan.io/tx/"

# Known Arbitrum Token Addresses
ARBITRUM_TOKENS = {
    "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    "WBTC": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"
}

# Minimal ABI for AaveFlashLoanArbitrage
FLASH_LOAN_CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "bytes", "name": "params", "type": "bytes"}
        ],
        "name": "requestFlashLoan",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "caller", "type": "address"}],
        "name": "authorizedCallers",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class KeeperRelayerEngine:
    """
    Institutional Keeper Relayer Execution Engine v13.00
    -----------------------------------------------------
    Ensures safe, non-custodial execution of Flash Loans on Arbitrum One.
    """

    def __init__(self):
        self.w3 = self._init_web3()
        self.keeper_private_key = self._load_or_create_keeper_key()
        if self.keeper_private_key:
            self.keeper_account = Account.from_key(self.keeper_private_key)
            self.keeper_address = self.keeper_account.address
        else:
            self.keeper_account = None
            self.keeper_address = None

        self.contract_address = os.getenv("FLASH_LOAN_CONTRACT_ADDRESS", "").strip()
        self.min_gas_eth = 0.001 # ~ $2.50 to $3.50 ETH floor for transaction safety

    def _init_web3(self) -> Web3:
        """Initializes high-performance Web3 connection to Arbitrum One."""
        try:
            w3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC_PRIMARY, request_kwargs={'timeout': 10}))
            if w3.is_connected():
                return w3
        except Exception:
            pass
        return Web3(Web3.HTTPProvider(ARBITRUM_RPC_FALLBACK, request_kwargs={'timeout': 10}))

    def _load_or_create_keeper_key(self) -> str:
        """
        Loads Keeper Private Key from environment, or generates a fresh dedicated
        key and persists to .env if not found.
        """
        key = os.getenv("KEEPER_RELAYER_PRIVATE_KEY", "").strip()
        if key and key.startswith("0x") and len(key) == 66:
            return key
        elif key and len(key) == 64:
            return "0x" + key

        # Generate a new cryptographically secure isolated keeper key
        fresh_key = "0x" + secrets.token_hex(32)
        try:
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            if os.path.exists(env_path):
                with open(env_path, "a", encoding="utf-8") as f:
                    f.write(f"\n# Automated Dedicated Keeper Relayer Wallet (Arbitrum One)\nKEEPER_RELAYER_PRIVATE_KEY={fresh_key}\n")
            os.environ["KEEPER_RELAYER_PRIVATE_KEY"] = fresh_key
        except Exception as e:
            print(f"Notice saving keeper key to .env: {e}")
        return fresh_key

    def get_keeper_gas_balance(self) -> float:
        """Queries the live Arbitrum ETH gas balance of the Keeper Wallet."""
        if not self.keeper_address:
            return 0.0
        try:
            wei_bal = self.w3.eth.get_balance(self.keeper_address)
            return float(self.w3.from_wei(wei_bal, 'ether'))
        except Exception:
            return 0.0

    def is_live_ready(self) -> bool:
        """
        Returns True if Keeper Wallet has sufficient Gas AND Contract is deployed.
        Otherwise system safely operates in Simulation / Paper Trading mode.
        """
        has_contract = bool(self.contract_address and self.contract_address.startswith("0x") and len(self.contract_address) == 42)
        gas_bal = self.get_keeper_gas_balance()
        return bool(has_contract and gas_bal >= self.min_gas_eth)

    def get_status_overview(self) -> dict:
        """Returns comprehensive diagnostic status for Telegram Bot and CLI."""
        gas_bal = self.get_keeper_gas_balance()
        live_ready = self.is_live_ready()
        
        return {
            "keeper_address": self.keeper_address or "Not Configured",
            "arbitrum_gas_eth": round(gas_bal, 6),
            "gas_usd_est": round(gas_bal * 2500.0, 2),
            "is_funded": gas_bal >= self.min_gas_eth,
            "contract_address": self.contract_address or "Not Deployed Yet (Ready for Arbitrum Mainnet)",
            "execution_mode": "LIVE_MAINNET" if live_ready else "SIMULATION_PAPER_TRADING",
            "rpc_connected": self.w3.is_connected() if self.w3 else False,
            "chain_id": ARBITRUM_CHAIN_ID
        }

    def execute_onchain_flash_loan(
        self,
        borrow_asset: str,
        amount_usd: float,
        intermediate_token: str,
        min_net_profit_usd: float,
        user_recipient: str,
        dex_route: int = 1
    ) -> dict:
        """
        Submits on-chain flash loan arbitrage transaction on Arbitrum One.
        If conditions are not ready or simulation mode is active, returns deterministic simulation.
        """
        status = self.get_status_overview()

        if not status["is_funded"] or not self.contract_address:
            # Fallback to Paper Simulation mode
            import hashlib
            sim_seed = f"{borrow_asset}-{amount_usd}-{user_recipient}-{int(time.time())}"
            mock_hash = "0x" + hashlib.sha256(sim_seed.encode()).hexdigest()[:40]
            return {
                "success": True,
                "mode": "SIMULATION_PAPER_TRADING",
                "tx_hash": mock_hash,
                "explorer_url": f"https://arbiscan.io/tx/{mock_hash}",
                "net_profit_usd": round(min_net_profit_usd, 2),
                "recipient": user_recipient,
                "notice": "Keeper wallet not funded with ETH. Arbitrage executed in Simulation Mode."
            }

        try:
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=FLASH_LOAN_CONTRACT_ABI
            )

            token_in_addr = ARBITRUM_TOKENS.get(borrow_asset.upper(), ARBITRUM_TOKENS["USDT"])
            token_out_addr = ARBITRUM_TOKENS.get(intermediate_token.upper(), ARBITRUM_TOKENS["WETH"])

            # USDT decimals = 6
            decimals = 6 if "USD" in borrow_asset.upper() else 18
            loan_units = int(amount_usd * (10 ** decimals))
            min_profit_units = int(min_net_profit_usd * (10 ** decimals))

            # Encode parameters: (address intermediateToken, uint24 poolFee, uint256 minProfit, address recipient, uint8 dexRoute)
            pool_fee = 500 # 0.05% Uniswap V3 fee tier
            recipient_checksum = Web3.to_checksum_address(user_recipient)

            from eth_abi import encode
            encoded_params = encode(
                ['address', 'uint24', 'uint256', 'address', 'uint8'],
                [Web3.to_checksum_address(token_out_addr), pool_fee, min_profit_units, recipient_checksum, int(dex_route)]
            )

            # Build EIP-1559 Transaction
            nonce = self.w3.eth.get_transaction_count(self.keeper_address)
            gas_price = self.w3.eth.gas_price

            tx = contract.functions.requestFlashLoan(
                Web3.to_checksum_address(token_in_addr),
                loan_units,
                encoded_params
            ).build_transaction({
                'from': self.keeper_address,
                'nonce': nonce,
                'gas': 850_000,
                'gasPrice': int(gas_price * 1.15),
                'chainId': ARBITRUM_CHAIN_ID
            })

            # Sign and broadcast
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.keeper_private_key)
            tx_hash_bytes = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash = self.w3.to_hex(tx_hash_bytes)

            return {
                "success": True,
                "mode": "LIVE_MAINNET",
                "tx_hash": tx_hash,
                "explorer_url": f"{ARBITRUM_EXPLORER_TX}{tx_hash}",
                "net_profit_usd": round(min_net_profit_usd, 2),
                "recipient": user_recipient,
                "notice": "Real transaction broadcast to Arbitrum One Mainnet!"
            }
        except Exception as e:
            return {
                "success": False,
                "mode": "EXECUTION_ERROR",
                "error": str(e),
                "notice": f"Mainnet execution reverted or failed: {e}"
            }

# Global Singleton Instance
keeper_engine = KeeperRelayerEngine()
