import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.core.utils.load_llm import LLMLoader
from app.api.models import ReportRequest, SessionResponse, ChatRequest, ChatResponse
from app.core.utils.load_data import load_data, Table
from app.core.utils.preprocess_data import preprocess_tables
from app.core.workflow import build_report_workflow
from app.core.state import ReportState

# Load environment variables
load_dotenv()

app = FastAPI(title="Agentic AI Data Analyst API")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory Session Storage ---
SESSIONS: dict[str, dict] = {}


@app.post("/session", response_model=SessionResponse)
async def create_session(data_file: UploadFile = File(...), schema_file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    session_path = f"app/data_storage/{session_id}"
    os.makedirs(session_path, exist_ok=True)

    data_path = os.path.join(session_path, "df")
    schema_path = os.path.join(session_path, "schema")
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(schema_path, exist_ok=True)

    try:
        data_filepath = os.path.join(data_path, data_file.filename or "data.csv")
        with open(data_filepath, "wb") as buffer:
            shutil.copyfileobj(data_file.file, buffer)

        schema_filepath = os.path.join(schema_path, schema_file.filename or "schema.csv")
        with open(schema_filepath, "wb") as buffer:
            shutil.copyfileobj(schema_file.file, buffer)

        input_files = [(data_file.filename or "data.csv").replace(".csv", "")]
        schema_files = [(schema_file.filename or "schema.csv").replace(".csv", "")]
        
        tables = load_data(input_files, schema_files, data_path, schema_path)
        processed_tables = preprocess_tables(tables)
        
        SESSIONS[session_id] = {
            "processed_tables": processed_tables,
            "session_path": session_path,
            "report_path": None,
            "plots_path": os.path.join(session_path, "plots")
        }
        os.makedirs(SESSIONS[session_id]["plots_path"], exist_ok=True)

    except Exception as e:
        shutil.rmtree(session_path)
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

    return SessionResponse(session_id=session_id, message="Session created successfully.")


@app.post("/report", response_model=ReportRequest)
async def generate_report(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        session_data = SESSIONS[session_id]
        
        loader = LLMLoader(google_api_key=os.getenv("GOOGLE_API_KEY"))
        llm = loader.load_google_model_flash(temperature=0)

        input_context = {
            "llm_model": llm,
            "processed_tables": session_data["processed_tables"],
            "plots_path": session_data["plots_path"],
            "pdf_path": None, # Will be populated by the workflow
        }
        
        # State
        state = ReportState(input_context)
        state = state.to_dict()
        
        
        try:
            # Build the workflow
            graph = build_report_workflow(state)
        except Exception as e:
            print(f"Error building workflow: {e}")  
            raise HTTPException(status_code=500, detail=f"Failed to build workflowt: {str(e)}")

        
        try:
            # Run the workflow
            final_state = graph.invoke(state)
        except Exception as e:
            print(f"Error running workflow: {e}")
            raise HTTPException(status_code=500, detail=f"Failed at Graph invoke: {str(e)}")
        
        # The final PDF path is returned by the workflow
        final_report_path = final_state.get('pdf_path')
        if not final_report_path or not os.path.exists(final_report_path):
            raise HTTPException(status_code=500, detail="Report generation failed to produce a file.")

        SESSIONS[session_id]["report_path"] = final_report_path

        return ReportRequest(
            session_id=session_id,
            message="Report generated successfully.",
            report_path=f"/report/download/{session_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@app.get("/report/download/{session_id}")
async def download_report(session_id: str):
    if session_id not in SESSIONS or not SESSIONS[session_id].get("report_path"):
        raise HTTPException(status_code=404, detail="Report not found.")
    
    report_path = SESSIONS[session_id]["report_path"]
    return FileResponse(path=report_path, media_type='application/pdf', filename="financial_analysis_report.pdf")


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    if request.session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    # For now, we'll just echo the message back.
    # Later, you can add your chat logic here.
    response_message = f"Received your message: '{request.message}'"
    
    return ChatResponse(response=response_message)