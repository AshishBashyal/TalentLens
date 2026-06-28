# Database Load Verification

This document describes how to verify that a small Kaggle job batch loaded into PostgreSQL correctly.

## Prerequisites

- Python dependencies installed from `requirements.txt`.
- PostgreSQL running locally.
- `.env` configured with `DATABASE_URL`.
- Migrations applied with `scripts/apply_migrations.py`.
- A small Kaggle load applied with `scripts/load_kaggle_jobs.py --apply`.

## Recommended Flow

Run migrations:

```powershell
python scripts/apply_migrations.py
```

Dry-run a small load:

```powershell
python scripts/load_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 25
```

Apply the same small load:

```powershell
python scripts/load_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 25 --apply
```

Verify table counts and quality checks:

```powershell
python scripts/verify_database_load.py
```

## Verification Checks

The verification script reports table counts for:

- Job sources.
- Companies.
- Locations.
- Jobs.
- Salaries.
- Skills.
- Job-skill relationships.
- Industries.
- Job-industry relationships.
- Job benefits.

It also reports basic quality checks:

- Jobs missing company.
- Jobs missing location.
- Jobs without skills.
- Jobs without salary.
- Orphan skills without job-skill links.

## Expected Early Behavior

In early Phase 2, some jobs will not have salary records because salary coverage is sparse in the source dataset. This is expected and should be tracked rather than hidden.

The first loader focuses on jobs, companies, locations, salaries, skills, and job-skill relationships. Industry and benefits loading will come after the core load is verified.
