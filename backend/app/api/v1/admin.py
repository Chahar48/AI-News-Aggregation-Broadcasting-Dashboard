# backend/app/api/v1/admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.db import get_db
from app.models import schemas

router = APIRouter()


# ---------------------------------------------------------
# GET /admin/sources  → List all news sources
# ---------------------------------------------------------
@router.get("/sources")
def get_sources(
    db: Session = Depends(get_db)
):
    return {
        "total": 0,
        "sources": []
    }


# ---------------------------------------------------------
# POST /admin/sources/refresh  → Refresh only sources table
# ---------------------------------------------------------
@router.post("/sources/refresh")
def refresh_sources(
    db: Session = Depends(get_db)
):
    return {"message": "Sources refreshed (placeholder)."}
