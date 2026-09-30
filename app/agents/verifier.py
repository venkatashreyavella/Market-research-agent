from app.schemas.research import VerifiedClaim

SYSTEM_PROMPT = "You are a verification agent. Check whether supplied evidence actually supports claims. A URL alone is not verification. Return verified, partially_verified, unsupported, or conflicting, preserving conflicts."


def verify(findings):
    claims = []
    for finding in findings:
        content = (finding.detail or "").strip()
        if content and "mock evidence" not in content.lower():
            status, confidence = "verified", "medium"
        elif content:
            status, confidence = "partially_verified", "low"
        else:
            status, confidence = "unsupported", "low"
        claims.append(VerifiedClaim(claim=finding.claim, status=status, source_url=finding.source.url, evidence=content[:500], confidence=confidence))
    return claims
