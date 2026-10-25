# -*- coding: utf-8 -*-
"""
Unit test suite for /menu - ANGKOR QUANT APEX AGI ENGINE v13.00 Master Control Panel.
Verifies:
1. Apex header presence and formatting for Admin and VIP users.
2. 5 Institutional Categories in Khmer, English, and Chinese.
3. Interactive 1-tap inline keyboard buttons mapping to all 5 categories.
4. Admin vs VIP role badges and permission isolation.
"""

import unittest
import smart_bot_guide


class TestMenuCommand(unittest.TestCase):

    def test_01_menu_rendering_khmer_admin(self):
        """Verifies /menu outputs the exact expected institutional structure in Khmer for Super Admin."""
        admin_chat_id = 859271875  # Super Admin ID
        menu_text, markup = smart_bot_guide.build_master_control_panel_payload(admin_chat_id, user_lang="km")

        self.assertIsNotNone(menu_text)
        # Check required blocks
        self.assertIn("ANGKOR QUANT / APEX AGI ENGINE v13.00", menu_text)
        self.assertIn("ស្ថានភាពប្រព័ន្ធ ៖", menu_text)
        self.assertIn("ONLINE 24/7", menu_text)
        self.assertIn("5-Model Swarm + 12 Wall Street ML Active", menu_text)
        self.assertIn("ISOLATED MARGIN", menu_text)
        self.assertIn("MASTER CONTROL PANEL", menu_text)
        self.assertIn("👑 SUPER ADMIN", menu_text)

        # Check 5 pillars
        self.assertIn("Spot Engines (គ្មានហានិភ័យ 0%)", menu_text)
        self.assertIn("/compound_grid", menu_text)
        self.assertIn("/infinity_matrix", menu_text)
        self.assertIn("Futures & Hedge (ផលចំណេញខ្ពស់)", menu_text)
        self.assertIn("/wealth", menu_text)
        self.assertIn("/turbo_hedge", menu_text)
        self.assertIn("/smartx", menu_text)
        self.assertIn("TradFi Global & MT5 (មាស/ភាគហ៊ុន)", menu_text)
        self.assertIn("/capital", menu_text)
        self.assertIn("/capital_scalp", menu_text)
        self.assertIn("/mt5", menu_text)
        self.assertIn("AI Intelligence & Radars", menu_text)
        self.assertIn("/whales", menu_text)
        self.assertIn("/analyze", menu_text)
        self.assertIn("/predict", menu_text)
        self.assertIn("Portfolio & Security", menu_text)
        self.assertIn("/portfolio", menu_text)
        self.assertIn("/balance", menu_text)
        self.assertIn("/stop", menu_text)

        # Verify buttons in keyboard
        self.assertIsNotNone(markup)
        callback_datas = [
            btn.callback_data
            for row in markup.inline_keyboard
            for btn in row
        ]
        self.assertIn("smart_cat_spot", callback_datas)
        self.assertIn("smart_cat_futures", callback_datas)
        self.assertIn("smart_cat_tradfi", callback_datas)
        self.assertIn("smart_cat_radars", callback_datas)
        self.assertIn("smart_cat_security", callback_datas)
        self.assertIn("btn_menu_portfolio", callback_datas)
        self.assertIn("btn_balance_refresh", callback_datas)
        self.assertIn("smart_cat_guide", callback_datas)
        self.assertIn("stopall_confirm_prompt", callback_datas)
        self.assertIn("btn_webapp", callback_datas)
        self.assertIn("smart_cat_admin", callback_datas)
        self.assertIn("btn_menu_refresh", callback_datas)

    def test_02_menu_rendering_vip_user(self):
        """Verifies /menu outputs VIP Quant Investor badge for non-admin users."""
        vip_chat_id = 999999999  # Normal VIP ID
        menu_text, markup = smart_bot_guide.build_master_control_panel_payload(vip_chat_id, user_lang="km")

        self.assertIsNotNone(menu_text)
        self.assertIn("💎 VERIFIED VIP QUANT INVESTOR", menu_text)
        # Admin button should NOT be present for normal users
        callback_datas = [
            btn.callback_data
            for row in markup.inline_keyboard
            for btn in row
        ]
        self.assertNotIn("smart_cat_admin", callback_datas)
        # All 5 core categories must still be present
        self.assertIn("smart_cat_spot", callback_datas)
        self.assertIn("smart_cat_futures", callback_datas)
        self.assertIn("smart_cat_tradfi", callback_datas)
        self.assertIn("smart_cat_radars", callback_datas)
        self.assertIn("smart_cat_security", callback_datas)

    def test_03_menu_rendering_english_and_chinese(self):
        """Verifies /menu outputs valid English and Chinese formats."""
        # English
        en_text, _ = smart_bot_guide.build_master_control_panel_payload(859271875, user_lang="en")
        self.assertIn("MASTER CONTROL PANEL", en_text)
        self.assertIn("SELECT AN INSTITUTIONAL ENGINE CATEGORY", en_text)
        self.assertIn("👑 SUPER ADMIN", en_text)

        # Chinese
        zh_text, _ = smart_bot_guide.build_master_control_panel_payload(859271875, user_lang="zh")
        self.assertIn("机构级主控控制台", zh_text)
        self.assertIn("请选择您要操作的量化模块", zh_text)
        self.assertIn("👑 超级管理员", zh_text)


if __name__ == "__main__":
    unittest.main()
