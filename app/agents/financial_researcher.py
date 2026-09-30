from app.config import MOCK_MODE
from app.schemas.financials import FinancialMetric
from app.tools.tavily_search import search

SYSTEM_PROMPT = "You are a financial research agent. Extract financial metrics only when directly supported by reliable evidence. Never invent numbers; use null and explain why when data is missing. Keep reporting periods separate."


def research(plan, max_sources=20):
    metrics = []
    for entity in plan.entities[:5]:
        sources = search(f"{entity} latest annual report revenue net income operating margin", min(3, max_sources))
        for src in sources:
            metrics.append(FinancialMetric(company=entity, metric="Revenue", value=None, unit="", currency=None,
                period="", source_title=src.title, source_url=src.url, confidence="low",
                note="No numeric value extracted in this pass; verify against the linked filing."))
    return metrics
