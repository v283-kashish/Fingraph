import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinGraph Fraud Detection",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 FinGraph Fraud Detection Dashboard")
st.write("Real-time financial transaction and fraud monitoring")


# ============================================================
# NEO4J CONFIGURATION
# ============================================================

NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = "neo4j"

if not NEO4J_PASSWORD:
    st.error("❌ NEO4J_PASSWORD environment variable is not set.")
    st.info(
        "Set it in PowerShell using: "
        '$env:NEO4J_PASSWORD="YOUR_NEO4J_PASSWORD"'
    )
    st.stop()


# ============================================================
# NEO4J CONNECTION
# ============================================================

@st.cache_resource
def connect_to_neo4j():

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    driver.verify_connectivity()

    return driver


try:

    driver = connect_to_neo4j()

except Exception as e:

    st.error("❌ Could not connect to Neo4j")
    st.error(str(e))
    st.stop()


# ============================================================
# FUNCTION TO RUN CYPHER
# ============================================================

def run_query(query, parameters=None):

    with driver.session(database=NEO4J_DATABASE) as session:

        result = session.run(
            query,
            parameters or {}
        )

        return [record.data() for record in result]


# ============================================================
# DASHBOARD METRICS
# ============================================================

transaction_result = run_query("""
MATCH (t:Transaction)
RETURN count(t) AS total_transactions
""")

total_transactions = transaction_result[0]["total_transactions"]


account_result = run_query("""
MATCH (a:Account)
RETURN count(a) AS total_accounts
""")

total_accounts = account_result[0]["total_accounts"]


high_risk_result = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)
WHERE alert.risk_score >= 80
RETURN count(DISTINCT a) AS high_risk
""")

high_risk = high_risk_result[0]["high_risk"]


alert_result = run_query("""
MATCH (alert:FraudAlert)
RETURN count(alert) AS total_alerts
""")

total_alerts = alert_result[0]["total_alerts"]


# ============================================================
# DISPLAY METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:
    st.metric(
        "Total Accounts",
        total_accounts
    )

with col3:
    st.metric(
        "High Risk Accounts",
        high_risk
    )

with col4:
    st.metric(
        "Fraud Alerts",
        total_alerts
    )


st.divider()


# ============================================================
# FRAUD ALERTS
# ============================================================

st.subheader("🚨 Fraud Alerts")

alerts = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)

WITH
    a.account_id AS account,
    alert.transaction_id AS transaction_id,
    alert.risk_score AS risk_score,
    alert.reason AS reason

RETURN
    account,
    transaction_id,
    risk_score,

    CASE
        WHEN risk_score >= 80 THEN "HIGH"
        WHEN risk_score >= 50 THEN "MEDIUM"
        ELSE "LOW"
    END AS risk_level,

    CASE
        WHEN reason CONTAINS "Starburst"
            THEN "STARBURST"
        WHEN reason CONTAINS "Circular"
            THEN "CIRCULAR"
        ELSE "OTHER"
    END AS pattern,

    "OPEN" AS status,

    reason

ORDER BY risk_score DESC
""")

if alerts:

    alerts_df = pd.DataFrame(alerts)

    st.dataframe(
        alerts_df,
        use_container_width=True
    )

else:

    st.info("No fraud alerts found.")


st.divider()


# ============================================================
# HIGH-RISK ACCOUNTS
# ============================================================

st.subheader("⚠️ High-Risk Accounts")

high_risk_accounts = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)
WHERE alert.risk_score >= 80

RETURN
    a.account_id AS account,
    max(alert.risk_score) AS risk_score,

    CASE
        WHEN max(alert.risk_score) >= 80 THEN "HIGH"
        WHEN max(alert.risk_score) >= 50 THEN "MEDIUM"
        ELSE "LOW"
    END AS risk_level,

    count(alert) AS fraud_alerts

ORDER BY risk_score DESC
""")

if high_risk_accounts:

    high_risk_df = pd.DataFrame(high_risk_accounts)

    st.dataframe(
        high_risk_df,
        use_container_width=True
    )

else:

    st.info("No high-risk accounts found.")


st.divider()


# ============================================================
# STARBURST FRAUD
# ============================================================

st.subheader("⭐ Starburst Fraud")

starburst = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)

WHERE alert.reason CONTAINS "Starburst"

RETURN
    a.account_id AS account,
    alert.transaction_id AS transaction_id,
    alert.risk_score AS risk_score,

    CASE
        WHEN alert.risk_score >= 80 THEN "HIGH"
        WHEN alert.risk_score >= 50 THEN "MEDIUM"
        ELSE "LOW"
    END AS risk_level,

    alert.reason AS description

ORDER BY alert.risk_score DESC
""")

