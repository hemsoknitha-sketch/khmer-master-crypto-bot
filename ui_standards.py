# ui_standards.py
"""
==============================================================================
KHMER MASTER CRYPTO - INSTITUTIONAL MOBILE UI & TYPOGRAPHY STANDARDS
==============================================================================
Calibrated for Zero Line-Wrap on ALL Mobile Devices (iOS & Android).
A smartphone screen width is ~6.5cm to 7.0cm. In Telegram mobile chat bubbles,
a 12-character Unicode box divider corresponds physically to ~2.0 cm (approx 1/3
of screen width), ensuring a clean, modern, institutional look that NEVER
overflows or wraps down to a second line even under large font settings.
"""

import re

# Standard 2.0 cm Mobile-Fit Dividers (12 characters)
DIVIDER_HEAVY = "━━━━━━━━━━━━"   # Heavy line (12 chars ~ 2.0 cm)
DIVIDER_LIGHT = "────────────"   # Light line (12 chars ~ 2.0 cm)
DIVIDER_DASH  = "┈┈┈┈┈┈┈┈┈┈┈┈"   # Dotted line (12 chars ~ 2.0 cm)
DIVIDER_DOUBLE = "════════════"  # Double line (12 chars ~ 2.0 cm)

# Backward-compatible aliases
SEP_HEAVY = DIVIDER_HEAVY
SEP_LIGHT = DIVIDER_LIGHT
SEP_DASH = DIVIDER_DASH
SEP_DOUBLE = DIVIDER_DOUBLE

# Official Brand Identity Standards (ANGKOR QUANT)
AQ_BRAND_NAME = "ANGKOR QUANT"
AQ_TAGLINE = "AI Quantitative Intelligence for Global Markets"
AQ_SHORT_DESC = "AI Quant • Automated Trading • Global Markets"
AQ_VERSION = "Angkor Quant v4.0 (AQ47)"

SUPER_ADMIN_ID = 859271875

INSTITUTIONAL_HEADER = (
    "🏛️ **ANGKOR QUANT** ⚡\n"
    f"_{AQ_TAGLINE}_\n"
    f"{DIVIDER_DOUBLE}\n"
)

INSTITUTIONAL_FOOTER = (
    f"\n{DIVIDER_LIGHT}\n"
    "🏛️ **ANGKOR QUANT** • AI Quantitative Intelligence\n"
    "💡 នេះជាមូលដ្ឋានសម្រាប់ស្រាវជ្រាវបន្ថែម • សូមធ្វើការសម្រេចចិត្តដោយទទួលខុសត្រូវ!"
)

# Backward-compatible aliases
HEADER_STANDARD = INSTITUTIONAL_HEADER
FOOTER_STANDARD = INSTITUTIONAL_FOOTER

# Official Institutional Footnote
OFFICIAL_FOOTNOTE = (
    "_Angkor Quant_\n"
    "_AI Quantitative Intelligence for Global Markets_\n"
    "ដំណើរការការពារហានិភ័យ & កើបចំណេញ ២៤/៧!"
)

def format_institutional_message(
    body: str,
    chat_id: int = 0,
    is_admin: bool = False,
    include_header: bool = True,
    include_footer: bool = True
) -> str:
    """
    Formats institutional responses for VIP Users by applying the official
    Header and Disclaimer Footer, while guaranteeing unredacted, unconstrained
    telemetry views for Super Admin ID: 859271875.
    """
    clean_body = body.strip()
    
    # If explicitly Super Admin and raw debug is requested, return clean body
    if (chat_id == SUPER_ADMIN_ID or is_admin) and not (include_header or include_footer):
        return clean_body
        
    parts = []
    if include_header:
        parts.append(INSTITUTIONAL_HEADER)
    parts.append(clean_body)
    if include_footer:
        parts.append(INSTITUTIONAL_FOOTER)
        
    return "".join(parts)

def get_divider(style: str = "heavy") -> str:
    """
    Returns the official 2.0 cm mobile-calibrated divider.
    Styles supported: 'heavy', 'light', 'dash', 'double'.
    """
    style_lower = (style or "heavy").lower()
    if style_lower == "light":
        return DIVIDER_LIGHT
    elif style_lower == "dash":
        return DIVIDER_DASH
    elif style_lower == "double":
        return DIVIDER_DOUBLE
    return DIVIDER_HEAVY


# ==============================================================================
# SACRED FIDUCIARY COVENANT: OFFICIAL RISK & RESPONSIBLE INVESTING DISCLAIMERS
# ==============================================================================
OFFICIAL_RISK_DISCLAIMER_KM = (
    "⚠️ **ការក្រើនរំលឹកពីហានិភ័យ និងការទទួលខុសត្រូវ ៖**\n"
    "ការវិនិយោគលើរូបិយបណ្ណឌីជីថល និងកិច្ចសន្យាដេរីវ៉េទីវ មានហានិភ័យទីផ្សារខ្ពស់ដែលអាចបាត់បង់ដើមទុន។ "
    "ប្រព័ន្ធ Angkor Quant ផ្ដល់ជូននូវការវិភាគផ្អែកលើគំរូគណិតវិទ្យា និងទិន្នន័យជាក់ស្តែង គ្មានការធានាផលចំណេញ ១០០% ឡើយ។ "
    "សូមវិនិយោគដោយការទទួលខុសត្រូវ គ្រប់គ្រងដើមទុនឱ្យបានហ្មត់ចត់ និងកំណត់ Stop-Loss ជានិច្ច!"
)

