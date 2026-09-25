path = "ui_components.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines before extermination: {len(lines)}")

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Target the exact multi-line broken read_sql block around line 263
    if "pd.read_sql" in line and "theoretical_bets" in line:
        print(f"🎯 Neutralizing broken query starting at line {i+1}")
        new_lines.append('    df = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE \'SBOX%\'", conn)\n')
        # Skip subsequent fragment lines of the old broken query
        i += 1
        while i < len(lines):
            if ")" in lines[i] or "conn" in lines[i] or "def " in lines[i]:
                if "def " in lines[i]:
                    # Don't skip if we hit a new function definition
                    i -= 1
                break
            i += 1
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

content = "".join(new_lines)

# Built-in check system with automatic validation
compile(content, path, 'exec')
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ SUCCESS: Line 263 has been permanently exterminated and ui_components.py compiles cleanly!")
