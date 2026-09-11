"""
Test Suite for Solana On-Chain Dedicated Hot Wallet & Smart Swap Engine
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from dotenv import load_dotenv

load_dotenv()

class TestSolanaOnChainEngine(unittest.TestCase):
    def test_01_base58_encoding(self):
        import solana_trading_wallet
        test_bytes = b"Hello, Solana High-Speed Mainnet!"
        encoded = solana_trading_wallet.b58encode(test_bytes)
        decoded = solana_trading_wallet.b58decode(encoded)
        self.assertEqual(test_bytes, decoded)

    def test_02_bot_hot_wallet_generation(self):
        import solana_trading_wallet
        sk, pub = solana_trading_wallet.load_or_create_bot_keypair()
        self.assertIsNotNone(sk)
        self.assertTrue(len(pub) >= 32 and len(pub) <= 44)
        
        overview = solana_trading_wallet.get_bot_solana_wallet_overview()
        self.assertEqual(overview["public_key"], pub)
        self.assertIn("sol_balance", overview)
        self.assertIn("usd_value", overview)
        self.assertIn("solscan_url", overview)
        print(f"[TEST 2] Bot Hot Wallet: {pub} | Balance: {overview['sol_balance']} SOL")

    def test_03_jupiter_quote_routing(self):
        import smart_swap_engine
        sol_mint = "So11111111111111111111111111111111111111112"
        usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        quote = smart_swap_engine.get_solana_jupiter_quote(sol_mint, usdc_mint, 10000000)
        self.assertEqual(quote.get("status"), "success")
        self.assertGreater(quote.get("out_amount", 0), 0)
        print(f"[TEST 3] Jupiter Quote: 0.01 SOL -> {quote['out_amount']/1e6:.2f} USDC (Steps: {quote['route_steps']})")

    def test_04_token_security_audit(self):
        import smart_swap_engine
        sol_mint = "So11111111111111111111111111111111111111112"
        audit = smart_swap_engine.evaluate_token_security("SOLANA", sol_mint)
        self.assertTrue(audit["is_safe"])
        self.assertEqual(audit["status"], "VERIFIED_BLUECHIP")
        print(f"[TEST 4] SOL Security Status: {audit['status']}")

    def test_05_execute_smart_swap_with_bot_wallet(self):
        import smart_swap_engine
        res = smart_swap_engine.execute_smart_swap(
            chat_id=859271875,
            chain="SOLANA",
            from_token="SOL",
            to_token="USDC",
            amount=0.01,
            slippage_pct=0.5
        )
        self.assertEqual(res.get("status"), "success")
        self.assertIn("bot_wallet", res)
        self.assertIn("solscan_url", res)
        self.assertIn("is_live_onchain", res)
        print(f"[TEST 5] Swap Executed! Tx: {res['tx_hash']} | Live: {res['is_live_onchain']} | Bot Wallet: {res['bot_wallet']}")

        # Clean up test position
        smart_swap_engine.stop_smart_swap(859271875, "ALL")

if __name__ == "__main__":
    unittest.main()
