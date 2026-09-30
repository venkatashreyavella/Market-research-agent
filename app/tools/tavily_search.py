from functools import lru_cache
from urllib.parse import urlparse
from app.config import MOCK_MODE, TAVILY_API_KEY
from app.schemas.research import Source


def _source(raw: dict) -> Source:
    url = raw.get("url", "https://example.com")
    parsed = urlparse(url)
    return Source(title=raw.get("title") or "Untitled source", url=url,
                  content=raw.get("content") or raw.get("snippet") or "",
                  domain=parsed.netloc, publication_date=raw.get("published_date"),
                  relevance=raw.get("score"), source_type="web")


@lru_cache(maxsize=128)
def search(query: str, max_results: int = 10, topic: str = "general") -> list[Source]:
    if MOCK_MODE:
        slug = query.lower().replace(" ", "-")[:40]
        return [Source(title=f"Research overview: {query}", url=f"https://example.com/research/{slug}",
                       content=f"Mock evidence for {query}. This is clearly labeled synthetic data for UI testing.",
                       domain="example.com", relevance=0.8, source_type="mock", tier=3, confidence="low")]
    if not TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is not configured.")
    from tavily import TavilyClient
    client = TavilyClient(api_key=TAVILY_API_KEY)
    response = client.search(query=query, max_results=max_results, topic=topic, include_answer=False)
    unique: dict[str, Source] = {}
    for item in response.get("results", []):
        source = _source(item)
        unique[str(source.url)] = source
    return list(unique.values())


def deduplicate_sources(sources: list[Source]) -> list[Source]:
    return list({str(s.url): s for s in sources}.values())
