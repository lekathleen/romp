import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.card import CardRepository
from app.repositories.image import ImageRepository
from app.repositories.trip import TripRepository
from app.schemas.card import CardCreate, CardImageResponse, CardResponse
from app.services.images import generate_presigned_upload_url
from app.services.scoring import apply_threshold

router = APIRouter()


@router.post("/trips/{trip_id}/cards", response_model=CardResponse)
async def create_card(
    trip_id: uuid.UUID,
    card_data: CardCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    trip = await TripRepository(db).get_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    created_by = request.client.host
    card = await CardRepository(db).create(trip_id, card_data, created_by)
    return card


@router.get("/trips/{trip_id}/cards", response_model=list[CardResponse])
async def list_cards(trip_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    trip = await TripRepository(db).get_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    rows = await CardRepository(db).get_all_with_scores(trip_id)
    cards = []
    for card, average_score, vote_count in rows:
        score_data = apply_threshold(average_score, trip.threshold_score)
        response = CardResponse.model_validate(card)
        response.average_score = score_data["average_score"]
        response.is_planned = score_data["is_planned"]
        cards.append(response)
    return cards


@router.get("/trips/{trip_id}/standings", response_model=list[CardResponse])
async def get_standings(trip_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    trip = await TripRepository(db).get_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    rows = await CardRepository(db).get_all_with_scores(trip_id)
    cards = []
    for card, average_score, vote_count in rows:
        score_data = apply_threshold(average_score, trip.threshold_score)
        response = CardResponse.model_validate(card)
        response.average_score = score_data["average_score"]
        response.is_planned = score_data["is_planned"]
        cards.append(response)
    return cards


@router.get("/trips/{trip_id}/planned", response_model=list[CardResponse])
async def get_planned(trip_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    trip = await TripRepository(db).get_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    rows = await CardRepository(db).get_all_with_scores(trip_id)
    cards = []
    for card, average_score, vote_count in rows:
        score_data = apply_threshold(average_score, trip.threshold_score)
        if score_data["is_planned"]:
            response = CardResponse.model_validate(card)
            response.average_score = score_data["average_score"]
            response.is_planned = True
            cards.append(response)
    return cards


@router.post("/trips/{trip_id}/cards/{card_id}/upload-url")
async def get_upload_url(
    trip_id: uuid.UUID,
    card_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    trip = await TripRepository(db).get_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    card = await CardRepository(db).get_by_id(card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    object_key = f"cards/{card_id}/{uuid.uuid4()}"
    url = generate_presigned_upload_url(object_key)
    return {"upload_url": url, "object_key": object_key}


@router.post(
    "/trips/{trip_id}/cards/{card_id}/images",
    response_model=CardImageResponse,
)
async def associate_image(
    trip_id: uuid.UUID,
    card_id: uuid.UUID,
    s3_key: str,
    is_thumbnail: bool = False,
    display_order: int = 0,
    db: AsyncSession = Depends(get_db),
):
    trip = await TripRepository(db).get_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    card = await CardRepository(db).get_by_id(card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    image = await ImageRepository(db).create(
        card_id, s3_key, is_thumbnail, display_order
    )
    return image
