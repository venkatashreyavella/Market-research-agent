from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator

ResearchType = Literal["company", "multi_company", "industry", "market", "mixed"]


class Source(BaseModel):
    title: str
    url: HttpUrl
    content: str = ""
    domain: str = ""
    publication_date: str | None = None
    relevance: float | None = Field(default=None, ge=0, le=1)
    source_type: str = "web"
    tier: int = Field(default=3, ge=1, le=3)
    confidence: Literal["high", "medium", "low"] = "medium"

    @field_validator("domain", mode="before")
    @classmethod
    def default_domain(cls, value, info):
        if value:
            return value
        return ""


class ResearchPlan(BaseModel):
    subject: str
    research_type: ResearchType
    entities: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)
    research_questions: list[str] = Field(default_factory=list)
    required_sections: list[str] = Field(default_factory=list)
    financial_metrics: list[str] = Field(default_factory=list)
    search_queries: list[str] = Field(default_factory=list)


class ResearchFinding(BaseModel):
    topic: str
    claim: str
    detail: str = ""
    source: Source
    confidence: Literal["high", "medium", "low"] = "medium"
    evidence_label: Literal["historical", "current", "estimate", "forecast", "opinion", "factual"] = "factual"


class Competitor(BaseModel):
    name: str
    rationale: str = ""
    products_services: list[str] = Field(default_factory=list)
    findings: list[ResearchFinding] = Field(default_factory=list)


class VerifiedClaim(BaseModel):
    claim: str
    status: Literal["verified", "partially_verified", "unsupported", "conflicting"]
    source_url: HttpUrl | None = None
    evidence: str = ""
    confidence: Literal["high", "medium", "low"] = "medium"


class ResearchResult(BaseModel):
    user_query: str
    plan: ResearchPlan
    company_findings: list[ResearchFinding] = Field(default_factory=list)
    competitor_findings: list[ResearchFinding] = Field(default_factory=list)
    financial_findings: list = Field(default_factory=list)
    market_findings: list[ResearchFinding] = Field(default_factory=list)
    news_findings: list[ResearchFinding] = Field(default_factory=list)
    all_sources: list[Source] = Field(default_factory=list)
    verified_claims: list[VerifiedClaim] = Field(default_factory=list)
    unsupported_claims: list[VerifiedClaim] = Field(default_factory=list)
    conflicting_claims: list[VerifiedClaim] = Field(default_factory=list)
    iteration_count: int = 0
    errors: list[str] = Field(default_factory=list)
