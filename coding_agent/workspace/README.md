# FastAPI Todo App

A simple FastAPI application with in-memory todo storage (now using SQLite) that provides CRUD operations and a toggle feature for marking todos as completed. Includes a frontend HTML page that interacts with the API.

## Features

- Create, list, update, and delete todos
- Mark todos as completed (toggle feature)
- In-memory storage (SQLite database for persistence)
- Interactive HTML frontend at `/` (served from `static/index.html`)
- Comprehensive test suite with 12 passing tests

## Features

- **`POST /todos/`** - Create a new todo
- **`GET /todos/`** - List all todos
- **`PUT /todos/{todo_id}`** - Update a todo
- **`POST /todos/{todo_id}/toggle`** - Toggle completed status
- **`DELETE /todos/{todo_id}`** - Delete a todo
- **`GET /`** - Serves the interactive HTML frontend

## Requirements

- Python 3.13+
- `fastapi`
- `uvicorn`
- `pytest`
- `pydantic`

## Installation

```bash
# Clone the repository
git clone <repository-url>

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app:app --reload
```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:8001/`
2. Use the frontend to:
   - Add new todos
   - Toggle todos as completed
   - Delete todos
3. API endpoints are available at `/docs` for interactive testing

## Running Tests

```bash
pytest test_app.py -v
```

## Project Structure

```
.
├── app.py              # FastAPI application
├── static/
│   └── index.html    # Frontend HTML/JS
├── test_app.py         # Test suite
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

## License

MIT License