#!/bin/bash
# ==============================================================================
# ANGKOR QUANT / APEX SUPER BRAIN AI
# SINGLE MASTER GTC PAMM MT5 SETUP SCRIPT FOR LINUX VPS (INVARIANT 105)
# ==============================================================================
# Master Account: #52171861 (GTC PAMM Master Gateway on GTCGlobalSA-Server 2)
# Architecture: Single Consolidated Terminal | Zero-Disk / Zero-Resource Client Ledgers
# Memory & Disk Impact: Clamped to single instance (~1.2 GB disk, ~120 MB RAM)
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🛡️ ANGKOR QUANT — GTC PAMM SINGLE MASTER MT5 SETUP 🛡️${NC}"
echo -e "${YELLOW}   Configuring Master PAMM Terminal #52171861 (Zero Disk Bloat)${NC}"
echo -e "${CYAN}==============================================================================${NC}"

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")
WORKSPACE_DIR="/opt/khmer-master-crypto-bot"
WINE_PROGRAMS="$TARGET_HOME/.wine/drive_c/Program Files"
MT5_ORIGINAL="$WINE_PROGRAMS/MetaTrader 5"
MT5_PLATFORM="$WINE_PROGRAMS/MetaTrader 5_Platform"
DESKTOP_DIR="$TARGET_HOME/Desktop"

# 1. Consolidate to single master directory without duplicating 1.5 GB
if [ -d "$MT5_PLATFORM" ] && [ -d "$MT5_ORIGINAL" ]; then
    echo -e "${YELLOW}ℹ️ Both MetaTrader 5 and MetaTrader 5_Platform found.${NC}"
    echo -e "${YELLOW}🧹 Removing redundant base folder to reclaim ~1.5 GB disk space...${NC}"
    rm -rf "$MT5_ORIGINAL"
    echo -e "${GREEN}✅ Reclaimed ~1.5 GB! Using MetaTrader 5_Platform as single master.${NC}"
elif [ ! -d "$MT5_PLATFORM" ] && [ -d "$MT5_ORIGINAL" ]; then
    echo -e "${CYAN}Renaming MetaTrader 5 to MetaTrader 5_Platform for canonical consistency...${NC}"
    mv "$MT5_ORIGINAL" "$MT5_PLATFORM"
elif [ ! -d "$MT5_PLATFORM" ]; then
    echo -e "${RED}❌ MetaTrader 5 base installation not found at: $MT5_PLATFORM${NC}"
    echo -e "${YELLOW}Please install MetaTrader 5 first via install_mt5_linux_vps.sh${NC}"
    exit 1
fi

# 2. Prune all other cloned account directories to save disk space
echo -e "${YELLOW}🧹 Pruning all non-PAMM account instances...${NC}"
for DIR in "$WINE_PROGRAMS/MetaTrader 5_"*; do
    if [ -d "$DIR" ] && [ "$DIR" != "$MT5_PLATFORM" ]; then
        echo -e "   ${RED}🗑️ Purging non-PAMM directory: $(basename "$DIR")...${NC}"
        pkill -9 -f "$DIR.*terminal64.exe" 2>/dev/null || true
        rm -rf "$DIR"
    fi
done

# 3. Configure startup.ini for Master PAMM Account #52171861
rm -f "$MT5_PLATFORM/config/accounts.dat"
cat << EOF > "$MT5_PLATFORM/startup.ini"
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

mkdir -p "$MT5_PLATFORM/config"
cp -f "$MT5_PLATFORM/startup.ini" "$MT5_PLATFORM/config/startup.ini"
chown -R "$TARGET_USER:$TARGET_USER" "$MT5_PLATFORM"
chmod -R 775 "$MT5_PLATFORM"
echo -e "${GREEN}✅ Configured startup.ini & fixed permissions for Master PAMM #52171861!${NC}"

# 4. Stage KhmerMasterCrypto_Bridge.mq5 into Experts folder
BRIDGE_SRC="$WORKSPACE_DIR/KhmerMasterCrypto_Bridge.mq5"
if [ ! -f "$BRIDGE_SRC" ]; then
    BRIDGE_SRC="$(dirname "$0")/KhmerMasterCrypto_Bridge.mq5"
