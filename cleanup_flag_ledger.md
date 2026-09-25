# 🧹 THE JUICER: CLEANUP FLAG LEDGER
*AI INSTRUCTION: Log messy code, deprecated functions, and redundant imports here. DO NOT delete them from the main codebase until explicitly instructed.*

| Date | File | Line/Function | Issue Description | Proposed Fix |
| :--- | :--- | :--- | :--- | :--- |
| 2026-09-24 | ui_the_rankings.py | get_positional_showdown_data() | Hardcoded mock data. | Route to data_service.py once Evaluator 3.0 SQL ingest is finalized. |
| 2026-09-24 | ui_dfs.py / ui_the_rankings.py | Raw Dataframes | Replaced with vertical scrollable glassmorphic cards to match UI guidelines. Old df rendering commented out. |
