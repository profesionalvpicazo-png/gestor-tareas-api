---
name: testing-gestor-tareas-api
description: Test the gestor-tareas-api FastAPI application end-to-end. Use when verifying task CRUD or filter endpoints.
---

# Testing gestor-tareas-api

## Prerequisites
- Python 3.12+ with dependencies installed (`pip install -r requirements.txt`)
- No external services needed (uses SQLite locally)

## Starting the Server
```bash
cd /home/ubuntu/repos/gestor-tareas-api
# Remove old DB for clean state (optional)
rm -f tareas.db
uvicorn aplicacion.principal:app --host 0.0.0.0 --port 8000 &
```

The server will be available at `http://localhost:8000`. Swagger docs at `/docs`.

## Running Unit Tests
```bash
python -m pytest tests/ -v
```

## Creating Test Data
```bash
# Create a pending task
curl -s -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" \
  -d '{"title": "Test task", "status": "pending"}'

# Create an in_progress task
curl -s -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" \
  -d '{"title": "In progress task", "status": "in_progress"}'

# Create a done task
curl -s -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" \
  -d '{"title": "Done task", "status": "done"}'
```

## Key Endpoints
- `GET /tasks/` — List all tasks
- `GET /tasks/{id}` — Get task by ID
- `GET /tasks/status/{status}` — Filter tasks by status (pending, in_progress, done)
- `POST /tasks/` — Create a task
- `PATCH /tasks/{id}` — Update a task (blocked if status is done)
- `DELETE /tasks/{id}` — Delete a task

## Testing Tips
- The `TaskStatus` enum values are: `pending`, `in_progress`, `done`
- Invalid enum values in path params return 422 automatically (FastAPI validation)
- Tasks with status `done` cannot be updated (returns 400)
- The SQLite DB file (`tareas.db`) is created at the repo root; delete it for a clean slate
- No authentication is required
- This is a shell-only test (no browser GUI needed) — use curl or httpx, no recording necessary

## Devin Secrets Needed
None — this API requires no authentication or external credentials.
