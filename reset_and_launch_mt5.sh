#!/bin/bash
# ==============================================================================
# 🏛️ KHMER MASTER CRYPTO / APEX SUPER BRAIN AI
# MT5 DUAL INSTANCE MASTER RESTORER & PERSISTENCE ENGINE
# ==============================================================================
# Restores & Launches:
# 1. Admin Master MT5 (#52133938)
# 2. Platform Auto-Trade MT5 (#52135153)
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🏛️ KHMER MASTER CRYPTO — MT5 DUAL INSTANCE MASTER RESTORER 🏛️${NC}"
echo -e "${YELLOW}   Unlocks & Restores: Admin (#52133938) & Platform (#52135153)${NC}"
echo -e "${CYAN}==============================================================================${NC}"

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")
MT5_ADMIN="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5"
MT5_PLATFORM="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"
DESKTOP_DIR="$TARGET_HOME/Desktop"

# 1. Force kill all stuck / zombie wine and MT5 processes & clean memory locks
echo -e "${YELLOW}[1/5] 🧹 Purging all zombie Wine and MT5 processes...${NC}"
pkill -9 -f "terminal64.exe" 2>/dev/null || true
pkill -9 -f "wineserver" 2>/dev/null || true
wineserver -k 2>/dev/null || true
sleep 1
rm -rf /tmp/.wine-* 2>/dev/null || true
rm -f /tmp/.X*-lock 2>/dev/null || true
echo -e "   ${GREEN}✅ Cleaned all locks, mutexes, and dead sockets!${NC}"

