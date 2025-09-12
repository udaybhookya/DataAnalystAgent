#!/bin/bash

# This script starts both the FastAPI backend and the Streamlit frontend.

echo "Starting FastAPI backend server on http://127.0.0.1:8000 ..."
uvicorn app.api.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "FastAPI backend running with PID: $BACKEND_PID"
echo "------------------------------------------------"
sleep 5 # Give the backend a moment to start up

echo "Starting Streamlit frontend on http://localhost:8501 ..."
# MODIFICATION: Added --server.address=0.0.0.0 to make it accessible
streamlit run app/frontend/app.py --server.address=0.0.0.0 &
FRONTEND_PID=$!

echo "Streamlit frontend running with PID: $FRONTEND_PID"
echo "------------------------------------------------"
echo "Application is running."
echo "Access the UI at http://localhost:8501"

# A simple trap to clean up the background processes when the script is exited
trap "echo 'Stopping servers...'; kill $BACKEND_PID; kill $FRONTEND_PID;" SIGINT SIGTERM
wait

