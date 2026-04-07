import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import CardImage


class ImageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        card_id: uuid.UUID,
        s3_key: str,
        is_thumbnail: bool = False,
        display_order: int = 0,
    ) -> CardImage:
        image = CardImage(
            card_id=card_id,
            s3_key=s3_key,
            is_thumbnail=is_thumbnail,
            display_order=display_order,
        )
        self.db.add(image)
        await self.db.commit()
        await self.db.refresh(image)
        return image

    async def get_by_card(self, card_id: uuid.UUID) -> list[CardImage]:
        result = await self.db.execute(
            select(CardImage).where(CardImage.card_id == card_id)
        )
        return list(result.scalars().all())
