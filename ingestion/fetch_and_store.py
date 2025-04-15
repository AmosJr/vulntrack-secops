# Import required libraries
import requests                    # To send HTTP requests to the mock API
import psycopg2                    # PostgreSQL client library
from datetime import datetime      # To parse timestamps
from dotenv import load_dotenv     # Loads environment variables from a .env file
import os                          # Lets us read environment variables

# Load environment variables from a .env file (like DB credentials)
load_dotenv()

# Get the database connection string from the .env file
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vulntrack")

# Define the mock API endpoint URL (from your Flask mock server)
MOCK_API_URL = "http://localhost:5001/vulnerabilities"

# Function to fetch vulnerability data from the mock API
def fetch_data():
    try:
        response = requests.get(MOCK_API_URL)  # Send GET request to the API
        response.raise_for_status()            # Raise an error if the request failed
        return response.json()                 # Parse and return the JSON response
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch data: {e}")
        return []                              # Return empty list on failure

# Function to insert the fetched vulnerability data into PostgreSQL
def insert_into_postgres(data):
    try:
        # Connect to the PostgreSQL database using the DB_URL
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Loop through each item in the fetched vulnerability data
        for vuln in data:
            # Insert the data into the "vulnerabilities" table
            cur.execute("""
                INSERT INTO vulnerabilities (source, severity, description, detected_on, remediation_status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                vuln['source'],
                vuln['severity'],
                vuln['description'],
                datetime.fromisoformat(vuln['detected_on']),  # Convert ISO timestamp to datetime object
                vuln['remediation_status']
            ))

        # Commit the changes to the database
        conn.commit()
        cur.close()
        conn.close()
        print(f"[SUCCESS] Inserted {len(data)} vulnerabilities into PostgreSQL.")

    except Exception as e:
        print(f"[ERROR] Database error: {e}")

# Main script execution
if __name__ == "__main__":
    # Step 1: Fetch data from the mock scanner API
    data = fetch_data()
    
    # Step 2: If data is available, insert it into the database
    if data:
        insert_into_postgres(data)
