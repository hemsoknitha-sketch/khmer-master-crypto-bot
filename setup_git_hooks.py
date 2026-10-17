#!/usr/bin/env python
"""
Khmer Master Crypto - Pre-Commit Invariant Gate Setup
=====================================================
Installs an automated pre-commit hook in .git/hooks/pre-commit
that forces 'python audit_system.py' to run before any commit.
If any of the 19 Invariants fail, the commit is strictly blocked!
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def setup():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    hook_dir = os.path.join(base_dir, ".git", "hooks")
    hook_path = os.path.join(hook_dir, "pre-commit")
    post_hook_path = os.path.join(hook_dir, "post-commit")
    
    if not os.path.exists(hook_dir):
        print(f"⚠️ Git hook directory not found at: {hook_dir}")
        return False
        
    hook_content = """#!/bin/sh
# Angkor Quant - Institutional Pre-Commit Invariant Gate
echo "🛡️ Running Institutional System Audit before commit..."
python audit_system.py
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ [PRE-COMMIT BLOCKED] System Audit failed! Commit aborted to prevent technical negligence."
    exit 1
fi
echo "✅ [PRE-COMMIT PASSED] 100% Invariants verified. Proceeding with commit."
exit 0
"""

    post_hook_content = """#!/bin/sh
# Angkor Quant - Institutional Auto-Push to GitHub Origin Main
echo "🚀 [POST-COMMIT] Auto-pushing certified commit to GitHub origin main..."
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
if [ "$BRANCH" = "main" ]; then
    git push origin main
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ [POST-COMMIT] Successfully pushed to GitHub origin main!"
    else
        echo "⚠️ [POST-COMMIT] git push exited with code $EXIT_CODE. Please verify internet connectivity."
    fi
fi
exit 0
"""
    try:
        with open(hook_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(hook_content)
        try:
            os.chmod(hook_path, 0o755)
        except Exception:
            pass
        print(f"✅ [SUCCESS] Institutional Pre-Commit Hook installed at: {hook_path}")

        with open(post_hook_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(post_hook_content)
        try:
            os.chmod(post_hook_path, 0o755)
        except Exception:
            pass
        print(f"✅ [SUCCESS] Institutional Post-Commit Auto-Push Hook installed at: {post_hook_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to install git hook: {e}")
        return False

if __name__ == "__main__":
    setup()

