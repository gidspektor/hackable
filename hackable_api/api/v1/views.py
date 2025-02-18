from fastapi import APIRouter

from hackable_api.app import settings

from hackable_api.api.v1.schemas import (
    ArticlesResponse,
    ArticleResponse,
    ArticleRequest
)

from hackable_api.db.db_driver import DbDriver

from hackable_api.db.repositories.articles_repository import ArticlesRepository

from hackable_api.services.articles_service import ArticlesService

router = APIRouter(prefix="/v1")

@router.get("/article_previews", response_model=ArticlesResponse)
async def get_articles():
    """API endpoint to get all article previews"""

    session = await DbDriver(settings.db_url).get_db_session()

    article_repository = ArticlesRepository(session)
    articles = await ArticlesService(article_repository).get_articles_previews()

    return ArticlesResponse(articles=articles)

@router.post("/create_article", response_model=ArticlesResponse)
async def create_article(article: ArticleRequest):
    """API endpoint to create an article"""

    session = await DbDriver(settings.db_url).get_db_session()

    article_repository = ArticlesRepository(session)
    article = await ArticlesService(article_repository).create_article(article)

    return ArticleResponse(title=article.title, body=article.body)
