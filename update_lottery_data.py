import requests, json, random, os
from datetime import datetime, timedelta
from decimal import Decimal

LOTTERY_ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
CREATOR_ADDRESS = "bc1prhcdy4ytncv8xgq0xwtqg0gfk2t38asddq3ex7xxa43dxhrfhkhsn6yhk9"
API_URL = f"https://open-api.unisat.io/v1/indexer/address/{LOTTERY_ADDRESS}/rune/txs"
WINNERS_FILE = "winners_history.json"
DOG_PRICE_API = "https://mempool.space/api/v1/rune/DOG"  # You can swap this with your own trusted source

headers = {"accept": "application/json"}
entries = []
cutoff_time = datetime.utcnow() - timedelta(hours=24)

# Converts raw Rune units (1e9) to float
def convert_rune_amount(raw_amount: str) -> float:
    return float(Decimal(raw_amount) / Decimal(1e9))

# Get current DOG price in USD (fallback value if needed)
def get_dog_price_usd() -> float:
    try:
        res = requests.get(DOG_PRICE_API, headers=headers)
        res.raise_for_status()
        data = res.json()
        return float(data.get("price", 0.001))  # fallback if price missing
    except:
        return 0.001  # Default fallback

try:
    res = requests.get(API_URL, headers=headers)
    res.raise_for_status()
    txs = res.json().get("data", {}).get("transactions", [])

    for tx in txs:
        tx_time = datetime.utcfromtimestamp(tx.get("blocktime", datetime.utcnow().timestamp()))
        if tx_time >= cutoff_time:
            for t in tx.get("transfers", []):
                if t.get("tick") == "DOG" and t.get("to") == LOTTERY_ADDRESS:
                    entries.append({
                        "txid": tx["txid"],
                        "amount": round(convert_rune_amount(t["amount"]), 4),
                        "timestamp": tx_time.isoformat()
                    })

    total = round(sum(e["amount"] for e in entries), 4)
    winner = random.choice(entries) if entries else {"txid": "none", "amount": 0}

    dog_price_usd = get_dog_price_usd()

    status = {
        "live_pot_total": total,
        "payout_to_winner": round(total * 0.75, 4),
        "rollover_to_next_round": round(total * 0.20, 4),
        "creator_fee": round(total * 0.05, 4),
        "winner": winner,
        "creator_address": CREATOR_ADDRESS,
        "usd_price": dog_price_usd,
        "total_pot_usd": round(total * dog_price_usd, 4),
        "timestamp": datetime.utcnow().isoformat()
    }

    with open("lottery_entries.json", "w") as f:
        json.dump(entries, f, indent=2)

    with open("lottery_status.json", "w") as f:
        json.dump(status, f, indent=2)

    # Append today's winner to winners_history.json
    today = datetime.utcnow().strftime('%Y-%m-%d')
    winners = {}

    if os.path.exists(WINNERS_FILE):
        with open(WINNERS_FILE, "r") as f:
            winners = json.load(f)

    winners[today] = {
        "txid": winner["txid"],
        "amount": winner["amount"],
        "usd_value": round(winner["amount"] * dog_price_usd, 4),
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(WINNERS_FILE, "w") as f:
        json.dump(winners, f, indent=2)

except Exception as e:
    print("Error:", e)