if starburst:

    st.dataframe(
        pd.DataFrame(starburst),
        use_container_width=True
    )

else:

    st.info("No Starburst fraud alerts found.")


# ============================================================
# CIRCULAR FRAUD
# ============================================================

st.subheader("🔄 Circular Fraud")

circular = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)

WHERE alert.reason CONTAINS "Circular"

RETURN
    a.account_id AS account,
    alert.transaction_id AS transaction_id,
    alert.risk_score AS risk_score,

    CASE
        WHEN alert.risk_score >= 80 THEN "HIGH"
        WHEN alert.risk_score >= 50 THEN "MEDIUM"
        ELSE "LOW"
    END AS risk_level,

    alert.reason AS description

ORDER BY alert.risk_score DESC
""")

if circular:

    st.dataframe(
        pd.DataFrame(circular),
        use_container_width=True
    )

else:

    st.info("No Circular fraud alerts found.")


st.divider()


# ============================================================
# TRANSACTIONS
# ============================================================

st.subheader("💰 Recent Transactions")

transactions = run_query("""
MATCH (sender:Account)-[:SENDS]->(t:Transaction)
      -[:RECEIVED_BY]->(receiver:Account)

RETURN
    t.transaction_id AS transaction_id,
    sender.account_id AS sender,
    receiver.account_id AS receiver,
    t.amount AS amount,
    t.bank AS bank,
    t.timestamp AS timestamp

ORDER BY t.timestamp DESC

LIMIT 50
""")

if transactions:

    transactions_df = pd.DataFrame(transactions)

    st.dataframe(
        transactions_df,
        use_container_width=True
    )

else:

    st.info("No transactions found.")


# ============================================================
# FRAUD ANALYTICS
# ============================================================

st.divider()

st.header("📊 Fraud Analytics")


# ------------------------------------------------------------
# 1. FRAUD ALERTS BY PATTERN
# ------------------------------------------------------------

st.subheader("🚨 Fraud Alerts by Pattern")

pattern_data = run_query("""
MATCH (alert:FraudAlert)

RETURN

CASE
    WHEN alert.reason CONTAINS "Starburst"
        THEN "STARBURST"

    WHEN alert.reason CONTAINS "Circular"
        THEN "CIRCULAR"

    ELSE "OTHER"
END AS pattern,

count(alert) AS count

ORDER BY count DESC
""")

if pattern_data:

    pattern_df = pd.DataFrame(pattern_data)

    st.bar_chart(
        pattern_df.set_index("pattern")["count"],
        use_container_width=True
    )

else:

    st.info("No fraud pattern data available.")


# ------------------------------------------------------------
# 2. RISK LEVEL DISTRIBUTION
# ------------------------------------------------------------

st.subheader("⚠️ Risk Level Distribution")

risk_data = run_query("""
MATCH (alert:FraudAlert)

RETURN

CASE
    WHEN alert.risk_score >= 80
        THEN "HIGH"

    WHEN alert.risk_score >= 50
        THEN "MEDIUM"

    ELSE "LOW"
END AS risk_level,

count(alert) AS count

ORDER BY count DESC
""")

if risk_data:

    risk_df = pd.DataFrame(risk_data)

    st.bar_chart(
        risk_df.set_index("risk_level")["count"],
        use_container_width=True
    )

else:

    st.info("No risk-level data available.")


# ------------------------------------------------------------
# 3. RISK SCORE ANALYSIS
# ------------------------------------------------------------

st.subheader("📈 Risk Score Analysis")

score_data = run_query("""
MATCH (alert:FraudAlert)

WHERE alert.risk_score IS NOT NULL

RETURN
    alert.transaction_id AS transaction_id,
    alert.risk_score AS risk_score

ORDER BY risk_score DESC
""")

if score_data:

    score_df = pd.DataFrame(score_data)

    st.line_chart(
        score_df.set_index("transaction_id")["risk_score"],
        use_container_width=True
    )

else:

    st.info("No risk-score data available.")


# ------------------------------------------------------------
# 4. TRANSACTION AMOUNT ANALYSIS
# ------------------------------------------------------------

st.subheader("💰 Transaction Amount Analysis")

amount_data = run_query("""
MATCH (t:Transaction)

RETURN
    t.transaction_id AS transaction_id,
    t.amount AS amount

ORDER BY t.timestamp DESC

LIMIT 50
""")

if amount_data:

    amount_df = pd.DataFrame(amount_data)

    st.bar_chart(
        amount_df.set_index("transaction_id")["amount"],
        use_container_width=True
    )

else:

    st.info("No transaction amount data available.")


# ============================================================
# TRANSACTION NETWORK
# ============================================================

st.divider()

st.header("🕸️ Transaction Network")

network_data = run_query("""
MATCH (sender:Account)-[:SENDS]->(t:Transaction)
      -[:RECEIVED_BY]->(receiver:Account)

