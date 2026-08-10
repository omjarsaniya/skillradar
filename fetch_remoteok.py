"""
SkillRadar - Data Source 2 (RemoteOK API)
"""

import requests
import json

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

API_URL = "https://remoteok.com/api"


def fetch_remoteok_jobs() -> list[dict]:
    response = requests.get(API_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    raw = response.json()

    jobs = []
    for item in raw:
        if "id" not in item or "position" not in item:
            continue

        jobs.append({
            "title": item.get("position", ""),
            "company": item.get("company", ""),
            "location": item.get("location", ""),
            "tags": item.get("tags", []),
            "description": item.get("description", ""),
            "salary_min": item.get("salary_min", 0),
            "salary_max": item.get("salary_max", 0),
            "date_posted": item.get("date", ""),
            "link": item.get("url", ""),
        })

    return jobs


def save_jobs(jobs: list[dict], path: str = "remoteok_jobs.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(jobs)} jobs to {path}")


if __name__ == "__main__":
    jobs = fetch_remoteok_jobs()
    for j in jobs[:5]:
        print(j)
    save_jobs(jobs)