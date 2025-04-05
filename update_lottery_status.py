import random, json
from datetime import datetime, timedelta

transactions = [
    {"txid": "tx001", "amount": 150, "timestamp": str(datetime.utcnow() - timedelta(hours=1))},
    {"txid": "tx002", "amount": 200, "timestamp": str(datetime.utcnow() - timedelta(hours=2))},
    {"txid": "tx003", "amount": 50, "timestamp": str(datetime.utcnow() - timedelta(hours=3))}
]

total_pot = sum(tx["amount"] for tx in transactions)
winner_payout = round(total_pot * 0.75, 2)
rollover = round(total_pot * 0.20, 2)
creator_fee = round(total_pot * 0.05, 2)
winner = random.choice(transactions)

lottery_status = {
    "live_pot_total": total_pot,
    "payout_to_winner": winner_payout,
    "rollover_to_next_round": rollover,
    "creator_fee": creator_fee,
    "winner": winner
}

with open("lottery_status.json", "w") as f:
    json.dump(lottery_status, f, indent=2)
