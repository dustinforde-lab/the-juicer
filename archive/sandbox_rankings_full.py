import sqlite3
import pandas as pd
import streamlit as st
import os

st.set_page_config(layout="wide")
DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def inject_aesthetic_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0914; color: #ffffff; }
        .neon-title { color: #bb88ff; text-align: center; font-weight: 900; letter-spacing: 2px; }
        
        .player-card {
            background-color: #12101b;
            border: 1px solid #2a224a;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a162b; padding-bottom: 10px; margin-bottom: 12px; }
        .p-name { font-size: 18px; font-weight: 900; color: #e6edf3; }
        .p-team { font-size: 14px; color: #8b949e; font-weight: bold; margin-left: 8px; }
        .p-pos { background-color: rgba(255, 42, 109, 0.15); color: #ff2a6d; border: 1px solid #ff2a6d; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 12px; }
        .p-fp { color: #00e5ff; font-size: 20px; font-weight: 900; letter-spacing: 1px; }
        
        .stat-container { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
        .stat-badge { background-color: #1a162b; border: 1px solid #2a224a; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; color: #a5b4fc; }
        .stat-val { color: #ffffff; font-weight: 900; margin-left: 4px; }
        .juice-badge { background-color: rgba(0, 229, 255, 0.1); border: 1px solid #00e5ff; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; color: #00e5ff; }
        </style>
    """, unsafe_allow_html=True)

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 class='neon-title'>🛠️ PHASE 4: FULL PROJECTED STAT LINES</h3><br>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # We fetch everything so we can group it in Pandas
            df = pd.read_sql("SELECT * FROM player_rankings LIMIT 500", conn)
            
        if df.empty:
            st.info("No records found in player_rankings.")
            return

        # Standardize column names based on the screenshot schema
        col_map = {
            'player_name': 'player', 
            'consensus_line': 'line', 
            'juice_score': 'juice',
            'stat_category': 'stat'
        }
        df = df.rename(columns=lambda x: col_map.get(x.lower(), x.lower()))

        # If the DB is structured vertically (one row per stat category like the screenshot)
        if 'stat' in df.columns and 'line' in df.columns:
            # Fill missing keys for grouping
            for col in ['player', 'team', 'pos', 'fp']:
                if col not in df.columns:
                    df[col] = "N/A" if col != 'fp' else "0.0"
                    
            # Group all stats for a single player together
            grouped = df.groupby(['player', 'team', 'pos']).apply(
                lambda x: x.to_dict('records')
            ).reset_index(name='stats')
            
            for _, row in grouped.iterrows():
                name, team, pos = row['player'], row['team'], row['pos']
                player_stats = row['stats']
                
                # Assume FP is attached to the player, default to 0.0 if not found
                fp = player_stats[0].get('fp', '0.0')
                # Grab the max juice score if it exists across their props
                max_juice = max([float(s.get('juice', 0)) for s in player_stats if s.get('juice')], default=0.0)
                
                stat_html = ""
                for s in player_stats:
                    stat = str(s.get('stat', '')).replace('_', ' ').title()
                    line = s.get('line', '0')
                    if stat and stat != 'Nan':
                        stat_html += f'<div class="stat-badge">{stat}: <span class="stat-val">{line}</span></div>'
                
                if max_juice > 0:
                    stat_html += f'<div class="juice-badge">Max Juice: <span class="stat-val">{max_juice:.2f}</span></div>'

                st.markdown(f'''
                <div class="player-card">
                    <div class="card-header">
                        <div>
                            <span class="p-pos">{pos}</span>
                            <span class="p-name">{name}</span>
                            <span class="p-team">({team})</span>
                        </div>
                        <div class="p-fp">{fp} FP</div>
                    </div>
                    <div class="stat-container">
                        {stat_html if stat_html else '<div class="stat-badge">No extended stats available</div>'}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning("Database schema does not match the expected stat_category format. Falling back to default.")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Sandbox Error: {e}")

if __name__ == "__main__":
    run_sandbox()