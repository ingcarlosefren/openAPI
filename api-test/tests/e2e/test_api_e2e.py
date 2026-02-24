from uuid import uuid4

from fastapi.testclient import TestClient

from src.app.main import app


client = TestClient(app)


def test_health_endpoint_returns_200() -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.text == ""


def test_users_and_articles_flow() -> None:
    unique_email = f"test-{uuid4()}@example.com"

    create_user = client.post(
        "/v1/users",
        json={
            "name": "Test User",
            "email": unique_email,
            "birthDate": "1990-01-01",
        },
    )
    assert create_user.status_code == 201
    user_id = create_user.json()["id"]

    create_article = client.post(
        "/v1/articles",
        json={
            "title": "Article title",
            "content": "Article content",
            "author": user_id,
            "category": "PROGRAMMING",
            "rating": 4.5,
        },
    )
    assert create_article.status_code == 201
    article_id = create_article.json()["id"]

    by_id = client.get(f"/v1/articles/{article_id}")
    assert by_id.status_code == 200

    by_user = client.get(f"/v1/users/{user_id}/articles")
    assert by_user.status_code == 200
    assert len(by_user.json()["data"]) >= 1


def test_error_payload_for_not_found_user_articles() -> None:
    response = client.get(f"/v1/users/{uuid4()}/articles")
    assert response.status_code == 404
    payload = response.json()
    assert payload["code"] == "NOT_FOUND"
    assert "message" in payload
    assert "details" in payload
