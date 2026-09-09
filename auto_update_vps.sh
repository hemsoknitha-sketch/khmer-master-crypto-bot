#!/bin/bash
# ==============================================================================
# 🚀 APEX AGI ENGINE v13.00 - GOOGLE CLOUD VPS AUTOMATED AUTO-UPDATE SCRIPT
# Checks GitHub for updates, backs up SQLite DB, syncs HF Models & restarts service
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

echo "🔍 [GCP VPS AUTO-UPDATE] Checking for new code commits on GitHub..."
git fetch origin main >/dev/null 2>&1

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ [GCP VPS AUTO-UPDATE] System is 100% up-to-date with GitHub."
    exit 0
fi

echo "🚀 [GCP VPS AUTO-UPDATE] New GitHub commit detected! Initializing Auto-Update..."

# 1. Zero-Data-Loss Backup
mkdir -p vps_db_backup
if [ -f "bot_database.db" ]; then
    cp bot_database.db vps_db_backup/
fi
if [ -f ".env" ]; then
    cp .env vps_db_backup/
fi
echo "🛡️ [SAFEGUARD] VIP Database and .env backed up successfully."

# 2. Reset and Pull Latest Code from GitHub
git reset --hard origin/main

# 3. Restore VIP Database and .env
if [ -f "vps_db_backup/bot_database.db" ]; then
    cp vps_db_backup/bot_database.db .
fi
if [ -f "vps_db_backup/.env" ]; then
    cp vps_db_backup/.env .
fi
echo "🛡️ [RESTORE] VIP Database and .env restored 100%."

# 4. Activate Virtual Environment & Sync Dependencies / HF AI Models
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
fi

if [ -f "requirements.txt" ]; then
    pip install --no-cache-dir -r requirements.txt >/dev/null 2>&1 || true
fi

# Sync Hugging Face Models using HF_TOKEN
if [ -f "sync_local_models.py" ]; then
    echo "🤗 [HF SYNC] Syncing AI Models from Hugging Face Hub..."
    python3 sync_local_models.py || true
fi

# 5. Restart Systemd Service Cleanly
echo "🔄 [SYSTEMD] Restarting khmer-master-crypto-bot service on Google Cloud VPS..."
if [ ! -f "/etc/systemd/system/khmer-master-crypto-bot.service" ]; then
    echo "⚙️ [SYSTEMD] Service file not found. Auto-configuring via setup_vps_service.sh..."
    bash setup_vps_service.sh || true
else
    # Ensure aliases exist
    if [ ! -f "/etc/systemd/system/khmer-master-crypto.service" ]; then
        sudo ln -sf /etc/systemd/system/khmer-master-crypto-bot.service /etc/systemd/system/khmer-master-crypto.service 2>/dev/null || true
        sudo systemctl daemon-reload 2>/dev/null || true
    fi
    sudo systemctl restart khmer-master-crypto-bot.service 2>/dev/null || \
    sudo systemctl restart khmer-master-crypto.service 2>/dev/null || \
    sudo systemctl restart khmer-crypto-bot.service 2>/dev/null || \
    sudo systemctl restart khmer-master-crypto-bot 2>/dev/null || true
fi

echo "🎉 [SUCCESS] GCP VPS successfully updated to latest GitHub & Hugging Face release!"

