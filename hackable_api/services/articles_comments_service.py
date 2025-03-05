from db.repositories.articles_comments_repository import ArticlesCommentsRepositoryInterface


class ArticlesCommentsService:
    def __init__(self, articles_comments_repository: ArticlesCommentsRepositoryInterface):
        self._articles_comments_repository = articles_comments_repository

    async def get_article_comments(self, article_id: int, offset: int) -> ArticlesCommentsRepositoryInterface:
        return await self._articles_comments_repository.get_article_comments(article_id, offset)

    async def create_article_comment(self, article_comment: str, author_id: int, article_id: int) -> ArticlesCommentsRepositoryInterface:
        return await self._articles_comments_repository.create_article_comment(article_comment, author_id, article_id)

    async def get_comments_by_user(self, user_id: int) -> ArticlesCommentsRepositoryInterface:
        return await self._articles_comments_repository.get_comments_by_user(user_id)
