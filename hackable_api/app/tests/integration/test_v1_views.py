import pytest

from starlette.testclient import TestClient
from sqlalchemy import text

from app.app.application import get_app
from app.db.db_driver import DbDriver
from app.app.settings import settings

from app.services.auth_service import AuthService
from app.services.articles_service import ArticlesService
from app.db.repositories.articles_repository import ArticlesRepository
from app.db.repositories.users_repository import UsersRepository
from app.services.users_service import UsersService

app = get_app()
client = TestClient(app)


@pytest.mark.asyncio
async def test_user():
    """
    Helper function to create a test user in the database.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        # Reset table before each test
        await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        await session.commit()

        user_repository = UsersRepository(session)
        user = await UsersService(user_repository).create_user(
            {
                "username": "testuser",
                "password": "testpassword",
            }
        )
    return user


@pytest.mark.asyncio
async def test_article():
    """
    Helper function to create a test article in the database.
    """

    # Articles will be linked to user id 1
    async with DbDriver(settings.db_url).get_db_session() as session:
        # Reset table before each test
        await session.execute(text("TRUNCATE TABLE articles RESTART IDENTITY CASCADE;"))
        await session.commit()

        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).create_article(
            "Test Article Title", "Test article content", 0, 1
        )
    return article


@pytest.mark.asyncio
async def test_featured_article():
    """
    Helper function to create a featured test article in the database.
    """

    # Articles will be linked to user id 1
    async with DbDriver(settings.db_url).get_db_session() as session:
        # Reset table before each test
        await session.execute(text("TRUNCATE TABLE articles RESTART IDENTITY CASCADE;"))
        await session.commit()

        article_repository = ArticlesRepository(session)
        article = await ArticlesService(article_repository).create_article(
            "Test Featured Article Title", "Test featured article content", 1, 1
        )
    return article


@pytest.fixture(scope="module")
def token():
    """
    Fixture to create a mock access token.
    """
    # Mock the data to be encoded
    data = {"sub": "1", "exp": 3600}

    # Create the access token
    return AuthService.create_access_token(data, 60)


@pytest.mark.asyncio
async def test_get_articles_previews():
    """
    Test retrieving all article previews.
    """

    await test_user()
    await test_article()

    response = client.get("/api/v1/articles/previews/")

    assert response.status_code == 200
    response_data = response.json()
    assert "articles" in response_data
    assert isinstance(response_data["articles"], list)
    assert response_data["articles"][0]["title"] == "Test Article Title"


@pytest.mark.asyncio
async def test_get_featured_articles():
    """
    Test retrieving featured articles.
    """

    await test_user()
    await test_featured_article()

    response = client.get("/api/v1/articles/featured/")

    assert response.status_code == 200
    response_data = response.json()
    assert "articles" in response_data
    assert isinstance(response_data["articles"], list)
    assert response_data["articles"][0]["title"] == "Test Featured Article Title"
    assert response_data["articles"][0]["featured"] is True


@pytest.mark.asyncio
async def test_create_article_success(token):
    """
    Test creating an article successfully.
    """

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": "Test Article One",
        "content": "This is a test article.",
        "featured": False,
    }

    response = client.post("/api/v1/article/", json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["title"] == "Test Article One"
    assert response_data["content"] == "This is a test article."
    assert response_data["featured"] is False
