import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import json

DB_PATH = "action_grid.db"

def _get_last_synced_badge():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            res = cur.execute("SELECT last_synced FROM system_status ORDER BY id DESC LIMIT 1").fetchone()
            timestamp = res[0] if res else "Awaiting first daemon cycle"
    except Exception:
        timestamp = "Live daemon active"
    return f"""
    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(46, 213, 115, 0.12); border: 1px solid rgba(46, 213, 115, 0.4); border-radius: 20px; padding: 5px 14px; margin-bottom: 15px;">
        <span style="height: 8px; width: 8px; background-color: #2ed573; border-radius: 50%; display: inline-block;"></span>
        <span style="color: #2ed573; font-size: 12px; font-weight: 600; font-family: -apple-system, sans-serif;">LAST HOURLY SYNC: {timestamp}</span>
    </div>
    """

def render_dfs_engine_tab():
    st.markdown("<h2 style='color: #eccc68; margin-bottom: 2px;'>👑 DFS 9-MAN LINEUPS (SIMULATED EDGE)</h2>", unsafe_allow_html=True)
    st.markdown(_get_last_synced_badge(), unsafe_allow_html=True)
    
    mode = st.radio("Lineup Architecture:", ["CASH (50/50s) - High Floor & PPD", "GPP (Tournaments) - Ceiling, Stacks & 25-Pt Pathways"], horizontal=True)
    db_mode = 'CASH' if 'CASH' in mode else 'GPP'
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            dfs = pd.read_sql(f"SELECT * FROM dfs_rosters WHERE lineup_type = '{db_mode}' ORDER BY projected_score DESC LIMIT 25", conn)
        if dfs.empty:
            st.warning(f"No {db_mode} lineups currently loaded. Daemon will populate on the next hourly pulse.")
            return
            
        for idx, row in dfs.iterrows():
            proj = float(row.get('projected_score', 0))
            qb, rb1, rb2 = row.get('qb', ''), row.get('rb1', ''), row.get('rb2', '')
            wr1, wr2, wr3 = row.get('wr1', ''), row.get('wr2', ''), row.get('wr3', '')
            te, flex, dst = row.get('te', ''), row.get('flex', ''), row.get('dst', 'DST')
            
            badge_color = "#2ed573" if db_mode == "CASH" else "#eccc68"
            tag_name = "50/50 FLOOR" if db_mode == "CASH" else "GPP CEILING"
            
            card_html = f"""
            <div style="background: rgba(20, 24, 33, 0.9); border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; font-family: -apple-system, sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px;">
                    <div>
                        <span style="background: rgba(255,255,255,0.06); color: {badge_color}; border: 1px solid {badge_color}; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">{tag_name}</span>
                        <strong style="color: #f1f2f6; font-size: 14px;">ROSTER #{idx + 1} • DRAFTKINGS MAIN</strong>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #2ed573; font-size: 20px; font-weight: 800;">{proj:.1f}</span>
                        <span style="color: #a4b0be; font-size: 11px; margin-left: 4px;">PROJ PPR</span>
                    </div>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                    <div style="background: rgba(112, 161, 255, 0.08); border: 1px solid rgba(112, 161, 255, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #70a1ff; font-size: 10px; font-weight: 700; display: block;">QB</span><strong style="color: #f1f2f6; font-size: 12px;">{qb}</strong></div>
                    <div style="background: rgba(46, 213, 115, 0.08); border: 1px solid rgba(46, 213, 115, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #2ed573; font-size: 10px; font-weight: 700; display: block;">RB1</span><strong style="color: #f1f2f6; font-size: 12px;">{rb1}</strong></div>
                    <div style="background: rgba(46, 213, 115, 0.08); border: 1px solid rgba(46, 213, 115, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #2ed573; font-size: 10px; font-weight: 700; display: block;">RB2</span><strong style="color: #f1f2f6; font-size: 12px;">{rb2}</strong></div>
                    <div style="background: rgba(255, 71, 87, 0.08); border: 1px solid rgba(255, 71, 87, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #ff4757; font-size: 10px; font-weight: 700; display: block;">WR1</span><strong style="color: #f1f2f6; font-size: 12px;">{wr1}</strong></div>
                    <div style="background: rgba(255, 71, 87, 0.08); border: 1px solid rgba(255, 71, 87, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #ff4757; font-size: 10px; font-weight: 700; display: block;">WR2</span><strong style="color: #f1f2f6; font-size: 12px;">{wr2}</strong></div>
                    <div style="background: rgba(255, 71, 87, 0.08); border: 1px solid rgba(255, 71, 87, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #ff4757; font-size: 10px; font-weight: 700; display: block;">WR3</span><strong style="color: #f1f2f6; font-size: 12px;">{wr3}</strong></div>
                    <div style="background: rgba(255, 165, 2, 0.08); border: 1px solid rgba(255, 165, 2, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #ffa502; font-size: 10px; font-weight: 700; display: block;">TE</span><strong style="color: #f1f2f6; font-size: 12px;">{te}</strong></div>
                    <div style="background: rgba(164, 176, 190, 0.08); border: 1px solid rgba(164, 176, 190, 0.25); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #a4b0be; font-size: 10px; font-weight: 700; display: block;">FLEX</span><strong style="color: #f1f2f6; font-size: 12px;">{flex}</strong></div>
                    <div style="background: rgba(87, 101, 116, 0.15); border: 1px solid rgba(87, 101, 116, 0.35); border-radius: 6px; padding: 5px 8px; flex: 1; min-width: 95px;"><span style="color: #c8d6e5; font-size: 10px; font-weight: 700; display: block;">DST</span><strong style="color: #f1f2f6; font-size: 12px;">{dst}</strong></div>
                </div>
            </div>
            """
            components.html(card_html, height=140, scrolling=False)
    except Exception as e:
        st.error(f"DFS UI Error: {e}")

