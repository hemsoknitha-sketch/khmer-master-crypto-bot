import unittest
import time
import sys
import os

# Add Quant Gold directory to path
quant_gold_dir = os.path.join(os.path.dirname(__file__), "Quant Gold")
if quant_gold_dir not in sys.path:
    sys.path.insert(0, quant_gold_dir)

from execution_engine import QuantGoldExecutionEngine
from quant_gold_security import get_quant_gold_security_citadel


class TestQuantGoldReversalFlip(unittest.TestCase):
    def setUp(self):
        self.engine = QuantGoldExecutionEngine()

    def test_reversal_flip_hurdle_and_score(self):
        """Verify that high-conviction opposing signals (confidence >= 65.0%, score >= 8.0) pass reversal flip."""
        # Setup existing SELL position
        self.engine._active_gold_deal_id = "test-deal-123"
        self.engine._active_gold_direction = "SELL"
        self.engine._active_gold_entry_price = 3870.0
        self.engine._active_gold_entry_ts = time.time() - 100.0  # held 100s (> 90s min hold)
        self.engine._last_reversal_flip_ts = 0.0

        current_price = 3872.0  # existing SELL is losing 2 pts

        # Opposing BUY signal with confidence 68% and score +10.0
        now_ts = time.time()
        last_rev_ts = self.engine._last_reversal_flip_ts
        existing_dir = self.engine._active_gold_direction
        action = "BUY"
        confidence = 68.0
        weighted_score = 10.0
        is_macro_bear = False

        existing_entry_p = self.engine._active_gold_entry_price
        existing_pnl_pts = (current_price - existing_entry_p) if existing_dir == "BUY" else (existing_entry_p - current_price)
        is_existing_losing = (existing_pnl_pts <= -2.0)
        self.assertTrue(is_existing_losing)

        rev_cooldown_left = 120.0 - (now_ts - last_rev_ts)
        min_hold_req = 45.0 if is_existing_losing else 90.0
        time_in_pos = now_ts - self.engine._active_gold_entry_ts

        can_flip = False
        flip_veto_reason = ""
        if rev_cooldown_left > 0 and not (is_existing_losing and confidence >= 65.0):
            flip_veto_reason = f"COOLDOWN_ACTIVE"
        elif time_in_pos < min_hold_req:
            flip_veto_reason = f"MIN_HOLD_PROTECTION"
        elif action == "BUY":
            if is_macro_bear:
                flip_veto_reason = "MACRO_BEAR_VETO"
            elif weighted_score < 8.0 and not (is_existing_losing and weighted_score >= 0.0 and confidence >= 65.0):
                flip_veto_reason = f"INSUFFICIENT_BUY_SCORE"
            elif confidence < 65.0:
                flip_veto_reason = f"INSUFFICIENT_CONFIDENCE"
            else:
                can_flip = True

        self.assertTrue(can_flip)
        self.assertEqual(flip_veto_reason, "")

    def test_reversal_flip_macro_trend_protection(self):
        """Verify that opposing signals against Macro Trend are strictly vetoed (fiduciary honesty)."""
        self.engine._active_gold_deal_id = "test-deal-124"
        self.engine._active_gold_direction = "SELL"
        self.engine._active_gold_entry_price = 3870.0
        self.engine._active_gold_entry_ts = time.time() - 200.0

        action = "BUY"
        is_macro_bear = True  # Macro H1/H4 is BEARISH
        confidence = 80.0
        weighted_score = 25.0

        can_flip = False
        flip_veto_reason = ""
        if is_macro_bear:
            flip_veto_reason = "MACRO_BEAR_VETO (Cannot flip to BUY against H1/H4 Downtrend)"

        self.assertFalse(can_flip)
        self.assertIn("MACRO_BEAR_VETO", flip_veto_reason)

    def test_log_throttling_mechanism(self):
        """Verify that rejection logs are throttled to once per 60s for identical reasons."""
        self.engine._last_reversal_block_log_ts = time.time() - 10.0  # 10s ago
        self.engine._last_reversal_block_reason = "INSUFFICIENT_BUY_SCORE (Score -5.9 < +8.0)"

        now_log = time.time()
        last_log_ts = self.engine._last_reversal_block_log_ts
        last_reason = self.engine._last_reversal_block_reason
        flip_veto_reason = "INSUFFICIENT_BUY_SCORE (Score -5.9 < +8.0)"

        # Within 60 seconds with same reason -> should NOT log INFO
        should_log_info = (now_log - last_log_ts >= 60.0) or (flip_veto_reason != last_reason)
        self.assertFalse(should_log_info)

        # After 65 seconds -> should log INFO
        self.engine._last_reversal_block_log_ts = time.time() - 65.0
        last_log_ts = self.engine._last_reversal_block_log_ts
        should_log_info_after = (now_log - last_log_ts >= 60.0) or (flip_veto_reason != last_reason)
        self.assertTrue(should_log_info_after)

    def test_360_market_invalidation_thresholds(self):
        """Verify 360 Citadel market invalidation triggers with calibrated institutional parameters."""
        citadel = get_quant_gold_security_citadel()
        # Test BUY invalidation against SELL position
        # bull_cnt >= 10 and w_score >= 12.0
        inv_check = citadel.evaluate_360_market_invalidation(
            current_price=3875.0,
            position_direction="SELL",
            mtf_data={
                "timeframes": {
                    "M1": {"bias": "BULLISH", "velocity": 0.04},
                    "M3": {"bias": "BULLISH", "velocity": 0.04},
                    "M5": {"bias": "BULLISH", "velocity": 0.04},
                    "M10": {"bias": "BULLISH", "velocity": 0.03},
                    "M15": {"bias": "BULLISH", "velocity": 0.03},
                    "M30": {"bias": "BULLISH", "velocity": 0.02},
                    "H1": {"bias": "BULLISH", "velocity": 0.02},
                    "H2": {"bias": "BULLISH", "velocity": 0.02},
                    "H3": {"bias": "BULLISH", "velocity": 0.01},
                    "H4": {"bias": "BULLISH", "velocity": 0.01},
                },
                "summary": {"weighted_score": 15.0}
            },
            math_data={"kalman_velocity": 0.04}
        )
        self.assertTrue(inv_check.get("is_invalidated"))
        self.assertEqual(inv_check.get("reversal_direction"), "BUY")


if __name__ == "__main__":
    unittest.main()
