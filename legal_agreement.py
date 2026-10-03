# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - PRIVATE SYSTEM USAGE AGREEMENT & ABSOLUTE RISK WAIVER
Document Version: V.25.12.1-PRIVATE (Private Proprietary Edition)
Ground Truth Authority: AGENTS.md (Invariants 1.1, 13, 15, 23, 24)

Customized Agreement specifically for Private / Proprietary Algorithmic Software Usage:
1. 100% User Sole Financial & Operational Responsibility.
2. Platform Zero Guarantee & Absolute Disclaimer of Liability for Losses,
   Setup / Configuration Errors, Glitches, Network Downtime, or System Crashes.
3. Private Proprietary Software License ("AS IS" & "AS AVAILABLE").
4. Complete Waiver of Claims & Non-Custodial Capital Architecture.
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, Any, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ui_standards import (
    DIVIDER_HEAVY,
    DIVIDER_LIGHT,
    DIVIDER_DOUBLE,
    INSTITUTIONAL_HEADER,
    INSTITUTIONAL_FOOTER
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "bot_database.db")

AGREEMENT_VERSION = "V.25.12.1-PRIVATE"
PLATFORM_NAME = "Angkor Quant AI Quantitative Engine"
PLATFORM_CODE = "AQ47 Master System (formerly Khmer Master Crypto)"


# ─── DATABASE INITIALIZATION & TRACKING ──────────────────────────────────────

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn


def init_legal_agreement_table():
    """Initializes table for tracking user private agreement acceptance."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_legal_agreements (
            chat_id INTEGER PRIMARY KEY,
            version TEXT NOT NULL,
            accepted_at TEXT NOT NULL,
            status TEXT DEFAULT 'ACCEPTED',
            ip_source TEXT DEFAULT 'Telegram Client'
        )
    """)
    conn.commit()
    conn.close()


