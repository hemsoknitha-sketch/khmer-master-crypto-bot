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
        if app and app.loop:
            # Check if we are already in an event loop
            try:
                loop = asyncio.get_running_loop()
                await app.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
            except RuntimeError:
                # We are not in an async context, schedule it threadsafe
                asyncio.run_coroutine_threadsafe(app.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode), app.loop)
    except Exception as e:
        logger.error(f"Failed to send telegram message to {chat_id}: {e}")

