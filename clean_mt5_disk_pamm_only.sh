#!/bin/bash
# ==============================================================================
# ANGKOR QUANT / APEX SUPER BRAIN AI
# DEDICATED MT5 DISK PRUNER & GTC PAMM MASTER CONSOLIDATOR (INVARIANT 105)
# ==============================================================================
# Objective:
#   Purges 100% of non-PAMM MT5 directories, obsolete EAs, crash dumps,
#   bloated historical logs, and duplicate wine bottles to reclaim VPS disk space.
#   Ensures ONLY the GTC PAMM Master Account (#52171861) is preserved.
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}   🛡️ ANGKOR QUANT — MT5 DISK PRUNER & PAMM CONSOLIDATOR 🛡️${NC}"
echo -e "${YELLOW}   Decommissions All Non-PAMM EAs & Reclaims Multi-Gigabyte VPS Disk Space${NC}"
echo -e "${CYAN}==============================================================================${NC}"

TARGET_USER="${SUDO_USER:-$USER}"
TARGET_HOME=$(eval echo "~$TARGET_USER")
WINE_PROGRAMS="$TARGET_HOME/.wine/drive_c/Program Files"
DESKTOP_DIR="$TARGET_HOME/Desktop"

echo -e "👤 Target User:     ${BOLD}${CYAN}$TARGET_USER${NC}"
echo -e "📁 Wine Programs:   ${CYAN}$WINE_PROGRAMS${NC}"
echo ""

# 1. Measure initial disk space
echo -e "${YELLOW}[1/6] 📊 Initial VPS Disk Space Usage:${NC}"
df -h / | tail -n 1
DISK_BEFORE=$(df -k / | tail -n 1 | awk '{print $3}')
echo ""

# 2. Stop all Wine & MT5 terminal processes safely
echo -e "${YELLOW}[2/6] 🛑 Terminating all running MT5 terminals and Wine servers...${NC}"
pkill -9 -f "terminal64.exe" 2>/dev/null || true
pkill -9 -f "metaeditor" 2>/dev/null || true
pkill -9 -f "wineserver" 2>/dev/null || true
wineserver -k 2>/dev/null || true
sleep 2
echo -e "   ${GREEN}✅ All processes halted cleanly.${NC}"
echo ""

# 3. Detect and remove all non-PAMM MT5 account clones
echo -e "${YELLOW}[3/6] 🧹 Scanning and pruning non-PAMM MT5 account folders...${NC}"
MT5_PLATFORM="$WINE_PROGRAMS/MetaTrader 5_Platform"
MT5_ORIGINAL="$WINE_PROGRAMS/MetaTrader 5"

# Remove all cloned folders like MetaTrader 5_<account_id>
CLONES_REMOVED=0
if [ -d "$WINE_PROGRAMS" ]; then
    for DIR in "$WINE_PROGRAMS/MetaTrader 5_"*; do
        if [ -d "$DIR" ] && [ "$DIR" != "$MT5_PLATFORM" ]; then
            echo -e "   ${RED}🗑️ Deleting non-PAMM clone: $(basename "$DIR")...${NC}"
            rm -rf "$DIR"
            CLONES_REMOVED=$((CLONES_REMOVED + 1))
        fi
    done
fi

if [ "$CLONES_REMOVED" -eq 0 ]; then
    echo -e "   ${GREEN}✅ No obsolete account clone folders found.${NC}"
else
    echo -e "   ${GREEN}✅ Removed $CLONES_REMOVED obsolete non-PAMM MT5 folders!${NC}"
fi

# Consolidate duplicate base folders if both MetaTrader 5 and MetaTrader 5_Platform exist
if [ -d "$MT5_PLATFORM" ] && [ -d "$MT5_ORIGINAL" ]; then
    echo -e "   ${YELLOW}ℹ️ Both MetaTrader 5 and MetaTrader 5_Platform exist.${NC}"
    echo -e "   ${YELLOW}🧹 Consolidating to single Master Platform folder and removing duplicate ~1.5 GB...${NC}"
    rm -rf "$MT5_ORIGINAL"
    echo -e "   ${GREEN}✅ Duplicate base folder removed successfully!${NC}"
elif [ ! -d "$MT5_PLATFORM" ] && [ -d "$MT5_ORIGINAL" ]; then
    echo -e "   ${CYAN}Renaming MetaTrader 5 to MetaTrader 5_Platform for canonical consistency...${NC}"
    mv "$MT5_ORIGINAL" "$MT5_PLATFORM"
fi

PRIMARY_MT5="$MT5_PLATFORM"
echo ""

# 4. Deep-clean crash dumps, logs, and temp files inside the remaining Master PAMM folder
echo -e "${YELLOW}[4/6] 🧹 Purging crash dumps, logs, and historical cache inside Master PAMM folder...${NC}"
if [ -d "$PRIMARY_MT5" ]; then
    find "$PRIMARY_MT5" -name "*.dmp" -type f -delete 2>/dev/null || true
    find "$PRIMARY_MT5" -name "compile.log" -type f -delete 2>/dev/null || true
    find "$PRIMARY_MT5" -path "*/Logs/*" -name "*.log" -type f -delete 2>/dev/null || true
    find "$PRIMARY_MT5" -path "*/logs/*" -name "*.log" -type f -delete 2>/dev/null || true
    find "$PRIMARY_MT5" -path "*/tester/*" -type f -delete 2>/dev/null || true
    echo -e "   ${GREEN}✅ Master PAMM terminal cache sanitized!${NC}"
