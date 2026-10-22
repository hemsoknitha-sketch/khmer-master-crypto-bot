# -*- coding: utf-8 -*-
"""
Test Suite: Structural Invalidation Anchor SL, Liquidity Pool TP1/TP2/Runner & 4-Phase Breakeven Armor (Invariant 98 - AQ98)
Verifies:
1. Sizing Dollar Risk Clamp (Lot = Max Allowed Risk ($2.50) / Structural Distance on <$500 accounts)
2. 3-Stage Liquidity Pool Targeting (TP1 at +1.8R, TP2 at +3.5R, Runner at +8.0R)
3. 4-Phase Trailing Stop & Breakeven Armor Lifecycle:
   - Phase 0: Structural Invalidation Point + 1.5x Spread Buffer
   - Phase 1: +1.2R -> Tighten SL to Entry - 0.5x ATR (Cuts risk 60%)
   - Phase 2: +1.8R to +2.0R -> Bank 50% TP1 & Lock Breakeven Armor (0.00R Free Roll)
   - Phase 3: +3.5R -> Bank 30% TP2 & Lock +2.0R Cash Floor
   - Phase 4: Parabolic RSI >= 80.0 / <= 20.0 Exhaustion -> Bank 85% Peak Profit Floor
"""

import unittest
from super_smart_capital_citadel import TradFiMultiTargetScaleOutManager
from capital_engine import CapitalKellyPositionSizer, PropFirmRiskManager


