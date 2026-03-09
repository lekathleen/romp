import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip import TripMember


class MemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, trip_id: uuid.UUID, nickname: str) -> TripMember:
        member = TripMember(trip_id=trip_id, nickname=nickname)
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def get_by_session_token(self, token: uuid.UUID) -> TripMember | None:
        result = await self.db.execute(
            select(TripMember).where(TripMember.session_token == token)
        )
        return result.scalar_one_or_none()

    async def get_by_nickname(
        self, trip_id: uuid.UUID, nickname: str
    ) -> TripMember | None:
        result = await self.db.execute(
            select(TripMember).where(
                TripMember.trip_id == trip_id,
                TripMember.nickname == nickname,
            )
        )
        return result.scalar_one_or_none()
