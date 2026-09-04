import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinGraph | Fraud Detection",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

h1, h2, h3 {
    color: #f8fafc;
}

p, label {
    color: #cbd5e1;
}

div[data-testid="stMetric"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

div[data-testid="stMetric"] label {
    color: #94a3b8;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

.alert-box {
    padding: 18px;
    border-radius: 12px;
    margin: 12px 0;
    background-color: #1e293b;
    border: 1px solid #334155;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 10px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


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
        'Set it in PowerShell using: '
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
# CYPHER QUERY FUNCTION
# ============================================================

def run_query(query, parameters=None):

    with driver.session(database=NEO4J_DATABASE) as session:

        result = session.run(
            query,
            parameters or {}
        )

        return [record.data() for record in result]


# ============================================================
# PROFESSIONAL HEADER
# ============================================================

st.html("""
<div style="
    margin-bottom: 8px;
">
    <div style="
        font-size: 2.4rem;
        font-weight: 800;
        color: #f8fafc;
    ">
        🚨 FinGraph
    </div>

    <div style="
        font-size: 1rem;
        color: #94a3b8;
        margin-top: 4px;
        margin-bottom: 25px;
    ">
        Financial Fraud Detection & Risk Monitoring Platform
    </div>
</div>
""")


# ============================================================
# SECURITY MONITORING BANNER
# ============================================================

st.html("""
<div style="
    background: linear-gradient(135deg, #1e293b, #111827);
    padding: 22px 26px;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 25px;
">

    <div style="
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
    ">
        🛡️ Real-Time Financial Security Monitoring
    </div>

    <div style="
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 7px;
    ">
        Monitor transactions, detect suspicious patterns, and investigate
        potential financial fraud using Kafka, Python and Neo4j.
    </div>

</div>
""")


# ============================================================
# DASHBOARD METRICS
# ============================================================

transaction_result = run_query("""
MATCH (t:Transaction)
RETURN count(t) AS total_transactions
""")

total_transactions = (
    transaction_result[0]["total_transactions"]
    if transaction_result
    else 0
)


account_result = run_query("""
MATCH (a:Account)
RETURN count(a) AS total_accounts
""")

total_accounts = (
    account_result[0]["total_accounts"]
    if account_result
    else 0
)


high_risk_result = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)

WHERE alert.risk_score >= 80

RETURN count(DISTINCT a) AS high_risk
""")

high_risk = (
    high_risk_result[0]["high_risk"]
    if high_risk_result
    else 0
)


alert_result = run_query("""
MATCH (alert:FraudAlert)
RETURN count(alert) AS total_alerts
""")

total_alerts = (
    alert_result[0]["total_alerts"]
    if alert_result
    else 0
)


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.html("""
<div style="
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 15px;
">
    📊 System Overview
</div>
""")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Total Transactions",
        f"{total_transactions:,}"
    )


with col2:

    st.metric(
        "👤 Total Accounts",
        f"{total_accounts:,}"
    )


with col3:

    st.metric(
        "🔴 High Risk Accounts",
        f"{high_risk:,}"
    )


with col4:

    st.metric(
        "🚨 Fraud Alerts",
        f"{total_alerts:,}"
    )


st.divider()


# ============================================================
# HIGH-RISK ACCOUNTS
# ============================================================

st.html("""
<div style="
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 15px;
">
    ⚠️ High-Risk Accounts
</div>
""")


high_risk_accounts = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)

WHERE alert.risk_score >= 80

RETURN
    a.account_id AS account,
    max(alert.risk_score) AS risk_score,
    count(alert) AS fraud_alerts

ORDER BY risk_score DESC
""")


if high_risk_accounts:

    high_risk_df = pd.DataFrame(high_risk_accounts)

    high_risk_df["risk_level"] = high_risk_df["risk_score"].apply(
        lambda x: "HIGH" if x >= 80
        else "MEDIUM" if x >= 50
        else "LOW"
    )

    high_risk_df = high_risk_df[
        [
            "account",
            "risk_score",
            "risk_level",
            "fraud_alerts"
        ]
    ]

    st.dataframe(
        high_risk_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("✅ No high-risk accounts detected.")


st.divider()


# ============================================================
# RECENT FRAUD ALERTS
# ============================================================

st.html("""
<div style="
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 15px;
">
    🚨 Recent Fraud Alerts
</div>
""")


recent_alerts = run_query("""
MATCH (a:Account)-[:HAS_ALERT]->(alert:FraudAlert)

RETURN
    a.account_id AS account,
    alert.transaction_id AS transaction_id,
    alert.risk_score AS risk_score,
    alert.reason AS reason

ORDER BY alert.risk_score DESC

LIMIT 10
""")


if recent_alerts:

    for alert in recent_alerts:

        account = alert["account"]
        transaction_id = alert["transaction_id"]

        risk_score = (
            alert["risk_score"]
            if alert["risk_score"] is not None
            else 0
        )

        reason = (
            alert["reason"]
            if alert["reason"]
            else "Suspicious activity detected."
        )


        if risk_score >= 80:

            risk_level = "HIGH"
            risk_icon = "🔴"

        elif risk_score >= 50:

            risk_level = "MEDIUM"
            risk_icon = "🟠"

        else:

            risk_level = "LOW"
            risk_icon = "🟢"


        if "Starburst" in reason:

            pattern = "STARBURST"

        elif "Circular" in reason:

            pattern = "CIRCULAR"

        else:

            pattern = "OTHER"


        # Escape user/database text before placing it into HTML
        account_safe = str(account).replace("<", "&lt;").replace(">", "&gt;")
        transaction_safe = str(transaction_id).replace("<", "&lt;").replace(">", "&gt;")
        reason_safe = str(reason).replace("<", "&lt;").replace(">", "&gt;")


        st.html(f"""
        <div style="
            padding: 18px;
            border-radius: 12px;
            margin: 12px 0;
            background: #1e293b;
            border: 1px solid #334155;
        ">

            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
            ">

                <div style="
                    font-size: 1.05rem;
                    font-weight: 700;
                    color: #f8fafc;
                ">
                    {risk_icon} {risk_level} RISK
                </div>

                <div style="
                    font-size: 1.1rem;
                    font-weight: 800;
                    color: #f8fafc;
                ">
                    Risk Score: {risk_score}
                </div>

            </div>


            <div style="
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
            ">

                <div>
                    <div style="
                        color: #94a3b8;
                        font-size: 0.75rem;
                    ">
                        ACCOUNT
                    </div>

                    <div style="
                        color: #f8fafc;
                        font-weight: 600;
                    ">
                        {account_safe}
                    </div>
                </div>


                <div>
                    <div style="
                        color: #94a3b8;
                        font-size: 0.75rem;
                    ">
                        TRANSACTION
                    </div>

                    <div style="
                        color: #f8fafc;
                        font-weight: 600;
                    ">
                        {transaction_safe}
                    </div>
                </div>


                <div>
                    <div style="
                        color: #94a3b8;
                        font-size: 0.75rem;
                    ">
                        PATTERN
                    </div>

                    <div style="
                        color: #f8fafc;
                        font-weight: 600;
                    ">
                        {pattern}
                    </div>
                </div>


                <div>
                    <div style="
                        color: #94a3b8;
                        font-size: 0.75rem;
                    ">
                        STATUS
                    </div>

                    <div style="
                        color: #f8fafc;
                        font-weight: 600;
                    ">
                        OPEN
                    </div>
                </div>

            </div>


            <div style="
                margin-top: 15px;
                padding-top: 12px;
                border-top: 1px solid #334155;
                color: #cbd5e1;
                font-size: 0.9rem;
            ">
                🔍 {reason_safe}
            </div>

        </div>
        """)

else:

    st.success("✅ No fraud alerts found.")


st.divider()


# ============================================================
# STARBURST FRAUD
# ============================================================

st.header("⭐ Starburst Fraud")


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
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Starburst fraud alerts found.")


# ============================================================
# CIRCULAR FRAUD
# ============================================================

st.header("🔄 Circular Fraud")


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
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Circular fraud alerts found.")


st.divider()


# ============================================================
# RECENT TRANSACTIONS
# ============================================================

st.header("💰 Recent Transactions")


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
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No transactions found.")


# ============================================================
# FRAUD ANALYTICS
# ============================================================

st.divider()

st.header("📊 Fraud Analytics")


# ------------------------------------------------------------
# FRAUD ALERTS BY PATTERN
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
# RISK LEVEL DISTRIBUTION
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
# RISK SCORE ANALYSIS
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
# TRANSACTION AMOUNT ANALYSIS
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
        use_container_width=True,
        hide_index=True
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


selected_account = None


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
    """, {
        "account": selected_account
    })


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

if selected_account:

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
    """, {
        "account": selected_account
    })


    if account_transactions:

        transaction_df = pd.DataFrame(
            account_transactions
        )

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No transactions found for this account."
        )


# ============================================================
# SELECTED ACCOUNT FRAUD ALERTS
# ============================================================

if selected_account:

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
    """, {
        "account": selected_account
    })


    if account_alerts:

        alert_df = pd.DataFrame(
            account_alerts
        )

        st.dataframe(
            alert_df,
            use_container_width=True,
            hide_index=True
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

    st.cache_resource.clear()

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FinGraph | Kafka + Python + Neo4j + Streamlit"
)