fi

# 5. Clean Wine temporary files and system locks
echo -e "${YELLOW}[5/6] 🧹 Purging Wine temporary directories and user temp files...${NC}"
rm -rf /tmp/.wine-* /tmp/wine-* /tmp/.X*-lock /tmp/*.log /tmp/core* 2>/dev/null || true
rm -rf "$TARGET_HOME/.wine/drive_c/users"/*/AppData/Local/Temp/* 2>/dev/null || true
rm -rf "$TARGET_HOME/.wine/drive_c/windows/temp/*" 2>/dev/null || true

# Clean stale desktop launchers for other accounts
if [ -d "$DESKTOP_DIR" ]; then
    rm -f "$DESKTOP_DIR"/Launch_MT5_*.desktop 2>/dev/null || true
    rm -f "$DESKTOP_DIR"/Launch_Admin_MT5.desktop 2>/dev/null || true
fi
echo -e "   ${GREEN}✅ Temporary files and stale desktop launchers purged!${NC}"
echo ""

# 6. Measure final disk space & show savings
echo -e "${YELLOW}[6/6] 📊 Final VPS Disk Space Usage:${NC}"
df -h / | tail -n 1
DISK_AFTER=$(df -k / | tail -n 1 | awk '{print $3}')
SAVED_KB=$((DISK_BEFORE - DISK_AFTER))
if [ "$SAVED_KB" -gt 0 ]; then
    SAVED_MB=$((SAVED_KB / 1024))
    echo -e "   ${BOLD}${GREEN}🎉 Total Disk Space Reclaimed: ~${SAVED_MB} MB (~$((SAVED_MB / 1024)) GB)!${NC}"
else
    echo -e "   ${GREEN}✅ Disk space is already fully optimized.${NC}"
fi
echo ""

# Ensure Master PAMM startup.ini is configured for #52171861
if [ -d "$PRIMARY_MT5" ]; then
    cat << EOF > "$PRIMARY_MT5/startup.ini"
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
    chown "$TARGET_USER:$TARGET_USER" "$PRIMARY_MT5/startup.ini"
    chmod 600 "$PRIMARY_MT5/startup.ini"
    mkdir -p "$PRIMARY_MT5/config"
    cp -f "$PRIMARY_MT5/startup.ini" "$PRIMARY_MT5/config/startup.ini"
    chown -R "$TARGET_USER:$TARGET_USER" "$PRIMARY_MT5"
    chmod -R 775 "$PRIMARY_MT5"

    # Create / update canonical Desktop Shortcut
    if [ -d "$DESKTOP_DIR" ]; then
        cat << EOF > "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=🛡️ START GTC PAMM MT5 (#52171861)
Comment=Launch Super Admin PAMM MetaTrader 5 Terminal 24/7
Exec=bash -c "cd '$PRIMARY_MT5' && wine terminal64.exe /portable /config:startup.ini"
Icon=wine
Path=$PRIMARY_MT5
Terminal=false
StartupNotify=true
Categories=Application;Finance;
EOF
        chown "$TARGET_USER:$TARGET_USER" "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
        chmod +x "$DESKTOP_DIR/0_START_GTC_PAMM_MT5.desktop"
    fi
fi

# Auto-launch the clean GTC PAMM Master MT5 Terminal
echo -e "${YELLOW}🚀 Launching sanitized GTC PAMM Master MT5 (#52171861)...${NC}"
DETECTED_DISPLAY="${DISPLAY:-:10.0}"
if [ -e /tmp/.X11-unix/X10 ]; then
    DETECTED_DISPLAY=":10.0"
elif [ -e /tmp/.X11-unix/X11 ]; then
    DETECTED_DISPLAY=":11.0"
elif [ -e /tmp/.X11-unix/X0 ]; then
    DETECTED_DISPLAY=":0.0"
fi

LOG_FILE="$TARGET_HOME/mt5_platform_launch.log"
sudo -u "$TARGET_USER" DISPLAY="$DETECTED_DISPLAY" bash -c "cd '$PRIMARY_MT5' && nohup wine terminal64.exe /portable /config:startup.ini > '$LOG_FILE' 2>&1 &"

sleep 3
if ps aux | grep -i "terminal64.exe" | grep -v grep >/dev/null; then
    echo -e "${GREEN}🚀 GTC PAMM Master MT5 (#52171861) is RUNNING actively in Wine!${NC}"
    ps aux | grep -i "terminal64.exe" | grep -v grep
fi

echo ""
echo -e "${CYAN}==============================================================================${NC}"
echo -e "${BOLD}${GREEN}✅ MT5 SYSTEM AUDIT & DISK CLEANUP COMPLETE!${NC}"
echo -e "${CYAN}• Retained: GTC PAMM Master Account (#52171861) exclusively.${NC}"
echo -e "${CYAN}• Purged: All non-PAMM EAs, redundant folders, crash dumps & bloated logs.${NC}"
echo -e "${CYAN}• Status: Single Master PAMM terminal active 24/7 with zero disk bloat.${NC}"
echo -e "${CYAN}==============================================================================${NC}"

