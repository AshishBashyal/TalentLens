import csv
from pathlib import Path

from data_collection.connectors.kaggle_jobs import KaggleJobsConnector
from data_processing.cleaning.jobs import normalize_job_posting


def test_kaggle_jobs_connector_maps_postings_csv(tmp_path: Path) -> None:
    postings_file = tmp_path / "postings.csv"
    with postings_file.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "job_id",
                "job_posting_url",
                "title",
                "company_name",
                "location",
                "min_salary",
                "med_salary",
                "max_salary",
                "currency",
                "pay_period",
                "formatted_experience_level",
                "formatted_work_type",
                "work_type",
                "skills_desc",
                "description",
                "listed_time",
                "original_listed_time",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "job_id": "123",
                "job_posting_url": "https://example.com/jobs/123",
                "title": "Data Analyst",
                "company_name": "Example Co",
                "location": "Remote",
                "min_salary": "50000",
                "med_salary": "",
                "max_salary": "70000",
                "currency": "USD",
                "pay_period": "YEARLY",
                "formatted_experience_level": "Entry level",
                "formatted_work_type": "Full-time",
                "work_type": "FULL_TIME",
                "skills_desc": "SQL, Python, Tableau",
                "description": "Analyze job market data and build dashboards.",
                "listed_time": "1716153600000",
                "original_listed_time": "",
            }
        )

    connector = KaggleJobsConnector(tmp_path)
    raw_jobs = connector.fetch(limit=1)
    normalized = normalize_job_posting(raw_jobs[0])

    assert len(raw_jobs) == 1
    assert raw_jobs[0].source == "kaggle_jobs"
    assert raw_jobs[0].source_job_id == "123"
    assert raw_jobs[0].salary == "USD 50000-70000 YEARLY"
    assert normalized.normalized_title == "data analyst"
    assert normalized.skills == ("sql", "python", "tableau")

