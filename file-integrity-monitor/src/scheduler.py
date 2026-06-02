import time
import logging
import schedule
from datetime import datetime

from monitor import run_scan
from config import SCAN_INTERVAL, MONITOR_PATH

# ── Logging setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ── Scheduled job ──────────────────────────────────────────
def scheduled_scan():
    logger.info(f"Scheduled scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    run_scan()
    logger.info("Scheduled scan complete.\n")


# ── Entry point ────────────────────────────────────────────
def start_scheduler():
    logger.info(f"Scheduler started — running scan every {SCAN_INTERVAL} seconds.")
    logger.info("Press Ctrl+C to stop.\n")

    scheduled_scan()  # Run once immediately on start

    schedule.every(SCAN_INTERVAL).seconds.do(scheduled_scan)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    start_scheduler()
