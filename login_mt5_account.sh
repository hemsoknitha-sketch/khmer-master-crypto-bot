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

# Auto-strip accidental angle brackets <...> if user copied placeholder syntax
ACCOUNT_ID="${ACCOUNT_ID#<}"
ACCOUNT_ID="${ACCOUNT_ID%>}"
PASSWORD="${PASSWORD#<}"
PASSWORD="${PASSWORD%>}"
SERVER="${SERVER#<}"
SERVER="${SERVER%>}"

if [ -z "$ACCOUNT_ID" ] || [ -z "$PASSWORD" ]; then
    echo -e "${RED}❌ Missing required parameters!${NC}"
    echo -e "${YELLOW}Usage:   bash login_mt5_account.sh <ACCOUNT_ID> <PASSWORD> [SERVER]${NC}"
    echo -e "${YELLOW}Example: bash login_mt5_account.sh 52135153 'MyPassword123' 'GTCGlobalSA-Server 2'${NC}"
    exit 1
fi

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")

MT5_ADMIN="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5"
MT5_PLATFORM="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"

TARGET_DIR=""
INSTANCE_NAME=""

# Auto-detect target instance directory
if [ "$ACCOUNT_ID" == "52135153" ]; then
    if [ -d "$MT5_PLATFORM" ]; then
        TARGET_DIR="$MT5_PLATFORM"
    else
        TARGET_DIR="$MT5_ADMIN"
    fi
    INSTANCE_NAME="Super Admin MT5 (52135153)"
elif [ "$ACCOUNT_ID" == "52133938" ]; then
    TARGET_DIR="$MT5_ADMIN"
    INSTANCE_NAME="Legacy Admin MT5 (52133938)"
else
    # Create isolated dynamic instance directory for this VIP account
    TARGET_DIR="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_$ACCOUNT_ID"
    INSTANCE_NAME="VIP Client MT5 ($ACCOUNT_ID)"
    if [ ! -d "$TARGET_DIR" ]; then
        echo -e "${YELLOW}📦 Creating isolated directory for Account #$ACCOUNT_ID...${NC}"
        SOURCE_DIR="$MT5_PLATFORM"
        if [ ! -d "$SOURCE_DIR" ]; then
            SOURCE_DIR="$MT5_ADMIN"
        fi
        cp -r "$SOURCE_DIR" "$TARGET_DIR"
        rm -f "$TARGET_DIR/config/accounts.dat"
        chown -R "$TARGET_USER:$TARGET_USER" "$TARGET_DIR"
        chmod -R 775 "$TARGET_DIR"
        echo -e "${GREEN}✅ Cloned MetaTrader 5 from $SOURCE_DIR into $TARGET_DIR successfully!${NC}"
    fi
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Target MT5 directory not found at: $TARGET_DIR${NC}"
    exit 1
fi

# Normalize broker server names (GTC Cent is officially "GTCGlobalSA-Server5" without space in MT5)
CHART_SYMBOL="EURUSD"
if [[ "$SERVER" =~ [Ss]erver[[:space:]]*5 ]] || [[ "$SERVER" =~ "CENT" ]] || [[ "$SERVER" =~ "Cent" ]]; then
    SERVER="GTCGlobalSA-Server5"
    CHART_SYMBOL="EURUSDc"
elif [[ "$SERVER" =~ [Ss]erver[[:space:]]*2 ]]; then
    SERVER="GTCGlobalSA-Server 2"
    CHART_SYMBOL="EURUSD"
fi

echo -e "👤 Target User:     ${BOLD}${CYAN}$TARGET_USER${NC}"
echo -e "🎯 Target Instance: ${BOLD}${YELLOW}$INSTANCE_NAME${NC}"
echo -e "📁 Directory:       ${CYAN}$TARGET_DIR${NC}"
echo -e "🔑 Account ID:      ${GREEN}$ACCOUNT_ID${NC}"
echo -e "🌐 Server:          ${GREEN}$SERVER${NC}"
echo ""

# Auto-detect active X display:
# Priority 1: Extract working DISPLAY from any active MT5 terminal process
DETECTED_DISPLAY=""
RUNNING_PID=$(pgrep -f "terminal64.exe" 2>/dev/null | head -n 1 || true)
if [ -n "$RUNNING_PID" ] && [ -r "/proc/$RUNNING_PID/environ" ]; then
    FOUND_DISPLAY=$(strings "/proc/$RUNNING_PID/environ" 2>/dev/null | grep '^DISPLAY=' | head -n 1 | cut -d= -f2 || true)
    if [ -n "$FOUND_DISPLAY" ]; then
        DETECTED_DISPLAY="$FOUND_DISPLAY"
        echo -e "📡 Cloned active Display from running MT5 (PID $RUNNING_PID): ${GREEN}$DETECTED_DISPLAY${NC}"
    fi
fi

if [ -z "$DETECTED_DISPLAY" ]; then
    DETECTED_DISPLAY="${DISPLAY:-:10.0}"
    if [ -e /tmp/.X11-unix/X10 ]; then
        DETECTED_DISPLAY=":10.0"
    elif [ -e /tmp/.X11-unix/X11 ]; then
        DETECTED_DISPLAY=":11.0"
    elif [ -e /tmp/.X11-unix/X0 ]; then
        DETECTED_DISPLAY=":0.0"
    fi
fi

