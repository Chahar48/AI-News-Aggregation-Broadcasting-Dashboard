# backend/app/tasks/jobs.py

"""
Ingestion jobs.

Reusable ingestion logic triggered by:
- API refresh
- Background worker
"""

import logging
from sqlalchemy.orm import Session

from app.models.db import SessionLocal
from app.services.ingestion.fetcher import fetch_all_sources
from app.services.ingestion.parsers import parse_raw_items
from app.services.normalizer import normalize_items
from app.services.deduper import is_duplicate
from app.services.summarizer import summarize_news_item
from app.models.orm_models import NewsItem

logger = logging.getLogger(__name__)


def run_news_ingestion_job():
    logger.info(" Starting ingestion job")

    db: Session = SessionLocal()

    try:
        raw_items = fetch_all_sources()
        parsed_items = parse_raw_items(raw_items)
        normalized_items = normalize_items(parsed_items)

        inserted, skipped = 0, 0

        for item in normalized_items:
            if is_duplicate(db, item["title"], item["url"]):
                skipped += 1
                continue

            summary = summarize_news_item(
                title=item["title"],
                content=item.get("content")
            )

            news = NewsItem(
                source_name=item.get("source_name"),
                title=item["title"],
                summary=summary,
                author=item.get("author"),
                url=item["url"],
                published_at=item.get("published_at"),
                content=item.get("content"),
                is_duplicate=False,
            )

            db.add(news)
            inserted += 1

        db.commit()
        logger.info(f" Inserted={inserted}, Skipped={skipped}")

    except Exception as e:
        db.rollback()
        logger.exception(" Ingestion failed", exc_info=e)

    finally:
        db.close()
