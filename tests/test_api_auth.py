import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock

client = TestClient(app)

@pytest_asyncio.fixture(autouse=True)
def override_auth_deps():
    from app.dependencies import get_token, get_user_id
    from app.api.device import UserIDDep
    app.dependency_overrides[get_token] = lambda: "testtoken"
    app.dependency_overrides[get_user_id] = lambda: 1
    app.dependency_overrides[UserIDDep] = lambda: 1
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_register_user(monkeypatch):
    async def mock_register_user(self, user_data):
        return {"id": 1, "email": user_data.email, "username": "testuser", "password_hash": "hash", "created_at": "2025-01-01T00:00:00", "devices": []}

    monkeypatch.setattr("app.services.auth.AuthService.register_user", mock_register_user)

    response = client.post("/auth/register", json={"username": "testuser", "email": "test@example.com", "password": "pass"})
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response.json()["data"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_user(monkeypatch):
    async def mock_login_user(self, user_data, response):
        return "dummy_token"

    monkeypatch.setattr("app.services.auth.AuthService.login_user", mock_login_user)

    response = client.post("/auth/login", json={"email": "test@example.com", "password": "pass"})
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response.json()["data"] == "dummy_token"
