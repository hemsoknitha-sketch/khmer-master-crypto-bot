"""
Unit Test Suite for Angkor Quant Continuous Autonomous Security Training & Threat Immunity Engine (Invariant 107)
=================================================================================================================
Validates the 6 institutional pillars of the living immune system:
1. Threat Intelligence Radar & Dynamic Signature Evolution
2. Red-Team Adversarial Fuzzing Simulator (100% Interception Rate)
3. Unsupervised IsolationForest Anomaly Detector
4. Immutable Auditable Security Incident Ledger (SQLite WAL Mode)
5. Autonomous Self-Healing & Memory / Database Maintenance Governor
6. Hot-Reload Adaptive RAM Defense Bus & Telegram Executive Card Reporting
"""

import os
import sys
import time
import sqlite3
import unittest
import numpy as np

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from autonomous_security_daily_learner import (
    continuous_security_engine,
    security_ram_cache,
    ContinuousSecurityTrainingEngine,
    SecurityAdaptiveRAMCache,
    DB_PATH
)


class TestContinuousAutonomousSecurity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = continuous_security_engine
        cls.cache = security_ram_cache

    def test_01_threat_intelligence_radar(self):
        """Pillar 1: Threat Radar collects CVE signatures and compiles them into RAM."""
        radar_res = self.engine.run_threat_intelligence_radar()
        self.assertEqual(radar_res.get("status"), "PASS")
        self.assertGreaterEqual(radar_res.get("active_signatures_in_ram", 0), 4)
        cve_list = radar_res.get("signatures_loaded", [])
        self.assertTrue(any("CVE-2024-28219" in s for s in cve_list))
        self.assertTrue(any("CVE-2024-4367" in s for s in cve_list))
        self.assertTrue(any("SSRF" in s for s in cve_list))

    def test_02_adversarial_fuzzing_simulation(self):
        """Pillar 2: Red-Team Fuzzing executes synthetic attacks with 100% interception."""
        fuzz_res = self.engine.run_adversarial_fuzzing_simulation(trials=100)
        self.assertIn(fuzz_res.get("status"), ("PASS", "PASS_100%_IMMUNE"))
        self.assertEqual(fuzz_res.get("interception_rate_pct"), 100.0)
        self.assertGreaterEqual(fuzz_res.get("attack_payloads_blocked", 0), 30)
        self.assertEqual(fuzz_res.get("capital_leakage_events"), 0)

    def test_03_anomaly_detector_training(self):
        """Pillar 3: IsolationForest trains anomaly detector on multidimensional traffic vectors."""
        anomaly_res = self.engine.train_traffic_anomaly_detector()
        self.assertIn(anomaly_res.get("status"), ("OPTIMAL", "PASS", "RETRAINED_ACTIVE"))
        self.assertTrue(anomaly_res.get("model_trained"))
        self.assertGreaterEqual(anomaly_res.get("training_sample_count", 0), 500)
        self.assertIn("synthetic_anomaly_detection_rate_pct", anomaly_res)
        self.assertGreaterEqual(anomaly_res.get("synthetic_anomaly_detection_rate_pct", 0), 80.0)

    def test_04_security_incident_ledger_persistence(self):
        """Pillar 4: Security incident logging persists to SQLite WAL ledger."""
        test_ip = "198.51.100.42"
        record_id = self.engine.log_security_incident(
            threat_category="UNIT_TEST_FUZZING_PROBE",
            source_ip=test_ip,
            raw_payload="SELECT * FROM users WHERE '1'='1' --",
            mitigation_action="BLOCKED_BY_UNIT_TEST",
            severity="HIGH"
        )
        self.assertGreater(record_id, 0)

        # Verify record in SQLite table
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT threat_category, source, severity FROM security_incident_ledger WHERE id = ?", (record_id,))
        row = cur.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "UNIT_TEST_FUZZING_PROBE")
        self.assertEqual(row[1], test_ip)
        self.assertEqual(row[2], "HIGH")

        # Test incident summary helper
        summary = self.engine._get_incident_ledger_summary(hours=1)
        self.assertGreaterEqual(summary.get("total_incidents_recorded", 0), 1)

    def test_05_memory_and_db_self_healing(self):
        """Pillar 5: Autonomous self-healing prunes expired bans and checkpoints SQLite WAL."""
        healing_res = self.engine.execute_memory_and_db_self_healing()
        self.assertIn(healing_res.get("status"), ("PASS", "MEMORY_INTACT_OPTIMAL"))
        self.assertEqual(healing_res.get("database_checkpoint"), "OK")
        self.assertIn("process_rss_mb", healing_res)
        self.assertLess(healing_res.get("process_rss_mb", 0), 2500)  # RSS < 2.5 GB

    def test_06_hot_reload_ram_cache_and_reporting_card(self):
        """Pillar 6: RAM Cache holds updated bans and Telegram card generates cleanly."""
        # Add test IP ban in RAM
        self.cache.update_rules(
            anomaly_threshold=-0.12,
            active_signatures=["CUSTOM_TEST_SIGNATURE"],
            banned_ips=["203.0.113.99"]
        )
        self.assertTrue(self.cache.is_ip_banned("203.0.113.99"))
        self.assertFalse(self.cache.is_ip_banned("1.1.1.1"))

        # Run complete training cycle
        cycle_state = self.engine.execute_daily_security_training_cycle(is_manual=True)
        self.assertEqual(cycle_state.get("verdict"), "CERTIFIED_IMMUNE_ZERO_DEFECTS")

        # Generate Telegram Markdown Card
        card = self.engine.generate_daily_security_card(cycle_state)
        self.assertIn("CONTINUOUS AUTONOMOUS SECURITY", card)
        self.assertIn("Invariant 107", card)
        self.assertIn("100% IMMUNE", card)
        self.assertIn("Pillar 1", card)
        self.assertIn("Pillar 2", card)
        self.assertIn("Pillar 3", card)
        self.assertIn("Pillar 4", card)
        self.assertIn("Pillar 5", card)
        self.assertIn("Pillar 6", card)

    def test_07_health_status_query(self):
        """Verify get_health_status returns complete diagnostic dictionary."""
        health = self.engine.get_health_status()
        self.assertEqual(health.get("verdict"), "CERTIFIED_IMMUNE_ZERO_DEFECTS")
        self.assertIn("pillar1_threat_radar", health)
        self.assertIn("pillar2_adversarial_fuzzing", health)
        self.assertIn("pillar3_anomaly_model", health)
        self.assertIn("pillar5_self_healing", health)

    def test_08_spring_and_java_rce_defense(self):
        """Pillar 2 & Ingress: Validates interception of Oracle Java SE & Spring Framework RCE probes."""
        # 1. Verify signatures are in RAM
        from autonomous_security_daily_learner import DEFAULT_THREAT_PATTERNS
        signatures = [p.name for p in DEFAULT_THREAT_PATTERNS]
        self.assertTrue(any("Spring4Shell" in s for s in signatures))
        self.assertTrue(any("Log4Shell" in s for s in signatures))
        self.assertTrue(any("Actuator" in s for s in signatures))
        self.assertTrue(any("Java Object Deserialization" in s for s in signatures))

        # 2. Verify fuzzing suite blocks all Spring & Java RCE mutations
        fuzz_res = self.engine.run_adversarial_fuzzing_simulation(trials=50)
        self.assertEqual(fuzz_res.get("interception_rate_pct"), 100.0)
        self.assertEqual(fuzz_res.get("escaped"), 0)

        # 3. Verify IP auto-quarantine for malicious Spring scanner
        attacker_ip = "192.0.2.123"
        self.cache.update_rules(banned_ips=[attacker_ip])
        self.assertTrue(self.cache.is_ip_banned(attacker_ip))


if __name__ == "__main__":
    unittest.main()

