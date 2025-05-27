import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from app.CRUD.user import UserCRUD
from app.schemas.user import User

@pytest.mark.asyncio
async def test_get_user_by_email(monkeypatch, async_session):
    crud = UserCRUD(session=async_session)

    mock_user_orm = MagicMock()
    class MockUser:
        id = 1
        email = "test@example.com"
        username = "testuser"
        password_hash = "hash"
        created_at = "2025-01-01T00:00:00"
        devices = []

    mock_user = MockUser()

    class MockResult:
        def scalars(self):
            class MockScalars:
                def one(self):
                    return mock_user_orm
            return MockScalars()

    async def mock_execute(query):
        return MockResult()

    monkeypatch.setattr(crud.session, "execute", mock_execute)
    monkeypatch.setattr(crud.schema, "model_validate", lambda self, from_attributes: mock_user)

    user = await crud.get_user_by_email("test@example.com")
    # Since mock_user is a plain object, not an instance of crud.schema, check attributes instead
    assert hasattr(user, "email")
    assert user.email == "test@example.com"
