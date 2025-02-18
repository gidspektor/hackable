from hackable_api.interfaces.repository_interfaces.articles_repository_interface import ArticlesRepositoryInterface


class ArticlesService:
    def __init__(self, article_repository: ArticlesRepositoryInterface):
        self._article_repository = article_repository

    async def get_articles_previews(self) -> ArticlesRepositoryInterface:
        return await self._article_repository.get_articles_previews()

    async def get_article(self, article_id: int) -> ArticlesRepositoryInterface|None:
        return await self._article_repository.get_article(article_id)

    async def create_article(self, article: dict) -> ArticlesRepositoryInterface:
        return await self._article_repository.create_article(article)

    async def update_article(self, article_id: int, article: dict) -> ArticlesRepositoryInterface:
        return await self._article_repository.update_article(article_id, article)

    async def delete_article(self, article_id: int) -> ArticlesRepositoryInterface:
        return await self._article_repository.delete_article(article_id)
