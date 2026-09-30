import re
from app.config import MOCK_MODE
from app.agents.common import llm_json
from app.schemas.research import ResearchPlan

SYSTEM_PROMPT = """You are a market research planning agent. Identify whether a request concerns a company, multiple companies, an industry, or a market; extract entities and competitors only when evidence supports them. Return the ResearchPlan schema. Never fabricate facts, competitors, or financial values."""


def plan_query(query: str, options: dict | None = None) -> ResearchPlan:
    if not MOCK_MODE:
        return llm_json(SYSTEM_PROMPT, query, ResearchPlan)
    cleaned = query.strip()
    lower = cleaned.lower()
    industry_words = ["industry", "market", "sector", "cybersecurity", "semiconductor", "electric vehicle", "cloud computing"]
    research_type = "industry" if any(w in lower for w in industry_words) else "company"
    entities = []
    for candidate in re.findall(r"[A-Z][A-Za-z0-9&.-]{2,}", cleaned):
        if candidate.lower() not in {"research", "compare", "analyze"} and candidate not in entities:
            entities.append(candidate)
    if len(entities) > 1:
        research_type = "multi_company"
    subject = entities[0] if entities else cleaned.replace("Research", "").strip() or "the requested market"
    sections = ["overview", "financials", "competition", "market trends", "recent developments", "risks", "opportunities"]
    return ResearchPlan(subject=subject, research_type=research_type, entities=entities or [subject],
        research_questions=[f"What are the key facts about {subject}?", f"What recent developments affect {subject}?"],
        required_sections=sections, financial_metrics=["Revenue", "Net income", "Operating margin"],
        search_queries=[f"{subject} official company overview", f"{subject} latest financial results", f"{subject} competitors market trends"])
