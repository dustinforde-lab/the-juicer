import os
import json
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")
AUTH_DIR = os.getcwd()
OAUTH_FILE = os.path.join(AUTH_DIR, "oauth2.json")

def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def run_yahoo_sync():
    print("\n" + "="*55)
    print("🏈 THE JUICER: YAHOO FANTASY MULTI-LEAGUE SYNC")
    print("="*55)
    
    # Check if developer app credentials exist
    if not os.path.exists(OAUTH_FILE):
        print(f"⚠️ Missing oauth2.json at {OAUTH_FILE}")
        print("To connect live Yahoo API:")
        print("1. Create an app at https://developer.yahoo.com/apps/create/")
        print("2. Set Redirect URI to: https://localhost:8080 or oob")
        print("3. Place credentials in oauth2.json formatted as:")
        print('   {"consumer_key": "YOUR_CLIENT_ID", "consumer_secret": "YOUR_CLIENT_SECRET"}')
        print("\nLoading mock multi-league Yahoo payload for pipeline validation...")
        
        # Mocking 2 distinct Yahoo leagues
        mock_yahoo_rosters = [
            # League 1: Main Competitive
            ("YAHOO", "y_44211", "Sunday Sweat League", "t_1", "Chuck's Squad", "Justin Herbert", "QB", "ROSTER", _utcnow_iso()),
            ("YAHOO", "y_44211", "Sunday Sweat League", "t_1", "Chuck's Squad", "De'Von Achane", "RB", "ROSTER", _utcnow_iso()),
            ("YAHOO", "y_44211", "Sunday Sweat League", "t_1", "Chuck's Squad", "Garrett Wilson", "WR", "ROSTER", _utcnow_iso()),
            ("YAHOO", "y_44211", "Sunday Sweat League", "waiver", "Free Agents", "Luther Burden", "WR", "FREE_AGENT", _utcnow_iso()),
            
            # League 2: Work / Secondary League
            ("YAHOO", "y_89904", "Prime Time Dynasty", "t_4", "Gridiron Syndicate", "Caleb Williams", "QB", "ROSTER", _utcnow_iso()),
            ("YAHOO", "y_89904", "Prime Time Dynasty", "t_4", "Gridiron Syndicate", "Aaron Jones", "RB", "ROSTER", _utcnow_iso()),
            ("YAHOO", "y_89904", "Prime Time Dynasty", "t_4", "Gridiron Syndicate", "Colston Loveland", "TE", "ROSTER", _utcnow_iso()),
            ("YAHOO", "y_89904", "Prime Time Dynasty", "waiver", "Free Agents", "Luke Farrell", "TE", "FREE_AGENT", _utcnow_iso())
        ]
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM season_long_rosters WHERE platform = 'YAHOO'")
            conn.executemany("""
                INSERT INTO season_long_rosters (platform, league_id, league_name, team_id, team_name, player_name, pos, status, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, mock_yahoo_rosters)
            conn.commit()
            
        print(f"✅ Ingested {len(mock_yahoo_rosters)} entries across 2 Yahoo leagues.")
        print("="*55 + "\n")
        return

    # Live Yahoo API execution when oauth2.json is populated
    try:
        from yahoo_oauth import OAuth2
        from yahoo_fantasy_api import Game
        sc = OAuth2(None, None, from_file=OAUTH_FILE)
        if not sc.token_is_valid():
            sc.refresh_access_token()
            
        gm = Game(sc, "nfl")
        league_ids = gm.league_ids(year=2026)
        
        records = []
        now_str = _utcnow_iso()
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM season_long_rosters WHERE platform = 'YAHOO'")
            
            for l_id in league_ids:
                lg = gm.to_league(l_id)
                meta = lg.settings()
                league_name = meta.get("name", f"Yahoo League {l_id}")
                team_key = lg.team_key()
                tm = lg.to_team(team_key)
                
                # Fetch user team roster
                roster = tm.roster()
                for p in roster:
                    records.append((
                        "YAHOO", str(l_id), league_name, team_key,
                        tm.name, p["name"], p["position_type"],
                        "ROSTER" if p["selected_position"] != "BN" else "BENCH",
                        now_str
                    ))
                    
                # Fetch top available waiver players
                fa = lg.free_agents("ALL")[:25]
                for p in fa:
                    records.append((
                        "YAHOO", str(l_id), league_name, "waiver",
                        "Free Agents", p["name"], p["position_type"], "FREE_AGENT", now_str
                    ))
                    
            conn.executemany("""
                INSERT INTO season_long_rosters (platform, league_id, league_name, team_id, team_name, player_name, pos, status, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, records)
            conn.commit()
            
        print(f"✅ Live Yahoo Sync Complete: Synced {len(league_ids)} leagues ({len(records)} total records).")
    except Exception as e:
        print(f"❌ Error during Yahoo Fantasy sync: {e}")
        
    print("="*55 + "\n")

if __name__ == "__main__":
    run_yahoo_sync()