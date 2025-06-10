import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from core.database.models.base import Base
from core.database.db_helper import db_helper

# Override target for dependency
get_db = db_helper.scoped_session_dependency

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def session(engine):
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with AsyncSessionLocal() as sess:
        yield sess

@pytest.fixture
async def async_client(session):
    # Override the get_db dependency to use our test session
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    # Use ASGITransport to test FastAPI app without running a server
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.anyio
async def test_register_and_login(async_client):
    # Test user registration
    register_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "phone_number": "1234567890",
        "password": "strongpassword",
    }
    response = await async_client.post("/auth/register", json=register_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["first_name"] == "Alice"
    assert data["phone_number"] == "1234567890"

    # Test duplicate registration
    dup_resp = await async_client.post("/auth/register", json=register_data)
    assert dup_resp.status_code == 400

    # Test login with correct credentials
    login_data = {"username": "1234567890", "password": "strongpassword"}
    login_resp = await async_client.post("/auth/login", data=login_data)
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Test login with incorrect password
    bad_login = {"username": "1234567890", "password": "wrong"}
    bad_resp = await async_client.post("/auth/login", data=bad_login)
    assert bad_resp.status_code == 401
