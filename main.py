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
from pyaspeller import YandexSpeller

load_dotenv()
app = FastAPI()
speller = YandexSpeller()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

class Note(BaseModel):
    title: str
    content: str

@app.get("/notes", response_model=list[Note])
async def get_notes_route(current_user: User = Depends(get_current_user)):
    notes = await get_notes(current_user.username)
    return JSONResponse(content=jsonable_encoder(notes), media_type="application/json")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User(username=form_data.username, email="")
    return generate_token(user)

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": f"Hello, {current_user.username}!"}, media_type="application/json")

@app.post("/notes")
async def create_note_route(note: Note, current_user: User = Depends(get_current_user)):
    errors = list(speller.spell(note.content))
    print(f"Spell check errors: {errors}")
    if errors:
        return {"message": "Spelling errors found", "errors": errors}, 400
    create_note_in_db(note, current_user.username)
    return {"message": "Note added"}, 200

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.on_event("startup")
async def startup_event():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            username VARCHAR(255)
        );
    """)
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.columns 
                WHERE table_name='notes' AND column_name='username'
            ) THEN
                ALTER TABLE notes ADD COLUMN username VARCHAR(255);
            END IF;
        END $$;
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.get("/notes")
async def get_notes(username: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM notes WHERE username = %s", (username,))
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return JSONResponse(content=jsonable_encoder(notes), media_type="application/json")

@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: Note, current_user: User = Depends(get_current_user)):
    # Spell check
    errors = list(speller.spell(note.content))  # Convert generator to list
    if errors:
        return {"message": "Spelling errors found", "errors": errors}, 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "UPDATE notes SET title = %s, content = %s WHERE id = %s AND username = %s",
        (note.title, note.content, note_id, current_user.username)
    )
    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(content={"message": "Note updated successfully"}, media_type="application/json")

@app.delete("/notes/")
def delete_all_notes(current_user: User = Depends(get_current_user)):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("DELETE FROM notes WHERE username = %s", (current_user.username,))
        conn.commit()
    return {"message": "All notes deleted"}, 200

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, current_user: User = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM notes WHERE id = %s AND username = %s", (note_id, current_user.username))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(content={"message": "Note deleted successfully"}, media_type="application/json")

@app.get("/notes/{note_id}")
async def get_note(note_id: int, current_user: User = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM notes WHERE id = %s AND username = %s", (note_id, current_user.username))
    note = cur.fetchone()
    cur.close()
    conn.close()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return JSONResponse(content=jsonable_encoder(note), media_type="application/json")

def get_all_notes(username: str):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM notes WHERE username = %s", (username,))
            return cur.fetchall()

def create_note_in_db(note: Note, username: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO notes (title, content, username) VALUES (%s, %s, %s)",
        (note.title, note.content, username)
    )
    conn.commit()
    cur.close()
    conn.close()
