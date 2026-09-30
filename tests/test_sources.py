from app.schemas.research import Source
from app.tools.tavily_search import deduplicate_sources


def test_deduplication():
    a = Source(title="a", url="https://example.com")
    b = Source(title="b", url="https://example.com")
    assert len(deduplicate_sources([a, b])) == 1
