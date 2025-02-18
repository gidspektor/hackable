from sqlalchemy.future import select
from sqlalchemy.sql import func
from sqlalchemy.engine import Row

from hackable_api.interfaces.driver_interfaces.db_driver_interface import DbDriverInterface
from hackable_api.interfaces.repository_interfaces.articles_repository_interface import ArticlesRepositoryInterface

from hackable_api.db.models.articles import Articles


class ArticlesRepository(ArticlesRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver

    async def get_articles_previews(self) -> list[dict]:
        stmt = select(
            Articles.id,
            Articles.title,
            func.substr(Articles.body, 1, 200).label("body")
        )

        result = await self._db.execute(stmt)

        rows: list[Row] = result.fetchall()

        return [{"id": row.id, "title": row.title, "body": row.body} for row in rows]

    async def get_article(self, article_id: int) -> dict|None:
        stmt = select(
            Articles.id, Articles.title, Articles.body
        ).where(Articles.id == article_id)

        article = await self._db.execute(stmt).first()

        return {"id": article.id, "title": article.title, "body": article.body} \
            if article \
            else None

    async def create_article(self, article: dict) -> Articles:
        return await self._db.add(article)

    async def update_article(self):
        return await []

    async def delete_article(self, article_id: int) -> Articles:
        return await self._db.query(Articles).filter(Articles.id == article_id).delete()
