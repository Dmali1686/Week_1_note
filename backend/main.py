from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="Notes API")

# Setup CORS to allow our frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, this should be specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOTES_FILE = "notes.txt"

class Note(BaseModel):
    content: str

@app.get("/notes")
def get_notes():
    if not os.path.exists(NOTES_FILE):
        return {"notes": []}
    
    with open(NOTES_FILE, "r") as f:
        notes = f.readlines()
        
    # Strip newlines and empty strings
    cleaned_notes = [note.strip() for note in notes if note.strip()]
    return {"notes": cleaned_notes}

@app.post("/notes")
def add_note(note: Note):
    if not note.content.strip():
        raise HTTPException(status_code=400, detail="Note cannot be empty")
        
    with open(NOTES_FILE, "a") as f:
        f.write(note.content.strip() + "\n")
        
    return {"message": "Note added successfully", "note": note.content.strip()}
