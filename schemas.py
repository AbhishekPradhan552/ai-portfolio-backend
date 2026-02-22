from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CreateSessionResponse(BaseModel):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class SendMessageRequest(BaseModel):
    session_id: UUID
    content: str

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True