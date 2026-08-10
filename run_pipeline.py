"""
SkillRadar - Full Pipeline
"""

import subprocess
import sys

STEPS = [
    ("Scraping python.org", "scraper_v1.py"),
    ("Fetching RemoteOK API", "fetch_remoteok.py"),
    ("Fetching WeWorkRemotely RSS", "fetch_wwr.py"),
    ("Cleaning combined data", "clean_data.py"),
    ("Loading into database", "load_to_db.py"),
    ("Extracting skills", "extract_skills.py"),
]

if __name__ == "__main__":
    for label, script in STEPS:
        print(f"\n{'='*50}")
        print(f"STEP: {label}")
        print('='*50)
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"'{script}' failed - stopping pipeline.")
            break
    else:
        print("\nPipeline complete.")