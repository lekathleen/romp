import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip import Trip


class TripRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Trip]:
        result = await self.session.execute(select(Trip))
        return list(result.scalars().all())

    async def get_by_id(self, trip_id: uuid.UUID) -> Trip | None:
        result = await self.session.execute(select(Trip).where(Trip.id == trip_id))
        return result.scalar_one_or_none()

    async def create(
        self, name: str, description: str | None, destinations: list[str]
    ) -> Trip:
        trip = Trip(name=name, description=description, destinations=destinations)
        self.session.add(trip)
        await self.session.flush()
        await self.session.refresh(trip)
        return trip
