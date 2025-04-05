# DOG Lottery

**DOG Lottery** is an on-chain lottery system for $DOG Rune that lets users participate in a daily lottery. Each day, users send a fixed amount of $DOG to join the lottery pot. After 24 hours, one lucky participant is randomly selected to win 75% of the pot, 20% is rolled over into the next round, and 5% goes to the creator.

## How It Works

1. **Entry:**  
   - Every user sends a fixed amount of $DOG Rune (e.g. 100,000 $DOG) to the lottery address.  
   - Each entry is recorded as an on-chain transaction.

2. **Lottery Round:**  
   - Each round lasts 24 hours.
   - All valid entries within the 24-hour window are collected.

3. **Winner Selection:**  
   - A random winner is chosen using an on-chain method (e.g., the hash of the latest block as entropy).
   - The winner receives 75% of the pot.
   - 20% of the pot is carried over to the next round.
   - 5% is allocated to the creator as a fee.

4. **Payout:**  
   - The selected winner is announced and the payout is automatically processed on-chain.
   - All transactions and results are recorded immutably.

## Why DOG Lottery?

- **Immutable:** All entries and outcomes are recorded on-chain, ensuring transparency and permanence.
- **Fair & Decentralized:** Winner selection is based on provable randomness from the blockchain.
- **Community-Driven:** The system is designed for the $DOG community, with a portion of the pot reinvested for future rounds.
- **Simple:** Just one entry per user per round—no complex mechanics.

## Getting Started

### Prerequisites
- A Bitcoin wallet or an Ordinals-compatible wallet that supports $DOG Rune.
- $DOG tokens for entry (ensure you know the fixed entry fee).
- Familiarity with on-chain transactions (optional but helpful).

### How to Participate
1. **Send $DOG:**  
   Send the fixed amount of $DOG Rune to the designated lottery address. Your entry is recorded automatically on-chain.

2. **Wait for the Round to End:**  
   Each round lasts 24 hours. After the round ends, the system randomly selects one winner.

3. **Receive Your Winnings:**  
   If you are the lucky winner, 75% of the pot is transferred to your address automatically.

## Roadmap

- **Phase 1:**  
  - Launch basic lottery mechanism.
  - Implement on-chain entry detection.
  - Winner selection based on blockchain randomness.

- **Phase 2:**  
  - Develop a user-friendly frontend dashboard.
  - Integrate a wallet connect feature for easier participation.
  - Provide live updates and lottery statistics.

- **Phase 3:**  
  - Explore additional features such as community voting on lottery rules, secondary prizes, and bonus rounds.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

## License

This project is open-source and distributed under the MIT License.

---

*Join the DOG Lottery and be part of an on-chain revolution where every block counts!*# onchain--DOG-Lottery
