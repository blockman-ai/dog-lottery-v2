import json
import random
import hashlib
from datetime import datetime

# Path to your lottery entries file
ENTRIES_FILE = "lottery_entries.json"

def load_entries():
    try:
        with open(ENTRIES_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading entries: {e}")
        return []

def pick_winner(entries):
    if not entries:
        print("No entries found!")
        return None

    # Use current UTC time as seed (replace with block hash for production)
    seed_input = str(datetime.utcnow())
    seed = int(hashlib.sha256(seed_input.encode("utf-8")).hexdigest(), 16)
    random.seed(seed)
    
    winner = random.choice(entries)
    return winner

def main():
    entries = load_entries()
    print(f"Total entries: {len(entries)}")
    
    winner = pick_winner(entries)
    if winner:
        print("The winner is:")
        print(json.dumps(winner, indent=2))
    else:
        print("No winner could be selected.")

if __name__ == "__main__":
    main()
from datetime import datetime, timedelta

# Simulate transactions (normally pulled from an API like Hiro or mempool.space)
transactions = [
    {"txid": "tx1", "amount": 10, "timestamp": datetime.utcnow() - timedelta(hours=1)},
    {"txid": "tx2", "amount": 20, "timestamp": datetime.utcnow() - timedelta(hours=2)},
    {"txid": "tx3", "amount": 15, "timestamp": datetime.utcnow() - timedelta(hours=3)}
]

# Calculate live pot total
total_pot = sum(tx["amount"] for tx in transactions)
creator_fee = total_pot * 0.05
rollover_amount = total_pot * 0.20
winner_payout = total_pot * 0.75

{
    "live_pot_total": total_pot,
    "payout_to_winner": winner_payout,
    "rollover_to_next_round": rollover_amount,
    "creator_fee": creator_fee
}
