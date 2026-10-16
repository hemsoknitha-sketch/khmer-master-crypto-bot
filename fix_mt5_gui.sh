#!/bin/bash
# ==============================================================================
# 🏛️ KHMER MASTER CRYPTO / APEX SUPER BRAIN AI
# MT5 REMOTE DESKTOP & PERMISSION AUTO-HEALER (24/7 PERSISTENCE)
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🏛️ KHMER MASTER CRYPTO — SUPER ADMIN MT5 AUTO-HEALER 🏛️${NC}"
echo -e "${YELLOW}   Fixes 24/7 Background Persistence & Restores Super Admin Account #52135153${NC}"
echo -e "${CYAN}==============================================================================${NC}"

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")
MT5_PLATFORM="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"
MT5_ADMIN="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5"
DESKTOP_DIR="$TARGET_HOME/Desktop"

# 1. Clean up any stuck / zombie Wine or terminal processes for Platform
echo -e "${YELLOW}[1/4] 🧹 Clearing lingering locks for Platform MT5...${NC}"
pkill -9 -f "MetaTrader 5_Platform.*terminal64.exe" 2>/dev/null || true
sleep 1

# 2. Fix Recursive Ownership & Permissions (Prevents Permission Denied crash in config/)
echo -e "${YELLOW}[2/4] 🔑 Fixing recursive file permissions for user $TARGET_USER...${NC}"
chown -R "$TARGET_USER:$TARGET_USER" "$MT5_PLATFORM" 2>/dev/null || true
chmod -R 775 "$MT5_PLATFORM" 2>/dev/null || true
if [ -d "$DESKTOP_DIR" ]; then
    chown -R "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR" 2>/dev/null || true
    chmod +x "$DESKTOP_DIR"/*.desktop 2>/dev/null || true
fi

# 3. Configure XRDP Sesman to NEVER kill sessions when Remote Desktop is closed!
echo -e "${YELLOW}[3/4] 🛡️ Configuring XRDP 24/7 Persistence (KillDisconnected=false)...${NC}"
if [ -f /etc/xrdp/sesman.ini ]; then
    sed -i 's/^KillDisconnected=.*/KillDisconnected=false/' /etc/xrdp/sesman.ini 2>/dev/null || true
    sed -i 's/^DisconnectedTimeLimit=.*/DisconnectedTimeLimit=0/' /etc/xrdp/sesman.ini 2>/dev/null || true
    sed -i 's/^IdleTimeLimit=.*/IdleTimeLimit=0/' /etc/xrdp/sesman.ini 2>/dev/null || true
    echo -e "   ${GREEN}✅ XRDP is configured to keep all desktop sessions running 24/7!${NC}"
fi

# 4. Auto-detect active X Display
DETECTED_DISPLAY="${DISPLAY}"
if [ -z "$DETECTED_DISPLAY" ]; then
    if [ -e /tmp/.X11-unix/X10 ]; then
        DETECTED_DISPLAY=":10.0"
    elif [ -e /tmp/.X11-unix/X11 ]; then
        DETECTED_DISPLAY=":11.0"
    elif [ -e /tmp/.X11-unix/X0 ]; then
        DETECTED_DISPLAY=":0.0"
    else
        DETECTED_DISPLAY=":10.0"
    fi
fi

echo -e "${YELLOW}[4/4] 🚀 Launching Super Admin MT5 (Account #52135153) on Display $DETECTED_DISPLAY...${NC}"
LOG_FILE="$TARGET_HOME/mt5_platform_launch.log"

sudo -u "$TARGET_USER" DISPLAY="$DETECTED_DISPLAY" bash -c "cd '$MT5_PLATFORM' && nohup wine terminal64.exe /portable /config:startup.ini > '$LOG_FILE' 2>&1 &"

sleep 3
if ps aux | grep -i "MetaTrader 5_Platform.*terminal64.exe" | grep -v grep >/dev/null; then
    echo ""
    echo -e "${BOLD}${GREEN}🎉 SUCCESS! Super Admin MT5 (#52135153) is now RUNNING actively in Wine!${NC}"
    ps aux | grep -i "MetaTrader 5_Platform.*terminal64.exe" | grep -v grep
    echo ""
    echo -e "${CYAN}👉 You can now safely close Remote Desktop anytime — MT5 will STAY RUNNING 24/7!${NC}"
    echo -e "${CYAN}👉 Verify in Telegram with: /mt5${NC}"
else
    echo -e "${RED}⚠️ Could not verify process in 3 seconds. Diagnostic log:${NC}"
    echo "------------------------------------------------------------------"
    tail -n 20 "$LOG_FILE" 2>/dev/null || true
    echo "------------------------------------------------------------------"
    echo -e "${YELLOW}👉 If Remote Desktop is not currently open, please open XRDP (mstsc) and double-click:${NC}"
    echo -e "${BOLD}   '1. Launch Super Admin MT5 (52135153)' on the Desktop!${NC}"
fi

echo -e "${CYAN}==============================================================================${NC}"
