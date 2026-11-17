# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD INTERBANK SESSION INVESTMENT PLANNER (AQ88 Invariant 122)
===================================================================================
Institutional Real-World Gold (XAUUSD) Market Trading Sessions & Execution Roadmap.

Covers the 5 Real-World Interbank Gold Sessions:
  1. Asian Session & Shanghai Physical Gold Fix (07:00 – 13:30 ICT / 00:00 – 06:30 UTC)
  2. London Interbank Open & LBMA Kill Zone (13:30 – 18:30 ICT / 06:30 – 11:30 UTC)
  3. London / NY Overlap & COMEX Floor Open ("The Golden Power Hours") (18:30 – 23:30 ICT / 11:30 – 16:30 UTC)
  4. Wall Street Afternoon & Institutional Profit-Taking (23:30 – 03:30 ICT / 16:30 – 20:30 UTC)
  5. Overnight Rollover Swap Shield & Flat Cash (03:30 – 07:00 ICT / 20:30 – 23:59 UTC)

Fiduciary Principles:
  - Aligns algorithmic capital allocation with physical and OTC gold liquidity waves.
  - Zero entries during Session 5 to eliminate 3x-10x spread blowout and overnight financing swaps.
  - High-conviction scaling (1.25x) during NY/COMEX Power Hours.
