from unittest.mock import AsyncMock, MagicMock
import pytest

from hackable_api.api.v1.views import get_articles
from hackable_api.api.v1.schemas import ArticlesResponse

@pytest.mark.asyncio
async def test_get_articles(mocker):
    db_driver = MagicMock()
    mocker.patch("hackable_api.api.v1.views.DbDriver", return_value=db_driver)

    article_repository = MagicMock()
    mocker.patch("hackable_api.api.v1.views.ArticleRepository", return_value=article_repository)

    article_service = mocker.patch("hackable_api.api.v1.views.ArticleService")
    article_service_instance = article_service.return_value
    article_service_instance.get_articles = AsyncMock(return_value=[
        {"title": "Title 1", "body": "article content 1"},
        {"title": "Title 2", "body": "article content 2"}
    ])

    articles = await get_articles()

    assert isinstance(articles, ArticlesResponse)

    assert len(articles.articles) == 2
    assert articles.articles[0].title == "Title 1"
    assert articles.articles[0].body == "article content 1"
    assert articles.articles[1].title == "Title 2"
    assert articles.articles[1].body == "article content 2"
