# -*- coding: utf-8 -*-
"""
Unit test suite for Live Conference & Speech Intelligence Engine (AQ84 Invariant 108/58/59/76).
Validates:
1. InstitutionalSpeechNLP Hawkish/Dovish scoring and Negation Inversion.
2. Q&A Phase Shock Multiplier.
3. ConferenceQuantStateMachine states and 150-second Toxic Zone clearance.
4. CrossMarketTriangulator divergence conflict detection.
5. Full Powell FOMC simulation replay.
"""

import unittest
import time
import live_conference_speech_engine as lce


class TestLiveConferenceSpeechEngine(unittest.TestCase):

    def setUp(self):
        self.engine = lce.CONFERENCE_ENGINE
        self.engine.reset_to_idle()

    def test_01_hawkish_scoring(self):
        """Tests clear hawkish statements generate positive policy tilt."""
        text = "Inflation remains elevated and the committee is prepared to hike rates further."
        res = lce.InstitutionalSpeechNLP.analyze_chunk(text, is_qa_phase=False)
        self.assertGreater(res["policy_tilt_scalar"], 0.20)
        self.assertIn("HAWKISH", res["classification"])
        self.assertIn("HIKE RATES", res["hawkish_matches"])

    def test_02_dovish_scoring(self):
        """Tests clear dovish statements generate negative policy tilt."""
        text = "We see cooling inflation and are confident inflation is moving toward our 2 percent target."
        res = lce.InstitutionalSpeechNLP.analyze_chunk(text, is_qa_phase=False)
        self.assertLess(res["policy_tilt_scalar"], -0.20)
        self.assertIn("DOVISH", res["classification"])
        self.assertIn("COOLING INFLATION", res["dovish_matches"])

    def test_03_negation_inversion(self):
        """Tests negation reverses sentiment: 'NOT see any reason to hike rates' -> DOVISH."""
        text_neg_hike = "We do not see any reason to hike rates at this time."
        res_neg_hike = lce.InstitutionalSpeechNLP.analyze_chunk(text_neg_hike, is_qa_phase=False)
        self.assertLess(res_neg_hike["policy_tilt_scalar"], 0.0)
        self.assertIn("NOT_HIKE RATES", res_neg_hike["dovish_matches"])

        text_neg_cut = "We do not believe it is time to ease policy today."
        res_neg_cut = lce.InstitutionalSpeechNLP.analyze_chunk(text_neg_cut, is_qa_phase=False)
        self.assertGreater(res_neg_cut["policy_tilt_scalar"], 0.0)
        self.assertIn("NOT_EASE POLICY", res_neg_cut["hawkish_matches"])

    def test_04_qa_shock_multiplier(self):
        """Tests Q&A phase applies 2.2x shock multiplier to scores."""
        text = "We will ease policy if needed."
        res_statement = lce.InstitutionalSpeechNLP.analyze_chunk(text, is_qa_phase=False)
        res_qa = lce.InstitutionalSpeechNLP.analyze_chunk(text, is_qa_phase=True)
        self.assertAlmostEqual(res_qa["shock_multiplier"], 2.2)
        self.assertGreater(res_qa["dovish_score"], res_statement["dovish_score"])

    def test_05_quant_state_machine_flow(self):
        """Tests full lifecycle: IDLE -> IN_SPEECH_ACTIVE -> POST_SPEECH_TOXIC_CLEARANCE -> VOLATILITY_HARVEST_EQUILIBRIUM."""
        self.assertEqual(self.engine.state, lce.ConferenceState.IDLE)

        # 1. Start conference
        self.engine.start_conference(stream_key="FED")
        self.assertEqual(self.engine.state, lce.ConferenceState.IN_SPEECH_ACTIVE)
        self.assertTrue(self.engine.stealth_radar_armed)

        # 2. Ingest speech chunk
        ingest_res = self.engine.ingest_speech_chunk("We are prepared to adjust policy as needed.")
        self.assertIn("rolling_tilt", ingest_res)
        self.assertGreater(len(self.engine.speech_chunks), 0)

        # 3. Conclude conference
        self.engine.conclude_conference()
        self.assertEqual(self.engine.state, lce.ConferenceState.POST_SPEECH_TOXIC_CLEARANCE)
        self.assertTrue(self.engine.toxic_window_active)

        # 4. Advance time past toxic window (150s)
        self.engine.toxic_window_ends_at = time.time() - 1.0
        new_state = self.engine.update_tick()
        self.assertEqual(new_state, lce.ConferenceState.VOLATILITY_HARVEST_EQUILIBRIUM)
        self.assertFalse(self.engine.toxic_window_active)

    def test_06_cross_market_triangulation_divergence(self):
        """Tests that market skepticism / conflict triggers STAY_FLAT_SKEPTICISM."""
        # Dovish speech but DXY surges and Gold falls
        fake_pulse = {
            "macro": {"us10y_yield": 4.50, "dxy_change_pct": 0.45},
            "gold": {"change_pct": -0.60},
            "equities": {"sp500_change_pct": -0.80},
            "crypto": {"btc_change_pct": -1.20}
        }
        dovish_tilt = -0.55
        tri = lce.CrossMarketTriangulator.triangulate(dovish_tilt, macro_pulse=fake_pulse)
        self.assertTrue(tri["is_divergence"])
        self.assertEqual(tri["action_verdict"], "STAY_FLAT_SKEPTICISM")
        self.assertEqual(tri["alignment_status"], "CONFLICT_DIVERGENCE")

    def test_07_full_powell_simulation(self):
        """Runs the complete simulated Powell FOMC meeting replay."""
        sim = lce.run_powell_fomc_simulation(speed_factor=0.0)
        self.assertEqual(sim["chunks_processed"], 8)
        self.assertIn("Federal Reserve FOMC", sim["event_name"])
        self.assertEqual(sim["final_state"], "POST_SPEECH_TOXIC_CLEARANCE")

        # Verify executive report generation
        km_rep = self.engine.generate_assessment(user_lang="km")
        en_rep = self.engine.generate_assessment(user_lang="en")
        self.assertIn("ANGKOR QUANT", km_rep)
        self.assertIn("ANGKOR QUANT", en_rep)
        self.assertIn("Jerome Powell", km_rep)


if __name__ == "__main__":
    unittest.main()
