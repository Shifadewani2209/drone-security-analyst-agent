import sqlite3
import os

DB_PATH = "data/drone_events.db"


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS frames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frame_id INTEGER,
            timestamp TEXT,
            location TEXT,
            altitude INTEGER,
            description TEXT,
            objects TEXT,
            event_type TEXT,
            alert_level TEXT,
            recommendation TEXT
        )
    """)

    conn.commit()
    conn.close()


def clear_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM frames")
    conn.commit()
    conn.close()


def insert_event(event):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO frames (
            frame_id, timestamp, location, altitude, description,
            objects, event_type, alert_level, recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event["frame_id"],
        event["timestamp"],
        event["location"],
        event["altitude"],
        event["description"],
        event["objects"],
        event["event_type"],
        event["alert_level"],
        event["recommendation"]
    ))

    conn.commit()
    conn.close()


def get_all_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT frame_id, timestamp, location, altitude, description, objects, event_type, alert_level, recommendation FROM frames")
    rows = cursor.fetchall()

    conn.close()

    events = []
    for row in rows:
        events.append({
            "frame_id": row[0],
            "timestamp": row[1],
            "location": row[2],
            "altitude": row[3],
            "description": row[4],
            "objects": row[5],
            "event_type": row[6],
            "alert_level": row[7],
            "recommendation": row[8]
        })

    return events


def search_events(keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    search_text = f"%{keyword}%"

    cursor.execute("""
        SELECT frame_id, timestamp, location, altitude, description, objects, event_type, alert_level, recommendation
        FROM frames
        WHERE description LIKE ?
        OR objects LIKE ?
        OR location LIKE ?
        OR event_type LIKE ?
        OR alert_level LIKE ?
    """, (search_text, search_text, search_text, search_text, search_text))

    rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "frame_id": row[0],
            "timestamp": row[1],
            "location": row[2],
            "altitude": row[3],
            "description": row[4],
            "objects": row[5],
            "event_type": row[6],
            "alert_level": row[7],
            "recommendation": row[8]
        })

    return events