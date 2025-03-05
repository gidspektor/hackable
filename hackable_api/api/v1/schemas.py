from pydantic import BaseModel, Field
from typing import List

from app.settings import settings


class ArticleResponse(BaseModel):
	"""
	Response schema for an article.
	"""

	id: int
	title: str
	content: str


class ArticlesResponse(BaseModel):
	"""
	Response schema for multiple articles.
	"""

	articles: List[ArticleResponse]


class ArticleCreateRequest(BaseModel):
	"""
	Request schema for creating an article.
	"""

	title: str = Field(max_length=settings.title_max_length)
	content: str = Field(max_length=settings.article_max_length)
	featured: bool


class ArticleGetRequest(BaseModel):
	"""
	Request schema for getting an article.
	"""

	article_id: int = Field(max_length=settings.article_max_length)


class ArticleCommentResponse(BaseModel):
	"""
	Response schema for an article comment.
	"""

	id: int
	author_id: int
	article_id: int
	comment: str


class ArticleCommentsResponse(BaseModel):
	"""
	Response schema for multiple article comments.
	"""

	comments: List[ArticleCommentResponse]


class ArticleCommentGetRequest(BaseModel):
	"""
	Request schema for getting article comments.
	"""

	article_id: int = Field(max_length=settings.request_max_length)
	offset: int = Field(max_length=settings.request_max_length)


class ArticleCommentPostRequest(BaseModel):
	"""
	Request schema for creating an article comment.
	"""

	article_id: int = Field(max_length=settings.request_max_length)
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
