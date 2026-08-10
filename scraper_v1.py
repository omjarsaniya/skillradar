"""
SkillRadar - Scraper v1 (python.org)
"""

import requests
from bs4 import BeautifulSoup
import time
import json

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

URL = "https://www.python.org/jobs/"


def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


def parse_jobs(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    jobs = []
    listings = soup.select("ol.list-recent-jobs li")

    for listing in listings:
        h2 = listing.select_one("h2")
        if not h2:
            continue
        a_tags = h2.select("a")
        if not a_tags:
            continue

        title_tag = a_tags[0]
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")

        location = ""
        for a in a_tags[1:]:
            if "/jobs/location/" in a.get("href", ""):
                location = a.get_text(strip=True)

        company = ""
        company_span = h2.select_one("span.listing-company-name")
        if company_span:
            br = company_span.find("br")
            if br and br.next_sibling:
                company = str(br.next_sibling).strip()

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "link": f"https://www.python.org{link}" if link.startswith("/") else link,
        })

    return jobs


def fetch_all_jobs(base_url: str, max_pages: int = 10) -> list[dict]:
    all_jobs = []
    page = 1

    while page <= max_pages:
        url = f"{base_url}?page={page}"
        try:
            html = fetch_page(url)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Page {page}: doesn't exist (404), stopping.")
                break
            raise

        jobs = parse_jobs(html)
        if not jobs:
            print(f"Page {page}: no jobs found, stopping.")
            break

        print(f"Page {page}: {len(jobs)} jobs")
        all_jobs.extend(jobs)
        page += 1
        time.sleep(1)

    return all_jobs


def save_jobs(jobs: list[dict], path: str = "jobs_raw.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(jobs)} jobs to {path}")


if __name__ == "__main__":
    all_jobs = fetch_all_jobs(URL)
    print(f"\nTotal jobs collected: {len(all_jobs)}")
    save_jobs(all_jobs)