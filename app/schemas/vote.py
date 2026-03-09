import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class VoteCreate(BaseModel):
    score: int = Field(..., ge=1, le=4)


class VoteResponse(BaseModel):
    id: uuid.UUID
    card_id: uuid.UUID
    member_id: uuid.UUID
    score: int
    voted_at: datetime

    model_config = {"from_attributes": True}
