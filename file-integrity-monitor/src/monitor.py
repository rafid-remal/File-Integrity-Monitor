import os
import sqlite3
from datetime import datetime

from config import MONITOR_PATH, HASH_ALGORITHM
from hashing import calculate_hash
from database import initialize_database
from alerts import create_alert

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fim.db"


def scan():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    current_files = set()

    for root, _, files in os.walk(MONITOR_PATH):
        for file in files:

            filepath = os.path.join(root, file)
            current_files.add(filepath)

            filehash = calculate_hash(
                filepath,
                HASH_ALGORITHM
            )

            cur.execute(
                "SELECT filehash FROM files WHERE filepath=?",
                (filepath,)
            )

            result = cur.fetchone()

            if result is None:

                cur.execute(
                    """
                    INSERT INTO files
                    VALUES (?, ?, ?)
                    """,
                    (
                        filepath,
                        filehash,
                        datetime.now().isoformat()
                    )
                )

                create_alert(cur, "CREATED", filepath)

            elif result[0] != filehash:

                cur.execute(
                    """
                    UPDATE files
                    SET filehash=?, last_scan=?
                    WHERE filepath=?
                    """,
                    (
                        filehash,
                        datetime.now().isoformat(),
                        filepath
                    )
                )

                create_alert(cur, "MODIFIED", filepath)

    cur.execute("SELECT filepath FROM files")

    known_files = {
        row[0]
        for row in cur.fetchall()
    }

    deleted = known_files - current_files

    for filepath in deleted:

        create_alert(cur, "DELETED", filepath)

        cur.execute(
            "DELETE FROM files WHERE filepath=?",
            (filepath,)
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    scan()
    print("Scan complete")