"""

import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Tuple, List, Optional

# ICT Timezone (UTC+7 - Cambodia / Indochina Time)
ICT_TZ = timezone(timedelta(hours=7))

# ── 5 INTERBANK GOLD SESSIONS SPECIFICATION ──
GOLD_SESSIONS_SPEC: List[Dict[str, Any]] = [
    {
        "id": "SESSION_1_ASIA",
        "name": "ASIAN_RANGE_SHANGHAI",
        "title_kh": "🌏 វគ្គទីផ្សារអាស៊ី & ផ្សារមាសសៀងហៃ (Asian & Shanghai Gold)",
        "icon": "🌏",
        "start_ict": "07:00",
        "end_ict": "13:30",
        "start_utc": "00:00",
        "end_utc": "06:30",
        "start_mins": 7 * 60,         # 420 mins
        "end_mins": 13 * 60 + 30,     # 810 mins
        "risk_multiplier": 0.85,
        "is_trading_allowed": True,
        "strategy_label": "Boundary Mean-Reversion & Turtle Soup Sweeps",
        "strategy_kh": "ជួញដូរនៅតាមព្រំដែន Range (Fib 0.618 / OLS 2σ) & ស្ទាក់ចាប់ Turtle Soup",
        "key_events": [
            "07:00 ICT (00:00 UTC) - Tokyo & Asian Interbank Open",
            "08:00 ICT (01:00 UTC) - Shanghai Gold Exchange (SGE) Open",
            "08:15 ICT (01:15 UTC) - SGE AM Gold Benchmark Price Fix",
            "13:30 ICT (06:30 UTC) - SGE PM Gold Benchmark Price Fix"
        ],
        "guidance": "ទីផ្សារកសាង Dealing Range (Asian High / Asian Low)។ ហាមដាច់ខាតមិនឱ្យដេញថ្លៃកណ្តាល Chop Zone (35%-65%)។"
    },
    {
        "id": "SESSION_2_LONDON",
        "name": "LONDON_OPEN_LBMA",
        "title_kh": "🏛️ វគ្គទីផ្សារឡុងដ៏ & LBMA Interbank Open (London Gold)",
        "icon": "🏛️",
        "start_ict": "13:30",
        "end_ict": "18:30",
        "start_utc": "06:30",
        "end_utc": "11:30",
        "start_mins": 13 * 60 + 30,   # 810 mins
        "end_mins": 18 * 60 + 30,     # 1110 mins
        "risk_multiplier": 1.00,
        "is_trading_allowed": True,
        "strategy_label": "Judas Swing Sweep Fade & London Trend Expansion",
        "strategy_kh": "ស្ទាក់ចាប់ Judas Swing ក្លែងក្លាយ & បើកតាមរលកកម្លាំងពិតប្រាកដ London Expansion",
        "key_events": [
            "13:30 ICT (06:30 UTC) - London Pre-Market Positioning",
            "14:00 ICT (07:00 UTC) - London LBMA Interbank Cash Market Open",
            "17:30 ICT (10:30 UTC) - LBMA AM Gold Price Auction Fix (Global Benchmark)"
        ],
        "guidance": "ស្ថាប័នហិរញ្ញវត្ថុអឺរ៉ុបចាក់ Liquidity ខ្លាំង។ ស្ទាក់ចាប់ក្បាលព្រួញបោកប្រាស់ (Judas Wick) នៅលើកំពូល/បាត Asian Range។"
    },
    {
        "id": "SESSION_3_NY_POWER",
        "name": "NY_COMEX_POWER_HOURS",
        "title_kh": "⚡ វគ្គត្រួតគ្នាកំពូល NY / London & COMEX (The Golden Power Hours)",
        "icon": "⚡",
        "start_ict": "18:30",
        "end_ict": "23:30",
        "start_utc": "11:30",
        "end_utc": "16:30",
        "start_mins": 18 * 60 + 30,   # 1110 mins
        "end_mins": 23 * 60 + 30,     # 1410 mins
        "risk_multiplier": 1.25,
        "is_trading_allowed": True,
        "strategy_label": "Institutional Momentum & Multi-TF Trend Stacking",
        "strategy_kh": "រលក Momentum ស្ថាប័នកំពូល & 19-TF Trend Stacking (Pos 1 Scalp + Runner)",
        "key_events": [
            "19:30/20:30 ICT (12:30/13:30 UTC) - US Macro News (CPI, NFP, Core PCE, FOMC)",
            "20:30 ICT (13:30 UTC) - Wall Street Cash Open & COMEX Gold Futures Floor Open",
            "22:00 ICT (15:00 UTC) - LBMA PM Gold Price Auction Fix (Central Bank Benchmark)"
        ],
        "guidance": "ពេលវេលាមាសកើបចំណេញធំបំផុតក្នុងថ្ងៃ (70% នៃទំហំចលនាមាសកើតឡើងត្រង់នេះ)។ កើប Pos 1 Scalp (+20p) និងចាក់សោរ Breakeven ឱ្យ Runner រត់ដល់ TP2/TP3!"
    },
    {
        "id": "SESSION_4_NY_AFTERNOON",
        "name": "NY_AFTERNOON_HARVEST",
        "title_kh": "🌇 វគ្គរសៀលញូវយ៉ក & កើបប្រាក់ចំណេញ (NY Afternoon & Profit Taking)",
        "icon": "🌇",
        "start_ict": "23:30",
        "end_ict": "03:30",
        "start_utc": "16:30",
        "end_utc": "20:30",
        "start_mins": 23 * 60 + 30,   # 1410 mins
        "end_mins": 3 * 60 + 30,      # Next day 210 mins (crosses midnight)
        "risk_multiplier": 0.50,
        "is_trading_allowed": True,
        "strategy_label": "Trend Exhaustion, Early Harvest & Capital Protection",
        "strategy_kh": "កាត់កើបចំណេញទាន់ពេល Micro-Exhaustion Harvest & ការពារប្រាក់ចំណេញថ្ងៃ",
        "key_events": [
            "23:30 ICT (16:30 UTC) - London & European Markets Close",
            "00:30 ICT (17:30 UTC) - COMEX Settlement Time"
        ],
        "guidance": "កម្លាំងទិញលក់ចាប់ផ្តើមថមថយ។ ផ្តោតសំខាន់លើការកើបប្រាក់ចំណេញដាក់ហោប៉ៅ ហាមបើក Position ធំៗថ្មីបន្ថែម។"
    },
    {
        "id": "SESSION_5_ROLLOVER_SHIELD",
        "name": "OVERNIGHT_ROLLOVER_SHIELD",
        "title_kh": "🛡️ របាំងការពារកម្រៃ Swap ឆ្លងយប់ & Spread ឡើងថ្លៃ (Overnight Rollover Shield)",
        "icon": "🛡️",
        "start_ict": "03:30",
        "end_ict": "07:00",
        "start_utc": "20:30",
        "end_utc": "23:59",
        "start_mins": 3 * 60 + 30,    # 210 mins
        "end_mins": 7 * 60,           # 420 mins
        "risk_multiplier": 0.00,
        "is_trading_allowed": False,
        "strategy_label": "Overnight Flat Cash Standby & Spread Blowout Armor",
        "strategy_kh": "ផ្អាកជួញដូរ ១០០% & ជម្រះ Flat Cash មុនម៉ោង Swap ឆ្លងយប់ 21:00 UTC",
        "key_events": [
            "04:00 - 05:00 ICT (21:00 - 22:00 UTC) - Broker Daily Maintenance & Rollover",
            "Wednesday Night - 3x Triple Rollover Swap Charge Window",
            "Broker Spread Expands 3x - 10x ($0.50 -> $2.50 - $5.00+)"
        ],
        "guidance": "ចន្លោះម៉ោងគ្រោះថ្នាក់បំផុត! Spread ឡើងថ្លៃខ្លាំង និងកាត់ថ្លៃ Swap។ ប្រព័ន្ធផ្អាកការបើក Position ថ្មី ១០០% ដើម្បីការពារដើមទុន។"
    }
]


class GoldSessionPlanner:
    """
    Core Planner Engine for Institutional Real-World Gold Sessions (AQ88 Invariant 122).
    """

    def __init__(self):
        self._cached_session: Optional[Dict[str, Any]] = None
        self._last_calc_ts = 0.0

    @staticmethod
    def get_current_ict_datetime(dt: Optional[datetime] = None) -> datetime:
        """Returns current localized Indochina Time (ICT / UTC+7)."""
        if dt is None:
            return datetime.now(ICT_TZ)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc).astimezone(ICT_TZ)
        return dt.astimezone(ICT_TZ)

    def get_current_session(self, dt: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Determines the current active real-world Gold trading session in ICT time.
        Calculates remaining session time, risk multiplier, and active guidelines.
        """
        now = time.time()
        if dt is None and (now - self._last_calc_ts) < 5.0 and self._cached_session:
            return self._cached_session

        ict_dt = self.get_current_ict_datetime(dt)
        cur_mins = ict_dt.hour * 60 + ict_dt.minute

        matched_spec = None
        # Check sessions
        for spec in GOLD_SESSIONS_SPEC:
            s_mins = spec["start_mins"]
            e_mins = spec["end_mins"]
            if s_mins < e_mins:
                # Normal daytime session (e.g. 07:00 to 13:30)
                if s_mins <= cur_mins < e_mins:
                    matched_spec = spec
                    break
            else:
                # Cross-midnight session (e.g. 23:30 to 03:30)
                if cur_mins >= s_mins or cur_mins < e_mins:
                    matched_spec = spec
                    break

        if not matched_spec:
            # Fallback to Session 1
            matched_spec = GOLD_SESSIONS_SPEC[0]

        # Calculate time remaining in current session
        end_mins = matched_spec["end_mins"]
        if end_mins > cur_mins:
            rem_mins = end_mins - cur_mins
        else:
            rem_mins = (24 * 60 - cur_mins) + end_mins
        rem_hours = rem_mins // 60
        rem_m = rem_mins % 60

        result = dict(matched_spec)
        result["current_time_ict"] = ict_dt.strftime("%H:%M:%S ICT")
        result["current_date_ict"] = ict_dt.strftime("%Y-%m-%d")
        result["current_time_utc"] = ict_dt.astimezone(timezone.utc).strftime("%H:%M:%S UTC")
        result["remaining_time_str"] = f"{rem_hours}h {rem_m}m"
        result["remaining_minutes"] = rem_mins

        if dt is None:
            self._cached_session = result
            self._last_calc_ts = now

        return result

    def is_trading_allowed(self, dt: Optional[datetime] = None) -> Tuple[bool, str]:
        """
        Strict Gatekeeper checking if opening a new Gold position is permitted right now.
        Returns: (is_allowed: bool, reason: str)
        """
        sess = self.get_current_session(dt)
        if not sess.get("is_trading_allowed", True):
            return (
                False,
                f"BLOCKED_OVERNIGHT_ROLLOVER_SHIELD: Current session is {sess['title_kh']} ({sess['start_ict']}-{sess['end_ict']} ICT). "
                f"All new entries strictly muted to eliminate spread blowout ($2-$5) and overnight financing swap drag."
            )
        return True, f"TRADING_PERMITTED: Active session is {sess['name']} (Risk Mult: {sess['risk_multiplier']}x)."

    def get_risk_multiplier(self, dt: Optional[datetime] = None) -> float:
        """Returns the dynamic position sizing risk multiplier for the current session."""
        sess = self.get_current_session(dt)
        return float(sess.get("risk_multiplier", 1.0))

    def format_session_badge(self, dt: Optional[datetime] = None) -> str:
        """
        Generates a concise 1-line session badge for embedding into live cards.
        Example: '⚡ វគ្គទីផ្សារ ៖ NY/COMEX Power Hours (Risk: 1.25x) 🟢 ACTIVE'
        """
        sess = self.get_current_session(dt)
        status_dot = "🟢 ACTIVE" if sess.get("is_trading_allowed", True) else "🛡️ STANDBY (SWAP SHIELD)"
        return f"{sess['icon']} <b>វគ្គទីផ្សារ ៖</b> <code>{sess['name']}</code> ({sess['start_ict']}-{sess['end_ict']} ICT) | Risk: <code>{sess['risk_multiplier']}x</code> {status_dot}"

    def build_gold_session_plan_card(self, chat_id: Optional[int] = None) -> str:
        """
        Builds the Master Institutional Gold Trading Plan & Session Roadmap Card in Khmer.
        """
        cur = self.get_current_session()
        ict_now = self.get_current_ict_datetime()

        lines = [
            "🏛️ <b>[ANGKOR QUANT - ផែនការវិនិយោគ GOLD តាមម៉ោងទីផ្សារពិភពលោក]</b> 💎",
            "══════════════════════════════════════",
            f"⏰ <b>ម៉ោងទីផ្សារបច្ចុប្បន្ន ៖</b> <code>{cur['current_time_ict']}</code> (<code>{cur['current_time_utc']}</code>)",
            f"📍 <b>វគ្គទីផ្សារកំពុងរត់ ៖</b> {cur['icon']} <b>{cur['title_kh']}</b>",
            f"⏳ <b>នៅសល់ក្នុងវគ្គនេះ ៖</b> <code>{cur['remaining_time_str']}</code> | Risk Mult: <code>{cur['risk_multiplier']}x</code>",
            f"🛡️ <b>ស្ថានភាពប្រតិបត្តិការ ៖</b> <b>{'🟢 អនុញ្ញាតជួញដូរ (ACTIVE)' if cur['is_trading_allowed'] else '🔴 ផ្អាកជួញដូរ (SWAP & SPREAD SHIELD)'}</b>",
            "──────────────────────────────────────",
            "📋 <b>កាលវិភាគវិនិយោគមាសទាំង ៥ វគ្គប្រចាំថ្ងៃ (24 Hours Roadmap) ៖</b>",
            ""
        ]

        for s in GOLD_SESSIONS_SPEC:
            is_active = (s["id"] == cur["id"])
            pointer = "▶️ <b>[កំពុងដំណើរការ]</b> " if is_active else "• "
            shield_tag = " [🛡️ គ្មានការជួញដូរ]" if not s["is_trading_allowed"] else ""
            lines.append(f"{pointer}{s['icon']} <b>{s['title_kh']}</b>{shield_tag}")
            lines.append(f"   └ <b>ម៉ោងកម្ពុជា (ICT) ៖</b> <code>{s['start_ict']} – {s['end_ict']}</code> (UTC: <code>{s['start_utc']}-{s['end_utc']}</code>)")
            lines.append(f"   └ <b>យុទ្ធសាស្ត្រស្នូល ៖</b> <i>{s['strategy_kh']}</i>")
            lines.append(f"   └ <b>ទម្ងន់ហានិភ័យ (Risk) ៖</b> <code>{s['risk_multiplier']}x</code> | <b>ព្រឹត្តិការណ៍ ៖</b> <code>{s['key_events'][0]}</code>")
            lines.append("")

        lines.extend([
            "──────────────────────────────────────",
            "👑 <b>គោលការណ៍ដែកការពារដើមទុន & ធានាប្រាក់ចំណេញ (Fiduciary Rules) ៖</b>",
            "1. <b>Session 3 (NY/COMEX Power Hours) ៖</b> ជាម៉ោងមាសកើបចំណេញធំបំផុត (Risk 1.25x) បើក Pos 1 Scalp (+20p) និង Trailing Runner ទៅ TP2 (+100p) & TP3 (+300p)!",
            "2. <b>Overnight Swap Shield (03:30 – 07:00 ICT) ៖</b> ហាមបើក Position ថ្មីដាច់ខាត ដើម្បីគេចផុតពី Spread ឡើងថ្លៃ $2-$5 និងកម្រៃ Swap ឆ្លងយប់ (ពិសេស 3x Triple Swap រាត្រីថ្ងៃពុធ)!",
            "3. <b>Universal Fleet Sync Exit ៖</b> គ្រប់ Position របស់ Super Admin និង VIP ត្រូវបានបិទព្រមគ្នា ១០០% គ្មានទុកឱ្យអ្នកណាម្នាក់ឯកោឡើយ!",
            "══════════════════════════════════════",
            "💡 <i>ប្រព័ន្ធ Quant Gold ដំណើរការស្វ័យប្រវត្ត 24/7 អនុវត្តតាមកាលវិភាគនេះយ៉ាងម៉ឺងម៉ាត់បំផុត!</i>"
        ])

        return "\n".join(lines)


# Singleton
_SESSION_PLANNER: Optional[GoldSessionPlanner] = None

def get_gold_session_planner() -> GoldSessionPlanner:
    global _SESSION_PLANNER
    if _SESSION_PLANNER is None:
        _SESSION_PLANNER = GoldSessionPlanner()
    return _SESSION_PLANNER
