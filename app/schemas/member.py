import uuid

from pydantic import BaseModel


class JoinTripRequest(BaseModel):
    nickname: str


class MemberResponse(BaseModel):
    id: uuid.UUID
    trip_id: uuid.UUID
    nickname: str
    session_token: uuid.UUID

    model_config = {"from_attributes": True}
