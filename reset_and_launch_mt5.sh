#!/bin/bash
# ==============================================================================
# ANGKOR QUANT / APEX SUPER BRAIN AI
# GTC PAMM SINGLE MASTER RESTORER & DISK HYGIENE ENGINE (INVARIANT 105)
# ==============================================================================
# Restores & Launches:
#   Super Admin Master PAMM MT5 (#52171861 on GTCGlobalSA-Server 2)
# Fiduciary Principle:
#   Eliminates all other account EAs and duplicate folders to maximize free VPS disk space.
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🛡️ ANGKOR QUANT — GTC PAMM MASTER RESTORER & DISK HYGIENE 🛡️${NC}"
echo -e "${YELLOW}   Unlocks & Restores: Super Admin PAMM MT5 (#52171861)${NC}"
echo -e "${CYAN}==============================================================================${NC}"

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")
WINE_PROGRAMS="$TARGET_HOME/.wine/drive_c/Program Files"
MT5_PLATFORM="$WINE_PROGRAMS/MetaTrader 5_Platform"
MT5_ORIGINAL="$WINE_PROGRAMS/MetaTrader 5"
DESKTOP_DIR="$TARGET_HOME/Desktop"

# 1. Force kill all stuck / zombie wine and MT5 processes & clean memory locks
echo -e "${YELLOW}[1/5] 🛑 Purging all zombie Wine and MT5 processes...${NC}"
pkill -9 -f "terminal64.exe" 2>/dev/null || true
pkill -9 -f "metaeditor" 2>/dev/null || true
pkill -9 -f "wine" 2>/dev/null || true
pkill -9 -f "wineserver" 2>/dev/null || true
wineserver -k 2>/dev/null || true
sleep 1
rm -rf /tmp/.wine-* 2>/dev/null || true
rm -f /tmp/.X*-lock 2>/dev/null || true
echo -e "   ${GREEN}✅ Cleaned all locks, mutexes, and dead sockets!${NC}"

# 2. Prune non-PAMM MT5 account instances & consolidate base folders to save disk space
echo -e "${YELLOW}[2/5] 🧹 Purging non-PAMM account instances & consolidating folders...${NC}"
if [ -d "$MT5_PLATFORM" ] && [ -d "$MT5_ORIGINAL" ]; then
    rm -rf "$MT5_ORIGINAL"
elif [ ! -d "$MT5_PLATFORM" ] && [ -d "$MT5_ORIGINAL" ]; then
    mv "$MT5_ORIGINAL" "$MT5_PLATFORM"
fi

PRIMARY_MT5="$MT5_PLATFORM"
if [ ! -d "$PRIMARY_MT5" ]; then
    echo -e "${RED}❌ MetaTrader 5 base installation not found at: $PRIMARY_MT5${NC}"
    exit 1
fi

for DIR in "$WINE_PROGRAMS/MetaTrader 5_"*; do
    if [ -d "$DIR" ] && [ "$DIR" != "$PRIMARY_MT5" ]; then
        echo -e "   ${RED}🗑️ Removed non-PAMM clone: $(basename "$DIR")${NC}"
        rm -rf "$DIR"
    fi
done

