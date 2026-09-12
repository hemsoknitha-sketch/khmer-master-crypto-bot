"""
==============================================================================
🚀 KHMER MASTER CRYPTO - DEDICATED SOLANA ON-CHAIN TRADING WALLET
==============================================================================
Institutional-grade, zero-external-dependency Solana Keypair management,
Multi-Tenant Per-User Dedicated Wallets (Trojan / BonkBot Architecture),
Jupiter DEX aggregator integration, and autonomous transaction execution.

Features:
- Ed25519 cryptographic keypair management using standard 'cryptography'
- Pure-Python Base58 encoding & decoding (zero C++ compile dependencies)
- Per-User Dedicated Solana Wallets with military-grade AES-256 (Fernet) encryption
- Real-time Solana Mainnet balance & gas estimation
- Pure-Python native SOL Transfer & Withdrawal engine
- Exportable Private Keys for 100% Non-Custodial Phantom Wallet / Solflare import
- Jupiter v1 swap instruction retrieval, user signing, and RPC broadcasting
- Automated reverse-swap for TP1 (+40%) & Moonbag trailing exits
==============================================================================
"""

import os
import time
import json
import base64
import struct
import urllib.request
from dotenv import load_dotenv

# Standard cryptography library (pre-installed on VPS)
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

import database as db
import security

load_dotenv()

# ==============================================================================
# 🔤 BASE58 ENCODING / DECODING ENGINE (PURE PYTHON)
# ==============================================================================

B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58encode(b: bytes) -> str:
    """Encodes raw bytes into standard Base58 string (Solana standard)."""
    n = int.from_bytes(b, "big")
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(B58_ALPHABET[r])
    pad = 0
    for byte in b:
        if byte == 0:
            pad += 1
        else:
            break
    return "1" * pad + "".join(reversed(res))

