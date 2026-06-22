import csv
from pathlib import Path

from data_collection.contracts import RawJobPosting


class CsvSampleConnector:
    """Read sample job postings from a local CSV file."""

    source_name = "sample_csv"

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def fetch(self) -> list[RawJobPosting]:
        with self.file_path.open(newline="", encoding="utf-8") as csv_file:
            rows = csv.DictReader(csv_file)
            return [
                RawJobPosting(
                    source=row.get("source", self.source_name),
                    source_job_id=row.get("source_job_id", ""),
                    job_url=row.get("job_url", ""),
                    title=row.get("title", ""),
                    company=row.get("company", ""),
                    location=row.get("location", ""),
                    salary=row.get("salary", ""),
                    experience=row.get("experience", ""),
                    employment_type=row.get("employment_type", ""),
                    skills=row.get("skills", ""),
                    description=row.get("description", ""),
                    posted_date=row.get("posted_date", ""),
                )
                for row in rows
            ]