# Stage and sync EA into target Experts directory
WORKSPACE_DIR="/opt/khmer-master-crypto-bot"
BRIDGE_SRC="$WORKSPACE_DIR/KhmerMasterCrypto_Bridge.mq5"
if [ ! -f "$BRIDGE_SRC" ]; then
    BRIDGE_SRC="$(dirname "$0")/KhmerMasterCrypto_Bridge.mq5"
fi

mkdir -p "$TARGET_DIR/MQL5/Experts"
if [ -f "$BRIDGE_SRC" ]; then
    cp -f "$BRIDGE_SRC" "$TARGET_DIR/MQL5/Experts/KhmerMasterCrypto_Bridge.mq5"
fi

# Copy pre-compiled .ex5 from existing instances if available
for CANDIDATE in "$MT5_PLATFORM/MQL5/Experts/KhmerMasterCrypto_Bridge.ex5" "$MT5_ADMIN/MQL5/Experts/KhmerMasterCrypto_Bridge.ex5"; do
    if [ -f "$CANDIDATE" ]; then
        cp -f "$CANDIDATE" "$TARGET_DIR/MQL5/Experts/KhmerMasterCrypto_Bridge.ex5"
        break
    fi
done

# Compile EA if MetaEditor binary is present
EDITOR_BIN=$(find "$TARGET_DIR" -maxdepth 1 -iname "metaeditor*.exe" 2>/dev/null | head -n 1 || true)
if [ -n "$EDITOR_BIN" ]; then
    echo -e "${YELLOW}⚙️ Compiling KhmerMasterCrypto_Bridge.mq5 for Account #$ACCOUNT_ID...${NC}"
    DISPLAY="$DETECTED_DISPLAY" wine "$EDITOR_BIN" /compile:"MQL5/Experts/KhmerMasterCrypto_Bridge.mq5" /log:"MQL5/Experts/compile.log" 2>/dev/null || true
fi

# 1. Write startup.ini with credentials, auto-enable algo trading, and auto-attach EA to chart
cat << EOF > "$TARGET_DIR/startup.ini"
[Common]
Login=$ACCOUNT_ID
Password=$PASSWORD
Server=$SERVER
KeepPrivate=1

[StartUp]
Expert=KhmerMasterCrypto_Bridge
Symbol=$CHART_SYMBOL
Period=M15

[Experts]
AllowDllImport=1
Enabled=1
Account=1
Profile=Default

[Chart]
Symbol=$CHART_SYMBOL
Period=M15
Expert=KhmerMasterCrypto_Bridge
EOF

chown "$TARGET_USER:$TARGET_USER" "$TARGET_DIR/startup.ini"
chmod 600 "$TARGET_DIR/startup.ini"

mkdir -p "$TARGET_DIR/config"
cp -f "$TARGET_DIR/startup.ini" "$TARGET_DIR/config/startup.ini"
chown -R "$TARGET_USER:$TARGET_USER" "$TARGET_DIR"
chmod -R 775 "$TARGET_DIR"

# Stage Desktop Shortcut for Remote Desktop (XRDP)
DESKTOP_DIR="$TARGET_HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    cat << EOF > "$DESKTOP_DIR/Launch_MT5_$ACCOUNT_ID.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=▶️ Launch MT5 ($ACCOUNT_ID)
Comment=Launch MT5 Client $ACCOUNT_ID
Exec=bash -c "cd '$TARGET_DIR' && wine terminal64.exe /portable /config:startup.ini"
Icon=wine
Path=$TARGET_DIR
Terminal=false
StartupNotify=true
EOF
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/Launch_MT5_$ACCOUNT_ID.desktop"
    chmod +x "$DESKTOP_DIR/Launch_MT5_$ACCOUNT_ID.desktop"
fi

echo -e "${GREEN}✅ Successfully written credentials & fixed permissions for user $TARGET_USER!${NC}"

# 2. Restart target MT5 instance in Wine with /config:startup.ini
echo -e "${YELLOW}🔄 Restarting target MT5 instance to establish live connection (Display $DETECTED_DISPLAY)...${NC}"

# Safely kill ONLY the instance running in this specific directory
pkill -9 -f "$TARGET_DIR.*terminal64.exe" 2>/dev/null || true
pkill -9 -f "start.exe.*$ACCOUNT_ID" 2>/dev/null || true
sleep 2

LOG_FILE="$TARGET_DIR/launch.log"
sudo -u "$TARGET_USER" DISPLAY="$DETECTED_DISPLAY" bash -c "cd '$TARGET_DIR' && nohup wine terminal64.exe /portable /config:startup.ini > '$LOG_FILE' 2>&1 &"

sleep 4
if ps aux | grep -i "$TARGET_DIR.*terminal64.exe" | grep -v grep >/dev/null; then
    echo -e "${GREEN}🚀 $INSTANCE_NAME is RUNNING actively in Wine!${NC}"
    ps aux | grep -i "$TARGET_DIR.*terminal64.exe" | grep -v grep
else
    echo -e "${YELLOW}⚠️ Notice: Terminal process launched. Log output:${NC}"
    tail -n 15 "$LOG_FILE" 2>/dev/null || true
fi

echo ""
echo -e "${BOLD}${GREEN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}🎉 MT5 ACCOUNT LOGIN CONFIGURED SUCCESSFULLY!${NC}"
echo -e "${CYAN}👉 MT5 is now connecting to $SERVER with KhmerMasterCrypto_Bridge auto-attached...${NC}"
echo -e "${CYAN}👉 Verify live balance in Telegram via: /mt5${NC}"
echo -e "${BOLD}${GREEN}==============================================================================${NC}"