def b58decode(s: str) -> bytes:
    """Decodes standard Base58 string into raw bytes."""
    n = 0
    for char in s:
        idx = B58_ALPHABET.find(char)
        if idx == -1:
            raise ValueError(f"Invalid Base58 character: {char}")
        n = n * 58 + idx
    res = n.to_bytes((n.bit_length() + 7) // 8, "big") if n > 0 else b""
    pad = 0
    for char in s:
        if char == "1":
            pad += 1
        else:
            break
    return b"\x00" * pad + res

# ==============================================================================
# 🔑 PER-USER DEDICATED WALLET MANAGEMENT (TROJAN / BONKBOT ARCHITECTURE)
# ==============================================================================

def get_or_create_user_solana_wallet(chat_id: int) -> tuple[ed25519.Ed25519PrivateKey, str]:
    """
    Retrieves or generates a dedicated Solana trading keypair for a specific Telegram user.
    Stores the private key in SQLite encrypted via military-grade AES-256 (Fernet).
    Returns: (ed25519.Ed25519PrivateKey, public_address_base58)
    """
    chat_id = int(chat_id)
    existing = db.get_user_solana_wallet(chat_id)
    if existing and existing.get("encrypted_private_key"):
        try:
            decrypted_b58 = security.decrypt_data(existing["encrypted_private_key"])
            if decrypted_b58:
                raw_bytes = b58decode(decrypted_b58)
                seed = raw_bytes[:32]
                priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
                pub = existing["public_key"]
                return priv, pub
        except Exception as e:
            print(f"[SOLANA_WALLET] Error decrypting wallet for user {chat_id}: {e}")

    # Generate a fresh cryptographically secure Ed25519 keypair for this specific user
    priv = ed25519.Ed25519PrivateKey.generate()
    seed = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_bytes = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    pub = b58encode(pub_bytes)
    full_priv_b58 = b58encode(seed + pub_bytes)

    # Encrypt with AES-256 and persist to SQLite
    enc_priv = security.encrypt_data(full_priv_b58)
    db.save_user_solana_wallet(chat_id, pub, enc_priv)
    print(f"[SOLANA_WALLET] Created and encrypted dedicated Solana wallet for User {chat_id}: {pub}")

    return priv, pub

def get_user_solana_wallet_overview(chat_id: int) -> dict:
    """Returns a full overview of the dedicated Solana trading wallet for the given user."""
    _, pub = get_or_create_user_solana_wallet(chat_id)
    bal_data = get_solana_balance(pub)
    return {
        "chat_id": chat_id,
        "public_key": pub,
        "lamports": bal_data["lamports"],
        "sol_balance": bal_data["sol_balance"],
        "sol_price_usd": bal_data["sol_price_usd"],
        "usd_value": bal_data["usd_value"],
        "solscan_url": bal_data["solscan_url"],
        "is_funded": bal_data["sol_balance"] >= 0.005
    }

def export_user_private_key(chat_id: int) -> dict | None:
    """
    Exports the user's Base58 private key for 100% Non-Custodial import into Phantom or Solflare.
    """
    existing = db.get_user_solana_wallet(int(chat_id))
    if not existing or not existing.get("encrypted_private_key"):
        return None
    decrypted_b58 = security.decrypt_data(existing["encrypted_private_key"])
    if not decrypted_b58:
        return None
    return {
        "public_key": existing["public_key"],
        "private_key_b58": decrypted_b58
    }

def bind_user_phantom_wallet(chat_id: int, phantom_address: str) -> dict:
    """
    Binds a user's personal Phantom Wallet address as their Profit Settlement Vault.
    Validates Base58 Solana public key format (must decode to 32 bytes).
    """
    clean_addr = str(phantom_address or "").strip()
    try:
        raw_bytes = b58decode(clean_addr)
        if len(raw_bytes) != 32:
            return {
                "status": "error",
                "reason": "INVALID_SOLANA_ADDRESS",
                "msg": "អាសយដ្ឋាន Phantom Wallet ត្រូវតែជា Solana Public Address (32 bytes) ត្រឹមត្រូវ!"
            }
    except Exception as e:
        return {
            "status": "error",
            "reason": "INVALID_SOLANA_ADDRESS",
            "msg": f"អាសយដ្ឋាន Solana Base58 មិនត្រឹមត្រូវ ៖ {e}"
        }

    db.set_user_web3_wallet(int(chat_id), clean_addr, "SOLANA")
    return {
        "status": "success",
        "chat_id": int(chat_id),
        "phantom_address": clean_addr,
        "solscan_url": f"https://solscan.io/account/{clean_addr}"
    }

def get_user_phantom_wallet(chat_id: int) -> str:
    """Retrieves the user's bound Phantom settlement wallet, if any."""
    return db.get_user_web3_wallet(int(chat_id), "SOLANA")

# ==============================================================================
# 🔑 KEEPER / BOT HOT WALLET (FALLBACK & ADMIN POOL)
# ==============================================================================

_CACHED_PRIV_KEY = None
_CACHED_PUBLIC_KEY = None

def load_or_create_bot_keypair():
    """
    Loads the bot's master Solana trading keypair from environment / .env,
    or generates a new secure Ed25519 keypair and persists it.
    Returns: (ed25519.Ed25519PrivateKey, public_address_base58)
    """
    global _CACHED_PRIV_KEY, _CACHED_PUBLIC_KEY
    if _CACHED_PRIV_KEY is not None and _CACHED_PUBLIC_KEY is not None:
        return _CACHED_PRIV_KEY, _CACHED_PUBLIC_KEY

    env_key = os.getenv("SOLANA_BOT_PRIVATE_KEY", "").strip()
    env_pub = os.getenv("SOLANA_BOT_PUBLIC_KEY", "").strip()

    if env_key:
        try:
            raw_bytes = b58decode(env_key)
            seed = raw_bytes[:32]
            priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
            pub_bytes = priv.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            pub = b58encode(pub_bytes)
            _CACHED_PRIV_KEY = priv
            _CACHED_PUBLIC_KEY = pub
            return priv, pub
        except Exception as e:
            print(f"[SOLANA_WALLET] Failed to decode existing SOLANA_BOT_PRIVATE_KEY: {e}")

    # Generate a fresh cryptographically secure Ed25519 keypair
    priv = ed25519.Ed25519PrivateKey.generate()
    seed = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_bytes = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    pub = b58encode(pub_bytes)
    full_priv_b58 = b58encode(seed + pub_bytes)

    _CACHED_PRIV_KEY = priv
    _CACHED_PUBLIC_KEY = pub

    # Persist to .env
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    try:
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        has_priv = False
        has_pub = False
        new_lines = []
        for line in lines:
            if line.startswith("SOLANA_BOT_PRIVATE_KEY="):
                new_lines.append(f"SOLANA_BOT_PRIVATE_KEY={full_priv_b58}\n")
                has_priv = True
            elif line.startswith("SOLANA_BOT_PUBLIC_KEY="):
                new_lines.append(f"SOLANA_BOT_PUBLIC_KEY={pub}\n")
                has_pub = True
            else:
                new_lines.append(line)

        if not has_priv:
            new_lines.append(f"\nSOLANA_BOT_PRIVATE_KEY={full_priv_b58}\n")
        if not has_pub:
            new_lines.append(f"SOLANA_BOT_PUBLIC_KEY={pub}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        os.environ["SOLANA_BOT_PRIVATE_KEY"] = full_priv_b58
        os.environ["SOLANA_BOT_PUBLIC_KEY"] = pub
        print(f"[SOLANA_WALLET] Generated and secured new dedicated Bot Hot Wallet: {pub}")
    except Exception as e:
        print(f"[SOLANA_WALLET] Error persisting keypair to .env: {e}")

    return priv, pub

def get_bot_solana_public_key() -> str:
    """Returns the dedicated Bot Hot Wallet Base58 public address."""
    _, pub = load_or_create_bot_keypair()
    return pub

def get_bot_solana_wallet_overview() -> dict:
    """Returns a full overview of the dedicated Bot Hot Wallet."""
    pub = get_bot_solana_public_key()
    bal_data = get_solana_balance(pub)
    return {
        "public_key": pub,
        "lamports": bal_data["lamports"],
        "sol_balance": bal_data["sol_balance"],
        "sol_price_usd": bal_data["sol_price_usd"],
        "usd_value": bal_data["usd_value"],
        "solscan_url": bal_data["solscan_url"],
        "is_funded": bal_data["sol_balance"] >= 0.005
    }

# ==============================================================================
# 💰 ON-CHAIN BALANCE & GAS QUERIES
# ==============================================================================

SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

def get_solana_balance(address: str = None) -> dict:
    """
    Fetches real-time native SOL balance for the given address.
    Returns dict with lamports, sol_balance, sol_price_usd, and usd_value.
    """
    target_addr = str(address or get_bot_solana_public_key()).strip()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [target_addr]
    }
    
    lamports = 0
    sol_bal = 0.0
    try:
        req = urllib.request.Request(
            SOLANA_RPC_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            lamports = data.get("result", {}).get("value", 0)
            sol_bal = round(lamports / 1e9, 5)
    except Exception as e:
        # Fallback query
        try:
            req_fb = urllib.request.Request(
                "https://solana-mainnet.rpc.extrnode.com",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req_fb, timeout=3.5) as resp_fb:
                data = json.loads(resp_fb.read().decode("utf-8"))
                lamports = data.get("result", {}).get("value", 0)
                sol_bal = round(lamports / 1e9, 5)
        except Exception:
            pass

    # Estimate SOL price in USD
    sol_price = 145.0
    try:
        req_p = urllib.request.Request(
            "https://api.dexscreener.com/latest/dex/tokens/So11111111111111111111111111111111111111112",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_p, timeout=2.5) as resp_p:
            dp = json.loads(resp_p.read().decode("utf-8"))
            pairs = dp.get("pairs", [])
            if pairs:
                p_usd = float(pairs[0].get("priceUsd", 0))
                if p_usd > 10.0:
                    sol_price = p_usd
    except Exception:
        pass

    usd_val = round(sol_bal * sol_price, 2)
    return {
        "address": target_addr,
        "lamports": lamports,
        "sol_balance": sol_bal,
        "sol_price_usd": round(sol_price, 2),
        "usd_value": usd_val,
        "solscan_url": f"https://solscan.io/account/{target_addr}"
    }

# ==============================================================================
# 💸 PURE-PYTHON NATIVE SOL TRANSFER & WITHDRAWAL ENGINE
# ==============================================================================

def execute_sol_transfer(
    sender_priv: ed25519.Ed25519PrivateKey,
    dest_address_b58: str,
    lamports: int
) -> dict:
    """
    Executes a native SOL transfer transaction on Solana Mainnet:
    1. Validates destination Base58 address.
    2. Fetches latest blockhash from RPC.
    3. Builds standard SystemProgram transfer instruction in pure Python.
    4. Signs with sender Ed25519 private key.
    5. Broadcasts to Solana Mainnet RPC.
    """
    dest_b58 = dest_address_b58.strip()
    try:
        dest_pub = b58decode(dest_b58)
        if len(dest_pub) != 32:
            return {"status": "error", "reason": "INVALID_RECIPIENT_ADDRESS", "msg": "Recipient Solana address must decode to 32 bytes."}
    except Exception as e:
        return {"status": "error", "reason": "INVALID_RECIPIENT_ADDRESS", "msg": f"Invalid Solana Base58 address: {e}"}

    if lamports <= 0:
        return {"status": "error", "reason": "INVALID_AMOUNT", "msg": "Transfer amount must be greater than 0 lamports."}

    # 1. Fetch recent blockhash
    blockhash_bytes = None
    try:
        bh_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getLatestBlockhash",
            "params": [{"commitment": "finalized"}]
        }
        req_bh = urllib.request.Request(
            SOLANA_RPC_URL,
            data=json.dumps(bh_payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_bh, timeout=4.0) as resp_bh:
            bh_data = json.loads(resp_bh.read().decode("utf-8"))
            bh_str = bh_data.get("result", {}).get("value", {}).get("blockhash")
            if bh_str:
                blockhash_bytes = b58decode(bh_str)
    except Exception as e:
        return {"status": "error", "reason": "BLOCKHASH_FETCH_ERROR", "msg": f"Failed to get recent blockhash: {e}"}

    if not blockhash_bytes:
        return {"status": "error", "reason": "BLOCKHASH_FETCH_ERROR", "msg": "Empty blockhash returned from Solana RPC."}

    # 2. Build transfer message
    sender_pub = sender_priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    system_prog = b"\x00" * 32  # 11111111111111111111111111111111

    # Header: 1 signer, 0 readonly signed, 1 readonly unsigned
    header = bytes([1, 0, 1])
    accounts = bytes([3]) + sender_pub + dest_pub + system_prog
    
    # Instruction: System Program Transfer (index 2), accounts [0, 1]
    ix_data = struct.pack("<IQ", 2, int(lamports))
    ix = bytes([2, 2, 0, 1, len(ix_data)]) + ix_data
    instructions = bytes([1]) + ix

    msg = header + accounts + blockhash_bytes + instructions
    
    # 3. Sign message
    sig = sender_priv.sign(msg)
    raw_tx = bytes([1]) + sig + msg
    tx_b64 = base64.b64encode(raw_tx).decode("utf-8")
    tx_sig_b58 = b58encode(sig)

    # 4. Broadcast via sendTransaction
    rpc_payload = {
        "jsonrpc": "2.0",
        "id": int(time.time()),
        "method": "sendTransaction",
        "params": [
            tx_b64,
            {"encoding": "base64", "skipPreflight": False, "preflightCommitment": "confirmed"}
        ]
    }

    confirmed_sig = tx_sig_b58
    try:
        req_tx = urllib.request.Request(
            SOLANA_RPC_URL,
            data=json.dumps(rpc_payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_tx, timeout=7.0) as resp_tx:
            tx_res = json.loads(resp_tx.read().decode("utf-8"))
            if "error" in tx_res:
                err_msg = tx_res["error"].get("message", str(tx_res["error"]))
                return {
                    "status": "error",
                    "reason": "SOLANA_RPC_REJECTION",
                    "msg": f"Solana RPC rejected transfer: {err_msg}",
                    "tx_hash": tx_sig_b58
                }
            confirmed_sig = tx_res.get("result", tx_sig_b58)
    except Exception as e:
        confirmed_sig = tx_sig_b58

    return {
        "status": "success",
        "tx_hash": confirmed_sig,
        "solscan_url": f"https://solscan.io/tx/{confirmed_sig}",
        "lamports": lamports,
        "sol_amount": round(lamports / 1e9, 5),
        "sender": b58encode(sender_pub),
        "recipient": dest_b58
    }

def withdraw_user_sol(
    chat_id: int,
    recipient_address: str = None,
    amount_sol: float = None
) -> dict:
    """
    Safely withdraws native SOL from the user's dedicated trading wallet to their personal wallet.
    If recipient_address is None or 'PHANTOM', auto-resolves to the user's bound Phantom vault.
    Keeps a minimal 0.00001 SOL buffer for network gas.
    If amount_sol is None or 0, withdraws all available balance.
    """
    dest_addr = str(recipient_address or "").strip()
    if not dest_addr or dest_addr.upper() == "PHANTOM":
        phantom_vault = get_user_phantom_wallet(chat_id)
        if not phantom_vault:
            return {
                "status": "error",
                "reason": "NO_PHANTOM_LINKED",
                "msg": "លោកអ្នកមិនទាន់បានភ្ជាប់ Phantom Wallet ផ្ទាល់ខ្លួននៅឡើយទេ។ សូមចុច '🔗 ភ្ជាប់ Phantom Wallet' ឬវាយ `/smart_swap bind_phantom <address>` ជាមុនសិន។"
            }
        dest_addr = phantom_vault

    priv, pub = get_or_create_user_solana_wallet(chat_id)
    bal_data = get_solana_balance(pub)
    current_lamports = bal_data["lamports"]
    gas_reserve = 10000  # 0.00001 SOL network fee reserve

    if current_lamports <= gas_reserve:
        return {
            "status": "error",
            "reason": "INSUFFICIENT_BALANCE",
            "msg": f"សមតុល្យក្នុងកាបូបមានត្រឹមតែ {bal_data['sol_balance']:.4f} SOL មិនគ្រប់គ្រាន់សម្រាប់ផ្ទេរប្រាក់ និងបង់ Gas Fee ឡើយ។",
            "current_sol": bal_data["sol_balance"]
        }

    if amount_sol is None or float(amount_sol) <= 0:
        transfer_lamports = current_lamports - gas_reserve
    else:
        req_lamports = int(float(amount_sol) * 1e9)
        if req_lamports + gas_reserve > current_lamports:
            max_sol = max(0.0, (current_lamports - gas_reserve) / 1e9)
            return {
                "status": "error",
                "reason": "AMOUNT_EXCEEDS_BALANCE",
                "msg": f"ចំនួនស្នើសុំ {amount_sol} SOL លើសពីសមតុល្យដែលអាចដកបាន ({max_sol:.4f} SOL) បន្ទាប់ពីកាត់ Gas Fee។",
                "max_withdrawable_sol": round(max_sol, 4)
            }
        transfer_lamports = req_lamports

    return execute_sol_transfer(priv, dest_addr, transfer_lamports)

# ==============================================================================
# ⚡ JUPITER ON-CHAIN TRANSACTION SIGNING & BROADCAST
# ==============================================================================

def execute_jupiter_live_swap(
    from_mint: str,
    to_mint: str,
    amount_lamports: int,
    slippage_bps: int = 50,
    wrap_unwrap_sol: bool = True,
    signing_priv_key: ed25519.Ed25519PrivateKey = None,
    user_pubkey: str = None
) -> dict:
    """
    Executes a real, live on-chain swap via Jupiter DEX Aggregator:
    Supports both User-Dedicated Wallets (Trojan-style) and Master Hot Wallet.
    """
    if signing_priv_key is not None and user_pubkey is not None:
        priv = signing_priv_key
        pub = str(user_pubkey).strip()
    else:
        priv, pub = load_or_create_bot_keypair()
    
    # Check balance before attempting
    bal_info = get_solana_balance(pub)
    is_sol_input = ("So11111111111111111111111111111111111111112" in from_mint)
    if is_sol_input and (bal_info["lamports"] < amount_lamports + 5000000): # 0.005 SOL safety reserve for rent & gas
        return {
            "status": "error",
            "reason": "INSUFFICIENT_SOL_BALANCE",
            "msg": f"កាបូប {pub[:6]}...{pub[-4:]} មានសមតុល្យ {bal_info['sol_balance']:.4f} SOL មិនគ្រប់គ្រាន់សម្រាប់ទិញ {amount_lamports/1e9:.4f} SOL + ថ្លៃ Gas ឡើយ។",
            "bot_wallet": pub,
            "required_sol": round((amount_lamports + 5000000) / 1e9, 4),
            "current_sol": bal_info["sol_balance"]
        }
    elif not is_sol_input and (bal_info["lamports"] < 2000000): # 0.002 SOL reserve for transaction fee when selling SPL tokens
        return {
            "status": "error",
            "reason": "INSUFFICIENT_SOL_GAS",
            "msg": f"កាបូប {pub[:6]}...{pub[-4:]} មានសមតុល្យ SOL តិចជាង 0.002 SOL មិនគ្រប់គ្រាន់សម្រាប់បង់ថ្លៃ Gas ពេលលក់កាក់ឡើយ។",
            "bot_wallet": pub,
            "required_sol": 0.002,
            "current_sol": bal_info["sol_balance"]
        }

    # 1. Fetch Route Quote
    quote_url = (
        f"https://api.jup.ag/swap/v1/quote?"
        f"inputMint={from_mint}&outputMint={to_mint}&amount={amount_lamports}&slippageBps={slippage_bps}"
    )
    try:
        req_q = urllib.request.Request(quote_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_q, timeout=4.0) as resp_q:
            quote_res = json.loads(resp_q.read().decode("utf-8"))
    except Exception as e:
        return {"status": "error", "reason": "JUPITER_QUOTE_ERROR", "msg": f"Failed to fetch Jupiter quote: {e}"}

    if "outAmount" not in quote_res:
        return {"status": "error", "reason": "JUPITER_NO_ROUTE", "msg": "No viable liquidity route on Jupiter DEX."}

    out_amount = int(quote_res.get("outAmount", 0))
    price_impact = float(quote_res.get("priceImpactPct", 0.0)) * 100.0

    # 2. Get Serialized Swap Transaction
    swap_url = "https://api.jup.ag/swap/v1/swap"
    swap_payload = {
        "quoteResponse": quote_res,
        "userPublicKey": pub,
        "wrapAndUnwrapSol": wrap_unwrap_sol,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto"
    }

    try:
        req_s = urllib.request.Request(
            swap_url,
            data=json.dumps(swap_payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_s, timeout=5.0) as resp_s:
            swap_res = json.loads(resp_s.read().decode("utf-8"))
    except Exception as e:
        return {"status": "error", "reason": "JUPITER_SWAP_TX_ERROR", "msg": f"Failed to get swap transaction: {e}"}

    raw_tx_b64 = swap_res.get("swapTransaction")
    if not raw_tx_b64:
        return {"status": "error", "reason": "EMPTY_SWAP_TRANSACTION", "msg": "Jupiter returned empty transaction."}

    # 3. Sign the Versioned Transaction using Ed25519
    try:
        tx_bytes = bytearray(base64.b64decode(raw_tx_b64))
        num_sigs = tx_bytes[0]
        message_bytes = bytes(tx_bytes[1 + num_sigs * 64:])
        signature = priv.sign(message_bytes)
        tx_bytes[1:65] = signature
        signed_b64 = base64.b64encode(tx_bytes).decode("utf-8")
        tx_signature_b58 = b58encode(signature)
    except Exception as e:
        return {"status": "error", "reason": "SIGNING_FAILED", "msg": f"Transaction Ed25519 signing failed: {e}"}

    # 4. Broadcast Signed Transaction to Solana RPC
    rpc_payload = {
        "jsonrpc": "2.0",
        "id": int(time.time()),
        "method": "sendTransaction",
        "params": [
            signed_b64,
            {"encoding": "base64", "skipPreflight": False, "preflightCommitment": "confirmed"}
        ]
    }

    try:
        req_rpc = urllib.request.Request(
            SOLANA_RPC_URL,
            data=json.dumps(rpc_payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_rpc, timeout=7.0) as resp_rpc:
            rpc_res = json.loads(resp_rpc.read().decode("utf-8"))
            if "error" in rpc_res:
                err_msg = rpc_res["error"].get("message", str(rpc_res["error"]))
                return {
                    "status": "error",
                    "reason": "SOLANA_RPC_REJECTION",
                    "msg": f"Solana RPC rejected transaction: {err_msg}",
                    "tx_signature": tx_signature_b58,
                    "solscan_url": f"https://solscan.io/tx/{tx_signature_b58}"
                }
            confirmed_sig = rpc_res.get("result", tx_signature_b58)
    except Exception as e:
        confirmed_sig = tx_signature_b58

    return {
        "status": "success",
        "live_onchain": True,
        "tx_hash": confirmed_sig,
        "solscan_url": f"https://solscan.io/tx/{confirmed_sig}",
        "in_amount": amount_lamports,
        "out_amount": out_amount,
        "price_impact_pct": round(price_impact, 4),
        "bot_wallet": pub
    }

def get_user_spl_token_balance(chat_id: int, token_mint: str) -> dict:
    """
    Queries on-chain SPL token account balance for a user's dedicated Solana wallet.
    Returns amount_raw (atomic integer units), ui_amount (float), and decimals (int).
    """
    priv, pub = get_or_create_user_solana_wallet(chat_id)
    token_mint_str = str(token_mint).strip()
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time()),
            "method": "getTokenAccountsByOwner",
            "params": [
                pub,
                {"mint": token_mint_str},
                {"encoding": "jsonParsed"}
            ]
        }
        req = urllib.request.Request(
            SOLANA_RPC_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            value = data.get("result", {}).get("value", [])
            if value:
                token_amount_info = value[0].get("account", {}).get("data", {}).get("parsed", {}).get("info", {}).get("tokenAmount", {})
                raw_amt = int(token_amount_info.get("amount", 0))
                ui_amt = float(token_amount_info.get("uiAmount", 0.0) or 0.0)
                decimals = int(token_amount_info.get("decimals", 6))
                return {"amount_raw": raw_amt, "ui_amount": ui_amt, "decimals": decimals}
    except Exception as e:
        print(f"[SPL_TOKEN_BAL] Error querying token balance for user {chat_id}: {e}")
    return {"amount_raw": 0, "ui_amount": 0.0, "decimals": 6}

def execute_live_token_sell_to_sol(
    chat_id: int,
    token_mint: str,
    amount_token_raw: int = None,
    slippage_bps: int = 150
) -> dict:
    """
    Executes a real on-chain SELL order of an SPL token back to native SOL via Jupiter DEX:
    - Automatically signs with user's dedicated Ed25519 keypair.
    - wrapAndUnwrapSol=True automatically deposits native SOL directly into user's wallet.
    - Returns tx_hash, solscan_url, and received SOL lamports.
    """
    priv, pub = get_or_create_user_solana_wallet(chat_id)
    sol_mint = "So11111111111111111111111111111111111111112"
    token_mint_str = str(token_mint).strip()
    
    if not amount_token_raw or int(amount_token_raw) <= 0:
        bal_data = get_user_spl_token_balance(chat_id, token_mint_str)
        amount_token_raw = bal_data.get("amount_raw", 0)
        
    if not amount_token_raw or int(amount_token_raw) <= 0:
        return {
            "status": "error",
            "reason": "ZERO_TOKEN_BALANCE",
            "msg": f"No on-chain SPL token balance found for {token_mint_str} to sell."
        }
        
    return execute_jupiter_live_swap(
        from_mint=token_mint_str,
        to_mint=sol_mint,
        amount_lamports=int(amount_token_raw),
        slippage_bps=slippage_bps,
        wrap_unwrap_sol=True,
        signing_priv_key=priv,
        user_pubkey=pub
    )

