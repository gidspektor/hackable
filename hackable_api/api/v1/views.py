from fastapi import APIRouter, Depends, HTTPException

from app.settings import settings

from api.v1.schemas import (
    ArticlesResponse, ArticleResponse,
    ArticleCreateRequest, ArticleCommentGetRequest,
    ArticleCommentsResponse, ArticleCommentResponse,
    ArticleGetRequest, ArticleCommentPostRequest,
    UsersArticlesResponse,
)

from api.dependencies import auth_exception_handler

from db.db_driver import DbDriver
from db.repositories.articles_repository import ArticlesRepository
from services.articles_service import ArticlesService
from services.articles_comments_service import ArticlesCommentsService
from db.repositories.articles_comments_repository import ArticlesCommentsRepository

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
@router.post("/article", response_model=ArticleResponse)
async def create_article(article: ArticleCreateRequest, decoded_token: str = Depends(auth_exception_handler)) -> ArticleResponse:
    """API endpoint to create an article"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).create_article(article, user_id)

    return ArticleResponse(title=article.title, content=article.content)

@router.get("/article/{article_id}", response_model=ArticleResponse)
async def get_article(article: ArticleGetRequest) -> ArticleResponse:
    """API endpoint to get a single article"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).get_article(article.article_id)

    return ArticleResponse(id=article.id, title=article.title, content=article.content)

@router.get("/article/{article_id}/comments/{offset}", response_model=ArticleCommentsResponse)
async def get_article_comments(article_comment: ArticleCommentGetRequest) -> ArticleCommentsResponse:
    """API endpoint to get article comments"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_comments_repository = ArticlesCommentsRepository(session)
        comments = await ArticlesCommentsService(
            article_comments_repository
        ).get_article_comments(article_comment.article_id, article_comment.offset)

    return ArticleCommentsResponse(comments=comments)

@router.post("/comment", response_model=ArticleCommentResponse)
async def create_comment(article_comment: ArticleCommentPostRequest, decoded_token: str = Depends(auth_exception_handler)) -> ArticleCommentResponse:
    """API endpoint to create a comment"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_comments_repository = ArticlesCommentsRepository(session)
        comment = await ArticlesCommentsService(
            article_comments_repository
        ).create_article_comment(article_comment.comment, user_id, article_comment.article_id)

    return ArticleCommentResponse(
        id=comment.id, author_id=comment.author_id, article_id=comment.article_id, comment=comment.comment
    )

@router.get("articles/featured", response_model=ArticlesResponse)
async def get_featured_articles() -> ArticlesResponse:
    """API endpoint to get a featured article"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).get_featured_articles()

    return ArticlesResponse(id=article.id, title=article.title, content=article.content)

@router.delete("/article/{article_id}", response_model=dict[str, str])
async def delete_article(article: int) -> dict[str, str]:
    """API endpoint to delete an article"""

    deleted = False

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        deleted = await ArticlesService(article_repository).delete_article(article.article_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")

    return {"message": "Ok"}

@router.get("/articles/{user_id}", response_model=UsersArticlesResponse)
async def get_user_articles(user_id: str, decoded_token: str = Depends(auth_exception_handler)) -> UsersArticlesResponse:
    """API endpoint to get all articles for a user"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        articles = await ArticlesService(article_repository).get_articles_by_user(user_id)

    return UsersArticlesResponse(articles=articles)

@router.get("/articles/comments/{user_id}", response_model=ArticleCommentsResponse)
async def get_user_comments(user_id: str, decoded_token: str = Depends(auth_exception_handler)) -> ArticleCommentsResponse:
    """API endpoint to get all comments for a user"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_comments_repository = ArticlesCommentsRepository(session)
        comments = await ArticlesCommentsService(
            article_comments_repository
        ).get_comments_by_user(user_id)

    return ArticleCommentsResponse(comments=comments)
