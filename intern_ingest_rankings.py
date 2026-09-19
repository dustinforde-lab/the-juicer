import sqlite3

DB_FILE = "action_grid.db"

QB_DATA = [
    (1, "Josh Allen", "BUF", 7, "DET"), (2, "Lamar Jackson", "BAL", 13, "NO"),
    (3, "Caleb Williams", "CHI", 10, "MIN"), (4, "Jalen Hurts", "PHI", 10, "TEN"),
    (5, "Dak Prescott", "DAL", 14, "WAS"), (6, "Jared Goff", "DET", 6, "BUF"),
    (7, "Justin Herbert", "LAC", 7, "LV"), (8, "Patrick Mahomes", "KC", 5, "IND"),
    (9, "Drake Maye", "NE", 11, "PIT"), (10, "Jayden Daniels", "WAS", 7, "DAL"),
    (11, "Matthew Stafford", "LAR", 11, "NYG"), (12, "Brock Purdy", "SF", 8, "MIA"),
    (13, "Joe Burrow", "CIN", 6, "HOU"), (14, "Trevor Lawrence", "JAX", 7, "DEN"),
    (15, "Jaxson Dart", "NYG", 8, "LAR"), (16, "Bo Nix", "DEN", 10, "JAX"),
    (17, "Baker Mayfield", "TB", 10, "CLE"), (18, "Jordan Love", "GB", 11, "NYJ"),
    (19, "Malik Willis", "MIA", 6, "SF"), (20, "C.J. Stroud", "HOU", 8, "CIN"),
    (21, "Tyler Shough", "NO", 8, "BAL"), (22, "Daniel Jones", "IND", 13, "KC"),
    (23, "Jacoby Brissett", "ARI", 14, "SEA"), (24, "Cam Ward", "TEN", 9, "PHI"),
    (25, "Carson Wentz", "MIN", 6, "CHI")
]

RB_DATA = [
    (1, "Bijan Robinson", "ATL", 11, "CAR"), (2, "Christian McCaffrey", "SF", 8, "MIA"),
    (3, "Jahmyr Gibbs", "DET", 6, "BUF"), (4, "Kenneth Walker", "KC", 5, "IND"),
    (5, "Ashton Jeanty", "LV", 13, "LAC"), (6, "Saquon Barkley", "PHI", 10, "TEN"),
    (7, "James Cook III", "BUF", 7, "DET"), (8, "Derrick Henry", "BAL", 13, "NO"),
    (9, "Jonathan Taylor", "IND", 13, "KC"), (10, "De'Von Achane", "MIA", 6, "SF"),
    (11, "Omarion Hampton", "LAC", 7, "LV"), (12, "Javonte Williams", "DAL", 14, "WAS"),
    (13, "D'Andre Swift", "CHI", 10, "MIN"), (14, "Chase Brown", "CIN", 6, "HOU"),
    (15, "Kyren Williams", "LAR", 11, "NYG"), (16, "Breece Hall", "NYJ", 13, "GB"),
    (17, "David Montgomery", "HOU", 8, "CIN"), (18, "Travis Etienne Jr.", "NO", 8, "BAL"),
    (19, "Jaylen Warren", "PIT", 9, "NE"), (20, "Jeremiyah Love", "ARI", 14, "SEA"),
    (21, "Rhamondre Stevenson", "NE", 11, "PIT"), (22, "Bucky Irving", "TB", 10, "CLE"),
    (23, "Cam Skattebo", "NYG", 8, "LAR"), (24, "Jordan Mason", "MIN", 6, "CHI"),
    (25, "Quinshon Judkins", "CLE", 11, "TB")
]

