from app.config import MOCK_MODE
from app.schemas.research import ResearchFinding
from app.tools.tavily_search import search

SYSTEM_PROMPT = "You are a competitor research agent. Dynamically identify competitors from evidence; do not use hard-coded competitor lists or invent comparisons. Cite every finding."


def research(plan, max_sources=20):
    findings = []
    for entity in plan.entities[:5]:
        for src in search(f"{entity} major competitors competitive landscape", min(3, max_sources)):
            findings.append(ResearchFinding(topic="Competition", claim=f"Competitive evidence related to {entity}", detail=src.content, source=src, confidence=src.confidence))
    return findings
