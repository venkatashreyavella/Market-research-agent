from app.graph.workflow import route_after_verification


def test_retry_routing():
    assert route_after_verification({"unsupported_claims": [1], "iteration_count": 1, "options": {"max_iterations": 3}}) == "targeted"
    assert route_after_verification({"unsupported_claims": [1], "iteration_count": 3, "options": {"max_iterations": 3}}) == "report"
