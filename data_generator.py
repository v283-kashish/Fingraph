import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta


# Create Faker object
fake = Faker()

# Number of transactions
NUM_NORMAL_TRANSACTIONS= 900

# Create account IDs
accounts = [f"A{i:03d}" for i in range(1, 101)]

# Store transactions
transactions = []

# Starting time
current_time = datetime.now()


# Generate normal transactions
for i in range(NUM_NORMAL_TRANSACTIONS):

    sender = random.choice(accounts)
    receiver = random.choice(accounts)

    # Make sure sender and receiver are different
    while receiver == sender:
        receiver = random.choice(accounts)

    amount = random.randint(100, 10000)

    current_time += timedelta(seconds=random.randint(1, 10))

    transaction = {
        "transaction_id": f"T{i+1:05d}",
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": current_time
    }

    transactions.append(transaction)
    # -----------------------------------------
# Generate circular fraud transactions
# -----------------------------------------

for group in range(10):

    # Create 5 accounts for this fraud ring
    ring_accounts = [
        f"F{group + 1:02d}_{i}"
        for i in range(1, 6)
    ]

    for i in range(len(ring_accounts)):

        sender = ring_accounts[i]
        receiver = ring_accounts[(i + 1) % len(ring_accounts)]

        amount = random.randint(4000, 9000)

        current_time += timedelta(seconds=random.randint(1, 5))

        transaction = {
            "transaction_id": f"FRAUD_CIRC_{group + 1:02d}_{i + 1}",
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": current_time
        }

        transactions.append(transaction)
        # -----------------------------------------
# Generate Starburst fraud transactions
# -----------------------------------------

for group in range(10):

    # Create one shell account
    shell_account = f"SHELL_{group + 1:02d}"

    # Create 5 accounts sending money to the shell account
    senders = [
        f"SB{group + 1:02d}_{i}"
        for i in range(1, 6)
    ]

    for sender in senders:

        amount = random.randint(5000, 15000)

        current_time += timedelta(seconds=random.randint(1, 5))

        transaction = {
            "transaction_id": f"FRAUD_STAR_{group + 1:02d}_{senders.index(sender) + 1}",
            "sender": sender,
            "receiver": shell_account,
            "amount": amount,
            "timestamp": current_time
        }

        transactions.append(transaction)


# Convert transactions into a DataFrame
df = pd.DataFrame(transactions)


# Save the data
df.to_csv("transaction.csv", index=False)

print("Transaction data generated successfully!")
print(f"Total transactions: {len(df)}")
print("\nFirst 10 transactions:")
print(df.head(10))