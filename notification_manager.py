import asyncio
import logging
import datetime

# Configure a silent logger for ICO
logger = logging.getLogger("ICO_Notification")
logger.setLevel(logging.INFO)
fh = logging.FileHandler('ico_silent_logs.txt', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

async def _safe_bot_send(bot, chat_id: int, text: str, parse_mode: str = "HTML"):
    """
    Safely dispatches bot.send_message with automatic fallback to plain-text on parse errors.
    Catches all exceptions within the coroutine to eliminate 'Task exception was never retrieved'.
    """
    import re
    # Intelligent parse_mode auto-detection
    has_html_tags = bool(re.search(r'<\/?(?:b|strong|i|em|code|pre|a|u|s|strike|tg-spoiler)\b', text, re.IGNORECASE))
    if has_html_tags:
        parse_mode = "HTML"

    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
    except Exception as ex:
        err_str = str(ex).lower()
        if "parse entities" in err_str or "can't parse" in err_str or "badrequest" in err_str:
            try:
                # Cleanly strip HTML tags before fallback so raw tags are never shown to user
                clean_text = re.sub(r'<[^>]+>', '', text)
                await bot.send_message(chat_id=chat_id, text=clean_text, parse_mode=None)
                return
            except Exception as ex2:
                logger.error(f"Fallback clean-text message failed for {chat_id}: {ex2}")
        else:
            logger.error(f"Failed to send telegram message to {chat_id}: {ex}")

async def send_smart_notification(app, chat_id: int, text: str, category: str = "INFO", parse_mode="HTML"):
    """
    Intelligent Notification Throttle.
    Filters out noise (like Insufficient Balance) and only sends important alerts to the user.
    Categories: CRITICAL, ACTION, INFO, SILENT
    """
    
    # 1. SPAM FILTER (Insufficient Balance)
    if "Insufficient USDT Balance" in text or ("Balance" in text and "Insufficient" in text) or "Insufficient Balance" in text:
        logger.info(f"SILENCED [User {chat_id}]: {text}")
        return # Drop silently!
        
    # 2. CATEGORY FILTER
    if category == "SILENT":
        logger.info(f"SILENCED [User {chat_id}]: {text}")
        return
        
    # Log all actions
    logger.info(f"{category} [User {chat_id}]: {text}")
    
    # 3. SEND TO TELEGRAM
    try:
        if app and hasattr(app, "bot"):
            try:
                loop = asyncio.get_running_loop()
                if loop and loop.is_running():
                    asyncio.create_task(_safe_bot_send(app.bot, chat_id, text, parse_mode=parse_mode))
                    return
            except RuntimeError:
                pass

            app_loop = None
            if hasattr(app, "bot_data") and isinstance(app.bot_data, dict):
                app_loop = app.bot_data.get("loop")
            if not app_loop:
                try:
                    import bot_thread
                    app_loop = getattr(bot_thread, "MAIN_BOT_LOOP", None)
                except Exception:
                    pass

            if app_loop and app_loop.is_running():
                asyncio.run_coroutine_threadsafe(_safe_bot_send(app.bot, chat_id, text, parse_mode=parse_mode), app_loop)
    except Exception as e:
        logger.error(f"Failed to send telegram message to {chat_id}: {e}")

async def send_telegram_alert(chat_id: int, text: str, parse_mode: str = "HTML") -> bool:
    """
    Universal non-blocking Telegram alert dispatcher for any component (Web GUI, MT5 Bridge, Watchdogs).
    Attempts active in-process bot application first, then falls back to direct async REST HTTP request.
    """
    if not chat_id:
        return False

    import re
    # Intelligent parse_mode auto-detection
    has_html_tags = bool(re.search(r'<\/?(?:b|strong|i|em|code|pre|a|u|s|strike|tg-spoiler)\b', text, re.IGNORECASE))
    if has_html_tags:
        parse_mode = "HTML"

    # 1. Try active in-process Telegram Application
    try:
        import bot_thread
        app = getattr(bot_thread, "MAIN_BOT_APP", None)
        if app and hasattr(app, "bot"):
            try:
                loop = asyncio.get_running_loop()
                if loop and loop.is_running():
                    asyncio.create_task(_safe_bot_send(app.bot, chat_id, text, parse_mode=parse_mode))
                    return True
            except RuntimeError:
                pass

            app_loop = getattr(bot_thread, "MAIN_BOT_LOOP", None)
            if app_loop and app_loop.is_running():
                asyncio.run_coroutine_threadsafe(_safe_bot_send(app.bot, chat_id, text, parse_mode=parse_mode), app_loop)
                return True
    except Exception:
        pass

    # 2. Direct Telegram REST API Fallback
    import os
    import aiohttp
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token or bot_token == "your_telegram_bot_token_here":
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5.0)) as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200 and "parse" in (await resp.text()).lower():
                    # Cleanly strip HTML tags so raw tags are never shown to user
                    payload["text"] = re.sub(r'<[^>]+>', '', text)
                    payload.pop("parse_mode", None)
                    async with session.post(url, json=payload) as resp2:
                        return resp2.status == 200
                return resp.status == 200
    except Exception as e:
        logger.error(f"Failed to send direct REST telegram alert to {chat_id}: {e}")
        return False

async def broadcast_admin(text: str, parse_mode: str = "HTML") -> int:
    """
    Broadcasts message to Master Admin (859271875) and all registered system admins.
    """
    import os
    admin_ids = {859271875}
    env_admin = os.getenv("TELEGRAM_ADMIN_ID")
    if env_admin and env_admin.isdigit():
        admin_ids.add(int(env_admin))
    try:
        import database as db
        for aid in db.get_all_admins():
            admin_ids.add(int(aid))
    except Exception:
        pass

    sent = 0
    for aid in admin_ids:
        try:
            ok = await send_telegram_alert(aid, text, parse_mode=parse_mode)
            if ok:
                sent += 1
        except Exception:
            pass
    return sent

# Backward-compatibility alias
send_telegram_notification = send_telegram_alert


