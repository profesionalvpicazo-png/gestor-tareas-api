import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aplicacion.base_de_datos import Base, get_db
from aplicacion.principal import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def _create_task(title="Test task", status="pending"):
    return client.post("/tasks/", json={"title": title, "status": status})


def test_update_pending_task_succeeds():
    task = _create_task().json()
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated"


def test_update_done_task_returns_400():
    task = _create_task(status="done").json()
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Nope"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Cannot update a completed task"


def test_update_in_progress_task_succeeds():
    task = _create_task(status="in_progress").json()
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Still going"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Still going"


def test_transition_to_done_allowed_from_pending():
    task = _create_task(status="pending").json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"


def test_done_task_cannot_change_status():
    task = _create_task(status="done").json()
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "pending"})
    assert resp.status_code == 400
