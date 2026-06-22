import argparse
import csv
from pathlib import Path


DEFAULT_FILES = (
    "postings.csv",
    "companies.csv",
    "company_specialities.csv",
    "employee_counts.csv",
    "skills.csv",
    "salaries.csv",
    "job_skills.csv",
    "job_industries.csv",
    "industries.csv",
    "benefits.csv",
)


def profile_csv(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or []
        non_empty_counts = {field: 0 for field in fieldnames}
        row_count = 0
        sample_row: dict[str, str] | None = None

        for row in reader:
            row_count += 1
            if sample_row is None:
                sample_row = row

            for field, value in row.items():
                if value and value.strip():
                    non_empty_counts[field] += 1

    sparse_fields = [
        field
        for field, count in non_empty_counts.items()
        if row_count > 0 and count / row_count < 0.5
    ]

    return {
        "file": path.name,
        "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
        "rows": row_count,
        "columns": fieldnames,
        "sparse_fields_lt_50_percent": sparse_fields,
        "sample": sample_row or {},
    }


def print_profile(profile: dict[str, object]) -> None:
    print(f"FILE: {profile['file']}")
    print(f"SIZE_MB: {profile['size_mb']}")
    print(f"ROWS: {profile['rows']}")
    print(f"COLUMNS: {', '.join(profile['columns'])}")

    sparse_fields = profile["sparse_fields_lt_50_percent"]
    if sparse_fields:
        print(f"SPARSE_FIELDS_LT_50_PERCENT: {', '.join(sparse_fields)}")

    sample = profile["sample"]
    if sample:
        preview = {
            key: value[:80] + "..." if len(value) > 80 else value
            for key, value in list(sample.items())[:8]
        }
        print(f"SAMPLE: {preview}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile CSV files for TalentLens ingestion planning.")
    parser.add_argument("dataset_dir", type=Path, help="Directory containing CSV dataset files.")
    parser.add_argument("--files", nargs="*", default=DEFAULT_FILES, help="CSV files to profile.")
    args = parser.parse_args()

    for file_name in args.files:
        path = args.dataset_dir / file_name
        if not path.exists():
            print(f"SKIPPED: {file_name} was not found")
            continue

        print_profile(profile_csv(path))


if __name__ == "__main__":
    main()

