#!/bin/bash
# ==============================================================================
# 🏛️ KHMER MASTER CRYPTO / APEX SUPER BRAIN AI
# DUAL-INSTANCE MT5 SETUP SCRIPT FOR GOOGLE CLOUD LINUX VPS (EQUINIX TOKYO TY3)
# ==============================================================================
# Instance 1: #52135153 (Super Admin Master MT5 Terminal 24/7)
# Instance 2: #52133938 (Legacy Admin / Secondary Terminal)
# Mode: Native Portable Isolation (/portable) via Wine on Ubuntu/Debian
# Memory Impact: ~120 MB RAM (Well within 16 GB RAM VPS limit)
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🏛️ KHMER MASTER CRYPTO — SUPER ADMIN MT5 CONFIGURATOR 🏛️${NC}"
echo -e "${YELLOW}   Super Admin MT5: #52135153 | Server: GTCGlobalSA-Server 2${NC}"
echo -e "${CYAN}==============================================================================${NC}"

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")
WORKSPACE_DIR="/opt/khmer-master-crypto-bot"
MT5_ORIGINAL="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5"
MT5_PLATFORM="$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform"
DESKTOP_DIR="$TARGET_HOME/Desktop"

if [ ! -d "$MT5_ORIGINAL" ]; then
    echo -e "${RED}❌ MetaTrader 5 base installation not found at: $MT5_ORIGINAL${NC}"
    echo -e "${YELLOW}👉 Please make sure MetaTrader 5 is installed first via install_mt5_linux_vps.sh${NC}"
    exit 1
fi

echo -e "👤 Target User: ${BOLD}${CYAN}$TARGET_USER${NC}"
echo -e "📁 MT5 Instance 1 (Admin):    ${CYAN}$MT5_ORIGINAL${NC}"
echo -e "📁 MT5 Instance 2 (Platform): ${CYAN}$MT5_PLATFORM${NC}"
echo ""

# 1. Duplicate MT5 base folder for Instance 2 (Platform Account 52135153)
if [ ! -d "$MT5_PLATFORM" ]; then
    echo -e "${YELLOW}📦 Creating isolated directory for Platform MT5 Instance...${NC}"
    cp -r "$MT5_ORIGINAL" "$MT5_PLATFORM"
    chown -R "$TARGET_USER:$TARGET_USER" "$MT5_PLATFORM"
    echo -e "${GREEN}✅ Cloned MetaTrader 5 into MetaTrader 5_Platform successfully!${NC}"
else
    echo -e "${GREEN}✅ Platform MT5 directory already exists at: $MT5_PLATFORM${NC}"
fi

# 2. Reset saved account data for Instance 2 so it does not auto-login to Admin account 52133938
rm -f "$MT5_PLATFORM/config/accounts.dat"
cat << EOF > "$MT5_PLATFORM/startup.ini"
[Common]
Login=52135153
Server=GTCGlobalSA-Server 2
EOF
chown -R "$TARGET_USER:$TARGET_USER" "$MT5_PLATFORM"
chmod -R 775 "$MT5_PLATFORM"
echo -e "${GREEN}✅ Configured startup.ini & fixed permissions for Platform Account #52135153!${NC}"

# 3. Stage KhmerMasterCrypto_Bridge.mq5 into Instance 2 Experts folder
BRIDGE_SRC="$WORKSPACE_DIR/KhmerMasterCrypto_Bridge.mq5"
if [ ! -f "$BRIDGE_SRC" ]; then
    BRIDGE_SRC="$(dirname "$0")/KhmerMasterCrypto_Bridge.mq5"
fi

PLATFORM_EXPERTS="$MT5_PLATFORM/MQL5/Experts"
mkdir -p "$PLATFORM_EXPERTS"
if [ -f "$BRIDGE_SRC" ]; then
    cp -f "$BRIDGE_SRC" "$PLATFORM_EXPERTS/KhmerMasterCrypto_Bridge.mq5"
    chown "$TARGET_USER:$TARGET_USER" "$PLATFORM_EXPERTS/KhmerMasterCrypto_Bridge.mq5"
    echo -e "${GREEN}✅ Staged KhmerMasterCrypto_Bridge.mq5 to Platform Experts directory!${NC}"
fi

# 4. Create Desktop Shortcuts for both instances (with strict working directory isolation)
if [ -d "$DESKTOP_DIR" ]; then
    # Shortcut 1: Super Admin MT5 (52135153)
    cat << EOF > "$DESKTOP_DIR/1_Launch_Super_Admin_MT5.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=1. Launch Super Admin MT5 (52135153)
