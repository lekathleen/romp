from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.redis import get_redis

router = APIRouter()


@router.websocket("/ws/{trip_id}")
async def trip_websocket(websocket: WebSocket, trip_id: str):
    await websocket.accept()

    client = get_redis()
    pubsub = client.pubsub()
    await pubsub.subscribe(f"trip:{trip_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            await websocket.send_text(message["data"])

    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(f"trip:{trip_id}")
        await client.aclose()
