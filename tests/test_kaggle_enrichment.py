import csv
from pathlib import Path

from data_collection.contracts import RawJobPosting
from data_processing.enrichment.kaggle import enrich_jobs_with_kaggle_skills


def test_enrich_jobs_with_kaggle_skills_uses_structured_mapping(tmp_path: Path) -> None:
    with (tmp_path / "skills.csv").open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["skill_abr", "skill_name"])
        writer.writeheader()
        writer.writerow({"skill_abr": "IT", "skill_name": "Information Technology"})
        writer.writerow({"skill_abr": "ENG", "skill_name": "Engineering"})

    with (tmp_path / "job_skills.csv").open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["job_id", "skill_abr"])
        writer.writeheader()
        writer.writerow({"job_id": "123", "skill_abr": "IT"})
        writer.writerow({"job_id": "123", "skill_abr": "ENG"})

    raw_job = RawJobPosting(
        source="kaggle_jobs",
        source_job_id="123",
        job_url="https://example.com/jobs/123",
        title="Data Engineer",
        company="Example Co",
        location="Remote",
        salary="",
        experience="Entry level",
        employment_type="Full-time",
        skills="",
        description="Build data pipelines.",
        posted_date="1716153600000",
    )

    enriched = enrich_jobs_with_kaggle_skills([raw_job], tmp_path)

    assert enriched[0].skills == "Information Technology, Engineering"

