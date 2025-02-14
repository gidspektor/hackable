from hackable_api.interfaces.repository_interfaces.article_repository_interface import ArticleRepositoryInterface


class ArticleService:
    def __init__(self, article_repository: ArticleRepositoryInterface):
        self._article_repository = article_repository

    def get_articles(self):
        return self._article_repository.get_articles()

    def get_article(self, article_id: int) -> ArticleRepositoryInterface|None:
        return self._article_repository.get_article(article_id)

    def create_article(self, article: list) -> ArticleRepositoryInterface:
        return self._article_repository.create_article(article)

    def update_article(self, article_id: int, article: list) -> ArticleRepositoryInterface:
        return self._article_repository.update_article(article_id, article)

    def delete_article(self, article_id: int) -> ArticleRepositoryInterface:
        return self._article_repository.delete_article(article_id)
