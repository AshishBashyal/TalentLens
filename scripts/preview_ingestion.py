from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_collection.connectors.csv_sample import CsvSampleConnector
from data_processing.cleaning.jobs import normalize_job_posting
from data_processing.validation.jobs import validate_raw_job


SAMPLE_FILE = PROJECT_ROOT / "data" / "samples" / "sample_jobs.csv"


def main() -> None:
    connector = CsvSampleConnector(SAMPLE_FILE)
    raw_jobs = connector.fetch()
    valid_jobs = []

    for raw_job in raw_jobs:
        issues = validate_raw_job(raw_job)
        if issues:
            print(f"Skipping {raw_job.source_job_id}: {issues}")
            continue

        valid_jobs.append(normalize_job_posting(raw_job))

    print(f"Loaded {len(raw_jobs)} raw sample jobs")
    print(f"Validated {len(valid_jobs)} sample jobs")

    for job in valid_jobs:
        skill_preview = ", ".join(job.skills[:3])
        print(f"- {job.normalized_title} at {job.company} ({job.location}) [{skill_preview}]")


if __name__ == "__main__":
    main()
