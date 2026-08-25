from kafka import KafkaProducer
import json
import time
# Kafka configuration
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"
KAFKA_TOPIC = "fingraph"

from transaction_simulator import (
    generate_transaction,
    generate_starburst_transactions,
    generate_circular_transactions
)


# -----------------------------
# Kafka Producer
# -----------------------------

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def send_transaction(transaction):

    try:

        future = producer.send(
            KAFKA_TOPIC,
            value=transaction
        )

        record_metadata = future.get(timeout=10)

        print("\nTransaction sent successfully!")
        print("--------------------------------")
        print(f"Transaction ID : {transaction['transaction_id']}")
        print(f"Sender         : {transaction['sender_account']}")
        print(f"Receiver       : {transaction['receiver_account']}")
        print(f"Amount         : ₹{transaction['amount']}")
        print(f"Bank           : {transaction['bank']}")
        print(f"Topic          : {record_metadata.topic}")
        print(f"Partition      : {record_metadata.partition}")
        print(f"Offset         : {record_metadata.offset}")

    except Exception as e:

        print("ERROR: Could not send transaction to Kafka")
        print(e)


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    print("FinGraph Kafka Producer started...")
    print("Sending financial transactions...\n")


    # -------------------------
    # Normal transactions
    # -------------------------

    for i in range(1, 6):

        transaction_id = f"TX{i:03d}"

        transaction = generate_transaction(transaction_id)

        send_transaction(transaction)

        time.sleep(1)


    # -------------------------
    # Starburst fraud
    # -------------------------

    print("\n==============================")
    print("STARBURST TRANSACTIONS")
    print("==============================")

    starburst_transactions = generate_starburst_transactions()

    for transaction in starburst_transactions:

        send_transaction(transaction)

        time.sleep(1)


    # -------------------------
    # Circular fraud
    # -------------------------

    print("\n==============================")
    print("CIRCULAR TRANSACTIONS")
    print("==============================")

    circular_transactions = generate_circular_transactions()

    for transaction in circular_transactions:

        send_transaction(transaction)

        time.sleep(1)


    producer.flush()
    producer.close()

    print("\nAll transactions sent successfully!")