WR_DATA = [
    (1, "Justin Jefferson", "MIN", 6, "CHI"), (2, "Amon-Ra St. Brown", "DET", 6, "BUF"),
    (3, "Jaxon Smith-Njigba", "SEA", 11, "ARI"), (4, "Puka Nacua", "LAR", 11, "NYG"),
    (5, "Ja'Marr Chase", "CIN", 6, "HOU"), (6, "CeeDee Lamb", "DAL", 14, "WAS"),
    (7, "Chris Olave", "NO", 8, "BAL"), (8, "Nico Collins", "HOU", 8, "CIN"),
    (9, "DJ Moore", "BUF", 7, "DET"), (10, "DeVonta Smith", "PHI", 10, "TEN"),
    (11, "Luther Burden III", "CHI", 10, "MIN"), (12, "George Pickens", "DAL", 14, "WAS"),
    (13, "Zay Flowers", "BAL", 13, "NO"), (14, "Garrett Wilson", "NYJ", 13, "GB"),
    (15, "Mike Evans", "SF", 8, "MIA"), (16, "Rashee Rice", "KC", 5, "IND"),
    (17, "Emeka Egbuka", "TB", 10, "CLE"), (18, "Drake London", "ATL", 11, "CAR"),
    (19, "Parker Washington", "JAX", 7, "DEN"), (20, "Rome Odunze", "CHI", 10, "MIN"),
    (21, "Malik Nabers", "NYG", 8, "LAR"), (22, "Tee Higgins", "CIN", 6, "HOU"),
    (23, "Ladd McConkey", "LAC", 7, "LV"), (24, "Christian Watson", "GB", 11, "NYJ"),
    (25, "Davante Adams", "LAR", 11, "NYG"), (26, "Tetairoa McMillan", "CAR", 5, "ATL"),
    (27, "Jameson Williams", "DET", 6, "BUF"), (28, "Terry McLaurin", "WAS", 7, "DAL"),
    (29, "Marvin Harrison Jr.", "ARI", 14, "SEA"), (30, "Michael Pittman Jr.", "PIT", 9, "NE"),
    (31, "Stefon Diggs", "WAS", 7, "DAL"), (32, "Michael Wilson", "ARI", 14, "SEA"),
    (33, "DK Metcalf", "PIT", 9, "NE"), (34, "Jordan Addison", "MIN", 6, "CHI"),
    (35, "Jalen Coker", "CAR", 5, "ATL"), (36, "Wan'Dale Robinson", "TEN", 9, "PHI"),
    (37, "Courtland Sutton", "DEN", 10, "JAX"), (38, "Chris Godwin Jr.", "TB", 10, "CLE"),
    (39, "Dontayvion Wicks", "PHI", 10, "TEN"), (40, "Alec Pierce", "IND", 13, "KC"),
    (41, "Denzel Boston", "CLE", 11, "TB"), (42, "Jaylen Waddle", "DEN", 10, "JAX"),
    (43, "Romeo Doubs", "NE", 11, "PIT"), (44, "Deebo Samuel Sr.", "SF", 8, "MIA"),
    (45, "Matthew Golden", "GB", 11, "NYJ"), (46, "Jakobi Meyers", "JAX", 7, "DEN"),
    (47, "Quentin Johnston", "LAC", 7, "LV"), (48, "Keenan Allen", "IND", 13, "KC"),
    (49, "Caleb Douglas", "MIA", 6, "SF"), (50, "Carnell Tate", "TEN", 9, "PHI")
]

TE_DATA = [
    (1, "Trey McBride", "ARI", 14, "SEA"), (2, "Tyler Warren", "IND", 13, "KC"),
    (3, "Sam LaPorta", "DET", 6, "BUF"), (4, "Dalton Kincaid", "BUF", 7, "DET"),
    (5, "Colston Loveland", "CHI", 10, "MIN"), (6, "Tucker Kraft", "GB", 11, "NYJ"),
    (7, "Kyle Pitts Sr.", "ATL", 11, "CAR"), (8, "Travis Kelce", "KC", 5, "IND"),
    (9, "Isaiah Likely", "NYG", 8, "LAR"), (10, "Mark Andrews", "BAL", 13, "NO"),
    (11, "George Kittle", "SF", 8, "MIA"), (12, "Harold Fannin Jr.", "CLE", 11, "TB"),
    (13, "Michael Mayer", "LV", 13, "LAC"), (14, "Dallas Goedert", "PHI", 10, "TEN"),
    (15, "Jake Ferguson", "DAL", 14, "WAS"), (16, "Juwan Johnson", "NO", 8, "BAL"),
    (17, "T.J. Hockenson", "MIN", 6, "CHI"), (18, "Dalton Schultz", "HOU", 8, "CIN"),
    (19, "Brenton Strange", "JAX", 7, "DEN"), (20, "Hunter Henry", "NE", 11, "PIT"),
    (21, "Pat Freiermuth", "PIT", 9, "NE"), (22, "AJ Barner", "SEA", 11, "ARI"),
    (23, "Greg Dulcich", "MIA", 6, "SF")
]

def ingest():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS weekly_power_rankings")
        cur.execute("""
            CREATE TABLE weekly_power_rankings (
                pos TEXT, pos_rank INTEGER, name TEXT, team TEXT, bye INTEGER, opponent TEXT,
                PRIMARY KEY (pos, pos_rank)
            )
        """)
        for r in QB_DATA: cur.execute("INSERT INTO weekly_power_rankings VALUES ('QB', ?, ?, ?, ?, ?)", r)
        for r in RB_DATA: cur.execute("INSERT INTO weekly_power_rankings VALUES ('RB', ?, ?, ?, ?, ?)", r)
        for r in WR_DATA: cur.execute("INSERT INTO weekly_power_rankings VALUES ('WR', ?, ?, ?, ?, ?)", r)
        for r in TE_DATA: cur.execute("INSERT INTO weekly_power_rankings VALUES ('TE', ?, ?, ?, ?, ?)", r)
        conn.commit()
    print("=== WEEK 2 POWER RANKINGS INGESTED ===")
    print(f"Total Rows Seeded: QBs: {len(QB_DATA)}, RBs: {len(RB_DATA)}, WRs: {len(WR_DATA)}, TEs: {len(TE_DATA)}")

if __name__ == "__main__": ingest()
