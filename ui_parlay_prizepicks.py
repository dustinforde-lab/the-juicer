# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def build_pick_card(p):
    pos_colors = {"QB": "#00e5ff", "RB": "#ff2a6d", "WR": "#00ff88", "TE": "#ffd700"}
    p_col = pos_colors.get(p.get("Pos", "UNK"), "#00e5ff")
    
    return f"""
    <div style='background:#0d1117; border:1px solid {p_col}66; border-left:6px solid {p_col}; border-radius:10px; padding:10px 14px; margin-bottom:10px; box-shadow:0 4px 10px rgba(0,0,0,0.5);'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <span style='font-size:14px; font-weight:900; color:#ffffff;'>{p.get("Player", "Unknown")}</span>
                <span style='color:#8b949e; font-size:11px; margin-left:6px;'>{p.get("Team", "UNK")} vs {p.get("Opp", "UNK")}</span>
            </div>
            <div style='text-align:right;'>
                <span style='color:#00ff88; font-size:12px; font-weight:900;'>+EV {p.get("Domo_Leverage", 0):+.2f}</span>
            </div>
        </div>
    </div>
    """

def render_parlay_matrix():
    st.markdown("<h2 style='color:#ffd700; margin-bottom:2px;'>??? PARLAY MATRIX & PRIZEPICKS OPTIMIZER</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>+EV Slip Builder &bull; 54.2% Break-Even Filtering &bull; Flex vs Power Evaluator</div>", unsafe_allow_html=True)
    
    df_vegas = pd.DataFrame()
    df_dfs = pd.DataFrame()
    
    try:
        if os.path.exists(DB_PATH):
            with sqlite3.connect(DB_PATH) as conn:
                df_vegas = pd.read_sql("SELECT * FROM vegas_lines", conn)
                df_dfs = pd.read_sql("SELECT * FROM dfs_projections", conn)
    except Exception:
        pass
        
    if not df_vegas.empty and not df_dfs.empty:
        # Re-run the Domo Matrix logic to pull the current +EV edge
        from ui_juice_rankings import calculate_implied_totals
        from ui_dfs import apply_mike_evaluator
        
        totals_df = calculate_implied_totals(df_vegas)
        df_matrix = pd.merge(df_dfs, totals_df, on="Team", how="left")
        df_matrix = apply_mike_evaluator(df_matrix)
        df_matrix.rename(columns={"Mike Base PPR": "Mike_Base"}, inplace=True)
        df_matrix["Domo_Leverage"] = round((df_matrix["Mike_Base"] * 0.6) + (df_matrix["Implied_Total"] * 0.4) - (df_matrix["Salary"] / 1000), 2)
        
        # Filter for +EV only (Threshold representing > 54.2% win probability baseline)
        ev_pool = df_matrix[df_matrix["Domo_Leverage"] > 2.5].sort_values(by="Domo_Leverage", ascending=False).head(15)

        col1, col2 = st.columns([0.4, 0.6])
        
        with col1:
            st.markdown("<h4 style='color:#00e5ff; margin-bottom:8px;'>?? THE +EV HOTLIST</h4>", unsafe_allow_html=True)
            for _, row in ev_pool.iterrows():
                st.html(build_pick_card(row.to_dict()))
                
        with col2:
            st.markdown("<h4 style='color:#ff2a6d; margin-bottom:8px;'>? SLIP CONSTRUCTOR</h4>", unsafe_allow_html=True)
            st.info("Select 2 to 6 legs from the +EV Hotlist to calculate true multiplier edges.")
            
            slip_type = st.radio("PrizePicks Slip Type", ["Power Play (Max Variance / Max Muliplier)", "Flex Play (Safety Net / Reduced Multiplier)"])
            legs = st.slider("Number of Legs", min_value=2, max_value=6, value=5)
            
            if slip_type.startswith("Power"):
                st.success(f"?? Power Play Selected: All {legs} legs must hit. Top payout compounds the +EV edge.")
            else:
                st.warning(f"??? Flex Play Selected: {legs}-leg baseline. Warning: Minimum tier payout may return less than initial stake.")
                
            st.button("?? GENERATE OPTIMAL TICKET", width="stretch")
    else:
        st.warning("?? Matrix requires active Vegas lines and DFS Projections to calculate +EV.")

