from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class RawJobPosting:
    """Source-shaped job posting before normalization."""

    source: str
    source_job_id: str
    job_url: str
    title: str
    company: str
    location: str
    salary: str
    experience: str
    employment_type: str
    skills: str
    description: str
    posted_date: str
    collected_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class NormalizedJobPosting:
    """Cleaned job posting shaped toward the database schema."""

    source: str
    source_job_id: str
    job_url: str
    title: str
    normalized_title: str
    company: str
    location: str
    salary: str
    experience: str
    employment_type: str
    skills: tuple[str, ...]
    description: str
    posted_date: str
    collected_at: datetime


@dataclass(frozen=True)
class ValidationIssue:
    """Validation issue produced while checking raw job records."""

    field: str
    message: str
