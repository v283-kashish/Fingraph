import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta


# Create Faker object
fake = Faker()

# Number of transactions
NUM_TRANSACTIONS = 1000

# Create account IDs
accounts = [f"A{i:03d}" for i in range(1, 101)]

# Store transactions
transactions = []

# Starting time
current_time = datetime.now()


# Generate normal transactions
for i in range(NUM_TRANSACTIONS):

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


# Convert transactions into a DataFrame
df = pd.DataFrame(transactions)


# Save the data
df.to_csv("transaction.csv", index=False)

print("Transaction data generated successfully!")
print(f"Total transactions: {len(df)}")
print("\nFirst 10 transactions:")
print(df.head(10))