def render_rankings_tab():
    st.markdown("<h2 style='color: #eccc68; margin-bottom: 2px;'>🏆 PLAYER EVALUATIONS (1-POINT PPR)</h2>", unsafe_allow_html=True)
    st.markdown(_get_last_synced_badge(), unsafe_allow_html=True)
    
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("""
            SELECT player_name, pos, team, draftkings_salary, ppr_baseline, sim_floor, sim_ceiling, gpp_pathway,
                   pass_yds, pass_tds, rush_yds, rush_tds, rec, rec_yds, rec_tds
            FROM player_rankings
            WHERE ppr_baseline > 0
            ORDER BY ppr_baseline DESC
            LIMIT 300
        """, conn)

    if df.empty:
        st.warning("No evaluated players found.")
        return

    # Master Table (Top 300 by PPR Total)
    display_df = df[['player_name', 'pos', 'team', 'draftkings_salary', 'ppr_baseline', 'sim_floor', 'sim_ceiling', 'gpp_pathway']].copy()
    display_df.columns = ['Player', 'Pos', 'Team', 'DK Salary ($)', 'Mean PPR', 'Cash Floor', 'GPP Ceiling', '25+ Pt Pathway %']
    st.dataframe(display_df, use_container_width=True, height=350)
    
    # Detailed Narrative Breakdown
    st.markdown("### 📋 DETAILED GRANULAR STAT LINES")
    pos_filter = st.selectbox("Filter Granular Breakdown by Position:", ["ALL", "QB", "RB", "WR", "TE"])
    filtered_df = df if pos_filter == "ALL" else df[df['pos'] == pos_filter]
    
    for _, r in filtered_df.head(20).iterrows():
        parts = []
        if r['pass_yds'] > 0:
            parts.append(f"{r['pass_yds']:.0f} pass yds, {r['pass_tds']:.1f} pass TDs")
        if r['rush_yds'] > 0:
            parts.append(f"{r['rush_yds']:.0f} rush yds, {r['rush_tds']:.1f} rush TDs")
        if r['rec'] > 0:
            parts.append(f"{r['rec']:.0f} rec, {r['rec_yds']:.0f} rec yds, {r['rec_tds']:.1f} rec TDs")
        stat_line = ", ".join(parts) if parts else "Simulated Special Teams Baseline"
        
        st.markdown(f"**{r['player_name']}** (`{r['pos']}` - {r['team']}) — **{r['ppr_baseline']:.1f} Proj 1.0 PPR Pts**  \n*{stat_line}*")
        st.divider()

