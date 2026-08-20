from kafka import KafkaConsumer
from neo4j import GraphDatabase
import json


# ============================================================
# NEO4J CONFIGURATION
# ============================================================

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "kashish@2005"
NEO4J_DATABASE = "neo4j"


# ============================================================
# NEO4J CONNECTION
# ============================================================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


# Check Neo4j connection
try:
    driver.verify_connectivity()
    print("Neo4j connected successfully!")

except Exception as e:
    print("ERROR: Could not connect to Neo4j")
    print(e)
    driver.close()
    exit()


# ============================================================
# CREATE GRAPH DATA
# ============================================================

def save_transaction(data):

    transaction_id = data.get("transaction_id")
    sender_account = data.get("sender_account")
    receiver_account = data.get("receiver_account")
    amount = data.get("amount")
    timestamp = data.get("timestamp")
    bank = data.get("bank")

    query = """
    MERGE (sender:Account {
        account_id: $sender_account
    })

    MERGE (receiver:Account {
        account_id: $receiver_account
    })

    MERGE (b:Bank {
        bank_id: $bank
    })

    MERGE (t:Transaction {
        transaction_id: $transaction_id
    })

    SET
        t.amount = $amount,
        t.timestamp = $timestamp

    MERGE (sender)-[:SENDS]->(t)

    MERGE (t)-[:RECEIVED_BY]->(receiver)

    MERGE (sender)-[:BELONGS_TO]->(b)

    RETURN t
    """

    with driver.session(database=NEO4J_DATABASE) as session:

        session.run(
            query,
            transaction_id=transaction_id,
            sender_account=sender_account,
            receiver_account=receiver_account,
            amount=amount,
            timestamp=timestamp,
            bank=bank
        )


# ============================================================
# KAFKA CONSUMER
# ============================================================

consumer = KafkaConsumer(
    "fingraph",

    bootstrap_servers="localhost:9092",

    auto_offset_reset="earliest",

    enable_auto_commit=True,

    group_id="fingraph-neo4j-consumer",

    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)


print("\n======================================")
print("FinGraph Kafka Consumer is running...")
print("Waiting for transactions...")
print("======================================\n")


# ============================================================
# RECEIVE KAFKA MESSAGES
# ============================================================

try:

    for message in consumer:

        data = message.value

        print("\nReceived transaction:")
        print(data)


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        required_fields = [
            "transaction_id",
            "sender_account",
            "receiver_account",
            "amount",
            "timestamp",
            "bank"
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in data
        ]


        if missing_fields:

            print("Invalid transaction!")
            print("Missing fields:", missing_fields)

            continue


        if not isinstance(data["amount"], (int, float)):

            print("Invalid amount!")

            continue


        # ----------------------------------------------------
        # SAVE TO NEO4J
        # ----------------------------------------------------

        try:

            save_transaction(data)

            print("Transaction saved to Neo4j successfully!")

            print("--------------------------------------")


        except Exception as e:

            print("ERROR: Could not save transaction to Neo4j")

            print(e)


except KeyboardInterrupt:

    print("\nConsumer stopped by user.")


finally:

    consumer.close()

    driver.close()

    print("Connections closed.")