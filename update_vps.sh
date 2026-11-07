#!/bin/bash
# ==============================================================================
# ANGKOR QUANT - QUANT GOLD VPS FAST UPDATE SCRIPT (update_vps.sh)
# Target: Google Cloud Linux VPS 'quant-gold' (us-central1-a, quant-gold-514007)
# ==============================================================================

set -e

APP_DIR="/opt/khmer-master-crypto-bot"
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
else
    cd "$(dirname "$0")"
fi

echo "🚀 [QUANT GOLD VPS UPDATE] Running automated zero-downtime update..."
bash auto_update_vps.sh "$@"

