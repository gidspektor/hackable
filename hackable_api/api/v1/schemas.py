from pydantic import BaseModel
from typing import List


class ArticleResponse(BaseModel):
	"""
	Response schema for any article.
	"""

	title: str
	body: str


class ArticlesResponse(BaseModel):
	"""
	Response schema for multiple articles.
	"""

	articles: List[ArticleResponse]
