import sys
import os

# Add bot directory to sys.path
repo_dir = r"e:\AI CODE PYTHON\Khmer Master Crypto\khmer-master-crypto-bot"
if repo_dir not in sys.path:
    sys.path.insert(0, repo_dir)

import trading_engine
import security
import database as db

def test_aliases():
    print("Testing trading_engine aliases...")
    assert hasattr(trading_engine, "market_close_all_futures_positions"), "market_close_all_futures_positions missing"
    assert hasattr(trading_engine, "close_all_futures_positions"), "close_all_futures_positions missing"
    assert trading_engine.market_close_all_futures_positions == trading_engine.close_all_futures_positions
    print("[PASS] trading_engine.market_close_all_futures_positions is correctly mapped to close_all_futures_positions")

    assert hasattr(trading_engine, "market_close_futures_position_for_symbol"), "market_close_futures_position_for_symbol missing"
    assert hasattr(trading_engine, "close_futures_position_for_symbol"), "close_futures_position_for_symbol missing"
    assert trading_engine.market_close_futures_position_for_symbol == trading_engine.close_futures_position_for_symbol
    print("[PASS] trading_engine.market_close_futures_position_for_symbol is correctly mapped")

def test_pin_verification():
    print("\nTesting security PIN verification...")
    chat_id = 999999999
    raw_pin = "1234"

    # 1. Test PBKDF2 hash
    pbkdf2 = security.hash_pin(raw_pin, chat_id)
    assert security.verify_pin(raw_pin, chat_id, pbkdf2) is True
    assert security.verify_pin("9999", chat_id, pbkdf2) is False
    print("[PASS] PBKDF2 100k rounds verification works")

    # 2. Test raw plaintext fallback with upgrade
    assert security.verify_pin(raw_pin, chat_id, raw_pin) is True
    print("[PASS] Plaintext raw PIN verification with automatic upgrade works")

if __name__ == "__main__":
    test_aliases()
    test_pin_verification()
    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")