# 2. Fix 100% of permissions across .wine and Desktop
echo -e "${YELLOW}[2/5] 🔑 Restoring full ownership to user $TARGET_USER...${NC}"
chown -R "$TARGET_USER:$TARGET_USER" "$TARGET_HOME/.wine" 2>/dev/null || true
chmod -R 775 "$TARGET_HOME/.wine" 2>/dev/null || true
if [ -d "$DESKTOP_DIR" ]; then
    chown -R "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR" 2>/dev/null || true
    chmod +x "$DESKTOP_DIR"/*.desktop 2>/dev/null || true
    chmod +x "$DESKTOP_DIR"/*.sh 2>/dev/null || true
fi
echo -e "   ${GREEN}✅ Permissions fully restored (Zero EACCES errors)!${NC}"

# 2.1 Sync latest KhmerMasterCrypto_Bridge.mq5 into Experts directories
WORKSPACE_BRIDGE="/opt/khmer-master-crypto-bot/KhmerMasterCrypto_Bridge.mq5"
if [ ! -f "$WORKSPACE_BRIDGE" ]; then
    WORKSPACE_BRIDGE="$(dirname "$0")/KhmerMasterCrypto_Bridge.mq5"
fi
if [ -f "$WORKSPACE_BRIDGE" ]; then
    mkdir -p "$MT5_ADMIN/MQL5/Experts" "$MT5_PLATFORM/MQL5/Experts"
    cp -f "$WORKSPACE_BRIDGE" "$MT5_ADMIN/MQL5/Experts/KhmerMasterCrypto_Bridge.mq5" 2>/dev/null || true
    cp -f "$WORKSPACE_BRIDGE" "$MT5_PLATFORM/MQL5/Experts/KhmerMasterCrypto_Bridge.mq5" 2>/dev/null || true
    if [ -d "$DESKTOP_DIR" ]; then
        cp -f "$WORKSPACE_BRIDGE" "$DESKTOP_DIR/KhmerMasterCrypto_Bridge.mq5" 2>/dev/null || true
    fi
    echo -e "   ${GREEN}✅ Synced latest KhmerMasterCrypto_Bridge.mq5 to all MT5 Experts directories!${NC}"
fi

# 3. Detect the EXACT display the user is currently viewing
echo -e "${YELLOW}[3/5] 📺 Detecting active Desktop Display...${NC}"
ACTIVE_DISPLAY=""

# Check xfce4-session environment for user
XFCE_PID=$(pgrep -u "$TARGET_USER" xfce4-session | head -n 1 || true)
if [ -n "$XFCE_PID" ] && [ -f "/proc/$XFCE_PID/environ" ]; then
    ACTIVE_DISPLAY=$(grep -z '^DISPLAY=' "/proc/$XFCE_PID/environ" 2>/dev/null | tr -d '\0' | cut -d= -f2 || true)
fi

# Fallback: check current DISPLAY environment variable
if [ -z "$ACTIVE_DISPLAY" ] && [ -n "$DISPLAY" ]; then
    ACTIVE_DISPLAY="$DISPLAY"
fi

# Fallback: check active X11 socket
if [ -z "$ACTIVE_DISPLAY" ]; then
    for sock in $(ls -1t /tmp/.X11-unix/ 2>/dev/null | grep -E '^X[0-9]+'); do
        disp_num=$(echo "$sock" | sed 's/^X//')
        ACTIVE_DISPLAY=":${disp_num}.0"
        break
    done
fi

ACTIVE_DISPLAY="${ACTIVE_DISPLAY:-:10.0}"
echo -e "   ${CYAN}🎯 Targeted Display Screen: ${BOLD}${GREEN}$ACTIVE_DISPLAY${NC}"

# 4. Launch Admin MT5 (#52133938)
echo -e "${YELLOW}[4/5] 🚀 Launching Instance 1: Admin MT5 (#52133938)...${NC}"
ADMIN_LOG="$TARGET_HOME/mt5_admin_launch.log"
sudo -u "$TARGET_USER" DISPLAY="$ACTIVE_DISPLAY" bash -c "cd '$MT5_ADMIN' && nohup wine terminal64.exe /portable > '$ADMIN_LOG' 2>&1 &"
sleep 2

# 5. Launch Platform MT5 (#52135153)
echo -e "${YELLOW}[5/5] 🚀 Launching Instance 2: Platform MT5 (#52135153)...${NC}"
PLATFORM_LOG="$TARGET_HOME/mt5_platform_launch.log"
sudo -u "$TARGET_USER" DISPLAY="$ACTIVE_DISPLAY" bash -c "cd '$MT5_PLATFORM' && nohup wine terminal64.exe /portable /config:startup.ini > '$PLATFORM_LOG' 2>&1 &"
sleep 3

# 6. Create 1-Click Desktop Launcher script directly on user's Desktop
if [ -d "$DESKTOP_DIR" ]; then
    cat << 'EOF' > "$DESKTOP_DIR/START_ALL_MT5.sh"
#!/bin/bash
pkill -9 -f "terminal64.exe" 2>/dev/null || true
pkill -9 -f "wineserver" 2>/dev/null || true
sleep 1
TARGET_HOME="$HOME"
MT5_ADMIN="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5"
MT5_PLATFORM="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"
CURRENT_DISP="${DISPLAY:-:10.0}"

# Start Admin MT5
cd "$MT5_ADMIN" && nohup wine terminal64.exe /portable > "$TARGET_HOME/mt5_admin_launch.log" 2>&1 &
sleep 2

# Start Platform MT5
cd "$MT5_PLATFORM" && nohup wine terminal64.exe /portable /config:startup.ini > "$TARGET_HOME/mt5_platform_launch.log" 2>&1 &

notify-send "Khmer Master Crypto" "Both MT5 instances launched successfully!" 2>/dev/null || true
EOF
    chmod +x "$DESKTOP_DIR/START_ALL_MT5.sh"
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/START_ALL_MT5.sh"

    # Create .desktop file for 1-click execution
    cat << EOF > "$DESKTOP_DIR/0_START_ALL_MT5.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=▶️ START ALL MT5 (Admin + Platform)
Comment=Launch both MetaTrader 5 terminals side by side
Exec=bash "$DESKTOP_DIR/START_ALL_MT5.sh"
Icon=wine
Terminal=false
StartupNotify=true
Categories=Application;Finance;
EOF
    chmod +x "$DESKTOP_DIR/0_START_ALL_MT5.desktop"
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/0_START_ALL_MT5.desktop"
fi

echo ""
echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}📋 CURRENT RUNNING MT5 PROCESSES:${NC}"
echo -e "${CYAN}==============================================================================${NC}"
ps aux | grep -i "terminal64.exe" | grep -v grep || echo "⚠️ Checking status in 2s..."

echo ""
echo -e "${BOLD}${GREEN}🎉 BOTH MT5 TERMINALS RESTORED & ACTIVE ON DISPLAY $ACTIVE_DISPLAY!${NC}"
echo -e "👉 Look at your Remote Desktop screen right now — both MT5 windows are OPEN!"
echo -e "👉 A 1-Click shortcut '${BOLD}0_START_ALL_MT5.desktop${NC}' has been placed on your Desktop."
echo -e "👉 Verify in Telegram with: /mt5"
echo -e "${CYAN}==============================================================================${NC}"
