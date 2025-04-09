import requests
import pytest

BASE_URL = "http://54.180.120.187:8000"

@pytest.mark.order(1)
def test_health_check():
    res = requests.get(f"{BASE_URL}/todos")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

@pytest.mark.order(2)
def test_create_todo():
    todo = {
        "id": 1,
        "title": "Test",
        "description": "Test description",
        "completed": False
    }
    res = requests.post(f"{BASE_URL}/todos", json=todo)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert data["title"] == "Test"

@pytest.mark.order(3)
def test_get_todos_with_item():
    res = requests.get(f"{BASE_URL}/todos")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    assert any(todo["id"] == 1 for todo in data)

@pytest.mark.order(4)
def test_update_todo():
    updated = {
        "id": 1,
        "title": "Updated",
        "description": "Updated description",
        "completed": True
    }
    res = requests.put(f"{BASE_URL}/todos/1", json=updated)
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True

@pytest.mark.order(5)
def test_delete_todo():
    res = requests.delete(f"{BASE_URL}/todos/1")
    assert res.status_code == 200
    assert res.json()["message"] == "To-Do item deleted"

@pytest.mark.order(6)
def test_delete_todo_not_found():
    res = requests.delete(f"{BASE_URL}/todos/1")
    assert res.status_code == 200
    assert res.json()["message"] == "To-Do item deleted"
