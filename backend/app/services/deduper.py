# backend/app/services/deduper.py

"""
Deduplication logic for news ingestion.

MVP rules:
1. URL-based deduplication (mandatory)
2. Title similarity deduplication (mandatory)
3. ONLY compare against DB (never within the same batch)
"""

from difflib import SequenceMatcher
from sqlalchemy.orm import Session
from app.models.orm_models import NewsItem


# ----------------------------------------
# Helper: title similarity
# ----------------------------------------
def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# ----------------------------------------
# Main dedup function
# ----------------------------------------
def check_duplicate(
    db: Session,
    title: str,
    url: str,
) -> tuple[bool, int | None]:
    """
    Returns:
        (is_duplicate, duplicate_of_id)
    """

    # -------------------------
    # 1. URL-based dedup
    # -------------------------
    existing_by_url = (
        db.query(NewsItem)
        .filter(NewsItem.url == url)
        .first()
    )

    if existing_by_url:
        return True, existing_by_url.id

    # -------------------------
    # 2. Title similarity dedup
    # -------------------------
    existing_titles = (
        db.query(NewsItem.id, NewsItem.title)
        .all()
    )

    for item_id, existing_title in existing_titles:
        if not existing_title:
            continue

        similarity = title_similarity(title, existing_title)

        # Strict threshold (prevents over-dedup)
        if similarity >= 0.90:
            return True, item_id

    # -------------------------
    # Not a duplicate
    # -------------------------
    return False, None