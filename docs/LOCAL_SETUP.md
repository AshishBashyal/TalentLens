# Local Setup

This guide describes the current Phase 2 development foundation for TalentLens.

## Prerequisites

- Python 3.11, 3.12, or 3.13.
- Git.
- PostgreSQL 14 or newer for database work.

The landing page remains a static HTML/CSS/JavaScript page and does not require the API to run.

Python 3.14 is not recommended for this project yet because some data and ML dependencies may not publish stable wheels immediately for the newest Python release.

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

## PostgreSQL Setup

Option 1: use Docker Compose.

```powershell
docker compose up -d postgres
```

Option 2: install PostgreSQL locally, then create a database and user that match `.env`.

Example SQL:

```sql
CREATE DATABASE talentlens;
CREATE USER talentlens WITH PASSWORD 'talentlens';
GRANT ALL PRIVILEGES ON DATABASE talentlens TO talentlens;
```

If you use a different username, password, host, port, or database name, update `DATABASE_URL` in `.env`.

More Docker-specific setup details are in `docs/DOCKER_POSTGRES_SETUP.md`.

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

## Verify The Database Load

After applying a small load, run:

```powershell
python scripts/verify_database_load.py
```

This prints table counts and basic quality checks for loaded records.
