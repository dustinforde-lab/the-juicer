path = "ui_components.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines before purge: {len(lines)}")

# Rebuild lines, filtering out the broken multi-line read_sql block around line 263
new_lines = []
skip = False
for i, line in enumerate(lines):
    # If we hit the broken query block start, replace it with a clean single line and skip fragment lines
    if "pd.read_sql" in line and "theoretical_bets" in line:
        new_lines.append('    df = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE \'SBOX%\'", conn)\n')
        skip = True
        continue
    
    if skip:
        # Stop skipping once we clear the old broken query lines (looking for 'conn' or closing parenthesis)
        if ")" in line or "conn" in line:
            skip = False
        continue
        
    new_lines.append(line)

content = "".join(new_lines)

# Compile check with built-in safety validation
compile(content, path, 'exec')
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ SUCCESS: Line 263 query block purged and replaced with a clean single line. Compiles cleanly!")
