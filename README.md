# SkillRadar

An automated, NLP-powered job market intelligence pipeline. SkillRadar scrapes live job postings from multiple sources daily, extracts structured skill data using NLP, and serves it through a REST API.

## Problem

Job descriptions for tech roles change faster than most people can track manually. Career guidance tends to be generic, while job postings are the actual ground truth of what employers want — but nobody's systematically mining them. SkillRadar turns scattered, unstructured job postings into structured, queryable skill-demand data.

## What it does

- Scrapes job postings daily from 3 real sources (HTML scraping, JSON API, RSS/XML feed)
- Cleans and deduplicates postings across sources
- Extracts structured skills (languages, frameworks, cloud tools, etc.) from titles and descriptions using spaCy NLP
- Strips prompt-injection boilerplate some sources embed to detect AI-generated applications
- Serves the data through a FastAPI REST API
- Runs fully automated via a scheduled daily pipeline
- Containerized with Docker for reproducible deployment

## Architecture

Automated daily via Windows Task Scheduler with retry-on-failure.

## Tech stack

Python · BeautifulSoup · requests · spaCy · SQLite · pandas · FastAPI · Docker

## API endpoints

- `GET /stats` — dataset overview
- `GET /jobs?skill=python&limit=10` — filter jobs by extracted skill
- `GET /skills/top` — most in-demand skills across all postings

## Running locally

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python run_pipeline.py   # scrape + clean + load + extract
uvicorn app:app --reload
```

## Running with Docker

```bash
docker build -t skillradar-api .
docker run -p 8000:8000 skillradar-api
```

## Known limitations

- Skill extraction relies on a curated taxonomy + phrase matching rather than a trained NER model, so it won't catch skills outside the predefined list
- The database is baked into the Docker image at build time rather than mounted as a volume
- RemoteOK descriptions occasionally contain non-English content that isn't fully filtered

## Roadmap

- [ ] RAG-based resume skill-gap analysis using LangGraph
- [ ] Salary trend analysis over time
- [ ] Deploy to a cloud host with a live public URL
