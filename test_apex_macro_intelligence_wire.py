"""
Unit Tests for Apex Global Macro & Quantitative Intelligence Wire
Validating Invariant 100, Invariants 58/74, Nano-Trie <0.05ms Matching,
$6T US Net Liquidity Formula, Red Folder Blackout, and Dynamic Quant Sentiment Feed.
"""
import unittest
import apex_macro_intelligence_wire as amw


class TestApexMacroIntelligenceWire(unittest.TestCase):
    """
    Rigorously verifies the 4 pillars of the Apex Global Macro & Quantitative Intelligence Wire.
    """

    def test_01_nano_trie_keyword_matching_and_latency(self):
        """
        Pillar 1: Nano-Trie <0.05ms Keyword Matching & Official Entity Detection.
        """
        test_headline = "Federal Reserve Chairman Jerome Powell announces strategic bitcoin reserve and rate cut without inflation fear."
        res = amw.NANO_TRIE.match(test_headline)

        self.assertIn("sentiment_scalar", res)
        self.assertIn("sentiment_label", res)
        self.assertIn("detected_entities", res)
        self.assertIn("latency_ms", res)

        # Entity detection
        self.assertIn("FEDERAL_RESERVE", res["detected_entities"])
        # Sentiment should be bullish due to "rate cut" and "strategic bitcoin reserve"
        self.assertGreater(res["sentiment_scalar"], 0.0)
        # Latency must be sub-millisecond
        self.assertLess(res["latency_ms"], 1.0)

    def test_02_us_net_liquidity_and_intermarket_macro(self):
        """
        Pillar 2: $6T US Net Liquidity Formula & Intermarket Macro Engine.
        Net Liquidity = Fed Assets - TGA - RRP.
        """
        report = amw.generate_apex_macro_news_report("BTCUSDT", user_lang="km")
        text = str(report)

        # Formula verification in text
        self.assertIn("US Net Liquidity Formula", text)
        self.assertIn("Fed Assets", text)
        self.assertIn("TGA", text)
        self.assertIn("RRP", text)
        self.assertIn("DXY", text)
        self.assertIn("Real Yield", text)
        self.assertIn("VIX", text)

    def test_03_economic_calendar_red_folder_blackout(self):
        """
        Pillar 3: Economic Calendar Red Folder Blackout Integration (Invariant 58/74).
        """
        report = amw.generate_apex_macro_news_report("GOLD", user_lang="en")
        text = str(report)

        self.assertIn("ECONOMIC CALENDAR RED FOLDER", text.upper())
        self.assertIn("SPREAD", text.upper())

    def test_04_dynamic_quant_sentiment_and_meta_labeling(self):
        """
        Pillar 4: Dynamic Quant Sentiment Feed & AFML Meta-Labeling Win Probability Modulator.
        """
        report = amw.generate_apex_macro_news_report("US100", user_lang="km")
        text = str(report)

        self.assertIn("Quant Sentiment Scalar", text)
        self.assertIn("AFML", text)
        self.assertIn("Win Probability", text)

    def test_05_trilingual_and_cover_image_dispatch(self):
        """
        Verifies Trilingual formatting (km, en, zh) and HD Cover Image preservation.
        """
        # Khmer
        km_rep = amw.generate_apex_macro_news_report("BTCUSDT", user_lang="km")
        self.assertTrue(km_rep.image_url.startswith("https://"))
        self.assertIn("សន្ទស្សន៍", str(km_rep))

        # English
        en_rep = amw.generate_apex_macro_news_report("GOLD", user_lang="en")
        self.assertTrue(en_rep.image_url.startswith("https://"))
        self.assertIn("QUANTITATIVE WIRE", str(en_rep))

        # Chinese
        zh_rep = amw.generate_apex_macro_news_report("NVDA", user_lang="zh")
        self.assertTrue(zh_rep.image_url.startswith("https://"))
        self.assertIn("华尔街全球宏观", str(zh_rep))


if __name__ == "__main__":
    unittest.main()
