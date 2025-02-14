from hackable_api.interfaces.driver_interfaces.db_driver_interface import DbDriverInterface
from hackable_api.interfaces.repository_interfaces.article_repository_interface import ArticleRepositoryInterface

from hackable_api.db.models.article import Articles


class ArticleRepository(ArticleRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver

    def get_articles(self):
        return self._db.query(Articles).all()

    def get_article(self, article_id: int) -> Articles|None:
        article = article.first() \
            if self._db.query(Articles).filter(Articles.id == article_id) \
            else None

    def create_article(self, article: list) -> Articles:
        self._db.add(article)
        return article

    def update_article(self):
        return []

    def delete_article(self, article_id: int) -> Articles:
        return self._db.query(Articles).filter(Articles.id == article_id).delete()
