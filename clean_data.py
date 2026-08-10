"""
SkillRadar - Data Cleaning
"""

import json
import re

TECH_KEYWORDS = {
    "python", "java", "javascript", "react", "node", "sql", "aws", "azure",
    "docker", "kubernetes", "api", "backend", "frontend", "full stack",
    "software", "developer", "engineer", "data science", "data scientist",
    "data analyst", "data engineer", "machine learning", "ml", "ai",
    "devops", "cloud", "database", "programming", "web dev",
    "mobile", "ios", "android", "golang", "c plus plus", "django", "flask",
}


def load_json(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_garbled(text: str) -> bool:
    return bool(re.search(r"[ÃØâ][^\s]", text))


def strip_html(text: str) -> str:
    """Removes HTML tags from description text (e.g. <p>, <ul>, <strong>)."""
    return re.sub(r"<[^>]+>", " ", text)


def is_tech_job(title: str, tags: list) -> bool:
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in TECH_KEYWORDS)


def normalize_pythonorg(jobs: list[dict]) -> list[dict]:
    normalized = []
    for j in jobs:
        normalized.append({
            "title": j["title"],
            "company": j["company"],
            "location": j["location"],
            "tags": [],
            "description": "",
            "source": "python.org",
            "link": j["link"],
        })
    return normalized


def normalize_remoteok(jobs: list[dict]) -> list[dict]:
    normalized = []
    for j in jobs:
        normalized.append({
            "title": j["title"],
            "company": j["company"],
            "location": j["location"],
            "tags": j["tags"],
            "description": j.get("description", ""),
            "source": "remoteok",
            "link": j["link"],
        })
    return normalized


def normalize_wwr(jobs: list[dict]) -> list[dict]:
    normalized = []
    for j in jobs:
        normalized.append({
            "title": j["title"],
            "company": j["company"],
            "location": j["location"],
            "tags": j["tags"],
            "description": j.get("description", ""),
            "source": j["source"],
            "link": j["link"],
        })
    return normalized


def clean_jobs(jobs: list[dict]) -> list[dict]:
    cleaned = []
    seen = set()

    for j in jobs:
        title = j["title"].strip()
        company = j["company"].strip()
        j["description"] = strip_html(j.get("description", ""))

        if not title or not company:
            continue
        if is_garbled(title) or is_garbled(company) or is_garbled(j.get("description", "")):
            continue
        if not is_tech_job(title, j["tags"]):
            continue

        key = (title.lower(), company.lower())
        if key in seen:
            continue
        seen.add(key)

        cleaned.append(j)

    return cleaned


def save_json(data: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} jobs to {path}")


if __name__ == "__main__":
    pythonorg_raw = load_json("jobs_raw.json")
    remoteok_raw = load_json("remoteok_jobs.json")
    wwr_raw = load_json("wwr_jobs.json")

    combined = (
        normalize_pythonorg(pythonorg_raw)
        + normalize_remoteok(remoteok_raw)
        + normalize_wwr(wwr_raw)
    )
    print(f"Combined raw total: {len(combined)}")

    cleaned = clean_jobs(combined)
    print(f"After cleaning: {len(cleaned)}")

    save_json(cleaned, "jobs_clean.json")