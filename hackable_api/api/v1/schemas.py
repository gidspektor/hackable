from pydantic import BaseModel
from typing import List

from hackable_api.app.settings import settings


class ArticleResponse(BaseModel):
	"""
	Response schema for an article.
	"""

	id: int
	title: str
	body: str


class ArticlesResponse(BaseModel):
	"""
	Response schema for multiple articles.
	"""

	articles: List[ArticleResponse]


class ArticleRequest(BaseModel):
	"""
	Request schema for creating an article.
	"""

	title: str
	body: str

	class Config:
		str_max_length = settings.request_max_lenth
