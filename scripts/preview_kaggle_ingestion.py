import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_collection.connectors.kaggle_jobs import KaggleJobsConnector
from data_processing.cleaning.jobs import normalize_job_posting
from data_processing.validation.jobs import validate_raw_job


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview Kaggle job posting ingestion.")
    parser.add_argument(
        "dataset_dir",
        nargs="?",
        default=PROJECT_ROOT / "data" / "raw" / "kaggle_jobs",
        type=Path,
        help="Directory containing postings.csv and related Kaggle files.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Number of postings to preview.")
    args = parser.parse_args()

    connector = KaggleJobsConnector(args.dataset_dir)
    raw_jobs = connector.fetch(limit=args.limit)
    normalized_jobs = []
    skipped: list[tuple[str, str]] = []

    for raw_job in raw_jobs:
        issues = validate_raw_job(raw_job)
        if issues:
            reason = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
            skipped.append((raw_job.source_job_id or "unknown", reason))
            continue

        normalized_jobs.append(normalize_job_posting(raw_job))

    print(f"Read {len(raw_jobs)} Kaggle postings")
    print(f"Validated {len(normalized_jobs)} postings")
    print(f"Skipped {len(skipped)} postings")

    for job in normalized_jobs[: args.limit]:
        print(f"- {job.normalized_title} at {job.company} ({job.location})")

    if skipped:
        print("Skipped posting reasons:")
        for source_job_id, reason in skipped:
            print(f"- {source_job_id}: {reason}")


if __name__ == "__main__":
    main()
