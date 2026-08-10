"""
SkillRadar - Phase 2, Quick Skill Check
Shows which skills were detected on real job titles, plus overall
skill frequency - the actual "market intelligence" insight.
"""

import sqlite3
import json
from collections import Counter

conn = sqlite3.connect("skillradar.db")
cursor = conn.cursor()

cursor.execute("SELECT title, extracted_skills FROM jobs WHERE extracted_skills != '[]'")
rows = cursor.fetchall()

print("--- Sample extractions ---")
for title, skills_json in rows[:10]:
    skills = json.loads(skills_json)
    print(f"{title}\n  -> {skills}\n")

# Skill frequency across all jobs - this is the actual market insight
all_skills = []
for _, skills_json in rows:
    all_skills.extend(json.loads(skills_json))

print("--- Top skills by frequency ---")
for skill, count in Counter(all_skills).most_common(10):
    print(f"{skill}: {count}")

conn.close()