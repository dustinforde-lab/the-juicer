import os
import sys
import shutil
import ast
import json
import py_compile
from datetime import datetime

BACKUP_DIR = ".deploy_backups"
MANIFEST_FILE = "approved_manifest.json"
os.makedirs(BACKUP_DIR, exist_ok=True)

def register_in_manifest(filename):
    if not os.path.exists(MANIFEST_FILE):
        return
    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        if filename not in data.get("approved_root_files", []):
            data["approved_root_files"].append(filename)
            with open(MANIFEST_FILE, "w", encoding="utf-8-sig") as f:
                json.dump(data, f, indent=2)
            print(f"  📋 Added '{filename}' to approved_manifest.json")
    except Exception as e:
        print(f"  ⚠️ Manifest update note: {e}")

def preflight_test(source_file):
    print(f"🔍 Testing {source_file} before deployment...")
    with open(source_file, "r", encoding="utf-8-sig") as f:
        code = f.read()
    try:
        ast.parse(code)
        print("  ✅ [PASS] Syntax verification passed.")
    except SyntaxError as e:
        print(f"  ❌ [FAIL] Syntax error at line {e.lineno}: {e.msg}")
        return False
        
    try:
        py_compile.compile(source_file, doraise=True)
        print("  ✅ [PASS] Bytecode compilation passed.")
    except Exception as e:
        print(f"  ❌ [FAIL] Compilation error: {e}")
        return False
        
    return True

def deploy(staged_file, target_file):
    if not os.path.exists(staged_file):
        print(f"❌ Staged file '{staged_file}' not found.")
        return False

    if not preflight_test(staged_file):
        print("\n🚫 DEPLOYMENT ABORTED: Failed pre-flight test. Root files untouched.")
        return False

    target_name = os.path.basename(target_file)

    if os.path.exists(target_file):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{target_name}_{ts}.bak"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        shutil.copy2(target_file, backup_path)
        print(f"  📦 Snapshot saved to: {backup_path}")

        latest_pointer = os.path.join(BACKUP_DIR, f"{target_name}.latest")
        shutil.copy2(target_file, latest_pointer)

    shutil.copy2(staged_file, target_file)
    print(f"  🚀 SUCCESS: '{target_file}' is live in working directory.")
    
    register_in_manifest(target_name)
    os.remove(staged_file)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python deploy_update.py <staged_patch_file.py> <production_target_file.py>")
        sys.exit(1)
        
    deploy(sys.argv[1], sys.argv[2])

