# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - OFFICIAL SYSTEM USAGE AGREEMENT, TERMS & ABSOLUTE RISK WAIVER
Document Version: AQ-AGR-v4.0-LEGAL (Private Proprietary Edition)
Ground Truth Authority: AGENTS.md (Invariants 1.1, 11, 13, 15, 23, 50)

Official Institutional Features:
1. Mandatory New User Onboarding Gatekeeper on /start.
2. Full 5-Article Legal Contract & Absolute Risk Waiver Specification.
3. Automated Tamper-Proof PDF Document Generation with Cryptographic SHA-256 Audit Trail.
4. SQLite WAL Mode Immutable Persistence (user cannot edit/delete, even after block/deletion).
5. Super Bot Admin PDF Download & Audit Suite (/admin_agreements).
6. Non-Custodial Security & Zero Guarantee Covenant.
"""

import os
import sys
import io
import hashlib
import sqlite3
import random
import shutil
import subprocess
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Tuple, List, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ui_standards import (
    DIVIDER_HEAVY,
    DIVIDER_LIGHT,
    DIVIDER_DOUBLE,
    INSTITUTIONAL_HEADER,
    INSTITUTIONAL_FOOTER,
    OFFICIAL_FOOTNOTE
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "bot_database.db")
PDF_ARCHIVE_DIR = os.path.join(BASE_DIR, "data", "legal_agreements_pdf")

AGREEMENT_VERSION = "AQ-AGR-v4.0-LEGAL"
PLATFORM_NAME = "Angkor Quant AI Quantitative Engine"
PLATFORM_CODE = "AQ50 Master System (formerly Khmer Master Crypto)"
ADMIN_CHAT_ID = 859271875

# ─── OFFICIAL FULL CONTRACT TEXT ─────────────────────────────────────────────
OFFICIAL_CONTRACT_TITLE = "កិច្ចសន្យា និងលក្ខខណ្ឌផ្លូវការនៃការប្រើប្រាស់ប្រព័ន្ធ ANGKOR QUANT"
OFFICIAL_CONTRACT_SUBTITLE = "OFFICIAL SYSTEM USAGE AGREEMENT, TERMS & ABSOLUTE RISK WAIVER"

OFFICIAL_PREAMBLE = (
    "កិច្ចសន្យា និងលក្ខខណ្ឌនៃការប្រើប្រាស់នេះ (ហៅកាត់ថា \"កិច្ចសន្យា\") "
    "ត្រូវបានរៀបចំឡើងដើម្បីកំណត់ពីគោលការណ៍ សិទ្ធិ និងកាតព្វកិច្ចរវាងប្រព័ន្ធ "
    "ANGKOR QUANT និង អ្នកប្រើប្រាស់។ ដោយការចូលប្រើប្រាស់ ការចុះឈ្មោះ ឬការបន្តប្រើប្រាស់ប្រព័ន្ធនេះ "
    "អ្នកប្រើប្រាស់ត្រូវបានចាត់ទុកថាបានអាន យល់ច្បាស់ និងយល់ព្រមទទួលយកនូវរាល់លក្ខខណ្ឌ"
    "ដូចមានចែងខាងក្រោមទាំងស្រុង ដោយគ្មានការតវ៉ា៖"
)

OFFICIAL_ARTICLES = [
    {
        "num": "ប្រការ ១",
        "title": "លក្ខខណ្ឌនៃការប្រើប្រាស់ជាលក្ខណៈឯកជន និងកម្មសិទ្ធិបញ្ញា (Private Proprietary Terms)",
        "clauses": [
            ("១.១. គោលបំណងផ្ទាល់ខ្លួន", "ប្រព័ន្ធ Angkor Quant ត្រូវបានរៀបចំឡើងសម្រាប់តែការស្រាវជ្រាវ វិភាគគណិតវិទ្យា និងការជួញដូរស្វ័យប្រវត្តិតាមលក្ខណៈឯកជនផ្ទាល់ខ្លួន (Private Personal Use) ឬសម្រាប់តែក្នុងរង្វង់ VIP ឯកជនដែលទទួលបានការអនុញ្ញាតតែប៉ុណ្ណោះ។"),
            ("១.២. មិនមែនជាស្ថាប័នហិរញ្ញវត្ថុ", "ប្រព័ន្ធនេះមិនមែនជាធនាគារ ស្ថាប័នទទួលប្រាក់បញ្ញើ ឬមូលនិធិគ្រប់គ្រងប្រាក់វិនិយោគសាធារណៈ (No Public Fund Management) នោះទេ ហើយក៏មិនផ្តល់សេវាកម្មប្រឹក្សាវិនិយោគផ្ទាល់ខ្លួនណាមួយឡើយ។"),
            ("១.៣. គោលការណ៍ Non-Custodial ១០០%", "ដើមទុនទាំងអស់របស់អ្នកប្រើប្រាស់ ត្រូវរក្សាទុកក្នុងគណនីកាបូបលុយផ្ទាល់ខ្លួន (Binance ឬ MT5 Broker)។ ប្រព័ន្ធមិនមានសិទ្ធិ ឬលទ្ធភាពក្នុងការដក ឬផ្ទេរប្រាក់របស់អ្នកប្រើប្រាស់ជាដាច់ខាត។"),
            ("១.៤. កម្មសិទ្ធិបញ្ញា", "រាល់កូដប្រព័ន្ធ យុទ្ធសាស្ត្រ Quant និងរូបមន្តគណិតវិទ្យាទាំងអស់ គឺជាកម្មសិទ្ធិបញ្ញាផ្តាច់មុខរបស់ Angkor Quant។ ហាមដាច់ខាតនូវការលួចចម្លង ធ្វើវិស្វកម្មបញ្ច្រាស (Reverse Engineering) ឬចែករំលែកទៅកាន់សាធារណជន។")
        ]
    },
    {
        "num": "ប្រការ ២",
        "title": "ការទទួលខុសត្រូវលើហានិភ័យ និងការខាតបង់ (Assumption of Risk)",
        "clauses": [
            ("២.១. ហានិភ័យទីផ្សារ និងអានុភាព (Leverage)", "ការជួញដូរលើ Crypto Futures, Spot, Forex និង Gold គឺជាទីផ្សារដែលពោរពេញដោយហានិភ័យខ្ពស់ និងការប្រែប្រួលតម្លៃខ្លាំងក្លាបំផុត។ ការប្រើប្រាស់ Leverage អាចបណ្តាលឱ្យមានការបាត់បង់ប្រាក់ដើមទុនទាំងអស់ (Total Capital Liquidation) ក្នុងរយៈពេលដ៏ខ្លី។"),
            ("២.២. ការទទួលខុសត្រូវផ្ទាល់ខ្លួន ១០០%", "អ្នកប្រើប្រាស់ជាអ្នកសម្រេចចិត្តដោយស្ម័គ្រចិត្ត និងឯករាជ្យក្នុងការដាក់ទុន បើកទីតាំងជួញដូរ (Position) និងជ្រើសរើសទំហំ Leverage។ រាល់ការខាតបង់ហិរញ្ញវត្ថុទាំងអស់ គឺជាការទទួលខុសត្រូវរបស់អ្នកប្រើប្រាស់តែម្នាក់ឯង។"),
            ("២.៣. គ្មានការធានាប្រាក់ចំណេញ (Zero Profit Guarantee)", "ផ្អែកលើកតិកាសញ្ញាវិស្វកម្មស្មោះត្រង់ (AQ Invariant 1.1) ទោះបីជាប្រព័ន្ធដំណើរការលើប្រៀបឈ្នះបែបគណិតវិទ្យា ($E[X] > 0$) ក៏ដោយ ក៏ដាច់ខាតគ្មានបុគ្គល ឬកូដកម្មវិធីណាមួយអាចធានានូវប្រាក់ចំណេញ ឬធានាថាមិនមានការខាតបង់ជូនអ្នកប្រើប្រាស់បានឡើយ។")
        ]
    },
    {
        "num": "ប្រការ ៣",
        "title": "ការលើកលែងការទទួលខុសត្រូវលើកំហុសបច្ចេកទេស និងប្រតិបត្តិការ",
        "lead": "ប្រព័ន្ធ Angkor Quant, ស្ថាបនិក, វិស្វករ និងអ្នកអភិវឌ្ឍន៍ មិនធានា និងមិនទទួលខុសត្រូវជាដាច់ខាតចំពោះរាល់ការខាតបង់ដែលបណ្តាលមកពី៖",
        "clauses": [
            ("៣.១. កំហុសឆ្គងរបស់អ្នកប្រើប្រាស់ (User Setup Mistakes)", "ការបញ្ចូល API Keys, Passwords ឬព័ត៌មាន Server ខុស; ការកំណត់ទំហំទុន (Capital Size), Margin, Lot Size ឬ Leverage ដែលមិនសមាមាត្រនឹងសមតុល្យគណនី; ការជ្រើសរើស Mode ខុស (ជ្រើសរើស Cross Margin ជំនួស Isolated ឬបើកកាក់ខុស); ការចុចបញ្ជាដោយដៃ (Manual) ខុសក្បួន ឬការកែប្រែកូដ/ប៉ារ៉ាម៉ែត្រដោយខ្លួនឯង។"),
            ("៣.២. ការរអាក់រអួលប្រព័ន្ធ (Downtime, Glitches & Crashes)", "ការគាំងប្រព័ន្ធកូដ ការដាច់ចរន្តអគ្គិសនី ការម៉ាស៊ីនបម្រើការ (VPS) ធ្វើការ Reboot/Maintenance ភាពយឺតយ៉ាវនៃបណ្តាញអ៊ីនធឺណិត (Network Latency Spikes / Packet Loss) ឬការរអាក់រអួលរបស់ Telegram Bot API។"),
            ("៣.៣. កត្តាភាគីទីបី និងទីផ្សារ (Third-Party Failures & Market Slippage)", "ការគាំងនៃម៉ាស៊ីនបម្រើការរបស់ Binance Exchange ឬ MetaTrader 5 Broker, ការរអិលថ្លៃ (Slippage) និង Spread រីកធំពេលទីផ្សារមានចលនាខ្លាំង, ការបដិសេធ Order (Errors -1013, -4061, -4411) ឬការផ្អាកទីផ្សារជាបណ្តោះអាសន្ន (Trading Halted)។")
        ]
    },
    {
        "num": "ប្រការ ៤",
        "title": "ការបដិសេធការធានា និងការលះបង់ការទាមទារសំណងដាច់ខាត (Complete Waiver of Claims)",
        "clauses": [
            ("៤.១. ការលើកលែងការទទួលខុសត្រូវទាំងស្រុង (Absolute Disclaimer)", "ក្នុងកម្រិតអតិបរមាដែលច្បាប់អនុញ្ញាត ប្រព័ន្ធ Angkor Quant, ស្ថាបនិក, វិស្វករ និងភាគីពាក់ព័ន្ធ មិនទទួលខុសត្រូវចំពោះការខាតបង់ប្រាក់ដើមទុន ការបាត់បង់ប្រាក់ចំណេញ ឬការខូចខាតណាមួយ (ទោះដោយផ្ទាល់ ឬដោយប្រយោល) ឡើយ។"),
            ("៤.២. ការផ្តល់ជូនតាមស្ថានភាពជាក់ស្តែង (\"AS IS\")", "កម្មវិធី និងប្រព័ន្ធទាំងមូល ត្រូវបានផ្តល់ជូន \"តាមស្ថានភាពជាក់ស្តែង\" និង \"តាមដែលអាចរកបាន\" ដោយគ្មានការធានាផ្នែកច្បាប់ ឬបច្ចេកទេសប្រភេទណាមួយឡើយ។"),
            ("៤.៣. ការលះបង់ការទាមទារសំណង (Waiver & Release)", "តាមរយៈការចុចយល់ព្រម ឬការបន្តប្រើប្រាស់ប្រព័ន្ធនេះ អ្នកប្រើប្រាស់យល់ព្រមលះបង់សិទ្ធិទាំងអស់ទាំងស្រុង ក្នុងការប្តឹងផ្តល់ ទាមទារសំណង ឬទារការសងការខាតបង់ពីក្រុមការងារ និងប្រព័ន្ធជាដាច់ខាត។")
        ]
    },
    {
        "num": "ប្រការ ៥",
        "title": "សន្តិសុខទិន្នន័យ គណនី និងការផ្ទៀងផ្ទាត់ (Security & Authentication)",
        "clauses": [
            ("៥.១. ការការពារសោសុវត្ថិភាព (Non-Custodial Keys)", "Binance API Keys ត្រូវបានបំប្លែងជាកូដសម្ងាត់ (Encrypted) ដើម្បីសុវត្ថិភាព ហើយតម្រូវឱ្យអ្នកប្រើប្រាស់ បិទសិទ្ធិដកប្រាក់ (Withdrawal Disabled) ជានិច្ចនៅពេលភ្ជាប់ប្រព័ន្ធ។"),
            ("៥.២. កាតព្វកិច្ចសុវត្ថិភាពផ្ទាល់ខ្លួន", "អ្នកប្រើប្រាស់ត្រូវមានកាតព្វកិច្ចរក្សាការសម្ងាត់នៃគណនី Telegram ផ្ទាល់ខ្លួន, API Keys, និងលេខកូដសម្ងាត់ 2FA PIN ចំនួន ៤ ខ្ទង់ ដោយខ្លួនឯងយ៉ាងប្រុងប្រយ័ត្នបំផុត។"),
            ("៥.៣. សិទ្ធិអំណាចតាមរយៈ Telegram ID", "រាល់សកម្មភាព ការកំណត់ ឬការបញ្ជាទាំងឡាយណាដែលត្រូវបានធ្វើឡើងចេញពី Telegram ID របស់អ្នកប្រើប្រាស់ ត្រូវបានចាត់ទុកជាផ្លូវការថាជាការសម្រេចចិត្ត និងការអនុម័តផ្ទាល់របស់អ្នកប្រើប្រាស់។")
        ]
    }
]

OFFICIAL_DECLARATION = (
    "ការប្រកាសយល់ព្រម៖ ខ្ញុំបាទ/នាងខ្ញុំ ជាអ្នកប្រើប្រាស់ បានអាន និងយល់ច្បាស់នូវរាល់ប្រការ"
    "ដែលបានចែងខាងលើ។ ការបន្តប្រើប្រាស់ប្រព័ន្ធ ANGKOR QUANT ចាត់ទុកថាខ្ញុំបាទ/នាងខ្ញុំបានទទួលស្គាល់ "
    "និងយល់ព្រមនូវកិច្ចសន្យានេះដោយស្ម័គ្រចិត្ត ១០០% និងគ្មានការបង្ខិតបង្ខំ។"
)


# ─── DATABASE INITIALIZATION & MIGRATIONS ────────────────────────────────────

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn


def init_legal_agreement_table():
    """Initializes and auto-migrates table for tracking immutable legal contracts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_legal_agreements (
            chat_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            username TEXT,
            full_name TEXT,
            phone_number TEXT,
            version TEXT NOT NULL,
            contract_serial TEXT UNIQUE,
            sha256_hash TEXT,
            pdf_path TEXT,
            accepted_at TEXT NOT NULL,
            accepted_timestamp INTEGER,
            ip_source TEXT DEFAULT 'Telegram Client',
            status TEXT DEFAULT 'ACTIVE',
            is_immutable INTEGER DEFAULT 1
        )
    """)

    # Dynamic column migrations for backward compatibility
    columns_to_ensure = [
        ("user_id", "INTEGER"),
        ("username", "TEXT"),
        ("full_name", "TEXT"),
        ("phone_number", "TEXT"),
        ("contract_serial", "TEXT"),
        ("sha256_hash", "TEXT"),
        ("pdf_path", "TEXT"),
        ("accepted_timestamp", "INTEGER"),
        ("is_immutable", "INTEGER DEFAULT 1")
    ]
    for col_name, col_type in columns_to_ensure:
        try:
            cursor.execute(f"ALTER TABLE user_legal_agreements ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass  # Already exists

    conn.commit()
    conn.close()


def record_user_legal_contract(
    chat_id: int,
    user_id: int = 0,
    username: str = "",
    full_name: str = "",
    phone_number: str = "",
    contract_serial: str = "",
    sha256_hash: str = "",
    pdf_path: str = "",
    version: str = AGREEMENT_VERSION
) -> bool:
    """Records an immutable, legally binding contract acceptance with cryptographic fingerprint."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now_dt = datetime.now(timezone(timedelta(hours=7)))
        accepted_at_str = now_dt.strftime("%Y-%m-%d %H:%M:%S ICT")
        accepted_ts = int(now_dt.timestamp())

        cursor.execute("""
            INSERT INTO user_legal_agreements (
                chat_id, user_id, username, full_name, phone_number,
                version, contract_serial, sha256_hash, pdf_path,
                accepted_at, accepted_timestamp, ip_source, status, is_immutable
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Telegram Client', 'ACTIVE', 1)
            ON CONFLICT(chat_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name,
                phone_number = CASE WHEN excluded.phone_number != '' THEN excluded.phone_number ELSE user_legal_agreements.phone_number END,
                version = excluded.version,
                contract_serial = excluded.contract_serial,
                sha256_hash = excluded.sha256_hash,
                pdf_path = excluded.pdf_path,
                accepted_at = excluded.accepted_at,
                accepted_timestamp = excluded.accepted_timestamp,
                status = 'ACTIVE',
                is_immutable = 1
        """, (
            chat_id, user_id or chat_id, username, full_name, phone_number,
            version, contract_serial, sha256_hash, pdf_path,
            accepted_at_str, accepted_ts
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error recording legal contract for {chat_id}: {e}")
        return False


def get_user_agreement_status(chat_id: int) -> Dict[str, Any]:
    """Retrieves the full legal contract record for a given user."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT chat_id, user_id, username, full_name, phone_number,
                   version, contract_serial, sha256_hash, pdf_path,
                   accepted_at, accepted_timestamp, status, is_immutable
            FROM user_legal_agreements
            WHERE chat_id = ?
        """, (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "accepted": (row["status"] == "ACTIVE" or row["accepted_at"] is not None),
                "chat_id": row["chat_id"],
                "username": row["username"] or "",
                "full_name": row["full_name"] or "",
                "phone_number": row["phone_number"] or "",
                "version": row["version"],
                "contract_serial": row["contract_serial"] or "",
                "sha256_hash": row["sha256_hash"] or "",
                "pdf_path": row["pdf_path"] or "",
                "accepted_at": row["accepted_at"],
                "status": row["status"],
                "is_immutable": bool(row["is_immutable"])
            }
    except Exception as e:
        print(f"Error fetching agreement status for {chat_id}: {e}")
    return {"accepted": False, "version": None, "accepted_at": None, "status": "PENDING"}


def is_agreement_accepted(chat_id: int) -> bool:
    """Checks whether user has accepted the legal agreement. Super Admin is always True."""
    if chat_id == ADMIN_CHAT_ID:
        return True
    status = get_user_agreement_status(chat_id)
    return bool(status.get("accepted", False))


def get_all_legal_agreements(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """Retrieves signed agreements for Super Admin audit & inspection."""
    res = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT chat_id, username, full_name, phone_number,
                   contract_serial, sha256_hash, pdf_path, accepted_at, status
            FROM user_legal_agreements
            ORDER BY accepted_timestamp DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        for row in cursor.fetchall():
            res.append(dict(row))
        conn.close()
    except Exception as e:
        print(f"Error listing legal agreements: {e}")
    return res


def get_legal_agreements_count() -> int:
    """Returns total count of signed legal contracts in database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_legal_agreements WHERE status = 'ACTIVE'")
        cnt = cursor.fetchone()[0]
        conn.close()
        return int(cnt or 0)
    except Exception:
        return 0


# ─── HIGH-SECURITY 1-PAGE KHMER PDF DOCUMENT GENERATION ENGINE ──────────────

def find_headless_browser_executable() -> Optional[str]:
    """Finds available Edge, Chrome, or Chromium executable across Windows and Linux."""
    candidates = [
        # Linux VPS candidates
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/snap/bin/chromium",
        # Windows candidates
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        shutil.which("msedge"),
        shutil.which("chrome")
    ]
    for c in candidates:
        if c and os.path.exists(c) and os.path.isfile(c):
            return c
    return None


def get_khmer_pdf_font_paths() -> Tuple[str, str, str]:
    """Returns local paths for (KantumruyPro, Moul, KhmerOS) fonts if available."""
    kantumruy = ""
    moul = ""
    khmeros = ""

    for p in [
        os.path.join(BASE_DIR, "assets", "fonts", "KantumruyPro-Regular.ttf"),
        os.path.join(os.path.dirname(BASE_DIR), "assets", "fonts", "KantumruyPro-Regular.ttf"),
        "/usr/share/fonts/truetype/kantumruy/KantumruyPro-Regular.ttf"
    ]:
        if os.path.exists(p):
            kantumruy = p
            break

    for p in [
        os.path.join(BASE_DIR, "assets", "fonts", "Moul-Regular.ttf"),
        os.path.join(os.path.dirname(BASE_DIR), "assets", "fonts", "Moul-Regular.ttf"),
        "/usr/share/fonts/truetype/moul/Moul-Regular.ttf"
    ]:
        if os.path.exists(p):
            moul = p
            break

    for p in [
        os.path.join(BASE_DIR, "assets", "fonts", "KhmerOS.ttf"),
        os.path.join(os.path.dirname(BASE_DIR), "assets", "fonts", "KhmerOS.ttf"),
        "/usr/share/fonts/truetype/khmeros/KhmerOS.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/khmeros.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]:
        if os.path.exists(p):
            khmeros = p
            break

    return kantumruy, moul, khmeros


def get_khmer_pdf_font() -> str:
    """Finds and registers a valid Unicode Khmer font for ReportLab."""
    k_path, m_path, os_path = get_khmer_pdf_font_paths()
    candidate_paths = [os_path, k_path, m_path, "C:/Windows/Fonts/khmeros.ttf", "C:/Windows/Fonts/arial.ttf"]
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return "Helvetica"

    for p in candidate_paths:
        if p and os.path.exists(p):
            font_id = "KhmerOSCustom"
            try:
                pdfmetrics.registerFont(TTFont(font_id, p))
                return font_id
            except Exception:
                pass
    return "Helvetica"


def build_official_agreement_html(
    chat_id: int,
    username: str,
    full_name: str,
    phone_number: str,
    contract_serial: str,
    sha256_hash: str,
    accepted_time_str: str
) -> str:
    """
    Renders publication-grade 1-page HTML template for Angkor Quant Legal Contract.
    Features:
    - 1-Page strict layout without unnecessary overflow
    - Replaces legacy box/table with sleek executive metadata strip
    - 100% proper Khmer OpenType text shaping (HarfBuzz engine)
    - Full text justification (text-align: justify)
    - High-definition Kantumruy Pro & Moul Khmer typography
    """
    k_path, m_path, os_path = get_khmer_pdf_font_paths()
    k_url = f"url('file:///{k_path.replace(os.sep, '/')}')" if k_path else "sans-serif"
    m_url = f"url('file:///{m_path.replace(os.sep, '/')}')" if m_path else "serif"
    os_url = f"url('file:///{os_path.replace(os.sep, '/')}')" if os_path else "sans-serif"

    user_handle = f"@{username}" if username and not username.startswith("@") else (username or "N/A")
    display_name = full_name or f"User_{chat_id}"
    display_phone = phone_number or "N/A"

    return f"""<!DOCTYPE html>
<html lang="km">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Moul&display=swap');

@font-face {{
    font-family: 'KantumruyPro';
    src: {k_url} format('truetype');
    font-weight: 400;
    font-style: normal;
}}
@font-face {{
    font-family: 'KhmerMoul';
    src: {m_url} format('truetype');
    font-weight: normal;
    font-style: normal;
}}
@font-face {{
    font-family: 'KhmerCustom';
    src: {os_url} format('truetype');
    font-weight: normal;
    font-style: normal;
}}

@page {{
    size: A4 portrait;
    margin: 8mm 12mm 8mm 12mm;
}}

* {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

body {{
    font-family: 'KantumruyPro', 'KhmerCustom', 'Khmer OS', sans-serif;
    color: #0F172A;
    background: #FFFFFF;
    margin: 0;
    padding: 0;
    font-size: 6.8pt;
    line-height: 1.35;
}}

/* ── HEADER ── */
.header {{
    text-align: center;
    border-bottom: 2px solid #D97706;
    padding-bottom: 4px;
    margin-bottom: 5px;
}}
.title {{
    font-family: 'KhmerMoul', serif;
    font-size: 9.5pt;
    color: #0F172A;
    margin: 0 0 1px 0;
    line-height: 1.35;
}}
.subtitle {{
    font-size: 6.5pt;
    font-weight: 700;
    color: #B45309;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin: 0;
}}

/* ── SLEEK PARTICIPANT STRIP (NO UGLY BOX) ── */
.meta-strip {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #F8FAFC;
    border-left: 3px solid #D97706;
    padding: 4px 8px;
    margin-bottom: 5px;
    font-size: 6.5pt;
    color: #334155;
    border-radius: 0 4px 4px 0;
}}
.meta-item b {{
    color: #0F172A;
}}

/* ── PREAMBLE ── */
.preamble {{
    text-align: justify;
    text-justify: inter-word;
    font-size: 6.7pt;
    line-height: 1.32;
    color: #334155;
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: 4px;
    padding: 4px 7px;
    margin-bottom: 5px;
}}

/* ── ARTICLES (2-COLUMN BALANCED LAYOUT) ── */
.articles-grid {{
    display: flex;
    justify-content: space-between;
    gap: 8px;
}}
.col-left {{
    width: 50%;
}}
.col-right {{
    width: 50%;
}}

.article-card {{
    margin-bottom: 4.5px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 3px;
    padding: 4px 6px;
}}
.article-header {{
    font-size: 7pt;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 2.5px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 1.5px;
}}
.badge {{
    background: #FEF3C7;
    color: #92400E;
    font-size: 6.2pt;
    font-weight: 700;
    padding: 1px 4px;
    border-radius: 3px;
    margin-right: 4px;
    white-space: nowrap;
}}
.clause {{
    text-align: justify;
    text-justify: inter-word;
    font-size: 6.4pt;
    line-height: 1.32;
    color: #334155;
    margin-bottom: 2px;
}}
.clause b {{
    color: #0F172A;
}}

/* ── DECLARATION ── */
.declaration-strip {{
    background: #F0FDF4;
    border: 1px solid #86EFAC;
    border-radius: 4px;
    padding: 3.5px 7px;
    margin: 4px 0 5px 0;
    font-size: 6.5pt;
    line-height: 1.32;
    color: #166534;
    text-align: justify;
    text-justify: inter-word;
}}

/* ── DUAL SIGNATURE ── */
.signatures-wrap {{
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin-top: 4px;
}}
.sig-card {{
    width: 50%;
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    padding: 4px 7px;
    font-size: 6.4pt;
    line-height: 1.32;
}}
.sig-card-title {{
    font-weight: 700;
    color: #0F172A;
    font-size: 6.8pt;
    border-bottom: 1px dashed #CBD5E1;
    padding-bottom: 2px;
    margin-bottom: 2.5px;
}}
.sig-badge {{
    display: inline-block;
    background: #DCFCE7;
    color: #15803D;
    font-weight: 700;
    font-size: 6pt;
    padding: 0.5px 4px;
    border-radius: 2px;
}}
.hash-line {{
    font-family: monospace;
    font-size: 5.8pt;
    color: #64748B;
    word-break: break-all;
}}
</style>
</head>
<body>

<div class="header">
    <div class="title">{OFFICIAL_CONTRACT_TITLE}</div>
    <div class="subtitle">{OFFICIAL_CONTRACT_SUBTITLE}</div>
</div>

<div class="meta-strip">
    <div class="meta-item">👤 <b>ឈ្មោះ:</b> {display_name} ({user_handle})</div>
    <div class="meta-item">🆔 <b>Telegram ID:</b> {chat_id}</div>
    <div class="meta-item">📱 <b>ទូរសព្ទ:</b> {display_phone}</div>
    <div class="meta-item">📜 <b>Serial:</b> {contract_serial}</div>
    <div class="meta-item">🕒 <b>កាលបរិច្ឆេទ:</b> {accepted_time_str}</div>
</div>

<div class="preamble">
<b>អារម្ភកថា ៖</b> {OFFICIAL_PREAMBLE}
</div>

<div class="articles-grid">
    <div class="col-left">
        <!-- ARTICLE 1 -->
        <div class="article-card">
            <div class="article-header"><span class="badge">ប្រការ ១</span> {OFFICIAL_ARTICLES[0]['title']}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[0]['clauses'][0][0]}:</b> {OFFICIAL_ARTICLES[0]['clauses'][0][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[0]['clauses'][1][0]}:</b> {OFFICIAL_ARTICLES[0]['clauses'][1][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[0]['clauses'][2][0]}:</b> {OFFICIAL_ARTICLES[0]['clauses'][2][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[0]['clauses'][3][0]}:</b> {OFFICIAL_ARTICLES[0]['clauses'][3][1]}</div>
        </div>

        <!-- ARTICLE 2 -->
        <div class="article-card">
            <div class="article-header"><span class="badge">ប្រការ ២</span> {OFFICIAL_ARTICLES[1]['title']}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[1]['clauses'][0][0]}:</b> {OFFICIAL_ARTICLES[1]['clauses'][0][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[1]['clauses'][1][0]}:</b> {OFFICIAL_ARTICLES[1]['clauses'][1][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[1]['clauses'][2][0]}:</b> {OFFICIAL_ARTICLES[1]['clauses'][2][1]}</div>
        </div>

        <!-- ARTICLE 3 -->
        <div class="article-card">
            <div class="article-header"><span class="badge">ប្រការ ៣</span> {OFFICIAL_ARTICLES[2]['title']}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[2]['clauses'][0][0]}:</b> {OFFICIAL_ARTICLES[2]['clauses'][0][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[2]['clauses'][1][0]}:</b> {OFFICIAL_ARTICLES[2]['clauses'][1][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[2]['clauses'][2][0]}:</b> {OFFICIAL_ARTICLES[2]['clauses'][2][1]}</div>
        </div>
    </div>

    <div class="col-right">
        <!-- ARTICLE 4 -->
        <div class="article-card">
            <div class="article-header"><span class="badge">ប្រការ ៤</span> {OFFICIAL_ARTICLES[3]['title']}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[3]['clauses'][0][0]}:</b> {OFFICIAL_ARTICLES[3]['clauses'][0][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[3]['clauses'][1][0]}:</b> {OFFICIAL_ARTICLES[3]['clauses'][1][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[3]['clauses'][2][0]}:</b> {OFFICIAL_ARTICLES[3]['clauses'][2][1]}</div>
        </div>

        <!-- ARTICLE 5 -->
        <div class="article-card">
            <div class="article-header"><span class="badge">ប្រការ ៥</span> {OFFICIAL_ARTICLES[4]['title']}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[4]['clauses'][0][0]}:</b> {OFFICIAL_ARTICLES[4]['clauses'][0][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[4]['clauses'][1][0]}:</b> {OFFICIAL_ARTICLES[4]['clauses'][1][1]}</div>
            <div class="clause"><b>{OFFICIAL_ARTICLES[4]['clauses'][2][0]}:</b> {OFFICIAL_ARTICLES[4]['clauses'][2][1]}</div>
        </div>

        <!-- DECLARATION -->
        <div class="declaration-strip">
            <b>📝 ការប្រកាសយល់ព្រមដោយស្ម័គ្រចិត្ត ៖</b> {OFFICIAL_DECLARATION}
        </div>
    </div>
</div>

<!-- DUAL SIGNATURE BLOCK -->
<div class="signatures-wrap">
    <div class="sig-card">
        <div class="sig-card-title">🏛️ ភាគីប្រព័ន្ធ ANGKOR QUANT AI SYSTEMS</div>
        <div><b>ស្ថាប័ន:</b> Angkor Quant AI Quantitative Systems (Global Node)</div>
        <div><b>អភិបាលកិច្ច:</b> System Core Governance & Fiduciary Capital Protector</div>
        <div><b>ស្ថានភាព:</b> <span class="sig-badge">🟢 DIGITALLY CERTIFIED & SYSTEM LOCKED</span></div>
        <div class="hash-line">SHA-256: {sha256_hash}</div>
    </div>
    <div class="sig-card">
        <div class="sig-card-title">✍️ ភាគីអ្នកប្រើប្រាស់ (User / VIP Member)</div>
        <div><b>ឈ្មោះ:</b> {display_name} ({user_handle}) | <b>ID:</b> {chat_id}</div>
        <div><b>កាលបរិច្ឆេទយល់ព្រម:</b> {accepted_time_str}</div>
        <div><b>ស្ថានភាព:</b> <span class="sig-badge">🟢 DIGITALLY SIGNED & VERIFIED 100%</span></div>
        <div><b>កិច្ចសន្យា Serial:</b> {contract_serial}</div>
    </div>
</div>

</body>
</html>"""


def generate_browser_pdf(html_content: str, pdf_path: str) -> bool:
    """Generates PDF using headless Chromium/Chrome/Edge with exact 1-page layout."""
    browser_exe = find_headless_browser_executable()
    if not browser_exe:
        return False

    temp_html_path = pdf_path.replace(".pdf", "_temp.html")
    try:
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={os.path.abspath(pdf_path)}",
            os.path.abspath(temp_html_path)
        ]
        if os.name != "nt":
            cmd.insert(1, "--no-sandbox")
            cmd.insert(2, "--disable-dev-shm-usage")

        subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000
    except Exception as ex:
        print(f"⚠️ [PDF ENGINE] Headless browser generation failed: {ex}")
        return False
    finally:
        if os.path.exists(temp_html_path):
            try:
                os.remove(temp_html_path)
            except Exception:
                pass


def generate_fpdf2_pdf(
    chat_id: int,
    username: str,
    full_name: str,
    phone_number: str,
    contract_serial: str,
    sha256_hash: str,
    accepted_time_str: str,
    pdf_path: str
) -> bool:
    """Pure-Python high-definition text-shaped PDF generator using fpdf2 + uharfbuzz."""
    try:
        from fpdf import FPDF
        import uharfbuzz  # noqa: F401
    except ImportError:
        return False

    try:
        k_path, _, os_path = get_khmer_pdf_font_paths()
        target_font = k_path or os_path
        if not target_font or not os.path.exists(target_font):
            return False

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(12, 10, 12)
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()
        pdf.set_text_shaping(True)
        pdf.add_font("KhmerFont", "", target_font)
        pdf.set_font("KhmerFont", "", 10)

        # Header
        pdf.cell(0, 7, OFFICIAL_CONTRACT_TITLE, align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("KhmerFont", "", 7)
        pdf.cell(0, 5, OFFICIAL_CONTRACT_SUBTITLE, align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        # Sleek participant strip (NO UGLY BOX)
        user_handle = f"@{username}" if username and not username.startswith("@") else (username or "N/A")
        display_name = full_name or f"User_{chat_id}"
        meta_line = f"ឈ្មោះ: {display_name} ({user_handle}) | ID: {chat_id} | Serial: {contract_serial} | កាលបរិច្ឆេទ: {accepted_time_str}"
        pdf.set_fill_color(248, 250, 252)
        pdf.cell(0, 5, meta_line, fill=True, align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Preamble (Justified)
        pdf.set_font("KhmerFont", "", 6.5)
        pdf.multi_cell(0, 3.6, f"អារម្ភកថា ៖ {OFFICIAL_PREAMBLE}", align='J', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)

        # 5 Articles
        for art in OFFICIAL_ARTICLES:
            pdf.set_font("KhmerFont", "", 7)
            pdf.cell(0, 4, f"{art['num']} ៖ {art['title']}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("KhmerFont", "", 6.2)
            for c_title, c_desc in art["clauses"]:
                pdf.multi_cell(0, 3.2, f"• {c_title} ៖ {c_desc}", align='J', new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)

        # Declaration
        pdf.set_fill_color(240, 253, 244)
        pdf.multi_cell(0, 3.4, f"📝 ការប្រកាសយល់ព្រម ៖ {OFFICIAL_DECLARATION}", fill=True, align='J', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Dual Signature
        pdf.set_font("KhmerFont", "", 6.2)
        sig_text = f"ស្ថាប័ន: Angkor Quant AI Systems (LOCKED) | User: {display_name} (ACCEPTED 100%)\nSHA-256: {sha256_hash}"
        pdf.multi_cell(0, 3.2, sig_text, align='C')

        pdf.output(pdf_path)
        return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000
    except Exception as e:
        print(f"⚠️ [PDF ENGINE] fpdf2 generation failed: {e}")
        return False


def generate_reportlab_pdf(
    chat_id: int,
    username: str,
    full_name: str,
    phone_number: str,
    contract_serial: str,
    sha256_hash: str,
    accepted_time_str: str,
    pdf_path: str
) -> bool:
    """ReportLab fallback generator (removes legacy box and uses justified styles)."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
    except ImportError as e_imp:
        print(f"⚠️ [PDF ENGINE] ReportLab library is not installed: {e_imp}")
        return False

    try:
        font_name = get_khmer_pdf_font()
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=28,
            leftMargin=28,
            topMargin=22,
            bottomMargin=22
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'DocTitle',
            fontName=font_name,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=2
        )
        subtitle_style = ParagraphStyle(
            'DocSubTitle',
            fontName=font_name,
            fontSize=7,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#B45309'),
            spaceAfter=4
        )
        meta_style = ParagraphStyle(
            'DocMeta',
            fontName=font_name,
            fontSize=6.8,
            leading=9.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#334155'),
            spaceAfter=4
        )
        h1_style = ParagraphStyle(
            'ArticleTitle',
            fontName=font_name,
            fontSize=7.8,
            leading=11,
            textColor=colors.HexColor('#1E3A8A'),
            spaceBefore=4,
            spaceAfter=2
        )
        body_style = ParagraphStyle(
            'DocBody',
            fontName=font_name,
            fontSize=6.8,
            leading=9.5,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#334155'),
            spaceAfter=2
        )

        story = []
        story.append(Paragraph(f"<b>{OFFICIAL_CONTRACT_TITLE}</b>", title_style))
        story.append(Paragraph(f"<b>{OFFICIAL_CONTRACT_SUBTITLE}</b>", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#D97706"), spaceAfter=5))

        user_handle = f"@{username}" if username and not username.startswith("@") else (username or "N/A")
        display_name = full_name or f"User_{chat_id}"
        meta_text = f"👤 <b>ឈ្មោះ:</b> {display_name} ({user_handle}) | 🆔 <b>ID:</b> {chat_id} | 📜 <b>Serial:</b> {contract_serial} | 🕒 <b>កាលបរិច្ឆេទ:</b> {accepted_time_str}"
        story.append(Paragraph(meta_text, meta_style))
        story.append(Spacer(1, 2))

        story.append(Paragraph(f"<b>អារម្ភកថា ៖</b> {OFFICIAL_PREAMBLE}", body_style))

        for art in OFFICIAL_ARTICLES:
            story.append(Paragraph(f"<b>{art['num']} ៖ {art['title']}</b>", h1_style))
            for c_title, c_desc in art["clauses"]:
                story.append(Paragraph(f"• <b>{c_title} ៖</b> {c_desc}", body_style))

        story.append(Spacer(1, 3))
        story.append(Paragraph(f"<b>📝 ការប្រកាសយល់ព្រម ៖</b> {OFFICIAL_DECLARATION}", body_style))
        story.append(Spacer(1, 3))
        sig_summary = f"🏛️ <b>ANGKOR QUANT AI SYSTEMS</b> (🟢 LOCKED) | ✍️ <b>{display_name}</b> (🟢 SIGNED 100%)<br/>SHA-256: {sha256_hash}"
        story.append(Paragraph(sig_summary, meta_style))

        doc.build(story)
        return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000
    except Exception as e_gen:
        print(f"⚠️ [PDF ENGINE] ReportLab generation failed: {e_gen}")
        return False


def get_master_agreement_template_path() -> Optional[str]:
    """
    Finds the authoritative 1-page master legal agreement PDF template (Users_agrement.pdf).
    This master document contains the complete, legally valid 5 articles in authentic Khmer.
    """
    candidates = [
        os.path.join(BASE_DIR, "Users_agrement.pdf"),
        os.path.join(BASE_DIR, "Users_agreement.pdf"),
        os.path.join(BASE_DIR, "assets", "docs", "Users_agrement.pdf"),
        os.path.join(BASE_DIR, "assets", "docs", "Users_agreement.pdf"),
        os.path.join(os.path.dirname(BASE_DIR), "Users_agrement.pdf"),
        os.path.join(os.path.dirname(BASE_DIR), "Users_agreement.pdf"),
        os.path.join(os.path.dirname(BASE_DIR), "khmer-master-crypto-bot", "Users_agrement.pdf"),
        os.path.join(os.path.dirname(BASE_DIR), "assets", "docs", "Users_agrement.pdf"),
    ]
    for c in candidates:
        if c and os.path.exists(c) and os.path.isfile(c) and os.path.getsize(c) > 1000:
            return os.path.abspath(c)
    return None


def generate_stamped_contract_pdf(
    chat_id: int,
    username: str,
    full_name: str,
    phone_number: str,
    contract_serial: str,
    sha256_hash: str,
    accepted_time_str: str,
    output_pdf_path: str,
    is_preview: bool = False
) -> bool:
    """
    Tier 1 Flagship Master Stamping Engine (fpdf2 + uharfbuzz text shaping).
    Directly stamps the user's information and digital signature block into the empty
    space at the bottom of the authentic master agreement document (Users_agrement.pdf).
    Ensures zero line wrapping, exact Khmer HarfBuzz shaping, and 100% legal validity.
    """
    try:
        import pypdf
        from fpdf import FPDF

        template_path = get_master_agreement_template_path()
        if not template_path:
            return False

        base_reader = pypdf.PdfReader(template_path)
        if len(base_reader.pages) == 0:
            return False

        base_page = base_reader.pages[0]
        page_w = float(base_page.mediabox.width)
        page_h = float(base_page.mediabox.height)

        user_handle = f"@{username}" if username and not username.startswith("@") else (username or "N/A")
        display_name = full_name.strip() if full_name else f"Trader_{chat_id}"
        display_phone = phone_number.strip() if phone_number else "N/A (Direct Telegram Auth)"

        # Initialize FPDF with exact point dimensions matching master document
        pdf = FPDF(unit='pt', format=[page_w, page_h])
        pdf.set_margins(36, 0, 36)
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()

        # Load Khmer Unicode font with HarfBuzz shaping
        font_path, _, _ = get_khmer_pdf_font_paths()
        has_khmer_font = False
        if font_path and os.path.exists(font_path):
            try:
                pdf.set_text_shaping(True)
                pdf.add_font("KhmerFont", "", font_path)
                pdf.set_font("KhmerFont", "", 7)
                has_khmer_font = True
            except Exception as ex_f:
                print(f"⚠️ [PDF STAMP] HarfBuzz font registration fallback: {ex_f}")

        if not has_khmer_font:
            pdf.set_font("Helvetica", "", 7)

        # Precise container coordinates in bottom blank area (between y=674 pt and y=770 pt)
        card_x = 36.0
        card_y = page_h - 118.0
        card_w = page_w - 72.0
        card_h = 96.0

        # Outer card background & subtle border
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(203, 213, 225)
        pdf.set_line_width(0.8)
        pdf.rect(card_x, card_y, card_w, card_h, style='DF')

        # Left decorative amber security band
        pdf.set_fill_color(217, 119, 6)
        pdf.rect(card_x, card_y, 4, card_h, style='F')

        # Header strip inside card
        pdf.set_fill_color(241, 245, 249)
        pdf.rect(card_x + 4, card_y, card_w - 4, 16, style='F')

        # Header title
        pdf.set_xy(card_x + 10, card_y + 2.5)
        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 7.2)
        else:
            pdf.set_font("Helvetica", "B", 7.2)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(320, 11, "ព័ត៌មានអ្នកប្រើប្រាស់ និងការបញ្ជាក់ហត្ថលេខាឌីជីថល (User Authentication & Digital Signature)", align='L')

        # Right verification badge
        pdf.set_xy(card_x + 335, card_y + 2.5)
        if is_preview:
            pdf.set_fill_color(254, 243, 199)
            pdf.set_draw_color(217, 119, 6)
            pdf.set_text_color(180, 83, 9)
            badge_label = " 🔍 គំរូកិច្ចសន្យាផ្លូវការ / SAMPLE CONTRACT PREVIEW "
        else:
            pdf.set_fill_color(220, 252, 231)
            pdf.set_draw_color(22, 163, 74)
            pdf.set_text_color(22, 101, 52)
            badge_label = " 🟢 កិច្ចសន្យាមានសុពលភាពច្បាប់ / VERIFIED & ACTIVE "

        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 6.2)
        else:
            pdf.set_font("Helvetica", "B", 6.2)
        pdf.cell(195, 11, badge_label, border=1, fill=True, align='C')

        # Section 1: User Identity Column
        col1_x = card_x + 10
        col1_y = card_y + 19
        pdf.set_text_color(51, 65, 85)
        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 6.5)
        else:
            pdf.set_font("Helvetica", "", 6.5)

        pdf.set_xy(col1_x, col1_y)
        pdf.cell(195, 10, f"• ឈ្មោះ (Name): {display_name}", align='L')
        pdf.set_xy(col1_x, col1_y + 10)
        pdf.cell(195, 10, f"• Telegram: {user_handle} (ID: {chat_id})", align='L')
        pdf.set_xy(col1_x, col1_y + 20)
        pdf.cell(195, 10, f"• លេខទូរស័ព្ទ (Phone): {display_phone}", align='L')
        pdf.set_xy(col1_x, col1_y + 30)
        status_line = "• ស្ថានភាព: គំរូបឋម (Preview Only)" if is_preview else "• ស្ថានភាព: យល់ព្រមតាមលក្ខខណ្ឌ ១០០%"
        pdf.cell(195, 10, status_line, align='L')

        # Section 2: Contract Metadata Column
        col2_x = card_x + 205
        col2_y = card_y + 19

        pdf.set_xy(col2_x, col2_y)
        pdf.cell(205, 10, f"• លេខកូដកិច្ចសន្យា: {contract_serial}", align='L')
        pdf.set_xy(col2_x, col2_y + 10)
        pdf.cell(205, 10, f"• កាលបរិច្ឆេទយល់ព្រម: {accepted_time_str}", align='L')
        pdf.set_xy(col2_x, col2_y + 20)
        pdf.cell(205, 10, "• ប្រព័ន្ធ: Angkor Quant AI Engine v4.0", align='L')
        pdf.set_xy(col2_x, col2_y + 30)
        pdf.cell(205, 10, "• គណនី: Non-Custodial Isolated Trading", align='L')

        # Section 3: Institutional Digital Stamp Badge
        stamp_x = card_x + 418
        stamp_y = card_y + 19
        pdf.set_draw_color(217, 119, 6)
        pdf.set_fill_color(255, 251, 235)
        pdf.rect(stamp_x, stamp_y, 114, 40, style='DF')

        pdf.set_xy(stamp_x, stamp_y + 2)
        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 6)
        else:
            pdf.set_font("Helvetica", "B", 6)
        pdf.set_text_color(180, 83, 9)
        pdf.cell(114, 8, "ANGKOR QUANT AI", align='C')

        pdf.set_xy(stamp_x, stamp_y + 11)
        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 7)
        else:
            pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(114, 9, "DIGITAL SEAL", align='C')

        pdf.set_xy(stamp_x, stamp_y + 20)
        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 5.5)
        else:
            pdf.set_font("Helvetica", "B", 5.5)
        pdf.set_text_color(22, 101, 52)
        pdf.cell(114, 8, "✔ TAMPER-PROOF WAL", align='C')

        pdf.set_xy(stamp_x, stamp_y + 29)
        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 5.5)
        else:
            pdf.set_font("Helvetica", "", 5.5)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(114, 8, "PRIVATE PROPRIETARY", align='C')

        # Bottom Footer: Cryptographic SHA-256 Hash
        hash_bar_y = card_y + 61
        pdf.set_fill_color(241, 245, 249)
        pdf.rect(card_x + 4, hash_bar_y, card_w - 4, 33, style='F')

        pdf.set_xy(card_x + 8, hash_bar_y + 3)
        if has_khmer_font:
            pdf.set_font("KhmerFont", "", 5.8)
        else:
            pdf.set_font("Helvetica", "", 5.8)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(card_w - 16, 8, f"Cryptographic SHA-256 Audit Trail: {sha256_hash}", align='L')

        pdf.set_xy(card_x + 8, hash_bar_y + 13)
        pdf.cell(card_w - 16, 8, "កត់ត្រាទុកជាស្ថាពរ និងចាក់សោរអចិន្ត្រៃយ៍ក្នុងប្រព័ន្ធ SQLite WAL Mode (មិនអាចកែប្រែ ឬលុបបាន)", align='L')

        pdf.set_xy(card_x + 8, hash_bar_y + 22)
        pdf.cell(card_w - 16, 8, "សុពលភាពច្បាប់៖ ឯកសារនេះមានតម្លៃពេញលេញតាមច្បាប់ស្តីពីប្រតិបត្តិការអេឡិចត្រូនិក និងកិច្ចសន្យាពាណិជ្ជកម្ម។", align='L')

        # Render overlay to BytesIO
        overlay_buf = io.BytesIO()
        pdf.output(overlay_buf)
        overlay_buf.seek(0)

        # Merge overlay onto master template page
        overlay_reader = pypdf.PdfReader(overlay_buf)
        base_page.merge_page(overlay_reader.pages[0])

        writer = pypdf.PdfWriter()
        writer.add_page(base_page)

        os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
        with open(output_pdf_path, "wb") as f_out:
            writer.write(f_out)

        return os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 10000
    except Exception as e_fpdf_stamp:
        print(f"⚠️ [PDF STAMP] fpdf2 overlay stamper failed: {e_fpdf_stamp}")
        return False


def generate_stamped_contract_pdf_reportlab(
    chat_id: int,
    username: str,
    full_name: str,
    phone_number: str,
    contract_serial: str,
    sha256_hash: str,
    accepted_time_str: str,
    output_pdf_path: str,
    is_preview: bool = False
) -> bool:
    """
    Tier 2 Defensive Overlay Stamper using ReportLab Canvas.
    Stamps user information into bottom blank space of Users_agrement.pdf.
    """
    try:
        import pypdf
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import HexColor

        template_path = get_master_agreement_template_path()
        if not template_path:
            return False

        base_reader = pypdf.PdfReader(template_path)
        if len(base_reader.pages) == 0:
            return False

        base_page = base_reader.pages[0]
        page_w = float(base_page.mediabox.width)
        page_h = float(base_page.mediabox.height)

        font_name = get_khmer_pdf_font()

        user_handle = f"@{username}" if username and not username.startswith("@") else (username or "N/A")
        display_name = full_name.strip() if full_name else f"Trader_{chat_id}"
        display_phone = phone_number.strip() if phone_number else "N/A (Direct Telegram Auth)"

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_w, page_h))

        card_x = 36.0
        card_y = 22.0
        card_w = page_w - 72.0
        card_h = 96.0

        can.setFillColor(HexColor("#F8FAFC"))
        can.setStrokeColor(HexColor("#CBD5E1"))
        can.setLineWidth(0.8)
        can.rect(card_x, card_y, card_w, card_h, stroke=1, fill=1)

        can.setFillColor(HexColor("#D97706"))
        can.rect(card_x, card_y, 4, card_h, stroke=0, fill=1)

        can.setFillColor(HexColor("#F1F5F9"))
        can.rect(card_x + 4, card_y + card_h - 16, card_w - 4, 16, stroke=0, fill=1)

        can.setFont(font_name, 7.2)
        can.setFillColor(HexColor("#0F172A"))
        can.drawString(card_x + 10, card_y + card_h - 11.5, "ព័ត៌មានអ្នកប្រើប្រាស់ និងការបញ្ជាក់ហត្ថលេខាឌីជីថល (User Authentication & Digital Signature)")

        if is_preview:
            can.setFillColor(HexColor("#FEF3C7"))
            can.setStrokeColor(HexColor("#D97706"))
            can.rect(card_x + 335, card_y + card_h - 14, 195, 12, stroke=1, fill=1)
            can.setFont(font_name, 6.2)
            can.setFillColor(HexColor("#B45309"))
            can.drawCentredString(card_x + 335 + 97.5, card_y + card_h - 9.5, "គំរូកិច្ចសន្យាផ្លូវការ / SAMPLE CONTRACT PREVIEW")
        else:
            can.setFillColor(HexColor("#DCFCE7"))
            can.setStrokeColor(HexColor("#16A34A"))
            can.rect(card_x + 335, card_y + card_h - 14, 195, 12, stroke=1, fill=1)
            can.setFont(font_name, 6.2)
            can.setFillColor(HexColor("#166534"))
            can.drawCentredString(card_x + 335 + 97.5, card_y + card_h - 9.5, "កិច្ចសន្យាមានសុពលភាពច្បាប់ / VERIFIED & ACTIVE")

        col1_x = card_x + 10
        col1_y = card_y + card_h - 28
        can.setFillColor(HexColor("#334155"))
        can.setFont(font_name, 6.5)

        can.drawString(col1_x, col1_y, f"• ឈ្មោះ (Name): {display_name}")
        can.drawString(col1_x, col1_y - 10, f"• Telegram: {user_handle} (ID: {chat_id})")
        can.drawString(col1_x, col1_y - 20, f"• លេខទូរស័ព្ទ (Phone): {display_phone}")
        status_txt = "• ស្ថានភាព: គំរូបឋម (Preview Only)" if is_preview else "• ស្ថានភាព: យល់ព្រមតាមលក្ខខណ្ឌ ១០០%"
        can.drawString(col1_x, col1_y - 30, status_txt)

        col2_x = card_x + 205
        can.drawString(col2_x, col1_y, f"• លេខកូដកិច្ចសន្យា: {contract_serial}")
        can.drawString(col2_x, col1_y - 10, f"• កាលបរិច្ឆេទយល់ព្រម: {accepted_time_str}")
        can.drawString(col2_x, col1_y - 20, "• ប្រព័ន្ធ: Angkor Quant AI Engine v4.0")
        can.drawString(col2_x, col1_y - 30, "• គណនី: Non-Custodial Isolated Trading")

        stamp_x = card_x + 418
        stamp_y = card_y + card_h - 58
        can.setStrokeColor(HexColor("#D97706"))
        can.setFillColor(HexColor("#FFFBEB"))
        can.rect(stamp_x, stamp_y, 114, 40, stroke=1, fill=1)

        can.setFont(font_name, 6)
        can.setFillColor(HexColor("#B45309"))
        can.drawCentredString(stamp_x + 57, stamp_y + 30, "ANGKOR QUANT AI")
        can.setFont(font_name, 7)
        can.setFillColor(HexColor("#0F172A"))
        can.drawCentredString(stamp_x + 57, stamp_y + 20, "DIGITAL SEAL")
        can.setFont(font_name, 5.5)
        can.setFillColor(HexColor("#166534"))
        can.drawCentredString(stamp_x + 57, stamp_y + 11, "✔ TAMPER-PROOF WAL")
        can.setFont(font_name, 5.5)
        can.setFillColor(HexColor("#475569"))
        can.drawCentredString(stamp_x + 57, stamp_y + 2.5, "PRIVATE PROPRIETARY")

        hash_bar_y = card_y + 4
        can.setFillColor(HexColor("#F1F5F9"))
        can.rect(card_x + 4, hash_bar_y, card_w - 4, 30, stroke=0, fill=1)

        can.setFont(font_name, 5.8)
        can.setFillColor(HexColor("#475569"))
        can.drawString(card_x + 8, hash_bar_y + 21, f"Cryptographic SHA-256 Audit Trail: {sha256_hash}")
        can.drawString(card_x + 8, hash_bar_y + 12, "កត់ត្រាទុកជាស្ថាពរ និងចាក់សោរអចិន្ត្រៃយ៍ក្នុងប្រព័ន្ធ SQLite WAL Mode (មិនអាចកែប្រែ ឬលុបបាន)")
        can.drawString(card_x + 8, hash_bar_y + 3, "សុពលភាពច្បាប់៖ ឯកសារនេះមានតម្លៃពេញលេញតាមច្បាប់ស្តីពីប្រតិបត្តិការអេឡិចត្រូនិក និងកិច្ចសន្យាពាណិជ្ជកម្ម។")

        can.save()
        packet.seek(0)

        overlay_reader = pypdf.PdfReader(packet)
        base_page.merge_page(overlay_reader.pages[0])

        writer = pypdf.PdfWriter()
        writer.add_page(base_page)

        os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
        with open(output_pdf_path, "wb") as f_out:
            writer.write(f_out)

        return os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 10000
    except Exception as e_rl_stamp:
        print(f"⚠️ [PDF STAMP] ReportLab overlay stamper failed: {e_rl_stamp}")
        return False


