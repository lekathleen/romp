import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Vote


class VoteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(
        self, card_id: uuid.UUID, member_id: uuid.UUID, score: int
    ) -> Vote:
        # Members can change their vote, so update the vote if one already exists.
        result = await self.db.execute(
            select(Vote).where(Vote.card_id == card_id, Vote.member_id == member_id)
        )
        vote = result.scalar_one_or_none()

        if vote is None:
            vote = Vote(card_id=card_id, member_id=member_id, score=score)
            self.db.add(vote)
        else:
            vote.score = score

        await self.db.commit()
        await self.db.refresh(vote)
        return vote

    async def get_by_card(self, card_id: uuid.UUID) -> list[Vote]:
        result = await self.db.execute(select(Vote).where(Vote.card_id == card_id))
        return list(result.scalars().all())
