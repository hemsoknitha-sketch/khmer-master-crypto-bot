# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - CLIENT AGREEMENT, TERMS OF SERVICE & RISK DISCLOSURE
Document Version: V.25.12.1 (Institutional Legal Citadel)
Ground Truth Authority: AGENTS.md (Invariants 1.1, 15, 23, 24, 36)

Formal Client Agreement, Terms of Service, MetaTrader 5 Execution & Risk Disclosure
harmonized between:
- GTC Global Trade Capital Co. Limited (License Number: 40354, Port Vila, Vanuatu)
- Angkor Quant AI Quantitative Intelligence Engine (Version 4.0 / AQ47)
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

AGREEMENT_VERSION = "V.25.12.1"
BROKER_ENTITY = "GTC Global Trade Capital Co. Limited"
BROKER_LICENSE = "License No. 40354 (VFSC, Vanuatu)"
BROKER_ADDRESS = "1/Floor, B&P House, Kumul Highway, Port Vila, Vanuatu"


# ─── DATABASE INITIALIZATION & TRACKING ──────────────────────────────────────

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn


def init_legal_agreement_table():
    """Initializes table for tracking user agreement acceptance."""
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
    """Records that a user has explicitly accepted the Client Agreement."""
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
    """Checks whether a user has accepted the current agreement version."""
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


# ─── NAVIGATION KEYBOARDS ───────────────────────────────────────────────────

def get_about_keyboard(current_section: str = "main", is_accepted: bool = False) -> InlineKeyboardMarkup:
    """
    Generates standardized 2.0 cm mobile-fit inline keyboards.
    All callbacks match Invariant 11 (Zero Dead Buttons).
    """
    buttons = []

    # Navigation buttons grid
    nav_row_1 = []
    if current_section != "terms":
        nav_row_1.append(InlineKeyboardButton("📜 លក្ខខណ្ឌកិច្ចព្រមព្រៀង", callback_data="btn_about_terms"))
    if current_section != "risk":
        nav_row_1.append(InlineKeyboardButton("⚠️ សេចក្តីប្រកាសហានិភ័យ", callback_data="btn_about_risk"))
    if nav_row_1:
        buttons.append(nav_row_1)

    nav_row_2 = []
    if current_section != "mt5":
        nav_row_2.append(InlineKeyboardButton("🏛️ MT5 & Latency Alpha", callback_data="btn_about_mt5"))
    if current_section != "liability":
        nav_row_2.append(InlineKeyboardButton("🛡️ ដែនកំណត់ទទួលខុសត្រូវ", callback_data="btn_about_liability"))
    if nav_row_2:
        buttons.append(nav_row_2)

    nav_row_3 = []
    if current_section != "privacy":
        nav_row_3.append(InlineKeyboardButton("🔒 ឯកជនភាព & 2FA PIN", callback_data="btn_about_privacy"))
    if current_section != "en":
        nav_row_3.append(InlineKeyboardButton("🌐 English Legal Text", callback_data="btn_about_en"))
    if nav_row_3:
        buttons.append(nav_row_3)

    # Acceptance Action Button
    if not is_accepted:
        buttons.append([InlineKeyboardButton("✅ ខ្ញុំបានអាន យល់ច្បាស់ និងយល់ព្រមកិច្ចព្រមព្រៀង", callback_data="btn_about_accept")])
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


# ─── BILINGUAL LEGAL CARDS (Khmer & English) ────────────────────────────────

