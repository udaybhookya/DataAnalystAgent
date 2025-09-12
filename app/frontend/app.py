import streamlit as st
import requests
import os
import time

st.title("Agentic AI Data Analyst")

# --- API Base URL ---
API_URL = "http://127.0.0.1:8000"

# --- Session State Initialization ---
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'report_path' not in st.session_state:
    st.session_state.report_path = None
if 'report_ready' not in st.session_state:
    st.session_state.report_ready = False

# --- Sidebar for Data Upload ---
with st.sidebar:
    st.header("1. Start New Session")
    data_file = st.file_uploader("Upload CSV Data File", type="csv")
    schema_file = st.file_uploader("Upload Schema File", type="csv")

    if st.button("Start Session"):
        if data_file and schema_file:
            with st.spinner("Creating session and processing data..."):
                files = {
                    "data_file": (data_file.name, data_file, "text/csv"),
                    "schema_file": (schema_file.name, schema_file, "text/csv")
                }
                try:
                    response = requests.post(f"{API_URL}/session", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.session_id = data.get("session_id")
                        st.session_state.report_ready = False
                        st.session_state.report_path = None
                        st.success(f"Session created: {st.session_state.session_id}")
                    else:
                        st.error(f"Error creating session: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Could not connect to the backend. Is it running?")
        else:
            st.warning("Please upload both data and schema files.")

# --- Main Area for Report Generation ---
st.header("2. Generate Analysis Report")

if st.session_state.session_id:
    st.info(f"Current Session ID: {st.session_state.session_id}")
    
    if st.button("Generate Report"):
        with st.spinner("Agent is analyzing and generating the report... This may take a moment."):
            try:
                # MODIFICATION: Sending session_id as a parameter in the POST request body/params
                # FastAPI reads it from the path, but we send it in the URL for clarity.
                response = requests.post(f"{API_URL}/report?session_id={st.session_state.session_id}")

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.report_path = data.get("report_path")
                    st.session_state.report_ready = True
                    st.success("Report generated successfully!")
                else:
                    st.error(f"Error generating report: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the backend.")

    if st.session_state.report_ready and st.session_state.report_path:
        st.markdown("### 3. Download Your Report")
        
        # To create a download button, we need the actual file.
        # We'll make a GET request to the download endpoint and provide the content.
        try:
            report_url = f"{API_URL}{st.session_state.report_path}"
            report_response = requests.get(report_url)
            if report_response.status_code == 200:
                st.download_button(
                    label="Download PDF Report",
                    data=report_response.content,
                    file_name="financial_analysis_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Could not fetch the report for download.")
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Could not fetch the report.")

else:
    st.warning("Please start a session in the sidebar to generate a report.")