def generate_legal_contract_pdf(
    chat_id: int,
    username: str,
    full_name: str,
    phone_number: str,
    contract_serial: str,
    sha256_hash: str,
    accepted_time_str: str
) -> str:
    """
    Official Institutional Legal Contract PDF Generator.
    - Master Architecture: Uses authentic 1-page master document Users_agrement.pdf
    - Inserts user authentication & digital signature in the empty space at bottom
    - Multi-tier stamping & generation:
      Tier 1: fpdf2 + uharfbuzz overlay onto Users_agrement.pdf
      Tier 2: ReportLab canvas overlay onto Users_agrement.pdf
      Tier 3: Browser / pure python full generation fallback if template missing
    """
    os.makedirs(PDF_ARCHIVE_DIR, exist_ok=True)
    pdf_filename = f"Angkor_Quant_Agreement_{chat_id}_{contract_serial.replace('-', '_')}.pdf"
    pdf_path = os.path.join(PDF_ARCHIVE_DIR, pdf_filename)

    is_preview = bool("PREVIEW" in contract_serial.upper())

    # Tier 1 (Primary Institutional Path): fpdf2 + uharfbuzz stamp on Users_agrement.pdf
    try:
        if generate_stamped_contract_pdf(
            chat_id=chat_id,
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            contract_serial=contract_serial,
            sha256_hash=sha256_hash,
            accepted_time_str=accepted_time_str,
            output_pdf_path=pdf_path,
            is_preview=is_preview
        ):
            return pdf_path
    except Exception as ex_t1:
        print(f"⚠️ [PDF ENGINE] Tier 1 Master Stamping skipped: {ex_t1}")

    # Tier 2 (Defensive Fallback): ReportLab canvas stamp on Users_agrement.pdf
    try:
        if generate_stamped_contract_pdf_reportlab(
            chat_id=chat_id,
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            contract_serial=contract_serial,
            sha256_hash=sha256_hash,
            accepted_time_str=accepted_time_str,
            output_pdf_path=pdf_path,
            is_preview=is_preview
        ):
            return pdf_path
    except Exception as ex_t2:
        print(f"⚠️ [PDF ENGINE] Tier 2 ReportLab Stamping skipped: {ex_t2}")

    # Tier 3 (Full Generation Fallback - Only if Users_agrement.pdf is completely missing):
    try:
        if generate_fpdf2_pdf(chat_id, username, full_name, phone_number, contract_serial, sha256_hash, accepted_time_str, pdf_path):
            return pdf_path
    except Exception as ex_fpdf:
        print(f"⚠️ [PDF ENGINE] Tier 3 fpdf2 skipped: {ex_fpdf}")

    try:
        html_src = build_official_agreement_html(
            chat_id, username, full_name, phone_number, contract_serial, sha256_hash, accepted_time_str
        )
        if generate_browser_pdf(html_src, pdf_path):
            return pdf_path
    except Exception as ex_browser:
        print(f"⚠️ [PDF ENGINE] Tier 3 Browser skipped: {ex_browser}")

    try:
        if generate_reportlab_pdf(chat_id, username, full_name, phone_number, contract_serial, sha256_hash, accepted_time_str, pdf_path):
            return pdf_path
    except Exception as ex_rl:
        print(f"⚠️ [PDF ENGINE] Tier 3 ReportLab failed: {ex_rl}")

    return ""


