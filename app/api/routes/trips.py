from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

from app.schemas.trip import TripResponse

router = APIRouter(prefix="/trips", tags=["trips"])

# Hardcoded data for testing
_FAKE_TRIPS: list[dict] = [
    {
        "id": uuid4(),
        "name": "Asia 2025",
        "description": "Japan, Vietnam, Thailand — 3 weeks",
        "destinations": ["Tokyo", "Hanoi", "Bangkok"],
        "threshold_score": 2.0,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "id": uuid4(),
        "name": "Portugal Trip",
        "description": "Lisbon and Porto food tour",
        "destinations": ["Lisbon", "Porto"],
        "threshold_score": 2.0,
        "created_at": datetime.now(timezone.utc),
    },
]


@router.get("", response_model=list[TripResponse])
async def list_trips() -> list[dict]:
    """
    Returns list all trips.
    """
    return _FAKE_TRIPS


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: str) -> dict:
    """
    Get a single trip by ID.
    FastAPI will automatically return 422 if trip_id isn't a valid UUID format.
    """
    return _FAKE_TRIPS[0]
