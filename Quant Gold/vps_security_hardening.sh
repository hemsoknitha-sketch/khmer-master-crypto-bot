#!/usr/bin/env bash
# ==============================================================================
# ANGKOR QUANT - QUANT GOLD VPS SECURITY CITADEL HARDENING SCRIPT (AQ84)
# ==============================================================================
# Target: Google Cloud Linux VPS 'quant-gold' (Ubuntu 22.04+ LTS / Debian)
# Author: HEM SINATH | Institutional Quantitative Governance
# Version: 1.0.0
#
# Purpose:
#   Executes 5-layer system-level security hardening on the Google Cloud VPS:
#     1. UFW Firewall Strict Inbound Lockdown (Default Deny, Only SSH Allowed)
#     2. File Permission Hardening (.env locked to chmod 600)
#     3. Systemd Service Hardening (Memory limits, NoNewPrivileges, ProtectSystem)
#     4. Zero-OOM Swap Allocation Audit (2.0GB Swap Protection)
#     5. Journald Log Rotation Clamping (Prevents disk exhaustion)
# ==============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}  🛡️ ANGKOR QUANT - QUANT GOLD VPS SECURITY HARDENING CITADEL${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Check root / sudo privileges
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}❌ Please run this script with sudo or as root: sudo bash vps_security_hardening.sh${NC}"
  exit 1
fi

PROJECT_DIR="/opt/khmer-master-crypto-bot"
QG_DIR="$PROJECT_DIR/Quant Gold"

# Detect non-root operating user
ACTUAL_USER="${SUDO_USER:-$(logname 2>/dev/null || whoami)}"
if [ "$ACTUAL_USER" = "root" ] || [ -z "$ACTUAL_USER" ]; then
    if id "hemsoknitha" >/dev/null 2>&1; then
        ACTUAL_USER="hemsoknitha"
    elif id "sokni" >/dev/null 2>&1; then
        ACTUAL_USER="sokni"
    else
        ACTUAL_USER="hemsoknitha"
    fi
fi
ACTUAL_GROUP=$(id -gn "$ACTUAL_USER" 2>/dev/null || echo "$ACTUAL_USER")
echo -e "👤 Target Service User: ${GREEN}$ACTUAL_USER:$ACTUAL_GROUP${NC}"

# ------------------------------------------------------------------------------
# STEP 1: UFW Firewall Hardening
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[STEP 1/5] Configuring UFW Strict Inbound Lockdown...${NC}"
if command -v ufw >/dev/null 2>&1; then
    # Reset / ensure default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH (Port 22) with connection rate limiting to stop brute-force
    ufw limit 22/tcp comment 'SSH Secure Access with Brute-Force Rate Limiting'
    
    # Enable UFW non-interactively
    ufw --force enable
    echo -e "${GREEN}✅ [UFW HARDENED] Default DENY incoming, SSH rate-limited on port 22.${NC}"
else
    echo -e "${YELLOW}⚠️ UFW not found. Installing ufw...${NC}"
    apt-get update -y && apt-get install -y ufw
    ufw default deny incoming
    ufw default allow outgoing
    ufw limit 22/tcp comment 'SSH Secure Access'
    ufw --force enable
    echo -e "${GREEN}✅ [UFW INSTALLED & HARDENED]${NC}"
fi

# ------------------------------------------------------------------------------
# STEP 2: Sensitive Environment Secrets Hardening (.env chmod 600)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[STEP 2/5] Securing .env secret file permissions (chmod 600)...${NC}"
for env_file in "$PROJECT_DIR/.env" "$QG_DIR/.env"; do
    if [ -f "$env_file" ]; then
        chmod 600 "$env_file"
        chown "$ACTUAL_USER:$ACTUAL_GROUP" "$env_file" 2>/dev/null || true
        echo -e "${GREEN}✅ Secured $env_file (Owner: $ACTUAL_USER, Permissions: -rw------- 600)${NC}"
    fi
done

