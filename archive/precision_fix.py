path = "ui_components.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in file: {len(lines)}")

new_lines = []
i = 0
fixed = False

while i < len(lines):
    line = lines[i]
    # Look for the broken pandas sql read block
    if "pd.read_sql" in line and "theoretical_bets" in line:
        print(f"🎯 Smashed broken query at line {i+1}")
        # Inject a 100% clean, single-line SQL read statement
        new_lines.append('    df = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE \'SBOX%\'", conn)\n')
        
        # Consume/skip all broken continuation lines until the closing parenthesis and connection variable
        i += 1
        while i < len(lines):
            current_line = lines[i]
            if ")" in current_line or "conn" in current_line:
                i += 1
                break
            i += 1
        fixed = True
        continue
        
    new_lines.append(line)
    i += 1

content = "".join(new_lines)

# Strict compilation check to guarantee no syntax errors remain
compile(content, path, 'exec')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

if fixed:
    print("✅ SUCCESS: Line 263 successfully neutralized and compiled clean!")
else:
    print("⚠️ Warning: Target line pattern not matched, check line numbers.")