def record_user_agreement_acceptance(chat_id: int, version: str = AGREEMENT_VERSION) -> bool:
    """Records that a user has explicitly accepted the Private Usage Agreement."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO user_legal_agreements (chat_id, version, accepted_at, status, ip_source)
            VALUES (?, ?, ?, 'ACCEPTED', 'Telegram Client')
            ON CONFLICT(chat_id) DO UPDATE SET
                version = excluded.version,
                accepted_at = excluded.accepted_at,
                status = 'ACCEPTED'
        """, (chat_id, version, now_str))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_user_agreement_status(chat_id: int) -> Dict[str, Any]:
    """Checks whether a user has accepted the private agreement."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version, accepted_at, status FROM user_legal_agreements WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "accepted": True,
                "version": row["version"],
                "accepted_at": row["accepted_at"],
                "status": row["status"]
            }
    except Exception:
        pass
    return {"accepted": False, "version": None, "accepted_at": None, "status": "PENDING"}


# ─── NAVIGATION KEYBOARDS (Invariant 11: 100% Routed) ─────────────────────────

def get_about_keyboard(current_section: str = "main", is_accepted: bool = False) -> InlineKeyboardMarkup:
    """
    Generates standardized 2.0 cm mobile-fit inline keyboards.
    All callbacks match Invariant 11 (Zero Dead Buttons).
    """
    buttons = []

    # Navigation buttons grid
    nav_row_1 = []
    if current_section != "terms":
        nav_row_1.append(InlineKeyboardButton("📜 ការប្រើប្រាស់ឯកជន", callback_data="btn_about_terms"))
    if current_section != "risk":
        nav_row_1.append(InlineKeyboardButton("⚠️ ហានិភ័យ & ទទួលខុសត្រូវ", callback_data="btn_about_risk"))
    if nav_row_1:
        buttons.append(nav_row_1)

    nav_row_2 = []
    if current_section != "mt5":
        nav_row_2.append(InlineKeyboardButton("⚙️ កំហុសរៀបចំ & គាំងប្រព័ន្ធ", callback_data="btn_about_mt5"))
    if current_section != "liability":
        nav_row_2.append(InlineKeyboardButton("🛡️ គ្មានការធានា & លះបង់សំណង", callback_data="btn_about_liability"))
    if nav_row_2:
        buttons.append(nav_row_2)

    nav_row_3 = []
    if current_section != "privacy":
        nav_row_3.append(InlineKeyboardButton("🔒 ឯកជនភាព & 2FA PIN", callback_data="btn_about_privacy"))
    if current_section != "en":
        nav_row_3.append(InlineKeyboardButton("🌐 English Private Terms", callback_data="btn_about_en"))
    if nav_row_3:
        buttons.append(nav_row_3)

    # Acceptance Action Button
    if not is_accepted:
        buttons.append([InlineKeyboardButton("✅ ខ្ញុំយល់ព្រមទទួលខុសត្រូវខ្លួនឯង & មិនទាមទារសំណង", callback_data="btn_about_accept")])
    else:
        buttons.append([InlineKeyboardButton("✅ បានយល់ព្រមកិច្ចព្រមព្រៀងរួចរាល់ (Accepted)", callback_data="btn_about_menu")])

    # Return to Main / Master Menu
    if current_section != "main":
        buttons.append([
            InlineKeyboardButton("📜 ទំព័រដើមកិច្ចព្រមព្រៀង", callback_data="btn_about_menu"),
            InlineKeyboardButton("🔙 ត្រឡប់ទៅ Menu មេ", callback_data="btn_menu_refresh")
        ])
    else:
        buttons.append([InlineKeyboardButton("🔙 ត្រឡប់ទៅ Master Control Panel", callback_data="btn_menu_refresh")])

    return InlineKeyboardMarkup(buttons)


# ─── BILINGUAL PRIVATE LEGAL CARDS (Khmer & English) ─────────────────────────

def build_about_main_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Overview card introducing the Private Usage Agreement, Risk Disclaimer & Structure."""
    status = get_user_agreement_status(chat_id)
    accepted_badge = f"✅ _បានយល់ព្រមនៅ {status['accepted_at']}_" if status["accepted"] else "⏳ _មិនទាន់បានចុចយល់ព្រម (Pending Review)_"

    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "📜 **កិច្ចព្រមព្រៀងប្រើប្រាស់ប្រព័ន្ធឯកជន & ការលះបង់ការទាមទារសំណង** 🛡️\n"
        f"**Private Quantitative Software Agreement & Risk Waiver** `{AGREEMENT_VERSION}`\n"
        f"{DIVIDER_HEAVY}\n\n"
        "🏛️ **លក្ខណៈនៃប្រព័ន្ធ & គោលបំណងឯកជន (Private Proprietary System) ៖**\n"
        f"• **ឈ្មោះប្រព័ន្ធ** ៖ `{PLATFORM_NAME}`\n"
        f"• **កូដស្ថាបត្យកម្ម** ៖ `{PLATFORM_CODE}`\n"
        "• **ប្រភេទនៃការប្រើប្រាស់** ៖ `ការស្រាវជ្រាវ & ជួញដូរជាលក្ខណៈឯកជន (Private Personal Use Only)`\n"
        "• **លក្ខណៈដើមទុន** ៖ `Non-Custodial ១០០% (គ្រប់គ្រងក្នុងគណនីផ្ទាល់ខ្លួនរបស់អ្នក)`\n\n"
        "⚖️ **គោលការណ៍គ្រឹះនៃការទទួលខុសត្រូវ & គ្មានការធានា (Core Principles) ៖**\n"
        "1️⃣ **ការទទួលខុសត្រូវដោយខ្លួនឯង ១០០% ៖** អ្នកប្រើប្រាស់ជាអ្នកសម្រេចចិត្តដោយស្ម័គ្រចិត្តក្នុងការដាក់ទុន បើក/បិទ Position និងជ្រើសរើស Leverage។ រាល់ការខាតបង់ ឬហានិភ័យហិរញ្ញវត្ថុណាមួយ គឺជាការទទួលខុសត្រូវទាំងស្រុងរបស់អ្នកប្រើប្រាស់តែម្នាក់ឯង។\n"
        "2️⃣ **ប្រព័ន្ធមិនធានាចំពោះការខាតបង់ឡើយ ៖** គ្មានការធានាប្រាក់ចំណេញ ឬធានាមិនខាតបង់នោះឡើយ។\n"
        "3️⃣ **ប្រព័ន្ធមិនទទួលខុសត្រូវចំពោះកំហុសឆ្គងក្នុងការរៀបចំ ៖** ការកំណត់ខុសពីសំណាក់អ្នកប្រើប្រាស់ ដូចជាទំហំទុន Leverage ឬ API មិនស្ថិតក្រោមការទទួលខុសត្រូវរបស់ប្រព័ន្ធឡើយ។\n"
        "4️⃣ **ប្រព័ន្ធមិនទទួលខុសត្រូវចំពោះការរអាក់រអួល ឬគាំងដំណើរការ ៖** បញ្ហាដាច់អ៊ីនធឺណិត ការគាំង VPS កំហុសកូដ Bug ឬការគាំង Server Exchange មិនអាចយកជាមូលដ្ឋានទាមទារសំណងបានឡើយ។\n\n"
        f"📊 **ស្ថានភាពកិច្ចព្រមព្រៀងរបស់អ្នក ៖**\n{accepted_badge}\n\n"
        "👉 _សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីពិនិត្យលម្អិតជំពូកនីមួយៗ មុនពេលចុចយល់ព្រម!_"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("main", status["accepted"])


