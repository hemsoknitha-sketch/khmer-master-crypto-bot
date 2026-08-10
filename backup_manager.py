import os
import shutil
import time
from datetime import datetime, timedelta
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "bot_database.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

HOURLY_RETENTION = 24
DAILY_RETENTION = 7

def perform_backup(is_boot=False):
    """
    Performs a backup of the SQLite database.
    """
    if not os.path.exists(DB_FILE):
        print("⚠️ No database found to backup.")
        return False
        
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    now = datetime.now()
    
    # Prefix for boot backups versus regular scheduled backups
    prefix = "boot_" if is_boot else "hourly_"
    
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    backup_file_name = f"{prefix}bot_database_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_file_name)
    
    try:
        shutil.copy2(DB_FILE, backup_path)
        print(f"Database backed up successfully: {backup_file_name}")
        
        daily_prefix = "daily_bot_database_"
        today_date = now.strftime("%Y%m%d")
        daily_backup_name = f"{daily_prefix}{today_date}.db"
        daily_backup_path = os.path.join(BACKUP_DIR, daily_backup_name)
        
        if not os.path.exists(daily_backup_path):
            shutil.copy2(DB_FILE, daily_backup_path)
            print(f"Daily Database backup created: {daily_backup_name}")
            
        _prune_backups()
        return backup_path
    except Exception as e:
        print(f"Failed to backup database: {e}")
        return None

def _prune_backups():
    """
    Removes old backups exceeding the retention policy.
    """
    # 1. Prune hourly backups
    hourly_pattern = os.path.join(BACKUP_DIR, "hourly_bot_database_*.db")
    hourly_files = glob.glob(hourly_pattern)
    hourly_files.sort(key=os.path.getmtime, reverse=True) # newest first
    
    if len(hourly_files) > HOURLY_RETENTION:
        for old_file in hourly_files[HOURLY_RETENTION:]:
            try:
                os.remove(old_file)
                print(f"Removed old hourly backup: {os.path.basename(old_file)}")
            except Exception as e:
                print(f"Failed to remove old backup {old_file}: {e}")
                
    # 2. Prune daily backups
    daily_pattern = os.path.join(BACKUP_DIR, "daily_bot_database_*.db")
    daily_files = glob.glob(daily_pattern)
    daily_files.sort(key=os.path.getmtime, reverse=True)
    
    if len(daily_files) > DAILY_RETENTION:
        for old_file in daily_files[DAILY_RETENTION:]:
            try:
                os.remove(old_file)
                print(f"Removed old daily backup: {os.path.basename(old_file)}")
            except Exception as e:
                print(f"Failed to remove old daily backup {old_file}: {e}")
                
    # 3. Prune boot backups (Keep last 3 just in case)
    boot_pattern = os.path.join(BACKUP_DIR, "boot_bot_database_*.db")
    boot_files = glob.glob(boot_pattern)
    boot_files.sort(key=os.path.getmtime, reverse=True)
    
    if len(boot_files) > 3:
        for old_file in boot_files[3:]:
            try:
                os.remove(old_file)
            except:
                pass

if __name__ == "__main__":
    print("Running manual backup test...")
    perform_backup(is_boot=True)
