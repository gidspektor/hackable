from fastapi import APIRouter, Depends

from app.settings import settings

from api.v1.schemas import (
    ArticlesResponse,
    ArticleResponse,
    ArticleRequest
)

from api.dependencies import auth_exception_handler

from db.db_driver import DbDriver
from db.repositories.articles_repository import ArticlesRepository
from services.articles_service import ArticlesService

router = APIRouter(prefix="/v1")

@router.get("/article_previews", response_model=ArticlesResponse)
async def get_articles() -> ArticlesResponse:
    """API endpoint to get all article previews"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        articles = await ArticlesService(article_repository).get_articles_previews()

    return ArticlesResponse(articles=articles)

# Open to be hit by anyone, should be checking the JWT token for the user
# and then confirming if it's an admin user in the db.
@router.post("/create_article", response_model=ArticleResponse, dependencies=[Depends(auth_exception_handler)])
async def create_article(article: ArticleRequest) -> ArticleResponse:
    """API endpoint to create an article"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).create_article(article)

    return ArticleResponse(title=article.title, content=article.content)
