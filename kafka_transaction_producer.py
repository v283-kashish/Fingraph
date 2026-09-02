from kafka import KafkaProducer
import json
import time

from transaction_simulator import (
    generate_transaction,
    generate_starburst_transactions,
    generate_circular_transactions
)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"
KAFKA_TOPIC = "fingraph"

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def send_transaction(transaction):
    try:
        future = producer.send(KAFKA_TOPIC, value=transaction)
        record_metadata = future.get(timeout=10)

        print("--------------------------------------")
        print("Transaction sent successfully")
        print(f"Transaction ID : {transaction['transaction_id']}")
        print(f"Sender         : {transaction['sender_account']}")
        print(f"Receiver       : {transaction['receiver_account']}")
        print(f"Amount         : Rs.{transaction['amount']}")
        print(f"Bank           : {transaction['bank']}")
        print(f"Topic          : {record_metadata.topic}")
        print(f"Partition      : {record_metadata.partition}")
        print(f"Offset         : {record_metadata.offset}")
        print("--------------------------------------")

    except Exception as e:
        print(f"Error sending transaction: {e}")


if __name__ == "__main__":

    print("======================================")
    print("FinGraph Kafka Transaction Producer")
    print("======================================")

    # Send normal transactions
    print("\nSending normal transactions...")

    for i in range(1, 6):
        transaction = generate_transaction(i)
        send_transaction(transaction)
        time.sleep(1)

    # Send starburst transactions
    print("\nSending starburst transactions...")

    starburst_transactions = generate_starburst_transactions()

    for transaction in starburst_transactions:
        send_transaction(transaction)
        time.sleep(1)

    # Send circular transactions
    print("\nSending circular transactions...")

    circular_transactions = generate_circular_transactions()

    for transaction in circular_transactions:
        send_transaction(transaction)
        time.sleep(1)

    # Finish
    producer.flush()
    producer.close()

    print("\n======================================")
    print("All transactions sent successfully!")
    print("======================================")