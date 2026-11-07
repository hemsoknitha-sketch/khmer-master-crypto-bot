#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
  ANGKOR QUANT - CAPITAL.COM USERS AUDITOR & SYNCHRONIZATION ENGINE
===============================================================================
Institutional Quantitative Governance & Safe User Ingestion System (AQ84 / AQ87)
Author: HEM SINATH | Angkor Quant AI Engine
Environment: Ubuntu Linux GCP VPS & Windows Desktop
===============================================================================
"""

import sys
import os
import sqlite3
import logging
from typing import Dict, List, Optional, Any

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import database as db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CAPITAL_USER_SYNC")


def ensure_database_indexes():
    """Ensures O(log N) B-Tree indexes exist for tens of thousands of users."""
    conn = db.get_db_connection()
    c = conn.cursor()
    indexes = [
        ("idx_user_capital_acc", "user_capital_credentials", "account_id"),
        ("idx_user_capital_demo_acc", "user_capital_credentials", "demo_account_id"),
        ("idx_user_capital_ref", "user_capital_credentials", "referral_code"),
        ("idx_capital_auto_cfg_enabled", "capital_auto_config", "is_enabled"),
        ("idx_capital_auto_trades_chat_status", "capital_auto_trades", "chat_id, status"),
        ("idx_capital_auto_trades_deal", "capital_auto_trades", "deal_id")
    ]
    created = 0
    for idx_name, table, cols in indexes:
        try:
            c.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table} ({cols})")
            created += 1
        except Exception as e:
            logger.debug(f"Index notice for {idx_name}: {e}")
    conn.commit()
    conn.close()
    return created


def audit_capital_users() -> List[Dict[str, Any]]:
    """Audits all registered Capital.com users in the database."""
    conn = db.get_db_connection()
    c = conn.cursor()
    users = []
    try:
        query = """
            SELECT c.chat_id, c.account_id, c.demo_account_id, c.is_demo, 
                   c.is_referral_verified, c.referral_code,
                   COALESCE(cfg.is_enabled, 0), COALESCE(cfg.budget, 200.0),
                   COALESCE(u.username, 'User_' || c.chat_id)
            FROM user_capital_credentials c
            LEFT JOIN capital_auto_config cfg ON c.chat_id = cfg.chat_id
            LEFT JOIN users u ON c.chat_id = u.chat_id
        """
        c.execute(query)
        rows = c.fetchall()
        for r in rows:
            users.append({
                "chat_id": r[0],
                "account_id": r[1],
                "demo_account_id": r[2],
                "is_demo": bool(r[3]),
                "is_referral_verified": bool(r[4]),
                "referral_code": r[5],
                "auto_enabled": bool(r[6]),
                "budget": float(r[7]),
                "username": r[8]
            })
    except Exception as e:
        logger.error(f"Error auditing capital users: {e}")
    finally:
        conn.close()
    return users


def find_user_by_account_id(account_id: str) -> Optional[Dict[str, Any]]:
    """Finds a user by exact or partial account ID."""
    clean = str(account_id or "").strip()
    return db.get_capital_user_by_account_id(clean)


def sync_user_to_quant_gold(chat_id: int, budget: float = 300.0, max_positions: int = 5, is_demo: bool = False):
    """Safely synchronizes an existing Capital user into Quant Gold autonomous trading."""
    db.set_capital_auto_config(
        chat_id=chat_id,
        enabled=True,
        budget=budget,
        max_positions=max_positions,
        is_demo=is_demo
    )
    logger.info(f"✅ User {chat_id} successfully synchronized and activated for Quant Gold 24/7!")


def run_full_diagnostic():
    print("=" * 70)
    print("  🥇 ANGKOR QUANT - CAPITAL.COM FLEET USER AUDIT & SYNC ENGINE")
    print("=" * 70)

    # 1. Database Indexes
    idx_count = ensure_database_indexes()
    print(f"📊 High-Concurrency Indexes: ✅ {idx_count} Indexes Verified (O(log N) Lookups)")

    # 2. Audit Registered Users
    users = audit_capital_users()
    print(f"👥 Total Registered Capital Users: {len(users)}")
    print("-" * 70)
    for u in users:
        live_str = "🟡 DEMO" if u["is_demo"] else "🟢 LIVE"
        ref_str = "🟢 VERIFIED" if u["is_referral_verified"] else "⚪ UNVERIFIED"
        auto_str = "🟢 ON" if u["auto_enabled"] else "🔴 OFF"
        print(f"• Chat ID: {u['chat_id']} | User: {u['username']}")
        print(f"  Account ID: {u['account_id']} | Demo ID: {u['demo_account_id']} | Mode: {live_str}")
        print(f"  Referral: {ref_str} | Quant Gold Auto: {auto_str} (${u['budget']:.2f})")
        print()

    # 3. Check Specific Target Accounts: 331963468326458564 & 332192407263204548
    target_accounts = ["331963468326458564", "332192407263204548"]
    print("=" * 70)
    print("🎯 TARGET ACCOUNT AUDIT & RESOLUTION CHECK:")
    print("=" * 70)

    for target in target_accounts:
        res = find_user_by_account_id(target)
        if res:
            print(f"✅ Account ID [{target}] RESOLVED SUCCESSFULLY:")
            print(f"   Chat ID: {res['chat_id']}")
            print(f"   Username: {res['username']}")
            print(f"   Mode: {'DEMO' if res['is_demo'] else 'LIVE MAINNET'}")
            print(f"   Referral Verified: {'YES' if res['is_referral_verified'] else 'NO'}")
            auto_cfg = db.get_capital_auto_config(res['chat_id']) or {}
            print(f"   Quant Gold Autonomous Status: {'🟢 ACTIVE' if auto_cfg.get('is_enabled') else '🔴 PAUSED'}")
        else:
            print(f"⚠️ Account ID [{target}] NOT FOUND in this local database clone.")
            print(f"   Notice: If this user registered on the remote Linux VPS, their credentials")
            print(f"   are stored in the VPS production database: /opt/khmer-master-crypto-bot/bot_database.db")
        print("-" * 70)


if __name__ == "__main__":
    run_full_diagnostic()
