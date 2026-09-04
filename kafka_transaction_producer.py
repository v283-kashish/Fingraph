from kafka import KafkaProducer
import json
import time

from transaction_simulator import (
    generate_transaction,
    generate_starburst_transactions,
    generate_circular_transactions
)

# ============================================================
# KAFKA CONFIGURATION
# ============================================================

KAFKA_BOOTSTRAP_SERVER = "localhost:9092"
KAFKA_TOPIC = "fingraph"

# Producer settings
SEND_TIMEOUT = 10
TRANSACTION_DELAY = 1


# ============================================================
# CREATE KAFKA PRODUCER
# ============================================================

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


# ============================================================
# SEND TRANSACTION
# ============================================================

def send_transaction(transaction):

    try:

        future = producer.send(
            KAFKA_TOPIC,
            value=transaction
        )

        record_metadata = future.get(
            timeout=SEND_TIMEOUT
        )

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


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("======================================")
    print("FinGraph Kafka Transaction Producer")
    print("======================================")

    # --------------------------------------------------------
    # SEND NORMAL TRANSACTIONS
    # --------------------------------------------------------

    print("\nSending normal transactions...")

    for i in range(1, 6):

        transaction = generate_transaction(i)

        send_transaction(transaction)

        time.sleep(TRANSACTION_DELAY)


    # --------------------------------------------------------
    # SEND STARBURST TRANSACTIONS
    # --------------------------------------------------------

    print("\nSending starburst transactions...")

    starburst_transactions = generate_starburst_transactions()

    for transaction in starburst_transactions:

        send_transaction(transaction)

        time.sleep(TRANSACTION_DELAY)


    # --------------------------------------------------------
    # SEND CIRCULAR TRANSACTIONS
    # --------------------------------------------------------

    print("\nSending circular transactions...")

    circular_transactions = generate_circular_transactions()

    for transaction in circular_transactions:

        send_transaction(transaction)

        time.sleep(TRANSACTION_DELAY)


    # --------------------------------------------------------
    # FINISH
    # --------------------------------------------------------

    producer.flush()
    producer.close()

    print("\n======================================")
    print("All transactions sent successfully!")
    print("======================================")