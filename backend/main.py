from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
import psycopg2.errors
import os

app = FastAPI(title="Notes API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")

class Note(BaseModel):
    title: str
    content: str

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST
    )

@app.on_event("startup")
def startup():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL
                )
            ''')
            # Safely try to add title column if it doesn't exist
            try:
                cur.execute("ALTER TABLE notes ADD COLUMN title TEXT DEFAULT 'Untitled'")
            except psycopg2.errors.DuplicateColumn:
                pass # Column already exists
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not connect to database on startup. Error: {e}")

@app.get("/notes")
def get_notes(search: Optional[str] = None):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            if search:
                # search in both title and content
                cur.execute("SELECT id, title, content FROM notes WHERE content ILIKE %s OR title ILIKE %s ORDER BY id ASC", (f"%{search}%", f"%{search}%"))
            else:
                cur.execute("SELECT id, title, content FROM notes ORDER BY id ASC")
            notes = cur.fetchall()
        conn.close()
        
        formatted_notes = [{"id": note[0], "title": note[1] if note[1] else "Untitled", "content": note[2].strip()} for note in notes if note[2].strip()]
        return {"notes": formatted_notes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.post("/notes")
def add_note(note: Note):
    if not note.content.strip():
        raise HTTPException(status_code=400, detail="Note content cannot be empty")
        
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id", (note.title.strip() or 'Untitled', note.content.strip()))
            new_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return {"message": "Note added successfully", "note": {"id": new_id, "title": note.title.strip() or 'Untitled', "content": note.content.strip()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    if not note.content.strip():
        raise HTTPException(status_code=400, detail="Note content cannot be empty")
        
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s RETURNING id", (note.title.strip() or 'Untitled', note.content.strip(), note_id))
            updated = cur.fetchone()
            if not updated:
                conn.close()
                raise HTTPException(status_code=404, detail="Note not found")
        conn.commit()
        conn.close()
        return {"message": "Note updated successfully", "note": {"id": note_id, "title": note.title.strip() or 'Untitled', "content": note.content.strip()}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (note_id,))
            deleted = cur.fetchone()
            if not deleted:
                conn.close()
                raise HTTPException(status_code=404, detail="Note not found")
        conn.commit()
        conn.close()
        return {"message": "Note deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
