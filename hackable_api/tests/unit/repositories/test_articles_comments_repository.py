import pytest
from unittest.mock import AsyncMock, MagicMock
from hackable_api.db.repositories.articles_comments_repository import ArticlesCommentsRepository
from sqlalchemy.engine import Result

@pytest.fixture
def mock_db_driver():
    """Fixture to mock the database driver."""
    return AsyncMock()

@pytest.mark.asyncio
async def test_get_article_comments(mock_db_driver):
    """Test the get_article_comments function of ArticlesCommentsRepository."""

    mock_result = MagicMock(spec=Result)
    mock_result.mappings.return_value.all.return_value = [
        {
            "id": 1,
            "article_id": 1,
            "comment": "This is a comment.",
            "author_id": 101,
            "username": "testuser"
        },
        {
            "id": 2,
            "article_id": 1,
            "comment": "This is another comment.",
            "author_id": 102,
            "username": "anotheruser"
        },
    ]

    mock_db_driver.execute.return_value = mock_result

    # Instantiate the repository with the mocked database driver
    repository = ArticlesCommentsRepository(mock_db_driver)

    # Act
    article_comments = await repository.get_article_comments(article_id=1, offset=0)

    # Assert
    assert len(article_comments) == 2
    assert article_comments[0]["comment"] == "This is a comment."
    assert article_comments[1]["username"] == "anotheruser"
    mock_db_driver.execute.assert_called_once()
