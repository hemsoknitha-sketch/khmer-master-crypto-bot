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
