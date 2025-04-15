from fastapi import APIRouter
from typing import List
from api.models import Vulnerability
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize FastAPI's router system
router = APIRouter()

# Pull database connection string from environment
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vulntrack")

# Function to query the database
def query_db(query: str, params=None):
    conn = psycopg2.connect(DB_URL)        # Connect to the PostgreSQL database
    cur = conn.cursor()                    # Create a cursor object to execute SQL
    cur.execute(query, params or ())       # Execute the provided SQL query
    rows = cur.fetchall()                  # Fetch all resulting rows
    cur.close()
    conn.close()
    return rows                            # Return the result rows

# Route: GET all vulnerabilities
@router.get("/vulnerabilities", response_model=List[Vulnerability])
def get_all():
    rows = query_db("SELECT * FROM vulnerabilities ORDER BY detected_on DESC")
    return [dict(zip(
        ["id", "source", "severity", "description", "detected_on", "remediation_status"], row
    )) for row in rows]

# Route: GET vulnerabilities by severity (e.g., /vulnerabilities/severity/high)
@router.get("/vulnerabilities/severity/{level}", response_model=List[Vulnerability])
def get_by_severity(level: str):
    rows = query_db(
        "SELECT * FROM vulnerabilities WHERE severity = %s ORDER BY detected_on DESC", 
        (level,)
    )
    return [dict(zip(
        ["id", "source", "severity", "description", "detected_on", "remediation_status"], row
    )) for row in rows]

# Route: GET recent vulnerabilities (last 7 days)
@router.get("/vulnerabilities/recent", response_model=List[Vulnerability])
def get_recent():
    rows = query_db(
        "SELECT * FROM vulnerabilities WHERE detected_on >= NOW() - INTERVAL '7 days' ORDER BY detected_on DESC"
    )
    return [dict(zip(
        ["id", "source", "severity", "description", "detected_on", "remediation_status"], row
    )) for row in rows]
