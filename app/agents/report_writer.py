from datetime import datetime, timezone
from app.schemas.report import ReportMetadata, FinalReport


def build_report(query, plan, findings, metrics, claims, sources, iterations=0):
    subject = plan.subject
    def bullets(items, limit=8):
        return "\n".join(f"- {x.claim} — {x.detail[:300]} [[{x.source.title}]]" for x in items[:limit]) or "- No supported findings were returned."
    financial_rows = "\n".join(f"| {m.company} | {m.metric} | {m.value if m.value is not None else 'N/A'} | {m.currency or 'N/A'} | {m.period or 'N/A'} |" for m in metrics) or "| N/A | N/A | N/A | N/A | N/A |"
    source_lines = "\n".join(f"- [{s.title}]({s.url}) — {s.domain or 'unknown domain'}" for s in sources)
    markdown = f"""# Market Research Report

## Executive Summary

This report examines **{subject}** in response to: _{query}_. It combines structured planning, web research, source preservation, and claim verification. Unsupported numeric values remain N/A.

## Research Scope and Methodology

Research type: **{plan.research_type}**. Findings were gathered from deduplicated sources and checked for evidentiary support. Forecasts and estimates should not be interpreted as established facts.

## Company / Industry Overview

{bullets(findings['company'])}

## Financial Analysis

| Company | Metric | Value | Currency | Period |
|---|---|---:|---|---|
{financial_rows}

## Competitive Landscape

{bullets(findings['competitor'])}

## Market Trends

{bullets(findings['market'])}

## Recent Developments

{bullets(findings['news'])}

## Risks

- Evidence quality and reporting periods vary by source; validate material decisions against primary filings.
- Market forecasts are estimates and may change as assumptions change.

## Opportunities

- Use the cited market and competitor evidence to identify areas for deeper diligence.

## Key Findings

Verified: {sum(c.status == 'verified' for c in claims)} | Partially verified: {sum(c.status == 'partially_verified' for c in claims)} | Unsupported: {sum(c.status == 'unsupported' for c in claims)}

## Limitations

This report is informational research, not investment, legal, or financial advice. Missing data is explicitly marked N/A rather than inferred.

## Sources

{source_lines or '- No sources returned.'}
"""
    metadata = ReportMetadata(title="Market Research Report", subject=subject, generated_at=datetime.now(timezone.utc), source_count=len(sources), verified_count=sum(c.status == 'verified' for c in claims), iteration_count=iterations)
    return FinalReport(metadata=metadata, markdown=markdown)


def validate_report(report: FinalReport) -> list[str]:
    errors = []
    required = ["Executive Summary", "Financial Analysis", "Sources"]
    if not report.markdown.strip(): errors.append("Report is empty.")
    for section in required:
        if section not in report.markdown: errors.append(f"Missing section: {section}")
    if "TODO" in report.markdown: errors.append("Report contains TODO placeholder.")
    return errors
