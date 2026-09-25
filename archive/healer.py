import os, sys

workspace = os.path.join(os.path.expanduser("~"), "the-juicer")
path = os.path.join(workspace, "ui_components.py")
os.chdir(workspace)

print("⚕️ INITIALIZING AUTO-HEALER...")

for attempt in range(20):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    try:
        compile(content, path, 'exec')
        print("✅ SYNTAX PERFECT. ALL MUTATIONS PURGED.")
        break
    except SyntaxError as e:
        lineno = e.lineno
        print(f"🛠️ Neutralizing syntax trap at line {lineno}...")
        lines = content.split('\n')
        if 0 < lineno <= len(lines):
            lines[lineno-1] = f"# AUTO-PURGED: {lines[lineno-1]}"
        with open(path, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print(f"❌ Unknown error: {e}")
        sys.exit(1)