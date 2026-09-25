"""
The Juicer - DFS War Room Card Component
Supports 9-Man Classic & 6-Man Showdown with Crowned Gold Captain Tiles.
"""
import json

POS_COLORS = {
    "QB": "#00e5ff",
    "RB": "#ff2a6d",
    "WR": "#00ff88",
    "TE": "#ffd700",
    "FLEX": "#9d4edd",
    "DEF": "#78909c",
    "K": "#e0e0e0"
}

def get_team_logo(team):
    logos = {
        "BUF": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png",
        "SF": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
        "MIA": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png",
        "MIN": "https://a.espncdn.com/i/teamlogos/nfl/500/min.png",
        "ATL": "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png",
        "GB": "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
        "KC": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
        "DET": "https://a.espncdn.com/i/teamlogos/nfl/500/det.png",
        "BAL": "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png",
        "LAR": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png",
        "LAC": "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png",
        "SEA": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png",
        "ARI": "https://a.espncdn.com/i/teamlogos/nfl/500/ari.png",
        "DAL": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png",
        "DEN": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png",
        "NYJ": "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png"
    }
    return logos.get(team, "https://a.espncdn.com/i/teamlogos/nfl/500/nfl.png")

def render_lineup_card_html(lineup_row):
    c_type = lineup_row["contest_type"]
    f_type = lineup_row.get("format_type", "CLASSIC")
    proj = float(lineup_row["projected_points"])
    floor = float(lineup_row["floor_points"])
    ceil = float(lineup_row["ceiling_points"])
    salary = int(lineup_row["total_salary"])
    stack_text = str(lineup_row.get("stack_summary", ""))
    
    roster = json.loads(lineup_row["roster_json"]) if isinstance(lineup_row["roster_json"], str) else lineup_row["roster_json"]
    meta = json.loads(lineup_row.get("meta_json", "{}")) if isinstance(lineup_row.get("meta_json", "{}"), str) else lineup_row.get("meta_json", {})

    rem_salary = meta.get("remaining_salary", 50000 - salary)
    studs = meta.get("stud_count", 2)
    mids = meta.get("mid_count", 4)
    punts = meta.get("punt_count", 3)
    lev_label = meta.get("leverage_label", "OPTIMAL")

    tiles_html = ""
    for idx, p in enumerate(roster):
        p_name = p.get("name", "Player")
        pos = p.get("pos", "FLEX")
        team = p.get("team", "NFL")
        opp = p.get("opp", "OPP")
        sal = f"${p.get('salary', 5000):,}"
        p_proj = p.get("proj", 10.0)
        alpha = p.get("alpha", 85.0)
        logo_url = get_team_logo(team)

        is_cpt = p.get("is_cpt", False) or (f_type == "SHOWDOWN" and idx == 0)

        if is_cpt:
            p_color = "#ffd700"
            border_css = "border: 2px solid #ffd700; box-shadow: inset 0 0 12px rgba(255, 215, 0, 0.25), 0 0 10px rgba(255, 215, 0, 0.2);"
            tag_label = "👑 CPT (1.5x)"
        else:
            p_color = POS_COLORS.get(pos, "#00e5ff")
            border_css = f"border:1px solid rgba(255,255,255,0.08); border-top:2px solid {p_color};"
            tag_label = "FLEX" if f_type == "SHOWDOWN" else pos

        tiles_html += (
            f"<div style='flex:1; min-width:115px; background:rgba(18,24,38,0.85); {border_css} border-radius:6px; padding:6px 8px; margin:2px; display:flex; flex-direction:column; justify-content:space-between;'>"
            f"<div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:10px; font-weight:800; color:{p_color};'>{tag_label}</span><img src='{logo_url}' style='width:16px; height:16px; object-fit:contain;'></div>"
            f"<div style='font-size:12px; font-weight:700; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:2px;'>{p_name}</div>"
            f"<div style='display:flex; justify-content:space-between; font-size:10px; color:#8b949e; margin-top:2px;'><span>{team} vs {opp}</span><span style='color:#00ff88; font-weight:600;'>{sal}</span></div>"
            f"<div style='display:flex; justify-content:space-between; font-size:9px; color:#cad3df; margin-top:4px; padding-top:3px; border-top:1px solid rgba(255,255,255,0.05);'><span>α {alpha}</span><b style='color:#00e5ff;'>{p_proj} pt</b></div>"
            f"</div>"
        )

    stack_badge = f"<span style='background:rgba(0,229,255,0.12); color:#00e5ff; font-size:11px; padding:2px 8px; border-radius:4px; border:1px solid rgba(0,229,255,0.3); font-weight:600;'>{stack_text}</span>" if stack_text else ""
    format_badge = f"<span style='background:rgba(255,215,0,0.15); color:#ffd700; font-size:11px; padding:2px 6px; border-radius:4px; font-weight:800; border:1px solid rgba(255,215,0,0.3);'>SHOWDOWN 6-MAN</span>" if f_type == "SHOWDOWN" else "<span style='background:rgba(0,229,255,0.1); color:#00e5ff; font-size:11px; padding:2px 6px; border-radius:4px; font-weight:800;'>CLASSIC 9-MAN</span>"

    return (
        f"<div style='width:100%; background:#0c1017; border:1px solid rgba(0,229,255,0.22); border-radius:10px; padding:12px 14px; margin-bottom:14px; box-shadow: 0 4px 16px rgba(0,0,0,0.4);'>"
        f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>"
        f"<div style='display:flex; align-items:center; gap:8px;'><span style='font-size:14px; font-weight:900; color:#ff3366; letter-spacing:1px;'>DRAFTKINGS | {c_type}</span>{format_badge}{stack_badge}</div>"
        f"<div style='display:flex; align-items:center; gap:14px; font-size:12px;'>"
        f"<span style='color:#8b949e;'>Cap: <b style='color:#cad3df;'>${salary:,}</b> (<span style='color:#00ff88;'>+${rem_salary}</span>)</span>"
        f"<span style='color:#8b949e;'>Floor: <b style='color:#ffd700;'>{floor}</b></span>"
        f"<span style='color:#8b949e;'>Median: <b style='color:#00e5ff;'>{proj}</b></span>"
        f"<span style='background:rgba(0,255,136,0.12); border:1px solid rgba(0,255,136,0.3); color:#00ff88; padding:2px 8px; border-radius:4px; font-weight:800; font-size:13px;'>Ceiling {ceil} pts</span>"
        f"</div>"
        f"</div>"
        f"<div style='display:flex; flex-wrap:nowrap; overflow-x:auto; width:100%; gap:4px;'>{tiles_html}</div>"
        f"<div style='display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:10px; color:#8b949e;'>"
        f"<div style='display:flex; gap:12px;'><span>🎯 <b>{studs}</b> Studs • <b>{mids}</b> Mid • <b>{punts}</b> Punts</span><span>📊 <b>{lev_label}</b></span></div>"
        f"<div style='color:#cad3df;'>💡 <i>{meta.get('mike_verdict', '')}</i></div>"
        f"</div>"
        f"</div>"
    )

