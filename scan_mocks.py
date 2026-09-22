import os
import glob

print("\n" + "="*65)
print(" 🔍 SCANNING WORKSPACE FOR BACKGROUND MOCK GENERATORS")
print("="*65)

# Find all python files in the workspace that might contain mock or tracer generators
py_files = glob.glob("*.py")
found_mocks = []

for file in py_files:
    if file in ["app.py", "ui_addresses.py", "tracer_eradicator.py", "pipeline_sync.py"]:
        continue
        
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            if "TRACER" in content or "TEST" in content or "mock" in content.lower():
                found_mocks.append(file)
                print(f"  ⚠️ Identified potential background generator: {file}")
                
                # Neutralize the mock generator by renaming or disabling its auto-execution block
                backup_name = file + ".bak"
                if not os.path.exists(backup_name):
                    os.rename(file, backup_name)
                    print(f"  🔒 Neutralized and backed up: {file} -> {backup_name}")
    except Exception as e:
        print(f"  Skipped {file}: {e}")

if not found_mocks:
    print("  ℹ️ No external mock generator scripts found. The source is likely embedded directly in database initialization.")

print("\n" + "="*65)
print(" ✅ BACKGROUND SCAN COMPLETE. RUNNING CLEAN RE-SEED.")
print("="*65 + "\n")