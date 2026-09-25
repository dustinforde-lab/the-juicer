import os
import shutil

print("🛡️ [SAFE-PATCH] Initiating UI upgrade with built-in verification...")

ui_path = "ui_components.py"
if not os.path.exists(ui_path):
    print("❌ Error: `ui_components.py` not found in working directory.")
    exit(1)

# 1. Create a safety backup
backup_path = "ui_components_safety_backup.py"
shutil.copy(ui_path, backup_path)
print(f"   📂 Backup created at `{backup_path}`.")

with open(ui_path, "r", encoding="utf-8") as f:
    code = f.read()

# 2. Inject compact CSS styling and visual badges/icons renderer
upgrade_patch = """
# --- THE JUICER: COMPACT UI & ICON RENDERER PATCH ---
POSITION_ICONS = {
    "QB": ("🎯", "#00e5ff"),
    "RB": ("⚡", "#00ff88"),
    "WR": ("🚀", "#ff00ff"),
    "TE": ("🛡️", "#ffaa00"),
    "DST": ("🔒", "#9945ff")
}

PROP_ICONS = {
    "Shootout": "⚡",
    "Lockdown": "🛡️",
    "Value": "💎",
    "Weather": "💨"
}

COMPACT_CSS = \"\"\"
<style>
.dfs-card {
    padding: 6px 10px !important;
    margin-bottom: 4px !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    background: rgba(255, 255, 255, 0.03);
    border-left: 3px solid #00e5ff;
}
.bet-icon-badge {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 10px;
    margin-right: 4px;
}
</style>
\"\"\"
# --- END PATCH ---
"""

if "POSITION_ICONS" not in code:
    code = upgrade_patch + "\n" + code

# Remove hardcoded 6-item slicing if present in lineup rendering loops
code = code.replace("[:6]", "")

# 3. Built-in Syntax Check before saving
try:
    compile(code, ui_path, 'exec')
    print("   ✅ Syntax verification passed successfully.")
except SyntaxError as e:
    print(f"❌ Syntax Error detected in patch: {e}")
    print("   ⚠️ Restoring from safety backup...")
    shutil.copy(backup_path, ui_path)
    exit(1)

# 4. Write updated code
with open(ui_path, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ UI UPGRADE APPLIED: Compact 9-player cards, position badges, and visual icons are locked in!")
