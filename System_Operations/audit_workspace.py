import os
import re
import json

WORKSPACE = "."
ACTIVE_PIPELINE = {
    "app.py", 
    "intern_odds_scraper.py", 
    "intern_showdown_dfs.py", 
    "intern_showdown_parlays.py", 
    "intern_slate_audit.py", 
    "setup_master_schema.py", 
    "set_week_flag.py"
}

def analyze_workspace():
    manifest = {
        "active_core": [],
        "detached_or_legacy": [],
        "data_and_state": [],
        "utility_and_batch": []
    }
    
    for root, dirs, files in os.walk(WORKSPACE):
        if ".git" in root or "__pycache__" in root:
            continue
            
        for file in files:
            path = os.path.relpath(os.path.join(root, file), WORKSPACE)
            size_kb = round(os.path.getsize(path) / 1024, 2)
            
            if file.endswith(".py"):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                functions = re.findall(r"def\s+([a-zA-Z0-9_]+)\(", content)
                imports = re.findall(r"(?:from\s+([a-zA-Z0-9_]+)\s+import|import\s+([a-zA-Z0-9_]+))", content)
                flat_imports = list(set([i[0] or i[1] for i in imports]))
                
                entry = {
                    "file": path,
                    "size_kb": size_kb,
                    "functions": functions,
                    "imports": flat_imports,
                    "touches_db": "action_grid.db" in content,
                    "touches_brain": "brain.json" in content
                }
                
                if file in ACTIVE_PIPELINE:
                    manifest["active_core"].append(entry)
                else:
                    manifest["detached_or_legacy"].append(entry)
                    
            elif file.endswith((".db", ".json", ".csv")):
                manifest["data_and_state"].append({"file": path, "size_kb": size_kb})
            elif file.endswith((".bat", ".ps1", ".txt", ".md")):
                manifest["utility_and_batch"].append({"file": path, "size_kb": size_kb})

    print("=" * 60)
    print("      THE JUICER: WORKSPACE & CODEBASE AUDIT")
    print("=" * 60)
    
    print(f"\n[ACTIVE PIPELINE ({len(manifest['active_core'])} files)]")
    for item in manifest["active_core"]:
        print(f"  * {item['file']} ({item['size_kb']} KB) -> Functions: {item['functions']}")
        
    print(f"\n[DETACHED / LEGACY SCRIPTS ({len(manifest['detached_or_legacy'])} files)]")
    if not manifest["detached_or_legacy"]:
        print("  * None found in root directory.")
    else:
        for item in manifest["detached_or_legacy"]:
            db_flag = "[DB Linked]" if item["touches_db"] else ""
            brain_flag = "[Brain Linked]" if item["touches_brain"] else ""
            print(f"  * {item['file']} ({item['size_kb']} KB) {db_flag} {brain_flag}")
            print(f"    Available Functions: {item['functions']}")
            
    print(f"\n[DATA & STATE FILES ({len(manifest['data_and_state'])} files)]")
    for item in manifest["data_and_state"]:
        print(f"  * {item['file']} ({item['size_kb']} KB)")
        
    print(f"\n[BATCH & UTILITY ({len(manifest['utility_and_batch'])} files)]")
    for item in manifest["utility_and_batch"]:
        print(f"  * {item['file']} ({item['size_kb']} KB)")

    with open("workspace_audit.json", "w") as f:
        json.dump(manifest, f, indent=4)
        
    print("\n" + "=" * 60)
    print("[SUCCESS] Full audit saved to 'workspace_audit.json'.")
    print("=" * 60)

if __name__ == "__main__":
    analyze_workspace()
