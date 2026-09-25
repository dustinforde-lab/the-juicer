import pandas as pd
import os

src = "Juicer_Showdown_GPP_150.csv"
dst = "DK_Upload_Showdown_150.csv"

if os.path.exists(src):
    df = pd.read_csv(src)
    # DraftKings strictly requires CPT and repeated FLEX column headers
    dk_df = df[["CPT", "FLEX_1", "FLEX_2", "FLEX_3", "FLEX_4", "FLEX_5"]].copy()
    dk_df.columns = ["CPT", "FLEX", "FLEX", "FLEX", "FLEX", "FLEX"]
    dk_df.to_csv(dst, index=False)
    print(f"✅ CLEAN EXPORT: Formatted 150 lineups into {dst} (DraftKings Batch Upload Ready).")
else:
    print(f"⚠️ {src} not found. Run dfs_solver.py first.")
