import json
from datetime import datetime
from pathlib import Path
import random

ENTRIES_FILE = "lottery_entries.json"
WINNERS_FILE = "winners_history.json"

def load_json(path):
    if not Path(path).exists():
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def draw_winner():
    entries = load_json(ENTRIES_FILE)
    if not entries:
        print("No entries to draw from.")
        return

    # Weighted by entry count
    weighted_pool = []
    for entry in entries:
        weighted_pool.extend([entry] * int(entry.get("entries", 1)))

    winner = random.choice(weighted_pool)
    prize = round(winner["amount"] * 0.75, 9)
    timestamp = datetime.utcnow().isoformat() + "Z"

    winner_data = {
        "txid": winner["txid"],
        "from": winner["from"],
        "amount": prize,
        "original_amount": winner["amount"],
        "timestamp": timestamp,
        "chain": winner.get("chain", "bitcoin")
    }

    winners_history = load_json(WINNERS_FILE)
    winners_history.insert(0, winner_data)
    save_json(WINNERS_FILE, winners_history)

    print(f"Winner drawn: {winner['from']} wins {prize} $DOG")

if __name__ == "__main__":
    draw_winner()