def build_about_main_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Overview card introducing the Agreement, Licensing, Status & Structure."""
    status = get_user_agreement_status(chat_id)
    accepted_badge = f"✅ _បានយល់ព្រមនៅ {status['accepted_at']}_" if status["accepted"] else "⏳ _មិនទាន់បានចុចយល់ព្រម (Pending Review)_"

    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "📜 **កិច្ចព្រមព្រៀងអតិថិជន & លក្ខខណ្ឌសេវាកម្ម** 🏛️\n"
        f"**Client Agreement & Terms of Service** `{AGREEMENT_VERSION}`\n"
        f"{DIVIDER_HEAVY}\n\n"
        "🏛️ **ស្ថាប័ន & អាជ្ញាប័ណ្ណផ្លូវការ (Regulatory Entity) ៖**\n"
        f"• **ក្រុមហ៊ុនដៃគូ** ៖ `{BROKER_ENTITY}`\n"
        f"• **លេខអាជ្ញាប័ណ្ណ** ៖ `{BROKER_LICENSE}`\n"
        f"• **អាសយដ្ឋាន** ៖ `{BROKER_ADDRESS}`\n"
        "• **ប្រព័ន្ធបច្ចេកវិទ្យា** ៖ `Angkor Quant AI Engine v4.0 (AQ47)`\n\n"
        "⚖️ **ស្ថានភាពមិនមែនជាស្ថាប័នទទួលប្រាក់បញ្ញើ (Clause 39) ៖**\n"
        "សូមបញ្ជាក់យ៉ាងច្បាស់ថា ក្រុមហ៊ុន និងប្រព័ន្ធ Angkor Quant **មិនមែនជាស្ថាប័នទទួលប្រាក់បញ្ញើ (Not an Authorized Deposit-Taking Institution)** ឡើយ។ "
        "ដើមទុនទាំងអស់ស្ថិតក្នុងកាបូប Binance (Spot/Futures) ឬគណនី Broker MetaTrader 5 ផ្ទាល់ខ្លួនរបស់អ្នកប្រើប្រាស់ ១០០% (Non-Custodial)។ "
        "ប្រព័ន្ធគ្មានសិទ្ធិដកប្រាក់ចេញពីគណនីរបស់អ្នកជាដាច់ខាត!\n\n"
        "📋 **រចនាសម្ព័ន្ធកិច្ចព្រមព្រៀង ៧ ជំពូកសំខាន់ៗ ៖**\n"
        "1. **លក្ខខណ្ឌសេវាកម្ម & ការគ្រប់គ្រងទុន** (Clauses 18, 19, 20)\n"
        "2. **សេចក្តីប្រកាសហានិភ័យ & អានុភាព Leverage** (Clause 24 & Sched 1)\n"
        "3. **MetaTrader 5, Latency & Slippage Tolerance** (Clause 37)\n"
        "4. **ដែនកំណត់នៃការទទួលខុសត្រូវ & សំណង** (Clause 22 & Waiver)\n"
        "5. **ការការពារទិន្នន័យ, AML & សុវត្ថិភាព 2FA** (Clause 29)\n"
        "6. **ឧបទ្ទវហេតុប្រធានស័ក្តិ (Force Majeure)** (Clause 27)\n"
        "7. **ច្បាប់គ្រប់គ្រង & យុត្តាធិការតុលាការ** (Clause 35: Vanuatu)\n\n"
        f"📊 **ស្ថានភាពកិច្ចព្រមព្រៀងរបស់អ្នក ៖**\n{accepted_badge}\n\n"
        "👉 _សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីអានជំពូកនីមួយៗឱ្យបានច្បាស់លាស់ មុនពេលចុចយល់ព្រម!_"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("main", status["accepted"])


def build_terms_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Terms of Service: Amendment, Termination & Application of Account Funds."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "📜 **ជំពូកទី ១ ៖ លក្ខខណ្ឌកិច្ចព្រមព្រៀង & មូលនិធិគណនី** 💼\n"
        f"**Amendment, Termination & Account Funds (Clauses 18, 19, 20)**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "1️⃣ **កិច្ចសន្យាគ្រប់គ្រង Margin FX, Options & CFDs (18.1) ៖**\n"
        "កំណែកិច្ចព្រមព្រៀងដែលបានផ្សព្វផ្សាយនៅពេលអ្នកចូល Position នឹងគ្រប់គ្រងរាល់កិច្ចសន្យាជួញដូរទាំងអស់ជាផ្លូវការ។\n\n"
        "2️⃣ **សិទ្ធិកែប្រែ ឬផ្លាស់ប្តូរកិច្ចព្រមព្រៀង (18.2) ៖**\n"
        "ក្រុមហ៊ុនរក្សាសិទ្ធិកែប្រែកិច្ចព្រមព្រៀង ដោយជូនដំណឹងជាលាយលក្ខណ៍អក្សរ ផ្អែកលើហេតុផលសមស្របដូចជា៖\n"
        "• ធ្វើឱ្យខសន្យាកាន់តែច្បាស់លាស់ និងផ្តល់អត្ថប្រយោជន៍ដល់អ្នក\n"
        "• ការកែសម្រួលថ្លៃដើមសេវាកម្មស្របច្បាប់\n"
        "• ការអនុលោមតាមការផ្លាស់ប្តូរច្បាប់ បទប្បញ្ញត្តិ ឬសេចក្តីសម្រេចរបស់តុលាការ\n"
        "• ការប្រែប្រួលនៃលក្ខខណ្ឌទីផ្សារសកល\n\n"
        "3️⃣ **សិទ្ធិតវ៉ារបស់អ្នកប្រើប្រាស់ (18.3 - 14 Days Objection) ៖**\n"
        "ប្រសិនបើអ្នកមិនយល់ស្របនឹងការផ្លាស់ប្តូរ អ្នកត្រូវតែជូនដំណឹងមកយើងក្នុងរយៈពេល **១៤ ថ្ងៃ**។ ប្រសិនបើគ្មានការតវ៉ាទេ "
        "អ្នកត្រូវបានចាត់ទុកជាយល់ព្រមដោយស្វ័យប្រវត្តិ។ ក្នុងករណីអ្នកតវ៉ា គណនីរបស់អ្នកនឹងត្រូវបិទបញ្ចប់ Position ដោយសមស្រប។\n\n"
        "4️⃣ **សិទ្ធិបញ្ចប់កិច្ចព្រមព្រៀង (18.5 & 18.6) ៖**\n"
        "ទាំងអ្នកប្រើប្រាស់ និងក្រុមហ៊ុន មានសិទ្ធិបញ្ចប់កិច្ចព្រមព្រៀងនៅពេលណាក៏បាន ដោយជូនដំណឹងជាមុន។ Position បើកចំហទាំងអស់ត្រូវតែបិទបញ្ចប់ ហើយកាតព្វកិច្ចដែលនៅសេសសល់ត្រូវតែទូទាត់ឱ្យបានរួចរាល់។\n\n"
        "5️⃣ **ការអនុវត្តមូលនិធិគណនី (Clause 19) ៖**\n"
        "ក្រុមហ៊ុនមានសិទ្ធិកាត់ប្រាក់ ឬប្តូររូបិយប័ណ្ណតាមអត្រាពាណិជ្ជកម្ម ដើម្បីទូទាត់កាតព្វកិច្ចជួញដូររបស់អ្នកប្រើប្រាស់ "
        "និងមានសិទ្ធិផ្អាកការជួញដូរឧបករណ៍ណាមួយដោយជូនដំណឹងមុនយ៉ាងតិច ៧ ថ្ងៃ (Clause 20)។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("terms", status["accepted"])


def build_risk_disclosure_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Risk Disclosure, Leverage, Suitability & Anti-Guarantee Fiduciary Clause."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "⚠️ **ជំពូកទី ២ ៖ សេចក្តីប្រកាសហានិភ័យ & អានុភាព LEVERAGE** 📉\n"
        f"**Risk Disclosure, Warranties & Suitability (Clause 24 & Sched 1)**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "🚨 **ការព្រមានពីហានិភ័យខ្ពស់នៃដេរីវេទីវ (High Risk Derivatives) ៖**\n"
        "កិច្ចសន្យា Margin FX, Crypto Futures, និង CFDs គឺជាឧបករណ៍ហិរញ្ញវត្ថុដែលមានកម្រិតហានិភ័យខ្ពស់ខ្លាំង។ "
        "អានុភាព (Leverage) អាចផ្តល់ផលចំណេញខ្ពស់ ប៉ុន្តែក៏អាចបណ្តាលឱ្យអ្នក **បាត់បង់ប្រាក់ដើមទុនទាំងអស់ (Total Capital Loss)** ក្នុងរយៈពេលដ៏ខ្លី!\n\n"
        "⚖️ **ការធានា និងការយល់ព្រមរបស់អ្នកប្រើប្រាស់ (24.1) ៖**\n"
        "នៅពេលប្រើប្រាស់ប្រព័ន្ធនេះ អ្នកបញ្ជាក់ និងធានាថា៖\n"
        "• អ្នកមានសមត្ថភាពពេញលេញតាមផ្លូវច្បាប់ មិនស្ថិតក្រោមវិវាទក្ស័យធន\n"
        "• អ្នកមិនប្រើប្រាស់ប្រព័ន្ធដើម្បីជួញដូរដោយប្រើព័ត៌មានផ្ទៃក្នុង (Insider Trading) ឬការបន្លំទីផ្សារ (Market Manipulation) ឡើយ\n"
        "• **ភាពសមស្រប (Suitability 24.1.i)** ៖ អ្នកបានយល់ច្បាស់ពីហានិភ័យខ្ពស់ និងបានពិចារណាលើស្ថានភាពហិរញ្ញវត្ថុផ្ទាល់ខ្លួនរបស់អ្នក\n"
        "• **គ្មានការប្រឹក្សាផ្ទាល់ខ្លួន (24.1.l)** ៖ Angkor Quant និងក្រុមហ៊ុន មិនផ្តល់ការប្រឹក្សាផ្នែកច្បាប់ ពន្ធដារ ឬហិរញ្ញវត្ថុផ្ទាល់ខ្លួនឡើយ\n\n"
        "🛡️ **គោលការណ៍វិស្វកម្មស្មោះត្រង់ គ្មានការធានាប្រាក់ចំណេញ (AQ Invariant 1.1 & 24) ៖**\n"
        "ផ្អែកលើកតិកាសញ្ញាវិស្វកម្មស្មោះត្រង់ (Sacred Covenant of Brutal Engineering Honesty) ៖\n"
        "• ប្រព័ន្ធ Angkor Quant ដំណើរការលើគំរូគណិតវិទ្យា Mathematical Edge ($E[X] > 0$) មិនមែនជាការសន្យា ឬធានាប្រាក់ចំណេញឡើយ\n"
        "• **ដាច់ខាតគ្មានបុគ្គល ឬកូដណាអាចធានាប្រាក់ចំណេញ ១០០% បានឡើយ!**\n"
        "• អ្នកប្រើប្រាស់ជាអ្នកទទួលខុសត្រូវ ១០០% លើការកំណត់ទុន និងកម្រិត Leverage។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("risk", status["accepted"])


def build_mt5_execution_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """MetaTrader 5 Order Execution, Slippage Tolerance & Latency Standards."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🏛️ **ជំពូកទី ៣ ៖ METATRADER 5, LATENCY & SLIPPAGE TOLERANCE** ⚡\n"
        f"**Order Execution Management (Clause 37 & Tokyo HFT Bridge)**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "💻 **ដំណោះស្រាយភាគីទីបី MetaTrader 5 (Clause 37) ៖**\n"
        "MetaTrader គឺជាកម្មវិធីភាគីទីបី (Third-Party Solution) ដែលតភ្ជាប់ទៅកាន់ប្រព័ន្ធ Execution របស់ Broker។ "
        "ក្រុមហ៊ុន និង Angkor Quant មិនមានការគ្រប់គ្រងលើកំហុសបច្ចេកទេសផ្ទៃក្នុងរបស់ Software ភាគីទីបីនេះឡើយ។\n\n"
        "🎯 **Instant Orders vs Market Orders & Slippage Deviation ៖**\n"
        "• នៅពេលប្រើប្រាស់ Market Orders តម្លៃអាចនឹងរអិល (Slippage) តិចតួចនៅពេលទីផ្សារមានចលនាខ្លាំង\n"
        "• អ្នកប្រើប្រាស់អាចគ្រប់គ្រងហានិភ័យ Slippage តាមរយៈការកំណត់ Maximum Deviation នៅលើ Client Terminal (Setting Deviation = 0 ឬ 1 pip)\n\n"
        "⚡ **ការគ្រប់គ្រងភាពយឺតយ៉ាវ (Latency Management) ៖**\n"
        "• ភាពយឺតយ៉ាវបណ្តាញ (Network Latency) អាចគ្រប់គ្រងបានតាមរយៈការប្រើប្រាស់ Virtual Private Server (VPS) និងប្រព័ន្ធអ៊ីនធឺណិតល្បឿនលឿន\n"
        "• ស្ថាបត្យកម្ម Angkor Quant ត្រូវបាន Co-locate នៅតំបន់ Tokyo VPS (`asia-northeast1`) ដើម្បីរក្សា Latency កម្រិត Sub-millisecond (< 0.42 ms)\n\n"
        "🛡️ **គោលការណ៍ Slippage 1 Pip Standard (Clause 37) ៖**\n"
        "ក្រុមហ៊ុនទទួលស្គាល់ថា Latency គឺជាធម្មជាតិនៃបណ្តាញអ៊ីនធឺណិត។ ហេតុនេះ ប្រព័ន្ធអនុញ្ញាតឱ្យមាន Slippage ត្រឹម **1 Pip** "
        "ទាំងផលចំណេញ និងផលខាត។ ប្រសិនបើអតិថិជនមិនចង់ឱ្យមាន Slippage ទាល់តែសោះ ត្រូវកំណត់ Deviation = 0។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("mt5", status["accepted"])


