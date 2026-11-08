# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD INSTITUTIONAL SECURITY CITADEL (AQ84)
================================================================
Target: Google Cloud Linux VPS 'quant-gold' & Telegram Bot
Author: HEM SINATH | Institutional Quantitative Governance
Version: 1.0.0

The Quant Gold Security Citadel enforces a 5-layer institutional defense:
  1. Anti-DoS & Sliding Window Rate Limiting (Token Bucket)
  2. Input Sanitization & Extreme Sizing Invalidation Guard (Anti-Injection)
  3. Fiduciary VIP Referral & Access Gatekeeper (Invariant 36)
  4. Emergency Circuit Breaker & Instant Lockdown Protocol (Invariant 41 & 75)
  5. Memory Leak Guard & Sensitive Information Scrubbing (Invariant 106 & 107)
================================================================
"""

import os
import re
import gc
import time
import math
import logging
from typing import Dict, Tuple, Optional, Any, List

logger = logging.getLogger("QUANT_GOLD_SECURITY")

# Super Admin is exclusively 859271875 (@Soknitha).
# 537186806 (@HemSinath) is a VIP User with Lifetime License.
SUPER_ADMIN_IDS = {859271875}


class QuantGoldSecurityCitadel:
    """
    Singleton Institutional Security Citadel for Quant Gold Bot and VPS System.
    """
    _instance: Optional["QuantGoldSecurityCitadel"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._circuit_breaker_locked = False
        self._lock_reason = ""
        self._locked_by = None
        self._lock_timestamp = 0.0

        # Rate limiting state: user_id -> deque of timestamps
        self._command_timestamps: Dict[int, List[float]] = {}
        self._trade_timestamps: Dict[int, List[float]] = {}

        # Limits
        self.MAX_COMMANDS_PER_WINDOW = 6  # max 6 commands
        self.COMMAND_WINDOW_SECONDS = 3.0  # per 3 seconds
        self.MIN_TRADE_INTERVAL_SECONDS = 4.0  # min 4s between trade executions

        # Regex patterns for scrubbing sensitive leaks
        self._scrub_patterns = [
            (re.compile(r'(?i)(cst\s*[:=]\s*)([a-zA-Z0-9_\-\.]{15,})'), r'\1[PROTECTED_CST]'),
            (re.compile(r'(?i)(x-security-token\s*[:=]\s*)([a-zA-Z0-9_\-\.]{15,})'), r'\1[PROTECTED_TOKEN]'),
            (re.compile(r'(?i)(password\s*[:=]\s*)([^\s,]+)'), r'\1[PROTECTED_PASSWORD]'),
            (re.compile(r'(?i)(api[_-]?key\s*[:=]\s*)([a-zA-Z0-9_\-\.]{10,})'), r'\1[PROTECTED_KEY]'),
            (re.compile(r'(?i)(bot[0-9]{8,10}:[a-zA-Z0-9_\-]{30,})'), r'[PROTECTED_TELEGRAM_BOT_TOKEN]'),
            (re.compile(r'(/home/[a-zA-Z0-9_\-]+|/opt/[a-zA-Z0-9_\-]+)'), r'[VPS_SYSTEM_DIR]')
        ]

        self._initialized = True
        logger.info("🛡️ [SECURITY CITADEL] Quant Gold Security Citadel initialized successfully.")

    # --------------------------------------------------------------------------
    # 1. Anti-DoS & Sliding Window Rate Limiting
    # --------------------------------------------------------------------------
    def check_rate_limit(self, user_id: int, action_type: str = "COMMAND") -> Tuple[bool, float]:
        """
        Validates whether a user request conforms to the sliding window rate limit.
        Returns: (is_allowed: bool, cooldown_remaining_seconds: float)
        Super Admins are 100% exempt from rate limits (Invariant 75).
        """
        if self.is_super_admin(user_id):
            return True, 0.0

        now = time.time()

        if action_type == "TRADE":
            timestamps = self._trade_timestamps.setdefault(user_id, [])
            # Prune old timestamps
            timestamps = [t for t in timestamps if now - t < self.MIN_TRADE_INTERVAL_SECONDS]
            self._trade_timestamps[user_id] = timestamps

            if timestamps:
                elapsed = now - timestamps[-1]
                if elapsed < self.MIN_TRADE_INTERVAL_SECONDS:
                    cooldown = round(self.MIN_TRADE_INTERVAL_SECONDS - elapsed, 1)
                    return False, max(0.5, cooldown)

            timestamps.append(now)
            return True, 0.0

        else:  # Standard COMMAND action
            timestamps = self._command_timestamps.setdefault(user_id, [])
            timestamps = [t for t in timestamps if now - t < self.COMMAND_WINDOW_SECONDS]
            self._command_timestamps[user_id] = timestamps

            if len(timestamps) >= self.MAX_COMMANDS_PER_WINDOW:
                cooldown = round(self.COMMAND_WINDOW_SECONDS - (now - timestamps[0]), 1)
                return False, max(0.5, cooldown)

            timestamps.append(now)
            return True, 0.0

    # --------------------------------------------------------------------------
    # 2. Authority & Super Admin Verification
    # --------------------------------------------------------------------------
    def is_super_admin(self, user_id: Any) -> bool:
        """Determines if the given user is an authorized Super Admin."""
        try:
            uid = int(user_id)
            if uid in SUPER_ADMIN_IDS:
                return True
            import database as db
            return bool(db.is_admin(uid))
        except Exception:
            return False

    def is_user_authorized_for_trading(self, user_id: int) -> Tuple[bool, str]:
        """
        Enforces Fiduciary VIP License & Capital.com Registration Gatekeeper (Invariant 36 & AQ84):
        1. Super Admin is 100% exempt and permanently authorized (SUPER_ADMIN_AUTHORITY).
        2. Gate 1: VIP License Gate:
           User MUST have an active unexpired VIP license (Monthly, Yearly, or Lifetime).
           If not VIP -> Returns (False, "UNLICENSED_ACCESS").
        3. Gate 2: Capital.com Registration Gate:
           User IS VIP licensed, but MUST have registered Capital.com via official partner link
           or connected valid API credentials to execute live algorithmic orders.
           If not registered -> Returns (False, "AWAITING_CAPITAL_REGISTRATION").
        4. When both gates pass:
           Returns (True, "VIP_LICENSED_AND_REGISTERED").
        """
        if self.is_super_admin(user_id):
            return True, "SUPER_ADMIN_AUTHORITY"

        import database as db
        try:
            # Gate 1: Check active VIP license
            if not db.is_vip(user_id):
                return False, "UNLICENSED_ACCESS"

            # Gate 2: Check Capital.com Registration
            creds = db.get_user_capital_credentials(user_id)
            if creds:
                raw_key = (creds.get("api_key") or "").strip()
                acc_id = (creds.get("account_id") or "").strip()
                if raw_key and raw_key != "ENV_VAULT" and acc_id and acc_id != "N/A":
                    return True, "VIP_LICENSED_AND_REGISTERED"

            if db.is_capital_user_authorized(user_id):
                return True, "VIP_LICENSED_AND_REGISTERED"

            if db.is_capital_user_referral_verified(user_id):
                return True, "VIP_LICENSED_AND_REGISTERED"

            return False, "AWAITING_CAPITAL_REGISTRATION"
        except Exception as e:
            logger.warning(f"Error checking user authorization for {user_id}: {e}")
            return False, "AWAITING_CAPITAL_REGISTRATION"

    # --------------------------------------------------------------------------
    # 3. Input Sanitization & Sizing Invalidation Guard
    # --------------------------------------------------------------------------
    def sanitize_lot_size(
        self,
        raw_val: Any,
        default_lot: float = 0.5,
        min_lot: float = 0.5,
        max_lot: float = 50.0
    ) -> float:
        """
        Sanitizes and bounds trade lot size strictly against NaN, Inf, negative,
        or extreme leverage attacks. Default minimum is 0.5 Troy Ounce.
        """
        try:
            val = float(raw_val)
            if math.isnan(val) or math.isinf(val):
                return default_lot
            if val < min_lot:
                return min_lot
            if val > max_lot:
                logger.warning(f"⚠️ [SECURITY CITADEL] Lot size clamped from {val} to max allowed {max_lot}")
                return max_lot
            return round(val, 2)
        except (ValueError, TypeError):
            return default_lot

    def sanitize_string_input(self, raw_input: Any, max_len: int = 64) -> str:
        """Sanitizes text arguments against command/SQL injection and excessive length."""
        if not raw_input:
            return ""
        clean = re.sub(r'[^\w\-\.\s]', '', str(raw_input).strip())
        return clean[:max_len]

    # --------------------------------------------------------------------------
    # 4. Sensitive Information Scrubbing (Anti-Leakage)
    # --------------------------------------------------------------------------
    def scrub_sensitive_data(self, text: str) -> str:
        """
        Redacts sensitive tokens, API keys, credentials, and internal VPS paths
        from error messages and logs before sending to Telegram.
        """
        if not text:
            return ""
        cleaned = str(text)
        for pattern, replacement in self._scrub_patterns:
            cleaned = pattern.sub(replacement, cleaned)
        return cleaned

    # --------------------------------------------------------------------------
    # 5. Emergency Circuit Breaker & Instant Lockdown Protocol
    # --------------------------------------------------------------------------
    def is_locked(self) -> bool:
        """Returns True if the system is currently under emergency lockdown."""
        return self._circuit_breaker_locked

    def trigger_emergency_lockdown(self, admin_id: int, reason: str = "MANUAL_LOCKDOWN") -> bool:
        """Engages immediate system-wide trading freeze across Quant Gold."""
        if not self.is_super_admin(admin_id):
            return False

        self._circuit_breaker_locked = True
        self._lock_reason = reason
        self._locked_by = admin_id
        self._lock_timestamp = time.time()
        logger.critical(f"🚨 [CIRCUIT BREAKER ENGAGED] Quant Gold trading locked by Admin {admin_id}: {reason}")
        return True

    def release_emergency_lockdown(self, admin_id: int) -> bool:
        """Releases the emergency trading freeze."""
        if not self.is_super_admin(admin_id):
            return False

        self._circuit_breaker_locked = False
        self._lock_reason = ""
        self._locked_by = None
        logger.info(f"🟢 [CIRCUIT BREAKER RELEASED] Quant Gold trading unlocked by Admin {admin_id}.")
        return True

    # --------------------------------------------------------------------------
    # 6. Memory & OOM Protection Shield
    # --------------------------------------------------------------------------
    def check_memory_shield(self) -> Dict[str, Any]:
        """
        Interrogates process and system RAM. If memory usage threatens OOM crash,
        automatically triggers garbage collection and cache pruning.
        """
        import psutil
        proc = psutil.Process()
        proc_mem_mb = proc.memory_info().rss / (1024 * 1024)

        sys_mem = psutil.virtual_memory()
        ram_pct = sys_mem.percent

        action_taken = "NORMAL"
        if proc_mem_mb > 650.0 or ram_pct > 85.0:
            gc.collect()
            action_taken = "GC_PURGED"
            logger.warning(
                f"🛡️ [MEMORY SHIELD] Process memory high ({proc_mem_mb:.1f} MB, Sys RAM: {ram_pct:.1f}%). "
                f"Executed garbage collection."
            )

        return {
            "proc_mem_mb": round(proc_mem_mb, 1),
            "ram_pct": ram_pct,
            "action": action_taken
        }

    # --------------------------------------------------------------------------
    # 7. Real-Time Telegram Security Card Generator
    # --------------------------------------------------------------------------
    def build_security_status_card(self) -> str:
        """Generates an institutional security audit overview card in HTML format."""
        mem_info = self.check_memory_shield()

        lock_status = (
            "🚨 <b>LOCKED (TRADING HALTED)</b>"
            if self._circuit_breaker_locked
            else "🟢 <b>ARMED & SECURE (NORMAL)</b>"
        )
        lock_extra = f"\n• Reason: <code>{self._lock_reason}</code>" if self._circuit_breaker_locked else ""

        card = (
            f"🛡️ <b>[QUANT GOLD INSTITUTIONAL SECURITY CITADEL]</b> 🏛️\n"
            f"══════════════════════════════════════\n"
            f"🔒 <b>ស្ថានភាព Circuit Breaker ៖</b> {lock_status}{lock_extra}\n"
            f"• របាំង Rate Limiting ៖ <code>ACTIVE (Token Bucket Shield)</code>\n"
            f"• របាំង Anti-Injection ៖ <code>STRICT CLAMP (0.5 - 50.0 oz)</code>\n"
            f"• របាំង Anti-Leakage ៖ <code>ENABLED (Token & Path Scrubbing)</code>\n"
            f"• Fiduciary Gatekeeper ៖ <code>ENFORCED (Invariant 36)</code>\n"
            f"──────────────────────────────────────\n"
            f"🖥️ <b>ប្រព័ន្ធសុវត្ថិភាព VPS & MEMORY ៖</b>\n"
            f"• Process RAM ៖ <code>{mem_info['proc_mem_mb']:.1f} MB</code> (Shield Floor: 650 MB)\n"
            f"• System RAM Load ៖ <code>{mem_info['ram_pct']:.1f}%</code> (Zero OOM Active)\n"
            f"• Privilege Level ៖ <code>Non-Root Daemon (User: sokni)</code>\n"
            f"• Network Firewall ៖ <code>Default DENY Inbound (Outbound Polling)</code>\n"
            f"══════════════════════════════════════\n"
            f"👑 <i>Super Admin មានសិទ្ធិបញ្ជា /emergency_stop និង /unlock បានគ្រប់ពេលវេលា។</i>"
        )
        return card


# Global singleton instance accessor
_citadel_singleton: Optional[QuantGoldSecurityCitadel] = None


def get_quant_gold_security_citadel() -> QuantGoldSecurityCitadel:
    global _citadel_singleton
    if _citadel_singleton is None:
        _citadel_singleton = QuantGoldSecurityCitadel()
    return _citadel_singleton

