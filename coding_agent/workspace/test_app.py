import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_create_todo():
    # Use unique titles to avoid conflicts with other tests
    response = client.post("/todos/", json={"title": "Buy milk", "description": "2% please"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy milk"
    assert data["description"] == "2% please"


def test_list_todos():
    # Clear existing todos first by getting current count
    existing = client.get("/todos/").json()
    initial_count = len(existing)

    response = client.post("/todos/", json={"title": "Task 1"})
    assert response.status_code == 200

    response = client.post("/todos/", json={"title": "Task 2"})
    assert response.status_code == 200

    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == initial_count + 2
    assert any(t["title"] == "Task 1" for t in data)
    assert any(t["title"] == "Task 2" for t in data)


def test_update_todo():
    create = client.post("/todos/", json={"title": "Original", "description": "Old"})
    todo_id = create.json()["id"]

    response = client.put(f"/todos/{todo_id}", json={"title": "Updated", "description": "New"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["description"] == "New"


def test_update_todo_not_found():
    response = client.put("/todos/999", json={"title": "Ghost"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_delete_todo():
    create = client.post("/todos/", json={"title": "To delete"})
    todo_id = create.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted"

    # Verify it's gone
    response = client.get("/todos/")
    assert all(t["id"] != todo_id for t in response.json())


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_create_todo_defaults_to_not_completed():
    response = client.post("/todos/", json={"title": "Not done yet"})
    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_create_todo_with_completed_true():
    response = client.post(
        "/todos/", json={"title": "Already done", "completed": True}
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_toggle_completed_on_and_off():
    create = client.post("/todos/", json={"title": "Toggle me"})
    todo_id = create.json()["id"]
    assert create.json()["completed"] is False

    # Toggle on
    response = client.post(f"/todos/{todo_id}/toggle")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["completed"] is True

    # Toggle back off
    response = client.post(f"/todos/{todo_id}/toggle")
    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_toggle_persists_across_requests():
    create = client.post("/todos/", json={"title": "Persist toggle"})
    todo_id = create.json()["id"]

    client.post(f"/todos/{todo_id}/toggle")

    # Re-list and confirm the change was stored
    listed = client.get("/todos/").json()
    todo = next(t for t in listed if t["id"] == todo_id)
    assert todo["completed"] is True


def test_toggle_todo_not_found():
    response = client.post("/todos/999/toggle")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"