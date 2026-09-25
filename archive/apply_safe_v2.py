import os
import shutil

ui_path = "ui_components.py"
shutil.copy(ui_path, "ui_components_backup.py")

with open(ui_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Normalize line 2 leading whitespace if it has a stray indent
if len(lines) > 1:
    lines[1] = lines[1].lstrip()

patch_block = """

# --- THE JUICER: POSITION & PROP ICONS ---
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
"""

new_content = "".join(lines) + patch_block

try:
    compile(new_content, ui_path, 'exec')
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ SUCCESS: UI components patched and verified with zero indentation errors!")
except Exception as e:
    print(f"❌ Error: {e}")
    shutil.copy("ui_components_backup.py", ui_path)
    print("⚠️ Reverted back safely.")