OFFICIAL_RISK_DISCLAIMER_EN = (
    "⚠️ **Risk & Fiduciary Disclaimer:**\n"
    "Digital assets and derivative trading involve substantial risk of capital loss. "
    "Angkor Quant provides quantitative probability models with zero 100% profit guarantees. "
    "Please trade responsibly, enforce strict Stop-Loss limits, and manage risk diligently."
)

OFFICIAL_RISK_DISCLAIMER_ZH = (
    "⚠️ **风险与合规提示：**\n"
    "数字资产及衍生品交易具有较高的资本损失风险。Angkor Quant 提供基于数学模型的概率分析，绝无 100% 收益保证。请务必理性投资，严格执行止损与风控管理。"
)

def get_risk_disclaimer(lang: str = "km") -> str:
    """Returns the official risk disclosure in the requested language."""
    clean_l = str(lang or "km").lower().strip()
    if clean_l in ["en", "english"]:
        return OFFICIAL_RISK_DISCLAIMER_EN
    elif clean_l in ["zh", "chinese"]:
        return OFFICIAL_RISK_DISCLAIMER_ZH
    return OFFICIAL_RISK_DISCLAIMER_KM

def sanitize_anti_guarantee_text(text: str) -> str:
    """
    Scans and permanently purges any false guarantees, 100% safety claims,
    or unrealistic profit promises from AI responses, enforcing fiduciary honesty.
    """
    if not text or not isinstance(text, str):
        return ""
    
    sanitized = text

    # Khmer Replacements
    replacements_km = [
        (r'ធានាសុវត្ថិភាពទុន\s*(?:១០០%|100%)', 'គ្រប់គ្រងហានិភ័យការពារដើមទុនជាអតិបរមា'),
        (r'ធានាសុវត្ថិភាព\s*(?:១០០%|100%)', 'បង្កើនសុវត្ថិភាពខ្ពស់បំផុត'),
        (r'ធានាចំណេញសុទ្ធ\s*(?:១០០%|100%)', 'កំណត់គោលដៅប្រាក់ចំណេញសុទ្ធ'),
        (r'ចំណេញ\s*(?:១០០%|100%)\s*ពេញលេញ', 'ប្រាក់ចំណេញតាមគោលដៅ'),
        (r'ចំណេញ\s*១០០%', 'បង្កើនប្រសិទ្ធភាពចំណេញ'),
        (r'ធានាដាច់ខាតមិនឱ្យខាត(?:ដើម)?', 'កាត់បន្ថយហានិភ័យខាតបង់ជាអតិបរមា'),
        (r'ធានាថាមិនខាតបង់ប្រាក់ដើម', 'ការពារដើមទុនជាអាទិភាព'),
        (r'ធានាថាមិនអាចធ្លាក់', 'ការពារកុំឱ្យធ្លាក់'),
        (r'ធានាមិនបាត់ដើមទុន\s*\$0\.00', 'កូដ Smart Contract នឹង Revert ដើម្បីការពារដើមទុន'),
        (r'ធានាមិនឱ្យរបូតមកខាតបង់', 'ជួយការពារផលចំណេញមិនឱ្យរបូតមកវិញ'),
        (r'ធានាមិនឱ្យខាតពីរសងខាង', 'ការពារកុំឱ្យខាតពីរសងខាង'),
        (r'ធានាសល់ចំណេញសុទ្ធ', 'គណនាផលចំណេញសុទ្ធ'),
        (r'ធានាថា\s*១\s*ឈ្នះស្រង់បាន', 'ជួយឱ្យ ១ ឈ្នះស្រង់បាន')
    ]
    for pattern, repl in replacements_km:
        sanitized = re.sub(pattern, repl, sanitized, flags=re.IGNORECASE)

    # English Replacements
    replacements_en = [
        (r'100%\s*guarantee[d]?', 'disciplined risk-managed'),
        (r'guarantee[ds]?\s*100%\s*profit', 'targets positive net expectancy'),
        (r'100%\s*safe\s*capital', 'strictly risk-managed capital'),
        (r'Zero-Loss Guarantee:?\s*`?100%\s*Wins Only`?', 'Disciplined Loss Mitigation Standard'),
        (r'Zero Market Risk \(100% Guaranteed Cash\)', 'Cash & Stablecoin Reserve (Risk-Mitigated)')
    ]
    for pattern, repl in replacements_en:
        sanitized = re.sub(pattern, repl, sanitized, flags=re.IGNORECASE)

    return sanitized

