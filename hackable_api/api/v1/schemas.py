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


class ArticleRequest(BaseModel):
    """
    Request schema for creating an article.
    """

    title: str = Field(max_length=settings.request_max_length)
    content: str = Field(max_length=settings.request_max_length)