def build_terms_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Terms of Private Use, Non-Custodial Architecture & Proprietary IP."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "📜 **ជំពូកទី ១ ៖ លក្ខខណ្ឌនៃការប្រើប្រាស់ជាលក្ខណៈឯកជន** 💼\n"
        f"**Private Proprietary License & Non-Custodial Terms**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "1️⃣ **គោលបំណងនៃការប្រើប្រាស់ជាលក្ខណៈឯកជន ៖**\n"
        "ប្រព័ន្ធ Angkor Quant ត្រូវបានរៀបចំ និងផ្តល់ជូនសម្រាប់តែការស្រាវជ្រាវ វិភាគគណិតវិទ្យា និងការជួញដូរស្វ័យប្រវត្តិតាមលក្ខណៈ **ឯកជនផ្ទាល់ខ្លួន (Private Personal Use)** ឬក្នុងរង្វង់ VIP ឯកជនដែលទទួលបានការអនុញ្ញាតតែប៉ុណ្ណោះ។\n\n"
        "2️⃣ **ស្ថានភាពមិនមែនជាស្ថាប័នហិរញ្ញវត្ថុសាធារណៈ ៖**\n"
        "• ប្រព័ន្ធនេះ **មិនមែន** ជាធនាគារ ស្ថាប័នទទួលប្រាក់បញ្ញើ ឬមូលនិធិគ្រប់គ្រងប្រាក់វិនិយោគសាធារណៈ (No Fund Management) ឡើយ\n"
        "• ប្រព័ន្ធមិនផ្តល់សេវាកម្មប្រឹក្សាវិនិយោគ ហិរញ្ញវត្ថុ គណនេយ្យ ឬច្បាប់ផ្ទាល់ខ្លួនដល់សាធារណជនឡើយ\n"
        "• ដើមទុនទាំងអស់ស្ថិតក្នុងគណនី Binance ឬ MT5 Broker ផ្ទាល់ខ្លួនរបស់អ្នកប្រើប្រាស់ ១០០% (Non-Custodial) ដោយប្រព័ន្ធគ្មានសិទ្ធិដកប្រាក់ឡើយ\n\n"
        "3️⃣ **ការផ្តល់ជូនតាមស្ថានភាពជាក់ស្តែង (\"AS IS\") ៖**\n"
        "កម្មវិធីកូដ និងប្រព័ន្ធស្វ័យប្រវត្តិត្រូវបានផ្តល់ជូន \"តាមស្ថានភាពជាក់ស្តែង\" (AS IS) និង \"តាមដែលអាចរកបាន\" (AS AVAILABLE) ដោយគ្មានការធានាលើលទ្ធផល ភាពឥតខ្ចោះ ឬការសមស្របសម្រាប់គោលដៅវិនិយោគជាក់លាក់ណាមួយឡើយ\n\n"
        "4️⃣ **សិទ្ធិកម្មសិទ្ធិបញ្ញា & ការរក្សាការសម្ងាត់ ៖**\n"
        "កូដប្រព័ន្ធ យុទ្ធសាស្ត្រ Quant និងរូបមន្តគណិតវិទ្យាទាំងអស់ជាកម្មសិទ្ធិបញ្ញាផ្តាច់មុខ។ ហាមដាច់ខាតការលួចចម្លង ចែករំលែកជាសាធារណៈ ឬកែច្នៃចែកចាយបន្តដោយគ្មានការអនុញ្ញាតជាលាយលក្ខណ៍អក្សរ។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("terms", status["accepted"])


