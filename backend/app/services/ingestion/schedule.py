# backend/app/services/ingestion/schedule.py

"""
Scheduler for periodic news ingestion.

Supports:
- Manual trigger (used for MVP)
- APScheduler (optional dev scheduler)
- Future integration with RQ/Celery workers

Pipeline:
fetch_all_sources → normalize_items → dedupe → summarize → save to DB
"""

from sqlalchemy.orm import Session

from app.services.ingestion.fetcher import fetch_all_sources
from app.services.normalizer import normalize_items


# ---------------------------------------------------------
# Main ingestion cycle (called manually or via scheduler)
# ---------------------------------------------------------
def run_ingestion_cycle(db: Session):

    print("🔄 Starting ingestion cycle...")

    # Step 1: Fetch raw items from all sources
    raw_items = fetch_all_sources(db)

    # Step 2: Normalize raw parsed items
    normalized_items = normalize_items(raw_items)

    print(f"✨ Normalization complete — {len(normalized_items)} clean items ready.")

    return normalized_items


# ================================================================================
# OPTIONAL: Simple APScheduler job (disabled by default)
# For development or MVP demonstration.
# ================================================================================

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    APSCHEDULER_AVAILABLE = True
except Exception:
    APSCHEDULER_AVAILABLE = False


scheduler = None


def start_scheduler(db_session_factory):
    """
    Starts APScheduler to run ingestion every 15 minutes.
    Only used during development (NOT required in Docker deployment).
    """
    global scheduler

    if not APSCHEDULER_AVAILABLE:
        print("⚠ APScheduler not installed. Skipping scheduler startup.")
        return

    if scheduler is None:
        scheduler = BackgroundScheduler()

        # Add a job every 15 minutes
        scheduler.add_job(
            lambda: run_ingestion_cycle(db_session_factory()),
            trigger="interval",
            minutes=15,
            id="news_ingestion_job",
        )

        scheduler.start()
        print("⏰ APScheduler started — ingestion every 15 minutes.")


def stop_scheduler():
    """
    Cleanly shuts down the scheduler.
    """
    global scheduler

    if scheduler:
        scheduler.shutdown()
        print("🛑 APScheduler stopped.")
