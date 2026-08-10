"""
SkillRadar - Load Clean Data into SQLite
"""

import sqlite3
import json

DB_PATH = "skillradar.db"


def load_jobs(json_path: str = "jobs_clean.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN description TEXT")
    except sqlite3.OperationalError:
        pass

    inserted = 0
    skipped = 0

    for job in jobs:
        tags_str = ",".join(job["tags"])

        try:
            cursor.execute("""
                INSERT INTO jobs (title, company, location, tags, description, source, link)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                job["title"],
                job["company"],
                job["location"],
                tags_str,
                job.get("description", ""),
                job["source"],
                job["link"],
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1

    conn.commit()
    conn.close()

    print(f"Inserted: {inserted}")
    print(f"Skipped (already existed): {skipped}")


if __name__ == "__main__":
    load_jobs()