Comment=Open Super Admin MetaTrader 5 Terminal 24/7
Path=$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform
Exec=bash -c 'cd "$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform" && wine terminal64.exe /portable /config:startup.ini'
Icon=wine
Terminal=false
StartupNotify=true
Categories=Application;Finance;
EOF
    chmod +x "$DESKTOP_DIR/1_Launch_Super_Admin_MT5.desktop"
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/1_Launch_Super_Admin_MT5.desktop"

    # Shortcut 2: Platform MT5 (52135153)
    cat << EOF > "$DESKTOP_DIR/2_Launch_MT5_Platform.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=2. Launch MT5 Platform (52135153)
Comment=Open Platform Auto-Trade MetaTrader 5 Terminal
Path=$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform
Exec=bash -c 'cd "$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform" && wine terminal64.exe /portable /config:startup.ini'
Icon=wine
Terminal=false
StartupNotify=true
Categories=Application;Finance;
EOF
    chmod +x "$DESKTOP_DIR/2_Launch_MT5_Platform.desktop"
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/2_Launch_MT5_Platform.desktop"
    echo -e "${GREEN}✅ Created isolated Desktop Shortcuts for Super Admin MT5 (#52135153)!${NC}"
fi

# 5. Install Global CLI Commands
cat << EOF > /usr/local/bin/mt5-dual-start
#!/bin/bash
TARGET_USER="$TARGET_USER"
TARGET_HOME="$TARGET_HOME"
echo "🚀 Starting Dual MT5 Terminals in Portable Mode under user \$TARGET_USER..."
# Launch Instance 1: Admin
sudo -u "\$TARGET_USER" DISPLAY=:10.0 bash -c "cd '\$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5' && nohup wine terminal64.exe /portable >/dev/null 2>&1 &"
sleep 2
# Launch Instance 2: Platform
sudo -u "\$TARGET_USER" DISPLAY=:10.0 bash -c "cd '\$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform' && nohup wine terminal64.exe /portable /config:startup.ini >/dev/null 2>&1 &"
echo "✅ Both MT5 Terminals (Admin 52133938 + Platform 52135153) launched in background!"
EOF
chmod +x /usr/local/bin/mt5-dual-start

cat << EOF > /usr/local/bin/mt5-admin-start
#!/bin/bash
TARGET_USER="$TARGET_USER"
TARGET_HOME="$TARGET_HOME"
echo "🚀 Starting Super Admin MT5 Terminal (52135153)..."
sudo -u "\$TARGET_USER" DISPLAY=:10.0 bash -c "cd '\$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform' && nohup wine terminal64.exe /portable /config:startup.ini >/dev/null 2>&1 &"
echo "✅ Super Admin MT5 Terminal (52135153) launched in background."
EOF
chmod +x /usr/local/bin/mt5-admin-start

cat << EOF > /usr/local/bin/mt5-platform-start
#!/bin/bash
TARGET_USER="$TARGET_USER"
TARGET_HOME="$TARGET_HOME"
echo "🚀 Restarting Platform MT5 Terminal (52135153)..."
pkill -9 -f "MetaTrader 5_Platform.*terminal64.exe" 2>/dev/null || true
sleep 2
sudo -u "\$TARGET_USER" DISPLAY=:10.0 bash -c "cd '\$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform' && nohup wine terminal64.exe /portable /config:startup.ini >/dev/null 2>&1 &"
echo "✅ Platform MT5 Terminal launched in background."
EOF
chmod +x /usr/local/bin/mt5-platform-start

echo ""
echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}🎉 DUAL MT5 SETUP COMPLETED SUCCESSFULLY!${NC}"
echo -e "${CYAN}==============================================================================${NC}"
echo -e "👉 ${BOLD}Next Simple Steps:${NC}"
echo -e "1. Open XRDP Remote Desktop (mstsc)."
echo -e "2. Double click ${BOLD}'2. Launch MT5 Platform (52135153)'${NC} on Desktop."
echo -e "3. Login with account: ${BOLD}52135153${NC}, Server: ${BOLD}GTCGlobalSA-Server 2${NC}."
echo -e "4. Attach ${BOLD}KhmerMasterCrypto_Bridge.mq5${NC} to any chart with Port 5555."
echo -e "5. Both terminals will now run 24/7 side by side with zero interference!"
echo -e "${CYAN}==============================================================================${NC}"
