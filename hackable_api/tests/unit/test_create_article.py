import pytest
from unittest.mock import MagicMock, AsyncMock

from hackable_api.api.v1.schemas import ArticleResponse
from hackable_api.api.v1.views import create_article

@pytest.mark.asyncio
async def test_create_article(mocker):
    db_driver = MagicMock()
    mocker.patch("hackable_api.api.v1.views.DbDriver", return_value=db_driver)

    article_repository = MagicMock()
    mocker.patch("hackable_api.api.v1.views.ArticleRepository", return_value=article_repository)

    article_service = mocker.patch("hackable_api.api.v1.views.ArticleService")
    article_service_instance = article_service.return_value
    article_service_instance.create_article = AsyncMock(return_value={"title": "Title 1", "body": "article content 1"})

    article = await create_article()

    assert isinstance(article, ArticleResponse)
    assert article.title == "Title 1"
    assert article.body == "article content 1"
