import pytest
from starlette.testclient import TestClient
from sqlalchemy import text

from app.app.application import get_app
from app.app.settings import settings
from app.db.db_driver import DbDriver
from app.db.repositories.users_repository import UsersRepository
from app.services.users_service import UsersService
from app.services.auth_service import AuthService

app = get_app()
client = TestClient(app)

@pytest.fixture(scope="module")
async def setup_test_user():
    """
    Fixture to set up a test user in the database.
    """

    # User ID will be 6
    async with DbDriver(settings.db_url).get_db_session() as session:
        user_repository = UsersRepository(session)
        await UsersService(user_repository).create_user({
            "username": "testuser",
            "password": "testpassword",
        })
    yield

    # async with DbDriver(settings.db_url).get_db_session() as session:
    #     await session.execute(text("DELETE FROM users WHERE username = 'testuser'"))
    #     await session.commit()

@pytest.fixture(scope="module")
def token():
    """
    Fixture to create a mock access token.
    """
    # Mock the data to be encoded
    data = {"sub": "6", "exp": 3600}

    # Create the access token
    return AuthService.create_access_token(data, 60)

def test_login_success(token):
    """
    Test successful login.
    """

    # Prepare the login request payload
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Add the Authorization header with the JWT
    headers = {"Authorization": f"Bearer {token}"}

    # Send a POST request to the /login/ endpoint
    response = client.post("/api/login/", json=payload, headers=headers)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response body contains the expected fields
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] == 6
    assert "username" in response_data
    assert response_data["username"] == "testuser"
    assert "is_admin" in response_data
    assert "jwt" in response_data

    # Assert the refresh token is set as a cookie
    cookies = response.cookies
    assert "refresh_token" in cookies
    assert cookies["refresh_token"] is not None


def test_login_failure(token):
    """
    Test login failure with incorrect credentials.
    """

    # Prepare the login request payload with incorrect credentials
    payload = {
        "username": "wronguser",
        "password": "wrongpassword"
    }

    # Add the Authorization header with the JWT
    headers = {"Authorization": f"Bearer {token}"}

    # Send a POST request to the /login/ endpoint
    response = client.post("/api/login/", json=payload, headers=headers)

    # Assert the response status code
    assert response.status_code == 401

    # Assert the response body contains the expected error message
    response_data = response.json()
    assert response_data["detail"] == "None"  # Adjust based on your error handling

def test_get_user_success(token):
    """
    Test successful retrieval of user information.
    """

    # Add the Authorization header with the JWT
    headers = {"Authorization": f"Bearer {token}"}

    # Send a GET request to the /user/ endpoint
    response = client.get("/api/user/", headers=headers)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response body contains the user information
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] == 6
    assert "username" in response_data
    assert response_data["username"] == "testuser"
    assert "is_admin" in response_data

def test_get_user_invalid_token():
    """
    Test retrieval of user information with an invalid token.
    """

    # Add an invalid Authorization header
    headers = {"Authorization": "Bearer invalid_token"}

    # Send a GET request to the /user/ endpoint
    response = client.get("/api/user/", headers=headers)

    # Assert the response status code
    assert response.status_code == 401

    # Assert the response body contains the expected error message
    response_data = response.json()
    assert response_data["detail"] == "Invalid or expired token"

def test_get_user_missing_token():
    """
    Test retrieval of user information without a token.
    """

    # Send a GET request to the /user/ endpoint without headers
    response = client.get("/api/user/")

    # Assert the response status code
    assert response.status_code == 401

    # Assert the response body contains the expected error message
    response_data = response.json()
    assert response_data["detail"] == "Authorization header missing or invalid"

@pytest.mark.asyncio
async def test_create_user_success(token):
    """
    Test successful user creation.
    """

    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/user/", json={
            "username": "newuser6578",
            "password": "newpassword"
        },
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] is not None
    assert "username" in response_data
    assert response_data["username"] == "newuser6578"

    async with DbDriver(settings.db_url).get_db_session() as session:
        user = await session.execute(text("SELECT id FROM users WHERE username = 'newuser6578'"))
        user_id = user.scalar_one_or_none()
        assert user_id is not None

        await session.execute(text("DELETE FROM users WHERE username = 'newuser6578'"))
        await session.commit()

def test_refresh_token_success(token):
    """
    Test successful token refresh.
    """

    # Set the refresh token as a cookie
    cookies = {"refresh_token": token}

    # Send a POST request to the /refresh/ endpoint
    response = client.post("/api/refresh/", cookies=cookies)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response body contains the new JWT
    response_data = response.json()
    assert "jwt" in response_data
    assert response_data["jwt"] is not None

def test_refresh_token_missing():
    """
    Test refresh token missing in the request.
    """

    cookies = {"refresh_token": ""}

    # Send a POST request to the /refresh/ endpoint without cookies
    response = client.post("/api/refresh/", cookies=cookies)

    # Assert the response status code
    assert response.status_code == 400

    # Assert the response body contains the expected error message
    response_data = response.json()
    assert response_data["detail"] == "Refresh token missing"

def test_refresh_token_invalid():
    """
    Test refresh token invalid.
    """

    # Set an invalid refresh token as a cookie
    cookies = {"refresh_token": "invalid_token"}

    # Send a POST request to the /refresh/ endpoint
    response = client.post("/api/refresh/", cookies=cookies)

    # Assert the response status code
    assert response.status_code == 401

    # Assert the response body contains the expected error message
    response_data = response.json()
    assert response_data["detail"] == "Refresh token invalid"
