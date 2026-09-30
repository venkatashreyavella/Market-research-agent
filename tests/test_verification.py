from app.agents.verifier import verify
from app.schemas.research import Source, ResearchFinding


def test_verification_status():
    s = Source(title="source", url="https://example.com", content="evidence")
    assert verify([ResearchFinding(topic="t", claim="claim", detail="evidence", source=s)])[0].status == "verified"
