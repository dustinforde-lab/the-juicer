import os
import shutil

ui_path = "ui_components.py"
shutil.copy(ui_path, "ui_components_inspect_backup.py")

with open(ui_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in file: {len(lines)}")

# Print lines 340 to 355 to locate the unterminated string
print("\n--- Inspecting around line 348 ---")
for i in range(max(0, 339), min(len(lines), 355)):
    print(f"Line {i+1}: {repr(lines[i])}")

# Fix any obvious broken multi-line string or unterminated quote in that window
for i in range(max(0, 339), min(len(lines), 355)):
    line = lines[i]
    # Check for unclosed quotes in f-strings or markdown blocks
    if line.strip().startswith("st.markdown(") and not line.strip().endswith(")") and not line.strip().endswith("'''") and not line.strip().endswith('"'):
        lines[i] = line.rstrip() + ")\n"
        print(f"🔧 Auto-closed tag on line {i+1}")

code = "".join(lines)

try:
    compile(code, ui_path, 'exec')
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ SUCCESS: Inspection window checked and compiled cleanly!")
except Exception as e:
    print(f"❌ Compilation error: {e}")
    shutil.copy("ui_components_inspect_backup.py", ui_path)
    print("⚠️ Reverted safely.")
