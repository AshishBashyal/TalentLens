from collections import Counter
from collections.abc import Iterable

from data_collection.contracts import RawJobPosting
from data_processing.validation.jobs import REQUIRED_RAW_FIELDS, validate_raw_job


def audit_raw_jobs(raw_jobs: Iterable[RawJobPosting]) -> dict[str, object]:
    """Summarize data quality issues for raw job postings."""

    total_records = 0
    valid_records = 0
    invalid_records = 0
    missing_fields: Counter[str] = Counter()
    source_job_ids: Counter[str] = Counter()
    empty_salary_records = 0
    empty_skills_records = 0
    remote_records = 0

    for raw_job in raw_jobs:
        total_records += 1

        if raw_job.source_job_id.strip():
            source_job_ids[raw_job.source_job_id] += 1

        issues = validate_raw_job(raw_job)
        if issues:
            invalid_records += 1
            for issue in issues:
                if issue.field in REQUIRED_RAW_FIELDS:
                    missing_fields[issue.field] += 1
        else:
            valid_records += 1

        if not raw_job.salary.strip():
            empty_salary_records += 1

        if not raw_job.skills.strip():
            empty_skills_records += 1

        if "remote" in raw_job.location.lower() or raw_job.employment_type.lower() == "remote":
            remote_records += 1

    duplicate_source_job_ids = {
        source_job_id: count
        for source_job_id, count in source_job_ids.items()
        if count > 1
    }

    return {
        "total_records": total_records,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "valid_rate": round(valid_records / total_records, 4) if total_records else 0,
        "missing_fields": dict(sorted(missing_fields.items())),
        "duplicate_source_job_ids": duplicate_source_job_ids,
        "duplicate_source_job_id_count": len(duplicate_source_job_ids),
        "empty_salary_records": empty_salary_records,
        "empty_skills_records": empty_skills_records,
        "remote_records": remote_records,
    }

