import streamlit as st
import traceback
import sys

st.set_page_config(page_title="Juicer Diagnostic", page_icon="🛠️", layout="wide")
st.title("🛠️ Backend Diagnostic & Data X-Ray")
st.markdown("This dashboard bypasses the UI formatting to expose the raw data coming from your backend engines.")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Juice Pipeline Data")
    try:
        import juice_pipeline
        df = juice_pipeline.get_juice_data()
        st.success(f"✅ juice_pipeline.py online. Retrieved {len(df)} players.")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"🚨 Crash in juice_pipeline.py: {e}")
        st.code(traceback.format_exc())

with col2:
    st.header("2. Parlay Engine & Evaluator Data")
    try:
        import parlay_engine
        st.success("✅ parlay_engine.py found and imported.")
        
        # Display the available functions inside parlay_engine
        engine_funcs = [f for f in dir(parlay_engine) if not f.startswith('_')]
        st.write("**Available Functions in parlay_engine.py:**")
        st.json(engine_funcs)
        
        st.info("Paste the raw output or any errors from this column back to the chat so we can map the PrizePicks/Parlay cards.")
        
    except Exception as e:
        st.error(f"🚨 Crash in parlay_engine.py: {e}")
        st.code(traceback.format_exc())

st.header("3. Database Connection Test")
try:
    import sqlite3
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        st.success(f"✅ action_grid.db connected. Found tables: {tables}")
    else:
        st.warning("⚠️ action_grid.db not found in this directory.")
except Exception as e:
    st.error(f"🚨 Database Error: {e}")
    st.code(traceback.format_exc())

