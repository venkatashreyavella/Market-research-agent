import json
import streamlit as st
from app.config import MOCK_MODE
from app.graph.workflow import run_workflow


def run_app():
    st.set_page_config(page_title="Automated Market Research Agent", page_icon="🤖", layout="wide")
    st.title("🤖 Automated Market Research Agent")
    st.caption("Research any company, industry, or market using AI-powered web research.")
    with st.sidebar:
        st.header("Research Settings")
        depth = st.selectbox("Research depth", ["Quick", "Standard", "Comprehensive"], index=1)
        max_sources = st.selectbox("Maximum sources", [10, 20, 30, 50], index=1)
        max_iterations = st.selectbox("Maximum verification iterations", [1, 2, 3, 4], index=2)
        financial = st.checkbox("Financial analysis", True); competitors = st.checkbox("Competitor analysis", True)
        market = st.checkbox("Market trends", True); news = st.checkbox("Recent developments", True); risks = st.checkbox("Risks & opportunities", True)
        if MOCK_MODE: st.info("Mock mode enabled")
    query = st.text_area("What would you like to research?", placeholder="Example: Research Tesla and its major competitors", height=110)
    if st.button("🚀 Start Research", type="primary", disabled=not query.strip()):
        options = {"depth": depth, "max_sources": max_sources, "max_iterations": max_iterations, "financial": financial, "competitors": competitors, "market": market, "news": news, "risks": risks}
        with st.status("Running research workflow...", expanded=True) as status:
            try:
                st.write("✓ Planning research and running parallel research agents")
                result = run_workflow(query, options)
                st.write("✓ Evidence aggregated and claims verified")
                st.write("✓ Markdown report and PDF generated")
                status.update(label="Research complete", state="complete")
                st.session_state["result"] = result
            except Exception as exc:
                status.update(label="Research could not be completed", state="error")
                st.error(f"Research could not be completed: {exc}")
    result = st.session_state.get("result")
    if not result: return
    plan = result["research_plan"]; claims = result.get("verified_claims", []); sources = result.get("all_sources", [])
    st.success("Research Complete")
    c1, c2, c3, c4 = st.columns(4); c1.metric("Subject", plan.subject); c2.metric("Sources", len(sources)); c3.metric("Verified claims", sum(x.status == "verified" for x in claims)); c4.metric("Iterations", result.get("iteration_count", 0))
    report = result["report"]
    tabs = st.tabs(["Executive Summary", "Full Report", "Financials", "Competitors", "Sources", "Research Data"])
    with tabs[0]: st.markdown(report.markdown.split("## Financial Analysis")[0])
    with tabs[1]: st.markdown(report.markdown)
    with tabs[2]: st.dataframe([m.model_dump(mode="json") for m in result.get("financial_findings", [])], use_container_width=True)
    with tabs[3]: st.markdown("\n".join(f"- {f.claim}: {f.detail}" for f in result.get("competitor_findings", [])) or "No competitor findings.")
    with tabs[4]:
        for source in sources: st.markdown(f"**{source.title}** · {source.domain} · {source.confidence}  \n[{source.url}]({source.url})")
    with tabs[5]: st.json({"plan": plan.model_dump(mode="json"), "claims": [c.model_dump(mode="json") for c in claims]})
    st.download_button("Download Markdown", report.markdown, file_name="market_research.md", mime="text/markdown")
    if result.get("pdf_path"):
        with open(result["pdf_path"], "rb") as f: st.download_button("Download PDF", f, file_name="market_research.pdf", mime="application/pdf")
    st.download_button("Download Research JSON", json.dumps({k: str(v) for k, v in result.items() if k != "report"}, indent=2), file_name="research.json", mime="application/json")
    st.download_button("Download Sources JSON", json.dumps([s.model_dump(mode="json") for s in sources], indent=2), file_name="sources.json", mime="application/json")
