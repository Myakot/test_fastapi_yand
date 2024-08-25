import os
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import psycopg2
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Depends, HTTPException
from auth import get_current_user, generate_token, User
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


class Note(BaseModel):
    title: str
    content: str


@app.get("/notes")
async def get_notes_route():
    notes = get_notes()
    return notes


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User(username=form_data.username, email="")
    return generate_token(user)


@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


@app.post("/notes")
async def create_note_route(note: Note):
    create_note_in_db(note)
    return {"message": "Заметка добавлена"}


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


@app.on_event("startup")
async def startup_event():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.get("/notes")
async def get_notes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM notes;")
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return JSONResponse(content=notes, media_type="application/json")


@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: Note):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "UPDATE notes SET title = %s, content = %s WHERE id = %s",
        (note.title, note.content, note_id),
    )
    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(
        content={"message": "Note updated successfully"},
        media_type="application/json",
    )


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    if cur.rowcount == 0:
        return JSONResponse(
            content={"error": "Note not found"},
            status_code=404,
            media_type="application/json",
        )
    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(
        content={"message": "Note deleted successfully"},
        media_type="application/json",
    )


@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
    note = cur.fetchone()
    cur.close()
    conn.close()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return JSONResponse(
        content=jsonable_encoder(note), media_type="application/json"
    )


def get_all_notes():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM notes")
            return cur.fetchall()


def create_note_in_db(note: Note):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s)",
        (note.title, note.content),
    )
    conn.commit()
    cur.close()
    conn.close()
