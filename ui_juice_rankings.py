# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def calculate_implied_totals(df_vegas):
    totals = []
    for _, row in df_vegas.iterrows():
        ou = row.get("Over_Under", 0)
        spread = row.get("Spread", 0)
        if spread < 0:
            home_total = (ou / 2) + (abs(spread) / 2)
            away_total = (ou / 2) - (abs(spread) / 2)
        else:
            home_total = (ou / 2) - (abs(spread) / 2)
            away_total = (ou / 2) + (abs(spread) / 2)
            
        totals.append({"Team": row["Home"], "Implied_Total": round(home_total, 2), "Opp": row["Away"]})
        totals.append({"Team": row["Away"], "Implied_Total": round(away_total, 2), "Opp": row["Home"]})
    return pd.DataFrame(totals)

def build_domo_card(p):
    pos_colors = {"QB": "#00e5ff", "RB": "#ff2a6d", "WR": "#00ff88", "TE": "#ffd700", "K": "#ff9f43", "DST": "#a55eea"}
    p_col = pos_colors.get(p.get("Pos", "UNK"), "#00e5ff")
    
    delta = p.get("Domo_Leverage", 0)
    delta_color = "#00ff88" if delta > 0 else "#ff4757"
    
    # Injury badge styling
    injury = p.get("Injury_Status", "Active")
    if injury in ["Out", "IR"]:
        badge = f"<span style='background:#ff4757; color:#ffffff; font-size:10px; font-weight:900; padding:2px 6px; border-radius:4px; margin-left:6px;'>{injury.upper()}</span>"
    elif injury in ["Questionable", "Doubtful"]:
        badge = f"<span style='background:#ffa502; color:#1e272e; font-size:10px; font-weight:900; padding:2px 6px; border-radius:4px; margin-left:6px;'>{injury[:1].upper()} - {p.get('Injury_Body_Part', 'Q')}</span>"
    else:
        badge = ""
    
    return f"""
    <div style='background:#0d1117; border:1px solid {p_col}66; border-left:6px solid {p_col}; border-radius:10px; padding:12px 16px; margin-bottom:14px; box-shadow:0 4px 16px rgba(0,0,0,0.5);'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <span style='font-size:16px; font-weight:900; color:#ffffff;'>{p.get("Player", "Unknown")}</span>
                <span style='background:{p_col}22; color:{p_col}; font-size:11px; font-weight:800; padding:2px 8px; border-radius:4px; margin-left:6px;'>{p.get("Pos", "UNK")}</span>
                {badge}
                <div style='color:#8b949e; font-size:12px; margin-top:3px;'>{p.get("Team", "UNK")} vs {p.get("Opp", "UNK")}</div>
            </div>
            <div style='text-align:right;'>
                <span style='color:#8b949e; font-size:11px;'>Mike PPR:</span>
                <div style='color:#ffffff; font-size:17px; font-weight:900;'>{p.get("Mike_Base", 0):.2f}</div>
            </div>
        </div>
        <div style='display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;'>
            <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; padding:4px 10px; font-size:11px;'>
                <span style='color:#8b949e;'>Implied Total:</span> <b style='color:#ffffff;'>{p.get("Implied_Total", 0)}</b>
            </div>
            <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; padding:4px 10px; font-size:11px;'>
                <span style='color:#8b949e;'>DK Salary:</span> <b style='color:#ffffff;'>${p.get("Salary", 0)}</b>
            </div>
            <div style='background:rgba({delta_color}22); border:1px solid {delta_color}; border-radius:6px; padding:4px 10px; font-size:11px;'>
                <span style='color:#cad3df;'>Domo Leverage: <b style='color:{delta_color};'>{delta:+.2f}</b></span>
            </div>
        </div>
    </div>
    """

def render_juice_tab():
    st.markdown("<h2 style='color:#00ff88; margin-bottom:2px;'>⚡ JUICE RANKINGS & DOMO LEVERAGE</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Dual-Ranking Matrix &bull; Live Injury Status &bull; Vegas Implied Totals</div>", unsafe_allow_html=True)
    
    # Breaking News Marquee
    try:
        if os.path.exists(DB_PATH):
            with sqlite3.connect(DB_PATH) as conn:
                news_items = pd.read_sql("SELECT Headline FROM breaking_news_feed ORDER BY Published_At DESC LIMIT 3", conn)
                if not news_items.empty:
                    headlines = " &nbsp;&nbsp;&bull;&nbsp;&nbsp; ".join(news_items["Headline"].tolist())
                    st.markdown(f"""
                        <div style='background:rgba(255,165,2,0.1); border:1px solid rgba(255,165,2,0.3); border-radius:6px; padding:6px 12px; font-size:12px; color:#ffa502; margin-bottom:14px; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;'>
                            <b>🚨 WIRE:</b> {headlines}
                        </div>
                    """, unsafe_allow_html=True)
    except Exception:
        pass

    df_vegas, df_dfs, df_injuries = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    try:
        if os.path.exists(DB_PATH):
            with sqlite3.connect(DB_PATH) as conn:
                df_vegas = pd.read_sql("SELECT * FROM vegas_lines", conn)
                df_dfs = pd.read_sql("SELECT * FROM dfs_projections", conn)
                df_injuries = pd.read_sql("SELECT * FROM player_status_wire", conn)
    except Exception:
        pass
        
    if not df_vegas.empty and not df_dfs.empty:
        totals_df = calculate_implied_totals(df_vegas)
        df_matrix = pd.merge(df_dfs, totals_df, on="Team", how="left")
        
        if not df_injuries.empty:
            df_matrix = pd.merge(df_matrix, df_injuries[["Player", "Injury_Status", "Injury_Body_Part"]], on="Player", how="left")
        else:
            df_matrix["Injury_Status"] = "Active"
            df_matrix["Injury_Body_Part"] = ""
            
        from ui_dfs import apply_mike_evaluator
        df_matrix = apply_mike_evaluator(df_matrix)
        df_matrix.rename(columns={"Mike Base PPR": "Mike_Base"}, inplace=True)
        
        df_matrix["Domo_Leverage"] = round((df_matrix["Mike_Base"] * 0.6) + (df_matrix["Implied_Total"] * 0.4) - (df_matrix["Salary"] / 1000), 2)
        df_matrix = df_matrix.sort_values(by="Domo_Leverage", ascending=False).dropna(subset=["Implied_Total"])

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.markdown("<h4 style='color:#ff2a6d; margin-bottom:8px;'>🔥 +EV LEVERAGE (TOP PLAYS)</h4>", unsafe_allow_html=True)
            for _, row in df_matrix.head(10).iterrows():
                st.html(build_domo_card(row.to_dict()))
                
        with col2:
            st.markdown("<h4 style='color:#a55eea; margin-bottom:8px;'>🧊 NEGATIVE DELTA (FADE LIST)</h4>", unsafe_allow_html=True)
            for _, row in df_matrix.tail(10).sort_values(by="Domo_Leverage", ascending=True).iterrows():
                st.html(build_domo_card(row.to_dict()))
    else:
        st.warning("⚠️ Matrix waiting for Live Vegas Lines and DFS Projections.")

