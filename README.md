\# FinGraph



FinGraph is a real-time financial fraud detection and risk monitoring platform that analyzes financial transactions and identifies suspicious transaction patterns using graph-based analysis.



\## Technologies Used



\- Python

\- Apache Kafka

\- Neo4j Graph Database

\- Streamlit

\- Pandas

\- Cypher

\- Git \& GitHub



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

\- Fraud alert monitoring

\- High-risk account identification

\- Starburst fraud analysis

\- Circular fraud analysis

\- Risk score analysis

\- Transaction amount analysis

\- Transaction network monitoring

\- Account-level fraud investigation

\- Account transaction history



\## Project Architecture



```text

Python Transaction Generator

&#x20;         |

&#x20;         v

&#x20;    Apache Kafka

&#x20;         |

&#x20;         v

&#x20;   Kafka Consumer

&#x20;         |

&#x20;         v

&#x20;  Neo4j Graph Database

&#x20;         |

&#x20;         v

Fraud Detection \& Risk Scoring

&#x20;         |

&#x20;         v

Streamlit Fraud Detection Dashboard

