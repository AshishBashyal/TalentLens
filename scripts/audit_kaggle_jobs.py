import argparse
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_collection.connectors.kaggle_jobs import KaggleJobsConnector
from data_processing.enrichment.kaggle import enrich_jobs_with_kaggle_skills
from data_processing.validation.audit import audit_raw_jobs


def render_markdown(summary: dict[str, object], dataset_dir: Path, limit: int | None) -> str:
    missing_fields = summary["missing_fields"]
    duplicate_count = summary["duplicate_source_job_id_count"]

    lines = [
        "# Kaggle Job Data Quality Audit",
        "",
        f"Dataset directory: `{dataset_dir}`",
        f"Record limit: `{limit if limit is not None else 'all'}`",
        "",
        "## Summary",
        "",
        f"- Total records: {summary['total_records']}",
        f"- Valid records: {summary['valid_records']}",
        f"- Invalid records: {summary['invalid_records']}",
        f"- Valid rate: {summary['valid_rate']}",
        f"- Duplicate source job IDs: {duplicate_count}",
        f"- Empty salary records: {summary['empty_salary_records']}",
        f"- Empty skills records after enrichment: {summary['empty_skills_records']}",
        f"- Remote records: {summary['remote_records']}",
        "",
        "## Missing Required Fields",
        "",
    ]

    if missing_fields:
        for field, count in missing_fields.items():
            lines.append(f"- `{field}`: {count}")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "This report is generated from local CSV files and should not be treated as a public dataset artifact until the Kaggle license is confirmed.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Kaggle job posting quality.")
    parser.add_argument(
        "dataset_dir",
        nargs="?",
        default=PROJECT_ROOT / "data" / "raw" / "kaggle_jobs",
        type=Path,
        help="Directory containing Kaggle CSV files.",
    )
    parser.add_argument("--limit", type=int, default=1000, help="Maximum postings to audit.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional markdown report path. Reports are generated locally and ignored by Git.",
    )
    args = parser.parse_args()

    connector = KaggleJobsConnector(args.dataset_dir)
    raw_jobs = connector.fetch(limit=args.limit)
    enriched_jobs = enrich_jobs_with_kaggle_skills(raw_jobs, args.dataset_dir)
    summary = audit_raw_jobs(enriched_jobs)

    print(json.dumps(summary, indent=2, sort_keys=True))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_markdown(summary, args.dataset_dir, args.limit), encoding="utf-8")
        print(f"Markdown report written to {args.output}")


if __name__ == "__main__":
    main()

