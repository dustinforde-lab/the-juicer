import os
import shutil

app_path = "app.py"
backup_path = "app_master_backup.py"

if not os.path.exists(app_path):
    print("❌ Error: app.py not found.")
    exit(1)

shutil.copy(app_path, backup_path)
print("🛡️ Safety backup of app.py created.")

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Search for where parlay matrix is rendered in app.py and update it to call our new function
updated = False
if "render_real_parlay_matrix" not in content:
    # Look for common tab or section names for parlay matrix
    for target in ["parlay_matrix", "Parlay Matrix", "render_parlay_card"]:
        if target in content:
            print(f"🔍 Found reference to '{target}' in app.py.")
            
# Let's replace any legacy parlay matrix display block with a clean call to render_real_parlay_matrix(conn)
# We will scan for lines displaying parlay tabs and ensure they invoke our real-book function.
lines = content.splitlines()
new_lines = []
for line in lines:
    if "render_parlay" in line and "render_real_parlay_matrix" not in line:
        # Swap legacy call with the real-book matrix renderer
        new_lines.append("    # --- UPDATED TO REAL-BOOK FEED ---")
        new_lines.append("    render_real_parlay_matrix(conn)")
        updated = True
    else:
        new_lines.append(line)

new_content = "\n".join(new_lines) + "\n"

try:
    compile(new_content, app_path, 'exec')
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ SUCCESS: app.py wired to render_real_parlay_matrix(conn) and compiled cleanly!")
except Exception as e:
    print(f"❌ Compilation Error: {e}")
    shutil.copy(backup_path, app_path)
    print("⚠️ Reverted app.py safely to backup.")
