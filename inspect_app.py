with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("🔍 Scanning app.py for Parlay Matrix references...")
for i, line in enumerate(lines):
    if "parlay" in line.lower() or "matrix" in line.lower() or "slip" in line.lower():
        print(f"Line {i+1}: {line.strip()}")
