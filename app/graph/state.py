from typing import TypedDict, Any


class ResearchState(TypedDict, total=False):
    user_query: str
    options: dict[str, Any]
    research_plan: Any
    company_findings: list
    competitor_findings: list
    financial_findings: list
    market_findings: list
    news_findings: list
    all_sources: list
    verified_claims: list
    unsupported_claims: list
    conflicting_claims: list
    validation_errors: list[str]
    iteration_count: int
    report_markdown: str
    pdf_path: str | None
    report: Any
    errors: list[str]
