from abc import ABC, abstractmethod


class ArticlesRepositoryInterface(ABC):
    @abstractmethod
    async def get_articles_previews(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_article(self, article_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def create_article(
        self, title: str, content: str, featured: bool, user_id: int
    ):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def delete_article(self, article_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_featured_articles(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    async def get_articles_by_user(self, user_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")
