from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers.chat import router as chat_router

app = FastAPI(
    title="AI Portfolio Backend",
    version="1.0.0"
)

# CORS (for frontend connection later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-portfolio-frontend-three.vercel.app"
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat routes
app.include_router(chat_router)


# Create tables on startup (Async Safe)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Optional health check (good for deployment platforms)
@app.get("/")
async def root():
    return {"status": "AI Portfolio Backend Running"}