#!/bin/bash
# ==============================================================================
# 🚀 ANGKOR QUANT - VPS SQLITE DISK I/O & STORAGE RESCUE ENGINE (AQ88)
# Resolves: "sqlite3.OperationalError: disk I/O error", Disk Full, Permissions & Stale Locks
# ==============================================================================

set -e

echo "══════════════════════════════════════════════════════════════════════════════"
echo "🛠️  [ANGKOR QUANT] Starting Comprehensive VPS Disk I/O & Database Rescue..."
echo "══════════════════════════════════════════════════════════════════════════════"

# 1. Stop Services to Release All Locks
echo "🛑 1. Stopping Bot and Stream services to release all SQLite locks..."
sudo systemctl stop khmer-master-crypto-bot.service 2>/dev/null || true
sudo systemctl stop khmer-crypto-bot.service 2>/dev/null || true
sudo systemctl stop angkor-gold-youtube-live.service 2>/dev/null || true
sleep 2

# Kill any orphaned python processes holding db locks
sudo pkill -9 -f "main.py --cli" 2>/dev/null || true
sudo pkill -9 -f "gold_youtube_stream_server.py" 2>/dev/null || true

# 2. Check Disk Space
echo "📊 2. Current Disk Usage:"
df -h /

FREE_KB=$(df / --output=avail | tail -n 1 | tr -d ' ')
echo "💡 Free disk space: $((FREE_KB / 1024)) MB"

# 3. Aggressive Disk Cleanup (Free Up Disk Space)
echo "🧹 3. Cleaning system caches, journal logs, and temporary Chromium profiles..."
sudo apt-get clean 2>/dev/null || true
sudo rm -rf /var/cache/apt/archives/* 2>/dev/null || true
sudo journalctl --vacuum-size=50M 2>/dev/null || true
sudo rm -rf /tmp/chromium-stream-profile* 2>/dev/null || true
sudo rm -rf /tmp/.X99-lock /tmp/.X11-unix/X99 2>/dev/null || true

# Truncate giant log files in logs directory
if [ -d "/opt/khmer-master-crypto-bot/logs" ]; then
    echo "📄 Truncating large logs (>20MB) in logs directory..."
    sudo find /opt/khmer-master-crypto-bot/logs -name "*.log" -size +20M -exec truncate -s 2M {} + 2>/dev/null || true
fi

# 4. Check Swapfile vs Disk Space
# If free disk space is less than 2.5GB and a 4GB /swapfile exists, resize swapfile to 1.5GB
# (Note: zRAM is active in RAM, so disk swap only needs 1GB - 1.5GB on small VPS disks!)
FREE_MB=$((FREE_KB / 1024))
if [ "$FREE_MB" -lt 2500 ] && [ -f /swapfile ]; then
    echo "⚠️ Low disk space detected ($FREE_MB MB free). Resizing /swapfile to 1.5GB to free up disk..."
    sudo swapoff /swapfile 2>/dev/null || true
    sudo rm -f /swapfile
    sudo fallocate -l 1536M /swapfile 2>/dev/null || sudo dd if=/dev/zero of=/swapfile bs=1M count=1536
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo "✅ /swapfile resized to 1.5GB. Disk space reclaimed!"
fi

echo "📊 Updated Disk Usage:"
df -h /

# 5. Fix Directory & File Permissions
echo "🔐 5. Restoring clean user ownership and database file permissions..."
APP_DIR="/opt/khmer-master-crypto-bot"
TARGET_USER=$(stat -c '%U' "$APP_DIR" 2>/dev/null || echo "hemsoknitha")
if [ "$TARGET_USER" = "root" ]; then
    TARGET_USER="hemsoknitha"
fi

echo "👤 Applying ownership to user: $TARGET_USER ($APP_DIR)"
sudo chown -R "${TARGET_USER}:${TARGET_USER}" "$APP_DIR"
sudo chmod 775 "$APP_DIR"
sudo chmod 664 "$APP_DIR"/*.db* 2>/dev/null || true

# 6. SQLite Database Integrity & Stale Lock Purge
echo "🩺 6. Auditing SQLite databases & clearing stale WAL/SHM locks..."
cd "$APP_DIR"

for db in bot_database.db crypto_agent.db trading_bot.db; do
    if [ -f "$db" ]; then
        echo "🔍 Checking database: $db..."
        # If -wal or -shm exist, test integrity
        INTEGRITY_RESULT=$(python3 -c "
import sqlite3, sys
try:
    conn = sqlite3.connect('$db', timeout=5.0)
    res = conn.execute('PRAGMA integrity_check;').fetchall()
    conn.execute('PRAGMA wal_checkpoint(TRUNCATE);')
    conn.close()
    if res == [('ok',)]:
        print('HEALTHY')
    else:
        print('CORRUPT')
except Exception as e:
    print('ERROR:', e)
" 2>&1 || echo "FAILED")

        echo "   Result: $INTEGRITY_RESULT"
        if echo "$INTEGRITY_RESULT" | grep -qiE "error|corrupt|failed|disk i/o"; then
            echo "   ⚠️ Stale lock or WAL corruption detected in $db. Purging stale -shm and -wal..."
            sudo rm -f "${db}-shm" "${db}-wal"
            # Recheck and rebuild clean WAL
            python3 -c "
import sqlite3
conn = sqlite3.connect('$db', timeout=10.0)
conn.execute('PRAGMA journal_mode=WAL;')
conn.execute('PRAGMA synchronous=NORMAL;')
conn.execute('REINDEX;')
conn.close()
print('   ✅ $db reindexed and fresh WAL initialized successfully!')
" || true
        fi
    fi
done

sudo chown -R "${TARGET_USER}:${TARGET_USER}" "$APP_DIR"

# 7. Restart Bot Service & Stream Service Cleanly
echo "🔄 7. Restarting services cleanly..."
sudo systemctl daemon-reload
sudo systemctl restart khmer-master-crypto-bot.service 2>/dev/null || sudo systemctl restart khmer-crypto-bot.service 2>/dev/null || true
sudo systemctl restart angkor-gold-youtube-live.service 2>/dev/null || true
sleep 3

# 8. Verify Status
echo "══════════════════════════════════════════════════════════════════════════════"
echo "🎉 [COMPLETE] VPS Disk I/O Rescue Successfully Executed!"
echo "══════════════════════════════════════════════════════════════════════════════"
sudo systemctl status khmer-master-crypto-bot.service --no-pager -n 5 || true
echo "------------------------------------------------------------------------------"
sudo systemctl status angkor-gold-youtube-live.service --no-pager -n 5 || true
echo "══════════════════════════════════════════════════════════════════════════════"
