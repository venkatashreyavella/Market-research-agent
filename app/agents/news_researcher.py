from app.schemas.research import ResearchFinding
from app.tools.tavily_search import search

SYSTEM_PROMPT = "You are a recent developments agent. Find announcements, launches, acquisitions, partnerships, regulation, and financial events. Preserve publication dates when available and cite each item."


def research(plan, max_sources=20):
    findings = []
    for src in search(f"{plan.subject} latest news announcements developments", min(5, max_sources), topic="news"):
        findings.append(ResearchFinding(topic="Recent developments", claim=src.title, detail=src.content, source=src, confidence=src.confidence))
    return findings
