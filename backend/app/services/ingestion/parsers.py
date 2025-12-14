# backend/app/services/ingestion/parsers.py

from typing import Dict, List, Optional
import re
from bs4 import BeautifulSoup


# ----------------------------------------------------
# Utility
# ----------------------------------------------------

def strip_html(text: Optional[str]) -> str:
    """
    Remove HTML tags, normalize whitespace.
    ALWAYS returns a string (never None).
    """
    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")
    clean = soup.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", clean).strip()


def safe_content(*candidates: Optional[str]) -> str:
    """
    Pick the first non-empty text candidate.
    Final fallback is empty string.
    """
    for c in candidates:
        cleaned = strip_html(c)
        if cleaned:
            return cleaned
    return ""


# ----------------------------------------------------
# Individual parsers
# ----------------------------------------------------

def parse_rss_generic(item: Dict) -> Dict:
    """
    Generic RSS parser (blogs, tech media, research feeds).
    """
    title = strip_html(item.get("title"))
    content = safe_content(
        item.get("summary"),
        item.get("description"),
        item.get("content"),
        item.get("title"),
    )

    return {
        "title": title,
        "author": item.get("author"),
        "url": item.get("link") or item.get("url"),
        "published_at": item.get("published") or item.get("published_at"),
        "content": content,
        "raw": item,
    }


def parse_arxiv(item: Dict) -> Dict:
    """
    arXiv feeds have clean summaries but still need fallback.
    """
    title = strip_html(item.get("title"))
    content = safe_content(
        item.get("summary"),
        item.get("title"),
    )

    return {
        "title": title,
        "author": item.get("author"),
        "url": item.get("link") or item.get("url"),
        "published_at": item.get("published") or item.get("published_at"),
        "content": content,
        "raw": item,
    }


def parse_reddit(item: Dict) -> Dict:
    """
    Reddit RSS often has HTML-heavy summaries.
    """
    title = strip_html(item.get("title"))
    content = safe_content(
        item.get("summary"),
        item.get("description"),
        item.get("title"),
    )

    return {
        "title": title,
        "author": item.get("author"),
        "url": item.get("link") or item.get("url"),
        "published_at": item.get("published") or item.get("published_at"),
        "content": content,
        "raw": item,
    }


def parse_youtube_mock(item: Dict) -> Dict:
    """
    MVP YouTube mock — metadata only.
    """
    title = item.get("title") or "AI YouTube Video"

    return {
        "title": title,
        "author": "YouTube",
        "url": item.get("url"),
        "published_at": item.get("published_at"),
        "content": strip_html(item.get("summary") or title),
        "raw": item,
    }


# ----------------------------------------------------
# Dispatcher
# ----------------------------------------------------

PARSER_MAP = {
    "rss_generic": parse_rss_generic,
    "arxiv": parse_arxiv,
    "reddit": parse_reddit,
    "youtube_mock": parse_youtube_mock,
}


def parse_raw_items(raw_items: List[Dict]) -> List[Dict]:

    parsed_items: List[Dict] = []

    for item in raw_items:
        parser_key = item.get("parser_key")
        parser = PARSER_MAP.get(parser_key)

        if not parser:
            continue

        parsed = parser(item)

        # FINAL SAFETY NET (never allow empty title or URL)
        if not parsed.get("title") or not parsed.get("url"):
            continue

        parsed_items.append({
            **parsed,
            "source_name": item.get("source_name"),
            "source_url": item.get("source_url"),
            "fetched_at": item.get("fetched_at"),
        })

    return parsed_items
