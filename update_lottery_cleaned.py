
import requests
import json
import random
from datetime import datetime
from decimal import Decimal
from pathlib import Path

# Config
LOTTERY_ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
CREATOR_ADDRESS = "bc1prhcdy4ytncv8xgq0xwtqg0gfk2t38asddq3ex7xxa43dxhrfhkhsn6yhk9"
DOG_RUNE_ID = "1000806"
ENTRIES_FILE = "data/lottery_entries.json"
STATUS_FILE = "data/lottery_status.json"
MIN_ENTRY_AMOUNT = 1000

# API Setup
API_URL = f"https://open-api.unisat.io/v1/indexer/address/{LOTTERY_ADDRESS}/rune/txs?runeId={DOG_RUNE_ID}&start=0&limit=100"
HEADERS = {"accept": "application/json"}

def load_existing_txids(filepath):
    if not Path(filepath).exists():
        return set()
    try:
        with open(filepath, "r") as f:
            entries = json.load(f)
            return {entry["txid"] for entry in entries}
    except:
        return set()

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def main():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        txs = response.json().get("data", {}).get("transactions", [])

        existing_txids = load_existing_txids(ENTRIES_FILE)
        entries = []

        for tx in txs:
            txid = tx.get("txid")
            timestamp = datetime.utcfromtimestamp(tx.get("blocktime", datetime.utcnow().timestamp())).isoformat()

            for t in tx.get("transfers", []):
                if t.get("tick") == "DOG" and t.get("to") == LOTTERY_ADDRESS:
                    amount = float(Decimal(t["amount"]) / Decimal(1e9))
                    if txid not in existing_txids and amount >= MIN_ENTRY_AMOUNT:
                        entry_count = int(amount) // MIN_ENTRY_AMOUNT
                        entries.append({
                            "txid": txid,
                            "from": t.get("from"),
                            "amount": amount,
                            "entries": entry_count,
                            "timestamp": timestamp,
                            "chain": "bitcoin"
                        })

        total_dog = sum(e["amount"] for e in entries)
        winner = random.choice(entries) if entries else {"txid": "none", "amount": 0, "entries": 0}

        status = {
            "live_pot_total": total_dog,
            "payout_to_winner": round(total_dog * 0.75, 9),
            "rollover_to_next_round": round(total_dog * 0.20, 9),
            "creator_fee": round(total_dog * 0.05, 9),
            "winner": winner,
            "creator_address": CREATOR_ADDRESS,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        save_json(ENTRIES_FILE, entries)
        save_json(STATUS_FILE, status)
        print(f"Saved {len(entries)} entries and updated status.")

    except Exception as e:
        print("Error updating lottery:", e)

if __name__ == "__main__":
    main()
