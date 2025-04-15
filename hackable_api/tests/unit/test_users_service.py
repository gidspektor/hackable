import pytest
import bcrypt
from unittest.mock import AsyncMock, MagicMock

from hackable_api.services.users_service import UsersService

from hackable_api.interfaces.repository_interfaces.users_repository_interface import UsersRepositoryInterface

@pytest.fixture
def mock_users_repository():
    """Mock UsersRepositoryInterface"""

    return AsyncMock(spec=UsersRepositoryInterface)

@pytest.mark.asyncio
async def test_create_user(mock_users_repository):
    """Test user service for creating a user"""

    # Create a mock User object with necessary attributes
    mock_user = MagicMock(id=1, username="testuser", password_hash="hashedpassword")

    # Mock the `create_user` method to return the mock user
    mock_users_repository.create_user = AsyncMock(return_value=mock_user)

    # Instantiate the service with the mocked repository
    service = UsersService(mock_users_repository)

    # Call the actual service method
    user_data = {"username": "testuser", "password": "password"}
    user = await service.create_user(user_data)

    assert user.username == "testuser"
    assert user.password_hash == "hashedpassword"

def test_hash_password():
    """Test user service for hashing a password"""

    # Call the actual service method
    password = "password"
    hashed_password = UsersService.hash_password(password)

    assert hashed_password != password
    assert bcrypt.checkpw(password.encode("utf-8"), hashed_password)

@pytest.mark.asyncio
async def test_change_password(mock_users_repository):
    """Test user service for changing a password"""

    # Mock the `get_user_password_by_id` method to return a hashed password
    mock_users_repository.get_user_password_by_id = AsyncMock(return_value=bcrypt.hashpw(b"oldpassword", bcrypt.gensalt()))

    # Mock the `change_password` method to return True
    mock_users_repository.change_password = AsyncMock(return_value=True)

    # Instantiate the service with the mocked repository
    service = UsersService(mock_users_repository)

    # Call the actual service method
    result = await service.change_password("newpassword", "newpassword", "oldpassword", 1)

    assert result is True

@pytest.mark.asyncio
async def test_change_passwords_dont_match(mock_users_repository):
    """Test user service for changing a password but they don't match"""

    # Instantiate the service with the mocked repository
    service = UsersService(mock_users_repository)

    # Call the actual service method
    result = await service.change_password("newpassword", "notsosnew", "oldpassword", 1)

    assert result is False
