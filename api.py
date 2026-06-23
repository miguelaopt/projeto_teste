from fastapi import FastAPI

app = FastAPI(title="Task Manager API")

tasks = [
    {"id": 1, "title": "Setup database", "done": False},
    {"id": 2, "title": "Create login", "done": False}
]

@app.get("/")
def read_root():
    return {"status": "API is running smoothly!"}

@app.get("/tasks")
def get_tasks():
    return {"data": tasks}