"""
SkillRadar - Phase 2, Skills Taxonomy
A curated list of real tech skills to detect in job postings.
"""

SKILLS_TAXONOMY = {
    "languages": [
        "Python", "Java", "JavaScript", "TypeScript", "Go", "Golang",
        "C++", "C#", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "SQL",
    ],
    "ml_ai": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "scikit-learn", "NLP", "Computer Vision", "LangChain", "LangGraph",
        "RAG", "LLM", "Hugging Face", "OpenAI",
    ],
    "web_backend": [
        "Django", "Flask", "FastAPI", "Node.js", "Express", "REST API",
        "GraphQL", "Spring Boot",
    ],
    "web_frontend": [
        "React", "Vue", "Angular", "Next.js", "HTML", "CSS", "Tailwind",
    ],
    "data": [
        "Pandas", "NumPy", "Spark", "Airflow", "ETL", "Data Pipeline",
        "MLflow", "dbt",
    ],
    "cloud_devops": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD",
        "Terraform", "Jenkins", "GitHub Actions",
    ],
    "databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite",
        "Elasticsearch", "ChromaDB", "FAISS", "Pinecone",
    ],
}

ALL_SKILLS = [skill for group in SKILLS_TAXONOMY.values() for skill in group]