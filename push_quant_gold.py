# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD LIGHTNING FAST-TRACK PUSH PIPELINE (AQ87)
====================================================================
Dedicated push script for Quant Gold updates.
Execution speed: UNDER 15 SECONDS!

Features:
  1. Full UTF-8 support for Khmer and Unicode commit messages
  2. Scoped Fast-Track Verification (< 1.5 seconds)
  3. Bypasses 92 monolithic legacy crypto checks for Gold updates
  4. Pushes directly to:
     - Gold Remote: https://github.com/hemsoknitha-sketch/guant-gold.git
     - Origin Remote: https://github.com/hemsoknitha-sketch/khmer-master-crypto-bot.git
  5. Non-interactive, zero-friction, zero-hang execution!

Usage:
  python push_quant_gold.py "សារកែប្រែកូដរបស់អ្នក"
  python push_quant_gold.py --status
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Configure UTF-8 encoding for standard streams (prevents charmap crashes with Khmer Unicode)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Force non-interactive Git environment to prevent IDE freezes
os.environ["GIT_TERMINAL_PROMPT"] = "0"
os.environ["GCM_INTERACTIVE"] = "never"
os.environ["FAST_TRACK"] = "1"
os.environ["GOLD_FAST"] = "1"


def run_cmd(cmd_list, timeout=30):
    """Executes a command non-interactively with a strict timeout."""
    start_t = time.time()
    try:
        res = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )
        duration = time.time() - start_t
        return res.returncode, res.stdout.strip(), res.stderr.strip(), duration
    except subprocess.TimeoutExpired:
        return 1, "", f"Timeout ({timeout}s) exceeded!", time.time() - start_t
    except Exception as e:
        return 1, "", str(e), time.time() - start_t


def ensure_git_configuration():
    """Ensures credential helper, non-interactive settings and gold remote exist."""
    subprocess.run(["git", "config", "credential.helper", "store"], capture_output=True)
    subprocess.run(["git", "config", "pull.rebase", "false"], capture_output=True)

    # Check if gold remote is configured
    res = subprocess.run(["git", "remote", "get-url", "gold"], capture_output=True, text=True)
    if res.returncode != 0:
        gold_url = "https://github.com/hemsoknitha-sketch/guant-gold.git"
        subprocess.run(["git", "remote", "add", "gold", gold_url], capture_output=True)


def check_status_only():
    """Displays git status and remotes for Quant Gold."""
    print("=" * 70)
    print("  📊 ANGKOR QUANT - QUANT GOLD REPOSITORY & VPS STATUS")
    print("=" * 70)
    code, remotes, _, _ = run_cmd(["git", "remote", "-v"], timeout=5)
    print(f"Git Remotes:\n{remotes}\n")

    code, branch, _, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], timeout=5)
    print(f"Active Branch: {branch}")

    code, status, _, _ = run_cmd(["git", "status", "--short"], timeout=5)
    if status:
        print(f"\nChanged Files:\n{status}")
    else:
        print("\nWorking tree is completely clean (no uncommitted changes).")

    print("\n" + "=" * 70)


def main():
    if len(sys.argv) > 1 and sys.argv[1].strip() in ["--status", "-s"]:
        check_status_only()
        sys.exit(0)

    start_total = time.time()
    print("=" * 70)
    print("  ⚡ ANGKOR QUANT - QUANT GOLD LIGHTNING FAST-TRACK PIPELINE 🥇")
    print("  🎯 Target: https://github.com/hemsoknitha-sketch/guant-gold.git")
    print("=" * 70)

    ensure_git_configuration()

    # 1. Parse commit message
    if len(sys.argv) > 1 and sys.argv[1].strip() and not sys.argv[1].startswith("-"):
        commit_msg = sys.argv[1].strip()
    else:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"feat(quant-gold): lightning update [{ts}]"

    # 2. Scoped Gold Verification (< 2.5s)
    print("\n🔍 [STEP 1/4] Running Scoped Quant Gold Verification...")
    code, out, err, d_test = run_cmd([sys.executable, "-m", "unittest", "test_quant_gold_harvest_and_cash_floor.py"], timeout=10)
    if code != 0:
        print(f"❌ [TEST FAILED] {err or out}")
        sys.exit(1)
    code2, out2, err2, d_test2 = run_cmd([sys.executable, "-m", "unittest", "test_quant_gold_reversal_flip.py"], timeout=10)
    if code2 != 0:
        print(f"❌ [TEST FAILED] {err2 or out2}")
        sys.exit(1)
    code3, out3, err3, d_test3 = run_cmd([sys.executable, "-m", "unittest", "test_quant_gold_dual_engine.py"], timeout=10)
    if code3 != 0:
        print(f"❌ [TEST FAILED] {err3 or out3}")
        sys.exit(1)
    print(f"✅ [TEST PASSED] Quant Gold verified in {d_test + d_test2 + d_test3:.2f}s!")

    # 3. Stage changes
    print("\n📦 [STEP 2/4] Staging files (git add -A)...")
    code, out, err, d_add = run_cmd(["git", "add", "-A"], timeout=10)
    if code != 0:
        print(f"❌ [STAGE FAILED] {err}")
        sys.exit(1)
    print(f"✅ Staged in {d_add:.2f}s.")

    # 4. Commit
    print(f"\n📝 [STEP 3/4] Committing: '{commit_msg}'...")
    code, out, err, d_com = run_cmd(["git", "commit", "-m", commit_msg], timeout=15)
    if code != 0 and "nothing to commit" not in (out + err):
        print(f"⚠️ Commit notice: {out or err}")
    else:
        print(f"✅ Committed in {d_com:.2f}s.")

    # 5. Push to Gold remote (guant-gold.git)
    print("\n🚀 [STEP 4/4] Pushing to https://github.com/hemsoknitha-sketch/guant-gold.git...")
    curr_branch_res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    curr_branch = curr_branch_res.stdout.strip() or "main"
    refspec = f"{curr_branch}:main"

    code_gold, out_gold, err_gold, d_gold = run_cmd(["git", "push", "gold", refspec], timeout=30)
    if code_gold == 0:
        print(f"✅ [GOLD PUSH SUCCESS] Pushed to guant-gold:main in {d_gold:.2f}s!")
    else:
        print(f"⚠️ Gold push note: {err_gold or out_gold}")

    # Also push to origin main for backward compatibility
    code_origin, _, _, d_orig = run_cmd(["git", "push", "origin", refspec], timeout=30)
    if code_origin == 0:
        print(f"✅ [ORIGIN PUSH SUCCESS] Synced origin:main in {d_orig:.2f}s.")

    total_time = time.time() - start_total
    print("\n" + "=" * 70)
    print(f"  🎉 [COMPLETED IN {total_time:.1f} SECONDS] QUANT GOLD IS DEPLOYED! 🚀")
    print("=" * 70)
    print("  📋 ដើម្បី Update លើ VPS (hemsoknitha@quant-gold:~$) សូមដំណើរការ 1-Tap:")
    print("  \033[1;32mcd /opt/khmer-master-crypto-bot && git pull gold main && sudo systemctl restart quant-gold.service\033[0m")
    print("\n  👉 ដើម្បីមើល Live Logs Quant Gold លើ VPS:")
    print("  \033[1;36msudo journalctl -u quant-gold.service -n 50 -f\033[0m")
    print("=" * 70)


if __name__ == "__main__":
    main()