def build_liability_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Limitation of Liability, Indemnity, Force Majeure & Governing Law."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🛡️ **ជំពូកទី ៤ ៖ ដែនកំណត់ទទួលខុសត្រូវ & យុត្តាធិការតុលាការ** ⚖️\n"
        f"**Limitation of Liability, Indemnity & Jurisdiction (Clauses 22, 27, 35)**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "1️⃣ **ដែនកំណត់នៃការទទួលខុសត្រូវ (Limitation of Liability 22.1 - 22.4) ៖**\n"
        "• ក្រុមហ៊ុន និងក្រុមការងារ Angkor Quant ទទួលខុសត្រូវត្រឹមតែការខាតបង់ណាដែលជាផលវិបាកផ្ទាល់ និងអាចព្យាករណ៍បានសមហេតុផលប៉ុណ្ណោះ\n"
        "• **មិនទទួលខុសត្រូវចំពោះការខាតបង់ប្រយោល (Indirect Losses 22.2)** ដែលកើតឡើងជាផលរំខាននៃហេតុការណ៍ចម្បងឡើយ\n"
        "• **មិនទទួលខុសត្រូវចំពោះការបាត់បង់ប្រាក់ចំណេញ ឬឱកាស (Loss of Profit / Opportunity 22.3)** ជាដាច់ខាត\n\n"
        "2️⃣ **កាតព្វកិច្ចសំណង & ការលើកលែងការទាមទារ (Indemnity 22.5 & Waiver) ៖**\n"
        "អ្នកប្រើប្រាស់យល់ព្រមការពារ និងមិនទាមទារសំណងពីក្រុមហ៊ុន បុគ្គលិក អ្នកតំណាង ឬដៃគូពាក់ព័ន្ធ ចំពោះការខាតបង់ "
        "ពន្ធដារ ការចំណាយ ឬថ្លៃមេធាវី ដែលបណ្តាលមកពីការរំលោភកិច្ចព្រមព្រៀង ឬការសម្រេចចិត្តជួញដូររបស់អ្នកឡើយ "
        "លើកលែងតែករណីដែលការខាតបង់នោះបណ្តាលមកពីការធ្វេសប្រហែសធ្ងន់ធ្ងរ (Gross Negligence) របស់ក្រុមហ៊ុនផ្ទាល់។\n\n"
        "3️⃣ **ឧបទ្ទវហេតុប្រធានស័ក្តិ (Force Majeure Clause 27) ៖**\n"
        "ក្រុមហ៊ុន និងប្រព័ន្ធមិនទទួលខុសត្រូវចំពោះការពន្យារពេល ឬការខកខានដែលបណ្តាលមកពីកត្តាហួសពីការគ្រប់គ្រង ដូចជា៖ "
        "ការដាច់ចរន្តអគ្គិសនី ការដាច់បណ្តាញទូរគមនាគមន៍សកល ការផ្អាកទីផ្សារ (Market Suspension) ឬចលាចលសង្គមឡើយ។\n\n"
        "4️⃣ **ច្បាប់គ្រប់គ្រង & យុត្តាធិការ (Governing Law Clause 35) ៖**\n"
        "កិច្ចព្រមព្រៀងនេះត្រូវបានគ្រប់គ្រង និងបកស្រាយស្របតាមច្បាប់នៃ **សាធារណរដ្ឋវ៉ានូអាទូ (Republic of Vanuatu)**។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("liability", status["accepted"])


