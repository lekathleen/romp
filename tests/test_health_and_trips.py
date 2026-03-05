import pytest


def test_root_returns_200():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check_returns_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert "version" in data


@pytest.mark.asyncio
async def test_create_trip(client):
    response = await client.post(
        "/trips",
        json={"name": "Test Trip", "description": "A test", "destinations": ["Tokyo"]},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Trip"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_trips_returns_list(client):
    response = await client.get("/trips")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_trip_not_found(client):
    response = await client.get("/trips/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
