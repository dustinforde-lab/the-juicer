import os
import shutil

print("🛡️ [SAFE-PATCH] Applying clean UI component patch...")

ui_path = "ui_components.py"
backup_path = "ui_components_safety_backup.py"

if os.path.exists(backup_path):
    shutil.copy(backup_path, ui_path)

with open(ui_path, "r", encoding="utf-8") as f:
    code = f.read()

# Remove any previous incomplete patch attempts if present
if "# --- THE JUICER: COMPACT UI & ICON RENDERER PATCH ---" in code:
    code = code.split("# --- THE JUICER: COMPACT UI & ICON RENDERER PATCH ---")[0]

# Clean, safe code block to append at the bottom or top level
patch_code = """

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
</style>
\"\"\"
# --- END PATCH ---
"""

full_code = code + patch_code

# Built-in syntax check
try:
    compile(full_code, ui_path, 'exec')
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(full_code)
    print("✅ PATCH SUCCESSFUL: UI upgraded with zero indentation errors!")
except SyntaxError as e:
    print(f"❌ Syntax Error caught: {e}")
    print("⚠️ Reverted safely to original state.")
