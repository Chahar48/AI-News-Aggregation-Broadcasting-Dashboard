# backend/app/api/v1/broadcast.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.db import get_db
from app.models.orm_models import Favorite, BroadcastLog
from app.models import schemas
from app.services.broadcaster import broadcaster


router = APIRouter()


# ---------------------------------------------------------
# POST /broadcast → Trigger broadcast for a favorite item
# ---------------------------------------------------------
#@router.post("/", response_model=schemas.BroadcastLogResponse)
@router.post("/", response_model=schemas.BroadcastResponse)
def broadcast_favorite(
    payload: schemas.BroadcastRequest,
    db: Session = Depends(get_db)
):
    """
    Broadcast a favorite news item via:
    - email
    - whatsapp
    - linkedin
    - blog
    - newsletter
    """

    # Step 1: Validate favorite exists
    favorite = (
        db.query(Favorite)
        .filter(Favorite.id == payload.favorite_id)
        .first()
    )

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    news = favorite.news_item
    if not news:
        raise HTTPException(status_code=404, detail="Linked news item not found")

    # Step 2: Determine message to broadcast
    text_to_send = payload.message_override or news.summary or news.title

    # Step 3: Choose broadcast platform
    platform = payload.platform.lower()

    if platform == "email":
        result = broadcaster.send_email(
            to_email=payload.to_email or "example@example.com",
            subject=news.title,
            content=text_to_send
        )

    elif platform == "whatsapp":
        result = broadcaster.send_whatsapp(
            message=text_to_send
        )

    elif platform == "linkedin":
        result = broadcaster.post_linkedin(
            news_title=news.title,
            ml_summary=news.summary
        )

    elif platform == "blog":
        result = broadcaster.generate_blog_markdown(
            news_title=news.title,
            summary=news.summary,
            url=news.url
        )

    elif platform == "newsletter":
        result = broadcaster.generate_newsletter_item(
            news_title=news.title,
            summary=news.summary,
            url=news.url
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid broadcast platform")

    # Step 4: Log broadcast
    log = BroadcastLog(
        favorite_id=favorite.id,
        platform=platform,
        status="sent",
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    # return {
    #     "favorite_id": favorite.id,
    #     "platform": platform,
    #     "result": result,
    #     "log_id": log.id,
    #     "timestamp": log.timestamp
    # }
    return {
        "id": log.id,
        "status": log.status,
        "message_preview": text_to_send[:200],
        "timestamp": log.timestamp,
    }


# ---------------------------------------------------------
# GET /broadcast/logs → Retrieve broadcast history
# ---------------------------------------------------------
# @router.get("/logs", response_model=list[schemas.BroadcastLogResponse])
# def list_broadcast_logs(db: Session = Depends(get_db)):
#     logs = db.query(BroadcastLog).order_by(BroadcastLog.timestamp.desc()).all()
#     return logs


