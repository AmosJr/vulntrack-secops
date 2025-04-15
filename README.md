# vulntrack-secops
A vulnerability tracking system for SecOps

MARKDOWN

# VulnTrack SecOps

A full-stack, enterprise-style vulnerability tracking system that simulates a real-world SecOps pipeline — including ingestion, storage, querying, frontend analytics, and data archiving.

Built with:
- Python
- PostgreSQL
- FastAPI
- Streamlit
- Docker

---

## Project Overview

VulnTrack SecOps is designed to replicate the tools and workflows used by security teams at financial institutions. It simulates how vulnerability data is collected from scanners, processed, stored securely, and then queried or visualized for decision-making and compliance.

---

## Architecture

SCSS

          ┌─────────────────────┐
          │  Flask Mock Scanner │
          │  (JSON API)         │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  Ingestion Script   │
          │ fetch_and_store.py  │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │   PostgreSQL (DB)   │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │  FastAPI Backend    │
          │   (RESTful API)     │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │  Streamlit Frontend │
          └─────────────────────┘

          ┌────────────┐
          │  Archive   │
          │  to JSON   │
          └────────────┘

YAML

---

## Tech Stack

| Component        | Tool/Framework      |
|------------------|---------------------|
| Backend API      | FastAPI + Uvicorn   |
| Data Ingestion   | Python + Requests   |
| Data Storage     | PostgreSQL (Docker) |
| Frontend UI      | Streamlit + Pandas  |
| Archiving        | JSON (S3-ready)     |
| Environment Mgmt | python-dotenv       |
| Mock Data Source | Flask               |

---

## 📁 Project Structure

vulntrack-secops/
├── api/                    # FastAPI backend
│   ├── main.py             # Entry point
│   ├── models.py           # Pydantic models
│   └── routes.py           # Endpoints
├── ingestion/              # Ingestion from mock API
│   └── fetch_and_store.py
├── archive/                # AWS S3 archiver
│   └── archive_to_s3.py
├── db/
│   └── init.sql            # DB schema
├── config/
│   └── settings.py         # DB, S3, API config
├── utils/
│   └── logger.py           # Custom logger
├── mock_scanner_api.py     # Mock API provider
├── requirements.txt
├── README.md
└── .env                    # Credentials & secrets

---

## 🚀 Getting Started

1. Clone the Repository
bash
git clone https://github.com/AmosJr/vulntrack-secops.git
cd vulntrack-secops

2. Create & Activate Virtual Environment
bash
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
bash
pip install -r requirements.txt

4. Start PostgreSQL (via Docker)
bash
docker compose up -d

Then run the schema:
bash
psql -h localhost -U postgres -d vulntrack -f db/init.sql

---

▶️ How to Run Each Component

-Mock Vulnerability Scanner

python3 mock_scanner_api.py

-Ingest Data into PostgreSQL

python3 ingestion/fetch_and_store.py

-Start FastAPI Backend

uvicorn api.main:app --reload

Visit: http://localhost:8000/docs

-Launch Streamlit Frontend

streamlit run dashboard/vuln_dashboard.py

Visit: http://localhost:8501

-Simulate Archiving (Resolved/Old Vulns)

python3 archive/archive_to_s3.py

_____
✅ Features
 Pull mock scanner data via API
 
 Store and query in PostgreSQL
 
 REST API to filter vulnerabilities
 
 Streamlit dashboard with filtering
 
 Highlight unresolved vulnerabilities
 
 Simulated archiving to local JSON
_____
📈 Future Enhancements
Add authentication to FastAPI

Connect archiver to AWS S3 (via boto3)

Add charts to Streamlit dashboard

Schedule ingestion with CRON or Airflow

Dockerize the whole stack
______
🧠 Real-World Relevance
This project simulates systems used by security teams in:

Banking & Fintech

Cloud Security Engineering

Cyber Threat Management

Built to demonstrate both backend & frontend engineering skills with a focus on security, data, and cloud-readiness.
_____

👨‍💻 Author
Amos K. Agyeman
