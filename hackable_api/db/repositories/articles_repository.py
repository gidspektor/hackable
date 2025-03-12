from sqlalchemy import select, delete
from sqlalchemy.sql import func
from sqlalchemy.engine import Row

from interfaces.driver_interfaces.db_driver_interface import DbDriverInterface
from interfaces.repository_interfaces.articles_repository_interface import ArticlesRepositoryInterface

from db.models.articles import Articles


class ArticlesRepository(ArticlesRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver
        self.featured_limit = 3

    async def get_articles_previews(self) -> list[dict]:
        stmt = select(
            Articles.id,
            Articles.title,
            func.substr(Articles.content, 1, 200).label("body")
        )

        result = await self._db.execute(stmt)

        rows: list[Row] = result.fetchall()

        return [{"id": row.id, "title": row.title, "content": row.content} for row in rows]

    async def get_article(self, article_id: int) -> dict|None:
        stmt = select(
            Articles.id, Articles.title, Articles.content
        ).where(Articles.id == article_id)

        article = await self._db.execute(stmt).scalar_one_or_none()

        return article

    async def create_article(self, title: str, content: str, featured: bool, user_id: int) -> Articles:
        new_article = Articles(
            title=title, content=content,
            featured=featured, author_id=user_id
        )
        await self._db.add(new_article)
        await self._db.commit()
        await self._db.refresh(new_article)

        return new_article

    async def delete_article(self, article_id: int) -> Articles:
        stmt = delete(Articles).where(Articles.id == article_id)
        result = await self._db.execute(stmt)
        await self._db.commit()

        if result.rowcount == 0:
            False

        return result

    async def get_featured_articles(self) -> list[dict]:
        stmt = select(
            Articles.id,
            Articles.title,
            func.substr(Articles.content, 1, 200).label("body")
        ).where(Articles.featured == True).limit(self.featured_limit)

        result = await self._db.execute(stmt)

        rows: list[Row] = result.fetchall()

        return [dict(row) for row in rows]

    async def get_articles_by_user(self, user_id: int) -> list[dict]:
        stmt = select(
            Articles.id,
            Articles.title,
        ).where(Articles.author_id == user_id)

        result = await self._db.execute(stmt)

        rows: list[Row] = result.fetchall()

        return [dict(row) for row in rows]