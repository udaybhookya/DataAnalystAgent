# Data Analyst Agent

Agentic AI Data Analyst (Scalable Architecture)This project has been restructured to support a scalable web application architecture using FastAPI for the backend and Streamlit for the frontend. This modular approach allows for independent development, scaling, and the easy addition of new features like interactive chat.📂 Project Structure.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI application: endpoints, routing
│   │   └── models.py           # Pydantic models for data validation
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agents/             # All agent node functions (your original agents)
│   │   ├── state.py            # Definition of the application state
│   │   ├── utils/              # Utility functions (LLM loading, data loading)
│   │   └── workflows.py        # LangGraph workflow definitions
│   │
│   ├── frontend/
│   │   ├── __init__.py
│   │   └── app.py              # The Streamlit user interface code
│   │
│   └── data_storage/           # For temporary session data, reports, plots
│       └── .gitkeep
│
├── prompts/                    # All prompt templates
│
├── .gitignore
├── Dockerfile                  # To containerize the FastAPI backend
├── requirements.txt            # All project dependencies
└── run.sh                      # Helper script to launch the app
🚀 How to Run the ApplicationThis application now runs as two separate services: the backend API and the frontend UI.1. Install Dependencies:pip install -r requirements.txt
2. Configure Environment Variables:Create a .env file in the root directory and add your API key:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
3. Run the Application:Use the provided shell script to launch both the backend and frontend servers concurrently.bash run.sh
This will:Start the FastAPI backend on http://122.0.0.1:8000Start the Streamlit frontend on http://localhost:8501Open your browser and navigate to http://localhost:8501 to use the application.🐳 Docker (For Backend Deployment)A Dockerfile is included to containerize the FastAPI backend for easy deployment.Build the Docker image:docker build -t ai-data-analyst-api .
Run the container:docker run -p 8000:8000 --env-file .env ai-data-analyst-api
