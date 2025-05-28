from starlette.testclient import TestClient

from app.app.application import get_app

app = get_app()
client = TestClient(app)


def test_health_check():
    response = client.get("/api/health/")
    assert response.status_code == 200
