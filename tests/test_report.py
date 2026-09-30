from app.agents.planner import plan_query
from app.agents.report_writer import build_report, validate_report


def test_report_validation():
    plan = plan_query("Research a market")
    report = build_report("Research a market", plan, {"company": [], "competitor": [], "market": [], "news": []}, [], [], [])
    assert not validate_report(report)
