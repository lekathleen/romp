import uuid

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.card import CardRepository
from app.repositories.member import MemberRepository
from app.repositories.trip import TripRepository
from app.repositories.vote import VoteRepository
from app.schemas.vote import VoteCreate, VoteResponse

router = APIRouter()


# Reusable dependency that validates the session token and returns the member.
async def get_current_member(
    x_session_token: uuid.UUID | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    if x_session_token is None:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    member = await MemberRepository(db).get_by_session_token(x_session_token)
    if member is None:
        raise HTTPException(status_code=401, detail="Invalid or missing session token")
    return member


@router.post("/trips/{trip_id}/cards/{card_id}/vote", response_model=VoteResponse)
async def vote_on_card(
    trip_id: uuid.UUID,
    card_id: uuid.UUID,
    vote_data: VoteCreate,
    db: AsyncSession = Depends(get_db),
    member=Depends(get_current_member),
):
    trip = await TripRepository(db).get_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    card = await CardRepository(db).get_by_id(card_id)
    if card is None or card.trip_id != trip_id:
        raise HTTPException(status_code=404, detail="Card not found")

    return await VoteRepository(db).upsert(card_id, member.id, vote_data.score)
