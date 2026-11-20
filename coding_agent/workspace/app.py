import sqlite3
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

DB_PATH = "todos.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        DROP TABLE IF EXISTS todos;
        CREATE TABLE todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    conn.commit()
    conn.close()


# Initialize the database when the module loads
init_db()


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Todo(TodoCreate):
    id: int


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.post("/todos/", response_model=Todo)
def create_todo(payload: TodoCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (payload.title, payload.description, 1 if payload.completed else 0),
    )
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    return {
        "id": todo_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
    }


@app.get("/todos/", response_model=List[Todo])
def list_todos():
    conn = get_db()
    rows = conn.execute("SELECT id, title, description, completed FROM todos").fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "completed": bool(row["completed"]),
        }
        for row in rows
    ]


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoCreate):
    conn = get_db()
    cursor = conn.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (payload.title, payload.description, 1 if payload.completed else 0, todo_id),
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()
    return {
        "id": todo_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
    }


@app.post("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT id, title, description, completed FROM todos WHERE id = ?",
        (todo_id,),
    ).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    new_completed = not bool(row["completed"])
    conn.execute(
        "UPDATE todos SET completed = ? WHERE id = ?",
        (1 if new_completed else 0, todo_id),
    )
    conn.commit()
    conn.close()
    return {
        "id": todo_id,
        "title": row["title"],
        "description": row["description"],
        "completed": new_completed,
    }


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db()
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()
    return {"message": "Todo deleted"}