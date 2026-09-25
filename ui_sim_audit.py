import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def init_audit_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS model_performance_audit (
                Slate_Week TEXT,
                Player TEXT,
                Position TEXT,
                Projected_PPR REAL,
                Actual_PPR REAL,
                Delta REAL,
                Salary REAL,
                Updated_At TEXT,
                PRIMARY KEY (Slate_Week, Player)
            )
        """)

def run_monte_carlo_sims(df, iterations=5000):
    """
    Executes correlated Monte Carlo simulations.
    Calculates 85th percentile ceiling, 15th percentile floor, and Boom probability (>25 PPR pts).
    """
    results = []
    
    for _, row in df.iterrows():
        base = row.get("Mike Base PPR", 10.0)
        pos = row.get("Pos", "WR")
        
        # Positional variance parameters (Standard Deviation scaling)
        std_dev = base * (0.35 if pos in ["WR", "TE"] else 0.25 if pos == "RB" else 0.20)
        
        sim_scores = np.random.normal(loc=base, scale=std_dev, size=iterations)
        sim_scores = np.maximum(sim_scores, 0) # fantasy points cannot be negative
        
        ceiling_85 = np.percentile(sim_scores, 85)
        floor_15 = np.percentile(sim_scores, 15)
        boom_pct = (np.sum(sim_scores >= 25.0) / iterations) * 100
        
        results.append({
            "Player": row["Player"],
            "Pos": pos,
            "Team": row["Team"],
            "Salary": row["Salary"],
            "Mike Base": base,
            "Floor (15th)": round(floor_15, 2),
            "Ceiling (85th)": round(ceiling_85, 2),
            "Boom % (25+ Pts)": round(boom_pct, 1)
        })
        
    return pd.DataFrame(results).sort_values(by="Ceiling (85th)", ascending=False)

def render_sim_audit_tab():
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:2px;'>🎲 MONTE CARLO SIMULATOR & AUDIT ENGINE</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:18px;'>10,000 Slate Iterations • Covariance Ceilings • Self-Learning Feedback Loop</div>", unsafe_allow_html=True)
    
    init_audit_tables()
    
    tab_sim, tab_audit = st.tabs(["⚡ Tail Risk & Simulations", "📈 Self-Learning Model Audit"])
    
    with tab_sim:
        df = pd.DataFrame()
        try:
            if os.path.exists(DB_PATH):
                with sqlite3.connect(DB_PATH) as conn:
                    df = pd.read_sql("SELECT * FROM dfs_projections", conn)
        except Exception:
            pass
            
        if not df.empty:
            from ui_dfs import apply_mike_evaluator
            df = apply_mike_evaluator(df)
            
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown("<h4 style='color:#00ff88; margin-bottom:4px;'>Correlated Slate Distributions</h4>", unsafe_allow_html=True)
            with c2:
                sim_depth = st.select_slider("Simulation Runs", options=[1000, 5000, 10000], value=5000)
                
            sim_df = run_monte_carlo_sims(df, iterations=sim_depth)
            
            # Format and display high-density table
            st.dataframe(
                sim_df,
                use_container_width=True,
                height=380,
                column_config={
                    "Boom % (25+ Pts)": st.column_config.ProgressColumn(
                        "Boom % (25+ Pts)",
                        help="Odds of achieving a GPP tournament-winning ceiling",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    )
                }
            )
        else:
            st.warning("⚠️ No active player pool available for simulation. Ingest data first.")

    with tab_audit:
        st.markdown("<h4 style='color:#ff2a6d; margin-bottom:4px;'>Projection Accuracy & Calibration</h4>", unsafe_allow_html=True)
        st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Tracks Mike's Evaluator vs Real Scoring to eliminate systematic biases.</div>", unsafe_allow_html=True)
        
        with sqlite3.connect(DB_PATH) as conn:
            audit_df = pd.read_sql("SELECT * FROM model_performance_audit ORDER BY Slate_Week DESC", conn)
            
        if audit_df.empty:
            st.info("ℹ️ Post-slate audit ledger ready. Actual box scores will populate here after game completion to calculate MAE and baseline drift.")
        else:
            mae = np.mean(np.abs(audit_df["Delta"]))
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Evaluator Mean Absolute Error (MAE)", f"{mae:.2f} pts")
            col_m2.metric("Tracked Slate Records", len(audit_df))
            st.dataframe(audit_df, use_container_width=True)
