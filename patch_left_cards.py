import os

with open("ui_components.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the table rendering block on the left with a compact card container
old_left_block = '''        with col_table:
            st.markdown("#### 🏆 Leaderboard Matrix")
            st.dataframe(
                display_df[["Rank", "Player", "Pos", "Team", "Proj FP"]].head(300),
                column_config={
                    "Rank": st.column_config.NumberColumn("Rank", width="small", format="%d"),
                    "Player": st.column_config.TextColumn("Player", width="medium"),
                    "Pos": st.column_config.TextColumn("Pos", width="small"),
                    "Team": st.column_config.TextColumn("Team", width="small"),
                    "Proj FP": st.column_config.NumberColumn("Proj FP", width="small", format="%.1f")
                },
                use_container_width=True,
                height=720,
                hide_index=True
            )'''

new_left_block = '''        with col_table:
            st.markdown("#### 🏆 Master Player List")
            with st.container(height=720):
                if display_df.empty:
                    st.info("No players found.")
                else:
                    for _, r in display_df.head(300).iterrows():
                        st.markdown(f"""
                        <div class="player-card" style="padding: 10px 14px; margin-bottom: 8px;">
                            <div class="card-header" style="margin-bottom: 0px;">
                                <div>
                                    <span class="p-pos" style="font-size: 11px; padding: 2px 6px;">{r["Pos"]}</span>
                                    <span class="p-name" style="font-size: 13px;">#{r["Rank"]} {r["Player"]}</span>
                                    <span class="p-team" style="font-size: 11px;">({r["Team"]})</span>
                                </div>
                                <div class="p-fp" style="font-size: 14px;">{r["Proj FP"]:.1f} FP</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)'''

if old_left_block in text:
    text = text.replace(old_left_block, new_left_block)
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ Successfully replaced the left leaderboard table with compact player cards.")
else:
    print("⚠️ Target block not found. Checking alternate signatures...")