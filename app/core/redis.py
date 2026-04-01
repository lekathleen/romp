import json

import redis.asyncio as aioredis

from app.core.config import settings


def get_redis() -> aioredis.Redis:
    return aioredis.from_url(settings.redis_url, decode_responses=True)


async def publish_vote_update(trip_id: str, payload: dict) -> None:
    client = get_redis()
    await client.publish(f"trip:{trip_id}", json.dumps(payload))
    await client.aclose()
