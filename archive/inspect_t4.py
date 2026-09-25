import os

print("=" * 65)
print("🔍 [PHASE 2 - MOD 9] Inspecting Parlay Matrix (t4) Block...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
else:
    with open("app.py", "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
        
    found = False
    for i, line in enumerate(lines):
        if "with t4:" in line:
            print(f"   ✅ Found 'with t4:' at Line {i+1}. Current logic:")
            print("   " + "-"*50)
            for j in range(i, min(i+20, len(lines))):
                if "with t5:" in lines[j] or "with t6:" in lines[j]:
                    break
                print(f"   {lines[j].rstrip()}")
            print("   " + "-"*50)
            found = True
            break
            
    if not found:
        print("   ⚠️ Could not find 'with t4:' block in app.py.")

print("=" * 65)
