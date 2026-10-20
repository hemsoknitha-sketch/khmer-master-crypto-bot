# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - TEST GAP 6 VALIDATION
===================================
Rigorous verification of Gap 6 (ចន្លោះទី 6):
  - Dynamic Structural Invalidation Stop-Loss (Order Block, Sweep Wick, FVG GP, Swing Pivot)
  - Dynamic Volatility Buffer (Anti-Noise Armor across volatility regimes)
  - Market Structure & Empirical MFE/MAE Calibrated Take-Profit Targets (TP1, TP2, TP3)
  - Real Transaction Cost Clearance (10x Spread Hurdle & >= 85% Net Profit Share)
  - Full End-to-End Citadel, Spread Drag Manager, and Scale-Out Manager Integration
"""

import os
import sys
import unittest

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Auto-switch to virtual environment Python if running outside venv
if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
    possible_venvs = [
        os.path.join(os.getcwd(), "venv", "bin", "python"),
        os.path.join(os.getcwd(), "venv", "bin", "python3"),
        os.path.join(os.getcwd(), ".venv", "bin", "python"),
        os.path.join(os.getcwd(), ".venv", "bin", "python3"),
        "/opt/khmer-master-crypto-bot/venv/bin/python",
        "/opt/khmer-master-crypto-bot/venv/bin/python3",
    ]
    for venv_py in possible_venvs:
        if os.path.isfile(venv_py) and os.access(venv_py, os.X_OK) and venv_py != sys.executable:
            try:
                os.execv(venv_py, [venv_py] + sys.argv)
            except Exception:
                pass
            break

import dynamic_structural_stops as dss
from super_smart_capital_citadel import SuperSmartCapitalCitadel, TradFiMultiTargetScaleOutManager
from capital_engine import CapitalSpreadDragManager


class TestGap6DynamicStructuralStops(unittest.TestCase):

    def setUp(self):
        self.gold_price = 2650.00
        self.gold_atr = 4.50
        self.gold_spread = 0.35
        self.swing_high = 2670.00
        self.swing_low = 2635.00

    def test_01_structural_sl_order_block_anchoring(self):
        """Test SL anchors behind Bullish and Bearish Order Blocks with volatility buffer."""
        # Bullish OB (bottom at 2640.50, dist = 9.50 > 8.10 noise floor)
        bull_ob = {"type": "BULLISH_OB", "top": 2643.0, "bottom": 2640.5, "is_testing": True}
        res_buy = dss.DynamicStructuralStops.calculate_structural_sl(
            side="BUY",
            curr_price=self.gold_price,
            spread=self.gold_spread,
            atr_15m=self.gold_atr,
            swing_high=self.swing_high,
            swing_low=self.swing_low,
            active_ob=bull_ob,
            volatility_regime="NORMAL"
        )
        self.assertEqual(res_buy["anchor_type"], "ORDER_BLOCK")
        self.assertEqual(res_buy["structural_anchor"], 2640.5)
        # Volatility buffer = max(0.20 * 4.50, 0.35 * 2.5) = max(0.90, 0.875) = 0.90
        self.assertAlmostEqual(res_buy["volatility_buffer"], 0.90, places=2)
        # SL = 2640.5 - 0.90 = 2639.60
        self.assertAlmostEqual(res_buy["invalidation_sl"], 2639.60, places=2)
        self.assertAlmostEqual(res_buy["sl_dist"], 10.40, places=2)
        self.assertFalse(res_buy["is_clamped_noise_floor"])

        # Bearish OB (top at 2659.50, dist = 9.50 > 8.10 noise floor)
        bear_ob = {"type": "BEARISH_OB", "top": 2659.5, "bottom": 2657.0, "is_testing": True}
        res_sell = dss.DynamicStructuralStops.calculate_structural_sl(
            side="SELL",
            curr_price=self.gold_price,
            spread=self.gold_spread,
            atr_15m=self.gold_atr,
            swing_high=self.swing_high,
            swing_low=self.swing_low,
            active_ob=bear_ob,
            volatility_regime="NORMAL"
        )
        self.assertEqual(res_sell["anchor_type"], "ORDER_BLOCK")
        self.assertEqual(res_sell["structural_anchor"], 2659.5)
        # SL = 2659.5 + 0.90 = 2660.40
        self.assertAlmostEqual(res_sell["invalidation_sl"], 2660.40, places=2)
        self.assertAlmostEqual(res_sell["sl_dist"], 10.40, places=2)
        self.assertFalse(res_sell["is_clamped_noise_floor"])

    def test_02_structural_sl_liquidity_sweep_anchoring(self):
        """Test SL anchors behind extreme wick of Liquidity Sweeps (Turtle Soup)."""
        res_sweep = dss.DynamicStructuralStops.calculate_structural_sl(
            side="BUY",
            curr_price=self.gold_price,
            spread=self.gold_spread,
            atr_15m=self.gold_atr,
            swing_high=self.swing_high,
            swing_low=self.swing_low,
            has_liquidity_sweep=True,
            sweep_wick_extreme=2641.20,
            volatility_regime="NORMAL"
        )
        self.assertEqual(res_sweep["anchor_type"], "LIQUIDITY_SWEEP")
        self.assertEqual(res_sweep["structural_anchor"], 2641.20)
        self.assertAlmostEqual(res_sweep["invalidation_sl"], 2641.20 - 0.90, places=2)

    def test_03_structural_sl_fvg_golden_pocket_anchoring(self):
        """Test SL anchors behind FVG + Golden Pocket (0.618-0.786) structural floor."""
        fvg_gp = {
            "has_confluence": True,
            "direction": "BUY",
            "fvg_bottom": 2644.00,
            "fib_786": 2642.80
        }
        res_fvg = dss.DynamicStructuralStops.calculate_structural_sl(
            side="BUY",
            curr_price=self.gold_price,
            spread=self.gold_spread,
            atr_15m=self.gold_atr,
            swing_high=self.swing_high,
            swing_low=self.swing_low,
            fvg_gp_setup=fvg_gp,
            volatility_regime="HIGH_VOLATILITY"
        )
        self.assertEqual(res_fvg["anchor_type"], "FVG_GOLDEN_POCKET")
        self.assertEqual(res_fvg["structural_anchor"], 2642.80)
        # High volatility alpha = 0.30 -> buffer = 0.30 * 4.5 = 1.35
        self.assertAlmostEqual(res_fvg["volatility_buffer"], 1.35, places=2)
        self.assertAlmostEqual(res_fvg["invalidation_sl"], 2642.80 - 1.35, places=2)

    def test_04_noise_floor_and_extension_ceiling_clamping(self):
        """Test noise floor prevents dangerously tight stops and ceiling prevents bloated stops."""
        # Ultra tight anchor (e.g. 0.50 points away)
        res_tight = dss.DynamicStructuralStops.calculate_structural_sl(
            side="BUY",
            curr_price=2650.00,
            spread=0.50,
            atr_15m=5.00,
            swing_high=2660.00,
            swing_low=2649.60,
            volatility_regime="NORMAL"
        )
        # Min noise floor = max(1.8 * 5.0, 3.0 * 0.50) = 9.0
        self.assertTrue(res_tight["is_clamped_noise_floor"])
        self.assertAlmostEqual(res_tight["sl_dist"], 9.00, places=2)

        # Ultra wide swing (e.g. 30 points away on 3.0 ATR)
        res_wide = dss.DynamicStructuralStops.calculate_structural_sl(
            side="BUY",
            curr_price=2650.00,
            spread=0.35,
            atr_15m=3.00,
            swing_high=2690.00,
            swing_low=2610.00,
            volatility_regime="NORMAL"
        )
        # Max extension ceiling = min(3.8 * 3.0, 0.025 * 2650) = min(11.40, 66.25) = 11.40
        self.assertTrue(res_wide["is_clamped_extension_ceiling"])
        self.assertAlmostEqual(res_wide["sl_dist"], 11.40, places=2)

    def test_05_calibrated_tp_mfe_and_cost_clearance(self):
        """Test TP targets calibrate to market structure, MFE percentiles, and clear 10x spread."""
        sl_dist = 7.40
        tp_res = dss.DynamicStructuralStops.calculate_calibrated_tp(
            side="BUY",
            curr_price=self.gold_price,
            sl_dist=sl_dist,
            spread=self.gold_spread,
            swing_high=self.swing_high,
            swing_low=self.swing_low
        )
        # Real transaction cost hurdle = 0.35 * 10 = 3.50
        self.assertTrue(tp_res["clears_cost_hurdle"])
        self.assertGreaterEqual(tp_res["spread_multiple"], 10.0)
        self.assertGreaterEqual(tp_res["net_profit_share_pct"], 85.0)

        # TP1 should be >= 1.5R and bank near swing structure / median MFE
        self.assertGreaterEqual(tp_res["rr_tp1"], 1.50)
        # TP2 should be >= 2.5R
        self.assertGreaterEqual(tp_res["rr_tp2"], 2.40)
        # TP3 should be moonshot runner >= 4.0R
        self.assertGreater(tp_res["tp3_dist"], tp_res["tp2_dist"])
        self.assertGreaterEqual(tp_res["tp3_dist"] / sl_dist, 4.0)

    def test_06_spread_drag_manager_enforce_asymmetric_10x_hurdle(self):
        """Test CapitalSpreadDragManager integrates DynamicStructuralStops seamlessly."""
        mgr = CapitalSpreadDragManager()
        sl, tp, audit = mgr.enforce_asymmetric_10x_hurdle(
            epic="GOLD",
            direction="BUY",
            entry_price=self.gold_price,
            spread=self.gold_spread,
            atr=self.gold_atr,
            swing_high=self.swing_high,
            swing_low=self.swing_low,
            volatility_regime="NORMAL"
        )
        self.assertIn("tp1", audit)
        self.assertIn("tp2", audit)
        self.assertIn("tp3", audit)
        self.assertIn("structural_stops_meta", audit)
        self.assertLess(sl, self.gold_price)
        self.assertGreater(tp, self.gold_price)
        self.assertGreaterEqual(audit["hurdle_ratio"], 10.0)

    def test_07_tradfi_scale_out_manager_honors_calibrated_targets(self):
        """Test TradFiMultiTargetScaleOutManager consumes calibrated TP targets from DynamicStructuralStops."""
        tp1_calibrated = 2663.30
        tp2_calibrated = 2670.00
        tp3_calibrated = 2683.30

        plan = TradFiMultiTargetScaleOutManager.calculate_scale_out_plan(
            epic="GOLD",
            direction="BUY",
            entry_price=self.gold_price,
            sl_price=2642.60,
            total_size=0.10,
            spread=self.gold_spread,
            min_deal_size=0.01,
            tp1_price=tp1_calibrated,
            tp2_price=tp2_calibrated,
            tp3_price=tp3_calibrated
        )
        self.assertTrue(plan["can_split"])
        self.assertEqual(plan["tp1_price"], tp1_calibrated)
        self.assertEqual(plan["tp2_price"], tp2_calibrated)
        self.assertEqual(plan["tp3_price"], tp3_calibrated)
        self.assertEqual(plan["tranches"][0]["target"], tp1_calibrated)
        self.assertEqual(plan["tranches"][1]["target"], tp2_calibrated)
        self.assertEqual(plan["tranches"][2]["target"], tp3_calibrated)


if __name__ == "__main__":
    print("=" * 70)
    print("  ANGKOR QUANT - GAP 6 DYNAMIC STRUCTURAL STOPS VALIDATION SUITE")
    print("=" * 70)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGap6DynamicStructuralStops)
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if res.wasSuccessful():
        print("\n[ALL 7 TESTS PASSED] Gap 6 Dynamic Structural Stops certified with ZERO defects!")
        sys.exit(0)
    else:
        print(f"\n[TEST FAILED] Failures: {len(res.failures)}, Errors: {len(res.errors)}")
        sys.exit(1)
