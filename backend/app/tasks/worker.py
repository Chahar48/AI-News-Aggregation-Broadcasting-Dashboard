# backend/app/tasks/worker.py

"""
Lightweight background worker.

Runs the ingestion job at a fixed interval.
Meets <15m latency requirement without Redis/RQ.
"""

import time
import logging
from app.tasks.jobs import run_news_ingestion_job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 15 minutes (BRD requirement)
REFRESH_INTERVAL_SECONDS = 15 * 60


def start_worker():
    logger.info(" Background ingestion worker started")

    while True:
        try:
            run_news_ingestion_job()
        except Exception as e:
            logger.exception(" Worker execution failed", exc_info=e)

        logger.info(f"⏳ Sleeping for {REFRESH_INTERVAL_SECONDS} seconds")
        time.sleep(REFRESH_INTERVAL_SECONDS)


if __name__ == "__main__":
    start_worker()
