# backend/app/services/normalizer.py

"""
Normalizer converts parsed items into a unified schema.
This is the FINAL structure before deduplication.
"""

from typing import List, Dict
from datetime import datetime, timezone
from dateutil import parser as date_parser


def normalize_datetime(value) -> datetime | None:
    if not value:
        return None
    try:
        dt = date_parser.parse(value)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def normalize_items(parsed_items: List[Dict]) -> List[Dict]:
    """
    Output strictly matches NewsItemCreate expectations.
    """

    normalized: List[Dict] = []

    for item in parsed_items:
        title = item.get("title")
        url = item.get("url")

        # Mandatory fields
        if not title or not url:
            continue

        normalized.append({
            "source_name": item.get("source_name"),
            "source_url": item.get("source_url"),  # 🔥 ADD THIS
            "title": title.strip(),
            "summary": item.get("content"),
            "author": item.get("author"),
            "url": url,
            "published_at": normalize_datetime(item.get("published_at")),
            "content": item.get("content"),
            "tags": None,
            "raw": item.get("raw"),
        })

    return normalized