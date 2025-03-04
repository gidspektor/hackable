from abc import ABC, abstractmethod


class ArticlesRepositoryInterface(ABC):
    @abstractmethod
    def get_articles_previews(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_article(self, article_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def create_article(self, article: int, user_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def delete_article(self, article_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_featured_articles(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_articles_by_user(self, user_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")
