# Local Setup

This guide describes the current Phase 2 development foundation for TalentLens.

## Prerequisites

- Python 3.11 or newer.
- Git.
- PostgreSQL 14 or newer for database work.

The landing page remains a static HTML/CSS/JavaScript page and does not require the API to run.

## Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```powershell
pip install -r requirements.txt
```

## Configure Environment

Copy `.env.example` to `.env` and update values as needed.

```powershell
Copy-Item .env.example .env
```

The most important value for later database work is:

```text
DATABASE_URL=postgresql://talentlens:talentlens@localhost:5432/talentlens
```

## Run the API

```powershell
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/health
```

The API currently exposes only a health endpoint. This is intentional. Phase 2 starts with foundation before real ingestion endpoints.

## Database Schema

The initial schema lives in:

```text
database/migrations/001_initial_schema.sql
```

The seed file for planned job sources lives in:

```text
database/seeds/job_sources.sql
```

Actual database automation will be added after the schema and setup flow are reviewed.

## Apply Migrations

After creating the local PostgreSQL database and configuring `.env`, run:

```powershell
python scripts/apply_migrations.py
```

## Load A Small Kaggle Batch

Start with a dry run:

```powershell
python scripts/load_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 100
```

When the dry run looks correct and PostgreSQL is configured, insert records with:

```powershell
python scripts/load_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 100 --apply
```

Use small limits first so validation, duplicate handling, and schema behavior can be reviewed safely.
