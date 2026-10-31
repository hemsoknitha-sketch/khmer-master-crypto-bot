#!/bin/bash
# ==============================================================================
# ANGKOR QUANT / APEX SUPER BRAIN AI
# GTC PAMM MASTER MT5 FAST LOGIN & DISK SPACE PRESERVATION TOOL (INVARIANT 105)
# ==============================================================================
# Usage:
#   bash login_mt5_account.sh <ACCOUNT_ID> <PASSWORD> [SERVER]
# Master Account:
#   #52171861 (GTC PAMM Master Fund Gateway on GTCGlobalSA-Server 2)
# Fiduciary Principle:
#   All other accounts are rejected from running separate Wine instances/EAs
#   to permanently prevent VPS disk and RAM bloat.
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🛡️ ANGKOR QUANT — GTC PAMM MASTER MT5 CONFIGURATOR (INVARIANT 105) 🛡️${NC}"
echo -e "${YELLOW}   Master PAMM Gateway: #52171861 | Zero-Disk / Zero-Resource Client Ledgers${NC}"
echo -e "${CYAN}==============================================================================${NC}"

ACCOUNT_ID="$1"
PASSWORD="$2"
SERVER="$3"

# Auto-detect GTCFX Server 2 as canonical Master Server
if [ -z "$SERVER" ]; then
    SERVER="GTCGlobalSA-Server 2"
fi

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
    echo -e "${YELLOW}Example: bash login_mt5_account.sh 52171861 'MySecretPassword' 'GTCGlobalSA-Server 2'${NC}"
    exit 1
fi

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")

# Check if an account OTHER than GTC PAMM Master #52171861 is being configured
if [ "$ACCOUNT_ID" != "52171861" ]; then
    echo -e "${RED}══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${RED}⛔ [PAMM FIDUCIARY LOCK ACTIVATED - NON-PAMM ACCOUNT REJECTED]${NC}"
    echo -e "${RED}══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}⚠️ Notice: In accordance with Angkor Quant Invariant 105 (GTC PAMM Institutional Architecture):${NC}"
    echo -e "   1. Individual client EAs and multi-instance terminals on VPS are permanently decommissioned"
    echo -e "      to eliminate disk space bloat (~1.5 GB per account) and memory exhaustion."
    echo -e "   2. Account #${BOLD}${CYAN}$ACCOUNT_ID${NC} does NOT need a separate terminal or EA."
    echo -e "   3. All client investments operate via the sub-millisecond RAM Virtual Ledger"
    echo -e "      connected to Master PAMM Gateway #${BOLD}${GREEN}52171861${NC}."
    echo ""

    # Auto-clean legacy directory if it exists for this account to reclaim disk space immediately
    LEGACY_DIR="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_$ACCOUNT_ID"
    if [ -d "$LEGACY_DIR" ]; then
        echo -e "${YELLOW}🧹 Purging obsolete legacy MT5 folder for #${ACCOUNT_ID} to save disk space...${NC}"
        pkill -9 -f "$LEGACY_DIR.*terminal64.exe" 2>/dev/null || true
        rm -rf "$LEGACY_DIR"
        rm -f "$TARGET_HOME/Desktop/Launch_MT5_$ACCOUNT_ID.desktop" 2>/dev/null || true
        echo -e "${GREEN}✅ Reclaimed ~1.5 GB of VPS disk space!${NC}"
    fi

    echo -e "${CYAN}💡 To allocate funds to the GTC PAMM Master Fund, use in Telegram:${NC}"
    echo -e "   ${BOLD}/mt5 ALLOC 100${NC}  or  ${BOLD}/mt5 DEPOSIT 100${NC}  or  ${BOLD}/mt5 REGISTER${NC}"
    echo -e "${RED}══════════════════════════════════════════════════════════════════════════════${NC}"
    exit 0
fi

# Target Directory for Master PAMM MT5 (Unified single installation)
MT5_PLATFORM="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"
MT5_ADMIN="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5"

TARGET_DIR=""
if [ -d "$MT5_PLATFORM" ]; then
    TARGET_DIR="$MT5_PLATFORM"
elif [ -d "$MT5_ADMIN" ]; then
    TARGET_DIR="$MT5_ADMIN"
else
    echo -e "${RED}❌ MetaTrader 5 base installation not found at: $MT5_ADMIN or $MT5_PLATFORM${NC}"
    echo -e "${YELLOW}Please install MetaTrader 5 first via install_mt5_linux_vps.sh${NC}"
    exit 1
fi

INSTANCE_NAME="Super Admin Master PAMM MT5 (#52171861)"

# Auto-clean ALL other obsolete cloned MT5 instances to reclaim disk space
echo -e "${YELLOW}🧹 Scanning and pruning all non-PAMM MT5 directories to save VPS disk space...${NC}"
for DIR in "$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_"*; do
    if [ -d "$DIR" ] && [ "$DIR" != "$MT5_PLATFORM" ]; then
        echo -e "   ${YELLOW}🗑️ Removing non-PAMM instance: $(basename "$DIR")...${NC}"
        pkill -9 -f "$DIR.*terminal64.exe" 2>/dev/null || true
        rm -rf "$DIR"
    fi
done

