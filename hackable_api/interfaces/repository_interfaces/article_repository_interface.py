from abc import ABC, abstractmethod


class ArticleRepositoryInterface(ABC):
    @abstractmethod
    def get_articles(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_article(self, article_id):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def create_article(self, article):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def update_article(self, article_id, article):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def delete_article(self, article_id):
        raise NotImplementedError("This method should be overridden by subclasses")
