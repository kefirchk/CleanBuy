import asyncio
import json
import os
from pathlib import Path
from typing import AsyncGenerator

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

import pytest

from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.main import app
from src.models.base import Base

load_dotenv()

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

# DATABASE
DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

engine_test = create_async_engine(url=DATABASE_URL_TEST, echo=False, poolclass=NullPool)
new_session_test = async_sessionmaker(engine_test, expire_on_commit=False)


@pytest.fixture(autouse=True)
def override_new_session(mocker):
    mocker.patch('src.database.new_session', new_session_test)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


client = TestClient(app)


# FIXTURES
def get_test_data(filename):
    data_path = Path(__file__).parent / 'test_data' / filename
    with open(data_path) as f:
        return json.load(f)


@pytest.fixture
def user_read_data():
    return get_test_data("user_read.json")


@pytest.fixture
def user_create_data():
    return get_test_data("user_create.json")


@pytest.fixture
def user_update_data():
    return get_test_data("user_update.json")


@pytest.fixture
def user_orm_data():
    return get_test_data("user_orm.json")


@pytest.fixture
def buyer_create_data():
    return get_test_data("buyer_create.json")
