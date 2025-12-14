# backend/app/api/v1/news.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.db import get_db
from app.models.orm_models import Source
from app.models.orm_models import NewsItem
from app.models import schemas

from app.services.ingestion.fetcher import fetch_all_sources
from app.services.ingestion.fetcher import NEWS_SOURCES
from app.services.ingestion.parsers import parse_raw_items
from app.services.normalizer import normalize_items
from app.services.deduper import check_duplicate
from app.services.ingestion.seed_data import get_seed_news

router = APIRouter()

def ensure_sources_exist(db: Session) -> dict[str, int]:
    """
    Ensures sources exist and returns a map: source_url -> source_id
    """
    existing = {s.url: s.id for s in db.query(Source).all()}

    for src in NEWS_SOURCES:
        if src["url"] not in existing:
            new = Source(
                name=src["name"],
                url=src["url"],
                type=src["type"],
                active=True,
            )
            db.add(new)
            db.flush()  # 🔥 get ID immediately
            existing[new.url] = new.id

    db.commit()
    return existing


# ---------------------------------------------------------
# GET /api/v1/news — Paginated news feed
# ---------------------------------------------------------
@router.get("/", response_model=schemas.PaginatedNewsResponse)
def get_news(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit

    total = db.query(NewsItem).count()

    items = (
        db.query(NewsItem)
        .order_by(NewsItem.published_at.desc().nullslast())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items,
    }


# ---------------------------------------------------------
# POST /api/v1/news/refresh — SAFE INGESTION PIPELINE
# ---------------------------------------------------------
@router.post("/refresh")
def refresh_news(db: Session = Depends(get_db)):

    # 1️⃣ Ensure sources exist
    source_map = ensure_sources_exist(db)

    # 2️⃣ Fetch
    # raw_items = fetch_all_sources()
    # if not raw_items:
    #     return {"inserted": 0, "duplicates": 0}
    # 2️⃣ Fetch (MODE SWITCH)
    USE_SEED_DATA = True  # 🔥 MVP DEMO MODE — set False for live RSS

    if USE_SEED_DATA:
        seed_items = get_seed_news()
        raw_items = []

        for item in seed_items:
            raw_items.append({
                "source_name": item["source_name"],
                "source_url": item["url"],  # IMPORTANT: used for source_id mapping
                "parser_key": "rss_generic",
                "title": item["title"],
                "url": item["url"],
                "author": item.get("author"),
                "published_at": item.get("published_at"),
                "summary": item.get("content"),
                "raw": item,
                "fetched_at": item.get("published_at"),
            })
    else:
        raw_items = fetch_all_sources()

    if not raw_items:
        return {"inserted": 0, "duplicates": 0}

    # 3️⃣ Parse + normalize
    parsed = parse_raw_items(raw_items)
    items = normalize_items(parsed)

    inserted = 0
    duplicates = 0

    for item in items:
        source_url = item.get("source_url")

        # HARD GUARD (prevents NULL FK forever)
        source_id = source_map.get(source_url)
        if not source_id:
            continue

        is_dup, _ = check_duplicate(
            db=db,
            title=item["title"],
            url=item["url"],
        )
        if is_dup:
            duplicates += 1
            continue

        news = NewsItem(
            source_id=source_id,
            title=item["title"],
            summary=item["content"][:500] if item.get("content") else None,
            author=item.get("author"),
            url=item["url"],
            published_at=item.get("published_at"),
            content=item.get("content"),
            is_duplicate=False,
        )

        db.add(news)
        inserted += 1

    db.commit()

    return {
        "inserted": inserted,
        "duplicates": duplicates,
        "message": "Ingestion completed",
    }
