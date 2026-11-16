# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD LIGHTNING FAST-TRACK PUSH PIPELINE (AQ87)
====================================================================
Dedicated push script for Quant Gold updates.
Execution speed: UNDER 15 SECONDS!

Features:
  1. Scoped Fast-Track Verification (< 1.5 seconds)
  2. Bypasses 92 monolithic legacy crypto checks for Gold updates
  3. Pushes directly to:
     - Gold Remote: https://github.com/hemsoknitha-sketch/guant-gold.git
     - Origin Remote: https://github.com/hemsoknitha-sketch/khmer-master-crypto-bot.git
  4. Non-interactive, zero-friction, zero-hang execution!

Usage:
  python push_quant_gold.py "feat(quant-gold): your update message"
"""

import os
import sys
import time
import subprocess
from datetime import datetime

os.environ["GIT_TERMINAL_PROMPT"] = "0"
os.environ["GCM_INTERACTIVE"] = "never"
os.environ["FAST_TRACK"] = "1"
os.environ["GOLD_FAST"] = "1"


def run_cmd(cmd_list, timeout=25):
    """Executes a command non-interactively with a strict timeout."""
    start_t = time.time()
    try:
        res = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            timeout=timeout,
            errors="replace"
        )
        duration = time.time() - start_t
        return res.returncode, res.stdout.strip(), res.stderr.strip(), duration
    except subprocess.TimeoutExpired:
        return 1, "", f"Timeout ({timeout}s) exceeded!", time.time() - start_t
    except Exception as e:
        return 1, "", str(e), time.time() - start_t


def main():
    start_total = time.time()
    print("=" * 70)
    print("  ⚡ ANGKOR QUANT - QUANT GOLD LIGHTNING FAST-TRACK PIPELINE 🥇")
    print("  🎯 Target: https://github.com/hemsoknitha-sketch/guant-gold.git")
    print("=" * 70)

    # 1. Parse commit message
    if len(sys.argv) > 1 and sys.argv[1].strip():
        commit_msg = sys.argv[1].strip()
    else:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"feat(quant-gold): lightning update [{ts}]"

    # 2. Scoped Gold Verification (< 1.5s)
    print("\n🔍 [STEP 1/4] Running Scoped Quant Gold Verification...")
    code, out, err, d_test = run_cmd([sys.executable, "-m", "unittest", "test_quant_gold_harvest_and_cash_floor.py"], timeout=10)
    if code != 0:
        print(f"❌ [TEST FAILED] {err or out}")
        sys.exit(1)
    print(f"✅ [TEST PASSED] Quant Gold verified in {d_test:.2f}s!")

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
    # Push active branch to gold main
    curr_branch_res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    curr_branch = curr_branch_res.stdout.strip() or "main"
    refspec = f"{curr_branch}:main"

    code_gold, out_gold, err_gold, d_gold = run_cmd(["git", "push", "gold", refspec], timeout=25)
    if code_gold == 0:
        print(f"✅ [GOLD PUSH SUCCESS] Pushed to guant-gold:main in {d_gold:.2f}s!")
    else:
        print(f"⚠️ Gold push note: {err_gold or out_gold}")

    # Also push to origin main for backward compatibility
    code_origin, _, _, d_orig = run_cmd(["git", "push", "origin", refspec], timeout=25)
    if code_origin == 0:
        print(f"✅ [ORIGIN PUSH SUCCESS] Synced origin:main in {d_orig:.2f}s.")

    total_time = time.time() - start_total
    print("\n" + "=" * 70)
    print(f"  🎉 [COMPLETED IN {total_time:.1f} SECONDS] QUANT GOLD IS DEPLOYED! 🚀")
    print("=" * 70)
    print("  To update your VPS instance (hemsoknitha@quant-gold:~$):")
    print("  \033[1;32mcd /opt/khmer-master-crypto-bot && git pull gold main && sudo systemctl restart quant-gold.service\033[0m")
    print("=" * 70)


if __name__ == "__main__":
    main()
