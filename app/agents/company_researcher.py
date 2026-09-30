from app.agents.common import llm_json
from app.config import MOCK_MODE
from app.schemas.research import ResearchFinding
from app.tools.tavily_search import search

SYSTEM_PROMPT = "You are a company research agent. Use only supplied evidence or live search results, cite every finding, and represent uncertainty explicitly. Never fabricate." 


def research(plan, max_sources=20):
    findings = []
    for entity in plan.entities[:5]:
        sources = search(f"{entity} company overview products financial results", min(3, max_sources))
        for src in sources:
            findings.append(ResearchFinding(topic=entity, claim=f"{entity}: {src.title}", detail=src.content, source=src, confidence=src.confidence))
    return findings
