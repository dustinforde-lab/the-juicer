import shutil

ui_path = "ui_components.py"
shutil.copy(ui_path, "ui_components_clean_backup.py")

with open(ui_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Filter out naked HTML/CSS lines at the top if they exist in lines 0-6
cleaned_lines = []
for i, line in enumerate(lines):
    if i < 6 and ("<style>" in line or "</style>" in line or ".dfs-card" in line):
        continue  # Skip the naked CSS block
    cleaned_lines.append(line)

new_content = "".join(cleaned_lines)

# Verify compilation
try:
    compile(new_content, ui_path, 'exec')
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ SUCCESS: Rogue top-level CSS removed. File compiles cleanly!")
except Exception as e:
    print(f"❌ Compilation Error: {e}")
    shutil.copy("ui_components_clean_backup.py", ui_path)
    print("⚠️ Reverted safely.")
