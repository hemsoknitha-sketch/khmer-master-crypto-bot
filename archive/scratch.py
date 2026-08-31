def get_market_brief_text(lang):
        user_lang = lang if lang in texts else 'khmer'
        return f"🌅 **Daily Market Brief**\n\n{texts[user_lang]}"