from fastapi import APIRouter, Depends, HTTPException

from app.app.settings import settings

from app.api.v1.schemas import (
    ArticlesPreviewsResponse,
    ArticleResponse,
    ArticleCreateRequest,
    ArticleCommentsResponse,
    ArticleCommentResponse,
    ArticleCommentPostRequest,
    UsersArticlesResponse,
    UserArticleCommentsResponse,
    FeaturedArticlesPreviewsResponse,
)

from app.api.dependencies import auth_exception_handler

from app.services.users_service import UsersService
from app.services.articles_service import ArticlesService
from app.services.articles_comments_service import ArticlesCommentsService

from app.db.db_driver import DbDriver
from app.db.repositories.articles_repository import ArticlesRepository
from app.db.repositories.articles_comments_repository import (
    ArticlesCommentsRepository,
)
from app.db.repositories.users_repository import UsersRepository

router = APIRouter(prefix="/v1")


@router.get("/articles/previews/", response_model=ArticlesPreviewsResponse)
async def get_articles() -> ArticlesPreviewsResponse:
    """API endpoint to get all article previews"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        articles = await ArticlesService(article_repository).get_articles_previews()

    return ArticlesPreviewsResponse(articles=articles)


@router.get("/articles/featured/", response_model=FeaturedArticlesPreviewsResponse)
async def get_featured_articles() -> FeaturedArticlesPreviewsResponse:
    """API endpoint to get a featured article"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        articles = await ArticlesService(article_repository).get_featured_articles()

    return FeaturedArticlesPreviewsResponse(articles=articles)


# Open to be hit by anyone, should be checking the JWT token for the user
# and then confirming if it's an admin user in the db.
@router.post("/article/", response_model=dict)
async def create_article(
    article: ArticleCreateRequest, decoded_token: dict = Depends(auth_exception_handler)
) -> dict[str]:
    """API endpoint to create an article"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).create_article(
            article.title, article.content, article.featured, int(user_id)
        )

    if not article:
        raise HTTPException(status_code=400, detail="Article not created")

    return { "message": "Article created successfully" }


@router.get("/article/{article_id}/", response_model=ArticleResponse)
async def get_article(article_id: int) -> ArticleResponse:
    """API endpoint to get a single article"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).get_article(article_id)

    return ArticleResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        featured=article.featured,
        username=article.username,
    )


@router.get(
    "/article/{article_id}/comments/{offset}/", response_model=ArticleCommentsResponse
)
async def get_article_comments(article_id: int, offset: int) -> ArticleCommentsResponse:
    """API endpoint to get article comments"""

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_comments_repository = ArticlesCommentsRepository(session)
        comments = await ArticlesCommentsService(
            article_comments_repository
        ).get_article_comments(article_id, offset)

    return ArticleCommentsResponse(comments=comments)


@router.post("/comment/", response_model=ArticleCommentResponse)
async def create_comment(
    article_comment: ArticleCommentPostRequest,
    decoded_token: dict = Depends(auth_exception_handler),
) -> ArticleCommentResponse:
    """API endpoint to create a comment"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_comments_repository = ArticlesCommentsRepository(session)
        comment = await ArticlesCommentsService(
            article_comments_repository
        ).create_article_comment(
            article_comment.comment, int(user_id), article_comment.article_id
        )

        user_repository = UsersRepository(session)
        username = await UsersService(user_repository).get_username(int(user_id))

    return ArticleCommentResponse(
        id=comment.id,
        username=username,
        article_id=comment.article_id,
        comment=comment.comment,
    )


@router.delete("/article/{article_id}/", response_model=dict[str, str])
async def delete_article(article_id: int) -> dict[str, str]:
    """API endpoint to delete an article"""

    deleted = False

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        deleted = await ArticlesService(article_repository).delete_article(
            article_id
        )

    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")

    return {"message": "Ok"}


@router.get("/user/articles/", response_model=UsersArticlesResponse)
async def get_user_articles(
    decoded_token: dict = Depends(auth_exception_handler),
) -> UsersArticlesResponse:
    """API endpoint to get all articles for a user"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_repository = ArticlesRepository(session)
        articles = await ArticlesService(article_repository).get_articles_by_user(
            int(user_id)
        )

    return UsersArticlesResponse(articles=articles)


@router.get("/user/comments/", response_model=UserArticleCommentsResponse)
async def get_user_comments(
    decoded_token: dict = Depends(auth_exception_handler),
) -> UserArticleCommentsResponse:
    """API endpoint to get all comments by a user"""

    user_id: str = decoded_token.get("sub")

    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid user ID")

    async with DbDriver(settings.db_url).get_db_session() as session:
        article_comments_repository = ArticlesCommentsRepository(session)
        comments = await ArticlesCommentsService(
            article_comments_repository
        ).get_comments_by_user(int(user_id))

    return UserArticleCommentsResponse(comments=comments)
