import os
import re
import shutil

print("=" * 65)
print("💉 [PHASE 2] Surgically Injecting Film Room Tab...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
    exit(1)

# 1. Take a Pre-Flight Backup
shutil.copyfile("app.py", "app_backup_pre_filmroom.py")
print("   ✅ Pre-flight backup created: app_backup_pre_filmroom.py")

with open("app.py", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 2. Safely locate and replace the tab definition using regex
pattern = r'(t1,\s*t2,\s*t3,\s*t4,\s*t5,\s*t6\s*=\s*st\.tabs\(\[.*?\]\))'
replacement = 't1, t2, t3, t4, t5, t6, t7 = st.tabs(["🏆 Vegas Scoreboard", "👑 DFS Optimizer", "📊 Classy Rankings", "🎯 Parlay Matrix", "🏈 Season-Long Fantasy", "⚡ PrizePicks & Underdog", "📡 Film Room"])'

if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
    print("   ✅ Tab list safely expanded to include t7 (Film Room).")
else:
    print("   ❌ Error: Could not find exact tab definition. Aborting to protect app.py.")
    exit(1)

# 3. Append the rendering logic for t7 at the bottom of the file
t7_block = """

# --- 📡 INJECTED FILM ROOM TELEMETRY ---
try:
    with t7:
        import ui_film_room
        ui_film_room.render_live_telemetry("action_grid.db")
except Exception as e:
    pass  # Fail silently to prevent crashing the main app
"""

if "with t7:" not in content:
    content += t7_block
    print("   ✅ Film Room rendering block successfully attached to t7.")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("=" * 65)
print("🟢 INJECTION COMPLETE: app.py successfully upgraded.")
print("=" * 65)