fi

PLATFORM_EXPERTS="$MT5_PLATFORM/MQL5/Experts"
mkdir -p "$PLATFORM_EXPERTS"
if [ -f "$BRIDGE_SRC" ]; then
    cp -f "$BRIDGE_SRC" "$PLATFORM_EXPERTS/KhmerMasterCrypto_Bridge.mq5"
    chown "$TARGET_USER:$TARGET_USER" "$PLATFORM_EXPERTS/KhmerMasterCrypto_Bridge.mq5"
    echo -e "${GREEN}✅ Staged KhmerMasterCrypto_Bridge.mq5 to Master Experts directory!${NC}"
fi

# Stage pre-compiled .ex5 if present
BRIDGE_EX5="$WORKSPACE_DIR/KhmerMasterCrypto_Bridge.ex5"
if [ ! -f "$BRIDGE_EX5" ]; then
    BRIDGE_EX5="$(dirname "$0")/KhmerMasterCrypto_Bridge.ex5"
fi
if [ -f "$BRIDGE_EX5" ]; then
    cp -f "$BRIDGE_EX5" "$PLATFORM_EXPERTS/KhmerMasterCrypto_Bridge.ex5"
    chown "$TARGET_USER:$TARGET_USER" "$PLATFORM_EXPERTS/KhmerMasterCrypto_Bridge.ex5"
fi

# 5. Create Desktop Shortcut for Master PAMM MT5
if [ -d "$DESKTOP_DIR" ]; then
    rm -f "$DESKTOP_DIR"/Launch_MT5_*.desktop 2>/dev/null || true
    rm -f "$DESKTOP_DIR"/1_Launch_Super_Admin_MT5.desktop 2>/dev/null || true
    rm -f "$DESKTOP_DIR"/2_Launch_MT5_Platform.desktop 2>/dev/null || true

    cat << EOF > "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=🛡️ START GTC PAMM MT5 (#52171861)
Comment=Launch Super Admin PAMM MetaTrader 5 Terminal 24/7
Path=$MT5_PLATFORM
Exec=bash -c 'cd "$MT5_PLATFORM" && wine terminal64.exe /portable /config:startup.ini'
Icon=wine
Terminal=false
StartupNotify=true
Categories=Application;Finance;
EOF
    chmod +x "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
    chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
    echo -e "${GREEN}✅ Created single canonical Desktop Shortcut for Master PAMM MT5 (#52171861)!${NC}"
fi

# 6. Install Global CLI Commands
cat << EOF > /usr/local/bin/mt5-pamm-start
#!/bin/bash
TARGET_USER="$TARGET_USER"
TARGET_HOME="$TARGET_HOME"
echo "🚀 Starting GTC PAMM Master MT5 Terminal (52171861)..."
sudo -u "\$TARGET_USER" DISPLAY=:10.0 bash -c "cd '\$TARGET_HOME/.wine/drive_c/Program Files/MetaTrader 5_Platform' && nohup wine terminal64.exe /portable /config:startup.ini >/dev/null 2>&1 &"
echo "✅ GTC PAMM Master MT5 Terminal (52171861) launched in background."
EOF
chmod +x /usr/local/bin/mt5-pamm-start

# Symlink legacy commands to mt5-pamm-start
ln -sf /usr/local/bin/mt5-pamm-start /usr/local/bin/mt5-admin-start
ln -sf /usr/local/bin/mt5-pamm-start /usr/local/bin/mt5-platform-start
ln -sf /usr/local/bin/mt5-pamm-start /usr/local/bin/mt5-dual-start

echo ""
echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}✅ GTC PAMM SINGLE MASTER MT5 SETUP COMPLETE!${NC}"
echo -e "${CYAN}• Master Account: #52171861 on GTCGlobalSA-Server 2.${NC}"
echo -e "${CYAN}• Disk Preservation: All duplicate/client folders purged; zero disk bloat.${NC}"
echo -e "${CYAN}• Launch shortcut: Desktop '0_START_GTC_PAMM_MT5.desktop' or 'mt5-pamm-start'.${NC}"
echo -e "${CYAN}==============================================================================${NC}"
