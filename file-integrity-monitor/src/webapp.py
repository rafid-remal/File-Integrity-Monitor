from flask import Flask, render_template
import sqlite3
from pathlib import Path

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__,template_folder=str(BASE_DIR / "templates"))

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fim.db"


@app.route("/")
def dashboard():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files")
    total_files = cur.fetchone()[0]

    cur.execute("""
        SELECT alert_type,
               filepath,
               timestamp
        FROM alerts
        ORDER BY id DESC
        LIMIT 50
    """)

    alerts = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_files=total_files,
        alerts=alerts
    )


if __name__ == "__main__":
    app.run(debug=True)
