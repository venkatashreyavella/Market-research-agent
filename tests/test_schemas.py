from app.schemas.research import Source, ResearchPlan


def test_source_url_and_plan():
    source = Source(title="x", url="https://example.com/a")
    assert str(source.url).startswith("https://")
    assert ResearchPlan(subject="x", research_type="company").subject == "x"
