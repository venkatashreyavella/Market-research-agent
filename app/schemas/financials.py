from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


class FinancialMetric(BaseModel):
    company: str
    metric: str
    value: float | None = None
    unit: str = ""
    currency: str | None = None
    period: str = ""
    source_title: str = ""
    source_url: HttpUrl | None = None
    confidence: Literal["high", "medium", "low"] = "low"
    note: str = ""