# Deep-clean crash dumps, logs, and temp files to maximize free disk
find "$PRIMARY_MT5" -name "*.dmp" -type f -delete 2>/dev/null || true
find "$PRIMARY_MT5" -name "compile.log" -type f -delete 2>/dev/null || true
find "$PRIMARY_MT5" -path "*/Logs/*" -name "*.log" -type f -delete 2>/dev/null || true
find "$PRIMARY_MT5" -path "*/logs/*" -name "*.log" -type f -delete 2>/dev/null || true
rm -rf "$TARGET_HOME/.wine/drive_c/users"/*/AppData/Local/Temp/* 2>/dev/null || true
echo -e "   ${GREEN}✅ VPS disk cleaned & sanitized!${NC}"

# Fix ownership and permissions
chown -R "$TARGET_USER:$TARGET_USER" "$TARGET_HOME/.wine" 2>/dev/null || true
chmod -R 775 "$PRIMARY_MT5" 2>/dev/null || true

# 3. Sync latest KhmerMasterCrypto_Bridge.mq5 and .ex5 into Master Experts directory
echo -e "${YELLOW}[3/5] 🔄 Syncing latest KhmerMasterCrypto_Bridge.mq5 into Master PAMM Experts...${NC}"
WORKSPACE_BRIDGE="/opt/khmer-master-crypto-bot/KhmerMasterCrypto_Bridge.mq5"
WORKSPACE_BRIDGE_EX5="/opt/khmer-master-crypto-bot/KhmerMasterCrypto_Bridge.ex5"
if [ ! -f "$WORKSPACE_BRIDGE" ]; then
    WORKSPACE_BRIDGE="$(dirname "$0")/KhmerMasterCrypto_Bridge.mq5"
    WORKSPACE_BRIDGE_EX5="$(dirname "$0")/KhmerMasterCrypto_Bridge.ex5"
fi

mkdir -p "$PRIMARY_MT5/MQL5/Experts"
if [ -f "$WORKSPACE_BRIDGE" ]; then
    cp -f "$WORKSPACE_BRIDGE" "$PRIMARY_MT5/MQL5/Experts/KhmerMasterCrypto_Bridge.mq5" 2>/dev/null || true
fi
if [ -f "$WORKSPACE_BRIDGE_EX5" ]; then
    cp -f "$WORKSPACE_BRIDGE_EX5" "$PRIMARY_MT5/MQL5/Experts/KhmerMasterCrypto_Bridge.ex5" 2>/dev/null || true
fi

# 4. Configure startup.ini for Master PAMM Account #52171861
echo -e "${YELLOW}[4/5] ⚙️ Configuring Master PAMM startup.ini...${NC}"
cat << 'EOF' > "$PRIMARY_MT5/startup.ini"
[Common]
Login=52171861
Server=GTCGlobalSA-Server 2

[StartUp]
Expert=KhmerMasterCrypto_Bridge
Symbol=XAUUSD
Period=M15

[Experts]
AllowDllImport=1
Enabled=1
Account=1
Profile=Default
WebRequest=1
WebRequestUrl=http://127.0.0.1;http://127.0.0.1:5555;http://localhost;127.0.0.1;127.0.0.1:5555

[Chart]
Symbol=XAUUSD
Period=M15
Expert=KhmerMasterCrypto_Bridge
EOF

mkdir -p "$PRIMARY_MT5/config"
cp -f "$PRIMARY_MT5/startup.ini" "$PRIMARY_MT5/config/startup.ini"
chown -R "$TARGET_USER:$TARGET_USER" "$PRIMARY_MT5"

# Auto-detect active Desktop Display
ACTIVE_DISPLAY=""
XFCE_PID=$(pgrep -u "$TARGET_USER" xfce4-session | head -n 1 || true)
if [ -n "$XFCE_PID" ] && [ -f "/proc/$XFCE_PID/environ" ]; then
    ACTIVE_DISPLAY=$(grep -z '^DISPLAY=' "/proc/$XFCE_PID/environ" 2>/dev/null | tr -d '\0' | cut -d= -f2 || true)
fi
if [ -z "$ACTIVE_DISPLAY" ]; then
    ACTIVE_DISPLAY="${DISPLAY:-:10.0}"
    if [ -e /tmp/.X11-unix/X10 ]; then
        ACTIVE_DISPLAY=":10.0"
    elif [ -e /tmp/.X11-unix/X11 ]; then
        ACTIVE_DISPLAY=":11.0"
    elif [ -e /tmp/.X11-unix/X0 ]; then
        ACTIVE_DISPLAY=":0.0"
    fi
fi

# 5. Launch Super Admin PAMM MT5 (#52171861)
echo -e "${YELLOW}[5/5] 🚀 Launching GTC PAMM Master MT5 (#52171861) on Display $ACTIVE_DISPLAY...${NC}"
PLATFORM_LOG="$TARGET_HOME/mt5_platform_launch.log"
sudo -u "$TARGET_USER" DISPLAY="$ACTIVE_DISPLAY" bash -c "cd '$PRIMARY_MT5' && nohup wine terminal64.exe /portable /config:startup.ini > '$PLATFORM_LOG' 2>&1 &"
sleep 3

# Setup 1-Click Desktop Launcher
if [ -d "$DESKTOP_DIR" ]; then
    rm -f "$DESKTOP_DIR"/Launch_MT5_*.desktop 2>/dev/null || true
    rm -f "$DESKTOP_DIR"/START_ALL_MT5.sh 2>/dev/null || true
    rm -f "$DESKTOP_DIR"/0_START_ALL_MT5.desktop 2>/dev/null || true

    cat << 'EOF' > "$DESKTOP_DIR/START_GTC_PAMM_MT5.sh"
#!/bin/bash
pkill -9 -f "terminal64.exe" 2>/dev/null || true
pkill -9 -f "wineserver" 2>/dev/null || true
sleep 1
TARGET_HOME="$HOME"
PRIMARY_MT5="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"
CURRENT_DISP="${DISPLAY:-:10.0}"
cd "$PRIMARY_MT5" && nohup wine terminal64.exe /portable /config:startup.ini > "$TARGET_HOME/mt5_platform_launch.log" 2>&1 &
notify-send "Angkor Quant" "GTC PAMM Master MT5 (#52171861) launched successfully!" 2>/dev/null || true
EOF
    chmod +x "$DESKTOP_DIR/START_GTC_PAMM_MT5.sh"
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/START_GTC_PAMM_MT5.sh"

    cat << EOF > "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=🛡️ START GTC PAMM MT5 (#52171861)
Comment=Launch Super Admin PAMM MetaTrader 5 Terminal 24/7
Exec=bash "$DESKTOP_DIR/START_GTC_PAMM_MT5.sh"
Icon=wine
Terminal=false
StartupNotify=true
Categories=Application;Finance;
EOF
    chmod +x "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
fi

# Auto-restart python bot service so Linux Brain & MT5 are in sync
sudo systemctl restart khmer-master-crypto-bot 2>/dev/null || true

echo ""
echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}✅ GTC PAMM MASTER MT5 RESTORED & ACTIVE ON DISPLAY $ACTIVE_DISPLAY!${NC}"
echo -e "${CYAN}• Single PAMM Terminal #52171861 active with KhmerMasterCrypto_Bridge.${NC}"
echo -e "${CYAN}• All non-PAMM EAs, duplicate folders, and bloated logs permanently purged.${NC}"
echo -e "${CYAN}• 1-Click Desktop Launcher: '0_START_GTC_PAMM_MT5.desktop'.${NC}"
echo -e "${CYAN}• Verify live telemetry in Telegram: /mt5${NC}"
echo -e "${CYAN}==============================================================================${NC}"