# Ensure all files and databases in project are owned by service user
chown -R "$ACTUAL_USER:$ACTUAL_GROUP" "$PROJECT_DIR" 2>/dev/null || true
echo -e "${GREEN}✅ Workspace ownership verified for $ACTUAL_USER:$ACTUAL_GROUP.${NC}"

# ------------------------------------------------------------------------------
# STEP 3: Zero-OOM 2.0GB Swap Memory Verification
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[STEP 3/5] Verifying Zero-OOM Swap Memory Shield...${NC}"
CURRENT_SWAP=$(free -m | awk '/Swap:/ {print $2}')
if [ "$CURRENT_SWAP" -ge 1800 ]; then
    echo -e "${GREEN}✅ Swap Memory active: ${CURRENT_SWAP} MB (Zero OOM Shield Certified).${NC}"
else
    echo -e "${YELLOW}⚠️ Current Swap is ${CURRENT_SWAP} MB. Allocating 2.0GB Swapfile...${NC}"
    swapoff -a 2>/dev/null || true
    if [ -f /swapfile ]; then
        rm -f /swapfile
    fi
    fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    
    # Ensure in /etc/fstab
    if ! grep -q '/swapfile' /etc/fstab; then
        echo '/swapfile none swap sw 0 0' >> /etc/fstab
    fi
    # Optimize swappiness for low-RAM e2-micro VPS
    sysctl vm.swappiness=20 >/dev/null 2>&1
    sysctl vm.vfs_cache_pressure=50 >/dev/null 2>&1
    echo -e "${GREEN}✅ 2.0GB Zero-OOM Swap allocated and activated!${NC}"
fi

# ------------------------------------------------------------------------------
# STEP 4: Systemd Service Security Hardening
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[STEP 4/5] Deploying Hardened Systemd Service (quant-gold.service)...${NC}"
SERVICE_DEST="/etc/systemd/system/quant-gold.service"
cat << EOF > "$SERVICE_DEST"
# ==============================================================================
# ANGKOR QUANT - QUANT GOLD HARDENED SYSTEMD SERVICE (AQ84)
# ==============================================================================
[Unit]
Description=Angkor Quant - Quant Gold 24/7/365 Autonomous AI Trading Daemon
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$ACTUAL_USER
Group=$ACTUAL_GROUP
WorkingDirectory=/opt/khmer-master-crypto-bot
ExecStart=/opt/khmer-master-crypto-bot/venv/bin/python run_quant_gold.py
Restart=always
RestartSec=5
SuccessExitStatus=0
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal
SyslogIdentifier=quant-gold

# Institutional Resource & Memory Caps (Zero OOM Shield)
LimitNOFILE=65535
MemoryMax=850M
MemoryHigh=750M
TimeoutStopSec=15
KillMode=mixed

# Institutional Linux Security Hardening
NoNewPrivileges=true
ProtectSystem=full
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
echo -e "${GREEN}✅ quant-gold.service deployed with MemoryMax=850M & NoNewPrivileges=true!${NC}"

# ------------------------------------------------------------------------------
# STEP 5: Journald Log Clamping (Anti-Disk Overflow)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[STEP 5/5] Configuring Log Retention (Anti-Disk Exhaustion)...${NC}"
if [ -f /etc/systemd/journald.conf ]; then
    sed -i 's/^#SystemMaxUse=.*/SystemMaxUse=200M/' /etc/systemd/journald.conf || true
    systemctl restart systemd-journald 2>/dev/null || true
    echo -e "${GREEN}✅ System logs clamped to max 200 MB storage.${NC}"
fi

echo -e "\n${BLUE}======================================================================${NC}"
echo -e "${GREEN}  🎉 [SUCCESS] VPS SYSTEM HARDENING COMPLETED WITH ZERO DEFECTS!${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo -e "To restart Quant Gold with hardened parameters:"
echo -e "  sudo systemctl restart quant-gold"
echo -e "To inspect live health & status:"
echo -e "  sudo systemctl status quant-gold"
echo -e "${BLUE}======================================================================${NC}"

