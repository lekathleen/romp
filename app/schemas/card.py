import uuid
from datetime import datetime

from pydantic import BaseModel


class CardBase(BaseModel):
    title: str
    description: str | None = None
    tags: list[str] = []
    location: str | None = None
    price_range: str | None = None


class CardCreate(CardBase):
    pass


class CardResponse(CardBase):
    id: uuid.UUID
    trip_id: uuid.UUID
    created_by: str | None
    created_at: datetime
    average_score: float | None = None
    is_planned: bool = False

    model_config = {"from_attributes": True}
