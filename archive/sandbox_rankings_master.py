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
        .neon-title { color: #bb88ff; text-align: left; font-weight: 900; letter-spacing: 2px; }
        
        /* Scaled down for Dual-Pane Density */
        .player-card {
            background-color: #12101b;
            border: 1px solid #2a224a;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a162b; padding-bottom: 8px; margin-bottom: 8px; }
        .p-name { font-size: 16px; font-weight: 900; color: #e6edf3; }
        .p-team { font-size: 12px; color: #8b949e; font-weight: bold; margin-left: 6px; }
        .p-pos { background-color: rgba(255, 42, 109, 0.15); color: #ff2a6d; border: 1px solid #ff2a6d; padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-right: 8px; }
        .p-fp { color: #00e5ff; font-size: 18px; font-weight: 900; letter-spacing: 1px; }
        
        .stat-container { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 8px; }
        .stat-badge { background-color: #1a162b; border: 1px solid #2a224a; padding: 4px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; color: #a5b4fc; }
        .stat-val { color: #ffffff; font-weight: 900; margin-left: 4px; }
        
        .analysis-box {
            background-color: #161224;
            border-left: 3px solid #bb88ff;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 11px;
            color: #c9d1d9;
            font-style: italic;
            line-height: 1.4;
        }
        .analysis-label { color: #bb88ff; font-weight: 900; font-style: normal; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; display: block; }
        </style>
    """, unsafe_allow_html=True)

def format_stat_name(stat_raw):
    mapping = {
        'REC': 'Receptions', 'REC_YDS': 'Rec Yards', 'PASS_YDS': 'Pass Yards',
        'RUSH_YDS': 'Rush Yards', 'PASS_TDS': 'Pass TDs', 'RUSH_TDS': 'Rush TDs',
        'REC_TDS': 'Rec TDs', 'ANYTIME_TD': 'TD Prob'
    }
    return mapping.get(str(stat_raw).upper(), str(stat_raw).replace('_', ' ').title())

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 class='neon-title'>🛠️ PHASE 4: THE MASTER SYNDICATE BOARD</h3><br>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT * FROM player_rankings LIMIT 2000", conn)
            
        if df.empty:
            st.info("No records found in player_rankings.")
            return

        col_map = {'player_name': 'player', 'consensus_line': 'line', 'juice_score': 'juice', 'stat_category': 'stat'}
        df = df.rename(columns=lambda x: col_map.get(x.lower(), x.lower()))

        if 'stat' in df.columns and 'line' in df.columns:
            for col in ['player', 'team', 'pos', 'fp', 'analysis']:
                if col not in df.columns: df[col] = "N/A" if col != 'fp' else "0.0"
                    
            grouped = df.groupby(['player', 'team', 'pos']).apply(lambda x: x.to_dict('records')).reset_index(name='stats')
            
            # Build master table for the left column
            table_data = []
            for _, row in grouped.iterrows():
                fp_val = row['stats'][0].get('fp', '0.0')
                try: fp_num = float(fp_val)
                except: fp_num = 0.0
                table_data.append({"Player": row['player'], "Pos": row['pos'], "Team": row['team'], "Proj FP": fp_num, "RawStats": row['stats']})
                
            master_df = pd.DataFrame(table_data).sort_values("Proj FP", ascending=False).reset_index(drop=True)
            master_df["Rank"] = master_df.index + 1
            
            # --- DUAL PANE LAYOUT ---
            col_table, col_cards = st.columns([1.2, 2])
            
            with col_table:
                st.markdown("#### 🏆 Top 300 Matrix")
                st.dataframe(master_df[["Rank", "Player", "Pos", "Team", "Proj FP"]].head(300), use_container_width=True, height=710)
                
            with col_cards:
                st.markdown("#### 🃏 Positional Intelligence")
                tabs = st.tabs(["QB (50)", "RB (50)", "WR (75)", "TE (50)", "FLEX (50)"])
                
                def render_cards(pos_filter, limit):
                    if pos_filter == "FLEX":
                        filtered = master_df[master_df['Pos'].isin(['RB', 'WR', 'TE'])].head(limit)
                    else:
                        filtered = master_df[master_df['Pos'] == pos_filter].head(limit)
                        
                    # Locks the height of the right side so it matches the table
                    with st.container(height=650):
                        for _, r in filtered.iterrows():
                            stats = r['RawStats']
                            fp_display = f"{r['Proj FP']:.1f}"
                            db_analysis = stats[0].get('analysis', 'N/A')
                            
                            if db_analysis == 'N/A' or not db_analysis:
                                if r['Proj FP'] > 20: db_analysis = f"High-leverage ceiling play. Game script projects a heavy shootout environment forcing {r['Team']} to an elevated pass rate."
                                elif r['Proj FP'] > 12: db_analysis = f"Solid median outcome projected. Floor is protected by consistent volume."
                                else: db_analysis = f"Fringe flex consideration. Projected volume is lower due to negative game script or timeshare constraints. Recommended fade."

                            stat_html = ""
                            for s in stats:
                                raw_stat = s.get('stat', '')
                                line = s.get('line', '0')
                                if raw_stat and raw_stat != 'Nan':
                                    clean_stat = format_stat_name(raw_stat)
                                    display_line = f"{line}%" if "Prob" in clean_stat else line
                                    stat_html += f'<div class="stat-badge">{clean_stat}: <span class="stat-val">{display_line}</span></div>'
                            
                            st.markdown(f'''
                            <div class="player-card">
                                <div class="card-header">
                                    <div>
                                        <span class="p-pos">{r['Pos']}</span>
                                        <span class="p-name">{r['Player']}</span>
                                        <span class="p-team">({r['Team']})</span>
                                    </div>
                                    <div class="p-fp">{fp_display} FP</div>
                                </div>
                                <div class="stat-container">{stat_html if stat_html else '<div class="stat-badge">No extended stats available</div>'}</div>
                                <div class="analysis-box"><span class="analysis-label">Mike & Donna's Diagnosis</span>{db_analysis}</div>
                            </div>
                            ''', unsafe_allow_html=True)
                            
                with tabs[0]: render_cards("QB", 50)
                with tabs[1]: render_cards("RB", 50)
                with tabs[2]: render_cards("WR", 75)
                with tabs[3]: render_cards("TE", 50)
                with tabs[4]: render_cards("FLEX", 50)
        else:
            st.warning("Database schema does not match the expected format.")

    except Exception as e:
        st.error(f"Sandbox Error: {e}")

if __name__ == "__main__":
    run_sandbox()