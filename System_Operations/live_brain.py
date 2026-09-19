import json
from nicegui import ui

with ui.card().classes("w-full max-w-md mx-auto mt-10 p-6 items-center"):
    ui.label("🧠 Mike & Donna's Live Brain").classes("text-2xl font-bold mb-4")
    wr = ui.label("Loading WR Modifier...").classes("text-xl mb-2")
    tix = ui.label("Loading Pending Tickets...").classes("text-xl")

def read_brain():
    try:
        with open("brain.json", "r") as f:
            b = json.load(f)
        wr.set_text(f"🏈 WR Receptions: {b.get('model_weights', {}).get('WR_RECEPTIONS', {}).get('modifier', 'N/A')}")
        tix.set_text(f"🎟️ Pending Tickets: {len(b.get('bet_ledger', []))}")
    except:
        pass

ui.timer(2.0, read_brain)
ui.run(port=8080, title="Live Brain")