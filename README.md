# AI Portfolio – Backend API

FastAPI backend powering the AI-powered interactive portfolio.

Handles chat sessions, message persistence, and AI response generation using PostgreSQL and async database operations.

---

## 🚀 Live API

https://your-render-backend-url.onrender.com

Health Check: GET /health

---

## 🧠 Project Overview

This backend provides:

- Chat session creation
- Persistent message storage
- Async database handling
- Production-ready CORS configuration
- Clean route separation
- PostgreSQL integration via Neon

---

## 🛠 Tech Stack

- FastAPI
- SQLAlchemy 2.0 (Async)
- PostgreSQL (Neon)
- Psycopg3
- Uvicorn
- Python 3.11+

---

## 📂 Project Structure

backend/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│ └── chat.py
├── requirements.txt
└── runtime.txt

---

## 🔄 API Endpoints

### Create Session

POST /chat/session

Creates a new chat session and returns a UUID.

---

### Get Session Messages

GET /chat/session/{session_id}

Returns all messages for a session.

---

### Send Message

POST /chat/message

Request body:

```json
{
  "session_id": "uuid",
  "content": "Hello"
}
```

## Database:

•Hosted on Neon (Serverless PostgreSQL)
•Async SQLAlchemy engine
•UUID-based session management
•Timestamped message persistence

## CORS Configuration

Configured to allow:

Local development:
http://localhost:5173

All Vercel deployments:
allow_origin_regex="https://.\*\.vercel\.app"

## Environment variables

Create .env file:
DATABASE_URL=your_neon_postgres_connection_string

## Local development

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Runs at: http://localhost:8000

## Deployment

•Hosted on Render
•Auto-deploy on push
•Connected to Neon PostgreSQL

## Engineering Highlights

•Async database session management
•Production-grade CORS handling
•Clean router architecture
•Schema validation with Pydantic
•Session recovery handling from frontend
•Full-stack integration ready
