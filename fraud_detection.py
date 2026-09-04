from neo4j import GraphDatabase
import os

# ======================================
# Neo4j Configuration
# ======================================

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_DATABASE = "neo4j"

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not NEO4J_PASSWORD:
    raise ValueError("NEO4J_PASSWORD environment variable is not set")


# ======================================
# Neo4j Driver
# ======================================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


# ======================================
# Risk Score Calculation
# ======================================

def calculate_risk_score(amount, starburst=False, circular=False):

    score = 0

    # Risk scoring thresholds
    HIGH_VALUE_THRESHOLD = 50000
    MEDIUM_VALUE_THRESHOLD = 25000

    # High transaction amount
    if amount >= HIGH_VALUE_THRESHOLD:
        score += 30
    elif amount >= MEDIUM_VALUE_THRESHOLD:
        score += 15

    # Starburst pattern
    if starburst:
        score += 30

    # Circular pattern
    if circular:
        score += 40

    # Keep risk score within 0-100
    return min(score, 100)


# ======================================
# Create Fraud Alert
# ======================================

def create_fraud_alert(
    tx,
    transaction_id,
    account_id,
    risk_score,
    reason
):

    query = """
    MATCH (a:Account {account_id: $account_id})

    MERGE (f:FraudAlert {
        transaction_id: $transaction_id
    })

    SET f.risk_score = $risk_score,
        f.reason = $reason

    MERGE (a)-[:HAS_ALERT]->(f)
    """

    tx.run(
        query,
        account_id=account_id,
        transaction_id=transaction_id,
        risk_score=risk_score,
        reason=reason
    )


# ======================================
# Detect Starburst Pattern
# ======================================

def process_starburst(tx):

    query = """
    MATCH (sender:Account)-[:SENDS|SENT]->(t:Transaction)
          -[:RECEIVED_BY]->(receiver:Account)

    WHERE receiver.account_id = 'A999'

    RETURN DISTINCT
           sender.account_id AS sender,
           t.transaction_id AS transaction_id,
           t.amount AS amount

    ORDER BY amount DESC
    LIMIT 20
    """

    return list(tx.run(query))


# ======================================
# Detect Circular Pattern
# ======================================

def process_circular(tx):

    query = """
    MATCH (a:Account)-[:SENDS|SENT]->(t1:Transaction)
          -[:RECEIVED_BY]->(b:Account),

          (b)-[:SENDS|SENT]->(t2:Transaction)
          -[:RECEIVED_BY]->(c:Account),

          (c)-[:SENDS|SENT]->(t3:Transaction)
          -[:RECEIVED_BY]->(a:Account)

    WHERE a.account_id < b.account_id
      AND a.account_id < c.account_id
      AND b.account_id < c.account_id

    RETURN DISTINCT
           a.account_id AS account1,
           b.account_id AS account2,
           c.account_id AS account3,

           t1.transaction_id AS transaction1,
           t2.transaction_id AS transaction2,
           t3.transaction_id AS transaction3,

           t1.amount AS amount1,
           t2.amount AS amount2,
           t3.amount AS amount3

    LIMIT 10
    """

    return list(tx.run(query))


# ======================================
# Main Function
# ======================================

def main():

    print("======================================")
    print("FinGraph Risk Scoring System")
    print("======================================")

    try:

        with driver.session(database=NEO4J_DATABASE) as session:

            # --------------------------------
            # STARBURST DETECTION
            # --------------------------------

            print("\nChecking Starburst Pattern...")

            starburst = session.execute_read(
                process_starburst
            )

            if starburst:

                print("Starburst pattern detected!")

                for record in starburst:

                    risk_score = calculate_risk_score(
                        record["amount"],
                        starburst=True
                    )

                    reason = (
                        "Starburst transaction to common receiver"
                    )

                    session.execute_write(
                        create_fraud_alert,
                        record["transaction_id"],
                        record["sender"],
                        risk_score,
                        reason
                    )

                    print(
                        f"{record['sender']} -> A999 | "
                        f"{record['transaction_id']} | "
                        f"Rs.{record['amount']:.2f} | "
                        f"Risk Score: {risk_score}"
                    )

            else:

                print("No starburst pattern detected.")


            # --------------------------------
            # CIRCULAR DETECTION
            # --------------------------------

            print("\nChecking Circular Pattern...")

            circular = session.execute_read(
                process_circular
            )

            if circular:

                print("Circular transaction pattern detected!")

                for record in circular:

                    accounts = [
                        record["account1"],
                        record["account2"],
                        record["account3"]
                    ]

                    transactions = [
                        record["transaction1"],
                        record["transaction2"],
                        record["transaction3"]
                    ]

                    amounts = [
                        record["amount1"],
                        record["amount2"],
                        record["amount3"]
                    ]

                    for account, transaction_id, amount in zip(
                        accounts,
                        transactions,
                        amounts
                    ):

                        risk_score = calculate_risk_score(
                            amount,
                            circular=True
                        )

                        reason = (
                            "Circular transaction pattern"
                        )

                        session.execute_write(
                            create_fraud_alert,
                            transaction_id,
                            account,
                            risk_score,
                            reason
                        )

                    print(
                        f"{record['account1']} -> "
                        f"{record['account2']} -> "
                        f"{record['account3']} -> "
                        f"{record['account1']}"
                    )

                    print(
                        "Risk Score: 100"
                    )

            else:

                print("No circular pattern detected.")


        print("\n======================================")
        print("Risk scoring completed!")
        print("Fraud alerts created in Neo4j.")
        print("======================================")


    except Exception as e:

        print("\nERROR:")
        print(e)


    finally:

        driver.close()


# ======================================
# Program Entry Point
# ======================================

if __name__ == "__main__":
    main()