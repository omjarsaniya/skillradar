"""
SkillRadar - Phase 3, Resume Skill-Gap Agent
A LangGraph agent: extract skills from a resume -> retrieve similar/relevant
jobs from the vector store -> generate a skill-gap report using a local LLM.
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
import chromadb
from sentence_transformers import SentenceTransformer

from extract_skills import extract_skills, strip_injection_boilerplate

CHROMA_PATH = "chroma_store"
LLM_MODEL = "qwen3:8b"

embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection("job_postings")
llm = ChatOllama(model=LLM_MODEL)


# --- State: the data that flows between nodes ---
class AgentState(TypedDict):
    resume_text: str
    resume_skills: List[str]
    relevant_jobs: List[dict]
    market_skills: List[str]
    gap_report: str


# --- Node 1: extract skills from the resume ---
def extract_resume_skills(state: AgentState) -> AgentState:
    text = strip_injection_boilerplate(state["resume_text"])
    skills = extract_skills(text)
    print(f"[Node: extract_resume_skills] Found: {skills}")
    return {**state, "resume_skills": skills}


# --- Node 2: retrieve relevant jobs via vector similarity ---
def retrieve_jobs(state: AgentState) -> AgentState:
    query_embedding = embedder.encode([state["resume_text"]]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=8)

    jobs = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        jobs.append({"title": metadata["title"], "company": metadata["company"], "text": doc})

    print(f"[Node: retrieve_jobs] Retrieved {len(jobs)} relevant postings")
    return {**state, "relevant_jobs": jobs}


# --- Node 3: extract the skills these relevant jobs actually ask for ---
def extract_market_skills(state: AgentState) -> AgentState:
    all_skills = set()
    for job in state["relevant_jobs"]:
        skills = extract_skills(strip_injection_boilerplate(job["text"]))
        all_skills.update(skills)

    print(f"[Node: extract_market_skills] Market skills: {sorted(all_skills)}")
    return {**state, "market_skills": sorted(all_skills)}


# --- Node 4: generate the gap report using the local LLM ---
def generate_report(state: AgentState) -> AgentState:
    have = {s.lower() for s in state["resume_skills"]}
    wanted = {s.lower() for s in state["market_skills"]}
    missing = sorted(wanted - have)
    matching = sorted(have & wanted)

    job_titles = ", ".join(j["title"] for j in state["relevant_jobs"][:5])

    prompt = f"""You are a career advisor. Based on this analysis, write a short,
encouraging but honest skill-gap report (3-4 sentences).

Resume skills: {', '.join(have) if have else 'none detected'}
Skills already matching the market: {', '.join(matching) if matching else 'none'}
Skills in demand but missing from resume: {', '.join(missing) if missing else 'none'}
Most similar current job postings: {job_titles}

Write the report now."""

    response = llm.invoke(prompt)
    print(f"[Node: generate_report] Done")
    return {**state, "gap_report": response.content}


# --- Build the graph ---
def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("extract_resume_skills", extract_resume_skills)
    graph.add_node("retrieve_jobs", retrieve_jobs)
    graph.add_node("extract_market_skills", extract_market_skills)
    graph.add_node("generate_report", generate_report)

    graph.set_entry_point("extract_resume_skills")
    graph.add_edge("extract_resume_skills", "retrieve_jobs")
    graph.add_edge("retrieve_jobs", "extract_market_skills")
    graph.add_edge("extract_market_skills", "generate_report")
    graph.add_edge("generate_report", END)

    return graph.compile()


if __name__ == "__main__":
    agent = build_agent()

    sample_resume = """
    Om Jarsaniya - BCA Student
    Skills: Python, SQL, basic machine learning, pandas
    Built a job market scraping pipeline with FastAPI and Docker.
    Interested in AI/ML engineering roles.
    """

    result = agent.invoke({
        "resume_text": sample_resume,
        "resume_skills": [],
        "relevant_jobs": [],
        "market_skills": [],
        "gap_report": "",
    })

    print("\n" + "=" * 50)
    print("SKILL GAP REPORT")
    print("=" * 50)
    print(result["gap_report"])