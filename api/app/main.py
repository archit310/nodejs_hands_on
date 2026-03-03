from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.notes import router as notes_router

app = FastAPI(title="Insight Inbox API", version="0.1.0")

# CORS for Next.js dev + Vercel later
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # later we’ll switch to env-based
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(notes_router, prefix="/notes", tags=["notes"])