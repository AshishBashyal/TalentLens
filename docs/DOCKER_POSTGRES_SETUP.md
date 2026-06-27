# Docker PostgreSQL Setup

TalentLens can run PostgreSQL locally through Docker Compose. This keeps local database setup reproducible and avoids mixing database installation steps with application code.

## Prerequisites

- Docker Desktop.
- Docker Compose.
- Python 3.11, 3.12, or 3.13 dependencies installed in a virtual environment.

## Start PostgreSQL

```powershell
docker compose up -d postgres
```

This starts a PostgreSQL container with:

```text
database: talentlens
user: talentlens
password: talentlens
port: 5432
```

These values match `.env.example`:

```text
DATABASE_URL=postgresql://talentlens:talentlens@localhost:5432/talentlens
```

## Check Container Status

```powershell
docker compose ps
```

## Apply Migrations

After PostgreSQL is healthy:

```powershell
python scripts/apply_migrations.py
```

## Dry-Run A Load

```powershell
python scripts/load_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 25
```

## Apply A Small Load

```powershell
python scripts/load_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 25 --apply
```

## Verify The Load

```powershell
python scripts/verify_database_load.py
```

## Stop PostgreSQL

```powershell
docker compose down
```

To delete the database volume as well:

```powershell
docker compose down -v
```

Use `down -v` only when you intentionally want to remove all local database data.
