from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.redis import get_redis

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    redis: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    db_status = "error"
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            db_status = "ok"
    except Exception:
        db_status = "error"
    try:
        redis_client = get_redis()
        await redis_client.ping()
        await redis_client.aclose()
        redis_status = "ok"
    except Exception:
        redis_status = "error"

    return HealthResponse(
        status="ok" if db_status == "ok" else "degraded",
        version=settings.version,
        database=db_status,
        redis=redis_status,
    )
