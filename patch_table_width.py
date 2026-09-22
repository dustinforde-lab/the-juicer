import os

with open("ui_components.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the broad st.dataframe call inside render_donna_matrix with configured column widths
old_df_render = '''        with col_table:
            st.markdown("#### 🏆 Leaderboard Matrix")
            st.dataframe(
                display_df[["Rank", "Player", "Pos", "Team", "Proj FP"]].head(300),
                use_container_width=True,
                height=720,
                hide_index=True
            )'''

new_df_render = '''        with col_table:
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

if old_df_render in text:
    text = text.replace(old_df_render, new_df_render)
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ Successfully tightened table column widths.")
else:
    print("⚠️ Target block already modified or not found.")