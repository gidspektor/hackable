import pytest
from unittest.mock import AsyncMock, MagicMock
from app.db.repositories.users_repository import UsersRepository
from sqlalchemy.engine import Result


@pytest.fixture
def mock_db_driver():
    """Fixture to mock the database driver."""
    return AsyncMock()

@pytest.mark.asyncio
async def test_get_user_by_username(mock_db_driver):
    """Test the get_user_by_username function of UsersRepository."""

    mock_result = MagicMock(spec=Result)

    mock_result.mappings.return_value.first.return_value = {
        "id": 1,
        "username": "testuser",
        "password_hash": "hashedpassword",
    }

    mock_db_driver.execute.return_value = mock_result

    result = await UsersRepository(mock_db_driver).get_user_by_username("testuser")

    assert result["username"] == "testuser"
    assert result["password_hash"] == "hashedpassword"
    mock_db_driver.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_bad_username(mock_db_driver):
    """Test the get_user_by_username function of UsersRepository with bad input."""

    mock_result = MagicMock(spec=Result)

    mock_result.mappings.return_value.first.return_value = None

    mock_db_driver.execute.return_value = mock_result

    result = await UsersRepository(mock_db_driver).get_user_by_username("testuser")

    assert result is None
