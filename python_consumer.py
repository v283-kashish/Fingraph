from kafka import KafkaConsumer
from neo4j import GraphDatabase
import json
import os

# ============================================================
# NEO4J CONFIGURATION
# ============================================================

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
if not NEO4J_PASSWORD:
    raise ValueError("NEO4J_PASSWORD environment variable is not set")
# IMPORTANT:
# Your Neo4j Query screen is showing database "fingraph"
NEO4J_DATABASE = "fingraph"


# ============================================================
# CONNECT TO NEO4J
# ============================================================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

try:
    driver.verify_connectivity()
    print("Neo4j connected successfully!")

except Exception as e:
    print("ERROR: Could not connect to Neo4j")
    print(e)
    driver.close()
    exit()


# ============================================================
# SAVE TRANSACTION TO NEO4J
# ============================================================

def save_transaction(data):

    query = """
    MERGE (sender:Account {
        account_id: $sender_account
    })

    MERGE (receiver:Account {
        account_id: $receiver_account
    })

    MERGE (t:Transaction {
        transaction_id: $transaction_id
    })

    SET
        t.amount = $amount,
        t.timestamp = $timestamp,
        t.bank = $bank

    MERGE (sender)-[:SENT]->(t)

    MERGE (t)-[:RECEIVED_BY]->(receiver)

    RETURN t
    """

    parameters = {
        "transaction_id": data["transaction_id"],
        "sender_account": data["sender_account"],
        "receiver_account": data["receiver_account"],
        "amount": data["amount"],
        "timestamp": data["timestamp"],
        "bank": data["bank"]
    }

    with driver.session(database=NEO4J_DATABASE) as session:

        session.run(
            query,
            parameters
        ).consume()


# ============================================================
# KAFKA CONSUMER
# ============================================================

consumer = KafkaConsumer(
    "fingraph",

    bootstrap_servers="localhost:9092",

    auto_offset_reset="earliest",

    enable_auto_commit=True,

    group_id="fingraph-neo4j-consumer-v2",

    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)


print("\n======================================")
print("FinGraph Kafka Consumer is running...")
print("Database: fingraph")
print("Waiting for transactions...")
print("======================================\n")


# ============================================================
# RECEIVE TRANSACTIONS
# ============================================================

try:

    for message in consumer:

        data = message.value

        print("\nReceived transaction:")
        print(data)

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
            print("Missing:", missing_fields)

            continue

        try:

            save_transaction(data)

            print(
                "Transaction + relationships "
                "saved to Neo4j successfully!"
            )

            print("--------------------------------------")

        except Exception as e:

            print("ERROR saving transaction:")
            print(e)


except KeyboardInterrupt:

    print("\nConsumer stopped.")

finally:

    consumer.close()
    driver.close()

    print("Connections closed.")