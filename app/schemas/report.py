from datetime import datetime
from pydantic import BaseModel, Field


class ReportMetadata(BaseModel):
    title: str
    subject: str
    generated_at: datetime
    source_count: int = 0
    verified_count: int = 0
    iteration_count: int = 0


class FinalReport(BaseModel):
    metadata: ReportMetadata
    markdown: str
    pdf_path: str | None = None
    validation_errors: list[str] = Field(default_factory=list)
