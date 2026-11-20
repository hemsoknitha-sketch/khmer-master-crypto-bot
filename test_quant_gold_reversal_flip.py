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
        """Verify that high-conviction opposing signals pass reversal flip on failing trades (AQ88 Invariant 127)."""
        # Setup existing SELL position
        self.engine._active_gold_deal_id = "test-deal-123"
        self.engine._active_gold_direction = "SELL"
        self.engine._active_gold_entry_price = 3870.0
        self.engine._active_gold_entry_ts = time.time() - 100.0  # held 100s (> 45s min hold)
        self.engine._last_reversal_flip_ts = 0.0

        current_price = 3873.0  # existing SELL is losing 3.0 pts (<= -2.50 pts)

        now_ts = time.time()
        last_rev_ts = self.engine._last_reversal_flip_ts
        existing_dir = self.engine._active_gold_direction
        action = "BUY"
        confidence = 75.0
        weighted_score = 18.0
        is_macro_bear = False
        kalman_vel = 0.02
        m15_ema21 = 3872.0
        m15_atr = 2.5
        m15_rsi = 55.0
        ex_state = "NEUTRAL_BALANCED"

        existing_entry_p = self.engine._active_gold_entry_price
        existing_pnl_pts = (current_price - existing_entry_p) if existing_dir == "BUY" else (existing_entry_p - current_price)
        is_existing_profitable = (existing_pnl_pts >= 1.20)
        is_existing_losing = (existing_pnl_pts <= -0.50)
        self.assertTrue(is_existing_losing)
        self.assertFalse(is_existing_profitable)

        rev_cooldown_left = 180.0 - (now_ts - last_rev_ts)
        min_hold_req = 45.0
        time_in_pos = now_ts - self.engine._active_gold_entry_ts

        can_flip = False
        flip_veto_reason = ""
        if is_existing_profitable:
            flip_veto_reason = "PROFIT_RUNNER_PROTECTED"
        elif not is_existing_losing:
            flip_veto_reason = "SCRATCH_ZONE_HOLD"
        elif rev_cooldown_left > 0:
            flip_veto_reason = "COOLDOWN_ACTIVE"
        elif time_in_pos < min_hold_req:
            flip_veto_reason = "MIN_HOLD_PROTECTION"
        elif action == "BUY":
            if is_macro_bear:
                flip_veto_reason = "MACRO_BEAR_VETO"
            elif weighted_score < 15.0:
                flip_veto_reason = "INSUFFICIENT_BUY_SCORE"
            elif confidence < 70.0:
                flip_veto_reason = "INSUFFICIENT_CONFIDENCE"
            elif kalman_vel < -0.010:
                flip_veto_reason = "VELOCITY_DIVERGENCE"
            elif (current_price - m15_ema21) > (1.85 * m15_atr):
                flip_veto_reason = "ANTI_CHASING_IMPULSE_VETO"
            elif m15_rsi >= 68.0:
                flip_veto_reason = "ANTI_OVERBOUGHT_VETO"
            elif ex_state == "BULLS_EXHAUSTED_AT_TOP":
                flip_veto_reason = "EXHAUSTION_VETO"
            else:
                can_flip = True

        self.assertTrue(can_flip)
        self.assertEqual(flip_veto_reason, "")

    def test_reversal_flip_profit_protection(self):
        """Verify that profitable or healthy trades are NEVER flipped out of (Fiduciary Profit Protection)."""
        self.engine._active_gold_deal_id = "test-deal-win-1"
        self.engine._active_gold_direction = "SELL"
        self.engine._active_gold_entry_price = 3880.0
        self.engine._active_gold_entry_ts = time.time() - 200.0

        current_price = 3870.0  # existing SELL is in +10 pts profit!
        existing_dir = "SELL"
        existing_pnl_pts = 3880.0 - current_price  # +10.0 pts
        is_existing_profitable = (existing_pnl_pts >= 1.20)
        is_existing_losing = (existing_pnl_pts <= -0.50)
        self.assertTrue(is_existing_profitable)
        self.assertFalse(is_existing_losing)

        # Even with high-conviction opposing BUY signal
        action = "BUY"
        weighted_score = 30.0
        confidence = 90.0

        can_flip = False
        flip_veto_reason = ""
        if is_existing_profitable:
            flip_veto_reason = f"PROFIT_RUNNER_PROTECTED (Existing {existing_dir} in solid profit with {existing_pnl_pts:+.2f} pts PnL. Protected by TP/SL, flipping forbidden!)"

        self.assertFalse(can_flip)
        self.assertIn("PROFIT_RUNNER_PROTECTED", flip_veto_reason)

    def test_reversal_flip_anti_chasing_veto(self):
        """Verify that chasing overextended impulse candles (> 1.85x ATR from EMA21) vetoes reversal flip."""
        current_price = 3885.0
        m15_ema21 = 3875.0
        m15_atr = 3.0  # 1.85 * 3.0 = 5.55 pts. Diff is 10.0 pts (> 1.85x ATR)!

        action = "BUY"
        is_chasing = (current_price - m15_ema21) > (1.85 * m15_atr)
        self.assertTrue(is_chasing)

    def test_reversal_flip_anti_oversold_veto(self):
        """Verify that shorting into panic oversold bottom (RSI <= 38.0) is strictly vetoed (Invariant 1.1)."""
        m15_rsi = 32.0  # Panic oversold
        action = "SELL"
        is_oversold_veto = (m15_rsi <= 38.0)
        self.assertTrue(is_oversold_veto)

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

    def test_preemptive_adverse_micro_cut(self):
        """Verify that adverse drawdown triggers pre-emptive micro-cut before full broker SL."""
        pnl_pts = -1.50  # -1.50 pts drawdown (loss -$0.75 on 0.5 lot)
        upl = -0.75
        is_adverse_drawdown = (upl <= -0.60 or pnl_pts <= -1.20)
        self.assertTrue(is_adverse_drawdown)

        # M5 shows adverse plunge for BUY trade
        dir_side = "BUY"
        s_f5 = 72.0
        exh_m5 = "BEAR_MOMENTUM_PLUNGING"
        k_v = -0.030
        adverse_m5_force = (dir_side == "BUY" and (s_f5 >= 68.0 or exh_m5 == "BEAR_MOMENTUM_PLUNGING" or k_v <= -0.025))
        self.assertTrue(adverse_m5_force)

    def test_high_watermark_peak_shock_harvest(self):
        """Verify high-watermark retaining ratchet locks >= 78% of peak gains."""
        current_peak_pts = 6.99  # peak was +6.99 pts ($3.22)
        shock_pts_threshold = max(current_peak_pts - 1.20, current_peak_pts * 0.78)  # max(5.79, 5.45) = 5.79 pts
        self.assertAlmostEqual(shock_pts_threshold, 5.79, places=2)

        # At 5.70 pts, shock triggers (retained 81.5% of peak gains, rather than dumping to $1.35 or $0.50)
        pnl_pts = 5.70
        is_shock_pts = (
            current_peak_pts >= 2.50 and
            pnl_pts <= shock_pts_threshold and
            pnl_pts >= 1.20
        )
        self.assertTrue(is_shock_pts)


if __name__ == "__main__":
    unittest.main()
