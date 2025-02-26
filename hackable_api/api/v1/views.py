from fastapi import APIRouter, Depends

from app.settings import settings

from api.v1.schemas import (
    ArticlesResponse,
    ArticleResponse,
    ArticleRequest
)

from db.db_driver import DbDriver
from db.repositories.articles_repository import ArticlesRepository
from services.articles_service import ArticlesService
from api.middlewares.jwt_middleware import JWTMiddleware

router = APIRouter(prefix="/v1", dependencies=[Depends(JWTMiddleware())])

@router.get("/article_previews", response_model=ArticlesResponse)
async def get_articles() -> ArticlesResponse:
    """API endpoint to get all article previews"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        articles = await ArticlesService(article_repository).get_articles_previews()

    return ArticlesResponse(articles=articles)

@router.post("/create_article", response_model=ArticlesResponse)
async def create_article(article: ArticleRequest) -> ArticleResponse:
    """API endpoint to create an article"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).create_article(article)

    return ArticleResponse(title=article.title, content=article.content)
