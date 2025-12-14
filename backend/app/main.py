# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.v1 import news, favorites, broadcast, admin

from app.models.db import init_db


# Load environment settings
settings = get_settings()


# -------------------------------------------------------------
# FastAPI Application Initialization
# -------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI News Aggregation & Broadcasting Dashboard Backend"
)


# -------------------------------------------------------------
# Middleware (CORS for frontend → backend communication)
# -------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# Event Hooks
# -------------------------------------------------------------
@app.on_event("startup")
async def startup():
    """
    This runs when the FastAPI app starts.
    Useful for initializing:
    - Model loading
    - Connections
    - Pre-warming caches
    """
    print(" FastAPI backend started successfully!")
    init_db() 


@app.on_event("shutdown")
async def shutdown():
    """
    This runs when the app is shutting down.
    Useful for:
    - Cleaning connections
    - Releasing resources
    """
    print(" FastAPI backend shutdown.")


# -------------------------------------------------------------
# Router Registration
# -------------------------------------------------------------
app.include_router(news.router, prefix="/api/v1/news", tags=["News"])
app.include_router(favorites.router, prefix="/api/v1/favorites", tags=["Favorites"])
app.include_router(broadcast.router, prefix="/api/v1/broadcast", tags=["Broadcast"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


# -------------------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "env": settings.APP_ENV}
