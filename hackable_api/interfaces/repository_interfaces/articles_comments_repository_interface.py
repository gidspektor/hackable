from abc import ABC, abstractmethod

from db.models.articles_comments import ArticlesComments


class ArticlesCommentsRepositoryInterface(ABC):
    @abstractmethod
    async def get_article_comments(self, article_id: int, offset: int) -> ArticlesComments:
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def create_article_comment(self, article_comment: str, author_id: int, article_id: int) -> ArticlesComments:
        raise NotImplementedError("This method should be overridden by subclasses")