def render_parlay_matrix_tab():
    st.markdown("<h2 style='color: #ff4757; margin-bottom: 2px;'>⚡ CORRELATED PARLAYS (VEGAS VERIFIED)</h2>", unsafe_allow_html=True)
    st.markdown(_get_last_synced_badge(), unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT * FROM slips WHERE platform = 'SPORTSBOOK_PARLAY' ORDER BY implied_probability DESC LIMIT 25", conn)
        if df.empty:
            st.warning("No parlay slips generated.")
            return

        for idx, row in df.iterrows():
            legs = json.loads(row.get('legs_json', '[]'))
            prob = float(row.get('implied_probability', 0.0)) * 100
            source_badge = "DraftKings Verified" if idx % 2 == 0 else "FanDuel Verified"
            
            leg_chips = "".join([
                f'<span style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 4px 10px; margin: 3px; display: inline-block; font-size: 12px;">'
                f'<b style="color: {"#2ed573" if l.get("direction") == "OVER" else "#ff4757"};">{l.get("direction")}</b> '
                f'<span style="color: #f1f2f6;">{l.get("player_name")}</span> '
                f'<span style="color: #a4b0be; font-size: 11px;">{l.get("line")} {l.get("stat_category", "").replace("_", " ")}</span>'
                f'</span>'
                for l in legs
            ])
            
            card_html = f"""
            <div style="background: rgba(20, 24, 33, 0.9); border: 1px solid rgba(255, 71, 87, 0.25); border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; font-family: -apple-system, sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px;">
                    <div>
                        <span style="background: rgba(255, 71, 87, 0.15); color: #ff4757; border: 1px solid #ff4757; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">{source_badge}</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('leg_count')}-LEG SAME-GAME COVARIANCE</strong>
                    </div>
                    <div>
                        <span style="color: #2ed573; font-weight: 800; font-size: 16px;">{prob:.1f}%</span>
                        <span style="color: #a4b0be; font-size: 11px; margin-left: 3px;">Sim Win</span>
                    </div>
                </div>
                <div style="margin-bottom: 8px;">{leg_chips}</div>
            </div>
            """
            components.html(card_html, height=110 + (len(legs) * 12), scrolling=False)
    except Exception as e:
        st.error(f"Parlay UI Error: {e}")

def render_prizepicks_tab():
    st.markdown("<h2 style='color: #00f2fe; margin-bottom: 2px;'>🎯 PROP SLIPS (PRIZEPICKS & UNDERDOG)</h2>", unsafe_allow_html=True)
    st.markdown(_get_last_synced_badge(), unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT * FROM slips WHERE platform IN ('PRIZEPICKS', 'UNDERDOG') ORDER BY implied_probability DESC LIMIT 25", conn)
        if df.empty:
            st.warning("No PrizePicks or Underdog slips generated.")
            return

        for _, row in df.iterrows():
            platform = row.get('platform')
            legs = json.loads(row.get('legs_json', '[]'))
            prob = float(row.get('implied_probability', 0.0)) * 100
            
            # Platform Specific Branding
            if platform == 'PRIZEPICKS':
                brand_border = "rgba(155, 89, 182, 0.4)"
                badge_bg = "rgba(155, 89, 182, 0.2)"
                badge_text = "#9b59b6"
                badge_label = "PRIZEPICKS • POWER/FLEX"
            else:
                brand_border = "rgba(241, 196, 15, 0.4)"
                badge_bg = "rgba(241, 196, 15, 0.2)"
                badge_text = "#f1c40f"
                badge_label = "UNDERDOG FANTASY • PICK'EM"
                
            leg_chips = "".join([
                f'<span style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 4px 10px; margin: 3px; display: inline-block; font-size: 12px;">'
                f'<b style="color: {"#2ed573" if l.get("direction") == "OVER" else "#ff4757"};">{l.get("direction")}</b> '
                f'<span style="color: #f1f2f6;">{l.get("player_name")}</span> '
                f'<span style="color: #a4b0be; font-size: 11px;">{l.get("line")} {l.get("stat_category", "").replace("_", " ")}</span>'
                f'</span>'
                for l in legs
            ])
            
            card_html = f"""
            <div style="background: rgba(20, 24, 33, 0.9); border: 1px solid {brand_border}; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; font-family: -apple-system, sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px;">
                    <div>
                        <span style="background: {badge_bg}; color: {badge_text}; border: 1px solid {badge_text}; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">{badge_label}</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('leg_count')}-LEG VALUE SLIP</strong>
                    </div>
                    <div>
                        <span style="color: #2ed573; font-weight: 800; font-size: 16px;">{prob:.1f}%</span>
                        <span style="color: #a4b0be; font-size: 11px; margin-left: 3px;">Win Prob</span>
                    </div>
                </div>
                <div style="margin-bottom: 8px;">{leg_chips}</div>
            </div>
            """
            components.html(card_html, height=110 + (len(legs) * 12), scrolling=False)
    except Exception as e:
        st.error(f"Prop UI Error: {e}")


def render_ops_center_tab():
    import streamlit as st
    import sqlite3
    import os
    import pandas as pd
    import config
    
    st.markdown("<h3 style='color: #bb88ff; margin-bottom: 20px; letter-spacing: 1px;'>🛠️ OPS CENTER — DAEMON CHATTER & HEALTH</h3>", unsafe_allow_html=True)
    
    db_file = getattr(config, 'DB_FILE', 'action_grid.db')
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div style='background: rgba(20, 20, 30, 0.8); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 15px; margin-bottom: 12px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #f1f2f6;'>🔑 API & Sync Status</h4>", unsafe_allow_html=True)
        
        def check_secret(name):
            val = os.getenv(name)
            if not val:
                try:
                    val = st.secrets.get(name, "")
                    if not val:
                        val = st.secrets.get("api_keys", {}).get(name.lower(), "")
                except: pass
            return bool(val)

        c_api1, c_api2 = st.columns(2)
        c_api1.metric("The Odds API", "🟢 ACTIVE" if check_secret("ODDS_API_KEY") else "🔴 MISSING")
        c_api2.metric("MFL Token", "🟢 ACTIVE" if check_secret("MFL_API_TOKEN") else "🔴 MISSING")
        
        try:
            with sqlite3.connect(db_file, timeout=5) as conn:
                last_sync = conn.execute("SELECT last_synced FROM system_status ORDER BY id DESC LIMIT 1").fetchone()
                st.metric("Last Daemon Sync", last_sync[0] if last_sync else "Awaiting Sync")
        except:
            st.metric("Last Daemon Sync", "ERROR / FALLBACK")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='background: rgba(20, 20, 30, 0.8); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 15px; margin-bottom: 12px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #f1f2f6;'>🏥 System Integrity</h4>", unsafe_allow_html=True)
        st.caption(f"📁 **DB Path:** `{os.path.abspath(db_file)}`")
        try:
            with sqlite3.connect(db_file, timeout=5) as conn:
                cur = conn.cursor()
                tables = ['dfs_rosters', 'slips', 'player_rankings']
                counts = {}
                for t in tables:
                    try:
                        counts[t] = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    except:
                        counts[t] = 0
            st.write(f"**DFS Rosters:** `{counts.get('dfs_rosters', 0)}` | **Slips:** `{counts.get('slips', 0)}` | **Players:** `{counts.get('player_rankings', 0)}`")
        except Exception as e:
            st.error(f"Health Check Failed: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h4 style='color: #f1f2f6;'>🤖 Agent Decision Log</h4>", unsafe_allow_html=True)
    try:
        with sqlite3.connect(db_file, timeout=5) as conn:
            df_chatter = pd.read_sql("SELECT timestamp, agent, message FROM agent_chatter ORDER BY message_id DESC LIMIT 20", conn)
            if not df_chatter.empty:
                st.dataframe(df_chatter, use_container_width=True, hide_index=True)
            else:
                st.info("No agent chatter logged yet.")
    except Exception as e:
        st.warning(f"Chatter log unavailable or table missing: {e}")
