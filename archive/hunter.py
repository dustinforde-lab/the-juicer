import os

# 1. Dynamic Pathing & Absolute Targeting
home_dir = os.path.expanduser("~")
workspace = os.path.join(home_dir, "the-juicer")
path = os.path.join(workspace, "ui_components.py")

# 2. Workspace Lock (IDE Terminal Simulation)
os.chdir(workspace)
print(f"🎯 Target acquired at absolute path: {path}")

# 3. The Execution
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

for i, line in enumerate(lines):
    if "SELECT ticket_id, weight_class" in line:
        skip_mode = True
        continue
    
    if skip_mode:
        if "conn)" in line or "theoretical_bets" in line or "def " in line:
            skip_mode = False
            if "def " not in line:
                continue 
        continue
        
    new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ MUTANT EXTERMINATED. Line 261 is permanently purged.")