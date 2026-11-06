# -*- coding: utf-8 -*-
"""
Unit test for ANGKOR QUANT - Manual Trade Guardian & Reverse-Turnaround Engine (AQ114).
"""
import unittest
from unittest.mock import MagicMock, patch

import capital_manual_trade_guardian as cmtg
import database as db


class MockCapitalEngine:
    def __init__(self, positions=None):
        self._positions = positions or []
        self.closed_positions = []
        self.updated_stops = []
        self.placed_orders = []

    def get_open_positions(self):
        return self._positions

    def get_market_details(self, epic):
        return {
            "success": True,
            "epic": epic,
            "spread": 0.60,
            "bid": 4050.0,
            "ask": 4050.60,
            "mid": 4050.30,
            "market_status": "TRADEABLE"
        }

    def evaluate_tradfi_quant_signal(self, epic):
        # Returns a strong Bearish signal to simulate downward market momentum
        return {
            "success": True,
            "epic": epic,
            "signal": "STRONG_SELL",
            "confidence": 85,
            "atr": 10.0,
            "rsi": 32.0,
            "market_status": "TRADEABLE"
        }

    def update_position_stops(self, deal_id, stop_loss=None, take_profit=None):
        self.updated_stops.append({"deal_id": deal_id, "sl": stop_loss, "tp": take_profit})
        return {"success": True, "deal_id": deal_id, "stopLevel": stop_loss}

    def close_position(self, deal_id):
        self.closed_positions.append(deal_id)
        # Remove from open positions
        self._positions = [p for p in self._positions if str(p.get("position", {}).get("dealId")) != str(deal_id)]
        return {"success": True, "deal_id": deal_id}

    def execute_smart_tradfi_order(self, epic, direction, size=None, sl=None, tp=None, **kwargs):
        order_info = {
            "success": True,
            "deal_id": "REVERSE_DEAL_999",
            "deal_reference": "REF_999",
            "epic": epic,
            "direction": direction,
            "size": size,
            "sl": sl,
            "tp": tp
        }
        self.placed_orders.append(order_info)
        return order_info


class TestManualTradeGuardian(unittest.TestCase):

    def test_audit_attaches_breathing_sl_to_naked_trade(self):
        naked_pos = [{
            "position": {
                "dealId": "MANUAL_101",
                "epic": "GOLD",
                "direction": "BUY",
                "size": 0.05,
                "level": 4060.0,
                "upl": -15.0,
                "stopLevel": 0.0,
                "profitLevel": 0.0
            }
        }]
        engine = MockCapitalEngine(naked_pos)
        res = cmtg.audit_and_adopt_capital_positions(engine, chat_id=859271875)

        self.assertTrue(res["success"])
        self.assertEqual(res["total_positions"], 1)
        # Verify emergency breathing SL was attached
        self.assertEqual(len(engine.updated_stops), 1)
        self.assertEqual(engine.updated_stops[0]["deal_id"], "MANUAL_101")
        self.assertGreater(engine.updated_stops[0]["sl"], 0)

        # Verify conflict was detected (BUY against STRONG_SELL signal)
        pos_audit = res["positions"][0]
        self.assertTrue(pos_audit["is_conflict"])
        self.assertEqual(pos_audit["severity"], "CRITICAL")
        self.assertEqual(pos_audit["opposing_direction"], "SELL")

    def test_audit_tightens_suicidal_sl(self):
        # Buy trade with SL suicidally far (> 15% distance)
        suicidal_pos = [{
            "position": {
                "dealId": "MANUAL_102",
                "epic": "GOLD",
                "direction": "BUY",
                "size": 0.05,
                "level": 4000.0,
                "upl": -5.0, # current_price = 4000 - (5 / 0.05) = 3900.0
                "stopLevel": 3200.0, # 20% down! Suicidal!
                "profitLevel": 0.0
            }
        }]
        engine = MockCapitalEngine(suicidal_pos)
        res = cmtg.audit_and_adopt_capital_positions(engine, chat_id=859271875)

        self.assertTrue(res["success"])
        self.assertEqual(len(engine.updated_stops), 1)
        # Tightened SL should be close to entry / market (3868.80), not suicidal 3200
        new_sl = engine.updated_stops[0]["sl"]
        self.assertGreater(new_sl, 3800.0)
        self.assertLess(new_sl, 3900.0)

    def test_execute_manual_position_reverse_flip(self):
        adverse_pos = [{
            "position": {
                "dealId": "MANUAL_103",
                "epic": "GOLD",
                "direction": "BUY",
                "size": 0.05,
                "level": 4070.0,
                "upl": -2.0, # current_price = 4070 - (2 / 0.05) = 4030.0
                "stopLevel": 3950.0,
                "profitLevel": 4150.0
            }
        }]
        engine = MockCapitalEngine(adverse_pos)
        rescue_res = cmtg.execute_manual_position_rescue(
            deal_id="MANUAL_103",
            engine=engine,
            chat_id=859271875,
            mode="REVERSE_FLIP"
        )

        self.assertTrue(rescue_res["success"])
        self.assertEqual(rescue_res["mode"], "REVERSE_FLIP")
        # Step 1: Old position was closed
        self.assertIn("MANUAL_103", engine.closed_positions)
        # Step 2: New opposite SELL order was placed
        self.assertEqual(len(engine.placed_orders), 1)
        new_order = engine.placed_orders[0]
        self.assertEqual(new_order["direction"], "SELL")
        self.assertEqual(new_order["epic"], "GOLD")
        # Structural SL above market price (4030 + safe_dist > 4030)
        self.assertGreater(new_order["sl"], 4030.0)
        # TP below market price for a SELL order
        self.assertLess(new_order["tp"], 4030.0)


    def test_format_guardian_audit_report(self):
        audit_data = {
            "success": True,
            "total_positions": 1,
            "manual_count": 1,
            "conflict_count": 1,
            "safe_count": 0,
            "positions": [{
                "deal_id": "MANUAL_104",
                "epic": "GOLD",
                "direction": "BUY",
                "size": 0.05,
                "entry_level": 4065.0,
                "current_price": 4054.0,
                "upl": -11.0,
                "sl": 4025.0,
                "status_badge": "🔴 គ្រោះថ្នាក់ (ខុសទិសដៅស្ថាប័ន)",
                "is_conflict": True,
                "conflict_reason": "ទីផ្សារធ្លាក់ចុះខ្លាំង",
                "opposing_direction": "SELL",
                "suggested_tp1": 4020.0,
                "attached_emergency_sl": True
            }]
        }
        msg, kb = cmtg.format_guardian_audit_report(audit_data, chat_id=859271875, user_lang="khmer")
        self.assertIn("ANGKOR QUANT | MANUAL TRADE GUARDIAN", msg)
        self.assertIn("GOLD", msg)
        self.assertIn("ទីផ្សារធ្លាក់ចុះខ្លាំង", msg)
        # Verify inline keyboard has reverse button
        btn_texts = [btn.text for row in kb.inline_keyboard for btn in row]
        self.assertTrue(any("បង្វែរជ័យជំនះ" in t for t in btn_texts))


if __name__ == "__main__":
    unittest.main()
