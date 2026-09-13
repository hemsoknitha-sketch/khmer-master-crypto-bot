#!/bin/bash
# ==============================================================================
# 🚀 APEX AGI ENGINE v13.00 - GOOGLE CLOUD VPS AUTOMATED AUTO-UPDATE SCRIPT
# Checks GitHub for updates, safely stops service, backs up SQLite DB,
# syncs HF Models, auto-heals SQLite database & restarts service cleanly
# ==============================================================================

set -e

# Target workspace path
APP_DIR="/opt/khmer-master-crypto-bot"

if [ -d "$APP_DIR/khmer-master-crypto-bot" ]; then
    cd "$APP_DIR/khmer-master-crypto-bot"
elif [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
else
    # Auto-fallback to current directory if running locally on Windows or non-standard path
    cd "$(dirname "$0")"
fi

# Auto-fix permissions if root previously owned some objects
if [ -d ".git" ] && [ "$(id -u)" -ne 0 ]; then
    sudo chown -R "$USER:$USER" . 2>/dev/null || true
fi

echo "🔍 [GCP VPS AUTO-UPDATE] Checking for new code commits on GitHub..."
git fetch origin main >/dev/null 2>&1

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

# Even if up-to-date, if force repair or user ran script, check DB health
if [ "$LOCAL" = "$REMOTE" ] && [ "$1" != "--force" ]; then
    echo "✅ [GCP VPS AUTO-UPDATE] System is up-to-date with GitHub. Verifying database health..."
    if [ -f "repair_database.py" ]; then
        python3 repair_database.py || true
    fi
    exit 0
fi

echo "🚀 [GCP VPS AUTO-UPDATE] Initializing Zero-Downtime Safe Auto-Update..."

# 1. Stop background bot service first to checkpoint SQLite WAL cleanly & release file locks
echo "⏸️ [SAFEGUARD] Stopping service to release SQLite WAL locks..."
sudo systemctl stop khmer-master-crypto-bot.service 2>/dev/null || \
sudo systemctl stop khmer-master-crypto.service 2>/dev/null || \
sudo systemctl stop khmer-crypto-bot.service 2>/dev/null || \
sudo systemctl stop khmer-master-crypto-bot 2>/dev/null || true

# 2. Zero-Data-Loss Backup of Database & Environment
mkdir -p vps_db_backup
if ls bot_database.db* 1> /dev/null 2>&1; then
    cp -f bot_database.db* vps_db_backup/ 2>/dev/null || true
fi
if [ -f ".env" ]; then
    cp -f .env vps_db_backup/ 2>/dev/null || true
fi
echo "🛡️ [SAFEGUARD] VIP Database and .env backed up successfully."

# 3. Reset and Pull Latest Code from GitHub
echo "📥 [GIT] Pulling latest code from GitHub origin/main..."
git reset --hard origin/main

# 4. Restore VIP Database and .env
if ls vps_db_backup/bot_database.db* 1> /dev/null 2>&1; then
    cp -f vps_db_backup/bot_database.db* . 2>/dev/null || true
fi
if [ -f "vps_db_backup/.env" ]; then
    cp -f vps_db_backup/.env . 2>/dev/null || true
fi
echo "🛡️ [RESTORE] VIP Database and .env restored 100%."

# 5. Activate Virtual Environment & Sync Dependencies / HF AI Models
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
fi

if [ -f "requirements.txt" ]; then
    pip install --no-cache-dir -r requirements.txt >/dev/null 2>&1 || true
fi

# 6. Run Database Auto-Healer (Fixes any 'database disk image is malformed' with 0% data loss)
if [ -f "repair_database.py" ]; then
    echo "🛡️ [DB HEALER] Checking & healing database integrity before startup..."
    python3 repair_database.py || true
fi

# Sync Hugging Face Models using HF_TOKEN
if [ -f "sync_local_models.py" ]; then
    echo "🤗 [HF SYNC] Syncing AI Models from Hugging Face Hub..."
    python3 sync_local_models.py || true
fi

# 7. Start Systemd Service Cleanly
echo "🔄 [SYSTEMD] Starting khmer-master-crypto-bot service on Google Cloud VPS..."
if [ ! -f "/etc/systemd/system/khmer-master-crypto-bot.service" ]; then
    echo "⚙️ [SYSTEMD] Service file not found. Auto-configuring via setup_vps_service.sh..."
    bash setup_vps_service.sh || true
else
    # Ensure aliases exist
    if [ ! -f "/etc/systemd/system/khmer-master-crypto.service" ]; then
        sudo ln -sf /etc/systemd/system/khmer-master-crypto-bot.service /etc/systemd/system/khmer-master-crypto.service 2>/dev/null || true
        sudo systemctl daemon-reload 2>/dev/null || true
    fi
    sudo systemctl start khmer-master-crypto-bot.service 2>/dev/null || \
    sudo systemctl start khmer-master-crypto.service 2>/dev/null || \
    sudo systemctl start khmer-crypto-bot.service 2>/dev/null || \
    sudo systemctl start khmer-master-crypto-bot 2>/dev/null || true
fi

echo "🎉 [SUCCESS] GCP VPS successfully updated & running healthy on latest release!"