def run_self_audit():
    sample_sd = {
        "lineup_id": "DK_SD_TEST", "contest_type": "GPP", "format_type": "SHOWDOWN",
        "projected_points": 118.5, "floor_points": 88.0, "ceiling_points": 145.2, "total_salary": 48600,
        "stack_summary": "⚡ 4-2 PACKERS SCRIPT",
        "roster_json": [
            {"name": "Jordan Love", "pos": "QB", "team": "GB", "opp": "ATL", "salary": 15600, "proj": 29.7, "is_cpt": True},
            {"name": "Jayden Reed", "pos": "WR", "team": "GB", "opp": "ATL", "salary": 8000, "proj": 14.8},
            {"name": "Bijan Robinson", "pos": "RB", "team": "ATL", "opp": "GB", "salary": 10800, "proj": 19.2}
        ],
        "meta_json": {"remaining_salary": 1400, "stud_count": 2, "mid_count": 1, "punt_count": 0, "leverage_label": "LEFT $1400", "mike_verdict": "Test Passed"}
    }
    html = render_lineup_card_html(sample_sd)
    assert "👑 CPT" in html, "Captain badge missing."
    assert "SHOWDOWN 6-MAN" in html, "Showdown badge missing."
    print("✅ [PASS] Chunk 2 v3 (Crowned Showdown Cards) verified.")
    return True

if __name__ == "__main__":
    run_self_audit()