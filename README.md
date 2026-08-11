# SkillRadar

**Live demo**: <https://skillradar-api-q6sh.onrender.com/docs>
*(Free tier — may take 30-60s to wake up on first request)*

An automated, NLP-powered job market intelligence pipeline. SkillRadar scrapes live job postings from multiple sources daily, extracts structured skill data using NLP, and serves it through a REST API.

## Problem

Job descriptions for tech roles change faster than most people can track manually. Career guidance tends to be generic, while job postings are the actual ground truth of what employers want — but nobody's systematically mining them. SkillRadar turns scattered, unstructured job postings into structured, queryable skill-demand data.

## What it does

- Scrapes job postings daily from 3 real sources (HTML scraping, JSON API, RSS/XML feed)
- Cleans and deduplicates postings across sources
- Extracts structured skills (languages, frameworks, cloud tools, etc.) from titles and descriptions using spaCy NLP
- Strips prompt-injection boilerplate some sources embed to detect AI-generated applications
- Embeds job postings into a ChromaDB vector store for semantic (meaning-based) search
- Runs a LangGraph agent that takes a resume, retrieves the most relevant current postings via vector similarity, and generates a skill-gap report using a local LLM (Ollama)
- Serves everything through a FastAPI REST API
- Runs fully automated via a scheduled daily pipeline
- Containerized with Docker for reproducible deployment

## Architecture

```text
3 scrapers (python.org, RemoteOK API, WeWorkRemotely RSS)
        ↓
   Clean + Deduplicate
        ↓
   SQLite (unique-link constraint prevents duplicate inserts)
        ↓
   spaCy PhraseMatcher skill extraction
        ↓
   ChromaDB vector store (sentence-transformer embeddings)
        ↓
   LangGraph agent: resume → skills → semantic retrieval → market skills → LLM report
        ↓
   FastAPI REST API
        ↓
   Docker container
```

Automated daily via Windows Task Scheduler with retry-on-failure.

## Tech stack

Python · BeautifulSoup · requests · spaCy · SQLite · pandas · FastAPI · Docker · ChromaDB · sentence-transformers · LangGraph · Ollama (local LLM, no API costs)

## API endpoints

- `GET /stats` — dataset overview
- `GET /jobs?skill=python&limit=10` — filter jobs by extracted skill
- `GET /skills/top` — most in-demand skills across all postings
- `POST /skill-gap` — submit resume text, get back matching/missing skills, similar live job postings, and an AI-generated gap report

## Running locally

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
# Install Ollama separately: https://ollama.com/download, then: ollama pull qwen3:8b
python run_pipeline.py       # scrape + clean + load + extract
python build_vectorstore.py  # embed jobs for semantic search
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
- The LangGraph agent currently requires Ollama running locally; it isn't yet containerized alongside the API
- Uses a small local LLM (qwen3:8b) rather than a hosted model, trading output polish for zero ongoing API cost
- The live demo runs a lightweight deployment without the resume-gap agent (no Ollama/LangGraph in the cloud); `/skill-gap` requires running the project locally with Ollama installed
- On the free-tier deploy, the database is rebuilt fresh from a live pipeline run on every deploy rather than persisting between deploys

## Completed

- RAG-based resume skill-gap analysis using LangGraph
- Deployed to a cloud host with a live public URL

## Roadmap

- [ ] Salary trend analysis over time
- [ ] Containerize Ollama alongside the API for a fully self-contained Docker setup
