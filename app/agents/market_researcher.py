from app.schemas.research import ResearchFinding
from app.tools.tavily_search import search

SYSTEM_PROMPT = "You are a market research agent. Distinguish historical data, current data, estimates, forecasts, and analyst opinions. Cite sources and never present forecasts as facts."


def research(plan, max_sources=20):
    findings = []
    for src in search(f"{plan.subject} market size growth trends forecast risks opportunities", min(5, max_sources)):
        findings.append(ResearchFinding(topic="Market trends", claim=f"Market evidence for {plan.subject}", detail=src.content, source=src, evidence_label="factual", confidence=src.confidence))
    return findings
