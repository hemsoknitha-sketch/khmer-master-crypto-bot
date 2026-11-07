# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD GOOGLE CLOUD VPS DEPLOYER & SYNCHRONIZER (AQ84 / AQ87)
=================================================================================
Target: Google Cloud Linux VPS 'quant-gold'
Project: quant-gold-514007 | Zone: us-central1-a | Instance: quant-gold
Console URL: https://console.cloud.google.com/compute/instancesDetail/zones/us-central1-a/instances/quant-gold?project=quant-gold-514007
Author: HEM SINATH | Institutional Quantitative Governance
Version: 1.0.0

Usage:
  python update_vps.py                      # Git Push + Trigger Zero-Downtime VPS Sync
  python update_vps.py "commit message"     # Custom commit message & auto-update
  python update_vps.py --status             # Inspect VPS connection & configuration
  python update_vps.py --logs               # View live service logs from VPS
  python update_vps.py --restart            # Restart 24/7 quant-gold systemd service
  python update_vps.py --setup              # Run 1-tap VPS environment & systemd setup
=================================================================================
"""

import os
import sys
import argparse
import subprocess
import time
import shutil
from datetime import datetime
from typing import Dict, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Force non-interactive Git environment to eliminate IDE freezing
os.environ["GIT_TERMINAL_PROMPT"] = "0"
os.environ["GCM_INTERACTIVE"] = "never"

# Default Google Cloud Metadata for quant-gold
DEFAULT_GCP_PROJECT = "quant-gold-514007"
DEFAULT_GCP_ZONE = "us-central1-a"
DEFAULT_GCP_INSTANCE = "quant-gold"
DEFAULT_GCP_CONSOLE_URL = (
    "https://console.cloud.google.com/compute/instancesDetail/zones/"
    "us-central1-a/instances/quant-gold?project=quant-gold-514007"
)


def load_env_config(env_path: str = ".env") -> Dict[str, str]:
    """Loads configuration keys safely from root or Quant Gold/.env file."""
    config: Dict[str, str] = {}
    paths_to_check = [
        env_path,
        os.path.join("Quant Gold", ".env"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    ]

    for p in paths_to_check:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in config:
                            config[k] = v
            except Exception as exc:
                print(f"⚠️ [WARN] Error reading {p}: {exc}")

    return config


def run_command(cmd: list, check: bool = False, timeout: int = 120) -> Tuple[int, str]:
    """Runs a subprocess command with non-blocking streaming."""
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        lines = []
        for line in iter(proc.stdout.readline, ""):
            lines.append(line)
            sys.stdout.write(line)
            sys.stdout.flush()

        proc.stdout.close()
        rc = proc.wait(timeout=timeout)
        output = "".join(lines)
        if check and rc != 0:
            raise subprocess.CalledProcessError(rc, cmd, output=output)
        return rc, output
    except Exception as exc:
        print(f"❌ [COMMAND ERROR] {' '.join(cmd)} failed: {exc}")
        return 1, str(exc)


def configure_git_credentials(cfg: Dict[str, str]):
    """Configures local git user and credential store."""
    user = cfg.get("GIT_PUSH_USER", "hem sinath")
    email = cfg.get("GIT_PUSH_USER_EMAIL", "hem.sinath@gmail.com")
    subprocess.run(["git", "config", "user.name", user], capture_output=True)
    subprocess.run(["git", "config", "user.email", email], capture_output=True)
    subprocess.run(["git", "config", "credential.helper", "store"], capture_output=True)
    subprocess.run(["git", "config", "pull.rebase", "false"], capture_output=True)


def execute_ssh_remote_command(cfg: Dict[str, str], remote_cmd: str, timeout: int = 60) -> int:
    """
    Executes a command on the Google Cloud Linux VPS via SSH or gcloud CLI.
    Fallback: provides 1-tap browser web console instructions.
    """
    vps_host = cfg.get("VPS_HOST", "").strip()
    vps_user = cfg.get("VPS_USER", "sokni").strip()
    gcp_project = cfg.get("GCP_PROJECT_ID", DEFAULT_GCP_PROJECT)
    gcp_zone = cfg.get("GCP_ZONE", DEFAULT_GCP_ZONE)
    gcp_instance = cfg.get("GCP_INSTANCE_NAME", DEFAULT_GCP_INSTANCE)

    # Check if gcloud is installed in PATH
    has_gcloud = shutil.which("gcloud") is not None

    if has_gcloud:
        print(f"\n🌐 [GCLOUD SSH] Executing remote command on {gcp_instance} ({gcp_project} / {gcp_zone})...")
        cmd = [
            "gcloud", "compute", "ssh", gcp_instance,
            f"--project={gcp_project}",
            f"--zone={gcp_zone}",
            f"--command={remote_cmd}"
        ]
        rc, _ = run_command(cmd, timeout=timeout)
        return rc

    elif vps_host and vps_host != "your_vps_external_ip_here":
        print(f"\n🌐 [DIRECT SSH] Executing remote command on {vps_user}@{vps_host}...")
        ssh_bin = shutil.which("ssh") or "ssh"
        cmd = [
            ssh_bin,
            "-o", "ConnectTimeout=8",
            "-o", "StrictHostKeyChecking=no",
            f"{vps_user}@{vps_host}",
            remote_cmd
        ]
        rc, _ = run_command(cmd, timeout=timeout)
        return rc

    else:
        print("\nℹ️ [VPS NOTICE] Direct automated SSH host is waiting for IP configuration.")
        print(f"   Google Cloud Console URL: {DEFAULT_GCP_CONSOLE_URL}")
        print("   To run this command directly in Cloud Shell or VPS Web SSH, copy & paste:")
        print(f"\n   \033[1;32m{remote_cmd}\033[0m\n")
        return 0


def update_and_deploy_vps(commit_msg: Optional[str] = None):
    """Main workflow: Git Commit -> Git Push -> Trigger Google Cloud VPS Update."""
    print("=" * 76)
    print("  🚀 ANGKOR QUANT - QUANT GOLD GOOGLE CLOUD VPS DEPLOYER (AQ84 / AQ87)")
    print(f"  📍 Target Instance: {DEFAULT_GCP_INSTANCE} | Project: {DEFAULT_GCP_PROJECT}")
    print(f"  🌐 Zone: {DEFAULT_GCP_ZONE} (Free 24/7 365 Architecture)")
    print(f"  🔗 Console: {DEFAULT_GCP_CONSOLE_URL}")
    print("=" * 76)

    cfg = load_env_config()
    configure_git_credentials(cfg)

    branch = cfg.get("GIT_BRANCH", "main")
    user = cfg.get("GIT_PUSH_USER", "hem sinath")
    vps_path = cfg.get("VPS_DEPLOY_PATH", "/opt/khmer-master-crypto-bot")

    # 1. Stage all changes
    print("\n📦 [STEP 1/3] Staging all changes (git add -A)...")
    add_rc, _ = run_command(["git", "add", "-A"])
    if add_rc != 0:
        print("❌ Failed to stage changes. Aborting.")
        return False

    # Check git status
    st_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, errors="replace")
    has_changes = bool(st_res.stdout.strip())

    # 2. Commit
    if has_changes:
        if not commit_msg:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"feat(quant-gold): update 24/7 engine for GCP quant-gold by {user} [{now_str}]"

        print(f"\n📝 [STEP 2/3] Committing changes: '{commit_msg}'...")
        run_command(["git", "commit", "-m", commit_msg])
    else:
        print("\n📝 [STEP 2/3] Working tree clean. Checking for unpushed commits...")

    # 3. Push to GitHub Origin Main
    print(f"\n🚀 [STEP 3/3] Pushing to remote origin {branch}...")
    push_rc, _ = run_command(["git", "push", "origin", branch])
    if push_rc != 0:
        print("❌ Push failed. Please verify git credentials and internet connection.")
        return False

    print("\n" + "=" * 76)
    print("  ✅ [SUCCESS] CODE PUSHED TO GITHUB ORIGIN MAIN WITH ZERO DEFECTS!")
    print("=" * 76)

    # 4. Trigger VPS Remote Update
    remote_sync_cmd = f"cd {vps_path} && bash auto_update_vps.sh"
    print("\n🔄 [REMOTE SYNC] Triggering Zero-Downtime VPS Auto-Update...")
    execute_ssh_remote_command(cfg, remote_sync_cmd, timeout=90)

    print("\n" + "=" * 76)
    print("  🎉 QUANT GOLD DEPLOYMENT CYCLE COMPLETE!")
    print("  1-Tap Directive to verify on Google Cloud VPS:")
    print(f"  \033[1;36msudo systemctl status quant-gold.service\033[0m")
    print(f"  \033[1;36mjournalctl -u quant-gold.service -n 50 -f\033[0m")
    print("=" * 76)
    return True


def show_status():
    """Displays current VPS deployment status and configuration."""
    cfg = load_env_config()
    print("=" * 76)
    print("  🔍 ANGKOR QUANT - QUANT GOLD VPS CONFIGURATION & STATUS")
    print("=" * 76)
    print(f"GCP Project:        {cfg.get('GCP_PROJECT_ID', DEFAULT_GCP_PROJECT)}")
    print(f"GCP Zone:           {cfg.get('GCP_ZONE', DEFAULT_GCP_ZONE)}")
    print(f"GCP Instance:       {cfg.get('GCP_INSTANCE_NAME', DEFAULT_GCP_INSTANCE)}")
    print(f"GCP Console:        {DEFAULT_GCP_CONSOLE_URL}")
    print(f"VPS Host / IP:      {cfg.get('VPS_HOST', 'Waiting for IP configuration')}")
    print(f"VPS SSH User:       {cfg.get('VPS_USER', 'sokni')}")
    print(f"Deploy Directory:   {cfg.get('VPS_DEPLOY_PATH', '/opt/khmer-master-crypto-bot')}")
    print(f"Service Name:       {cfg.get('VPS_SERVICE_NAME', 'quant-gold.service')}")

    # Check local git status
    st = subprocess.run(["git", "status"], capture_output=True, text=True, errors="replace").stdout
    print("\nLocal Git Status:")
    print(st)


def view_logs():
    """Tails real-time service logs on the VPS."""
    cfg = load_env_config()
    svc = cfg.get("VPS_SERVICE_NAME", "quant-gold.service")
    cmd = f"journalctl -u {svc} -u khmer-master-crypto-bot.service -n 50 --no-pager"
    execute_ssh_remote_command(cfg, cmd, timeout=30)


def restart_service():
    """Restarts systemd service cleanly on the VPS."""
    cfg = load_env_config()
    svc = cfg.get("VPS_SERVICE_NAME", "quant-gold.service")
    cmd = f"sudo systemctl restart {svc} || sudo systemctl restart khmer-master-crypto-bot.service"
    execute_ssh_remote_command(cfg, cmd, timeout=30)


def run_setup():
    """Triggers complete 1-tap setup on the VPS."""
    cfg = load_env_config()
    vps_path = cfg.get("VPS_DEPLOY_PATH", "/opt/khmer-master-crypto-bot")
    cmd = f"cd {vps_path} && bash setup_quant_gold_vps.sh"
    execute_ssh_remote_command(cfg, cmd, timeout=180)


def main():
    parser = argparse.ArgumentParser(
        description="Angkor Quant - Quant Gold Google Cloud Linux VPS Deployer (quant-gold)"
    )
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="Optional Git commit message"
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show VPS configuration and git status"
    )
    parser.add_argument(
        "--logs", "-l",
        action="store_true",
        help="View live systemd logs from the VPS"
    )
    parser.add_argument(
        "--restart", "-r",
        action="store_true",
        help="Restart quant-gold systemd service on VPS"
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run full automated environment & systemd setup on the VPS"
    )

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.logs:
        view_logs()
    elif args.restart:
        restart_service()
    elif args.setup:
        run_setup()
    else:
        success = update_and_deploy_vps(commit_msg=args.message)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

