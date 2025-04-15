import streamlit as st
import requests
import pandas as pd

# Base URL of your FastAPI backend
API_BASE = "http://localhost:8000"

# App title
st.set_page_config(page_title="VulnTrack Dashboard", layout="wide")
st.title("🔐 VulnTrack SecOps Dashboard")
st.markdown("Easily view and analyze tracked vulnerabilities from your security ingestion pipeline.")

# Sidebar filter
severity_filter = st.sidebar.selectbox("Filter by Severity", options=["all", "high", "medium", "low"])

# Function to load data from API
@st.cache_data
def load_data(severity=None):
    try:
        if severity and severity != "all":
            response = requests.get(f"{API_BASE}/vulnerabilities/severity/{severity}")
        else:
            response = requests.get(f"{API_BASE}/vulnerabilities")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# Load data using selected filter
df = load_data(severity_filter)

# Display data summary
st.subheader(f"📊 Showing {len(df)} vulnerabilities")
if not df.empty:
    # Format date column
    df["detected_on"] = pd.to_datetime(df["detected_on"])

    # Highlight unresolved rows
    def highlight_unresolved(row):
        return ['background-color: #ffe6e6' if row['remediation_status'] != 'resolved' else '' for _ in row]

    styled_df = df.style.apply(highlight_unresolved, axis=1)
    st.dataframe(styled_df, use_container_width=True)
else:
    st.warning("No vulnerability data available.")
