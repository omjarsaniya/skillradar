"""
SkillRadar - FastAPI Service
Serves job market data over HTTP.
"""

from fastapi import FastAPI, Query
import sqlite3
import json
from collections import Counter
from typing import Optional

app = FastAPI(title="SkillRadar API", version="0.1.0")

DB_PATH = "skillradar.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, not just index
    return conn


@app.get("/")
def root():
    return {"message": "SkillRadar API is running", "docs": "/docs"}


@app.get("/jobs")
def list_jobs(
    source: Optional[str] = None,
    skill: Optional[str] = None,
    limit: int = Query(default=20, le=100),
):
    """List jobs, optionally filtered by source or a required skill."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        job = dict(row)
        job["extracted_skills"] = json.loads(job["extracted_skills"] or "[]")

        if source and job["source"] != source:
            continue
        if skill and skill.lower() not in [s.lower() for s in job["extracted_skills"]]:
            continue

        results.append(job)

    return {"count": len(results), "jobs": results[:limit]}


@app.get("/skills/top")
def top_skills(limit: int = Query(default=10, le=50)):
    """Returns the most frequently requested skills across all jobs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT extracted_skills FROM jobs WHERE extracted_skills != '[]'")
    rows = cursor.fetchall()
    conn.close()

    all_skills = []
    for row in rows:
        all_skills.extend(json.loads(row["extracted_skills"]))

    top = Counter(all_skills).most_common(limit)
    return {"top_skills": [{"skill": s, "count": c} for s, c in top]}


@app.get("/stats")
def stats():
    """High-level dataset stats."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM jobs")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT source, COUNT(*) as count FROM jobs GROUP BY source")
    by_source = {row["source"]: row["count"] for row in cursor.fetchall()}
    conn.close()

    return {"total_jobs": total, "by_source": by_source}