from datetime import datetime

def create_alert(cursor, alert_type, filepath):
    cursor.execute(
        """
        INSERT INTO alerts(alert_type, filepath, timestamp)
        VALUES (?, ?, ?)
        """,
        (
            alert_type,
            filepath,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    print(f"[{alert_type}] {filepath}")
