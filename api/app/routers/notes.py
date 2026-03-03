from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()

class NoteCreate(BaseModel):
    title: str
    content: str

@router.post("")
def create_note(payload: NoteCreate):
    # for now: mock response (DB later)
    return {
        "id": str(uuid4()),
        "title": payload.title,
        "content": payload.content,
    }

@router.get("")
def list_notes():
    # for now: mock response
    return {"items": [], "next_cursor": None}