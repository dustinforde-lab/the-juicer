import os

code_to_inject = '''
def render_donna_matrix(*a, **k):
    inject_elite_aesthetic()
    st.markdown("<h3 class='neon-title'>📊 DONNA'S POSITIONAL LEVERAGE & PLAYER MATRIX</h3>", unsafe_allow_html=True)
    
    # Static position map for premier NFL players as an instant fallback
    KNOWN_POS = {
        "Patrick Mahomes": ("QB", "KC"), "Josh Allen": ("QB", "BUF"), "Lamar Jackson": ("QB", "BAL"),
        "Jalen Hurts": ("QB", "PHI"), "Dak Prescott": ("QB", "DAL"), "Caleb Williams": ("QB", "CHI"),
        "Justin Herbert": ("QB", "LAC"), "Jayden Daniels": ("QB", "WAS"), "Carson Wentz": ("QB", "MIN"),
        "Brock Purdy": ("QB", "SF"), "Jordan Love": ("QB", "GB"), "Joe Burrow": ("QB", "CIN"),
        "C.J. Stroud": ("QB", "HOU"), "Kirk Cousins": ("QB", "LV"), "Baker Mayfield": ("QB", "TB"),
        "Breece Hall": ("RB", "NYJ"), "Bijan Robinson": ("RB", "ATL"), "Christian McCaffrey": ("RB", "SF"),
        "Jahmyr Gibbs": ("RB", "DET"), "Saquon Barkley": ("RB", "PHI"), "Derrick Henry": ("RB", "BAL"),
        "De\'Von Achane": ("RB", "MIA"), "Aaron Jones": ("RB", "MIN"), "Javonte Williams": ("RB", "DAL"),
        "Kenneth Walker": ("RB", "KC"), "Kyren Williams": ("RB", "LAR"), "D\'Andre Swift": ("RB", "CHI"),
        "Chuba Hubbard": ("RB", "CAR"), "Quinshon Judkins": ("RB", "CLE"), "Ashton Jeanty": ("RB", "LV"),
        "CeeDee Lamb": ("WR", "DAL"), "Justin Jefferson": ("WR", "MIN"), "Ja\'Marr Chase": ("WR", "CIN"),
        "Amon-Ra St. Brown": ("WR", "DET"), "Garrett Wilson": ("WR", "NYJ"), "Terry McLaurin": ("WR", "WAS"),
        "Quentin Johnston": ("WR", "LAC"), "Luther Burden": ("WR", "CHI"), "George Pickens": ("WR", "DAL"),
        "Rome Odunze": ("WR", "CHI"), "Rashod Bateman": ("WR", "BAL"), "Matthew Golden": ("WR", "GB"),
        "Denzel Boston": ("WR", "CLE"), "Kayshon Boutte": ("WR", "HOU"), "Wan\'Dale Robinson": ("WR", "TEN"),
        "Travis Kelce": ("TE", "KC"), "Mark Andrews": ("TE", "BAL"), "Trey McBride": ("TE", "ARI"),
        "George Kittle": ("TE", "SF"), "Sam LaPorta": ("TE", "DET"), "Dalton Kincaid": ("TE", "BUF"),
        "Dalton Schultz": ("TE", "HOU"), "Colston Loveland": ("TE", "CHI"), "Luke Farrell": ("TE", "SF"),
        "Michael Mayer": ("TE", "LV"), "Kyle Pitts": ("TE", "ATL"), "T.J. Hockenson": ("TE", "MIN")
    }

    try:
        with sqlite3.connect(DB) as conn:
            df = pd.read_sql("SELECT * FROM player_rankings", conn)
            
        if df.empty:
            st.warning("⚠️ No player records available in player_rankings.")
            return

        # Normalize column headers
        cols_lower = {c.lower(): c for c in df.columns}
        p_col = cols_lower.get("player_name") or cols_lower.get("player") or "player"
        pos_col = cols_lower.get("pos") or cols_lower.get("position") or cols_lower.get("pos_abbr")
        team_col = cols_lower.get("team") or cols_lower.get("team_abbr") or "team"
        fp_col = cols_lower.get("fp") or cols_lower.get("projected_fp") or cols_lower.get("fantasy_points") or cols_lower.get("projected_pts")
        line_col = cols_lower.get("consensus_line") or cols_lower.get("line") or "line"
        stat_col = cols_lower.get("stat_category") or cols_lower.get("stat") or "stat"

        df_clean = pd.DataFrame()
        df_clean["player"] = df[p_col]
        df_clean["pos"] = df[pos_col] if pos_col else "N/A"
        df_clean["team"] = df[team_col] if team_col else "FA"
        df_clean["fp"] = pd.to_numeric(df[fp_col], errors="coerce").fillna(0.0) if fp_col else 0.0
        df_clean["line"] = df[line_col] if line_col in df.columns else "N/A"
        df_clean["stat"] = df[stat_col] if stat_col in df.columns else "FP"

        # Apply fallback for missing position and team tags
        for idx, row in df_clean.iterrows():
            p_name = row["player"]
            if (row["pos"] == "N/A" or not row["pos"]) and p_name in KNOWN_POS:
                df_clean.at[idx, "pos"] = KNOWN_POS[p_name][0]
                if row["team"] in ("FA", "N/A", ""):
                    df_clean.at[idx, "team"] = KNOWN_POS[p_name][1]
            if df_clean.at[idx, "fp"] == 0.0:
                # Baseline projection estimates if uncomputed
                pos = df_clean.at[idx, "pos"]
                df_clean.at[idx, "fp"] = 18.5 if pos == "QB" else 15.2 if pos == "RB" else 14.8 if pos == "WR" else 10.4 if pos == "TE" else 12.0

        # Group stats by unique player
        records = []
        for (player, pos, team), group in df_clean.groupby(["player", "pos", "team"]):
            max_fp = group["fp"].max()
            stats_list = group[["stat", "line"]].to_dict("records")
            records.append({
                "Player": player,
                "Pos": pos,
                "Team": team,
                "Proj FP": round(max_fp, 1),
                "Stats": stats_list
            })

        master_df = pd.DataFrame(records).sort_values("Proj FP", ascending=False).reset_index(drop=True)
        master_df.insert(0, "Rank", master_df.index + 1)

        # Top Bar: Quick Search
        c_filter, c_metric = st.columns([3, 1])
        with c_filter:
            search_query = st.text_input("🔍 Quick Player Search:", placeholder="Filter by player or team name...").strip().lower()
        with c_metric:
            st.metric("Total Players Board", len(master_df))

        if search_query:
            display_df = master_df[master_df["Player"].str.lower().str.contains(search_query) | master_df["Team"].str.lower().str.contains(search_query)]
        else:
            display_df = master_df

        col_table, col_cards = st.columns([1.1, 1.9])

        with col_table:
            st.markdown("#### 🏆 Leaderboard Matrix")
            st.dataframe(
                display_df[["Rank", "Player", "Pos", "Team", "Proj FP"]].head(300),
                use_container_width=True,
                height=720,
                hide_index=True
            )

        with col_cards:
            st.markdown("#### 🃏 Positional Intelligence & Matchup Cards")
            tabs = st.tabs(["ALL", "QB (50)", "RB (50)", "WR (75)", "TE (50)", "FLEX (50)"])

            def render_player_cards(filtered_subset):
                with st.container(height=660):
                    if filtered_subset.empty:
                        st.info("No players match this position category.")
                        return

                    for _, r in filtered_subset.iterrows():
                        stats = r["Stats"]
                        fp_val = r["Proj FP"]
                        team = r["Team"]

                        if fp_val > 18:
                            analysis_text = f"Priority leverage candidate. Matchup game script projects heavy volume for {team} with explosive ceiling potential."
                        elif fp_val > 13:
                            analysis_text = f"Stable median projection with a protected volume floor. Ideal cash or high-floor flex consideration."
                        else:
                            analysis_text = f"Secondary tournament option. Snap rate or game script caps upside in primary 9-man configurations."

                        stat_badges = ""
                        for s in stats:
                            st_name = str(s.get("stat", "")).replace("_", " ").title()
                            st_line = str(s.get("line", ""))
                            if st_name and st_name != "Fp" and st_line != "N/A":
                                stat_badges += f'<div class="stat-badge">{st_name}: <span class="stat-val">{st_line}</span></div>'

                        st.markdown(f"""
                        <div class="player-card">
                            <div class="card-header">
                                <div>
                                    <span class="p-pos">{r["Pos"]}</span>
                                    <span class="p-name">{r["Player"]}</span>
                                    <span class="p-team">({team})</span>
                                </div>
                                <div class="p-fp">{fp_val:.1f} FP</div>
                            </div>
                            <div class="stat-container">
                                {stat_badges if stat_badges else '<div class="stat-badge">Standard Target Projections Active</div>'}
                            </div>
                            <div class="analysis-box">
                                <span class="analysis-label">Mike & Donna Syndicate Diagnosis</span>
                                {analysis_text}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            with tabs[0]: render_player_cards(display_df.head(50))
            with tabs[1]: render_player_cards(display_df[display_df["Pos"] == "QB"].head(50))
            with tabs[2]: render_player_cards(display_df[display_df["Pos"] == "RB"].head(50))
            with tabs[3]: render_player_cards(display_df[display_df["Pos"] == "WR"].head(75))
            with tabs[4]: render_player_cards(display_df[display_df["Pos"] == "TE"].head(50))
            with tabs[5]: render_player_cards(display_df[display_df["Pos"].isin(["RB", "WR", "TE"])].head(50))

    except Exception as e:
        st.error(f"Error rendering player matrix: {e}")
'''

# Update ui_components.py
with open("ui_components.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace existing render_donna_matrix function
start_marker = "def render_donna_matrix(*a, **k):"
if start_marker in text:
    parts = text.split(start_marker)
    # The next function starts with def render_season_long
    next_func_marker = "def render_season_long(*a, **k):"
    if next_func_marker in parts[1]:
        donna_block, rest = parts[1].split(next_func_marker, 1)
        new_text = parts[0] + code_to_inject.strip() + "\n\n" + next_func_marker + rest
    else:
        new_text = parts[0] + code_to_inject.strip()
else:
    new_text = text + "\n\n" + code_to_inject.strip()

with open("ui_components.py", "w", encoding="utf-8") as f:
    f.write(new_text)

print("✅ ui_components.py successfully patched with the upgraded Matrix & Cards UI.")