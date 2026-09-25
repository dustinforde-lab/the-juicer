import sqlite3
import json
import streamlit as st
import os

st.set_page_config(layout="wide")
DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def inject_aesthetic_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0914; color: #ffffff; }
        .streamlit-expanderHeader { font-weight: 800 !important; color: #00ff88 !important; background-color: #12101b !important; border: 1px solid #2a224a !important; }
        .leg-box {
            background-color: #1a162b;
            border-left: 4px solid #00ff88;
            padding: 12px 18px;
            border-radius: 6px;
            margin: 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .leg-player { color: #e6edf3; font-weight: 800; font-size: 15px; }
        .leg-team { color: #8b949e; font-size: 12px; margin-left: 8px; font-weight: bold; }
        .leg-stat { color: #00ff88; font-weight: bold; font-size: 14px; }
        .leg-line { color: #ffffff; font-weight: 900; font-size: 16px; margin-left: 8px; }
        .book-badge { background: #2a224a; color: #00e5ff; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; border: 1px solid #00e5ff; }
        </style>
    """, unsafe_allow_html=True)

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 style='color:#00ff88; text-align:center;'>🛠️ PHASE 3 SANDBOX: SINGLE-BOOK PARLAY MATRIX</h3><br>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM theoretical_bets LIMIT 10")
            rows = [dict(r) for r in cur.fetchall()]
            
        if not rows:
            st.info("No rows currently in theoretical_bets table.")
            return

        for r in rows:
            ticket_id = r.get("ticket_id") or r.get("id") or "Slip"
            odds = r.get("odds") or "+450"
            book_source = r.get("sportsbook_source") or r.get("sportsbook") or r.get("book") or "DraftKings"
            ticket_raw = r.get("ticket_json") or r.get("legs_json") or r.get("legs") or "[]"
            
            legs = []
            if isinstance(ticket_raw, str) and ticket_raw.startswith("["):
                try:
                    legs = json.loads(ticket_raw)
                except Exception:
                    legs = []
            elif isinstance(ticket_raw, list):
                legs = ticket_raw

            with st.expander(f"🎯 SYNDICATE SLIP: #{ticket_id}  |  ODDS: {odds}  |  BOOK: {book_source}", expanded=True):
                if not legs:
                    st.caption(f"Raw ticket data: {ticket_raw}")
                for leg in legs:
                    player = leg.get("player") or leg.get("player_name") or "Unknown"
                    team = leg.get("team", "FA")
                    stat = leg.get("stat") or leg.get("prop") or "Prop"
                    line = leg.get("line") or leg.get("target") or "N/A"
                    leg_book = leg.get("sportsbook_source") or leg.get("book") or book_source
                    
                    st.markdown(f'''
                    <div class="leg-box">
                        <div>
                            <span class="leg-player">{player}</span>
                            <span class="leg-team">({team})</span>
                        </div>
                        <div>
                            <span class="leg-stat">{stat}:</span>
                            <span class="leg-line">{line}</span>
                        </div>
                        <div class="book-badge">🏛️ {leg_book}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Sandbox Error: {e}")

if __name__ == "__main__":
    run_sandbox()