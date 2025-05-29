from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import os
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Prometheus 메트릭스 엔드포인트 (/metrics)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# To-Do 항목 모델
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    priority: str = "medium"    # ← 기본 우선순위 추가

# JSON 파일 경로
TODO_FILE = "todo.json"

def load_todos():
    todos = []
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            todos = json.load(file)

    # 기존에 priority가 없던 항목이 있으면 기본값 채워주기
    for t in todos:
        if "priority" not in t:
            t["priority"] = "medium"
    return todos

def save_todos(todos):
    with open(TODO_FILE, "w") as file:
        json.dump(todos, file, indent=4)

@app.get("/todos", response_model=list[TodoItem])
def get_todos():
    return load_todos()

@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todos = load_todos()
    todos.append(todo.dict())
    save_todos(todos)
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    todos = load_todos()
    for idx, t in enumerate(todos):
        if t["id"] == todo_id:
            todos[idx] = updated_todo.dict()   # priority 포함 전체 덮어쓰기
            save_todos(todos)
            return updated_todo
    raise HTTPException(status_code=404, detail="To-Do item not found")

@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todos = [t for t in load_todos() if t["id"] != todo_id]
    save_todos(todos)
    return {"message": "To-Do item deleted"}

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("templates/index.html", "r") as file:
        return HTMLResponse(file.read())

@app.get("/health")
def health_check():
    return {"status": "ok"}
