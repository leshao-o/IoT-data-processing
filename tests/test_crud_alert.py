import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from app.CRUD.alert import AlertCRUD

@pytest.mark.asyncio
async def test_alertcrud_basic(monkeypatch, async_session):
    crud = AlertCRUD(session=async_session)

    class MockAlert:
        id = 1
        sensor_id = 1
        alert_type = "type1"
        description = "desc"
        created_at = "2025-01-01T00:00:00"

    mock_alert = MockAlert()

    class MockResult:
        def scalars(self):
            class MockScalars:
                def all(self):
                    return [mock_alert]
            return MockScalars()

    async def mock_execute(query):
        return MockResult()

    monkeypatch.setattr(crud.session, "execute", mock_execute)
    monkeypatch.setattr(crud.schema, "model_validate", lambda self, from_attributes: mock_alert)

    result = await crud.get_filtered()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].description == "desc"
