from starlette import status
from app.core.enums import UserRole
from app.main import app
from app.db.session import get_db
from app.api.dependencies import get_current_user
from test.conftest import override_get_db, override_current_user
from app.models import User
from app.core.security import hash_password


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user



def test_create_user(client, db_session):
    payload = {
        "username": "ravinder77",
        "first_name": "ravinder",
        "last_name": "singh",
        "email": "ravinder@gmail.com",
        "password": "ravinder123",
        "role": "candidate",
    }

    response = client.post('/api/v1/auth/signup', json=payload)

    #Assert that api responded correctly
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['id'] == 1
    assert data['username'] == payload['username']
    assert data['first_name'] == payload['first_name']
    assert data['last_name'] == payload['last_name']
    assert data['email'] == payload['email']
    assert data['role'] == payload['role']

    # check in db
    user_in_db = db_session.query(User).filter(User.id == 1).first()
    assert user_in_db is not None

    assert 'access_token' in data


    assert user_in_db.username == payload['username']
    assert user_in_db.hashed_password != payload['password']


def test_login_user(client, db_session):
    #Create user
    user = User(
        username="ravinder77",
        first_name="ravinder",
        last_name="singh",
        email="ravinder@gmail.com",
        hashed_password=hash_password("ravinder123"),
        role=UserRole.CANDIDATE,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()

    # Login with form data
    response = client.post('/api/v1/auth/login',
                           data={'username': user.email, 'password': 'ravinder123'},
                           headers={"Content-Type": "application/x-www-form-urlencoded"}
                           )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # verify response content
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'

    #verify cookies
    assert 'refresh_token' in response.cookies