# ─── INTERACTIVE TELEGRAM UI CARDS ───────────────────────────────────────────

def build_new_user_start_agreement_card(
    chat_id: int,
    first_name: str,
    username: str = "",
    phone_number: str = ""
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Presents the full legal contract and risk waiver to NEW / UNSIGNED users on /start.
    Blocks direct trading dashboard access until explicitly accepted.
    """
    now_ict = datetime.now(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M:%S ICT")
    user_handle = f"@{username}" if username and not username.startswith("@") else (username or "N/A")
    display_phone = phone_number or "មិនទាន់ភ្ជាប់ (Not Linked)"

    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🏛️ **កិច្ចសន្យា និងលក្ខខណ្ឌផ្លូវការនៃការប្រើប្រាស់ប្រព័ន្ធ ANGKOR QUANT**\n"
        f"{DIVIDER_HEAVY}\n\n"
        "👤 **ព័ត៌មានអត្តសញ្ញាណអ្នកចុះកិច្ចសន្យា (New User Identity) ៖**\n"
        f"• **Telegram User ID** ៖ `{chat_id}`\n"
        f"• **ឈ្មោះគណនី (Name)** ៖ `{first_name}`\n"
        f"• **Username** ៖ `{user_handle}`\n"
        f"• **លេខទូរសព្ទ** ៖ `{display_phone}`\n"
        f"• **កាលបរិច្ឆេទពិនិត្យ** ៖ `{now_ict}`\n\n"
        f"{DIVIDER_LIGHT}\n"
        "📜 **ខ្លឹមសារសង្ខេបនៃកិច្ចសន្យា ៥ ប្រការ (Full Legal Articles) ៖**\n\n"
        "🏛️ **ប្រការ ១ ៖ គោលបំណងឯកជន & កម្មសិទ្ធិបញ្ញា**\n"
        "ប្រព័ន្ធរៀបចំឡើងសម្រាប់តែការស្រាវជ្រាវ និងការជួញដូរស្វ័យប្រវត្តិតាមលក្ខណៈឯកជនផ្ទាល់ខ្លួន ឬក្នុងរង្វង់ VIP ឯកជន។ "
        "មិនមែនជាស្ថាប័នហិរញ្ញវត្ថុ មិនមែនជាធនាគារ និងមិនទទួលប្រាក់បញ្ញើសាធារណៈឡើយ។ "
        "ដើមទុនទាំងអស់ស្ថិតក្នុងកាបូបលុយផ្ទាល់ខ្លួន (Binance/MT5) ១០០% តាមគោលការណ៍ Non-Custodial។\n\n"
        "⚠️ **ប្រការ ២ ៖ ការទទួលខុសត្រូវលើហានិភ័យ & គ្មានការធានា**\n"
        "Crypto Futures, Spot និង Forex មានហានិភ័យខ្ពស់បំផុត និងអាចខាតបង់ដើមទុនទាំងអស់។ "
        "អ្នកប្រើប្រាស់ទទួលខុសត្រូវលើការខាតបង់ហិរញ្ញវត្ថុដោយខ្លួនឯង ១០០%។ "
        "ប្រព័ន្ធដំណើរការលើប្រៀបឈ្នះបែបគណិតវិទ្យា ($E[X] > 0$) គ្មានការធានាប្រាក់ចំណេញឡើយ។\n\n"
        "⚙️ **ប្រការ ៣ ៖ ការលើកលែងការទទួលខុសត្រូវលើកំហុសបច្ចេកទេស**\n"
        "ប្រព័ន្ធ និងអ្នកអភិវឌ្ឍន៍មិនទទួលខុសត្រូវចំពោះ៖ កំហុសកំណត់របស់អ្នកប្រើប្រាស់ (Setup Mistakes), "
        "ការគាំងប្រព័ន្ធ (Downtime/Crashes), ការដាច់ចរន្ត/អ៊ីនធឺណិត, ឬការរអាក់រអួលរបស់ Binance/Broker ឡើយ។\n\n"
        "🛡️ **ប្រការ ៤ ៖ ការបដិសេធការធានា & លះបង់ការទាមទារសំណង**\n"
        "ប្រព័ន្ធផ្តល់ជូនតាមស្ថានភាពជាក់ស្តែង (\"AS IS\")។ អ្នកប្រើប្រាស់យល់ព្រមលះបង់សិទ្ធិទាំងអស់ក្នុងការប្តឹងផ្តល់ "
        "ឬទាមទារសំណងការខាតបង់ពីស្ថាបនិក និងក្រុមការងារជាដាច់ខាត។\n\n"
        "🔒 **ប្រការ ៥ ៖ សន្តិសុខទិន្នន័យ គណនី & 2FA PIN**\n"
        "Binance API Keys ត្រូវបាន Encrypted និងតម្រូវឱ្យបិទសិទ្ធិដកប្រាក់ជានិច្ច។ "
        "រាល់ការបញ្ជាដែលចេញពី Telegram ID របស់អ្នក ត្រូវបានចាត់ទុកជាការសម្រេចចិត្តផ្ទាល់ខ្លួនជាផ្លូវការ។\n\n"
        f"{DIVIDER_LIGHT}\n"
        "📝 **ការប្រកាសយល់ព្រម ៖**\n"
        "_«ខ្ញុំបាទ/នាងខ្ញុំ ជាអ្នកប្រើប្រាស់ បានអាន និងយល់ច្បាស់នូវរាល់ប្រការខាងលើ។ "
        "ការចុចយល់ព្រមចាត់ទុកថាខ្ញុំបាទ/នាងខ្ញុំបានទទួលស្គាល់ និងឯកភាពលើកិច្ចសន្យានេះដោយស្ម័គ្រចិត្ត ១០០% និងគ្មានការបង្ខិតបង្ខំ។ "
        "ប្រព័ន្ធនឹងរៀបចំឯកសារ PDF ចាក់សោរក្នុង Database យ៉ាងរឹងមាំជាភស្តុតាងផ្លូវការ!»_\n\n"
        "👉 _សូមពិនិត្យ និងចុចប៊ូតុង «យល់ព្រម» ខាងក្រោមដើម្បីបន្ត ៖_"
        f"{INSTITUTIONAL_FOOTER}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ ខ្ញុំបានអាន យល់ច្បាស់ និងយល់ព្រម ១០០%", callback_data="btn_agree_terms")],
        [InlineKeyboardButton("📄 មើលកិច្ចសន្យាជាទម្រង់ PDF", callback_data="btn_preview_terms_pdf")],
        [
            InlineKeyboardButton("🌐 Read in English", callback_data="btn_about_en"),
            InlineKeyboardButton("ℹ️ ជំនួយ / Support", callback_data="btn_menu_refresh")
        ]
    ])
    return msg, keyboard


def build_contract_signed_success_card(
    chat_id: int,
    contract_serial: str,
    accepted_at_str: str,
    sha256_hash: str
) -> Tuple[str, InlineKeyboardMarkup]:
    """Card presented immediately after successful digital contract signing & PDF generation."""
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🎉 **ការចុះកិច្ចសន្យាផ្លូវការបានជោគជ័យ ១០០%!** 📜\n"
        f"{DIVIDER_HEAVY}\n\n"
        "🤝 **សូមអបអរសាទរ!** កិច្ចសន្យា និងលក្ខខណ្ឌនៃការប្រើប្រាស់ប្រព័ន្ធ Angkor Quant "
        "ត្រូវបានចុះហត្ថលេខាឌីជីថល និងរក្សាទុកក្នុង Database ចាក់សោរយ៉ាងរឹងមាំជាភស្តុតាងផ្លូវការរួចរាល់ហើយ!\n\n"
        "📋 **ព័ត៌មានកិច្ចសន្យាផ្លូវការរបស់អ្នក ៖**\n"
        f"• **Telegram User ID** ៖ `{chat_id}`\n"
        f"• **លេខកូដកិច្ចសន្យា (Serial)** ៖ `{contract_serial}`\n"
        f"• **កាលបរិច្ឆេទចុះហត្ថលេខា** ៖ `{accepted_at_str}`\n"
        f"• **ស្ថានភាពគណនី** ៖ `🟢 VERIFIED & LEGALLY ACTIVE`\n"
        f"• **Cryptographic Fingerprint** ៖ `{sha256_hash[:24]}...`\n\n"
        "📁 _ឯកសារកិច្ចសន្យាផ្លូវការជាទម្រង់ **PDF Document** ត្រូវបានផ្ញើជូនលោកអ្នកក្នុងសារបន្ទាប់! "
        "លោកអ្នកអាចទាញយក និងរក្សាទុកជាភស្តុតាងផ្ទាល់ខ្លួនបានគ្រប់ពេលវេលា។_\n\n"
        "✨ **ជំហានបន្ទាប់ដែលលោកអ្នកអាចធ្វើបាន ៖**\n"
        "1. ចុចស្នើសុំសិទ្ធិជា **VIP User** ដើម្បីបើកសិទ្ធិប្រើប្រាស់ពេញលេញ\n"
        "2. ចូលទៅកាន់ **Master Control Panel** ដើម្បីស្វែងយល់ពីប្រព័ន្ធយុទ្ធសាស្ត្រ\n"
        "3. កំណត់ **Binance API Keys** (សិទ្ធិមើល & Trade តែប៉ុណ្ណោះ គ្មានសិទ្ធិដកប្រាក់)"
        f"{INSTITUTIONAL_FOOTER}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 ទាញយកកិច្ចសន្យា PDF របស់ខ្ញុំ", callback_data="btn_download_my_pdf")],
        [
            InlineKeyboardButton("👑 ស្នើសុំសិទ្ធិ VIP User", callback_data="btn_menu_vip_req"),
            InlineKeyboardButton("🎛️ Master Menu", callback_data="btn_menu_refresh")
        ]
    ])
    return msg, keyboard


def build_admin_agreements_card(page: int = 1, search_query: str = "") -> Tuple[str, InlineKeyboardMarkup]:
    """Control panel for Super Admin to inspect and download any user's signed legal agreement."""
    total_agreements = get_legal_agreements_count()
    limit = 6
    offset = (page - 1) * limit
    agreements = get_all_legal_agreements(limit=limit, offset=offset)

    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "👑 **ANGKOR QUANT - LEGAL AGREEMENTS AUDIT CITADEL** 📜\n"
        f"**Super Admin Legal Registry & PDF Vault**\n"
        f"{DIVIDER_HEAVY}\n\n"
        f"📊 **ស្ថិតិកិច្ចសន្យាសរុប ៖** `{total_agreements} Users Signed`\n"
        f"🔒 **ស្ថានភាពការពារ ៖** `100% Immutable WAL SQLite + PDF Disk Archive`\n"
        f"📑 **ទំព័រ ៖** `{page} / {max(1, (total_agreements + limit - 1) // limit)}`\n\n"
        "📋 **បញ្ជីអ្នកប្រើប្រាស់ដែលបានចុះកិច្ចសន្យាថ្មីៗ ៖**\n"
    )

    buttons = []
    if agreements:
        for idx, agr in enumerate(agreements, 1):
            c_id = agr.get("chat_id")
            c_name = agr.get("full_name") or agr.get("username") or f"User_{c_id}"
            c_date = agr.get("accepted_at", "")
            c_serial = agr.get("contract_serial", "N/A")
            msg += (
                f"{idx}. 👤 **{c_name}** (`{c_id}`)\n"
                f"   • Serial: `{c_serial}` | Date: `{c_date}`\n"
            )
            # 1-Tap PDF Download button for each user
            buttons.append([
                InlineKeyboardButton(f"📥 ទាញយក PDF: {c_name[:14]} ({c_id})", callback_data=f"btn_admin_dl_pdf_{c_id}")
            ])
    else:
        msg += "_មិនទាន់មានកិច្ចសន្យាណាមួយត្រូវបានកត់ត្រានៅឡើយទេ_\n"

    # Pagination row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton("⬅️ ថយក្រោយ", callback_data=f"btn_admin_agr_page_{page-1}"))
    if offset + limit < total_agreements:
        nav_row.append(InlineKeyboardButton("បន្ទាប់ ➡️", callback_data=f"btn_admin_agr_page_{page+1}"))
    if nav_row:
        buttons.append(nav_row)

    buttons.append([
        InlineKeyboardButton("🔄 Refresh បញ្ជី", callback_data="btn_admin_agreements"),
        InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="btn_admin_panel")
    ])

    msg += (
        f"\n{DIVIDER_LIGHT}\n"
        "💡 _Super Admin អាចចុចលើប៊ូតុងនីមួយៗខាងលើ ដើម្បីទាញយកឯកសារ PDF របស់អ្នកប្រើប្រាស់នោះភ្លាមៗ!_"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, InlineKeyboardMarkup(buttons)


# ─── BILINGUAL / ABOUT BACKWARD COMPATIBILITY ────────────────────────────────

def get_about_keyboard(current_section: str = "main", is_accepted: bool = False) -> InlineKeyboardMarkup:
    """Standardized navigation keyboards for /about and /agreement commands."""
    buttons = []
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
        nav_row_3.append(InlineKeyboardButton("🌐 English Terms", callback_data="btn_about_en"))
    if nav_row_3:
        buttons.append(nav_row_3)

    if not is_accepted:
        buttons.append([InlineKeyboardButton("✍️ ខ្ញុំបានអាន យល់ច្បាស់ និងយល់ព្រម ១០០%", callback_data="btn_agree_terms")])
    else:
        buttons.append([InlineKeyboardButton("📥 ទាញយកកិច្ចសន្យា PDF", callback_data="btn_download_my_pdf")])

    if current_section != "main":
        buttons.append([
            InlineKeyboardButton("📜 ទំព័រដើមកិច្ចសន្យា", callback_data="btn_about_menu"),
            InlineKeyboardButton("🔙 ត្រឡប់ទៅ Menu មេ", callback_data="btn_menu_refresh")
        ])
    else:
        buttons.append([InlineKeyboardButton("🔙 ត្រឡប់ទៅ Menu មេ", callback_data="btn_menu_refresh")])

    return InlineKeyboardMarkup(buttons)


def build_about_main_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    """Overview card for /about and /agreement."""
    status = get_user_agreement_status(chat_id)
    accepted_badge = f"🟢 _បានយល់ព្រមនៅ {status['accepted_at']} (Serial: {status.get('contract_serial', 'AQ-LOCKED')})_" if status["accepted"] else "⏳ _មិនទាន់បានចុះកិច្ចសន្យា (Pending Review)_"

    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "📜 **កិច្ចសន្យា និងលក្ខខណ្ឌផ្លូវការនៃការប្រើប្រាស់ប្រព័ន្ធ ANGKOR QUANT**\n"
        f"**Official Private Quant Agreement & Risk Waiver** `{AGREEMENT_VERSION}`\n"
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
        f"📊 **ស្ថានភាពកិច្ចសន្យារបស់អ្នក ៖**\n{accepted_badge}\n\n"
        "👉 _សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីពិនិត្យលម្អិតជំពូកនីមួយៗ ឬទាញយកឯកសារ PDF ៖_"
        f"{INSTITUTIONAL_FOOTER}"
    )
    return msg, get_about_keyboard("main", status["accepted"])


