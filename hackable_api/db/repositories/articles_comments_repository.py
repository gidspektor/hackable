from sqlalchemy.future import select

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

        article_comments = await self._db.execute(stmt).fetchall()

        return [
            {
                "article_id": article_comment.article_id,
                "article_comment": article_comment.comment,
                "author_id": article_comment.author_id,
                "id": article_comment.id,
            }
            for article_comment in article_comments
        ]

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
