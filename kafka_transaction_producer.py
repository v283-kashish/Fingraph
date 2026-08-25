from kafka import KafkaProducer
import json
import time

# Kafka configuration
bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
KAFKA_TOPIC = "fingraph"

from transaction_simulator import (
    generate_transaction,
    generate_starburst_transactions,
    generate_circular_transactions
)


# --------------------------------
# KAFKA PRODUCER
# --------------------------------

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


print("======================================")
print("   FinGraph Transaction Producer")
print("======================================")
print("Kafka connected successfully!")
print("")


try:

    # --------------------------------
    # 1. NORMAL TRANSACTIONS
    # --------------------------------

    print("Sending normal transactions...")

    for i in range(1, 6):

        transaction = generate_transaction(
            f"TX{i:05d}"
        )

        producer.send(
            KAFKA_TOPIC,
            value=transaction
        )

        producer.flush()

        print(
            f"NORMAL | "
            f"{transaction['transaction_id']} | "
            f"{transaction['sender_account']} -> "
            f"{transaction['receiver_account']} | "
           Amount: ₹{transaction['amount']}
        )

        time.sleep(1)


    # --------------------------------
    # 2. STARBURST FRAUD PATTERN
    # --------------------------------

    print("\nSending STARBURST fraud pattern...")

    starburst_transactions = generate_starburst_transactions()

    for transaction in starburst_transactions:

        producer.send(
            KAFKA_TOPIC,
            value=transaction
        )

        producer.flush()

        print(
            f"⚠ STARBURST | "
            f"{transaction['transaction_id']} | "
            f"{transaction['sender_account']} -> "
            f"{transaction['receiver_account']} | "
            f"Amount: ₹{transaction['amount']}"
        )

        time.sleep(1)


    # --------------------------------
    # 3. CIRCULAR FRAUD PATTERN
    # --------------------------------

    print("\nSending CIRCULAR fraud pattern...")

    circular_transactions = generate_circular_transactions()

    for transaction in circular_transactions:

        producer.send(
             KAFKA_TOPIC,
            value=transaction
        )

        producer.flush()

        print(
            f"⚠ CIRCULAR | "
            f"{transaction['transaction_id']} | "
            f"{transaction['sender_account']} -> "
            f"{transaction['receiver_account']} | "
            f"Amount: ₹{transaction['amount']}"
        )

        time.sleep(1)


    print("\n======================================")
    print("All test transactions sent successfully!")
    print("======================================")


except Exception as e:

    print("\nERROR:")
    print(e)


finally:

    producer.close()