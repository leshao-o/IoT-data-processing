import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.CRUD.device import DeviceCRUD
from unittest.mock import AsyncMock
from app.api.device import UserIDDep
from app.dependencies import get_token, get_user_id

client = TestClient(app)

@pytest_asyncio.fixture(autouse=True)
def override_auth_deps():
    app.dependency_overrides[get_token] = lambda: "testtoken"
    app.dependency_overrides[get_user_id] = lambda: 1
    app.dependency_overrides[UserIDDep] = lambda: 1
    yield
    app.dependency_overrides.pop(get_token, None)
    app.dependency_overrides.pop(get_user_id, None)
    app.dependency_overrides.pop(UserIDDep, None)

@pytest.mark.asyncio
async def test_get_devices(monkeypatch):
    sample_devices = [{"id": 1, "name": "Device1"}]
    async def mock_get_devices(self, user_id):
        return sample_devices

    monkeypatch.setattr("app.services.device.DeviceService.get_devices", mock_get_devices)

    response = client.get("/device")
    assert response.status_code == 200
    assert response.json() == sample_devices

@pytest.mark.asyncio
async def test_add_device(monkeypatch):
    sample_device = {"id": 1, "name": "Device1"}
    async def mock_add_device(self, data, user_id):
        return sample_device

    monkeypatch.setattr("app.services.device.DeviceService.add_device", mock_add_device)

    response = client.post("/device", json={"name": "Device1", "description": "desc"})
    assert response.status_code == 200
    assert response.json() == sample_device

@pytest.mark.asyncio
async def test_devicecrud_get_filtered(monkeypatch, async_session):
    crud = DeviceCRUD(session=async_session)

    class MockResult:
        def scalars(self):
            class MockScalars:
                def all(self):
                    return []
            return MockScalars()

    async def mock_execute(query):
        return MockResult()

    monkeypatch.setattr(crud.session, "execute", mock_execute)

    result = await crud.get_filtered(name="test")
    assert isinstance(result, list)

def test_get_devices_empty(monkeypatch):
    async def mock_get_devices(self, user_id):
        return []

    monkeypatch.setattr("app.services.device.DeviceService.get_devices", mock_get_devices)

    response = client.get("/device")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_devicecrud_get_filtered_nonempty(monkeypatch, async_session):
    class DummyDevice:
        name = "Device1"
        user_id = 1
        description = "desc"
        id = 1
        created_at = "2025-01-01T00:00:00"
        sensors = []
        commands = []

    class MockResult:
        def scalars(self):
            class MockScalars:
                def all(self):
                    return [DummyDevice()]
            return MockScalars()

    async def mock_execute(query):
        return MockResult()

    monkeypatch.setattr(async_session, "execute", mock_execute)

    crud = DeviceCRUD(session=async_session)
    result = await crud.get_filtered(name="test")
    assert isinstance(result, list)
