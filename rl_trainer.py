import os
import subprocess
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RL_Trainer")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_SCRIPT = os.path.join(BASE_DIR, "train_model.py")

def execute_nightly_training():
    """Runs the train_model.py script as a subprocess for RL Continuous Learning."""
    logger.info("🧠 [RL Trainer] Starting Nightly AI Training Job...")
    try:
        # Run the training script in a detached process to avoid blocking the main bot loop
        process = subprocess.Popen(["python", TRAIN_SCRIPT], cwd=BASE_DIR)
        logger.info(f"🧠 [RL Trainer] Training job launched successfully. PID: {process.pid}")
    except Exception as e:
        logger.error(f"❌ [RL Trainer] Failed to start nightly training: {e}")

async def start_rl_trainer():
    """Starts the APScheduler for nightly training."""
    scheduler = AsyncIOScheduler()
    # Schedule the job to run at 02:00 AM every day
    scheduler.add_job(execute_nightly_training, 'cron', hour=2, minute=0)
    scheduler.start()
    logger.info("🧠 RL Continuous Learning Scheduler Initialized (Runs at 02:00 AM).")
