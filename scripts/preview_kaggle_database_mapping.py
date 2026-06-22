import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_collection.connectors.kaggle_jobs import KaggleJobsConnector
from data_processing.cleaning.jobs import normalize_job_posting
from data_processing.enrichment.kaggle import enrich_jobs_with_kaggle_skills
from data_processing.transformers.kaggle_database import build_database_record_preview
from data_processing.validation.jobs import validate_raw_job


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview database-shaped records from Kaggle jobs.")
    parser.add_argument(
        "dataset_dir",
        nargs="?",
        default=PROJECT_ROOT / "data" / "raw" / "kaggle_jobs",
        type=Path,
        help="Directory containing Kaggle CSV files.",
    )
    parser.add_argument("--limit", type=int, default=25, help="Number of postings to preview.")
    args = parser.parse_args()

    connector = KaggleJobsConnector(args.dataset_dir)
    raw_jobs = enrich_jobs_with_kaggle_skills(connector.fetch(limit=args.limit), args.dataset_dir)
    normalized_jobs = [
        normalize_job_posting(raw_job)
        for raw_job in raw_jobs
        if not validate_raw_job(raw_job)
    ]

    preview = build_database_record_preview(normalized_jobs)

    print(f"Read {len(raw_jobs)} raw jobs")
    print(f"Database-ready valid jobs: {len(normalized_jobs)}")
    for table_name, records in preview.items():
        print(f"{table_name}: {len(records)} records")

    if preview["jobs"]:
        first_job = preview["jobs"][0]
        print("First job record preview:")
        for key, value in first_job.items():
            text = str(value)
            print(f"- {key}: {text[:120]}")


if __name__ == "__main__":
    main()

