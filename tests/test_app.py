"""Basic smoke tests for the SkyBook Flask app."""

from app import create_app


def test_index_returns_200():
    client = create_app().test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_health_check():
    client = create_app().test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
