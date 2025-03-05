from sqlalchemy.future import select
from sqlalchemy.engine import Row

from interfaces.driver_interfaces.db_driver_interface import DbDriverInterface
from interfaces.repository_interfaces.articles_comments_repository_interface import ArticlesCommentsRepositoryInterface

from db.models.articles_comments import ArticlesComments
from db.models.users import Users
from db.models.articles import Articles


class ArticlesCommentsRepository(ArticlesCommentsRepositoryInterface):
    def __init__(self, db_driver: DbDriverInterface):
        self._db = db_driver
        self.comment_limmit = 10

    async def get_article_comments(self, article_id: int, offset: int) -> dict|None:
        stmt = select(
            ArticlesComments.id, ArticlesComments.article_id,
            ArticlesComments.comment, ArticlesComments.author_id
        ).where(ArticlesComments.article_id == article_id).offset(offset).limit(self.comment_limmit)

        article_comments: list[Row] = await self._db.execute(stmt).fetchall()

        return [dict(article_comment) for article_comment in article_comments]

    async def create_article_comment(self, article_comment: str, author_id: Users, article_id: Articles) -> ArticlesComments:
        new_comment = ArticlesComments(
            article_id=article_id.id,
            comment=article_comment,
            author_id=author_id.id
        )

        await self._db.add(new_comment)
        await self._db.commit()
        await self._db.refresh(new_comment)

        return new_comment

    async def get_comments_by_user(self, user_id: int) -> dict|None:
        stmt = select(
            ArticlesComments.id, ArticlesComments.article_id,
            ArticlesComments.comment, ArticlesComments.author_id
        ).where(ArticlesComments.author_id == user_id)

        comments: list[Row] = await self._db.execute(stmt).fetchall()

        return [dict(comment) for comment in comments]
