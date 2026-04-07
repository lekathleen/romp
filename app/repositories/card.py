import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.card import Card, Vote
from app.schemas.card import CardCreate


class CardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, trip_id: int, card_data: CardCreate, created_by: str
    ) -> Card:
        card = Card(
            trip_id=trip_id,
            created_by=created_by,
            **card_data.model_dump(),
        )
        self.db.add(card)
        await self.db.commit()

        result = await self.db.execute(
            select(Card).options(selectinload(Card.images)).where(Card.id == card.id)
        )
        return result.scalar_one()

    async def get_all_with_scores(self, trip_id: int) -> list[dict]:
        result = await self.db.execute(
            select(
                Card,
                func.avg(Vote.score).label("average_score"),
                func.count(Vote.id).label("vote_count"),
            )
            .outerjoin(Vote, Vote.card_id == Card.id)
            .where(Card.trip_id == trip_id)
            .group_by(Card.id)
            .order_by(func.avg(Vote.score).asc().nulls_last())
            .options(selectinload(Card.images))
        )
        return result.all()

    async def get_by_id(self, card_id: uuid.UUID) -> Card | None:
        result = await self.db.execute(
            select(Card).options(selectinload(Card.images)).where(Card.id == card_id)
        )
        return result.scalar_one_or_none()
