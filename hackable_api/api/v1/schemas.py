from pydantic import BaseModel, Field
from typing import List

from hackable_api.app.settings import settings


class ArticlePreviewResponse(BaseModel):
    """
    Response schema for an article preview.
    """

    id: int
    title: str
    content: str
    featured: bool


class ArticleResponse(BaseModel):
    """
    Response schema for an article.
    """

    id: int
    title: str
    content: str
    featured: bool
    username: str


class ArticlesPreviewsResponse(BaseModel):
    """
    Response schema for multiple articles.
    """

    articles: List[ArticlePreviewResponse]


class ArticleCreateRequest(BaseModel):
    """
    Request schema for creating an article.
    """

    title: str = Field(max_length=settings.title_max_length)
    content: str = Field(max_length=settings.article_max_length)
    featured: bool


class UserArticleCommentResponse(BaseModel):
    """
    Response schema for a user comment.
    """

    id: int
    comment: str
    article_id: int


class UserArticleCommentsResponse(BaseModel):
    """
    Response schema for multiple user comments.
    """

    comments: List[UserArticleCommentResponse]


class ArticleCommentResponse(BaseModel):
    """
    Response schema for an article comment.
    """

    id: int
    username: str
    article_id: int
    comment: str


class ArticleCommentsResponse(BaseModel):
    """
    Response schema for multiple article comments.
    """

    comments: List[ArticleCommentResponse]


class ArticleCommentPostRequest(BaseModel):
    """
    Request schema for creating an article comment.
    """

    article_id: int
    comment: str = Field(max_length=settings.comment_max_length)


class UsersArticleResponse(BaseModel):
    """
    Response schema for an article by a user.
    """

    id: int
    title: str


class UsersArticlesResponse(BaseModel):
    """
    Response schema for multiple articles by a user.
    """

    articles: List[UsersArticleResponse]
