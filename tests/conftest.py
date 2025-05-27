import sys
import os
import pytest
import pytest_asyncio

# Добавляем корень проекта в sys.path для корректного импорта app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import settings
from app.database import async_session_maker

@pytest.fixture(scope="session", autouse=True)
def set_test_mode():
    # Устанавливаем режим TEST для тестов
    settings.MODE = "TEST"

@pytest_asyncio.fixture(scope="session")
async def async_session():
    # Асинхронная сессия для работы с тестовой базой
    async with async_session_maker() as session:
        yield session

@pytest_asyncio.fixture(scope="function", autouse=True)
async def session_transaction(async_session):
    # Транзакция для отката изменений после каждого теста
    async with async_session.begin():
        yield
        # rollback будет выполнен автоматически при выходе из блока
