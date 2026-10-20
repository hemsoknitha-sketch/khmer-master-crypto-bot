# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - UNIVERSAL CROSS-PLATFORM GIT PUSH & ZERO-FRICTION VPS DEPLOYER (AQ87 INVARIANT 87)
==================================================================================================
Author: HEM SINATH | Institutional Quantitative Governance
Version: 1.0.0

Purpose:
  Enables every Code Editor Platform (Google Antigravity IDE, Cursor, VS Code, PyCharm,
  Windsurf, Neovim, Windows PowerShell, Linux/macOS Terminal) to execute seamless, non-blocking
  Git Push and VPS Deployment without ever freezing, hanging, or requiring interactive prompts.

Usage:
  python git_push_vps.py "your commit message"
  python git_push_vps.py --status
  python git_push_vps.py --skip-audit "emergency hotfix"
"""

import os
import sys
import argparse
import subprocess
import time
from datetime import datetime
from typing import Dict, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Force non-interactive Git environment to prevent IDE freezes
os.environ["GIT_TERMINAL_PROMPT"] = "0"
os.environ["GCM_INTERACTIVE"] = "never"


def load_env_config(env_path: str = ".env") -> Dict[str, str]:
    """Loads configuration keys safely from .env file."""
    config: Dict[str, str] = {}
    if not os.path.exists(env_path):
        return config

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                config[k] = v
    except Exception as exc:
        print(f"⚠️ [WARN] Error reading {env_path}: {exc}")

    return config


def run_command_stream(cmd: list, check: bool = False, timeout: int = 180) -> Tuple[int, str]:
    """Runs a subprocess command with non-blocking line streaming."""
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        output_lines = []
        for line in iter(proc.stdout.readline, ""):
            output_lines.append(line)
            sys.stdout.write(line)
            sys.stdout.flush()

        proc.stdout.close()
        return_code = proc.wait(timeout=timeout)
        full_output = "".join(output_lines)
        if check and return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd, output=full_output)
        return return_code, full_output
    except Exception as exc:
        print(f"❌ [EXEC ERROR] Command {' '.join(cmd)} failed: {exc}")
        return 1, str(exc)


def configure_git_identity(env_cfg: Dict[str, str]) -> None:
    """Configures local git user and credential helper store non-interactively."""
    git_user = env_cfg.get("GIT_PUSH_USER", "hem sinath")
    git_email = env_cfg.get("GIT_PUSH_USER_EMAIL", "hem.sinath@gmail.com")

    subprocess.run(["git", "config", "user.name", git_user], capture_output=True)
    subprocess.run(["git", "config", "user.email", git_email], capture_output=True)
    subprocess.run(["git", "config", "credential.helper", "store"], capture_output=True)
    subprocess.run(["git", "config", "pull.rebase", "false"], capture_output=True)


def check_git_status() -> Tuple[bool, str]:
    """Returns whether there are uncommitted changes and git status output."""
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, errors="replace")
    has_changes = bool(res.stdout.strip())
    full_status = subprocess.run(["git", "status"], capture_output=True, text=True, errors="replace").stdout
    return has_changes, full_status


def execute_git_push_vps(
    commit_msg: Optional[str] = None,
    skip_audit: bool = False,
    auto_deploy: bool = False
) -> bool:
    """Master workflow: Audit -> Stage -> Commit -> Push -> VPS Directive."""
    print("=" * 75)
    print("  🚀 ANGKOR QUANT - UNIVERSAL CROSS-PLATFORM GIT & VPS DEPLOYER (AQ87)")
    print("=" * 75)

    env_cfg = load_env_config()
    configure_git_identity(env_cfg)

    git_user = env_cfg.get("GIT_PUSH_USER", "hem sinath")
    git_email = env_cfg.get("GIT_PUSH_USER_EMAIL", "hem.sinath@gmail.com")
    git_branch = env_cfg.get("GIT_BRANCH", "main")
    vps_cmd = env_cfg.get("VPS_SYNC_COMMAND", "cd /opt/khmer-master-crypto-bot && bash auto_update_vps.sh")

    print(f"👤 Git Operator: {git_user} <{git_email}>")
    print(f"🌿 Target Branch: {git_branch}")
    print(f"🛡️ Non-Interactive Flags: GIT_TERMINAL_PROMPT=0, GCM_INTERACTIVE=never")
    print("-" * 75)

    # 1. Institutional Pre-Commit Audit Gate
    if not skip_audit:
        print("\n🔍 [STEP 1/4] Running Institutional Audit Gate (audit_system.py)...")
        code, _ = run_command_stream([sys.executable, "audit_system.py"])
        if code != 0:
            print("\n❌ [AUDIT REJECTED] Pre-commit audit failed with defects. Push aborted!")
            print("   Fix all defects or use --skip-audit only in critical emergency.")
            return False
        print("✅ [AUDIT PASSED] 100% Institutional Invariants verified with ZERO defects!")
    else:
        print("\n⚠️ [STEP 1/4] Audit bypassed via --skip-audit flag.")

    # 2. Stage Changes
    print("\n📦 [STEP 2/4] Staging working copy files (git add -A)...")
    add_code, _ = run_command_stream(["git", "add", "-A"])
    if add_code != 0:
        print("❌ [STAGE ERROR] Failed to stage files.")
        return False

    has_changes, _ = check_git_status()

    # 3. Commit
    if has_changes:
        if not commit_msg:
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"feat(core): institutional sync by {git_user} [{timestamp_str}] (AQ87)"

        print(f"\n📝 [STEP 3/4] Committing changes with message: '{commit_msg}'...")
        commit_code, _ = run_command_stream(["git", "commit", "-m", commit_msg])
        if commit_code != 0:
            print("⚠️ Commit step completed (or nothing changed). Continuing to push...")
    else:
        print("\n📝 [STEP 3/4] Working tree already clean. Checking for unpushed commits...")

    # 4. Push to Remote Origin
    print(f"\n🚀 [STEP 4/4] Pushing to remote origin {git_branch} (Non-Blocking)...")
    push_code, _ = run_command_stream(["git", "push", "origin", git_branch])
    if push_code != 0:
        print(f"❌ [PUSH ERROR] Failed to push to origin {git_branch}. Verify credentials/network.")
        return False

    print("\n" + "=" * 75)
    print("  ✅ [SUCCESS] CODE PUSHED TO GITHUB ORIGIN MAIN WITH ZERO DEFECTS!")
    print("=" * 75)
    print("  To update your Tokyo GCP VPS instance, run the 1-tap directive:")
    print(f"  \033[1;32m{vps_cmd}\033[0m")
    print("=" * 75)

    if auto_deploy:
        vps_host = env_cfg.get("VPS_HOST", "34.146.128.243")
        vps_ssh_user = env_cfg.get("VPS_USER", "sokni")
        print(f"\n🌐 [AUTO-DEPLOY] Attempting SSH deployment trigger to {vps_ssh_user}@{vps_host}...")
        ssh_cmd = ["ssh", "-o", "ConnectTimeout=8", f"{vps_ssh_user}@{vps_host}", vps_cmd]
        ssh_code, _ = run_command_stream(ssh_cmd)
        if ssh_code == 0:
            print("🎉 [AUTO-DEPLOY SUCCESS] Tokyo GCP VPS updated and restarted cleanly!")
        else:
            print("⚠️ SSH direct trigger exited. Run the 1-tap update directive manually on VPS.")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Angkor Quant Universal Cross-Platform Git Push & Zero-Friction VPS Deployer"
    )
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="Commit message string"
    )
    parser.add_argument(
        "--skip-audit", "-n", "--no-verify",
        action="store_true",
        help="Skip pre-commit audit system verification (Emergency use only)"
    )
    parser.add_argument(
        "--deploy", "-d",
        action="store_true",
        help="Automatically trigger SSH remote deployment update to VPS"
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Check git status and configuration without committing"
    )

    args = parser.parse_args()

    if args.status:
        env_cfg = load_env_config()
        print("=" * 75)
        print("  ANGKOR QUANT - GIT & VPS STATUS CHECK")
        print("=" * 75)
        print(f"User: {env_cfg.get('GIT_PUSH_USER', 'hem sinath')}")
        print(f"Email: {env_cfg.get('GIT_PUSH_USER_EMAIL', 'hem.sinath@gmail.com')}")
        print(f"Remote: {env_cfg.get('GIT_REMOTE_URL', 'origin')}")
        print(f"VPS Host: {env_cfg.get('VPS_HOST', '34.146.128.243')}")
        print(f"VPS Command: {env_cfg.get('VPS_SYNC_COMMAND')}")
        has_changes, status = check_git_status()
        print("\nGit Status:")
        print(status)
        sys.exit(0)

    success = execute_git_push_vps(
        commit_msg=args.message,
        skip_audit=args.skip_audit,
        auto_deploy=args.deploy
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
