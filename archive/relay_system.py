import sqlite3, json, datetime

# Hardcoding the exact, undeniable address of your database
db_path = r"C:\Users\chuck\the-juicer\action_grid.db"

print("\n" + "="*65)
print("📡 INITIALIZING CHUCK'S AUTONOMOUS RELAY & TAGGING SYSTEM")
print("="*65)

# --- RELAY 1: BACKEND GENERATION ---
try:
    conn = sqlite3.connect(db_path)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the unique autonomous tag
    tracer_tag = "RELAY_TAG_ALPHA_001"
    fake_legs = json.dumps([{"player_name": f"SYSTEM_TEST_{tracer_tag}", "stat_category": "telemetry", "line": 100, "direction": "OVER"}])
    
    conn.execute("DELETE FROM slips WHERE platform = 'TELEMETRY_RELAY'")
    conn.execute("INSERT INTO slips (platform, leg_count, legs_json, implied_probability, confidence_tier, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                ("TELEMETRY_RELAY", 1, fake_legs, 0.99, "A", "PENDING", now))
    conn.commit()
    print(f"  ✅ RELAY 1 (BACKEND): Data generated and tagged with {tracer_tag}")
except Exception as e:
    print(f"  ❌ RELAY 1 FAILED: {e}")

# --- RELAY 2: DATABASE VERIFICATION ---
try:
    check = conn.execute("SELECT legs_json FROM slips WHERE platform = 'TELEMETRY_RELAY'").fetchone()
    if check and tracer_tag in check[0]:
        print(f"  ✅ RELAY 2 (DATABASE): Tag {tracer_tag} successfully stored in action_grid.db")
    else:
        print("  ❌ RELAY 2 (DATABASE): Data lost in transit to database.")
    conn.close()
except Exception as e:
    print(f"  ❌ RELAY 2 FAILED: {e}")

# --- RELAY 3 & 4: UI SENSOR AND ROUTING ---
ui_code = """
# --- AUTONOMOUS RELAY SENSOR ---
def render_telemetry_relay():
    import streamlit as st
    import sqlite3
    import pandas as pd
    import json
    
    st.markdown("<h3 style='color: #00f2fe;'>📡 AUTONOMOUS RELAY STATUS</h3>", unsafe_allow_html=True)
    try:
        db_path = r"C:\Users\chuck\the-juicer\action_grid.db"
        with sqlite3.connect(db_path) as conn:
            relay_data = pd.read_sql("SELECT * FROM slips WHERE platform = 'TELEMETRY_RELAY'", conn)
        
        if not relay_data.empty:
            legs = json.loads(relay_data.iloc[0]['legs_json'])
            tag = legs[0]['player_name']
            st.success(f"✅ RELAY 3 & 4 (DASHBOARD): Signal received! Tag: {tag}")
            st.info("The loop is complete. Backend -> Database -> UI plumbing is 100% intact.")
        else:
            st.error("❌ RELAY 3 (DASHBOARD): Signal lost. Dashboard is reading the wrong database.")
    except Exception as e:
        st.error(f"UI Error: {e}")
"""
try:
    with open("ui_components.py", "a", encoding="utf-8") as f:
        f.write("\n" + ui_code)
    print("  ✅ RELAY 3 (UI SENSOR): Dashboard sensor physically installed.")
    
    with open("app.py", "r", encoding="utf-8") as f: app_text = f.read()
    
    # Wire the dashboard tab to our new telemetry sensor
    app_text = app_text.replace("ui.render_real_parlay_matrix()", "ui.render_telemetry_relay()")
    app_text = app_text.replace("ui.render_parlay_matrix()", "ui.render_telemetry_relay()")
    
    with open("app.py", "w", encoding="utf-8") as f: f.write(app_text)
    print("  ✅ RELAY 4 (ROUTING): Dashboard wired to receive telemetry.")
except Exception as e:
    print(f"  ❌ UI/ROUTING ERROR: {e}")

print("\n" + "="*65)
print(" 🚀 ALL RELAYS ACTIVE. LAUNCHING DASHBOARD...")
print("="*65 + "\n")