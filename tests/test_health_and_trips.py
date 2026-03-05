"""
Verify basic routing and response shapes.
Uses FastAPI's TestClient which runs the app in-process (no real server needed).
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_health_check_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert data["database"] == "unchecked"
    assert data["redis"] == "unchecked"


def test_list_trips_returns_list():
    response = client.get("/trips")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_trip_has_expected_fields():
    response = client.get("/trips")
    trip = response.json()[0]
    assert "id" in trip
    assert "name" in trip
    assert "destinations" in trip
    assert "threshold_score" in trip
    assert isinstance(trip["destinations"], list)
