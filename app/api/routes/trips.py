import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.trip import TripRepository
from app.schemas.trip import TripCreate, TripResponse

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("", response_model=list[TripResponse])
async def list_trips(db: AsyncSession = Depends(get_db)) -> list:
    repo = TripRepository(db)
    return await repo.get_all()


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    repo = TripRepository(db)
    trip = await repo.get_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post("", response_model=TripResponse, status_code=201)
async def create_trip(body: TripCreate, db: AsyncSession = Depends(get_db)):
    repo = TripRepository(db)
    return await repo.create(
        name=body.name,
        description=body.description,
        destinations=body.destinations,
    )
