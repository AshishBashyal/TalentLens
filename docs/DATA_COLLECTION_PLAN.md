# Data Collection Plan

TalentLens will collect job posting data incrementally and responsibly.

## Phase 2 Objective

The goal of Phase 2 is to establish a reliable data collection and storage foundation, not to scrape every source immediately.

Initial work should focus on:

- Choosing one source for the first ingestion workflow.
- Capturing raw source data before transformation.
- Normalizing key job fields.
- Loading validated records into PostgreSQL.
- Documenting source-specific constraints and assumptions.

## Responsible Collection Guidelines

Before building a connector for any source:

- Review the source terms and access rules.
- Prefer official APIs, exports, or permitted public access.
- Respect robots policies where applicable.
- Use rate limits and retries.
- Store source URLs and collection timestamps.
- Avoid collecting private or account-protected data.

## Planned Sources

Initial candidate sources:

- LinkedIn.
- Indeed.
- Wellfound.
- Internshala.
- Naukri.

Each source should receive its own connector or scraper module only after the access method is approved.

## Raw Data Contract

Raw collected records should preserve source-specific fields where possible.

Minimum raw metadata:

- Source name.
- Source job ID when available.
- Original job URL.
- Collection timestamp.
- Raw title.
- Raw company.
- Raw location.
- Raw salary.
- Raw description.
- Raw posting date.

## Normalized Job Contract

Cleaned records should map toward the database schema:

- Job title.
- Normalized title.
- Company.
- Location.
- Salary.
- Experience requirements.
- Description.
- Skills when available.
- Posting date.
- Source metadata.

## Next Implementation Step

The first safe implementation step is now in place:

- `data_collection/contracts.py` defines raw and normalized job posting contracts.
- `data_collection/connectors/base.py` defines the connector interface.
- `data_collection/connectors/csv_sample.py` provides a local CSV connector.
- `data_processing/validation/jobs.py` validates minimum raw job fields.
- `data_processing/cleaning/jobs.py` normalizes text and job titles.
- `data/samples/sample_jobs.csv` provides safe local sample data.
- `scripts/preview_ingestion.py` previews the local ingestion flow.
- `docs/DATASET_SPECIFICATION.md` documents the dataset contract.

The next step is to select the first real source and implement it behind the same connector interface.

## Kaggle Dataset Candidate

A local Kaggle dataset has been inspected as the first realistic ingestion candidate. It contains job postings, companies, skills, industries, salaries, benefits, specialities, and employee counts.

Assessment:

```text
docs/KAGGLE_DATASET_ASSESSMENT.md
```

Profiling helper:

```powershell
python scripts/profile_csv_dataset.py "C:\Users\ashis\Downloads\Datasets"
```

Do not commit the raw CSV files unless the Kaggle license clearly permits redistribution.

Local raw-data placeholder:

```text
data/raw/kaggle_jobs/README.md
```

Kaggle ingestion preview:

```powershell
python scripts/preview_kaggle_ingestion.py "C:\Users\ashis\Downloads\Datasets" --limit 10
```

The connector reads `postings.csv` from the provided directory and maps records into the shared `RawJobPosting` contract.

Database mapping preview:

```powershell
python scripts/preview_kaggle_database_mapping.py "C:\Users\ashis\Downloads\Datasets" --limit 25
```

This prepares database-shaped records in memory and helps validate the ingestion design before writing to PostgreSQL.

Small-batch database loader:

```powershell
python scripts/load_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 100
```

This command runs in dry-run mode by default. Add `--apply` only after PostgreSQL migrations have been applied and the preview counts look correct.

Data quality audit:

```powershell
python scripts/audit_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 1000
```

The audit logic lives separately from connectors and loaders so the ingestion pipeline keeps high cohesion and low coupling.

Database load verification:

```powershell
python scripts/verify_database_load.py
```

Verification logic lives in `database/verification.py` so query checks remain separate from loading logic.

## Preview the Sample Flow

Run:

```powershell
python scripts/preview_ingestion.py
```

Expected behavior:

- Load raw rows from `data/samples/sample_jobs.csv`.
- Validate required fields.
- Normalize job titles, text fields, employment type, and skills.
- Print a short summary without writing to the database.
