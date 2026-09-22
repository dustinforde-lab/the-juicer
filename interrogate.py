import os, glob

print("🚨 INTERNAL AFFAIRS: AUDITING AGENT PIPELINES...\n")

py_files = glob.glob("*.py")
lewis_suspects = []
mike_suspects = []

for file in py_files:
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Hunting Lewis's fake data
            if "Starter Prop 1" in content or "SLIP-CB-01" in content:
                lewis_suspects.append(file)
                
            # Hunting Mike and Dom's DB writing scripts
            if "INSERT INTO dfs_classic_lineups" in content or "to_sql('dfs_classic_lineups'" in content:
                mike_suspects.append(file)
    except:
        pass

print("🕵️‍♂️ LEWIS (PARLAY INGESTION) SUSPECTS:")
if lewis_suspects:
    for s in lewis_suspects: print(f"  -> {s} (Contains hardcoded dummy parlay data)")
else:
    print("  -> No hardcoded strings found. Lewis might be pulling from a dead JSON file.")

print("\n🕵️‍♂️ MIKE & DOM (DFS PROJECTIONS) SUSPECTS:")
if mike_suspects:
    for s in mike_suspects: print(f"  -> {s} (Handles writing the DFS lineups)")
else:
    print("  -> Could not locate the SQL insert command for Classic Lineups.")
    
print("\n=======================================================")