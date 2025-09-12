# Data Analyst AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 🚀 Data Analyst AI Agent

A scalable, modular **AI Data Analyst Agent** that autonomously ingests, explores, analyzes, and reports on tabular datasets.  
Built with **FastAPI**, **Streamlit**, **LangGraph**, and **modern LLMs** — designed for independent scaling and easy feature extension (e.g., interactive chat).

---
## 📝 Overview

This project re-structures the Agentic AI Data Analyst into a **scalable web application** with independent backend and frontend services.

* **Backend (FastAPI):** Provides APIs, LangGraph workflows, and state management.
* **Frontend (Streamlit):** Delivers an interactive UI for chat-based data exploration and visualization.
* **Agents & Workflows:** Encapsulated agent nodes orchestrated via LangGraph.
* **Scalable Design:** Modular, containerized backend with Docker for easy deployment.

---

## 🤖 Agentic Workflow

The LangGraph-based workflow coordinates specialized agents:

`START` → `data_understanding` → `analytics_planning` → `code_execution` → `content_planning` → `report_generation` → `END`

---

## 🚀 Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/udaybhookya/DataAnalystAgent.git
   cd DataAnalystAgent
   ```
   
2. **Create & activate a virtual environment**

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```

3. Install dependencies
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Configure environment variables
    ```bash
    Create a .env file in the root directory and add your API key:
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

5. Run the application
    ```bash
    bash run.sh
    ```
    - Backend: http://127.0.0.1:8000
    - Frontend: http://localhost:850
    - Open your browser at http://localhost:8501 🎉

## 📂 Project Structure
```
.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI application: endpoints, routing
│   │   └── models.py           # Pydantic models for validation
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agents/             # Agent node functions
│   │   ├── state.py            # Application state definition
│   │   ├── utils/              # Utility functions (LLM, data loading)
│   │   └── workflows.py        # LangGraph workflow definitions
│   │
│   ├── frontend/
│   │   ├── __init__.py
│   │   └── app.py              # Streamlit UI code
│   │
│   └── data_storage/           # Temp session data, reports, plots
│       └── .gitkeep
│
├── prompts/                    # Prompt templates
├── .gitignore
├── Dockerfile                  # FastAPI backend containerization
├── requirements.txt            # Project dependencies
└── run.sh                      # Launch script
```
## 🤝 Contributing

1.  Fork the repository
2.  Create a feature branch: `git checkout -b feature/my-new-feature`
3.  Commit your changes: `git commit -m "Add my new feature"`
4.  Push to your branch: `git push origin feature/my-new-feature`
5.  Open a Pull Request and describe your changes.

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.