def build_privacy_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Privacy, AML/CFT Data Compliance & 2FA Security Architecture."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🔒 **ជំពូកទី ៥ ៖ ឯកជនភាព, AML & សុវត្ថិភាព 2FA PIN** 🛡️\n"
        f"**Privacy, Anti-Money Laundering & Security Standards (Clause 29)**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "1️⃣ **ការការពារទិន្នន័យផ្ទាល់ខ្លួន & AML/CFT (Clause 29.1) ៖**\n"
        "ព័ត៌មានដែលទទួលបានពីអ្នកប្រើប្រាស់ត្រូវបានរក្សាទុក និងដំណើរការស្របតាមច្បាប់ការពារទិន្នន័យ (Data Protection) "
        "និងបទប្បញ្ញត្តិប្រឆាំងការសម្អាតប្រាក់ និងហិរញ្ញប្បទានភេរវកម្ម (Anti-Money Laundering & Counter-Terrorism Financing)។\n\n"
        "2️⃣ **ការចែករំលែកទិន្នន័យស្របច្បាប់ (Clause 29.3 & 29.4) ៖**\n"
        "ទិន្នន័យអាចត្រូវបានបង្ហាញជូនតែអាជ្ញាធរមានសមត្ថកិច្ច ឬភ្នាក់ងារត្រួតពិនិត្យអត្តសញ្ញាណ (Identity Checks) "
        "ក្នុងគោលបំណងទប់ស្កាត់បទល្មើសហិរញ្ញវត្ថុតែប៉ុណ្ណោះ។\n\n"
        "3️⃣ **ស្ថាបត្យកម្ម Non-Custodial & សុវត្ថិភាព 2FA PIN ៖**\n"
        "• ប្រព័ន្ធ Angkor Quant មិនរក្សាទុក Private Key នៃកាបូបរបស់អ្នកឡើយ\n"
        "• Binance API Keys ត្រូវបានការពារដោយការ Encrypt កម្រិតខ្ពស់ និងតម្រូវឱ្យបិទសិទ្ធិដកប្រាក់ (Withdrawal Disabled) ជានិច្ច\n"
        "• រាល់ការបញ្ជាទិញទំហំធំ ឬការកែប្រែការកំណត់យុទ្ធសាស្ត្រ តម្រូវឱ្យផ្ទៀងផ្ទាត់លេខកូដសម្ងាត់ **2FA Security PIN 4 ខ្ទង់** ជានិច្ច។"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("privacy", status["accepted"])


