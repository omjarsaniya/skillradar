"""
SkillRadar - Phase 1, Quick DB Check
Prints a few rows to confirm data landed correctly.
"""

import sqlite3

conn = sqlite3.connect("skillradar.db")
cursor = conn.cursor()

cursor.execute("SELECT title, company, source FROM jobs LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute("SELECT COUNT(*) FROM jobs")
total = cursor.fetchone()[0]
print(f"\nTotal jobs in database: {total}")

conn.close()