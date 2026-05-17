from fastapi.testclient import TestClient
from app.main import app

def test_list_games_returns_200():
    with TestClient(app) as client:
        response = client.get("/v1/games")
        assert response.status_code == 200
        assert isinstance(response.json(), list)