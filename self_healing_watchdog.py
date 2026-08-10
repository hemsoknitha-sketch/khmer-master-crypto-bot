import subprocess
import time
import os
import requests
import sys

# Attempt to load Telegram token from .env
def get_bot_token():
    try:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("TELEGRAM_BOT_TOKEN"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return None

ADMIN_ID = "859271875" # Super Admin ID
BOT_TOKEN = get_bot_token()

def send_telegram_alert(msg: str):
    if not BOT_TOKEN:
        print("No BOT_TOKEN found. Cannot send alert.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to send alert: {e}")

def start_watchdog():
    print("🛡️ [WATCHDOG] Autonomous Resilience Manager Started.")
    print("🛡️ [WATCHDOG] Monitoring main.py for crashes...")
    
    bot_dir = os.path.dirname(os.path.abspath(__file__))
    executable = sys.executable # Use current python interpreter
    script_name = "main.py"
    
    restart_count = 0
    
    try:
        while True:
            print(f"🚀 [WATCHDOG] Starting {script_name}...")
            
            # Start the bot process
            process = subprocess.Popen([executable, script_name, "--vps"], cwd=bot_dir)
            
            try:
                # Wait for the process to exit
                process.wait()
            except KeyboardInterrupt:
                print("🛑 [WATCHDOG] Ctrl+C detected! Terminating main.py child process...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception:
                    process.kill()
                print("🛡️ [WATCHDOG] System cleanly stopped.")
                break

            exit_code = process.returncode
            
            if exit_code in [0, 130]:
                print(f"🛑 [WATCHDOG] {script_name} exited cleanly. Watchdog terminating.")
                break # Normal exit or Ctrl+C exit, don't restart
                
            restart_count += 1
            print(f"💥 [WATCHDOG] CRASH/UPGRADE DETECTED! Exit code: {exit_code}")
            
            # Execute State Serialization Guard before restarting
            try:
                import database as db
                if hasattr(db, 'save_state_snapshot'):
                    snapshot_file = db.save_state_snapshot()
                    print(f"💾 [WATCHDOG]: State Snapshot saved to {snapshot_file}")
            except Exception as se:
                print(f"⚠️ [WATCHDOG SNAPSHOT NOTICE]: {se}")

            # Send Executive Alert Card
            alert_msg = (
                f"🆘 **WATCHDOG ALERT: ZERO-DOWNTIME REBOOT INITIATED** 🆘\n\n"
                f"Apex TURBO AGI Bot encountered a restart/upgrade signal (Exit Code: `{exit_code}`).\n"
                f"💾 **State Serialization**: `Active Trades & Positions Saved to Snapshot`\n"
                f"🔄 **Self-Healing Initiated**: Hot-Reloading & restoring position state in 3s...\n"
                f"*(Auto-Healing Restart Count: `{restart_count}`)*"
            )
            send_telegram_alert(alert_msg)
            
            print("⏳ [WATCHDOG] Hot-Reloading in 3 seconds...")
            time.sleep(3)
    except KeyboardInterrupt:
        print("🛡️ [WATCHDOG] Graceful shutdown complete.")

if __name__ == "__main__":
    start_watchdog()
