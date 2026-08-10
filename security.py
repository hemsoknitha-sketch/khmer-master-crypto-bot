import os
import hmac
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    except Exception:
        pass

# Ensure environment variables are loaded
load_dotenv()

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

def get_or_create_master_key() -> bytes:
    """Retrieves the master key from .env, or creates one if it doesn't exist."""
    key = os.getenv("MASTER_KEY")
    if not key:
        print("🔐 MASTER_KEY not found. Generating a new military-grade AES-256 (Fernet) key...")
        key = Fernet.generate_key().decode('utf-8')
        
        # Ensure .env file exists
        if not os.path.exists(ENV_PATH):
            open(ENV_PATH, 'w').close()
            
        set_key(ENV_PATH, "MASTER_KEY", key)
        # Reload to ensure it's in the environment
        load_dotenv()
    return key.encode('utf-8')

# Initialize the cipher suite globally
try:
    _master_key = get_or_create_master_key()
    _cipher_suite = Fernet(_master_key)
except Exception as e:
    print(f"⚠️ CRITICAL: Failed to initialize encryption module: {e}")
    _cipher_suite = None

def encrypt_data(plaintext: str) -> str:
    """Encrypts a plaintext string into a secure ciphertext string."""
    if not plaintext or _cipher_suite is None:
        return ""
    encrypted_bytes = _cipher_suite.encrypt(plaintext.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_data(ciphertext: str) -> str:
    """Decrypts a ciphertext string back into plaintext."""
    if not ciphertext or _cipher_suite is None:
        return ""
    try:
        decrypted_bytes = _cipher_suite.decrypt(ciphertext.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        # If decryption fails (e.g., old unencrypted keys or wrong key)
        print(f"⚠️ Decryption failed (might be legacy unencrypted key): {e}")
        return ""

def hash_pin(pin: str, chat_id: int) -> str:
    """Hashes a PIN using PBKDF2-HMAC-SHA256 with 100,000 iterative rounds and unique user salt."""
    if not pin:
        return ""
    str_pin = str(pin).strip()
    salt = f"{chat_id}_TURBO_AGI_SALT_2026".encode('utf-8')
    master = _master_key if _master_key else b"APEX_TURBO_AGI_DEFAULT_SALT"
    combined_salt = salt + master
    dk = hashlib.pbkdf2_hmac('sha256', str_pin.encode('utf-8'), combined_salt, 100000)
    return dk.hex()

def verify_pin(pin: str, chat_id: int, stored_hash: str) -> bool:
    """
    Verifies the provided PIN against the stored hash.
    Seamlessly supports PBKDF2-HMAC-SHA256 (100k rounds), legacy HMAC-SHA256, and plain SHA256,
    automatically upgrading legacy hashes to PBKDF2 100,000 rounds.
    """
    if not pin or not stored_hash:
        return False
        
    str_pin = str(pin).strip()

    # 1. Check current PBKDF2 100,000 rounds standard
    pbkdf2_hash = hash_pin(str_pin, chat_id)
    if hmac.compare_digest(pbkdf2_hash, stored_hash):
        return True
        
    # 2. Check legacy HMAC-SHA256 standard
    salt = f"{chat_id}_PIN_SALT"
    key = (_master_key if _master_key else b"") + salt.encode('utf-8')
    legacy_hmac = hmac.new(key, str_pin.encode('utf-8'), hashlib.sha256).hexdigest()
    if hmac.compare_digest(legacy_hmac, stored_hash):
        try:
            import database as db
            db.set_user_pin(chat_id, pbkdf2_hash)
            print(f"🔐 Seamlessly upgraded legacy HMAC PIN hash for user {chat_id} to PBKDF2 100k rounds.")
        except Exception:
            pass
        return True

    # 3. Check legacy plain SHA256 (Seamless Migration)
    legacy_plain = hashlib.sha256(str_pin.encode('utf-8')).hexdigest()
    if hmac.compare_digest(legacy_plain, stored_hash):
        try:
            import database as db
            db.set_user_pin(chat_id, pbkdf2_hash)
            print(f"🔐 Seamlessly upgraded legacy plain SHA256 PIN hash for user {chat_id} to PBKDF2 100k rounds.")
        except Exception:
            pass
        return True
        
    return False
