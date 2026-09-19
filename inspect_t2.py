import os

print("=" * 65)
print("🔍 [PHASE 2 - MOD 10] Inspecting DFS Optimizer (t2) Block...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
else:
    with open("app.py", "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
        
    found = False
    for i, line in enumerate(lines):
        if "with t2:" in line:
            print(f"   ✅ Found 'with t2:' at Line {i+1}. Current logic:")
            print("   " + "-"*50)
            for j in range(i, min(i+20, len(lines))):
                if "with t3:" in lines[j] or "with t4:" in lines[j]:
                    break
                print(f"   {lines[j].rstrip()}")
            print("   " + "-"*50)
            found = True
            break
            
    if not found:
        print("   ⚠️ Could not find 'with t2:' block in app.py.")

print("=" * 65)
