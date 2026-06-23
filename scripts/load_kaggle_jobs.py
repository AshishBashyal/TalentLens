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


def build_preview(dataset_dir: Path, limit: int) -> dict[str, list[dict[str, object]]]:
    connector = KaggleJobsConnector(dataset_dir)
    raw_jobs = enrich_jobs_with_kaggle_skills(connector.fetch(limit=limit), dataset_dir)
    normalized_jobs = [
        normalize_job_posting(raw_job)
        for raw_job in raw_jobs
        if not validate_raw_job(raw_job)
    ]
    return build_database_record_preview(normalized_jobs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load Kaggle job records into PostgreSQL.")
    parser.add_argument(
        "dataset_dir",
        nargs="?",
        default=PROJECT_ROOT / "data" / "raw" / "kaggle_jobs",
        type=Path,
        help="Directory containing Kaggle CSV files.",
    )
    parser.add_argument("--limit", type=int, default=100, help="Maximum postings to read.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write records to PostgreSQL. Omit this flag for a dry run.",
    )
    args = parser.parse_args()

    preview = build_preview(args.dataset_dir, args.limit)
    print("Prepared database records:")
    for table_name, records in preview.items():
        print(f"- {table_name}: {len(records)}")

    if not args.apply:
        print("Dry run complete. Re-run with --apply to insert records into PostgreSQL.")
        return

    from api.config import get_settings
    from database.connection import open_connection
    from database.loaders.job_ingestion import JobIngestionLoader

    settings = get_settings()
    with open_connection(settings.database_url) as connection:
        loader = JobIngestionLoader(connection, source_name=KaggleJobsConnector.source_name)
        counts = loader.load(preview)

    print("Loaded records:")
    for table_name, count in counts.items():
        print(f"- {table_name}: {count}")


if __name__ == "__main__":
    main()
