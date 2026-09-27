#!/bin/bash
# ==============================================================================
# 🏛️ KHMER MASTER CRYPTO / APEX SUPER BRAIN AI
# MT5 ACCOUNT CREDENTIAL CONFIGURATOR & FAST LOGIN TOOL
# ==============================================================================
# Usage:
#   bash login_mt5_account.sh <ACCOUNT_ID> <PASSWORD> [SERVER]
# Examples:
#   bash login_mt5_account.sh 52135153 "MySecretPass123" "GTCGlobalSA-Server 2"
#   bash login_mt5_account.sh 52133938 "AdminPass456" "GTCGlobalSA-Server 2"
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🏛️ KHMER MASTER CRYPTO — MT5 FAST LOGIN TOOL 🏛️${NC}"
echo -e "${CYAN}==============================================================================${NC}"

ACCOUNT_ID="$1"
PASSWORD="$2"
SERVER="${3:-GTCGlobalSA-Server 2}"

if [ -z "$ACCOUNT_ID" ] || [ -z "$PASSWORD" ]; then
    echo -e "${RED}❌ Missing required parameters!${NC}"
    echo -e "${YELLOW}Usage:   bash login_mt5_account.sh <ACCOUNT_ID> <PASSWORD> [SERVER]${NC}"
    echo -e "${YELLOW}Example: bash login_mt5_account.sh 52135153 \"MyPassword123\" \"GTCGlobalSA-Server 2\"${NC}"
    exit 1
fi

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")

MT5_ADMIN="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5"
MT5_PLATFORM="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"

TARGET_DIR=""
INSTANCE_NAME=""

# Auto-detect target instance directory
if [ "$ACCOUNT_ID" == "52133938" ]; then
    TARGET_DIR="$MT5_ADMIN"
    INSTANCE_NAME="Super Admin MT5 (52133938)"
elif [ "$ACCOUNT_ID" == "52135153" ]; then
    TARGET_DIR="$MT5_PLATFORM"
    INSTANCE_NAME="Platform MT5 (52135153)"
else
    # Default to platform if exists, else admin
    if [ -d "$MT5_PLATFORM" ]; then
        TARGET_DIR="$MT5_PLATFORM"
        INSTANCE_NAME="Platform MT5 ($ACCOUNT_ID)"
    else
        TARGET_DIR="$MT5_ADMIN"
        INSTANCE_NAME="Admin MT5 ($ACCOUNT_ID)"
    fi
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Target MT5 directory not found at: $TARGET_DIR${NC}"
    exit 1
fi

echo -e "👤 Target User:     ${BOLD}${CYAN}$TARGET_USER${NC}"
echo -e "🎯 Target Instance: ${BOLD}${YELLOW}$INSTANCE_NAME${NC}"
echo -e "📁 Directory:       ${CYAN}$TARGET_DIR${NC}"
echo -e "🔑 Account ID:      ${GREEN}$ACCOUNT_ID${NC}"
echo -e "🌐 Server:          ${GREEN}$SERVER${NC}"
echo ""

# 1. Write startup.ini with credentials
cat << EOF > "$TARGET_DIR/startup.ini"
[Common]
Login=$ACCOUNT_ID
Password=$PASSWORD
Server=$SERVER
EOF

chown "$TARGET_USER:$TARGET_USER" "$TARGET_DIR/startup.ini"
chmod 600 "$TARGET_DIR/startup.ini"

mkdir -p "$TARGET_DIR/config"
cp -f "$TARGET_DIR/startup.ini" "$TARGET_DIR/config/startup.ini"
chown "$TARGET_USER:$TARGET_USER" "$TARGET_DIR/config/startup.ini"
chmod 600 "$TARGET_DIR/config/startup.ini"

echo -e "${GREEN}✅ Successfully written credentials to startup.ini (root & config/)!${NC}"

# Auto-detect active X display (XRDP on Ubuntu typically uses :10.0, fallback :0.0)
DETECTED_DISPLAY="${DISPLAY:-:10.0}"
if [ -e /tmp/.X11-unix/X10 ]; then
    DETECTED_DISPLAY=":10.0"
elif [ -e /tmp/.X11-unix/X0 ]; then
    DETECTED_DISPLAY=":0.0"
fi

# 2. Restart target MT5 instance in Wine with /config:startup.ini
echo -e "${YELLOW}🔄 Restarting target MT5 instance to establish live connection (Display $DETECTED_DISPLAY)...${NC}"

if [ "$TARGET_DIR" == "$MT5_PLATFORM" ]; then
    # Force kill lingering Platform instance
    pkill -9 -f "MetaTrader 5_Platform.*terminal64.exe" 2>/dev/null || true
    sleep 2
    sudo -u "$TARGET_USER" DISPLAY="$DETECTED_DISPLAY" bash -c "cd '$MT5_PLATFORM' && nohup wine terminal64.exe /portable /config:startup.ini >/dev/null 2>&1 &"
    echo -e "${GREEN}🚀 Platform MT5 instance restarted in Wine with credentials!${NC}"
else
    # Force kill lingering Admin instance
    pkill -9 -f "MetaTrader 5/terminal64.exe" 2>/dev/null || true
    sleep 2
    sudo -u "$TARGET_USER" DISPLAY="$DETECTED_DISPLAY" bash -c "cd '$MT5_ADMIN' && nohup wine terminal64.exe /portable /config:startup.ini >/dev/null 2>&1 &"
    echo -e "${GREEN}🚀 Admin MT5 instance restarted in Wine with credentials!${NC}"
fi

echo ""
echo -e "${BOLD}${GREEN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}🎉 MT5 ACCOUNT LOGIN CONFIGURED SUCCESSFULLY!${NC}"
echo -e "${CYAN}👉 MT5 is now connecting to $SERVER...${NC}"
echo -e "${CYAN}👉 Verify live balance in Telegram via: /mt5${NC}"
echo -e "${BOLD}${GREEN}==============================================================================${NC}"
