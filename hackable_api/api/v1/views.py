from fastapi import APIRouter

from hackable_api.app import settings

from hackable_api.api.v1.schemas import ArticlesResponse, ArticleResponse

from hackable_api.db.db_driver import DbDriver

from hackable_api.db.repositories.article_repository import ArticleRepository

from hackable_api.services.article_service import ArticleService

router = APIRouter(prefix="/v1")

@router.get("/articles", response_model=ArticlesResponse)
async def get_articles():
    """API endpoint to get all articles"""

    session = await DbDriver(settings.db_url).get_db_session()

    article_repository = ArticleRepository(session)
    articles = await ArticleService(article_repository).get_articles()

    return ArticlesResponse(articles=articles)

@router.get("/create_article", response_model=ArticlesResponse)
async def create_article():
    """API endpoint to create an article"""

    session = await DbDriver(settings.db_url).get_db_session()

    article_repository = ArticleRepository(session)
    article = await ArticleService(article_repository).create_article()

    return ArticleResponse(title=article.title, body=article.body)
