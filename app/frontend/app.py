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
if 'page' not in st.session_state:
    st.session_state.page = "main"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- Page Navigation ---
def navigate_to(page):
    st.session_state.page = page

# --- Main Page ---
def main_page():
    st.header("2. Generate Analysis Report")

    if st.session_state.session_id:
        st.info(f"Current Session ID: {st.session_state.session_id}")
        
        if st.button("Generate Report"):
            with st.spinner("Agent is analyzing and generating the report... This may take a moment."):
                try:
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

# --- Chat Page ---
def chat_page():
    st.header("Chat with the Agent")

    if not st.session_state.session_id:
        st.warning("Please start a new session in the sidebar to begin chatting.")
        return

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is up?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Agent is thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"session_id": st.session_state.session_id, "message": prompt}
                )
                if response.status_code == 200:
                    data = response.json()
                    agent_response = data.get("response")
                    st.session_state.chat_history.append({"role": "assistant", "content": agent_response})
                    with st.chat_message("assistant"):
                        st.markdown(agent_response)
                else:
                    st.error(f"Error communicating with agent: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the backend.")


# --- Sidebar for Data Upload and Navigation ---
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
                        st.session_state.chat_history = []
                        st.success(f"Session created: {st.session_state.session_id}")
                        navigate_to("main")  # Switch to main page after session creation
                    else:
                        st.error(f"Error creating session: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Could not connect to the backend. Is it running?")
        else:
            st.warning("Please upload both data and schema files.")
    
    st.header("Navigation")
    if st.button("Report Generation"):
        navigate_to("main")
    if st.button("Go to Chat"):
        navigate_to("chat")


# --- Main Area ---
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "chat":
    chat_page()