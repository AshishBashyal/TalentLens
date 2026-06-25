from data_collection.contracts import RawJobPosting
from data_processing.validation.audit import audit_raw_jobs


def test_audit_raw_jobs_counts_quality_issues() -> None:
    jobs = [
        RawJobPosting(
            source="kaggle_jobs",
            source_job_id="1",
            job_url="https://example.com/jobs/1",
            title="Data Analyst",
            company="Example Co",
            location="Remote",
            salary="",
            experience="Entry level",
            employment_type="Full-time",
            skills="SQL",
            description="Analyze data.",
            posted_date="2024-01-01",
        ),
        RawJobPosting(
            source="kaggle_jobs",
            source_job_id="1",
            job_url="https://example.com/jobs/1-copy",
            title="",
            company="",
            location="New York, NY",
            salary="USD 100000 YEARLY",
            experience="Entry level",
            employment_type="Full-time",
            skills="",
            description="Analyze data.",
            posted_date="2024-01-02",
        ),
    ]

    summary = audit_raw_jobs(jobs)

    assert summary["total_records"] == 2
    assert summary["valid_records"] == 1
    assert summary["invalid_records"] == 1
    assert summary["missing_fields"] == {"company": 1, "title": 1}
    assert summary["duplicate_source_job_id_count"] == 1
    assert summary["empty_salary_records"] == 1
    assert summary["empty_skills_records"] == 1
    assert summary["remote_records"] == 1

