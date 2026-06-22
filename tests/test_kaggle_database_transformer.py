from datetime import datetime

from data_collection.contracts import NormalizedJobPosting
from data_processing.transformers.kaggle_database import build_database_record_preview


def test_build_database_record_preview_deduplicates_dimensions() -> None:
    jobs = [
        NormalizedJobPosting(
            source="kaggle_jobs",
            source_job_id="1",
            job_url="https://example.com/jobs/1",
            title="Data Analyst",
            normalized_title="data analyst",
            company="Example Co",
            location="Remote",
            salary="USD 100000 YEARLY",
            experience="Entry level",
            employment_type="full-time",
            skills=("sql", "python"),
            description="Analyze data.",
            posted_date="1716153600000",
            collected_at=datetime.utcnow(),
        ),
        NormalizedJobPosting(
            source="kaggle_jobs",
            source_job_id="2",
            job_url="https://example.com/jobs/2",
            title="BI Analyst",
            normalized_title="bi analyst",
            company="Example Co",
            location="Remote",
            salary="",
            experience="Associate",
            employment_type="full-time",
            skills=("sql", "tableau"),
            description="Build dashboards.",
            posted_date="1716240000000",
            collected_at=datetime.utcnow(),
        ),
    ]

    preview = build_database_record_preview(jobs)

    assert len(preview["companies"]) == 1
    assert len(preview["locations"]) == 1
    assert len(preview["jobs"]) == 2
    assert len(preview["salaries"]) == 1
    assert len(preview["skills"]) == 3
    assert len(preview["job_skills"]) == 4

