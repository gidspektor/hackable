import pytest
from unittest.mock import AsyncMock, MagicMock
from app.db.repositories.articles_repository import ArticlesRepository
from sqlalchemy.engine import Result


@pytest.fixture
def mock_db_driver():
    """Fixture to mock the database driver."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_get_articles_previews(mock_db_driver):
    """Test the get_articles_previews function of ArticlesRepository."""

    mock_result = MagicMock(spec=Result)
    mock_result.mappings.return_value.all.return_value = [
        {
            "id": 1,
            "title": "Article 1",
            "content": "This is a preview of article 1.",
            "featured": False,
            "author_id": 101,
        },
        {
            "id": 2,
            "title": "Article 2",
            "content": "This is a preview of article 2.",
            "featured": False,
            "author_id": 102,
        },
    ]

    mock_db_driver.execute.return_value = mock_result

    # Instantiate the repository with the mocked database driver
    repository = ArticlesRepository(mock_db_driver)

    # Act
    articles_previews = await repository.get_articles_previews()

    # Assert
    assert len(articles_previews) == 2
    assert articles_previews[0]["title"] == "Article 1"
    assert articles_previews[1]["content"] == "This is a preview of article 2."
    mock_db_driver.execute.assert_called_once()


@pytest.mark.asyncio
async def test_delete_article_success(mock_db_driver):
    """Test delete_article when the article is successfully deleted."""

    # Arrange
    mock_result = MagicMock(spec=Result)
    mock_result.rowcount = 1
    mock_db_driver.execute.return_value = mock_result

    repository = ArticlesRepository(mock_db_driver)

    # Act
    result = await repository.delete_article(article_id=1)

    # Assert
    mock_db_driver.execute.assert_called_once()
    mock_db_driver.commit.assert_called_once()
    assert result.rowcount == 1


@pytest.mark.asyncio
async def test_delete_article_not_found(mock_db_driver):
    """Test delete_article when the article is not found."""

    # Arrange
    mock_result = MagicMock(spec=Result)
    mock_result.rowcount = 0
    mock_db_driver.execute.return_value = mock_result

    repository = ArticlesRepository(mock_db_driver)

    # Act
    result = await repository.delete_article(article_id=999)

    # Assert
    mock_db_driver.execute.assert_called_once()
    mock_db_driver.commit.assert_called_once()
    assert result == False
