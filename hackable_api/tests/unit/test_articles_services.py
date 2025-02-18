import pytest
from unittest.mock import AsyncMock, MagicMock

from hackable_api.services.articles_service import ArticlesService
from hackable_api.interfaces.repository_interfaces.articles_repository_interface import ArticlesRepositoryInterface

@pytest.fixture
def mock_article_repository():
    """Mock ArticlesRepositoryInterface"""

    # Create a mock repository
    return AsyncMock(spec=ArticlesRepositoryInterface)

@pytest.mark.asyncio
async def test_create_article_service(mock_article_repository):
    """Test article service for creating an article"""

    # Create a mock Article object with necessary attributes
    mock_article = MagicMock(id=1, title="Test Title", body="Test Body")

    # Mock the `create_article` method to return the mock article
    mock_article_repository.create_article = AsyncMock(return_value=mock_article)

    # Instantiate the service with the mocked repository
    service = ArticlesService(mock_article_repository)

    # Call the actual service method
    article = await service.create_article({"title": "Test Title", "body": "Test Body"})

    # Verify the service method returns the expected article
    assert article.title == "Test Title"
    assert article.body == "Test Body"

@pytest.mark.asyncio
async def test_get_articles_previews(mock_article_repository):
    """Test article service for getting articles"""

    # Create a mock Article object with necessary attributes
    mock_article = [
        MagicMock(id=1, title="Test Title", body="Test Body"),
        MagicMock(id=2, title="Test Title 2", body="Test Body 2")
    ]

    # Mock the `get_articles` method to return the mock article
    mock_article_repository.get_articles_previews = AsyncMock(return_value=mock_article)

    # Instantiate the service with the mocked repository
    service = ArticlesService(mock_article_repository)

    # Call the actual service method
    articles = await service.get_articles_previews()

    # Verify the service method returns the expected article
    assert articles[0].title == "Test Title"
    assert articles[0].body == "Test Body"
    assert articles[1].title == "Test Title 2"
    assert articles[1].body == "Test Body 2"

@pytest.mark.asyncio
async def test_get_article(mock_article_repository):
    """Test article service for getting a single article"""

    # Create a mock Article object with necessary attributes
    mock_article = MagicMock(id=1, title="Test Title", body="Test Body")

    # Mock the `get_article` method to return the mock article
    mock_article_repository.get_article = AsyncMock(return_value=mock_article)

    # Instantiate the service with the mocked repository
    service = ArticlesService(mock_article_repository)

    # Call the actual service method
    article = await service.get_article(1)

    # Verify the service method returns the expected article
    assert article.title == "Test Title"
    assert article.body == "Test Body"