import os
import ast
import sys

repo_dir = r"e:\AI CODE PYTHON\Khmer Master Crypto\khmer-master-crypto-bot"
sys.path.insert(0, repo_dir)

import database as db

db_attrs = set(dir(db))

print(f"Total attributes in database.py: {len(db_attrs)}")

missing_by_file = {}

for root, _, files in os.walk(repo_dir):
    if "venv" in root or ".git" in root or "__pycache__" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, repo_dir)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                tree = ast.parse(content, filename=filepath)
            except Exception as e:
                print(f"Error parsing {relpath}: {e}")
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    # Check if value is named 'db' or 'database'
                    if isinstance(node.value, ast.Name) and node.value.id in ["db", "database"]:
                        attr = node.attr
                        if attr not in db_attrs:
                            if relpath not in missing_by_file:
                                missing_by_file[relpath] = set()
                            missing_by_file[relpath].add((node.lineno, attr))

print("\n--- AUDIT RESULTS FOR db.<attr> ---")
if not missing_by_file:
    print("[PASS] All db.<attr> calls across all files exist in database.py!")
else:
    for relpath, missing in missing_by_file.items():
        print(f"\nFile: {relpath}")
        for lineno, attr in sorted(missing):
            print(f"  Line {lineno}: db.{attr} NOT FOUND in database.py")
