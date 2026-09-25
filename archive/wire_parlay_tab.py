import os
import shutil

app_path = "app.py"
backup_path = "app_parlay_fix_backup.py"

shutil.copy(app_path, backup_path)
print("🛡️ Safety backup created.")

with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip_mode = False
replaced = False

for i, line in enumerate(lines):
    # Target the parlay matrix section header or card rendering call
    if "THE PARLAY MATRIX" in line or "render_stamped_parlay_card" in line:
        if not replaced:
            new_lines.append("    # --- REPLACED WITH REAL-BOOK PARLAY MATRIX ---\n")
            new_lines.append("    render_real_parlay_matrix(conn)\n")
            replaced = True
        skip_mode = True
        continue
    
    # Skip stale rendering loop lines until the next tab or major section
    if skip_mode:
        if "st.tab" in line or "Season-Long Fantasy" in line or "Film Room" in line or "Vegas Scoreboard" in line or "DFS Optimizer" in line:
            skip_mode = False
            new_lines.append(line)
        continue
        
    new_lines.append(line)

code = "".join(new_lines)

# Built-in check system with automatic rollback
try:
    compile(code, app_path, 'exec')
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ SUCCESS: app.py successfully wired to render_real_parlay_matrix(conn) and compiled cleanly!")
except Exception as e:
    print(f"❌ Compilation Error: {e}")
    shutil.copy(backup_path, app_path)
    print("⚠️ Restored app.py safely from backup.")
