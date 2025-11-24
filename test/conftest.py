import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.enums import UserRole
from app.models.base import Base
from main import app

TEST_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override FastAPI dependencies
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_current_user():
    return {
        "id": 1,
        "username": "ravinder77",
        "first_name": "ravinder",
        "last_name": "singh",
        "email": "ravinder@gmail.com",
        "password": "ravinder123",
        "role": "candidate",
    }


@pytest.fixture(scope="function", autouse=True)
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture
def user_payload():
    return {
        "username": "ravinder77",
        "first_name": "ravinder",
        "last_name": "singh",
        "email": "ravinder@gmail.com",
        "password": "ravinder123",
        "role": UserRole.CANDIDATE.value,
    }
