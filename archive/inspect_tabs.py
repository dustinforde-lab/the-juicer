import os

print("=" * 65)
print("🔍 [PHASE 2] Inspecting app.py Tab Structure...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
else:
    with open("app.py", "r", encoding="utf-8-sig", errors="ignore") as f:
        lines = f.readlines()
        
    found_tabs = False
    for i, line in enumerate(lines):
        if "st.tabs([" in line:
            print(f"   ✅ Found Tab Definition at Line {i+1}:")
            print(f"      {line.strip()}")
            found_tabs = True
            
    if not found_tabs:
        print("   ⚠️ Could not find exact 'st.tabs' definition. Using dynamic injection.")

print("=" * 65)
