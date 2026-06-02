import time
import logging
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from hash_utils import sha256_file
from database import get_connection, initialize_database
from config import MONITOR_PATH

# ── Logging setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ── Database helpers ───────────────────────────────────────
def get_stored_hash(filepath):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT filehash FROM files WHERE filepath = ?", (filepath,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def upsert_file(filepath, filehash):
    conn = get_connection()
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO files (filepath, filehash, last_scan)
        VALUES (?, ?, ?)
        ON CONFLICT(filepath) DO UPDATE SET filehash=excluded.filehash, last_scan=excluded.last_scan
    """, (filepath, filehash, timestamp))
    conn.commit()
    conn.close()


def delete_file(filepath):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM files WHERE filepath = ?", (filepath,))
    conn.commit()
    conn.close()


def save_alert(alert_type, filepath):
    conn = get_connection()
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO alerts (alert_type, filepath, timestamp)
        VALUES (?, ?, ?)
    """, (alert_type, filepath, timestamp))
    conn.commit()
    conn.close()


# ── Alert helper ───────────────────────────────────────────
def generate_alert(event_type, filepath):
    icons = {
        "CREATED":  "[+] NEW FILE",
        "MODIFIED": "[!] MODIFIED",
        "DELETED":  "[!] DELETED",
    }
    label = icons.get(event_type, "[?] UNKNOWN")
    message = f"{label}  →  {filepath}"
    logger.warning(message)
    save_alert(event_type, filepath)


# ── Event handler ──────────────────────────────────────────
class IntegrityEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path
        filehash = sha256_file(filepath)
        upsert_file(filepath, filehash)
        generate_alert("CREATED", filepath)

    def on_modified(self, event):
        if event.is_directory:
            return
        filepath = event.src_path
        if not os.path.exists(filepath):
            return
        new_hash = sha256_file(filepath)
        old_hash = get_stored_hash(filepath)
        if old_hash is None or new_hash != old_hash:
            upsert_file(filepath, new_hash)
            generate_alert("MODIFIED", filepath)

    def on_deleted(self, event):
        if event.is_directory:
            return
        filepath = event.src_path
        delete_file(filepath)
        generate_alert("DELETED", filepath)


# ── Entry point ────────────────────────────────────────────
def start_realtime_monitor():
    initialize_database()
    logger.info(f"Real-time monitoring started on: {MONITOR_PATH}")
    logger.info("Watching for changes... (Ctrl+C to stop)\n")

    event_handler = IntegrityEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITOR_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping real-time monitor...")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_realtime_monitor()
