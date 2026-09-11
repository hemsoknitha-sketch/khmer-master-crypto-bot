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

# Official Institutional Footnote
OFFICIAL_FOOTNOTE = (
    "_Khmer Master Crypto_\n"
    "_APEX SUPER BRAIN AI_\n"
    "ដំណើរការការពារហានិភ័យ & កើបចំណេញ ២៤/៧!"
)

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
