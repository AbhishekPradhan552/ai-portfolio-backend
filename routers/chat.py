from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from database import get_db
from models import ChatSession, ChatMessage
from schemas import (
    CreateSessionResponse,
    SendMessageRequest,
    MessageResponse
)
from services.openrouter_service import ask_ai, AIServiceError
from context.resume_context import RESUME_CONTEXT

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/session", response_model=CreateSessionResponse)
async def create_session(db: AsyncSession = Depends(get_db)):
    session = ChatSession()
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


@router.get("/session/{session_id}", response_model=list[MessageResponse])
async def get_messages(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )

    messages = result.scalars().all()
    return messages


@router.post("/message", response_model=MessageResponse)
async def send_message(
    request: SendMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    # 1️⃣ Validate session exists
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == request.session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # 2️⃣ Save user message
    user_message = ChatMessage(
        session_id=request.session_id,
        role="user",
        content=request.content
    )

    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)

    # 3️⃣ Fetch full conversation history
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == request.session_id)
        .order_by(ChatMessage.created_at)
    )
    history = result.scalars().all()

    # 4️⃣ Build LLM message structure
    messages = [
        {
            "role": "system",
            "content": f"""
You are an AI assistant for Abhishek Pradhan's portfolio website.

Answer ONLY using the resume information below.

If a question is not directly answerable from the resume, respond with:
"Not mentioned in resume."

Resume:
{RESUME_CONTEXT}
"""
        }
    ]

    for msg in history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # 5️⃣ Call OpenRouter (Fully Async)
    try:
        ai_reply = await ask_ai(messages)
    except AIServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 6️⃣ Save assistant reply
    assistant_message = ChatMessage(
        session_id=request.session_id,
        role="assistant",
        content=ai_reply
    )

    db.add(assistant_message)
    await db.commit()
    await db.refresh(assistant_message)

    return assistant_message
