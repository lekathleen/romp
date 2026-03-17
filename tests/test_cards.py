import pytest


@pytest.fixture
async def trip(client):
    response = await client.post(
        "/trips",
        json={
            "name": "Japan Trip",
            "description": "Two weeks in Japan",
            "destinations": ["Tokyo", "Kyoto"],
        },
    )
    return response.json()


async def test_create_card(client, trip):
    response = await client.post(
        f"/trips/{trip['id']}/cards",
        json={
            "title": "Miffy Bakery",
            "description": "Miffy themed bakery",
            "tags": ["cafes"],
            "location": "Kyoto",
            "price_range": "$",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Miffy Bakery"
    assert data["trip_id"] == trip["id"]
    assert data["average_score"] is None
    assert data["is_planned"] is False


async def test_create_card_trip_not_found(client):
    response = await client.post(
        "/trips/00000000-0000-0000-0000-000000000000/cards",
        json={"title": "Ghost Card"},
    )
    assert response.status_code == 404


async def test_list_cards(client, trip):
    await client.post(f"/trips/{trip['id']}/cards", json={"title": "Nishiki Market"})
    response = await client.get(f"/trips/{trip['id']}/cards")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "average_score" in data[0]
    assert "is_planned" in data[0]


async def test_list_cards_trip_not_found(client):
    response = await client.get("/trips/00000000-0000-0000-0000-000000000000/cards")
    assert response.status_code == 404


async def test_get_standings(client, test_trip, test_card):
    response = await client.get(f"/trips/{test_trip['id']}/standings")
    print("\nDEBUG status:", response.status_code)
    print("DEBUG body:", response.json())
    assert response.status_code == 200


async def test_get_standings_trip_not_found(client):
    response = await client.get("/trips/00000000-0000-0000-0000-000000000000/standings")
    assert response.status_code == 404


async def test_get_planned_empty(client, test_trip, test_card):
    # No votes cast — nothing crosses the threshold yet
    response = await client.get(f"/trips/{test_trip['id']}/planned")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_planned_trip_not_found(client):
    response = await client.get("/trips/00000000-0000-0000-0000-000000000000/planned")
    assert response.status_code == 404