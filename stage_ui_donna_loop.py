"""
The Juicer - Donna Learning Loop & God-Mode Review Center
Displays Donna's betting record, qualitative debrief, and pending parameter tweaks with Approve/Reject toggles.
"""
import streamlit as st
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    conn.row_factory = sqlite3.Row
    return conn

def seed_sample_debrief_if_empty():
    with get_db() as conn:
        cnt = conn.execute("SELECT COUNT(*) FROM donna_learning_proposals").fetchone()[0]
        if cnt == 0:
            # Seed 2 realistic pending tweaks for God-Mode testing
            conn.execute("""
                INSERT INTO donna_learning_proposals (week_num, category, target_variable, current_value, proposed_value, rationale, status)
                VALUES 
                (3, 'Yardage Skew', 'wr_yardage_scalar', 1.06, 1.04, 'Consensus receiving yardage lines were slightly aggressive in Week 2; lowering over-skew multiplier to tighten floor.', 'PENDING_APPROVAL'),
                (3, 'Injury Decay', 'questionable_tag_penalty', 0.88, 0.82, 'WRs playing through ankle sprains averaged 18% lower snap counts; recommending stricter floor haircut.', 'PENDING_APPROVAL')
            """)
            conn.execute("""
                INSERT OR REPLACE INTO donna_weekly_debriefs (week_num, record_summary, net_units, debrief_markdown)
                VALUES (
                    3,
                    'DFS Cash: 85% Cash Rate | Parlays: 4-2 (+3.8u) | Pick''ems: 18-7 (72%)',
                    3.8,
                    '### 🧠 Donna''s Weekly Field Debrief — Week 3\n\n**What Worked:**\n* **High-Floor Showdown Cash:** The 2-stud RB foundation produced an 85% double-up conversion rate.\n* **Consensus Steam Following:** Catching Jordan Love''s line before the +8 yard move captured significant closing-line value (CLV).\n\n**What Underperformed:**\n* **Downfield WR Stacks:** Classic GPP stacks overweighted deep targets in windy weather profiles. Recommend reducing wind-tolerance threshold.\n\n**Proposed Action Items:**\nReview the two parameter tweaks below. Once approved, they will apply directly to Week 4 simulations.'
                )
            """)
            conn.commit()

def render_learning_loop_tab():
    seed_sample_debrief_if_empty()

    st.markdown("<h2 style='color:#00e5ff; margin-bottom:4px;'>🧠 DONNA'S LEARNING LOOP & DEBRIEF</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:16px;'>Autonomous Performance Telemetry, Weekly Audit Reports, and God-Mode Parameter Approval.</div>", unsafe_allow_html=True)

    with get_db() as conn:
        debrief = conn.execute("SELECT * FROM donna_weekly_debriefs ORDER BY week_num DESC LIMIT 1").fetchone()
        proposals = conn.execute("SELECT * FROM donna_learning_proposals WHERE status='PENDING_APPROVAL'").fetchall()

    # 1. Performance Telemetry Ribbon
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("DFS Cash Win Rate", "85.0%", "+5.0% vs target")
    with col2:
        st.metric("Parlay Units Net", "+3.80u", "ROI: +18.4%")
    with col3:
        st.metric("Pick'em Prop Accuracy", "72.0%", "18-7 record")
    with col4:
        st.metric("Active Proposals", f"{len(proposals)} Pending", "Needs God-Mode Review")

    st.markdown("---")

    # 2. Donna's Narrative Debrief
    if debrief:
        st.markdown(debrief["debrief_markdown"])
    else:
        st.info("Settlement engine runs Tuesday morning. Weekly debrief will populate following game completion.")

    st.markdown("---")

    # 3. God Mode Review Stage
    st.markdown("<h3 style='color:#ffd700; margin-bottom:8px;'>👑 GOD-MODE: PROPOSED MULTIPLIER TWEAKS</h3>", unsafe_allow_html=True)
    st.markdown("<div style='color:#cad3df; font-size:12px; margin-bottom:12px;'>Donna recommends these parameter adjustments based on last week's game script variance. You retain full veto power before they are committed to live production:</div>", unsafe_allow_html=True)

    if not proposals:
        st.success("All proposed adjustments have been processed. Engine operating on approved configuration.")
        return

    for p in proposals:
        pid = p["proposal_id"]
        cat = p["category"]
        var_name = p["target_variable"]
        cur_val = p["current_value"]
        prop_val = p["proposed_value"]
        rat = p["rationale"]

        with st.container():
            st.html(f"""
            <div style='background:rgba(18,24,38,0.9); border:1px solid rgba(255,215,0,0.3); border-radius:8px; padding:12px 14px; margin-bottom:10px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='color:#ffd700; font-weight:800; font-size:13px;'>{cat} • <code>{var_name}</code></span>
                    <span style='color:#8b949e; font-size:11px;'>Shift: <b style='color:#ff2a6d;'>{cur_val}</b> ➔ <b style='color:#00ff88;'>{prop_val}</b></span>
                </div>
                <div style='color:#cad3df; font-size:12px; margin-top:6px;'><b>Donna's Rationale:</b> {rat}</div>
            </div>
            """)

            btn_col1, btn_col2, btn_col3 = st.columns([0.25, 0.25, 0.5])
            with btn_col1:
                if st.button(f"✅ APPROVE TWEAK", key=f"app_{pid}", use_container_width=True):
                    with get_db() as conn:
                        conn.execute("UPDATE donna_learning_proposals SET status='APPROVED' WHERE proposal_id=?", (pid,))
                        conn.commit()
                    st.toast(f"Tweak {var_name} approved and pushed to live loop!", icon="✅")
                    st.rerun()

            with btn_col2:
                if st.button(f"🛑 REJECT / VETO", key=f"rej_{pid}", use_container_width=True):
                    with get_db() as conn:
                        conn.execute("UPDATE donna_learning_proposals SET status='REJECTED' WHERE proposal_id=?", (pid,))
                        conn.commit()
                    st.toast(f"Tweak {var_name} rejected. Kept at {cur_val}.", icon="🛑")
                    st.rerun()

if __name__ == "__main__":
    pass