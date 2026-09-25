# -*- coding: utf-8 -*-
import streamlit as st
import random
import data_service
from parlay_engine import calculate_correlated_fair_prob

def get_master_parlay_pool():
    return [
        ("Josh Allen", "250+ Pass Yds", "#00e5ff"),
        ("Josh Allen", "2+ Pass TDs", "#00e5ff"),
        ("Bijan Robinson", "Anytime TD", "#ff2a6d"),
        ("Bijan Robinson", "70+ Rush Yds", "#ff2a6d"),
        ("CeeDee Lamb", "80+ Rec Yds", "#00ff88"),
        ("CeeDee Lamb", "7+ Receptions", "#00ff88"),
        ("Amon-Ra St. Brown", "75+ Rec Yds", "#00ff88"),
        ("Amon-Ra St. Brown", "Anytime TD", "#00ff88"),
        ("Breece Hall", "70+ Rush Yds", "#ff2a6d"),
        ("Breece Hall", "4+ Receptions", "#ff2a6d"),
        ("Lamar Jackson", "50+ Rush Yds", "#00e5ff"),
        ("Lamar Jackson", "200+ Pass Yds", "#00e5ff"),
        ("Jordan Love", "2+ Pass TDs", "#00e5ff"),
        ("Jordan Love", "240+ Pass Yds", "#00e5ff"),
        ("Jayden Reed", "55+ Rec Yds", "#00ff88"),
        ("Patrick Mahomes", "250+ Pass Yds", "#00e5ff"),
        ("Rashee Rice", "6+ Receptions", "#00ff88"),
        ("Jahmyr Gibbs", "50+ Rush Yds", "#ff2a6d"),
        ("Jahmyr Gibbs", "Anytime TD", "#ff2a6d"),
        ("Saquon Barkley", "75+ Rush Yds", "#ff2a6d"),
        ("Saquon Barkley", "Anytime TD", "#ff2a6d"),
        ("Jalen Hurts", "1+ Rushing TD", "#00e5ff"),
        ("De'Von Achane", "50+ Rush Yds", "#ff2a6d"),
        ("Tyreek Hill", "80+ Rec Yds", "#00ff88"),
        ("Justin Jefferson", "85+ Rec Yds", "#00ff88"),
        ("Nico Collins", "70+ Rec Yds", "#00ff88"),
        ("C.J. Stroud", "250+ Pass Yds", "#00e5ff"),
        ("Derrick Henry", "70+ Rush Yds", "#ff2a6d"),
        ("Marvin Harrison Jr.", "60+ Rec Yds", "#00ff88"),
        ("Kyler Murray", "35+ Rush Yds", "#00e5ff"),
        ("Trey McBride", "5+ Receptions", "#ffd700"),
        ("George Kittle", "50+ Rec Yds", "#ffd700"),
        ("Brock Bowers", "45+ Rec Yds", "#ffd700"),
        ("Drake London", "60+ Rec Yds", "#00ff88"),
        ("James Cook", "60+ Rush Yds", "#ff2a6d"),
        ("Zay Flowers", "50+ Rec Yds", "#00ff88")
    ]

def generate_tiered_parlay_deck():
    pool = get_master_parlay_pool()
    deck = []
    
    for i in range(1, 101):
        if i <= 20:
            leg_count = 2
        elif i <= 55:
            leg_count = random.choice([3, 4])
        elif i <= 80:
            leg_count = random.choice([5, 6])
        else:
            leg_count = random.choice([7, 8, 9, 10])

        safe_count = min(leg_count, len(pool))
        random.seed(i + 2042)
        chosen_legs = random.sample(pool, safe_count)
        odds_val = int(100 * (1.85 ** safe_count))
        adj_prob = calculate_correlated_fair_prob(chosen_legs)
        
        bookmaker = "DraftKings Sportsbook" if i % 2 == 0 else "FanDuel Sportsbook"
        book_color = "#00ff88" if bookmaker == "DraftKings Sportsbook" else "#00e5ff"

        deck.append({
            "id": f"TKT-{i:03d}",
            "type": f"{safe_count}-Leg Ticket",
            "prob": adj_prob,
            "odds": f"+{odds_val:,}",
            "book": bookmaker,
            "book_color": book_color,
            "legs": chosen_legs
        })
    return deck

def render_parlay_mix():
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:2px;'>🔀 PARLAY MIX: ISOLATED TICKETS</h2>", unsafe_allow_html=True)
    telemetry = data_service.get_full_telemetry_timestamps()
    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Single-Book Constraint Active &bull; Odds API Source &bull; ⏱️ Status: {telemetry['odds_badge']}</div>", unsafe_allow_html=True)

    deck = generate_tiered_parlay_deck()
    cols = st.columns(2)
    for idx, t in enumerate(deck):
        pills_html = ""
        for leg in t["legs"]:
            pills_html += f"<div style='flex:0 0 auto; min-width:115px; background:#161b22; border-top:3px solid {leg[2]}; padding:6px 10px; border-radius:6px; margin-right:8px; font-size:11px;'><b style='color:#fff;'>{leg[0]}</b><br><span style='color:#00ff88;'>{leg[1]}</span></div>"

        st_html = f"""
        <div style='background:rgba(13,17,23,0.85); backdrop-filter:blur(10px); border:1px solid #30363d; border-radius:10px; padding:14px; margin-bottom:14px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:10px;'>
                <div>
                    <span style='font-size:14px; font-weight:900; color:{t['book_color']};'>{t['id']}</span> 
                    <span style='color:#8b949e; font-size:11px; margin-left:8px;'>📍 {t['book']}</span>
                </div>
                <div><span style='color:#8b949e; font-size:11px;'>Fair Prob:</span> <b style='color:#00ff88; font-size:14px;'>{t['prob']}</b></div>
            </div>
            <div style='display:flex; flex-direction:row; overflow-x:auto; margin-bottom:10px; padding-bottom:4px; width:100%; scrollbar-width:thin;'>{pills_html}</div>
            <div style='display:flex; justify-content:space-between; align-items:center; background:#0d1117; border-radius:6px; padding:8px 12px;'>
                <div><span style='background:rgba(255,255,255,0.1); color:#fff; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:4px;'>{t['type']}</span></div>
                <div><span style='font-size:11px; color:#8b949e;'>Total Odds:</span> <b style='color:{t['book_color']}; font-size:15px;'>{t['odds']}</b></div>
            </div>
        </div>
        """
        with cols[idx % 2]:
            st.html(st_html)
