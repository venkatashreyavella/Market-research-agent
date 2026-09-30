from app.graph.nodes import *
from app.graph.state import ResearchState


def route_after_verification(s):
    max_iterations = s.get("options", {}).get("max_iterations", 3)
    if s.get("unsupported_claims") and s.get("iteration_count", 0) < max_iterations:
        return "targeted"
    return "report"


def build_workflow():
    try:
        from langgraph.graph import StateGraph, START, END
        graph = StateGraph(ResearchState)
        graph.add_node("planner", planner_node)
        for name, fn in [("company", company_research_node), ("competitor", competitor_research_node), ("financial", financial_research_node), ("market", market_research_node), ("news", news_research_node)]: graph.add_node(name, fn)
        for name in ("aggregation", "verification", "targeted", "report", "validation", "pdf"): graph.add_node(name, {"aggregation": aggregation_node, "verification": verification_node, "targeted": targeted_research_node, "report": report_writer_node, "validation": report_validation_node, "pdf": pdf_generation_node}[name])
        graph.add_edge(START, "planner")
        for n in ("company", "competitor", "financial", "market", "news"): graph.add_edge("planner", n); graph.add_edge(n, "aggregation")
        graph.add_edge("aggregation", "verification")
        graph.add_conditional_edges("verification", route_after_verification, {"targeted": "targeted", "report": "report"})
        graph.add_edge("targeted", "verification"); graph.add_edge("report", "validation"); graph.add_edge("validation", "pdf"); graph.add_edge("pdf", END)
        return graph.compile()
    except ImportError:
        return None


def run_workflow(query: str, options: dict) -> ResearchState:
    workflow = build_workflow()
    initial = {"user_query": query, "options": options, "iteration_count": 0, "errors": []}
    if workflow is not None:
        return workflow.invoke(initial)
    # Useful fallback for environments where optional LangGraph dependencies are unavailable.
    state = initial | planner_node(initial)
    for fn in (company_research_node, competitor_research_node, financial_research_node, market_research_node, news_research_node): state.update(fn(state))
    state.update(aggregation_node(state)); state.update(verification_node(state)); state.update(report_writer_node(state)); state.update(report_validation_node(state)); state.update(pdf_generation_node(state)); return state
