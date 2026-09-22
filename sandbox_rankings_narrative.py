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
            margin-bottom: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a162b; padding-bottom: 10px; margin-bottom: 12px; }
        .p-name { font-size: 20px; font-weight: 900; color: #e6edf3; }
        .p-team { font-size: 14px; color: #8b949e; font-weight: bold; margin-left: 8px; }
        .p-pos { background-color: rgba(255, 42, 109, 0.15); color: #ff2a6d; border: 1px solid #ff2a6d; padding: 3px 8px; border-radius: 4px; font-size: 13px; font-weight: bold; margin-right: 12px; }
        .p-fp { color: #00e5ff; font-size: 22px; font-weight: 900; letter-spacing: 1px; }
        
        .stat-container { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px; }
        .stat-badge { background-color: #1a162b; border: 1px solid #2a224a; padding: 6px 12px; border-radius: 4px; font-size: 13px; font-weight: bold; color: #a5b4fc; }
        .stat-val { color: #ffffff; font-weight: 900; margin-left: 4px; }
        
        .analysis-box {
            background-color: #161224;
            border-left: 3px solid #bb88ff;
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 13px;
            color: #c9d1d9;
            font-style: italic;
            line-height: 1.5;
        }
        .analysis-label { color: #bb88ff; font-weight: 900; font-style: normal; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; display: block; }
        </style>
    """, unsafe_allow_html=True)

def format_stat_name(stat_raw):
    """Cleans up raw DB stat names for a polished UI look."""
    mapping = {
        'REC': 'Receptions',
        'REC_YDS': 'Rec Yards',
        'PASS_YDS': 'Pass Yards',
        'RUSH_YDS': 'Rush Yards',
        'PASS_TDS': 'Pass TDs',
        'RUSH_TDS': 'Rush TDs',
        'REC_TDS': 'Rec TDs',
        'ANYTIME_TD': 'TD Probability'
    }
    raw_upper = str(stat_raw).upper()
    return mapping.get(raw_upper, str(stat_raw).replace('_', ' ').title())

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 class='neon-title'>🛠️ PHASE 4: FULL STAT LINES & DIAGNOSIS</h3><br>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT * FROM player_rankings LIMIT 500", conn)
            
        if df.empty:
            st.info("No records found in player_rankings.")
            return

        col_map = {
            'player_name': 'player', 
            'consensus_line': 'line', 
            'juice_score': 'juice',
            'stat_category': 'stat'
        }
        df = df.rename(columns=lambda x: col_map.get(x.lower(), x.lower()))

        if 'stat' in df.columns and 'line' in df.columns:
            for col in ['player', 'team', 'pos', 'fp', 'analysis']:
                if col not in df.columns:
                    df[col] = "N/A" if col != 'fp' else "0.0"
                    
            grouped = df.groupby(['player', 'team', 'pos']).apply(
                lambda x: x.to_dict('records')
            ).reset_index(name='stats')
            
            for _, row in grouped.iterrows():
                name, team, pos = row['player'], row['team'], row['pos']
                player_stats = row['stats']
                
                # Extract FP (defaulting to a clean number if possible)
                fp_val = player_stats[0].get('fp', '0.0')
                try: fp_display = f"{float(fp_val):.1f}"
                except: fp_display = str(fp_val)
                
                # Check for real analysis, or generate a placeholder based on FP
                db_analysis = player_stats[0].get('analysis', 'N/A')
                if db_analysis == 'N/A' or not db_analysis:
                    if float(fp_display) > 20:
                        db_analysis = f"High-leverage ceiling play. Game script projects a heavy shootout environment, forcing {team} into an elevated pass rate. Donna flags strong median leverage."
                    elif float(fp_display) > 12:
                        db_analysis = f"Solid median outcome projected. Floor is protected by consistent volume, though touchdown variance keeps ceiling capped."
                    else:
                        db_analysis = f"Fringe flex consideration. Projected volume is lower due to negative game script or timeshare constraints. Recommended fade in 9-man."

                stat_html = ""
                for s in player_stats:
                    raw_stat = s.get('stat', '')
                    line = s.get('line', '0')
                    if raw_stat and raw_stat != 'Nan':
                        clean_stat = format_stat_name(raw_stat)
                        # Add a % sign if it's a probability stat
                        display_line = f"{line}%" if "Probability" in clean_stat else line
                        stat_html += f'<div class="stat-badge">{clean_stat}: <span class="stat-val">{display_line}</span></div>'
                
                st.markdown(f'''
                <div class="player-card">
                    <div class="card-header">
                        <div>
                            <span class="p-pos">{pos}</span>
                            <span class="p-name">{name}</span>
                            <span class="p-team">({team})</span>
                        </div>
                        <div class="p-fp">{fp_display} FP</div>
                    </div>
                    
                    <div class="stat-container">
                        {stat_html if stat_html else '<div class="stat-badge">No extended stats available</div>'}
                    </div>
                    
                    <div class="analysis-box">
                        <span class="analysis-label">Mike & Donna's Diagnosis</span>
                        {db_analysis}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning("Database schema does not match the expected format.")

    except Exception as e:
        st.error(f"Sandbox Error: {e}")

if __name__ == "__main__":
    run_sandbox()