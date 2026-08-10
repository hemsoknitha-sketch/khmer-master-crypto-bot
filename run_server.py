import os
import sys

# CRITICAL: Forces PyQt5 to run headless so it doesn't crash on Linux VPS without a graphical display
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from dotenv import load_dotenv
from ai_engine import AIInvestmentEngine
from bot_thread import TelegramBotThread

def main():
    print("==================================================")
    print("🚀 Starting Apex AI Bot in Headless Server Mode...")
    print("==================================================")
    
    # Load environment variables
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not bot_token or not gemini_api_key:
        print("❌ Error: Missing API keys in .env file.")
        print("Please make sure you have TELEGRAM_BOT_TOKEN and GEMINI_API_KEY configured.")
        sys.exit(1)

    # Initialize AI Engine
    ai_engine = AIInvestmentEngine(gemini_api_key)
    
    # Initialize Bot Thread
    bot_thread = TelegramBotThread(bot_token, ai_engine)
    
    # Connect GUI log signals to standard output terminal instead
    bot_thread.log_signal.connect(lambda msg: print(f"[BOT LOG]: {msg}"))
    
    print("✅ Initialization complete. Bot is now polling Telegram...")
    
    # Run the bot synchronously in the main thread (blocking)
    # We call run() directly instead of start() so it blocks the main thread
    try:
        bot_thread.run()
    except KeyboardInterrupt:
        print("\n🛑 KeyboardInterrupt received. Stopping Server cleanly...")
        bot_thread.stop()

if __name__ == "__main__":
    main()
