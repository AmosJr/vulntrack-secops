import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load database credentials from .env file
load_dotenv()
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vulntrack")

# Local archive folder
ARCHIVE_DIR = "archive/output"
os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Create the folder if it doesn't exist

# Query to select vulnerabilities that are either resolved or older than 7 days
ARCHIVE_QUERY = """
SELECT * FROM vulnerabilities
WHERE remediation_status = 'resolved'
   OR detected_on < NOW() - INTERVAL '7 days'
ORDER BY detected_on ASC
"""

def fetch_archivable_records():
    """Connects to the DB and retrieves rows to be archived."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(ARCHIVE_QUERY)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def save_as_json(data):
    """Saves the archived data into a local .json file."""
    if not data:
        print("[INFO] No records to archive.")
        return

    # Convert DB rows into dictionaries
    field_names = ["id", "source", "severity", "description", "detected_on", "remediation_status"]
    records = [dict(zip(field_names, row)) for row in data]

    # Filename includes a timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_path = os.path.join(ARCHIVE_DIR, f"vulnerabilities_archive_{timestamp}.json")

    # Save data to JSON file
    with open(file_path, "w") as f:
        json.dump(records, f, indent=4, default=str)  # default=str handles datetime serialization

    print(f"[SUCCESS] Archived {len(records)} records to {file_path}")

if __name__ == "__main__":
    data = fetch_archivable_records()
    save_as_json(data)
