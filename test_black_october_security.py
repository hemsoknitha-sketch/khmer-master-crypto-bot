# -*- coding: utf-8 -*-
"""
Unit Test Suite for Black October Python Ecosystem Institutional Defense (Invariant 106).
Tests all 4 Pillars:
1. Pillow 13.0 Zero-Upload & Decompression Bomb Guard
2. LiteLLM Supply Chain & Docker Jailbreak Guard
3. SAP Cloud SDK SSRF 10.0 & Data Theft Shield (CVSS 10.0)
4. Memory Crash & DoS Protection (OOM Sentinel & Allocation Governor)
"""

import os
import sys
import unittest
from black_october_security_guard import (
    black_october_guard,
    UploadForbiddenError,
    SSRFSecurityViolation,
    DataTheftPreventedException,
    MemoryExhaustionPrevented
)
from system_security_citadel import security_citadel


class TestBlackOctoberSecurity(unittest.TestCase):

    def test_pillar_1_pillow_zero_upload(self):
        """Pillar 1: User uploads are 100% blocked and Pillow is hardened."""
        # 1. Verify policy
        self.assertFalse(black_october_guard.pillow_guard.ALLOW_USER_UPLOADS)
        self.assertTrue(black_october_guard.pillow_guard.is_hardened)
        self.assertIn("13.0", black_october_guard.pillow_guard.pillow_version)

        # 2. Verify upload rejection
        blocked, reason = black_october_guard.pillow_guard.validate_upload_attempt(
            source="USER_TELEGRAM", filename="malicious.png"
        )
        self.assertFalse(blocked)
        self.assertIn("BLACK OCTOBER SHIELD", reason)
        self.assertIn("100% prohibited", reason)

        # 3. Verify exception assertion
        with self.assertRaises(UploadForbiddenError):
            black_october_guard.pillow_guard.assert_no_upload(
                source="USER_API", filename="exploit.webp"
            )

    def test_pillar_2_litellm_supply_chain(self):
        """Pillar 2: Native SDKs only, zero vulnerable LiteLLM proxies, Docker socket isolated."""
        ok, msg = black_october_guard.litellm_guard.verify_supply_chain_integrity()
        self.assertTrue(ok)
        self.assertIn("100% Certified", msg)

    def test_pillar_3_sap_ssrf_10_and_data_theft(self):
        """Pillar 3: CVSS 10.0 SSRF blocking and data theft prevention."""
        # 1. Cloud metadata IP blocked
        ok, msg = black_october_guard.ssrf_guard.validate_outgoing_url_ssrf("http://169.254.169.254/latest/meta-data/")
        self.assertFalse(ok)
        self.assertIn("SSRF Blocked", msg)

        # 2. Cloud metadata hostname blocked
        ok, msg = black_october_guard.ssrf_guard.validate_outgoing_url_ssrf("https://metadata.google.internal/computeMetadata/v1/")
        self.assertFalse(ok)
        self.assertIn("SSRF Blocked", msg)

        # 3. RFC 1918 private IP blocked
        ok, msg = black_october_guard.ssrf_guard.validate_outgoing_url_ssrf("https://10.0.0.1:8080/internal_api")
        self.assertFalse(ok)
        self.assertIn("SSRF Blocked", msg)

        # 4. Localhost loopback blocked
        ok, msg = black_october_guard.ssrf_guard.validate_outgoing_url_ssrf("https://127.0.0.1:5000/keys")
        self.assertFalse(ok)
        self.assertIn("SSRF Blocked", msg)

        # 5. Insecure schemes blocked (file, gopher, dict)
        ok, msg = black_october_guard.ssrf_guard.validate_outgoing_url_ssrf("file:///etc/passwd")
        self.assertFalse(ok)
        self.assertIn("SSRF Blocked", msg)

        # 6. Valid public HTTPS URL allowed
        ok, msg = black_october_guard.ssrf_guard.validate_outgoing_url_ssrf("https://api.binance.com/api/v3/ping")
        self.assertTrue(ok)

        # 7. Data Theft Prevention: catches sensitive tokens
        secret = os.getenv("MASTER_KEY") or "VERY_SECRET_KEY_12345"
        clean, theft_msg = black_october_guard.ssrf_guard.validate_outbound_data_theft(
            f"Sensitive request with secret: {secret}"
        )
        self.assertFalse(clean)
        self.assertIn("DATA THEFT PREVENTED", theft_msg)

        # 8. Clean data passes
        clean_ok, _ = black_october_guard.ssrf_guard.validate_outbound_data_theft("XAUUSD price inquiry")
        self.assertTrue(clean_ok)

    def test_pillar_4_memory_crash_governor(self):
        """Pillar 4: Request payload clamping & RAM headroom tracking."""
        # 1. Huge payload (>1MB) blocked
        ok, reason = black_october_guard.memory_governor.validate_payload_size(2 * 1024 * 1024)
        self.assertFalse(ok)
        self.assertIn("Memory Crash Guard", reason)

        # 2. Normal payload (<1MB) allowed
        ok, _ = black_october_guard.memory_governor.validate_payload_size(1024)
        self.assertTrue(ok)

        # 3. Memory headroom check
        info = black_october_guard.memory_governor.check_memory_headroom()
        self.assertIn("process_rss_mb", info)
        self.assertIn("system_ram_pct", info)
        self.assertIn("status", info)

    def test_citadel_integration(self):
        """Integration with Layer 6 in SecurityCitadelManager."""
        ok, msg, data = security_citadel.verify_black_october_shield()
        self.assertTrue(ok)
        self.assertIn("100% Certified", msg)
        self.assertEqual(data.get("overall_status"), "CERTIFIED_IMMUNE_TO_BLACK_OCTOBER")

        # Verify card contains Layer 6
        card = security_citadel.generate_citadel_status_card()
        self.assertIn("Layer 6: Black October Ecosystem Shield", card)
        self.assertIn("Pillow Runtime: `v13.0.0", card)


if __name__ == "__main__":
    unittest.main()
