from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import trips, health

# Swagger UI available at /docs, ReDoc at /redoc
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Social group travel planning and voting app",
)

# Register routers
app.include_router(health.router)
app.include_router(trips.router)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": f"Welcome to {settings.app_name}. See /docs for the API."}
