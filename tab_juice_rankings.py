# -*- coding: utf-8 -*-
import streamlit as st
import data_service

def render_the_rankings():
    # THE JUICER HEADER PITCH (OPTION 1)
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(13,17,23,0.95), rgba(22,27,34,0.95)); backdrop-filter: blur(12px); border: 1px solid #30363d; border-bottom: 3px solid #00ff88; padding: 16px 20px; border-radius: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;'>
        <div style='display: flex; align-items: center;'>
            <div style='font-size: 28px; margin-right: 14px; background: rgba(0,255,136,0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(0,255,136,0.3);'>⚡🥤</div>
            <div>
                <h1 style='color: #fff; font-size: 24px; font-weight: 900; margin: 0; letter-spacing: 0.5px;'>THE JUICER <span style='color: #00ff88; font-size: 14px; font-weight: 600; margin-left: 8px;'>COMMAND CENTER v3.0</span></h1>
                <div style='color: #8b949e; font-size: 12px; margin-top: 2px;'>Autonomous Quantitative Quant &bull; Evaluator 3.0 Engine Active</div>
            </div>
        </div>
        <div style='text-align: right;'>
            <span style='background: rgba(0,229,255,0.1); color: #00e5ff; font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(0,229,255,0.3);'>🟢 LIVE TELEMETRY</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    telemetry = data_service.get_full_telemetry_timestamps()
    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Sleeper NFL API Data &bull; Source: Evaluator 3.0 &bull; ⏱️ {telemetry['odds_badge']}</div>", unsafe_allow_html=True)

    df = data_service.get_slate_master_300("Classic")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("<h4 style='color:#ffd700; margin-bottom:12px;'>🏆 Overall Top 300 Board</h4>", unsafe_allow_html=True)
        left_html = "<div style='height: 750px; overflow-y: auto; scrollbar-width: thin; padding-right: 12px;'>"
        for idx, row in df.iterrows():
            status = row.get('Injury', 'FULL')
            inj_col = "#00ff88" if status == 'FULL' else ("#ffeb3b" if status == 'PROBABLE' else ("#ff9f43" if status == 'QUESTIONABLE' else "#ff2a6d"))
            health_icon = "🩺" if status == 'FULL' else ("🩹" if status in ['PROBABLE', 'QUESTIONABLE'] else "🚑")
            stat_line = data_service.get_projected_stat_line(row['Pos'], row['Player'])
            
            left_html += f"""
            <div style='background:rgba(13,17,23,0.75); border:1px solid rgba(255,255,255,0.08); border-left:4px solid {inj_col}; border-radius:8px; padding:12px; margin-bottom:10px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div style='display:flex; align-items:center;'>
                        <div style='color:#8b949e; font-size:13px; font-weight:900; width:28px;'>#{idx+1}</div>
                        <div>
                            <div style='color:#fff; font-size:14px; font-weight:bold;'>{row['Player']} <span style='color:#8b949e; font-size:11px;'>{row['Team']} vs {row['Opp']}</span></div>
                            <div style='color:#00ff88; font-size:11px; margin-top:2px;'>{stat_line}</div>
                        </div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='color:#00ff88; font-size:14px; font-weight:900;'>{row.get('xFP', 0):.1f} xFP</div>
                        <div style='color:#8b949e; font-size:10px;'>${row.get('Salary', 0):,} | {health_icon}</div>
                    </div>
                </div>
            </div>"""
        left_html += "</div>"
        st.html(left_html)
        
    with col_right:
        st.markdown("<h4 style='color:#00e5ff; margin-bottom:12px;'>🎯 Positional Recon Workspace</h4>", unsafe_allow_html=True)
        tabs = st.tabs(["QB", "RB", "WR", "TE", "K", "DST"])
        positions = ["QB", "RB", "WR", "TE", "K", "DST"]
        
        for i, pos in enumerate(positions):
            with tabs[i]:
                pos_df = df[df['Pos'] == pos]
                right_html = "<div style='height: 700px; overflow-y: auto; scrollbar-width: thin; padding-right: 12px;'>"
                for _, row in pos_df.iterrows():
                    stat_line = data_service.get_projected_stat_line(row['Pos'], row['Player'])
                    right_html += f"""
                    <div style='background:rgba(22,27,34,0.85); border:1px solid #30363d; border-radius:8px; padding:14px; margin-bottom:12px;'>
                        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                            <b style='color:#fff; font-size:15px;'>{row['Player']}</b>
                            <span style='color:#00e5ff; font-weight:bold; font-size:12px;'>{row.get('Donna_Tier', 'Core')}</span>
                        </div>
                        <div style='color:#00ff88; font-size:12px; margin-bottom:8px; background:#0d1117; padding:6px 10px; border-radius:4px;'>{stat_line}</div>
                        <div style='display:flex; justify-content:space-between; background:#0d1117; padding:8px; border-radius:6px; font-size:12px; margin-bottom:8px;'>
                            <span style='color:#8b949e;'>⚡ Ceil: <b style='color:#00ff88;'>{row.get('Sim_Ceiling', 0):.1f}</b></span>
                            <span style='color:#8b949e;'>🛡️ Floor: <b style='color:#ff2a6d;'>{row.get('Sim_Floor', 0):.1f}</b></span>
                            <span style='color:#8b949e;'>💰 Salary: <b style='color:#ffd700;'>${row.get('Salary', 0):,}</b></span>
                        </div>
                    </div>"""
                right_html += "</div>"
                st.html(right_html)
