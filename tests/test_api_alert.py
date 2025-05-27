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
async def test_get_alerts(monkeypatch):
    sample_alerts = [{"id": 1, "message": "Alert1"}]
    async def mock_get_alerts(self, sensor_id):
        return sample_alerts

    monkeypatch.setattr("app.services.alert.AlertService.get_alerts", mock_get_alerts)

    response = client.get("/alert?sensor_id=1")
    assert response.status_code == 200
    assert response.json() == sample_alerts

@pytest.mark.asyncio
async def test_add_alert(monkeypatch):
    sample_alert = {
        "id": 1,
        "sensor_id": 1,
        "alert_type": "type1",
        "description": "desc",
        "created_at": "2025-01-01T00:00:00"
    }
    async def mock_add_alert(self, alert_data):
        return sample_alert

    monkeypatch.setattr("app.services.alert.AlertService.add_alert", mock_add_alert)

    response = client.post("/alert", json={
        "sensor_id": 1,
        "alert_type": "type1",
        "description": "desc"
    })
    assert response.status_code == 200
    assert response.json() == sample_alert
