import random
import json
from datetime import datetime


# -----------------------------
# ACCOUNTS
# -----------------------------

accounts = [
    "A001",
    "A002",
    "A003",
    "A004",
    "A005",
    "A006",
    "A007",
    "A008",
    "A009",
    "A010"
]


# -----------------------------
# BANKS
# -----------------------------

banks = [
    "BANK01",
    "BANK02",
    "BANK03"
]
# -----------------------------
# TRANSACTION VALIDATION
# -----------------------------

def validate_transaction(transaction):

    required_fields = [
        "transaction_id",
        "sender_account",
        "receiver_account",
        "amount",
        "timestamp",
        "bank"
    ]

    # Check required fields
    for field in required_fields:
        if field not in transaction:
            return False

    # Sender and receiver must be different
    if transaction["sender_account"] == transaction["receiver_account"]:
        return False

    # Amount must be positive
    if not isinstance(transaction["amount"], (int, float)):
        return False

    if transaction["amount"] <= 0:
        return False

    return True


# -----------------------------
# NORMAL TRANSACTION
# -----------------------------

def generate_transaction(transaction_id):

    sender = random.choice(accounts)
    receiver = random.choice(accounts)

    # Make sure sender and receiver are different
    while receiver == sender:
        receiver = random.choice(accounts)

    transaction = {
        "transaction_id": transaction_id,
        "sender_account": sender,
        "receiver_account": receiver,
        "amount": round(random.uniform(1000, 100000), 2),
        "timestamp": datetime.now().isoformat(),
        "bank": random.choice(banks)
    }
    if not validate_transaction(transaction):
        raise ValueError("Invalid transaction generated")


    return transaction


# -----------------------------
# STARBURST FRAUD PATTERN
# -----------------------------

def generate_starburst_transactions():

    # Central/shell account
    shell_account = "A999"

    # Multiple accounts sending money
    senders = [
        "A001",
        "A002",
        "A003",
        "A004",
        "A005"
    ]

    transactions = []

    for i, sender in enumerate(senders, start=1):

        transaction = {
            "transaction_id": f"STAR{i:03d}",
            "sender_account": sender,
            "receiver_account": shell_account,
            "amount": round(random.uniform(50000, 100000), 2),
            "timestamp": datetime.now().isoformat(),
            "bank": random.choice(banks)
        }

        transactions.append(transaction)

    return transactions


# -----------------------------
# CIRCULAR FRAUD PATTERN
# -----------------------------

def generate_circular_transactions():

    transactions = [

        {
            "transaction_id": "CIRC001",
            "sender_account": "A101",
            "receiver_account": "A102",
            "amount": 75000,
            "timestamp": datetime.now().isoformat(),
            "bank": "BANK01"
        },

        {
            "transaction_id": "CIRC002",
            "sender_account": "A102",
            "receiver_account": "A103",
            "amount": 73000,
            "timestamp": datetime.now().isoformat(),
            "bank": "BANK01"
        },

        {
            "transaction_id": "CIRC003",
            "sender_account": "A103",
            "receiver_account": "A101",
            "amount": 71000,
            "timestamp": datetime.now().isoformat(),
            "bank": "BANK01"
        }

    ]

    return transactions


# -----------------------------
# TEST THE FUNCTIONS
# -----------------------------

if __name__ == "__main__":

    # Test normal transaction
    print("\nNORMAL TRANSACTION")
    print("==================")

    normal = generate_transaction("TX001")

    print(json.dumps(normal, indent=4))


    # Test Starburst
    print("\nSTARBURST FRAUD PATTERN")
    print("=======================")

    starburst = generate_starburst_transactions()

    for transaction in starburst:
        print(json.dumps(transaction, indent=4))


    # Test Circular
    print("\nCIRCULAR FRAUD PATTERN")
    print("======================")

    circular = generate_circular_transactions()

    for transaction in circular:
        print(json.dumps(transaction, indent=4))