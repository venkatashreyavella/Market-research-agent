from app.agents.planner import plan_query
from app.agents.company_researcher import research as company_research
from app.agents.competitor_researcher import research as competitor_research
from app.agents.financial_researcher import research as financial_research
from app.agents.market_researcher import research as market_research
from app.agents.news_researcher import research as news_research
from app.agents.verifier import verify
from app.agents.report_writer import build_report, validate_report
from app.tools.tavily_search import deduplicate_sources, search


def planner_node(s): return {"research_plan": plan_query(s["user_query"], s.get("options"))}
def company_research_node(s): return {"company_findings": company_research(s["research_plan"], s.get("options", {}).get("max_sources", 20))}
def competitor_research_node(s): return {"competitor_findings": competitor_research(s["research_plan"], s.get("options", {}).get("max_sources", 20))}
def financial_research_node(s): return {"financial_findings": financial_research(s["research_plan"], s.get("options", {}).get("max_sources", 20))}
def market_research_node(s): return {"market_findings": market_research(s["research_plan"], s.get("options", {}).get("max_sources", 20))}
def news_research_node(s): return {"news_findings": news_research(s["research_plan"], s.get("options", {}).get("max_sources", 20))}


def aggregation_node(s):
    groups = [s.get(k, []) for k in ("company_findings", "competitor_findings", "market_findings", "news_findings")]
    return {"all_sources": deduplicate_sources([f.source for group in groups for f in group])}


def verification_node(s):
    findings = [f for key in ("company_findings", "competitor_findings", "market_findings", "news_findings") for f in s.get(key, [])]
    claims = verify(findings)
    return {"verified_claims": claims, "unsupported_claims": [c for c in claims if c.status == "unsupported"], "conflicting_claims": [c for c in claims if c.status == "conflicting"], "iteration_count": s.get("iteration_count", 0) + 1}


def targeted_research_node(s):
    plan = s["research_plan"]
    extra = []
    for src in search(f"{plan.subject} verification evidence filing", 3):
        from app.schemas.research import ResearchFinding
        extra.append(ResearchFinding(topic="Targeted verification", claim=f"Additional evidence for {plan.subject}", detail=src.content, source=src))
    return {"company_findings": s.get("company_findings", []) + extra}


def report_writer_node(s):
    report = build_report(s["user_query"], s["research_plan"], {"company": s.get("company_findings", []), "competitor": s.get("competitor_findings", []), "market": s.get("market_findings", []), "news": s.get("news_findings", [])}, s.get("financial_findings", []), s.get("verified_claims", []), s.get("all_sources", []), s.get("iteration_count", 0))
    return {"report": report, "report_markdown": report.markdown}


def report_validation_node(s): return {"validation_errors": validate_report(s["report"])}


def pdf_generation_node(s):
    from app.pdf.generator import generate_pdf
    path = generate_pdf(s["report"].markdown, s["report"].metadata.subject)
    return {"pdf_path": str(path)}