def build_risk_disclosure_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """100% User Sole Financial & Operational Risk Responsibility."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "⚠️ **ជំពូកទី ២ ៖ ការទទួលខុសត្រូវលើការខាតបង់ & ហានិភ័យដោយខ្លួនឯង** 📉\n"
        f"**100% User Sole Financial Responsibility & Anti-Guarantee Covenant**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "🚨 **ហានិភ័យទីផ្សារ & អានុភាព Leverage ៖**\n"
        "ការជួញដូររូបិយប័ណ្ណឌីជីថល (Crypto Spot / Futures) និង Forex / Gold ផ្ទុកនូវកម្រិតហានិភ័យខ្ពស់បំផុត និងភាពប្រែប្រួលតម្លៃខ្លាំងក្លាដែលមិនអាចព្យាករណ៍ទុកជាមុនបាន។ "
        "ការប្រើប្រាស់អានុភាព (Leverage) អាចបង្កើនផលចំណេញ ប៉ុន្តែក៏អាចបណ្តាលឱ្យ **បាត់បង់ប្រាក់ដើមទុនទាំងអស់ (Total Capital Liquidation)** ក្នុងរយៈពេលដ៏ខ្លីបំផុត!\n\n"
        "⚖️ **ការទទួលខុសត្រូវចំពោះការខាតបង់ និងហានិភ័យដោយខ្លួនឯង ១០០% ៖**\n"
        "នៅពេលអ្នកប្រើប្រាស់ប្រព័ន្ធនេះ អ្នកបញ្ជាក់ យល់ព្រម និងធានាថា៖\n"
        "• អ្នកជាអ្នកសម្រេចចិត្តដោយស្ម័គ្រចិត្ត ១០០% ក្នុងការដាក់ទុន ការជ្រើសរើសទំហំ Position និងកម្រិត Leverage\n"
        "• រាល់ការខាតបង់ហិរញ្ញវត្ថុទាំងអស់ មិនថាបណ្តាលមកពីចលនាទីផ្សារ ឬកត្តាផ្សេងៗ គឺជាការទទួលខុសត្រូវរបស់អ្នកប្រើប្រាស់តែម្នាក់ឯងដោយខ្លួនឯង\n"
        "• អ្នកប្រើប្រាស់មានស្ថានភាពហិរញ្ញវត្ថុរឹងមាំ និងមានសមត្ថភាពពេញលេញក្នុងការទទួលយកការខាតបង់ដើមទុនដោយគ្មានផលប៉ះពាល់ដល់ជីវភាពរស់នៅ\n\n"
        "🛡️ **កតិកាសញ្ញាវិស្វកម្មស្មោះត្រង់ គ្មានការធានាប្រាក់ចំណេញ (Zero Guarantee) ៖**\n"
        "ផ្អែកលើកតិកាសញ្ញាវិស្វកម្មស្មោះត្រង់ (AQ Invariant 1.1) ៖\n"
        "• ប្រព័ន្ធដំណើរការលើប្រៀបឈ្នះបែបគណិតវិទ្យា ($E[X] > 0$) មិនមែនជាការសន្យា ឬធានាប្រាក់ចំណេញឡើយ\n"
        "• **ដាច់ខាតគ្មានបុគ្គល ឬកូដកម្មវិធីណាអាចធានាប្រាក់ចំណេញ ឬធានាថាមិនខាតបង់ជូនអ្នកប្រើប្រាស់បានឡើយ!**"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("risk", status["accepted"])


def build_mt5_execution_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Disclaimer on Setup Errors, Technical Glitches, Crashes & Downtime."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "⚙️ **ជំពូកទី ៣ ៖ កំហុសឆ្គងក្នុងការរៀបចំ & ការរអាក់រអួលគាំងប្រព័ន្ធ** ⚡\n"
        f"**Disclaimer for Setup Mistakes, System Downtime & Glitches**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "ប្រព័ន្ធ Angkor Quant, ស្ថាបនិក, វិស្វករ និងអ្នកអភិវឌ្ឍន៍ **មិនធានា និងមិនទទួលខុសត្រូវជាដាច់ខាត** ចំពោះការខាតបង់ដែលបណ្តាលមកពីកត្តាដូចខាងក្រោម៖\n\n"
        "1️⃣ **កំហុសឆ្គងក្នុងការរៀបចំរបស់អ្នកប្រើប្រាស់ (User Setup Mistakes) ៖**\n"
        "• ការបញ្ចូល API Keys, Passwords, ឬ Server Details ខុស\n"
        "• ការកំណត់ទំហំទុន (Capital Size), Margin, Lot Size ឬ Leverage មិនសមស្របនឹងសមតុល្យគណនី\n"
        "• ការជ្រើសរើស Mode ខុស (ដូចជាជ្រើសរើស Cross Margin ជំនួស Isolated, ឬបើកកាក់ខុស)\n"
        "• ការចុចបញ្ជា Manual ខុសក្បួន ឬការកែប្រែកូដ/ប៉ារ៉ាម៉ែត្រដោយខ្លួនឯង\n\n"
        "2️⃣ **ការរអាក់រអួល ឬគាំងដំណើរការរបស់ប្រព័ន្ធ (Downtime & System Crashes) ៖**\n"
        "• ការគាំងប្រព័ន្ធកូដ (Software Glitches / Crashes / Exceptions)\n"
        "• ការដាច់ចរន្តអគ្គិសនី ឬម៉ាស៊ីនបម្រើការ VPS Reboot / Maintenance\n"
        "• ភាពយឺតយ៉ាវបណ្តាញអ៊ីនធឺណិត (Network Latency Spikes / Packet Loss)\n"
        "• ការរអាក់រអួល ឬដាច់សេវា Telegram Bot API\n\n"
        "3️⃣ **កត្តាភាគីទីបី (Third-Party Outages & Market Slippage) ៖**\n"
        "• ការគាំង ឬ Freeze នៃម៉ាស៊ីនបម្រើការ Binance Exchange ឬ MetaTrader 5 Broker\n"
        "• ការរអិលថ្លៃ (Slippage) និង Spread រីកធំពេលទីផ្សារប្រែប្រួលខ្លាំង\n"
        "• ការបដិសេធ Order (Errors -1013, -4061, -4411) ឬការផ្អាកទីផ្សារ (Trading Halted)។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("mt5", status["accepted"])


def build_liability_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Total Disclaimer of Liability, Waiver of Claims & Indemnity."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🛡️ **ជំពូកទី ៤ ៖ គ្មានការធានា & ការលះបង់ការទាមទារសំណងដាច់ខាត** ⚖️\n"
        f"**Absolute Disclaimer of Liability & Complete Waiver of Claims**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "1️⃣ **ការលើកលែងការទទួលខុសត្រូវជាដាច់ខាត (Absolute Disclaimer) ៖**\n"
        "ក្នុងកម្រិតអតិបរិមាដែលអនុញ្ញាតដោយច្បាប់ ប្រព័ន្ធ Angkor Quant, ស្ថាបនិក, វិស្វករ និងអ្នកពាក់ព័ន្ធទាំងអស់ **មិនទទួលខុសត្រូវជាដាច់ខាត** ចំពោះ៖\n"
        "• ការខាតបង់ប្រាក់ដើមទុន (Direct Financial Loss) ឬការបាត់បង់ប្រាក់ចំណេញ (Loss of Profit)\n"
        "• ការបាត់បង់ឱកាសអាជីវកម្ម ឬការខាតបង់ដោយប្រយោល (Consequential / Indirect Loss)\n"
        "• រាល់ការខូចខាតដែលកើតចេញពីការប្រើប្រាស់ ការពឹងផ្អែក ឬការមិនអាចដំណើរការបាននៃប្រព័ន្ធនេះ\n\n"
        "2️⃣ **ការលះបង់ការទាមទារសំណង (Complete Waiver of Claims) ៖**\n"
        "តាមរយៈការចុចយល់ព្រម ឬការបន្តប្រើប្រាស់ប្រព័ន្ធនេះ អ្នកប្រើប្រាស់យល់ព្រមជាផ្លូវការថា៖\n"
        "• **លះបង់សិទ្ធិទាំងអស់ក្នុងការប្តឹងផ្តល់** ទាមទារសំណង ឬទាមទារការសងការខាតបង់ពីក្រុមការងារ និងប្រព័ន្ធជាដាច់ខាត\n"
        "• យល់ព្រមការពារ និងមិនទាមទារសំណង (Indemnify and Hold Harmless) ពីស្ថាបនិក និងអ្នកអភិវឌ្ឍន៍ ចំពោះរាល់ទំនួលខុសត្រូវផ្លូវច្បាប់ ឬពាក្យបណ្តឹងណាមួយ\n\n"
        "3️⃣ **ការទទួលស្គាល់ហានិភ័យពេញលេញ (Voluntary Assumption of Risk) ៖**\n"
        "អ្នកប្រើប្រាស់បញ្ជាក់ថាបានអាន យល់ច្បាស់ និងទទួលយកហានិភ័យទាំងអស់ខាងលើដោយស្ម័គ្រចិត្ត និងដោយគ្មានការបង្ខិតបង្ខំឡើយ។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("liability", status["accepted"])


def build_privacy_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Data Privacy, Non-Custodial Keys & 2FA PIN Security Standard."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🔒 **ជំពូកទី ៥ ៖ សុវត្ថិភាពទិន្នន័យ, API KEYS & 2FA PIN** 🛡️\n"
        f"**Private Security Architecture & Two-Factor Authentication**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "1️⃣ **ស្ថាបត្យកម្ម Non-Custodial សុវត្ថិភាព ៖**\n"
        "• ប្រព័ន្ធ Angkor Quant មិនរក្សាទុក Private Key នៃកាបូបគ្រីបតូរបស់អ្នកឡើយ\n"
        "• Binance API Keys ត្រូវបានការពារយ៉ាងតឹងរ៉ឹងក្នុងកម្រិត Encrypted Storage ហើយតម្រូវឱ្យ **បិទសិទ្ធិដកប្រាក់ (Withdrawal Disabled)** ជានិច្ច\n"
        "• ប្រព័ន្ធមិនអាចដក ឬផ្ទេរប្រាក់របស់អ្នកចេញពីគណនីបានឡើយ\n\n"
        "2️⃣ **កាតព្វកិច្ចសុវត្ថិភាពរបស់អ្នកប្រើប្រាស់ ៖**\n"
        "• អ្នកប្រើប្រាស់មានកាតព្វកិច្ចរក្សាការសម្ងាត់នៃគណនី Telegram ផ្ទាល់ខ្លួន API Keys និងលេខកូដសម្ងាត់ **2FA PIN ៤ ខ្ទង់** ដោយខ្លួនឯង\n"
        "• រាល់ការបញ្ជាទិញ ឬការប្រតិបត្តិការដែលផ្ញើចេញពី Telegram ID របស់អ្នក ត្រូវបានចាត់ទុកថាជាការសម្រេចចិត្តផ្ទាល់ខ្លួនរបស់អ្នកប្រើប្រាស់ជាផ្លូវការ\n\n"
        "3️⃣ **ការរក្សាការសម្ងាត់ឯកជន ៖**\n"
        "ព័ត៌មាននៃការប្រើប្រាស់របស់អ្នកត្រូវបានរក្សាទុកជាការសម្ងាត់ក្នុងទម្រង់ SQLite WAL Database មូលដ្ឋាន ដោយគ្មានការលក់ ឬចែកចាយទិន្នន័យទៅភាគីខាងក្រៅឡើយ។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("privacy", status["accepted"])


def build_full_english_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Official English Private Usage Agreement & Total Risk Waiver."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🌐 **ANGKOR QUANT - PRIVATE SYSTEM USAGE AGREEMENT** 🏛️\n"
        f"**Private Proprietary Edition & Complete Risk Waiver** `{AGREEMENT_VERSION}`\n"
        f"{DIVIDER_HEAVY}\n\n"
        "📜 **1. Private Proprietary Software License:**\n"
        "The Angkor Quant AI Quantitative Engine is provided strictly for private, personal quantitative research and autonomous execution. "
        "It is NOT a public financial service, authorized deposit-taking institution, or investment fund manager. "
        "All assets remain 100% within your personal exchange/broker accounts in a strictly non-custodial architecture.\n\n"
        "⚠️ **2. 100% User Sole Financial Responsibility:**\n"
        "Trading digital assets, futures, margin FX, and commodities involves high volatility and extreme risk of capital destruction. "
        "The user assumes 100% sole responsibility for all financial losses, liquidation events, and trading decisions. "
        "There is absolutely ZERO guarantee of profit ($E[X] > 0$ model represents mathematical edge, not a profit warranty).\n\n"
        "⚙️ **3. Disclaimer for Setup Mistakes, Glitches & Downtime:**\n"
        "The system, founders, and developers expressly disclaim ANY and ALL liability for:\n"
        "• User setup errors (wrong API keys, incorrect margin, excessive leverage, invalid lot size, or manual misconfigurations).\n"
        "• System downtime, software crashes, bugs, exceptions, VPS reboots, or network latency spikes.\n"
        "• Third-party exchange/broker outages, freeze events, execution slippage, or order rejections (-1013, -4061).\n\n"
        "🛡️ **4. Absolute Waiver of Claims & Indemnity:**\n"
        "By accessing or utilizing this system, the user irrevocably waives all rights to file claims, seek damages, or demand compensation "
        "against Angkor Quant, its developers, or its founders. Software is provided strictly 'AS IS' and 'AS AVAILABLE'.\n\n"
        "👉 _Click the button below to formally accept and record your agreement._"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("en", status["accepted"])


def build_acceptance_success_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Confirmation card when user accepts the private agreement."""
    status = get_user_agreement_status(chat_id)
    accepted_time = status.get("accepted_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🎉 **ការយល់ព្រមកិច្ចព្រមព្រៀងឯកជនទទួលបានជោគជ័យ!** ✅\n"
        f"**Private Usage Agreement Formally Accepted**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "📋 **ព័ត៌មានលម្អិតនៃការកត់ត្រា ៖**\n"
        f"• **Telegram User ID** ៖ `{chat_id}`\n"
        f"• **កំណែកិច្ចព្រមព្រៀង** ៖ `{AGREEMENT_VERSION}`\n"
        f"• **កាលបរិច្ឆេទយល់ព្រម** ៖ `{accepted_time}`\n"
        "• **ស្ថានភាពទទួលខុសត្រូវ** ៖ `យល់ព្រមទទួលខុសត្រូវខ្លួនឯង ១០០% & មិនទាមទារសំណង`\n"
        "• **ស្ថានភាពគណនី** ៖ `VERIFIED & FULLY ACTIVE ✅`\n\n"
        "💡 **សិទ្ធិ & អត្ថប្រយោជន៍ដែលបានបើកដំណើរការ ៖**\n"
        "1. ចូលប្រើប្រាស់ពេញលេញលើ **Angkor Quant AI Engine v4.0**\n"
        "2. ដំណើរការប្រព័ន្ធស្វ័យប្រវត្តិកម្ម **Turbo Hedge**, **SmartX Swarm**, និង **Trading Journal**\n"
        "3. ដំណើរការប្រព័ន្ធការពារហានិភ័យស្វ័យប្រវត្តិ **Zero Technical Negligence**\n\n"
        "👉 _សូមចុចប៊ូតុងខាងក្រោមដើម្បីចូលទៅកាន់ផ្ទាំងបញ្ជាមេ Master Control Panel!_"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("main", is_accepted=True)