class TestStructuralSLTPBreakeven(unittest.TestCase):

    def test_01_lot_size_dollar_risk_clamp(self):
        """Verify on <$500 account, max allowed dollar risk is clamped to <= $2.50."""
        # 1. PropFirmRiskManager clamp
        guardian = PropFirmRiskManager()
        lot_prop = guardian.calculate_prop_position_size(
            equity=250.0,
            risk_pct=1.5,
            entry_price=2650.0,  # Gold
            sl_price=2640.0,     # 10.0 distance
            epic="GOLD"
        )
        # Structural SL distance is 10.0 points.
        # Max allowed dollar risk = $2.50.
        # Max contract size = $2.50 / 10.0 = 0.25
        self.assertGreater(lot_prop, 0.0)
        self.assertLessEqual(lot_prop, 0.25)
        print(f"[TEST 1A PASS] Prop Guardian Lot Clamped: {lot_prop} contracts (Max Risk: $2.50)")

        # 2. CapitalKellyPositionSizer clamp
        sizer = CapitalKellyPositionSizer()
        lot_kelly = sizer.calculate_lot_size(
            chat_id=12345,
            epic="GOLD",
            entry_price=2650.0,
            sl_price=2640.0,
            tp_price=2680.0,
            confidence_score=75.0,
            budget=250.0,
            available_equity=250.0
        )
        self.assertGreater(lot_kelly, 0.0)
        self.assertLessEqual(lot_kelly, 0.25)
        print(f"[TEST 1B PASS] Kelly Sizer Lot Clamped: {lot_kelly} contracts (Max Risk: $2.50)")

    def test_02_calculate_scale_out_plan(self):
        """Verify calculation of 3-stage liquidity pool targets and phase 1 breathing stop."""
        plan = TradFiMultiTargetScaleOutManager.calculate_scale_out_plan(
            epic="GOLD",
            direction="BUY",
            entry_price=2650.0,
            sl_price=2640.0,      # sl_dist = 10.0
            total_size=1.0,
            spread=0.40,
            tp1_r=1.80,
            tp2_r=3.50,
            runner_r=8.00,
            atr_15m=4.0
        )
        self.assertEqual(plan["tp1_r"], 1.80)
        self.assertEqual(plan["tp2_r"], 3.50)
        self.assertEqual(plan["runner_r"], 8.00)
        # Buy TP1 = 2650 + (1.8 * 10.0) = 2668.0
        self.assertEqual(plan["tp1_price"], 2668.0)
        # Buy TP2 = 2650 + (3.5 * 10.0) = 2685.0
        self.assertEqual(plan["tp2_price"], 2685.0)
        # Buy Runner (tp3) = 2650 + (8.0 * 10.0) = 2730.0
        self.assertEqual(plan["tp3_price"], 2730.0)
        # Buy Breakeven Armor = 2650 + max(0.40 * 0.5, 2650 * 0.001) = 2650 + 2.65 = 2652.65
        self.assertGreater(plan["be_sl"], 2650.0)
        # Buy Phase 1 SL = Entry - 0.5 * eff_atr = 2650 - (0.5 * 4.0) = 2648.0
        self.assertEqual(plan["phase1_sl"], 2648.0)
        # Lot distribution 50% / 30% / 20%
        self.assertEqual(plan["tranches"][0]["size"], 0.50)
        self.assertEqual(plan["tranches"][1]["size"], 0.30)
        self.assertEqual(plan["tranches"][2]["size"], 0.20)
        print(f"[TEST 2 PASS] Scale-out Plan verified: TP1={plan['tp1_price']}, TP2={plan['tp2_price']}, Runner={plan['tp3_price']}, Phase1_SL={plan['phase1_sl']}")

    def test_03_phase_1_risk_reduction(self):
        """Verify Phase 1 (+1.2R) tightens SL to Entry - 0.5x ATR, cutting initial risk by 60%."""
        res = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="US100",
            direction="BUY",
            entry_price=20000.0,
            current_price=20120.0,  # +1.2R on 100 pt SL
            sl_dist=100.0,
            spread=1.50,
            upl=12.0,
            peak_upl=12.0,
            scale_tier=0.0,
            atr_15m=30.0
        )
        self.assertEqual(res["action"], "PHASE_1_RISK_REDUCTION")
        self.assertEqual(res["new_scale_tier"], 0.5)
        # Entry - 0.5x ATR = 20000 - 15 = 19985.0
        self.assertEqual(res["new_sl"], 19985.0)
        print(f"[TEST 3 PASS] Phase 1 (+1.2R) Risk Reduction verified: New SL={res['new_sl']}")

    def test_04_phase_2_breakeven_armor(self):
        """Verify Phase 2 (+1.8R to +2.0R) triggers Breakeven Armor, locking Risk = 0.00R Free Roll."""
        res = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="US100",
            direction="BUY",
            entry_price=20000.0,
            current_price=20185.0,  # +1.85R
            sl_dist=100.0,
            spread=1.50,
            upl=18.50,
            peak_upl=18.50,
            scale_tier=0.5,
            atr_15m=30.0
        )
        self.assertEqual(res["action"], "STAGE_1_BREAKEVEN_ARMOR")
        self.assertEqual(res["new_scale_tier"], 1)
        # Breakeven Armor = 20000 + max(1.5 * 0.5, 20000 * 0.001) = 20020.0
        self.assertGreaterEqual(res["new_sl"], 20000.75)
        print(f"[TEST 4 PASS] Phase 2 (+1.8R) Breakeven Armor verified: New SL={res['new_sl']} (0.00R Free Roll)")

    def test_05_phase_3_profit_floor_lock(self):
        """Verify Phase 3 (+3.5R) ratchets SL to +2.0R Guaranteed Cash Profit Floor."""
        res = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="US100",
            direction="BUY",
            entry_price=20000.0,
            current_price=20360.0,  # +3.6R
            sl_dist=100.0,
            spread=1.50,
            upl=36.0,
            peak_upl=36.0,
            scale_tier=1,
            atr_15m=30.0
        )
        self.assertEqual(res["action"], "STAGE_2_PROFIT_LOCK")
        self.assertEqual(res["new_scale_tier"], 2)
        # +2.0R profit floor = 20000 + (2.0 * 100.0) = 20200.0
        self.assertEqual(res["new_sl"], 20200.0)
        print(f"[TEST 5 PASS] Phase 3 (+3.5R) Cash Floor Lock verified: New SL={res['new_sl']}")

    def test_06_phase_4_parabolic_exhaustion_harvest(self):
        """Verify Phase 4 Parabolic RSI Exhaustion harvests 85% peak cash floor."""
        res = TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle(
            epic="NVDA",
            direction="BUY",
            entry_price=130.0,
            current_price=137.0,
            sl_dist=2.0,
            spread=0.05,
            upl=8.0,          # Dropped to 8.0 from peak 10.0 (pullback <= peak * 0.85)
            peak_upl=10.0,
            scale_tier=2,
            rsi_15m=83.5       # RSI > 80.0
        )
        self.assertEqual(res["action"], "PHASE_4_PARABOLIC_HARVEST")
        self.assertEqual(res["new_scale_tier"], 4)
        self.assertTrue(res["should_close_tranche"])
        print(f"[TEST 6 PASS] Phase 4 Parabolic RSI Exhaustion Harvest verified: Action={res['action']}")


if __name__ == "__main__":
    unittest.main()
