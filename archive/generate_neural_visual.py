import sqlite3, random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DB_FILE = "action_grid.db"

# Seed advanced Neural Vector data
ARCHETYPES = [
    {"name": "QB_WR_Shootout (Same Game)", "prec": 78, "vol": 12, "edge": 91, "volu": 85, "mom": 92},
    {"name": "Cross-Game RB_DST Correlation", "prec": 64, "vol": 35, "edge": 55, "volu": 62, "mom": 58},
    {"name": "Contrarian DFS Fade Stack", "prec": 31, "vol": 88, "edge": 88, "volu": 41, "mom": 45},
    {"name": "Moonshot Whale Moonshot (5 Leg+)", "prec": 15, "vol": 95, "edge": 99, "volu": 18, "mom": 25}
]

def generate_neural_radar_chart():
    print("=" * 65)
    print("🎬 [PHASE 4: STEP 2] Visualizing Mike's Neural Correlation Map (Radar)...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        
        # 1. Update the Analytics Ledger in SQLite
        cur.execute("DELETE FROM correlation_weights")
        for a in ARCHETYPES:
            cur.execute("""
                INSERT INTO correlation_weights VALUES (?, ?, ?, ?)
            """, (a["name"], random.randint(30, 80), random.uniform(22.5, 78.5), random.uniform(0.95, 1.25)))
        conn.commit()

        # 2. Extract and format data for radar
        df = pd.DataFrame(ARCHETYPES)
        df = df.set_index("name")
        categories = ["Precision", "Volatility", "EdgeDiscrepancy", "SampleVolume", "Momentum"]
        num_vars = len(categories)

        # 3. Define Plot Aesthetics (Sleek Dark Cyberpunk)
        plt.style.use("dark_background")
        plt.rcParams["font.family"] = "sans-serif"
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1] # Complete the circle

        # Draw a line for each correlation recipe
        for idx, row in df.iterrows():
            values = row.values.flatten().tolist()
            values += values[:1] # Complete the circle
            ax.plot(angles, values, linewidth=2.5, linestyle='solid', label=idx)
            ax.fill(angles, values, alpha=0.1)

        # Labels & Styling
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=10, fontname="monospace", color="#00e5ff", fontweight="bold")
        ax.set_rgrids([25, 50, 75, 100], ["25", "50", "75", "100"], fontsize=9, color="#444")
        ax.set_ylim(0, 100)
        
        ax.grid(color='#333', linewidth=1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=8, facecolor='#000', edgecolor='#222')
        
        # Save output for Streamlit dashboard ingestion
        plt.tight_layout()
        plt.savefig("film_room_radar.png", dpi=100, facecolor='#0d1117', edgecolor='#0d1117')
        print("   ✅ Neural Map visual (film_room_radar.png) generated for Film Room ingestion.")

if __name__ == "__main__":
    generate_neural_radar_chart()
