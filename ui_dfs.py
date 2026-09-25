import streamlit as st
import data_service

def render_dfs_tab():
    st.markdown("<h2 style='color:#00ff88; margin-bottom:2px;'>🧬 DFS ENGINE & MASTER PLAYER POOL</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Dark Glassmorphism • Neon Positional Accents • Evaluator 3.0 Valuations</div>", unsafe_allow_html=True)

    if "dfs_engine_slate" not in st.session_state:
        st.session_state["dfs_engine_slate"] = "Sunday Classic Main Slate"

    c_tog, c_fltr = st.columns([1.5, 2.5])
    with c_tog:
        st.session_state["dfs_engine_slate"] = st.radio("Slate Context", ["Showdown", "Sunday Classic Main Slate"], horizontal=True, key="dfs_eng_rad")
    with c_fltr:
        pos_filter = st.selectbox("Position Filter", ["ALL", "QB", "RB", "WR", "TE", "K", "DST"])

    df = data_service.get_slate_master_300(st.session_state["dfs_engine_slate"])
    if pos_filter != "ALL":
        df = df[df["Pos"] == pos_filter]

    st.markdown(f"<div style='color:#8b949e; font-size:11px; margin-bottom:12px;'>Showing <b>{len(df)}</b> active targets in the {st.session_state['dfs_engine_slate']} pool.</div>", unsafe_allow_html=True)

    # Render as Custom Glassmorphic Cards
    cols = st.columns(3)
    for idx, row in df.iterrows():
        pos = row['Pos']
        pos_col = "#00e5ff" if pos=="QB" else ("#ff2a6d" if pos=="RB" else ("#00ff88" if pos=="WR" else ("#ffd700" if pos=="TE" else ("#ff9f43" if pos=="K" else "#a55eea"))))
        
        card_html = f"""
        <div style='background:rgba(13,17,23,0.75); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.08); border-top:4px solid {pos_col}; border-radius:10px; padding:14px; margin-bottom:14px; box-shadow:0 4px 12px rgba(0,0,0,0.5); transition: transform 0.2s;'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;'>
                <div>
                    <h4 style='margin:0; color:#fff; font-size:16px;'>{row['Player']}</h4>
                    <span style='color:#8b949e; font-size:11px;'>{row['Team']} • {row['Donna_Tier']}</span>
                </div>
                <div style='background:{pos_col}22; color:{pos_col}; font-weight:900; font-size:11px; padding:4px 8px; border-radius:6px;'>{pos}</div>
            </div>
            <div style='display:flex; justify-content:space-between; background:#161b22; padding:8px 10px; border-radius:6px; font-size:12px;'>
                <div style='text-align:center;'><span style='color:#8b949e; font-size:10px;'>DK SAL</span><br><b style='color:#fff;'>${row['Salary']:,}</b></div>
                <div style='text-align:center;'><span style='color:#8b949e; font-size:10px;'>xFP BASE</span><br><b style='color:#00ff88;'>{row['Mike_PPR']:.1f}</b></div>
                <div style='text-align:center;'><span style='color:#8b949e; font-size:10px;'>VALUE</span><br><b style='color:#ffd700;'>{row['Value']}x</b></div>
            </div>
        </div>
        """
        with cols[idx % 3]:
            st.html(card_html)
