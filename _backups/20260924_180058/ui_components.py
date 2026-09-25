import streamlit as st
import pandas as pd
import sqlite3

DB = "action_grid.db"

@st.cache_data(ttl=60, show_spinner=False)
def _read_sql_cached(q):
    try:
        with sqlite3.connect(DB) as conn: 
            return pd.read_sql(q, conn)
    except Exception:
        return pd.DataFrame()

def inject_elite_aesthetic():
    st.markdown("""
    <style>
    .glass-card { background: rgba(30, 34, 45, 0.6); border: 1px solid rgba(187, 136, 255, 0.2); border-radius: 8px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); }
    .live-game { background: rgba(20, 24, 33, 0.8); border: 1px solid rgba(0, 255, 127, 0.5); border-radius: 8px; padding: 16px; margin-bottom: 16px; box-shadow: 0 0 12px rgba(0, 255, 127, 0.15); }
    .neon-header { color: #bb88ff; font-size: 1.1rem; font-weight: 900; margin-bottom: 8px; }
    .stat-badge { background-color: #1a162b; border: 1px solid #2a224a; padding: 4px 8px; border-radius: 4px; color: #a5b4fc; font-weight: bold; font-size: 0.9rem; }
    .stat-val { color: #ffffff; font-weight: 900; margin-left: 4px; }
    </style>
    """, unsafe_allow_html=True)

def render_vegas_wall(games_list=None):
    st.markdown("### 🎲 Vegas Viewing Wall")
    
    # If app.py passes no arguments, fallback to database or render safe placeholder
    if games_list is None:
        try:
            df = _read_sql_cached("SELECT * FROM live_odds LIMIT 10")
            games_list = df.to_dict('records') if not df.empty else []
        except Exception:
            games_list = []
            
    if not games_list:
        st.info("Awaiting Live Vegas Data Pipeline...")
        return
        
    cols = st.columns(3)
    for i, game in enumerate(games_list):
        away = game.get("away_team", "TBD")
        home = game.get("home_team", "TBD")
        spread = game.get("spread", "-")
        card_class = "live-game" if game.get("is_live") else "glass-card"
        
        with cols[i % 3]:
            st.markdown(f'<div class="{card_class}"><div class="neon-header">{away} @ {home}</div><div style="margin-top: 10px;"><span class="stat-badge">Spread: <span class="stat-val">{spread}</span></span></div></div>', unsafe_allow_html=True)

def render_dfs_engine(dfs_players=None):
    st.markdown("### 🧬 DFS Engine")
    
    if dfs_players is None:
        dfs_players = []
        
    if not dfs_players:
        st.info("Awaiting DFS Player Projections...")
        return
        
    dfs_cols = st.columns(4)
    for i, player in enumerate(dfs_players):
        name = player.get("name", "Unknown")
        team = player.get("team", "FA")
        try: prop = float(player.get("prop_val") or 0.0)
        except: prop = 0.0
            
        with dfs_cols[i % 4]:
            st.markdown(f'<div class="glass-card"><div class="neon-header">⚡ {name} | {team}</div><div style="margin-top: 10px;"><span class="stat-badge">Line: <span class="stat-val">{prop}</span></span></div></div>', unsafe_allow_html=True)

def render_juice_rankings(juice_df_1=None, juice_df_2=None):
    st.markdown("### 🍹 Donna's Leverage (Juice Rankings)")
    
    if juice_df_1 is None: juice_df_1 = pd.DataFrame()
    if juice_df_2 is None: juice_df_2 = pd.DataFrame()
    
    table_col1, table_col2 = st.columns(2)
    with table_col1:
        st.markdown("<div class='neon-header'>Top Projected Value</div>", unsafe_allow_html=True)
        st.dataframe(juice_df_1, use_container_width=True, hide_index=True)
    with table_col2:
        st.markdown("<div class='neon-header'>Sharp Action & Leverage</div>", unsafe_allow_html=True)
        st.dataframe(juice_df_2, use_container_width=True, hide_index=True)
