"""WebSocket tests.

The vote -> Redis -> WebSocket broadcast flow is verified manually with
the running stack. See TESTING.md for instructions.
"""

import json

import redis
from fastapi.testclient import TestClient


def test_websocket_accepts_connection(sync_client: TestClient, test_trip):
    trip_id = test_trip["id"]
    with sync_client.websocket_connect(f"/ws/{trip_id}") as ws:
        assert ws is not None


def test_publish_vote_update_runs(test_trip):
    trip_id = test_trip["id"]
    r = redis.from_url("redis://localhost:6379", decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe(f"trip:{trip_id}")

    pubsub.get_message(timeout=1)

    payload = {"event": "vote_update", "card_id": "abc", "trip_id": trip_id}
    r.publish(f"trip:{trip_id}", json.dumps(payload))

    msg = pubsub.get_message(timeout=1)
    assert msg is not None
    assert msg["type"] == "message"
    data = json.loads(msg["data"])
    assert data["event"] == "vote_update"
    assert data["trip_id"] == trip_id

    pubsub.unsubscribe()
    r.close()
