import os

learning_ui_code = """
# --- BAYESIAN KNOWLEDGE BASE (ROADMAP #99-100) ---
def render_learning_loop():
    import streamlit as st
    import sqlite3
    import pandas as pd
    
    st.markdown("<h3 class='neon-title'>🧠 BAYESIAN KNOWLEDGE BASE</h3>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect("action_grid.db") as conn:
            weights_df = pd.read_sql("SELECT * FROM correlation_weights ORDER BY confidence_multiplier DESC", conn)
            
        if weights_df.empty:
            st.info("The learning loop is currently accumulating baseline data. Check back after the next slate is graded.")
            return
            
        st.markdown("#### Dynamic Correlation Weights")
        st.markdown("The system's active standard deviation (sigma) adjustments and confidence multipliers based on historical delta errors.")
        
        # UI Formatting
        weights_df['confidence_tier'] = weights_df['confidence_multiplier'].apply(
            lambda x: '🔥 HIGH' if x >= 1.1 else ('❄️ LOW' if x < 1.0 else '⚖️ NEUTRAL')
        )
        
        st.dataframe(
            weights_df[['stat_category', 'sigma_adjustment', 'confidence_multiplier', 'confidence_tier', 'last_updated']], 
            use_container_width=True, 
            hide_index=True,
            height=400
        )
            
    except Exception as e:
        st.error(f"Error loading Bayesian weights: {e}")
"""

with open("ui_components.py", "a", encoding="utf-8") as f:
    f.write("\n" + learning_ui_code)
print("✅ Bayesian Knowledge Base injected into ui_components.py")