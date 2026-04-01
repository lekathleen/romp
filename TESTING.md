# Testing

## Automated Tests

Run the full test suite with coverage:
```bash
make test
```

Or directly:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Coverage threshold is 70%. The test suite covers:

- Scoring logic (unit tests, parametrized)
- Trip, card, and vote endpoints (integration tests against a real test DB)
- WebSocket connection acceptance and Redis pub/sub channel correctness
- Health check endpoint

## Manual: Vote -> Redis -> WebSocket Broadcast

The end-to-end flow (vote submitted -> published to Redis -> broadcast to
connected WebSocket clients) is verified manually against the running stack.

**Setup:**
```bash
docker compose up --build
```

**Steps:**

1. Create a trip:
```bash
curl -s -X POST http://localhost:8000/trips \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Trip", "description": "manual test", "destinations": ["Tokyo"]}' | jq .
```
Copy the trip `id`.

2. Join the trip:
```bash
curl -s -X POST http://localhost:8000/trips/{trip_id}/join \
  -H "Content-Type: application/json" \
  -d '{"nickname": "tester"}' | jq .
```
Copy the `session_token`.

3. Add a card:
```bash
curl -s -X POST http://localhost:8000/trips/{trip_id}/cards \
  -H "Content-Type: application/json" \
  -H "X-Session-Token: {session_token}" \
  -d '{"title": "Senso-ji Temple", "description": "Famous temple", "tags": ["Nature"], "location": "Tokyo", "price_range": "$"}' | jq .
```
Copy the card `id`.

4. Open Chrome devtools (Cmd+Option+J) and connect a WebSocket listener:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/{trip_id}');
ws.onmessage = (e) => console.log(e.data);
```

5. Submit a vote:
```bash
curl -s -X POST http://localhost:8000/trips/{trip_id}/cards/{card_id}/vote \
  -H "Content-Type: application/json" \
  -H "X-Session-Token: {session_token}" \
  -d '{"score": 1}' | jq .
```

**Expected result:** The browser console receives:
```json
{"event": "vote_update", "card_id": "{card_id}", "trip_id": "{trip_id}"}
```

This confirms the full pub/sub broadcast path is working.