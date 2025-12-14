# backend/app/api/v1/favorites.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.db import get_db
from app.models.orm_models import Favorite, NewsItem
from app.models import schemas

router = APIRouter()


# ---------------------------------------------------------
# GET /favorites → List all favorite news items
# ---------------------------------------------------------
@router.get("/", response_model=list[schemas.FavoriteResponse])
def get_favorites(db: Session = Depends(get_db)):
    favorites = db.query(Favorite).order_by(Favorite.created_at.desc()).all()
    return favorites


# ---------------------------------------------------------
# POST /favorites → Add a news item to favorites
# ---------------------------------------------------------
@router.post("/", response_model=schemas.FavoriteResponse)
def add_favorite(
    favorite: schemas.FavoriteCreate,
    db: Session = Depends(get_db),
):
    # Ensure the news item exists
    news_item = db.query(NewsItem).filter(NewsItem.id == favorite.news_item_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News item not found")

    # Prevent duplicate favorites
    existing_favorite = (
        db.query(Favorite)
        .filter(Favorite.news_item_id == favorite.news_item_id)
        .first()
    )
    if existing_favorite:
        raise HTTPException(status_code=400, detail="Already in favorites")

    new_fav = Favorite(news_item_id=favorite.news_item_id)

    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)

    return new_fav


# ---------------------------------------------------------
# DELETE /favorites/{id} → Remove favorite
# ---------------------------------------------------------
@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()

    return {"message": "Favorite removed successfully"}