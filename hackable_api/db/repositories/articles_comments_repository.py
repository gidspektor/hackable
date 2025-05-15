from sqlalchemy.future import select
from sqlalchemy.sql import func

from datetime import datetime

from hackable_api.interfaces.driver_interfaces.db_driver_interface import (
    DbDriverInterface,
)
from hackable_api.interfaces.repository_interfaces.articles_comments_repository_interface import (
    ArticlesCommentsRepositoryInterface,
)

from hackable_api.db.models.articles_comments import ArticlesComments
from hackable_api.db.models.users import Users


class ArticlesCommentsRepository(ArticlesCommentsRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver
        self.comment_limmit = 10

    async def get_article_comments(self, article_id: int, offset: int) -> dict | None:
        stmt = (
            select(
                ArticlesComments.id,
                ArticlesComments.article_id,
                ArticlesComments.comment,
                ArticlesComments.author_id,
                Users.username,
            )
            .join(Users, ArticlesComments.author_id == Users.id)
            .where(ArticlesComments.article_id == article_id)
            .order_by(ArticlesComments.created_at.asc())
            .offset(offset)
            .limit(self.comment_limmit)
        )

        article_comments = await self._db.execute(stmt)

        return article_comments.mappings().all()

    async def create_article_comment(
        self, article_comment: str, author_id: int, article_id: int
    ) -> ArticlesComments:
        new_comment = ArticlesComments(
            article_id=article_id,
            comment=article_comment,
            author_id=author_id,
            created_at=datetime.utcnow(),
        )

        self._db.add(new_comment)
        await self._db.commit()
        await self._db.refresh(new_comment)

        return new_comment

    async def get_comments_by_user(self, user_id: int) -> dict | None:
        stmt = select(
            ArticlesComments.id,
            ArticlesComments.article_id,
            func.substr(ArticlesComments.comment, 1, 100).label("comment"),
        ).where(ArticlesComments.author_id == user_id)

        comments = await self._db.execute(stmt)

        return comments.mappings().all()
