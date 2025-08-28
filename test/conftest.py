import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import  sessionmaker
from app.db.base import Base
from app.models import User
from fastapi.testclient import TestClient
from starlette import status
import time
from app.main import app
from app.db.session import get_db
from app.api.dependencies import get_current_user




TEST_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
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
def default_user():
    return User(
        id=1,
        username="ravinder77",
        first_name="ravinder",
        last_name="singh",
        email="ravinder@gmail.com",
        role="candidate"
    )


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user




def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {
        'status': 'ok'
    }


