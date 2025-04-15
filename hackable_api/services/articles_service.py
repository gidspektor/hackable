from hackable_api.interfaces.repository_interfaces.articles_repository_interface import ArticlesRepositoryInterface


class ArticlesService:
    def __init__(self, article_repository: ArticlesRepositoryInterface):
        self._article_repository = article_repository

    async def get_articles_previews(self) -> ArticlesRepositoryInterface:
        return await self._article_repository.get_articles_previews()

    async def get_article(self, article_id: int) -> ArticlesRepositoryInterface|None:
        return await self._article_repository.get_article(article_id)

    async def create_article(self, title: str, content: str, featured: bool, user_id: int) -> ArticlesRepositoryInterface:
        featured = featured == 1
        return await self._article_repository.create_article(title, content, featured, user_id)

    async def delete_article(self, article_id: int) -> ArticlesRepositoryInterface:
        return await self._article_repository.delete_article(article_id)

    async def get_featured_articles(self) -> ArticlesRepositoryInterface:
        return await self._article_repository.get_featured_articles()

    async def get_articles_by_user(self, user_id: int) -> ArticlesRepositoryInterface:
        return await self._article_repository.get_articles_by_user(user_id)
