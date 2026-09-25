import os

with open("ui_components.py", "r", encoding="utf-8") as f:
    text = f.read()

# Locate and replace the DFS optimizer rendering section inside ui_components.py
# We will inject custom HTML cards with position color-coding
old_dfs_render_marker = "def render_dfs_optimizer"

# Let's write a targeted patch for the DFS cards
patch_snippet = '''
def render_dfs_optimizer(*a, **k):
    inject_elite_aesthetic()
    st.markdown("<h3 class='neon-title'>👑 DFS OPTIMIZER ENGINE (LOCKED & LOADED)</h3>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB) as conn:
            df = pd.read_sql("SELECT * FROM dfs_classic_lineups ORDER BY projected_pts DESC LIMIT 200", conn)
            
        if df.empty:
            st.warning("⚠️ No optimized lineups found. Run your builder script first.")
            return

        for idx, row in df.iterrows():
            lineup_id = row.get("id", idx + 1)
            lineup_type = row.get("lineup_type", "GPP")
            proj = row.get("projected_pts", 0.0)
            roster_json = row.get("roster_json", "[]")
            
            try:
                roster = json.loads(roster_json)
            except:
                roster = []

            with st.expander(f"🏈 Lineup #{lineup_id} | Type: {lineup_type} | Proj: {proj:.2f} FP"):
                st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 10px; margin-top: 5px;'>", unsafe_allow_html=True)
                
                pos_colors = {
                    "QB": "background: rgba(0, 242, 254, 0.15); color: #00f2fe; border: 1px solid #00f2fe;",
                    "RB": "background: rgba(46, 213, 115, 0.15); color: #2ed573; border: 1px solid #2ed573;",
                    "WR": "background: rgba(255, 71, 87, 0.15); color: #ff4757; border: 1px solid #ff4757;",
                    "TE": "background: rgba(255, 165, 2, 0.15); color: #ffa502; border: 1px solid #ffa502;",
                    "FLEX": "background: rgba(165, 94, 234, 0.15); color: #a55eea; border: 1px solid #a55eea;",
                    "DST": "background: rgba(112, 161, 255, 0.15); color: #70a1ff; border: 1px solid #70a1ff;"
                }

                for p in roster:
                    pos = p.get("pos", "FLEX")
                    name = p.get("name", "Unknown")
                    style = pos_colors.get(pos, pos_colors["FLEX"])
                    
                    st.markdown(f"""
                    <div style="{style} padding: 8px 12px; border-radius: 8px; font-family: monospace; font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
                        <span style="opacity: 0.8; font-size: 11px;">[{pos}]</span> {name}
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading DFS lineups: {e}")
'''

if old_dfs_render_marker in text:
    # Replace the render_dfs_optimizer block
    parts = text.split(old_dfs_render_marker)
    # find next function or end of file
    next_func_idx = parts[1].find("\ndef ")
    if next_func_idx != -1:
        rest = parts[1][next_func_idx:]
        new_text = parts[0] + patch_snippet.strip() + "\n\n" + rest
    else:
        new_text = parts[0] + patch_snippet.strip()
        
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("✅ Successfully patched DFS Engine with color-coded positional card UI.")
else:
    print("⚠️ render_dfs_optimizer function not found.")