import os

code_to_inject = """
def render_season_long(*a, **k):
    inject_elite_aesthetic()
    st.markdown("<h3 class='neon-title'>🏈 SEASON-LONG OPERATIONS & WAIVER WIRE</h3>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB) as conn:
            rosters_df = pd.read_sql("SELECT * FROM season_long_rosters", conn)
            rankings_df = pd.read_sql("SELECT player_name, pos, projected_fp, ceiling_fp FROM player_rankings", conn)
            
        if rosters_df.empty:
            st.warning("⚠️ No season-long data found. Ensure the background scheduler is running.")
            return
            
        # Get unique leagues
        leagues = rosters_df[['platform', 'league_name', 'league_id']].drop_duplicates()
        league_options = [f"[{r['platform']}] {r['league_name']}" for _, r in leagues.iterrows()]
        
        if not league_options:
            return
            
        selected_league_str = st.selectbox("Select League Workspace:", league_options)
        
        # Filter to selected league
        selected_platform = selected_league_str.split("] ")[0].replace("[", "")
        selected_league_name = selected_league_str.split("] ")[1]
        
        league_df = rosters_df[(rosters_df['platform'] == selected_platform) & (rosters_df['league_name'] == selected_league_name)]
        
        my_team_df = league_df[league_df['status'].isin(['ROSTER', 'BENCH'])]
        free_agents_df = league_df[league_df['status'] == 'FREE_AGENT']
        
        # Join with Juicer projections
        my_team_proj = pd.merge(my_team_df, rankings_df, on=['player_name', 'pos'], how='inner').sort_values('projected_fp', ascending=False)
        fa_proj = pd.merge(free_agents_df, rankings_df, on=['player_name', 'pos'], how='inner').sort_values('projected_fp', ascending=False)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🛡️ Your Active Roster")
            st.dataframe(
                my_team_proj[['player_name', 'pos', 'status', 'projected_fp', 'ceiling_fp']], 
                use_container_width=True, 
                hide_index=True,
                height=500
            )
            
        with col2:
            st.markdown("#### 🚨 The Juicer's Waiver Targets")
            st.dataframe(
                fa_proj[['player_name', 'pos', 'projected_fp', 'ceiling_fp']].head(15), 
                use_container_width=True, 
                hide_index=True,
                height=500
            )
            
        # Actionable AI Recommendation
        st.markdown("---")
        if not my_team_proj.empty and not fa_proj.empty:
            weakest_link = my_team_proj.iloc[-1]
            top_pickup = fa_proj.iloc[0]
            
            if top_pickup['projected_fp'] > weakest_link['projected_fp']:
                st.success(f"**JUICER SYNDICATE DIRECTIVE:** Drop **{weakest_link['player_name']}** ({weakest_link['projected_fp']:.1f} FP) and claim **{top_pickup['player_name']}** ({top_pickup['projected_fp']:.1f} FP) off the waiver wire.")
            else:
                st.info("Your weakest bench player currently projects higher than the top available free agent. Hold steady.")
                
    except Exception as e:
        st.error(f"Error rendering season-long tab: {e}")
"""

with open("ui_components.py", "r", encoding="utf-8") as f:
    text = f.read()

start_marker = "def render_season_long(*a, **k):"
if start_marker in text:
    parts = text.split(start_marker)
    next_func_idx = parts[1].find("\ndef ")
    if next_func_idx != -1:
        rest = parts[1][next_func_idx:]
        new_text = parts[0] + code_to_inject.strip() + "\n" + rest
    else:
        new_text = parts[0] + code_to_inject.strip()
        
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("✅ Successfully patched Season-Long UI Tab.")
else:
    print("⚠️ render_season_long function not found in ui_components.py.")