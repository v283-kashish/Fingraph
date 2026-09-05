# FinGraph

## Project Overview

FinGraph is a real-time financial fraud detection and risk monitoring platform designed to analyze financial transactions and identify suspicious activities using graph-based analysis.

The system combines Apache Kafka for real-time transaction streaming, Python for transaction processing and fraud analysis, Neo4j for graph-based relationship analysis, and Streamlit for interactive visualization and monitoring.

FinGraph detects suspicious transaction patterns such as starburst transactions, circular transactions, and high-value transactions. It assigns risk scores to suspicious activities and generates fraud alerts that can be investigated through the dashboard.

## Technologies Used





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

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/v283-kashish/Fingraph.git
cd Fingraph

