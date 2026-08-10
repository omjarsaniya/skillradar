"""
SkillRadar - Phase 2, Trend Analysis
Real market intelligence: skill frequency by category, top companies
hiring, and source comparison - using pandas.
"""

import sqlite3
import pandas as pd
import json
from collections import Counter

DB_PATH = "skillradar.db"


def load_dataframe() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df


def analyze(df: pd.DataFrame):
    print(f"Total jobs in dataset: {len(df)}\n")

    print("--- Jobs by source ---")
    print(df["source"].value_counts(), "\n")

    print("--- Top hiring companies ---")
    print(df["company"].value_counts().head(10), "\n")

    print("--- Top skills overall ---")
    all_skills = []
    for skills_json in df["extracted_skills"].dropna():
        all_skills.extend(json.loads(skills_json))
    for skill, count in Counter(all_skills).most_common(15):
        print(f"{skill}: {count}")


if __name__ == "__main__":
    df = load_dataframe()
    analyze(df)