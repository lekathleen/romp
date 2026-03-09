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


@pytest.fixture
async def member(client, trip):
    response = await client.post(
        f"/trips/{trip['id']}/join", json={"nickname": "MisoYuzu"}
    )
    return response.json()


@pytest.fixture
async def card(client, trip):
    response = await client.post(
        f"/trips/{trip['id']}/cards",
        json={
            "title": "Miffy Bakery",
            "location": "Kyoto",
        },
    )
    return response.json()


async def test_join_trip(client, trip):
    response = await client.post(f"/trips/{trip['id']}/join", json={"nickname": "Otto"})
    assert response.status_code == 201
    data = response.json()
    assert data["nickname"] == "Otto"
    assert "session_token" in data


async def test_join_trip_duplicate_nickname(client, trip, member):
    response = await client.post(
        f"/trips/{trip['id']}/join", json={"nickname": "MisoYuzu"}
    )
    assert response.status_code == 409


async def test_vote_on_card(client, trip, member, card):
    response = await client.post(
        f"/trips/{trip['id']}/cards/{card['id']}/vote",
        json={"score": 1},
        headers={"X-Session-Token": member["session_token"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 1


async def test_vote_upsert(client, trip, member, card):
    headers = {"X-Session-Token": member["session_token"]}
    await client.post(
        f"/trips/{trip['id']}/cards/{card['id']}/vote",
        json={"score": 1},
        headers=headers,
    )
    response = await client.post(
        f"/trips/{trip['id']}/cards/{card['id']}/vote",
        json={"score": 3},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["score"] == 3


async def test_vote_without_session_token(client, trip, card):
    response = await client.post(
        f"/trips/{trip['id']}/cards/{card['id']}/vote",
        json={"score": 2},
    )
    assert response.status_code == 401


async def test_standings(client, trip, member, card):
    await client.post(
        f"/trips/{trip['id']}/cards/{card['id']}/vote",
        json={"score": 1},
        headers={"X-Session-Token": member["session_token"]},
    )
    response = await client.get(f"/trips/{trip['id']}/standings")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["average_score"] is not None


async def test_planned(client, trip, member, card):
    await client.post(
        f"/trips/{trip['id']}/cards/{card['id']}/vote",
        json={"score": 1},
        headers={"X-Session-Token": member["session_token"]},
    )
    response = await client.get(f"/trips/{trip['id']}/planned")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["is_planned"] is True