def build_full_english_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Official English Legal Summary directly addressing GTC Agreement V.25.12.1."""
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🌐 **GTC GLOBAL TRADE CAPITAL - CLIENT AGREEMENT SUMMARY** 🏛️\n"
        f"**Official Legal Text Overview** `{AGREEMENT_VERSION}`\n"
        f"{DIVIDER_HEAVY}\n\n"
        "🏛️ **1. Company Entity & Licensing:**\n"
        f"• **Company:** `{BROKER_ENTITY}`\n"
        f"• **License:** `{BROKER_LICENSE}`\n"
        f"• **Address:** `{BROKER_ADDRESS}`\n"
        "• **Status:** Not an Authorized Deposit-Taking Institution (Clause 39).\n\n"
        "📜 **2. Amendment & Termination (Clause 18):**\n"
        "• Current version published on the website governs all margin FX, options, and CFD contracts.\n"
        "• Company may amend with written notice for good reasons (clarity, compliance, market conditions).\n"
        "• 14-day objection window: client may object, leading to orderly position closure without penalty.\n\n"
        "⚠️ **3. Risk Disclosure & Suitability (Clause 24):**\n"
        "• Derivatives involve substantial risk of capital loss due to leverage.\n"
        "• Client warrants full legal capacity, solvency, and compliance with anti-insider trading laws.\n"
        "• Angkor Quant & GTC do not provide personalized financial, legal, or tax advice.\n\n"
        "⚡ **4. MetaTrader & Execution Latency (Clause 37):**\n"
        "• MetaTrader is a third-party solution. Latency is inherent to internet communications.\n"
        "• 1-pip slippage tolerance policy applies in both company's and client's favor.\n"
        "• Clients can control slippage via local deviation settings.\n\n"
        "⚖️ **5. Limitation of Liability & Governing Law (Clauses 22 & 35):**\n"
        "• Non-liability for indirect, consequential losses or loss of profit/opportunity.\n"
        "• Client indemnifies Company against non-gross-negligence claims.\n"
        "• Governed by and construed under the laws of the **Republic of Vanuatu**.\n\n"
        "👉 _Click the button below to accept and record your agreement._"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("en", status["accepted"])


def build_acceptance_success_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Confirmation card when user accepts the agreement."""
    status = get_user_agreement_status(chat_id)
    accepted_time = status.get("accepted_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🎉 **ការយល់ព្រមកិច្ចព្រមព្រៀងទទួលបានជោគជ័យ!** ✅\n"
        f"**Client Agreement Formally Accepted**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "📋 **ព័ត៌មានលម្អិតនៃការកត់ត្រាផ្លូវច្បាប់ ៖**\n"
        f"• **Telegram User ID** ៖ `{chat_id}`\n"
        f"• **កំណែកិច្ចព្រមព្រៀង** ៖ `{AGREEMENT_VERSION}`\n"
        f"• **កាលបរិច្ឆេទយល់ព្រម** ៖ `{accepted_time}`\n"
        "• **ស្ថានភាពគណនី** ៖ `VERIFIED & FULLY COMPLIANT ✅`\n\n"
        "💡 **សិទ្ធិ & អត្ថប្រយោជន៍ដែលបានបើកដំណើរការ ៖**\n"
        "1. ចូលប្រើប្រាស់ពេញលេញលើ **Angkor Quant AI Engine v4.0**\n"
        "2. ដំណើរការប្រព័ន្ធស្វ័យប្រវត្តិកម្ម **Turbo Hedge**, **SmartX Swarm**, និង **Trading Journal**\n"
        "3. ទទួលបានការការពារហានិភ័យដោយស្វ័យប្រវត្តិតាមស្តង់ដារ **Zero Technical Negligence**\n\n"
        "👉 _សូមចុចប៊ូតុងខាងក្រោមដើម្បីចូលទៅកាន់ផ្ទាំងបញ្ជាមេ Master Control Panel!_"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("main", is_accepted=True)
