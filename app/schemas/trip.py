from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TripBase(BaseModel):
    name: str
    description: str | None = None
    destinations: list[str] = []


class TripCreate(TripBase):
    """Schema for POST /trips request body."""

    pass


class TripResponse(TripBase):
    """Schema for API responses."""

    id: UUID
    threshold_score: float
    created_at: datetime

    model_config = {"from_attributes": True}