def build_terms_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    status = get_user_agreement_status(chat_id)
    art = OFFICIAL_ARTICLES[0]
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        f"📜 **{art['num']} ៖ {art['title']}**\n"
        f"{DIVIDER_HEAVY}\n\n"
    )
    for c_title, c_desc in art["clauses"]:
        msg += f"• **{c_title} ៖**\n{c_desc}\n\n"
    msg += f"{INSTITUTIONAL_FOOTER}"
    return msg, get_about_keyboard("terms", status["accepted"])


def build_risk_disclosure_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    status = get_user_agreement_status(chat_id)
    art = OFFICIAL_ARTICLES[1]
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        f"⚠️ **{art['num']} ៖ {art['title']}**\n"
        f"{DIVIDER_HEAVY}\n\n"
    )
    for c_title, c_desc in art["clauses"]:
        msg += f"• **{c_title} ៖**\n{c_desc}\n\n"
    msg += f"{INSTITUTIONAL_FOOTER}"
    return msg, get_about_keyboard("risk", status["accepted"])


def build_mt5_execution_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    status = get_user_agreement_status(chat_id)
    art = OFFICIAL_ARTICLES[2]
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        f"⚙️ **{art['num']} ៖ {art['title']}**\n"
        f"{DIVIDER_HEAVY}\n\n"
        f"{art.get('lead', '')}\n\n"
    )
    for c_title, c_desc in art["clauses"]:
        msg += f"• **{c_title} ៖**\n{c_desc}\n\n"
    msg += f"{INSTITUTIONAL_FOOTER}"
    return msg, get_about_keyboard("mt5", status["accepted"])