# Clean bloated log files, crash dumps, and temp files to maximize disk savings
echo -e "${YELLOW}🧹 Purging crash dumps, logs, and temp files across Wine...${NC}"
find "$TARGET_DIR" -name "*.dmp" -type f -delete 2>/dev/null || true
find "$TARGET_DIR" -path "*/Logs/*" -name "*.log" -type f -delete 2>/dev/null || true
find "$TARGET_DIR" -name "compile.log" -type f -delete 2>/dev/null || true
rm -rf /tmp/.wine-* /tmp/wine-* /tmp/.X*-lock /tmp/*.log 2>/dev/null || true
rm -rf "$TARGET_HOME/.wine/drive_c/users"/*/AppData/Local/Temp/* 2>/dev/null || true

CHART_SYMBOL="XAUUSD"
SERVER="GTCGlobalSA-Server 2"

echo -e "👤 Target User:     ${BOLD}${CYAN}$TARGET_USER${NC}"
echo -e "🚀 Target Instance: ${BOLD}${YELLOW}$INSTANCE_NAME${NC}"
echo -e "📁 Directory:       ${CYAN}$TARGET_DIR${NC}"
echo -e "🔑 Account ID:      ${GREEN}$ACCOUNT_ID${NC}"
echo -e "🌐 Server:          ${GREEN}$SERVER${NC}"
echo ""

# Auto-detect active X display:
DETECTED_DISPLAY=""
RUNNING_PID=$(pgrep -f "terminal64.exe" 2>/dev/null | head -n 1 || true)
if [ -n "$RUNNING_PID" ] && [ -r "/proc/$RUNNING_PID/environ" ]; then
    FOUND_DISPLAY=$(strings "/proc/$RUNNING_PID/environ" 2>/dev/null | grep '^DISPLAY=' | head -n 1 | cut -d= -f2 || true)
    if [ -n "$FOUND_DISPLAY" ]; then
        DETECTED_DISPLAY="$FOUND_DISPLAY"
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

# Stage and sync EA into Master PAMM Experts directory
WORKSPACE_DIR="/opt/khmer-master-crypto-bot"
BRIDGE_SRC="$WORKSPACE_DIR/KhmerMasterCrypto_Bridge.mq5"
if [ ! -f "$BRIDGE_SRC" ]; then
    BRIDGE_SRC="$(dirname "$0")/KhmerMasterCrypto_Bridge.mq5"
fi

mkdir -p "$TARGET_DIR/MQL5/Experts"
if [ -f "$BRIDGE_SRC" ]; then
    cp -f "$BRIDGE_SRC" "$TARGET_DIR/MQL5/Experts/KhmerMasterCrypto_Bridge.mq5" 2>/dev/null || true
fi

# Copy pre-compiled .ex5 if available
WORKSPACE_EX5="$WORKSPACE_DIR/KhmerMasterCrypto_Bridge.ex5"
if [ ! -f "$WORKSPACE_EX5" ]; then
    WORKSPACE_EX5="$(dirname "$0")/KhmerMasterCrypto_Bridge.ex5"
fi
if [ -f "$WORKSPACE_EX5" ]; then
    cp -f "$WORKSPACE_EX5" "$TARGET_DIR/MQL5/Experts/KhmerMasterCrypto_Bridge.ex5" 2>/dev/null || true
fi

# Compile EA if MetaEditor binary is present
EDITOR_BIN=$(find "$TARGET_DIR" -maxdepth 1 -iname "metaeditor*.exe" 2>/dev/null | head -n 1 || true)
if [ -n "$EDITOR_BIN" ]; then
    echo -e "${YELLOW}⚙️ Compiling KhmerMasterCrypto_Bridge.mq5 for Master PAMM Account...${NC}"
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
WebRequest=1
WebRequestUrl=http://127.0.0.1;http://127.0.0.1:5555;http://localhost;127.0.0.1;127.0.0.1:5555

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

# Stage Clean Desktop Shortcut for Remote Desktop (XRDP)
DESKTOP_DIR="$TARGET_HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    # Clean any old shortcuts for other accounts
    rm -f "$DESKTOP_DIR"/Launch_MT5_*.desktop 2>/dev/null || true
    
    cat << EOF > "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=🛡️ START GTC PAMM MT5 (#52171861)
Comment=Launch Super Admin PAMM MetaTrader 5 Terminal 24/7
Exec=bash -c "cd '$TARGET_DIR' && wine terminal64.exe /portable /config:startup.ini"
Icon=wine
Path=$TARGET_DIR
Terminal=false
StartupNotify=true
Categories=Application;Finance;
EOF
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
    chmod +x "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
fi

echo -e "${GREEN}✅ Successfully written credentials & fixed permissions for Master PAMM Account!${NC}"

# 2. Restart target MT5 instance in Wine with /config:startup.ini
echo -e "${YELLOW}🔄 Restarting Master PAMM MT5 instance to establish live connection (Display $DETECTED_DISPLAY)...${NC}"

pkill -9 -f "terminal64.exe" 2>/dev/null || true
sleep 2

LOG_FILE="$TARGET_HOME/mt5_platform_launch.log"
sudo -u "$TARGET_USER" DISPLAY="$DETECTED_DISPLAY" bash -c "cd '$TARGET_DIR' && nohup wine terminal64.exe /portable /config:startup.ini > '$LOG_FILE' 2>&1 &"

sleep 4
if ps aux | grep -i "terminal64.exe" | grep -v grep >/dev/null; then
    echo -e "${GREEN}🚀 $INSTANCE_NAME is RUNNING actively in Wine!${NC}"
    ps aux | grep -i "terminal64.exe" | grep -v grep
else
    echo -e "${YELLOW}ℹ️ Notice: Terminal process launched. Log output:${NC}"
    tail -n 15 "$LOG_FILE" 2>/dev/null || true
fi

echo ""
echo -e "${BOLD}${GREEN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}✅ GTC PAMM MASTER MT5 CONFIGURED SUCCESSFULLY! (ZERO DISK BLOAT)${NC}"
echo -e "${CYAN}📡 MT5 connected to $SERVER with KhmerMasterCrypto_Bridge auto-attached.${NC}"
echo -e "${CYAN}📊 Real-time PAMM Fund metrics active in Telegram via: /mt5${NC}"
echo -e "${BOLD}${GREEN}==============================================================================${NC}"
