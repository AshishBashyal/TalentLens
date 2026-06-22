# TalentLens

TalentLens is an AI-powered Job Market Intelligence Platform designed to help students, job seekers, recruiters, and businesses understand labor market trends through data.

The platform will collect job postings from multiple public sources, process them into structured datasets, extract insights from unstructured descriptions, and present business-grade intelligence about skills, salaries, hiring demand, technology adoption, and regional job market movement.

TalentLens is intentionally being built in phases. Phase 1 focused on project structure, documentation, database design, architecture, and a simple polished landing page. Phase 2 begins the development foundation for data collection, storage, and API readiness. Advanced analytics, NLP, and machine learning will be introduced only after the data pipeline and storage layers are mature.

## Product Goals

- Track the most demanded skills and technologies across job markets.
- Analyze salary trends by role, experience level, skill, company, and location.
- Identify hiring hotspots and location-based demand.
- Detect emerging technologies and declining skill demand.
- Support career planning through future recommendation and skill-gap features.
- Provide recruiters and businesses with market intelligence for workforce planning.

## Target Users

### Students

Students can use TalentLens to understand which skills are valuable, discover learning priorities, and follow industry trends before entering the job market.

### Job Seekers

Job seekers can analyze salary expectations, compare hiring locations, and identify growing technologies relevant to their next career move.

### Recruiters

Recruiters can monitor demand, skill shortages, company hiring activity, and market competition.

### Businesses

Businesses can use TalentLens to understand labor market conditions, technology adoption, and workforce planning signals.

## Current Phase

TalentLens is now entering Phase 2: data collection and storage foundation.

Current Phase 2 work includes:

- Python dependency setup.
- FastAPI application foundation.
- PostgreSQL schema migration draft.
- Seed data for planned job sources.
- Local sample ingestion workflow.
- Local development setup documentation.
- Responsible data collection planning.

The API currently exposes only a health endpoint. Real ingestion endpoints and source connectors will be added after review.

## Technology Direction

### Data Engineering

- Python
- Pandas
- PostgreSQL
- SQL

### Backend

- FastAPI

### NLP and Machine Learning

- spaCy
- Scikit-Learn

### Visualization

- Tableau
- Future web dashboards

### Version Control

- GitHub

## Project Structure

```text
TalentLens/
|-- api/
|-- data/
|   |-- external/
|   |-- interim/
|   |-- processed/
|   `-- raw/
|-- data_collection/
|   |-- connectors/
|   `-- scrapers/
|-- data_processing/
|   |-- cleaning/
|   |-- enrichment/
|   `-- validation/
|-- database/
|   |-- migrations/
|   |-- models/
|   `-- seeds/
|-- dashboard/
|   `-- landing-page/
|-- docs/
|-- machine_learning/
|   |-- experiments/
|   |-- features/
|   `-- models/
|-- nlp/
|   |-- extraction/
|   `-- taxonomies/
|-- reports/
|-- scripts/
|-- tests/
|-- ARCHITECTURE.md
|-- DATABASE_DESIGN.md
|-- PROJECT_VISION.md
|-- README.md
`-- ROADMAP.md
```

Each folder is intentionally separated by responsibility so the platform can grow without mixing scraping logic, processing logic, database assets, API code, analytics, and ML experiments.

## Opening the Landing Page

Open the static landing page at:

```text
dashboard/landing-page/index.html
```

No backend server is required for the landing page.

## Local Development

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the API foundation:

```powershell
uvicorn api.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/health
```

More setup details are in `docs/LOCAL_SETUP.md`.

Preview the local sample ingestion flow:

```powershell
python scripts/preview_ingestion.py
```

This reads `data/samples/sample_jobs.csv`, validates required fields, normalizes basic job text and skills, and prints a short summary. It does not write to the database yet.

The dataset contract is documented in `docs/DATASET_SPECIFICATION.md`.

Preview local Kaggle dataset ingestion without copying raw CSVs:

```powershell
python scripts/preview_kaggle_ingestion.py "C:\Users\ashis\Downloads\Datasets" --limit 10
```

Preview how valid Kaggle postings map toward database records:

```powershell
python scripts/preview_kaggle_database_mapping.py "C:\Users\ashis\Downloads\Datasets" --limit 25
```

## Database Foundation

The first PostgreSQL schema draft is in:

```text
database/migrations/001_initial_schema.sql
```

Planned job source seed data is in:

```text
database/seeds/job_sources.sql
```

## Current Status

TalentLens is in early Phase 2. The foundation for API configuration, database schema planning, and responsible data collection documentation is in place.