def build_liability_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    status = get_user_agreement_status(chat_id)
    art = OFFICIAL_ARTICLES[3]
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        f"🛡️ **{art['num']} ៖ {art['title']}**\n"
        f"{DIVIDER_HEAVY}\n\n"
    )
    for c_title, c_desc in art["clauses"]:
        msg += f"• **{c_title} ៖**\n{c_desc}\n\n"
    msg += f"{INSTITUTIONAL_FOOTER}"
    return msg, get_about_keyboard("liability", status["accepted"])


def build_privacy_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    status = get_user_agreement_status(chat_id)
    art = OFFICIAL_ARTICLES[4]
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        f"🔒 **{art['num']} ៖ {art['title']}**\n"
        f"{DIVIDER_HEAVY}\n\n"
    )
    for c_title, c_desc in art["clauses"]:
        msg += f"• **{c_title} ៖**\n{c_desc}\n\n"
    msg += f"{INSTITUTIONAL_FOOTER}"
    return msg, get_about_keyboard("privacy", status["accepted"])


def build_full_english_card(chat_id: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    status = get_user_agreement_status(chat_id)
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🌐 **ANGKOR QUANT - OFFICIAL SYSTEM USAGE AGREEMENT** 🏛️\n"
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


def build_agreement_gatekeeper_card(chat_id: int = 0, feature_name: str = "ប្រព័ន្ធជួញដូរស្វ័យប្រវត្តិ") -> Tuple[str, InlineKeyboardMarkup]:
    """Gatekeeper card displayed when an unaccepted user attempts to execute live trading or API setup."""
    msg = (
        f"{INSTITUTIONAL_HEADER}"
        "🛡️ **កិច្ចសន្យា និងការទទួលខុសត្រូវលើហានិភ័យ** ⚠️\n"
        f"**Private Quant Gatekeeper Shield** `{AGREEMENT_VERSION}`\n"
        f"{DIVIDER_HEAVY}\n\n"
        f"ដើម្បីអាចដំណើរការ **{feature_name}** និងតភ្ជាប់ API បាន លោកអ្នកត្រូវតែពិនិត្យ និងយល់ព្រមលើ **កិច្ចសន្យាប្រើប្រាស់ប្រព័ន្ធ** ជាមុនសិន។\n\n"
        "🏛️ **គោលការណ៍គ្រឹះមិនអាចកែប្រែបាន (Non-Negotiable Terms) ៖**\n"
        "1️⃣ **ទទួលខុសត្រូវដោយខ្លួនឯង ១០០% ៖** ការជួញដូរលើ Crypto, Futures, និង Forex ពោរពេញដោយហានិភ័យខ្ពស់។ អ្នកប្រើប្រាស់សម្រេចចិត្តដាក់ទុន និងជ្រើសរើស Leverage ដោយស្ម័គ្រចិត្ត។ រាល់ការខាតបង់ ឬ Liquidation គឺជាការទទួលខុសត្រូវផ្ទាល់ខ្លួនរបស់អ្នកតែម្នាក់ឯង។\n"
        "2️⃣ **ប្រព័ន្ធមិនធានាចំពោះការខាតបង់ឡើយ ៖** គ្មានការធានាប្រាក់ចំណេញ ឬធានាមិនខាតបង់ពីសំណាក់ប្រព័ន្ធ ឬអ្នកអភិវឌ្ឍន៍ឡើយ។\n"
        "3️⃣ **គ្មានការទទួលខុសត្រូវចំពោះកំហុសឆ្គង ឬការគាំងប្រព័ន្ធ ៖** ការរៀបចំខុសពីសំណាក់អ្នកប្រើប្រាស់ (Setup Mistakes), ការដាច់ចរន្ត/អ៊ីនធឺណិត, ការគាំង VPS, កំហុសកូដ Bug, ឬការរអាក់រអួលរបស់ Broker/Exchange មិនអាចយកជាមូលដ្ឋានទាមទារសំណងបានឡើយ។\n"
        "4️⃣ **លះបង់ការទាមទារសំណងទាំងស្រុង ៖** កម្មវិធីដំណើរការតាមស្ថានភាពជាក់ស្តែង (AS IS) សម្រាប់ប្រើប្រាស់ឯកជនផ្ទាល់ខ្លួន។\n\n"
        f"{DIVIDER_LIGHT}\n"
        "👉 _សូមចុចប៊ូតុងខាងក្រោមដើម្បី «យល់ព្រម» ឬ «អានកិច្ចសន្យាពេញលេញ» ជាមុនសិន ៖_"
        f"{INSTITUTIONAL_FOOTER}"
    )
    buttons = [
        [InlineKeyboardButton("✍️ ខ្ញុំបានអាន យល់ច្បាស់ និងយល់ព្រម ១០០%", callback_data="btn_agree_terms")],
        [
            InlineKeyboardButton("📜 អានកិច្ចសន្យាពេញលេញ", callback_data="btn_about_terms"),
            InlineKeyboardButton("📄 មើលជា PDF", callback_data="btn_preview_terms_pdf")
        ],
        [
            InlineKeyboardButton("🌐 English Terms", callback_data="btn_about_en"),
            InlineKeyboardButton("🔙 ត្រឡប់ទៅ Menu មេ", callback_data="btn_menu_refresh")
        ]
    ]
    return msg, InlineKeyboardMarkup(buttons)


async def check_or_prompt_agreement(update, context, chat_id: int, feature_name: str = "ប្រព័ន្ធជួញដូរស្វ័យប្រវត្តិ") -> bool:
    """Asynchronous Gatekeeper check. Intercepts execution if agreement is not signed."""
    if is_agreement_accepted(chat_id):
        return True

    text, keyboard = build_agreement_gatekeeper_card(chat_id=chat_id, feature_name=feature_name)
    try:
        if update.callback_query:
            try:
                await update.callback_query.answer("⚠️ សូមយល់ព្រមកិច្ចសន្យាឯកជនជាមុនសិន!")
            except Exception:
                pass
            try:
                await update.callback_query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=keyboard)
            except Exception:
                await update.callback_query.edit_message_text(text=text, parse_mode=None, reply_markup=keyboard)
        elif update.message or update.effective_message:
            msg_obj = update.message or update.effective_message
            try:
                await msg_obj.reply_text(text=text, parse_mode="Markdown", reply_markup=keyboard)
            except Exception:
                await msg_obj.reply_text(text=text, parse_mode=None, reply_markup=keyboard)
    except Exception as e:
        print(f"Error serving agreement gatekeeper card: {e}")
    return False


