from pydantic import BaseModel
from typing import Optional

class SessionResponse(BaseModel):
    session_id: str
    message: str

class ReportRequest(BaseModel):
    session_id: str
    message: str
    report_path: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str