RETURN
    sender.account_id AS sender,
    receiver.account_id AS receiver,
    t.transaction_id AS transaction_id,
    t.amount AS amount

LIMIT 100
""")

if network_data:

    network_df = pd.DataFrame(network_data)

    st.dataframe(
        network_df,
        use_container_width=True
    )

else:

    st.info("No transaction network data available.")


# ============================================================
# FRAUD INVESTIGATION
# ============================================================

st.divider()

st.header("🔎 Fraud Investigation")

accounts_data = run_query("""
MATCH (a:Account)

RETURN a.account_id AS account

ORDER BY account
""")

if accounts_data:

    account_list = [
        row["account"]
        for row in accounts_data
    ]

    selected_account = st.selectbox(
        "Select an account to investigate",
        account_list
    )

    investigation = run_query("""
    MATCH (a:Account {account_id: $account})

    OPTIONAL MATCH (a)-[:SENDS]->(sent:Transaction)

    OPTIONAL MATCH (a)<-[:RECEIVED_BY]-(received:Transaction)

    OPTIONAL MATCH (a)-[:HAS_ALERT]->(alert:FraudAlert)

    WITH
        a,
        count(DISTINCT sent) AS transactions_sent,
        count(DISTINCT received) AS transactions_received,
        count(DISTINCT alert) AS fraud_alerts,
        max(alert.risk_score) AS risk_score

    RETURN
        a.account_id AS account,
        risk_score,

        CASE
            WHEN risk_score >= 80 THEN "HIGH"
            WHEN risk_score >= 50 THEN "MEDIUM"
            ELSE "LOW"
        END AS risk_level,

        transactions_sent,
        transactions_received,
        fraud_alerts
    """, {"account": selected_account})

    if investigation:

        result = investigation[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Risk Score",
                result["risk_score"] or 0
            )

        with col2:
            st.metric(
                "Risk Level",
                result["risk_level"]
            )

        with col3:
            st.metric(
                "Transactions Sent",
                result["transactions_sent"]
            )

        with col4:
            st.metric(
                "Fraud Alerts",
                result["fraud_alerts"]
            )

else:

    st.info("No accounts available for investigation.")


# ============================================================
# SELECTED ACCOUNT TRANSACTIONS
# ============================================================

if accounts_data:

    st.subheader("💰 Account Transactions")

    account_transactions = run_query("""
    MATCH (sender:Account)-[:SENDS]->(t:Transaction)
          -[:RECEIVED_BY]->(receiver:Account)

    WHERE sender.account_id = $account
       OR receiver.account_id = $account

    RETURN
        t.transaction_id AS transaction_id,
        sender.account_id AS sender,
        receiver.account_id AS receiver,
        t.amount AS amount,
        t.bank AS bank,
        t.timestamp AS timestamp

    ORDER BY t.timestamp DESC
    """, {"account": selected_account})

    if account_transactions:

        transaction_df = pd.DataFrame(
            account_transactions
        )

        st.dataframe(
            transaction_df,
            use_container_width=True
        )

    else:

        st.info(
            "No transactions found for this account."
        )


# ============================================================
# SELECTED ACCOUNT FRAUD ALERTS
# ============================================================

if accounts_data:

    st.subheader("🚨 Account Fraud Alerts")

    account_alerts = run_query("""
    MATCH (a:Account {account_id: $account})
          -[:HAS_ALERT]->(alert:FraudAlert)

    RETURN
        alert.transaction_id AS transaction_id,
        alert.risk_score AS risk_score,

        CASE
            WHEN alert.risk_score >= 80 THEN "HIGH"
            WHEN alert.risk_score >= 50 THEN "MEDIUM"
            ELSE "LOW"
        END AS risk_level,

        CASE
            WHEN alert.reason CONTAINS "Starburst"
                THEN "STARBURST"

            WHEN alert.reason CONTAINS "Circular"
                THEN "CIRCULAR"

            ELSE "OTHER"
        END AS pattern,

        "OPEN" AS status,

        alert.reason AS reason

    ORDER BY alert.risk_score DESC
    """, {"account": selected_account})

    if account_alerts:

        alert_df = pd.DataFrame(
            account_alerts
        )

        st.dataframe(
            alert_df,
            use_container_width=True
        )

    else:

        st.info(
            "No fraud alerts found for this account."
        )


# ============================================================
# REFRESH BUTTON
# ============================================================

st.divider()

if st.button("🔄 Refresh Dashboard"):

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FinGraph | Kafka + Python + Neo4j + Streamlit"
)