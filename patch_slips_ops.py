import os

slips_and_ops_code = """
# --- PICK'EM SLIPS VIEWER (ROADMAP #83-92) ---
def render_pickem_slips():
    import streamlit as st
    import sqlite3
    import pandas as pd
    import json
    
    st.markdown("<h3 class='neon-title'>🎫 PRIZEPICKS & UNDERDOG SLIPS</h3>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect("action_grid.db") as conn:
            slips_df = pd.read_sql("SELECT * FROM slips WHERE status = 'PENDING' ORDER BY implied_probability DESC", conn)
            
        if slips_df.empty:
            st.info("No active slips generated. Waiting for the AI generator loop.")
            return
            
        for _, row in slips_df.iterrows():
            legs = json.loads(row['legs_json'])
            
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                    <strong style="color: var(--flex);">{row['platform']} | {row['leg_count']}-Leg Slip</strong>
                    <span style="background: rgba(0,242,254,0.15); color: #00f2fe; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                        Win Prob: {row['implied_probability']*100:.1f}%
                    </span>
                </div>
            ''', unsafe_allow_html=True)
            
            for leg in legs:
                st.markdown(f'''
                <div style="display: flex; justify-content: space-between; border-left: 3px solid var(--qb); padding-left: 10px; margin-bottom: 8px; font-size: 14px;">
                    <span><strong>{leg['player_name']}</strong> <span style="opacity: 0.6;">({leg['stat_category'].replace('_', ' ')})</span></span>
                    <span><strong>{leg['direction']} {leg['line']}</strong> <span style="opacity: 0.5;">(Proj: {leg['predicted_value']})</span></span>
                </div>
                ''', unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading slips: {e}")

# --- OPS CENTER & KILL SWITCH (ROADMAP #60, #62) ---
def render_ops_center():
    import streamlit as st
    import sqlite3
    import pandas as pd
    
    st.markdown("<h3 class='neon-title'>⚙️ SYSTEM OPS & SCHEDULER</h3>", unsafe_allow_html=True)
    
    # 1. Global Scheduler Kill Switch
    st.markdown("#### Autonomous Engine Status")
    try:
        from app import global_scheduler
        sched = global_scheduler
        status_color = "#ff4757" if sched.is_paused else "#2ed573"
        status_text = "PAUSED (KILL SWITCH ENGAGED)" if sched.is_paused else "ACTIVE (POLLING LIVE)"
        
        st.markdown(f"<div style='font-size: 14px; margin-bottom: 15px; padding: 10px; border-left: 4px solid {status_color}; background: rgba(255,255,255,0.05);'>{status_text}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏸️ ENGAGE KILL SWITCH", use_container_width=True):
                sched.pause()
                st.rerun()
        with col2:
            if st.button("▶️ RESUME AUTONOMY", use_container_width=True):
                sched.resume()
                st.rerun()
                
        # 2. Active Jobs
        st.markdown("#### Scheduled Jobs")
        try:
            jobs = sched.get_job_statuses()
            for job in jobs:
                st.markdown(f"- **{job['name']}** — *Next tick in {job['secs_until_next']}s*")
        except AttributeError:
            pass
            
    except ImportError:
        st.error("Global scheduler singleton not found. Check app.py injection.")
        
    # 3. Agent Chatter / Decision Log
    st.markdown("---")
    st.markdown("#### 🤖 Agent Decision Log")
    try:
        with sqlite3.connect("action_grid.db") as conn:
            chatter_df = pd.read_sql("SELECT timestamp, agent, message FROM agent_chatter ORDER BY message_id DESC LIMIT 20", conn)
            st.dataframe(chatter_df, use_container_width=True, hide_index=True, height=300)
    except Exception:
        st.info("No agent chatter logged yet.")
"""

with open("ui_components.py", "a", encoding="utf-8") as f:
    f.write("\n" + slips_and_ops_code)
print("✅ Slips Viewer and Ops Center functions injected into ui_components.py")