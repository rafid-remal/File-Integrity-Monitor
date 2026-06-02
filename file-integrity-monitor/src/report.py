import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "fim.db"
REPORT_DIR = BASE_DIR / "reports"


def generate_report():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT alert_type,
               filepath,
               timestamp
        FROM alerts
        ORDER BY id DESC
    """)

    alerts = cur.fetchall()

    REPORT_DIR.mkdir(exist_ok=True)

    report_file = REPORT_DIR / (
        f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )

    with open(report_file, "w") as f:
        f.write("""
        <html>
        <head>
            <title>FIM Report</title>
        </head>
        <body>
            <h1>File Integrity Monitoring Report</h1>

            <table border="1">
            <tr>
                <th>Alert Type</th>
                <th>File</th>
                <th>Timestamp</th>
            </tr>
        """)

        for alert in alerts:
            f.write(
                f"<tr>"
                f"<td>{alert[0]}</td>"
                f"<td>{alert[1]}</td>"
                f"<td>{alert[2]}</td>"
                f"</tr>"
            )

        f.write("""
            </table>
        </body>
        </html>
        """)

    conn.close()

    print(f"Report generated: {report_file}")
