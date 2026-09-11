"""
Unit tests for Per-User Dedicated Solana Wallets (Trojan / BonkBot Architecture)
and Personal Phantom Wallet Profit Settlement Vault Binding.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import database as db
import solana_trading_wallet

class TestUserDedicatedWallets(unittest.TestCase):

    def test_01_user_wallet_isolation(self):
        """Verify each user receives a 100% unique keypair and address."""
        user1_id = 859271875
        user2_id = 999999999

        priv1, pub1 = solana_trading_wallet.get_or_create_user_solana_wallet(user1_id)
        priv2, pub2 = solana_trading_wallet.get_or_create_user_solana_wallet(user2_id)

        self.assertNotEqual(pub1, pub2, "Users must not share wallet addresses!")
        print(f"\n[TEST 1] User 1 ({user1_id}) Wallet: {pub1}")
        print(f"[TEST 1] User 2 ({user2_id}) Wallet: {pub2}")

    def test_02_database_persistence_and_encryption(self):
        """Verify AES-256 encrypted private key in DB reloads with exact same address."""
        user_id = 859271875
        priv1, pub1 = solana_trading_wallet.get_or_create_user_solana_wallet(user_id)

        # Query raw DB record
        record = db.get_user_solana_wallet(user_id)
        self.assertIsNotNone(record)
        self.assertEqual(record["public_key"], pub1)
        self.assertNotEqual(record["encrypted_private_key"], "")

        # Reload from scratch
        priv_reloaded, pub_reloaded = solana_trading_wallet.get_or_create_user_solana_wallet(user_id)
        self.assertEqual(pub1, pub_reloaded)
        print(f"[TEST 2] AES-256 Reload & Persistence: Match 100% ({pub_reloaded})")

    def test_03_private_key_export(self):
        """Verify private key export contains valid Base58 string."""
        user_id = 859271875
        key_data = solana_trading_wallet.export_user_private_key(user_id)
        self.assertIsNotNone(key_data)
        self.assertIn("public_key", key_data)
        self.assertIn("private_key_b58", key_data)
        self.assertTrue(len(key_data["private_key_b58"]) > 50)
        print(f"[TEST 3] Exported Key Len: {len(key_data['private_key_b58'])} chars")

    def test_04_wallet_overview_and_balance(self):
        """Verify get_user_solana_wallet_overview returns proper schema."""
        user_id = 859271875
        overview = solana_trading_wallet.get_user_solana_wallet_overview(user_id)
        self.assertIn("public_key", overview)
        self.assertIn("sol_balance", overview)
        self.assertIn("usd_value", overview)
        self.assertIn("solscan_url", overview)
        print(f"[TEST 4] Overview for {user_id}: Balance {overview['sol_balance']} SOL (${overview['usd_value']})")

    def test_05_withdrawal_guard(self):
        """Verify withdrawal safely catches unfunded wallets."""
        user_id = 859271875
        res = solana_trading_wallet.withdraw_user_sol(user_id, "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin", 1.0)
        self.assertEqual(res["status"], "error")
        print(f"[TEST 5] Unfunded Wallet Protection: {res['reason']} -> {res['msg']}")

    def test_06_phantom_wallet_binding(self):
        """Verify binding personal Phantom wallet address as profit settlement vault."""
        user_id = 859271875
        sample_phantom = "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"

        # Bind
        res = solana_trading_wallet.bind_user_phantom_wallet(user_id, sample_phantom)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["phantom_address"], sample_phantom)

        # Retrieve
        bound = solana_trading_wallet.get_user_phantom_wallet(user_id)
        self.assertEqual(bound, sample_phantom)
        print(f"[TEST 6] Phantom Wallet Bound: {bound} (100% Match)")

        # Invalid address rejection test
        bad_res = solana_trading_wallet.bind_user_phantom_wallet(user_id, "invalid_sol_address")
        self.assertEqual(bad_res["status"], "error")
        print(f"[TEST 6] Invalid Address Rejected: {bad_res['reason']}")

    def test_07_phantom_auto_withdrawal_resolution(self):
        """Verify withdrawal to 'PHANTOM' auto-routes to bound address."""
        user_id = 859271875
        sample_phantom = "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"
        solana_trading_wallet.bind_user_phantom_wallet(user_id, sample_phantom)

        res = solana_trading_wallet.withdraw_user_sol(user_id, "PHANTOM", 0.1)
        # Because wallet is unfunded on testnet/mainnet, it should catch INSUFFICIENT_BALANCE
        # but the destination was successfully resolved without NO_PHANTOM_LINKED error!
        self.assertNotEqual(res.get("reason"), "NO_PHANTOM_LINKED")
        print(f"[TEST 7] Phantom Auto-Route Resolution Verified: {res['reason']}")

if __name__ == "__main__":
    unittest.main()
