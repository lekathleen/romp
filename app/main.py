from fastapi import FastAPI

from app.api.routes import cards, health, trips, votes
from app.core.config import settings

# Swagger UI available at /docs, ReDoc at /redoc
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Social group travel planning and voting app",
)

app.include_router(health.router)
app.include_router(trips.router)
app.include_router(cards.router)
app.include_router(votes.router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": f"Welcome to {settings.app_name}. See /docs for the API."}
