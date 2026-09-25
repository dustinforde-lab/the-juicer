import sqlite3
import pandas as pd
import os

print("\n" + "="*55 + "\n🐍 RUNNING THE PLUMBING SNAKE (DIAGNOSTIC)\n" + "="*55)

# 1. Check the Database Pipe
try:
    with sqlite3.connect("action_grid.db") as conn:
        slips = pd.read_sql("SELECT * FROM slips", conn)
        print(f"[DB STATUS] Total rows in 'slips' table: {len(slips)}")
        
        if len(slips) > 0:
            print("\n[DB STATUS] Slip Count by Platform:")
            print(slips['platform'].value_counts().to_string())
            print(f"\n[DB STATUS] Columns detected: {', '.join(list(slips.columns))}")
        else:
            print("\n[DB STATUS] ⚠️ The table is completely empty. The generator silently failed.")
except Exception as e:
    print(f"[DB ERROR] Could not read slips table: {e}")

# 2. Check the app.py Routing (The Control Wiring)
try:
    with open("app.py", "r", encoding="utf-8") as f:
        app_code = f.read()
        print("\n[APP ROUTING] How app.py is trying to load Parlays and Pick'ems:")
        for line in app_code.split('\n'):
            if 'ui.render_' in line and ('parlay' in line.lower() or 'pickem' in line.lower() or 'prize' in line.lower()):
                print(f"   -> {line.strip()}")
except Exception as e:
    print(f"[APP ERROR] {e}")

# 3. Check the ui_components.py Definitions
try:
    with open("ui_components.py", "r", encoding="utf-8") as f:
        ui_code = f.read()
        print("\n[UI DEFINITIONS] What ui_components.py actually has available:")
        for line in ui_code.split('\n'):
            if line.startswith('def render_') and ('parlay' in line.lower() or 'pickem' in line.lower() or 'prize' in line.lower()):
                print(f"   -> {line.strip()}")
except Exception as e:
    print(f"[UI ERROR] {e}")

print("="*55 + "\n")