# backend/app/services/ingestion/fetcher.py

from typing import List, Dict
import feedparser
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# STEP 1 — Canonical list of 20 AI news sources
# -------------------------------------------------------------------

NEWS_SOURCES: List[Dict] = [
    # ----------- Official AI Labs (RSS) -----------
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/news/rss.xml",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Meta AI",
        "url": "https://ai.meta.com/blog/rss/",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "DeepMind",
        "url": "https://deepmind.com/blog/feed/basic/",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Anthropic",
        "url": "https://www.anthropic.com/news/rss.xml",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },

    # ----------- Tech Media -----------
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Wired AI",
        "url": "https://www.wired.com/feed/tag/ai/latest/rss",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "MIT Technology Review AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/index.xml",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },

    # ----------- Research -----------
    {
        "name": "arXiv AI",
        "url": "https://export.arxiv.org/rss/cs.AI",
        "type": "rss",
        "parser_key": "arxiv",
        "active": True,
    },
    {
        "name": "arXiv ML",
        "url": "https://export.arxiv.org/rss/cs.LG",
        "type": "rss",
        "parser_key": "arxiv",
        "active": True,
    },
    {
        "name": "Papers With Code",
        "url": "https://paperswithcode.com/rss",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },

    # ----------- Community / Social -----------
    {
        "name": "Hacker News (AI)",
        "url": "https://hnrss.org/newest?q=AI",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Reddit r/MachineLearning",
        "url": "https://www.reddit.com/r/MachineLearning/.rss",
        "type": "rss",
        "parser_key": "reddit",
        "active": True,
    },

    # ----------- Platforms / Products -----------
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Microsoft AI Blog",
        "url": "https://www.microsoft.com/en-us/ai/blog/feed/",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Stability AI Blog",
        "url": "https://stability.ai/blog/rss.xml",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },
    {
        "name": "Y Combinator Blog",
        "url": "https://www.ycombinator.com/blog/rss",
        "type": "rss",
        "parser_key": "rss_generic",
        "active": True,
    },

    # ----------- YouTube (metadata only for MVP) -----------
    {
        "name": "YouTube AI Channels",
        "url": "mock://youtube-ai",
        "type": "youtube",
        "parser_key": "youtube_mock",
        "active": True,
    },
]

# -------------------------------------------------------------------
# STEP 2 — Fetch raw data (NO processing)
# -------------------------------------------------------------------

def fetch_all_sources() -> List[Dict]:
    """
    Fetch raw news items from all active sources.
    Returns source-specific raw items (not normalized).
    """

    raw_items: List[Dict] = []

    for source in NEWS_SOURCES:
        if not source["active"]:
            continue

        logger.info(f"Fetching source: {source['name']}")

        try:
            if source["type"] == "rss":
                feed = feedparser.parse(
                    source["url"],
                    request_headers={
                        "User-Agent": "Mozilla/5.0 (AI News Aggregator; +https://example.com)"
                    }
                )

                if not feed.entries:
                    logger.warning(f"No entries found for {source['name']}")
                    continue

                for entry in feed.entries:
                    raw_items.append({
                        "source_name": source["name"],
                        "source_url": source["url"],
                        "parser_key": source["parser_key"],
                        "title": entry.get("title"),
                        "url": entry.get("link"),
                        "author": entry.get("author"),
                        "published_at": entry.get("published"),
                        "summary": entry.get("summary"),
                        "raw": entry,
                        "fetched_at": datetime.utcnow(),
                    })

            elif source["type"] == "api":
                response = requests.get(source["url"], timeout=10)
                response.raise_for_status()

                data = response.json()
                raw_items.append({
                    "source_name": source["name"],
                    "parser_key": source["parser_key"],
                    "raw": data,
                    "fetched_at": datetime.utcnow(),
                })

            elif source["type"] == "youtube":
                # MVP: mock metadata only
                raw_items.append({
                    "source_name": source["name"],
                    "parser_key": "youtube_mock",
                    "title": "Sample AI YouTube Video",
                    "url": "https://youtube.com",
                    "summary": "Mock AI video metadata for MVP",
                    "published_at": datetime.utcnow().isoformat(),
                    "fetched_at": datetime.utcnow(),
                })

        except Exception as e:
            logger.error(f"Failed to fetch {source['name']}: {e}")
            continue

    logger.info(f"Fetched {len(raw_items)} raw items from sources")
    return raw_items