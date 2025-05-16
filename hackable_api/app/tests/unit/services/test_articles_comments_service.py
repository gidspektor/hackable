import pytest
from unittest.mock import AsyncMock, MagicMock

from app.db.repositories.articles_comments_repository import (
    ArticlesCommentsRepositoryInterface,
)

from app.services.articles_comments_service import ArticlesCommentsService


@pytest.fixture
def mock_articles_comments_repository():
    return MagicMock(spec=ArticlesCommentsRepositoryInterface)


@pytest.mark.asyncio
async def test_get_article_comments(mock_articles_comments_repository):
    mock_comments = [
        MagicMock(id=1, article_id=1, comment="Test Comment 1"),
        MagicMock(id=2, article_id=1, comment="Test Comment 2"),
        MagicMock(id=3, article_id=1, comment="Test Comment 3"),
    ]

    mock_articles_comments_repository.get_article_comments = AsyncMock(
        return_value=mock_comments
    )

    service = ArticlesCommentsService(mock_articles_comments_repository)

    article_comments = await service.get_article_comments(1, 0)

    assert article_comments[0].id == 1
    assert article_comments[0].article_id == 1
    assert article_comments[0].comment == "Test Comment 1"

    assert article_comments[1].id == 2
    assert article_comments[1].article_id == 1
    assert article_comments[1].comment == "Test Comment 2"

    assert article_comments[2].id == 3
    assert article_comments[2].article_id == 1
    assert article_comments[2].comment == "Test Comment 3"


@pytest.mark.asyncio
async def test_create_article_comment(mock_articles_comments_repository):
    mock_comment = MagicMock(id=1, article_id=1, comment="Test Comment")

    mock_articles_comments_repository.create_article_comment = AsyncMock(
        return_value=mock_comment
    )

    service = ArticlesCommentsService(mock_articles_comments_repository)

    article_comment = await service.create_article_comment("Test Comment", 1, 1)

    assert article_comment.id == 1
    assert article_comment.article_id == 1
    assert article_comment.comment == "Test Comment"
