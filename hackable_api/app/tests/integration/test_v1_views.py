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
from app.services.articles_comments_service import ArticlesCommentsService
from app.db.repositories.articles_comments_repository import ArticlesCommentsRepository

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


@pytest.mark.asyncio
async def test_article_comments():
    """
    Helper function to create a test comment for an article.
    """

    async with DbDriver(settings.db_url).get_db_session() as session:
        # Reset table before each test
        await session.execute(text("TRUNCATE TABLE articles_comments RESTART IDENTITY CASCADE;"))
        await session.commit()

        article_repository = ArticlesCommentsRepository(session)

        await ArticlesCommentsService(article_repository).create_article_comment(
            "This is a test comment.", 1, 1
        )
        await ArticlesCommentsService(article_repository).create_article_comment(
            "This is another test comment.", 1, 1
        )
        await ArticlesCommentsService(article_repository).create_article_comment(
            "This is a third test comment.", 1, 1
        )


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


@pytest.mark.asyncio
async def test_get_article_success():
    """
    Test retrieving a single article by ID.
    """

    await test_user()
    await test_article()

    response = client.get("/api/v1/article/1/")

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] == 1
    assert response_data["title"] == "Test Article Title"


@pytest.mark.asyncio
async def test_get_article_comments():
    """
    Test retrieving comments for an article.
    """

    await test_user()
    await test_article()
    await test_article_comments()

    article_id = 1
    offset = 0

    response = client.get(f"/api/v1/article/{article_id}/comments/{offset}/")

    assert response.status_code == 200
    response_data = response.json()
    assert "comments" in response_data
    assert isinstance(response_data["comments"], list)
    assert len(response_data["comments"]) == 3


@pytest.mark.asyncio
async def test_get_article_comments_with_offset():
    """
    Test retrieving comments for an article.
    """

    await test_user()
    await test_article()
    await test_article_comments()

    article_id = 1
    offset = 2

    response = client.get(f"/api/v1/article/{article_id}/comments/{offset}/")

    assert response.status_code == 200
    response_data = response.json()
    assert "comments" in response_data
    assert isinstance(response_data["comments"], list)
    assert len(response_data["comments"]) == 1


@pytest.mark.asyncio
async def test_create_comment_success(token):
    """
    Test creating a comment successfully.
    """

    await test_user()
    await test_article()

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "comment": "This is a test comment.",
        "article_id": 1
    }

    response = client.post("/api/v1/comment/", json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["comment"] == "This is a test comment."
    assert response_data["article_id"] == 1


@pytest.mark.asyncio
async def test_delete_article_success():
    """
    Test deleting an article successfully.
    """

    await test_user()
    await test_article()

    article_id = 1

    response = client.delete(f"/api/v1/article/{article_id}/")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Ok"


@pytest.mark.asyncio
async def test_get_user_articles(token):
    """
    Test retrieving all articles for a user.
    """

    await test_user()
    await test_article()

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/user/articles/", headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "articles" in response_data
    assert isinstance(response_data["articles"], list)
    assert response_data["articles"][0]["title"] == "Test Article Title"


@pytest.mark.asyncio
async def test_get_user_comments(token):
    """
    Test retrieving all comments by a user.
    """

    await test_user()
    await test_article()
    await test_article_comments()

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/user/comments/", headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "comments" in response_data
    assert isinstance(response_data["comments"], list)
    assert response_data["comments"][0]["comment"] == "This is a test comment."
