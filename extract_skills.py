"""
SkillRadar - Skill Extraction
"""

import spacy
from spacy.matcher import PhraseMatcher
import sqlite3
import json
import re

from skills_taxonomy import ALL_SKILLS

DB_PATH = "skillradar.db"

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in ALL_SKILLS]
matcher.add("SKILLS", patterns)


def strip_injection_boilerplate(text: str) -> str:
    return re.sub(
        r"Please mention the word.*?human\.",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


def extract_skills(text: str) -> list[str]:
    doc = nlp(text)
    matches = matcher(doc)
    found = set()
    for match_id, start, end in matches:
        found.add(doc[start:end].text)
    return sorted(found)


def process_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN extracted_skills TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute("SELECT id, title, description FROM jobs")
    rows = cursor.fetchall()

    updated = 0
    for job_id, title, description in rows:
        combined_text = strip_injection_boilerplate(f"{title} {description or ''}")
        skills = extract_skills(combined_text)
        skills_str = json.dumps(skills)
        cursor.execute(
            "UPDATE jobs SET extracted_skills = ? WHERE id = ?",
            (skills_str, job_id)
        )
        if skills:
            updated += 1

    conn.commit()
    conn.close()
    print(f"Processed {len(rows)} jobs, {updated} had at least one detected skill")


if __name__ == "__main__":
    process_all_jobs()