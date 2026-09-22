import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                api TEXT NOT NULL,
                passed INTEGER NOT NULL,
                failed INTEGER NOT NULL,
                error_rate REAL NOT NULL,
                latency_avg REAL NOT NULL,
                latency_p95 REAL NOT NULL,
                payload TEXT NOT NULL
            )
        """)
        conn.commit()

def save_run(run_data):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO runs (timestamp, api, passed, failed, error_rate, latency_avg, latency_p95, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_data["timestamp"],
            run_data["api"],
            run_data["summary"]["passed"],
            run_data["summary"]["failed"],
            run_data["summary"]["error_rate"],
            run_data["summary"]["latency_ms_avg"],
            run_data["summary"]["latency_ms_p95"],
            json.dumps(run_data)
        ))
        conn.commit()

def list_runs(limit=15):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in cursor.fetchall()]
