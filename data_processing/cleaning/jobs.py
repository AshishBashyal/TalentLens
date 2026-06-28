import re
from datetime import datetime, timezone

from data_collection.contracts import NormalizedJobPosting, RawJobPosting


def clean_text(value: str) -> str:
    """Normalize whitespace in a text field."""

    return re.sub(r"\s+", " ", value).strip()


def normalize_title(title: str) -> str:
    """Create a simple normalized title for early analytics."""

    cleaned = clean_text(title).lower()
    cleaned = cleaned.replace("-", " ")
    return re.sub(r"[^a-z0-9+#. ]", "", cleaned)


def split_skills(skills: str) -> tuple[str, ...]:
    """Split a comma-separated skill field into normalized skill names."""

    normalized_skills = []
    for skill in skills.split(","):
        normalized_skill = normalize_skill(skill)
        if normalized_skill:
            normalized_skills.append(normalized_skill)

    return tuple(dict.fromkeys(normalized_skills))


def normalize_skill(skill: str) -> str:
    """Normalize and conservatively filter a single skill label."""

    normalized = clean_text(skill).lower()
    if not normalized:
        return ""

    if len(normalized) > 60:
        return ""

    if len(normalized.split()) > 6:
        return ""

    if any(marker in normalized for marker in (". ", ": ", "; ")):
        return ""

    return normalized


def normalize_posted_date(posted_date: str) -> str:
    """Normalize simple epoch timestamps to ISO dates when possible."""

    value = clean_text(posted_date)
    if not value:
        return ""

    try:
        timestamp = float(value)
    except ValueError:
        return value

    if timestamp > 10_000_000_000:
        timestamp = timestamp / 1000

    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()


def normalize_job_posting(raw_job: RawJobPosting) -> NormalizedJobPosting:
    """Convert a raw job posting into the first normalized contract."""

    title = clean_text(raw_job.title)
    return NormalizedJobPosting(
        source=clean_text(raw_job.source),
        source_job_id=clean_text(raw_job.source_job_id),
        job_url=clean_text(raw_job.job_url),
        title=title,
        normalized_title=normalize_title(title),
        company=clean_text(raw_job.company),
        location=clean_text(raw_job.location),
        salary=clean_text(raw_job.salary),
        experience=clean_text(raw_job.experience),
        employment_type=clean_text(raw_job.employment_type).lower(),
        skills=split_skills(raw_job.skills),
        description=clean_text(raw_job.description),
        posted_date=normalize_posted_date(raw_job.posted_date),
        collected_at=raw_job.collected_at,
    )
