import tempfile
import pytest
import bcrypt
import os

from starlette.testclient import TestClient
from sqlalchemy import text
from pathlib import Path

from app.app.application import get_app
from app.app.settings import settings
from app.db.db_driver import DbDriver
from app.db.repositories.users_repository import UsersRepository
from app.services.users_service import UsersService
from app.services.auth_service import AuthService

APP_ROOT = Path(__file__).parent.parent.parent

app = get_app()
client = TestClient(app)


@pytest.mark.asyncio
async def test_user():
    """
    Helper function to create a test user in the database.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        # Reset table before each test
        await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        await session.commit()

        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).create_user(
            {
                "username": "testuser",
                "password": "testpassword",
            }
        )
    return user


@pytest.fixture(scope="module")
def token():
    """
    Fixture to create a mock access token.
    """

    # Mock the data to be encoded
    data = {"sub": "1", "exp": 3600}

    # Create the access token
    return AuthService.create_access_token(data, 60)


@pytest.mark.asyncio
async def test_login_success():
    """
    Test successful login.
    """
    await test_user()  # Ensure the test user is created
    # Prepare the login request payload
    payload = {"username": "testuser", "password": "testpassword"}

    # Send a POST request to the /login/ endpoint
    response = client.post("/api/login/", json=payload)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response body contains the expected fields
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] is not None
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
    payload = {"username": "wronguser", "password": "wrongpassword"}

    # Add the Authorization header with the JWT
    headers = {"Authorization": f"Bearer {token}"}

    # Send a POST request to the /login/ endpoint
    response = client.post("/api/login/", json=payload, headers=headers)

    # Assert the response status code
    assert response.status_code == 401

    # Assert the response body contains the expected error message
    response_data = response.json()
    assert response_data["detail"] == "None"  # Adjust based on your error handling


@pytest.mark.asyncio
async def test_get_user_success(token):
    """
    Test successful retrieval of user information.
    """

    await test_user()  # Ensure the test user is created

    # Add the Authorization header with the JWT
    headers = {"Authorization": f"Bearer {token}"}

    # Send a GET request to the /user/ endpoint
    response = client.get("/api/user/", headers=headers)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response body contains the user information
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] == 1
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
async def test_create_user_success():
    """
    Test successful user creation.
    """

    response = client.post(
        "/api/user/", json={"username": "newuser6578", "password": "newpassword"}
    )

    assert response.status_code == 200

    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] is not None
    assert "username" in response_data
    assert response_data["username"] == "newuser6578"

    async with DbDriver(settings.db_url).get_db_session() as session:
        user = await session.execute(
            text("SELECT id FROM users WHERE username = 'newuser6578'")
        )
        user_id = user.scalar_one_or_none()
        assert user_id is not None

        await session.execute(text("DELETE FROM users WHERE username = 'newuser6578'"))
        await session.commit()


@pytest.mark.asyncio
async def test_change_password(token):
    """
    Test successful password change for an existing user.
    """

    await test_user()  # Ensure the test user is created

    # Add the Authorization header with the JWT
    headers = {"Authorization": f"Bearer {token}"}

    response = client.patch(
        "/api/user/password/",
        json={
            "old_password": "testpassword",
            "new_password": "newpassword",
            "new_password_match": "newpassword",
        },
        headers=headers,
    )

    assert response.status_code == 200

    async with DbDriver(settings.db_url).get_db_session() as session:
        user = await session.execute(
            text("SELECT password_hash FROM users WHERE username = 'testuser'")
        )
        password_hash = user.scalar_one_or_none()
        bcrypt.checkpw(
            password_hash.encode("utf-8"),
            UsersService.hash_password("newpassword").encode("utf-8"),
        )


@pytest.mark.asyncio
async def test_upload_image_success(token):
    """
    Test successful image upload.
    """

    await test_user()  # Ensure the test user is created

    # Create a temporary file to simulate an uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(b"Test file content")
        temp_file_path = temp_file.name

    # Open the file in binary mode for the request
    with open(temp_file_path, "rb") as file:
        headers = {"Authorization": f"Bearer {token}"}

        response = client.patch(
            "/api/upload/image/",
            headers=headers,
            files={"image": ("test_file.png", file, "png")},
        )

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert "image_path" in response_data

    # Clean up the temporary file
    os.remove(temp_file_path)


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
