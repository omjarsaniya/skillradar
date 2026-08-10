"""
SkillRadar - Data Source 3 (WeWorkRemotely RSS)
"""

import requests
import xml.etree.ElementTree as ET
import json

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

RSS_URL = "https://weworkremotely.com/categories/remote-programming-jobs.rss"


def fetch_wwr_jobs() -> list[dict]:
    response = requests.get(RSS_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    jobs = []

    for item in root.findall(".//item"):
        raw_title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        pub_date = item.findtext("pubDate", default="")
        description = item.findtext("description", default="")

        if ":" in raw_title:
            company, job_title = raw_title.split(":", 1)
            company = company.strip()
            job_title = job_title.strip()
        else:
            company = ""
            job_title = raw_title.strip()

        jobs.append({
            "title": job_title,
            "company": company,
            "location": "Remote",
            "tags": [],
            "description": description,
            "source": "weworkremotely",
            "link": link,
            "date_posted": pub_date,
        })

    return jobs


def save_jobs(jobs: list[dict], path: str = "wwr_jobs.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(jobs)} jobs to {path}")


if __name__ == "__main__":
    jobs = fetch_wwr_jobs()
    for j in jobs[:5]:
        print(j)
    save_jobs(jobs)