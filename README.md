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

## System Workflow

FinGraph processes transactions through the following workflow:

1. Python generates financial transactions.
2. The Kafka Producer publishes transactions to the `fingraph` topic.
3. Apache Kafka streams the transaction data.
4. The Kafka Consumer receives the transactions.
5. Transactions are stored as nodes and relationships in Neo4j.
6. The Fraud Detection module analyzes transaction patterns.
7. Risk scores and fraud alerts are generated.
8. The Streamlit dashboard displays real-time monitoring and investigation results.
## Fraud Detection Patterns

FinGraph identifies multiple suspicious transaction patterns.

### High-Value Transactions

Transactions involving unusually large amounts are assigned additional risk points.

### Starburst Transactions

A starburst pattern occurs when one account sends transactions to multiple accounts in a short period. FinGraph identifies this pattern and increases the associated risk score.

### Circular Transactions

A circular pattern occurs when transactions form a cycle between accounts, such as:

A101 → A102 → A103 → A101

These cycles are analyzed as potentially suspicious transaction behavior.

### Risk Score

The fraud detection module combines transaction amount and detected patterns to calculate a risk score. Higher scores indicate greater potential risk.

## Dashboard Features

The FinGraph Streamlit dashboard provides an interactive interface for monitoring and investigating financial transactions.

### Monitoring

- Total transaction count
- Total account count
- Fraud alert count
- High-risk account monitoring

### Fraud Analysis

- Risk score analysis
- Starburst fraud detection
- Circular fraud detection
- Recent fraud alerts
- Fraud pattern analysis

### Investigation

- Transaction network visualization
- Account-level investigation
- Account transaction history
- Account-level fraud alerts

The dashboard helps users monitor suspicious activity and investigate potentially fraudulent accounts and transactions.
## Project Purpose

FinGraph is developed as an academic and practical project to demonstrate the use of real-time data streaming, graph databases, and fraud detection techniques.

The project provides a foundation for monitoring financial transactions and identifying suspicious relationships between accounts.

## Future Enhancements

- Machine learning-based fraud prediction
- Real-time alert notifications
- Advanced graph analytics
- Historical fraud trend analysis
- Role-based dashboard access
- Deployment on cloud infrastructure