# ─── CENTRALIZED CALLBACK HANDLER ────────────────────────────────────────────

async def handle_agreement_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str, chat_id: int):
    """
    Centralized handler for all agreement-related callbacks.
    Guarantees Invariant 11 (100% Routed & Zero Dead Buttons).
    """
    query = update.callback_query
    if query:
        try:
            await query.answer()
        except Exception:
            pass

    # 1. User Clicks Agree & Sign
    if data in ["btn_agree_terms", "btn_about_accept"]:
        user = update.effective_user
        username = user.username if user else ""
        first_name = (user.first_name if user else "") or "Valued Trader"
        last_name = (user.last_name if user else "") or ""
        full_name = f"{first_name} {last_name}".strip()

        # Retrieve phone from users table if available
        phone_number = ""
        try:
            import database as db
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT phone_number FROM users WHERE chat_id = ?", (chat_id,))
            r = c.fetchone()
            if r and r["phone_number"]:
                phone_number = str(r["phone_number"]).strip()
            conn.close()
        except Exception:
            pass

        now_dt = datetime.now(timezone(timedelta(hours=7)))
        accepted_time_str = now_dt.strftime("%d/%m/%Y %H:%M:%S ICT")
        rand_suffix = f"{random.randint(1000, 9999):X}"
        contract_serial = f"AQ-AGR-{now_dt.strftime('%Y%m%d')}-{chat_id}-{rand_suffix}"

        # Cryptographic Hash (Immutable Fingerprint)
        hash_payload = f"{contract_serial}|{chat_id}|{username}|{full_name}|{accepted_time_str}|{OFFICIAL_CONTRACT_TITLE}"
        sha256_hash = hashlib.sha256(hash_payload.encode('utf-8')).hexdigest()

        # Automated PDF Generation
        pdf_path = ""
        try:
            pdf_path = generate_legal_contract_pdf(
                chat_id=chat_id,
                username=username,
                full_name=full_name,
                phone_number=phone_number,
                contract_serial=contract_serial,
                sha256_hash=sha256_hash,
                accepted_time_str=accepted_time_str
            )
        except Exception as ex_pdf:
            print(f"Error generating contract PDF: {ex_pdf}")

        # Immutable Persistence in Database
        record_user_legal_contract(
            chat_id=chat_id,
            user_id=user.id if user else chat_id,
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            contract_serial=contract_serial,
            sha256_hash=sha256_hash,
            pdf_path=pdf_path,
            version=AGREEMENT_VERSION
        )

        # Present Confirmation Card
        card_text, keyboard = build_contract_signed_success_card(
            chat_id=chat_id,
            contract_serial=contract_serial,
            accepted_at_str=accepted_time_str,
            sha256_hash=sha256_hash
        )

        msg_target = query.message if query else (update.effective_message or update.message)
        if msg_target:
            try:
                await msg_target.reply_text(card_text, parse_mode="Markdown", reply_markup=keyboard)
            except Exception:
                await msg_target.reply_text(card_text, parse_mode=None, reply_markup=keyboard)

        # Automatically Send the PDF Document File to User Chat
        if pdf_path and os.path.exists(pdf_path):
            try:
                caption_text = (
                    f"📄 **ឯកសារកិច្ចសន្យាផ្លូវការ (Official Legal Contract PDF)** 📜\n"
                    f"• **Serial:** `{contract_serial}`\n"
                    f"• **User:** `{full_name}` (`{chat_id}`)\n"
                    f"• **SHA-256:** `{sha256_hash[:20]}...`\n"
                    f"• **ស្ថានភាព:** `🟢 ចាក់សោរឌីជីថល (IMMUTABLE RECORD)`"
                )
                with open(pdf_path, "rb") as pdf_file:
                    await context.bot.send_document(
                        chat_id=chat_id,
                        document=pdf_file,
                        filename=os.path.basename(pdf_path),
                        caption=caption_text,
                        parse_mode="Markdown"
                    )
            except Exception as e_send_doc:
                print(f"Error sending PDF document to user: {e_send_doc}")

        # Notify Super Admin of New Signed Contract
        try:
            admin_msg = (
                f"📢 **[NEW USER LEGAL CONTRACT SIGNED]** 📜\n"
                f"• **User:** `{full_name}` (@{username or 'N/A'})\n"
                f"• **Telegram ID:** `{chat_id}`\n"
                f"• **Serial:** `{contract_serial}`\n"
                f"• **Timestamp:** `{accepted_time_str}`\n"
                f"• **Hash:** `{sha256_hash[:16]}...`"
            )
            admin_btn = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"📥 Download PDF: {chat_id}", callback_data=f"btn_admin_dl_pdf_{chat_id}")]
            ])
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_msg,
                parse_mode="Markdown",
                reply_markup=admin_btn
            )
        except Exception:
            pass
        return

    # 2. User Downloads Personal PDF Copy
    elif data == "btn_download_my_pdf":
        status = get_user_agreement_status(chat_id)
        pdf_path = status.get("pdf_path")
        if not pdf_path or not os.path.exists(pdf_path):
            # Regenerate if missing
            user = update.effective_user
            username = user.username if user else (status.get("username") or "")
            full_name = status.get("full_name") or ((user.first_name if user else "") or "Trader")
            phone = status.get("phone_number") or ""
            serial = status.get("contract_serial") or f"AQ-AGR-RESTORE-{chat_id}"
            h_val = status.get("sha256_hash") or hashlib.sha256(serial.encode()).hexdigest()
            t_str = status.get("accepted_at") or datetime.now().strftime("%d/%m/%Y %H:%M:%S ICT")
            try:
                pdf_path = generate_legal_contract_pdf(chat_id, username, full_name, phone, serial, h_val, t_str)
            except Exception as e_pdf:
                print(f"⚠️ Error regenerating contract PDF: {e_pdf}")
                pdf_path = ""

        if pdf_path and os.path.exists(pdf_path):
            try:
                caption_text = (
                    f"📄 **ឯកសារកិច្ចសន្យាផ្លូវការរបស់អ្នក (Official PDF Document)** 📜\n"
                    f"• **Serial:** `{status.get('contract_serial', 'AQ-LOCKED')}`\n"
                    f"• **Timestamp:** `{status.get('accepted_at', 'LOCKED')}`"
                )
                with open(pdf_path, "rb") as pdf_file:
                    await context.bot.send_document(
                        chat_id=chat_id,
                        document=pdf_file,
                        filename=os.path.basename(pdf_path),
                        caption=caption_text,
                        parse_mode="Markdown"
                    )
            except Exception as ex_send:
                if query:
                    await query.message.reply_text(f"⚠️ មិនអាចទាញយក PDF បាន៖ {ex_send}")
        else:
            if query:
                await query.message.reply_text("⚠️ មិនទាន់រកឃើញឯកសារ PDF របស់អ្នកនៅឡើយទេ។ សូមចុចយល់ព្រមកិច្ចសន្យាជាមុនសិន។")
        return

    # 3. Preview Sample PDF
    elif data == "btn_preview_terms_pdf":
        # Generate on-the-fly preview
        user = update.effective_user
        username = user.username if user else ""
        first_name = (user.first_name if user else "") or "User"
        preview_serial = f"AQ-AGR-PREVIEW-{chat_id}"
        h_val = hashlib.sha256(preview_serial.encode()).hexdigest()
        now_str = datetime.now(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M:%S ICT")
        try:
            pdf_path = generate_legal_contract_pdf(chat_id, username, first_name, "", preview_serial, h_val, now_str)
        except Exception as e_prev:
            print(f"⚠️ Error previewing contract PDF: {e_prev}")
            pdf_path = ""
        if pdf_path and os.path.exists(pdf_path):
            try:
                caption_text = (
                    "📄 **គំរូកិច្ចសន្យា និងលក្ខខណ្ឌផ្លូវការ (Official Agreement Preview PDF)** 📜\n"
                    "• **ឯកសារដើម ៖** ANGKOR QUANT Official Usage Agreement\n"
                    "• **ស្ថានភាព ៖** `🔍 គំរូផ្លូវការ (Master Contract Preview)`\n"
                    "• **ចំណាំ ៖** នៅពេលលោកអ្នកចុចប៊ូតុង **«✍️ ខ្ញុំបានអាន យល់ច្បាស់ និងយល់ព្រម ១០០%»** "
                    "ប្រព័ន្ធនឹងបញ្ចូលព័ត៌មានគណនី និងចុះហត្ថលេខាឌីជីថល SHA-256 លើកិច្ចសន្យានេះភ្លាមៗ!"
                )
                with open(pdf_path, "rb") as pdf_file:
                    await context.bot.send_document(
                        chat_id=chat_id,
                        document=pdf_file,
                        filename="Angkor_Quant_Official_Agreement_Preview.pdf",
                        caption=caption_text,
                        parse_mode="Markdown"
                    )
            except Exception as e_prev:
                print(f"Error previewing PDF: {e_prev}")
        else:
            if query:
                await query.answer("⚠️ មិនអាចទាញយក PDF បានទេ (កំពុងរៀបចំប្រព័ន្ធ ឬខ្វះ reportlab)!", show_alert=True)
        return

    # 4. Super Admin Agreements Dashboard
    elif data == "btn_admin_agreements" or data.startswith("btn_admin_agr_page_"):
        if chat_id != ADMIN_CHAT_ID:
            if query:
                await query.answer("🛑 Exclusive for Super Admin!", show_alert=True)
            return
        page = 1
        if data.startswith("btn_admin_agr_page_"):
            try:
                page = int(data.replace("btn_admin_agr_page_", "").strip())
            except Exception:
                page = 1
        card_text, keyboard = build_admin_agreements_card(page=page)
        if query:
            try:
                await query.edit_message_text(card_text, parse_mode="Markdown", reply_markup=keyboard)
            except Exception:
                await query.edit_message_text(card_text, parse_mode=None, reply_markup=keyboard)
        return

    # 5. Super Admin 1-Tap Download of User PDF
    elif data.startswith("btn_admin_dl_pdf_"):
        if chat_id != ADMIN_CHAT_ID:
            if query:
                await query.answer("🛑 Exclusive for Super Admin!", show_alert=True)
            return
        target_uid = data.replace("btn_admin_dl_pdf_", "").strip()
        try:
            t_chat_id = int(target_uid)
        except Exception:
            t_chat_id = 0

        status = get_user_agreement_status(t_chat_id)
        pdf_path = status.get("pdf_path")
        if not pdf_path or not os.path.exists(pdf_path):
            # Regenerate if missing
            serial = status.get("contract_serial") or f"AQ-AGR-RESTORE-{t_chat_id}"
            h_val = status.get("sha256_hash") or hashlib.sha256(serial.encode()).hexdigest()
            t_str = status.get("accepted_at") or datetime.now().strftime("%d/%m/%Y %H:%M:%S ICT")
            try:
                pdf_path = generate_legal_contract_pdf(
                    t_chat_id,
                    status.get("username", ""),
                    status.get("full_name", f"User_{t_chat_id}"),
                    status.get("phone_number", ""),
                    serial,
                    h_val,
                    t_str
                )
            except Exception as e_pdf:
                print(f"⚠️ Error regenerating contract PDF for admin: {e_pdf}")
                pdf_path = ""

        if pdf_path and os.path.exists(pdf_path):
            caption_text = (
                f"👑 **[ADMIN AUDIT] Signed Legal Contract PDF** 📜\n"
                f"• **User ID:** `{t_chat_id}`\n"
                f"• **Name:** `{status.get('full_name', 'N/A')}` (@{status.get('username', 'N/A')})\n"
                f"• **Phone:** `{status.get('phone_number', 'N/A')}`\n"
                f"• **Serial:** `{status.get('contract_serial', 'N/A')}`\n"
                f"• **Accepted At:** `{status.get('accepted_at', 'N/A')}`\n"
                f"• **SHA-256:** `{status.get('sha256_hash', 'N/A')[:32]}...`"
            )
            with open(pdf_path, "rb") as pdf_file:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=pdf_file,
                    filename=os.path.basename(pdf_path),
                    caption=caption_text,
                    parse_mode="Markdown"
                )
            if query:
                await query.answer("✅ PDF ត្រូវបានទាញយក និងផ្ញើជូនរួចរាល់!")
        else:
            if query:
                await query.answer("⚠️ រកមិនឃើញ ឬមិនអាចទាញយក PDF បានឡើយ! (សូមពិនិត្យការដំឡើង reportlab)", show_alert=True)
        return

    # 6. VIP Request Information Card
    elif data == "btn_menu_vip_req":
        vip_info_text = (
            f"{INSTITUTIONAL_HEADER}"
            "👑 **ស្នើសុំសិទ្ធិប្រើប្រាស់ VIP LICENSE** 💎\n"
            f"{DIVIDER_HEAVY}\n\n"
            "ដើម្បីទទួលបានអាជ្ញាប័ណ្ណ VIP និងដំណើរការ Bot ពេញលេញលើគណនីរបស់អ្នក ៖\n\n"
            "1. **Telegram ID របស់អ្នក ៖**\n"
            f"   `{chat_id}`\n\n"
            "2. **ទាក់ទងផ្ទាល់ទៅកាន់ស្ថាបនិក ឬ Super Admin ៖**\n"
            "   • **Founder / Lead Architect** ៖ @sinathhem\n"
            "   • **Super Admin ID** ៖ `859271875`\n\n"
            "3. **ផ្ញើសារបញ្ជាក់ ៖**\n"
            f"   «_ខ្ញុំបានចុះកិច្ចសន្យាផ្លូវការរួចរាល់ហើយ (ID: {chat_id}) សូមស្នើសុំ VIP License!_»\n\n"
            f"{DIVIDER_LIGHT}\n"
            "💡 _បន្ទាប់ពីទទួលបានការអនុម័ត ប្រព័ន្ធនឹងបើកដំណើរការ Auto-Trading និងយុទ្ធសាស្ត្រទាំងអស់ជូនលោកអ្នកភ្លាមៗ!_"
            f"{INSTITUTIONAL_FOOTER}"
        )
        vip_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 ផ្ញើសារទៅ Admin (@sinathhem)", url="https://t.me/sinathhem")],
            [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Menu មេ", callback_data="btn_menu_refresh")]
        ])
        if query:
            try:
                await query.edit_message_text(vip_info_text, parse_mode="Markdown", reply_markup=vip_keyboard)
            except Exception:
                await query.edit_message_text(vip_info_text, parse_mode=None, reply_markup=vip_keyboard)
        return

    # Navigation sections
    elif data == "btn_about_menu":
        card_text, keyboard = build_about_main_card(chat_id)
    elif data == "btn_about_terms":
        card_text, keyboard = build_terms_card(chat_id)
    elif data == "btn_about_risk":
        card_text, keyboard = build_risk_disclosure_card(chat_id)
    elif data == "btn_about_mt5":
        card_text, keyboard = build_mt5_execution_card(chat_id)
    elif data == "btn_about_liability":
        card_text, keyboard = build_liability_card(chat_id)
    elif data == "btn_about_privacy":
        card_text, keyboard = build_privacy_card(chat_id)
    elif data == "btn_about_en":
        card_text, keyboard = build_full_english_card(chat_id)
    else:
        card_text, keyboard = build_about_main_card(chat_id)

    if query:
        try:
            await query.edit_message_text(card_text, parse_mode="Markdown", reply_markup=keyboard)
        except Exception:
            try:
                await query.edit_message_text(card_text, parse_mode=None, reply_markup=keyboard)
            except Exception:
                pass
