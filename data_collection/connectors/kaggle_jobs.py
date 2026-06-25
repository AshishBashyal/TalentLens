import csv
from collections.abc import Iterator
from itertools import islice
from pathlib import Path

from data_collection.contracts import RawJobPosting


class KaggleJobsConnector:
    """Read LinkedIn-style Kaggle job postings from a local dataset directory."""

    source_name = "kaggle_jobs"

    def __init__(self, dataset_dir: str | Path) -> None:
        self.dataset_dir = Path(dataset_dir)
        self.postings_file = self.dataset_dir / "postings.csv"

    def fetch(self, limit: int | None = None) -> list[RawJobPosting]:
        return list(self.iter_fetch(limit=limit))

    def iter_fetch(self, limit: int | None = None) -> Iterator[RawJobPosting]:
        if not self.postings_file.exists():
            raise FileNotFoundError(f"Missing postings file: {self.postings_file}")

        with self.postings_file.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = islice(reader, limit) if limit is not None else reader
            for row in rows:
                yield self._row_to_raw_job(row)

    def _row_to_raw_job(self, row: dict[str, str]) -> RawJobPosting:
        salary = self._format_salary(row)
        skills = row.get("skills_desc", "")

        return RawJobPosting(
            source=self.source_name,
            source_job_id=row.get("job_id", ""),
            job_url=row.get("job_posting_url", ""),
            title=row.get("title", ""),
            company=row.get("company_name", ""),
            location=row.get("location", ""),
            salary=salary,
            experience=row.get("formatted_experience_level", ""),
            employment_type=row.get("formatted_work_type", "") or row.get("work_type", ""),
            skills=skills,
            description=row.get("description", ""),
            posted_date=row.get("listed_time", "") or row.get("original_listed_time", ""),
        )

    def _format_salary(self, row: dict[str, str]) -> str:
        min_salary = row.get("min_salary", "")
        med_salary = row.get("med_salary", "")
        max_salary = row.get("max_salary", "")
        currency = row.get("currency", "")
        pay_period = row.get("pay_period", "")

        if min_salary and max_salary:
            return f"{currency} {min_salary}-{max_salary} {pay_period}".strip()

        if med_salary:
            return f"{currency} {med_salary} {pay_period}".strip()

        if max_salary:
            return f"{currency} {max_salary} {pay_period}".strip()

        return ""
