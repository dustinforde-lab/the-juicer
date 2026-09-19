import os
import shutil
import py_compile

print("=" * 65)
print("💉 [PHASE 2 - MOD 10] Boundary-Target Injection (t2)...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
    exit(1)

# 1. Take a fresh pre-flight backup
shutil.copyfile("app.py", "app_backup_pre_t2.py")
print("   ✅ Pre-flight backup created: app_backup_pre_t2.py")

with open("app.py", "r", encoding="utf-8-sig", errors="ignore") as f:
    lines = f.readlines()

t2_idx = None
t3_idx = None

for i, line in enumerate(lines):
    if "with t2:" in line and t2_idx is None:
        t2_idx = i
    elif "with t3:" in line and t2_idx is not None and t3_idx is None:
        t3_idx = i
        break

if t2_idx is None or t3_idx is None:
    print(f"❌ Error: Could not boundary t2 (idx={t2_idx}) and t3 (idx={t3_idx}). Aborting.")
    exit(1)

print(f"   ✅ Identified t2 boundaries: Line {t2_idx + 1} to Line {t3_idx}")

# Detect base indentation
base_line = lines[t2_idx]
indent = base_line[:len(base_line) - len(base_line.lstrip())]
pad = indent + "    "
pad2 = pad + "    "
pad3 = pad2 + "    "

orig_body = "".join(lines[t2_idx + 1 : t3_idx])

# Build the enhanced t2 block preserving existing call
t2_replacement = (
    base_line
    + pad + "import pandas as pd\n"
    + pad + "st.markdown(\"<h3 style='color:#00e5ff;'>👑 DFS OPTIMIZER & SOLVENCY ENGINE</h3>\", unsafe_allow_html=True)\n"
    + pad + "try:\n"
    + pad2 + "conn = q_db() if callable(q_db) else q_db\n"
    + pad2 + "df_donna = pd.read_sql(\"SELECT player_name, team, projected_ownership, vibe_rating, updated_at FROM ownership_projections ORDER BY updated_at DESC\", conn)\n"
    + pad2 + "if not df_donna.empty:\n"
    + pad3 + "st.markdown(\"<h5 style='color:#8b949e;'>Donna's Leverage Matrix</h5>\", unsafe_allow_html=True)\n"
    + pad3 + "for _, row in df_donna.iterrows():\n"
    + pad3 + "    vibe_color = '#ff2a6d' if row['vibe_rating'] == 'FADE' else '#00ff88'\n"
    + pad3 + "    card = f'''\n"
    + pad3 + "    <div style=\"background: #121824; border-left: 4px solid {vibe_color}; padding: 12px; margin-bottom: 8px; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);\">\n"
    + pad3 + "        <div style=\"display: flex; justify-content: space-between;\">\n"
    + pad3 + "            <span style=\"color: #e6edf3; font-weight: 800;\">{row['player_name']} <span style=\"color:#8b949e; font-size:0.85rem;\">({row['team']})</span></span>\n"
    + pad3 + "            <span style=\"color: {vibe_color}; font-weight: 900; letter-spacing: 1px;\">{row['vibe_rating']}</span>\n"
    + pad3 + "        </div>\n"
    + pad3 + "        <div style=\"display: flex; justify-content: space-between; margin-top: 6px;\">\n"
    + pad3 + "            <span style=\"color: #8b949e; font-size: 0.85rem; font-weight: 600;\">Proj Own: {row['projected_ownership']}</span>\n"
    + pad3 + "            <span style=\"color: #6e7681; font-size: 0.75rem; font-family: monospace;\">🕒 LINE LOCKED: {row['updated_at']}</span>\n"
    + pad3 + "        </div>\n"
    + pad3 + "    </div>\n"
    + pad3 + "    '''\n"
    + pad3 + "    st.markdown(card, unsafe_allow_html=True)\n"
    + pad3 + "st.markdown('<br>', unsafe_allow_html=True)\n"
    + pad2 + "else:\n"
    + pad3 + "st.caption('Awaiting Donna\\'s DFS vibe checks...')\n"
    + pad + "except Exception as e:\n"
    + pad2 + "st.error(f'DFS Engine Offline: {e}')\n\n"
    + orig_body
)

# Apply modification
updated_lines = lines[:t2_idx] + [t2_replacement] + lines[t3_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(updated_lines)

# Compile to guarantee clean syntax
try:
    py_compile.compile("app.py", doraise=True)
    print("   ✅ app.py compiled with zero syntax or indentation errors.")
    print("=" * 65)
    print("🟢 INJECTION COMPLETE: DFS Optimizer (t2) successfully upgraded.")
    print("=" * 65)
except Exception as err:
    print(f"❌ Syntax validation failed: {err}. Rolling back...")
    shutil.copyfile("app_backup_pre_t2.py", "app.py")
