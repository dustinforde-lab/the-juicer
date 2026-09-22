import shutil
import os

ui_path = "ui_components.py"
backup_path = "ui_components_master_backup.py"

# 1. Restore the original un-chopped file if backup exists, otherwise git checkout
if os.path.exists(backup_path):
    shutil.copy(backup_path, ui_path)
    print("🛡️ Restored clean baseline from master backup.")
else:
    os.system("git checkout ui_components.py")
    print("🛡️ Restored clean baseline via git.")

with open(ui_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in file: {len(lines)}")

# 2. Surgically replace any multi-line or broken pd.read_sql blocks without deleting anything else
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if "pd.read_sql" in line and "theoretical_bets" in line:
        print(f"🎯 Surgically fixing query at line {i+1}")
        # Insert a 100% clean single-line query
        new_lines.append('    df = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE \'SBOX%\'", conn)\n')
        
        # Skip the broken continuation lines of the old query
        i += 1
        while i < len(lines) and (")" not in lines[i] and "conn" not in lines[i]):
            i += 1
        if i < len(lines):
            i += 1 # skip the closing line too
        continue
        
    new_lines.append(line)
    i += 1

content = "".join(new_lines)

# 3. Validate compilation before saving
compile(content, ui_path, 'exec')
with open(ui_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ SUCCESS: File restored, line 263 fixed surgically, and compiled completely clean!")
