\## Fraud Detection



FinGraph includes a fraud detection and risk scoring module that identifies suspicious financial transaction patterns.



\### Detected Fraud Patterns



\- Starburst transactions

\- Circular transactions

\- High-value transactions



\### Risk Scoring



Transactions are assigned a risk score based on:



\- Transaction amount

\- Starburst pattern detection

\- Circular transaction detection



Fraud alerts are stored in Neo4j and displayed through the Streamlit dashboard.



\## Dashboard



The Streamlit dashboard provides:



\- Total transaction monitoring

\- Account monitoring

\- Fraud alerts

\- High-risk account identification

\- Starburst fraud analysis

\- Circular fraud analysis

\- Risk score analysis

\- Transaction network

\- Account-level fraud investigation



\## Project Flow



Python Transaction Generator  

↓  

Apache Kafka  

↓  

Kafka Consumer  

↓  

Neo4j Graph Database  

↓  

Fraud Detection \& Risk Scoring  

↓  

Streamlit Fraud Detection Dashboard

