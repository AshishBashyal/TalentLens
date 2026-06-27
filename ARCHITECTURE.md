# TalentLens Architecture

## Architecture Overview

TalentLens will follow a modular architecture with clear separation between ingestion, processing, storage, analytics, API delivery, reporting, and future machine learning features.

The platform is designed to grow in stages. Phase 1 defines the foundation. Later phases will add data collection, cleaning, analytics, NLP, machine learning, and advanced AI capabilities.

## High-Level Flow

```text
Job Sources
    ↓
Data Collection Layer
    ↓
Raw Data Storage
    ↓
Data Processing and Validation
    ↓
PostgreSQL Analytical Store
    ↓
API Layer and Reporting Layer
    ↓
Frontend, Tableau, Reports, and Future Intelligence Features
```

## Major Components

### Data Collection Layer

Responsible for collecting job postings from public and permitted sources such as LinkedIn, Indeed, Wellfound, Internshala, Naukri, and other job platforms.

This layer will eventually include:

- Source-specific connectors.
- Scrapers where legally and technically appropriate.
- API integrations where available.
- Rate limiting.
- Retry handling.
- Source metadata tracking.

The collection layer should store data in raw form before transformation so the platform has traceability and can reprocess data when logic improves.

### Raw Data Layer

The raw layer preserves original collected data with minimal transformation.

Purpose:

- Maintain data lineage.
- Support debugging.
- Allow reprocessing.
- Preserve source-specific fields before normalization.

### Data Processing Layer

Responsible for cleaning, normalizing, validating, and enriching job data.

Processing responsibilities include:

- Standardizing job titles.
- Normalizing locations.
- Parsing salary values.
- Cleaning descriptions.
- Removing duplicates.
- Validating required fields.
- Preparing data for database insertion.

### Database Layer

PostgreSQL will be the primary structured data store.

The database will store normalized entities such as jobs, companies, locations, skills, salaries, job sources, and extraction results.

This layer should support both operational queries and analytical queries.

### NLP Layer

The NLP layer will be added after reliable data collection and storage exist.

Future responsibilities:

- Extract skills from job descriptions.
- Identify technologies and tools.
- Detect certifications.
- Parse experience requirements.
- Build and maintain skill taxonomies.

### Machine Learning Layer

The ML layer will be introduced in later phases.

Future responsibilities:

- Job clustering.
- Salary prediction.
- Trend forecasting.
- Career recommendations.
- Skill-gap analysis.

### API Layer

FastAPI will expose structured data and insights to frontend clients, dashboards, and reporting tools.

The current API foundation includes a minimal health endpoint so local setup and deployment checks have a stable target before business endpoints are introduced.

Future API responsibilities:

- Job search and filtering.
- Skill trend endpoints.
- Salary analytics endpoints.
- Location trend endpoints.
- Company hiring activity endpoints.
- Recommendation endpoints.

### Dashboard and Reporting Layer

Phase 1 includes only a static landing page.

Future reporting may include:

- Tableau dashboards.
- Web-based analytics views.
- Exportable market intelligence reports.
- Role-specific insight pages.

## Folder Responsibilities

### `api/`

Holds future FastAPI code, route definitions, schemas, dependencies, and service logic. It remains empty in Phase 1 because backend implementation is intentionally deferred.

### `data/`

Stores local datasets during development.

- `raw/` contains unchanged source data.
- `interim/` contains temporary partially processed data.
- `processed/` contains cleaned datasets ready for loading or analysis.
- `external/` contains third-party reference datasets such as skill taxonomies.

### `data_collection/`

Contains future ingestion logic.

- `connectors/` is for API-based or source-specific integration clients.
- `scrapers/` is for scraping modules where permitted.

### `data_processing/`

Contains cleaning, normalization, validation, and enrichment logic.

- `cleaning/` handles text cleanup, missing values, duplicate removal, and normalization.
- `validation/` checks data quality rules.
- `enrichment/` adds derived fields such as normalized location or extracted salary bands.

### `database/`

Contains database design assets.

- `migrations/` will store schema migration files.
- `models/` will store future ORM or SQL model definitions.
- `seeds/` will store reference data such as standard skills or locations.

### `dashboard/`

Contains user-facing visual surfaces. Phase 1 includes only the landing page. Future dashboard code or Tableau exports can live here.

### `docs/`

Stores supporting documentation, diagrams, decisions, and research notes beyond the root project documents.

### `machine_learning/`

Contains future ML experiments, feature engineering, and trained model artifacts.

- `experiments/` stores notebooks or experiment notes.
- `features/` stores feature generation logic.
- `models/` stores model definitions or tracked outputs.

### `nlp/`

Contains future NLP extraction logic and taxonomies.

- `extraction/` stores logic for extracting skills, technologies, certifications, and experience requirements.
- `taxonomies/` stores controlled vocabularies and mappings.

### `reports/`

Stores generated analytical reports, exported insights, and future business intelligence outputs.

### `scripts/`

Stores operational helper scripts, such as local setup, data loading, or scheduled job commands.

### `tests/`

Stores automated tests for data processing, API behavior, database logic, and future ML utilities.

## Architectural Priorities

TalentLens should prioritize:

- Data quality before model complexity.
- Clear module boundaries.
- Reproducible processing.
- Traceable source metadata.
- Responsible data collection.
- Testable business logic.
- Extensible analytics interfaces.

The engineering principles for high cohesion and low coupling are documented in `docs/ENGINEERING_PRINCIPLES.md`.

## Phase 2 Foundation Boundary

Phase 2 begins with project setup, schema planning, API readiness, and data collection design. Real source connectors should be added one at a time after the source access method is reviewed.

Current foundation files:

- `api/main.py` defines the FastAPI application and health check.
- `api/config.py` centralizes environment-based settings.
- `database/migrations/001_initial_schema.sql` drafts the initial PostgreSQL schema.
- `database/seeds/job_sources.sql` records planned job sources.
- `docs/LOCAL_SETUP.md` documents local development setup.
- `docs/DATA_COLLECTION_PLAN.md` documents responsible collection guidelines.

## Phase 1 Architecture Boundary

Phase 1 should not include backend routes, real scraping code, ML models, or dashboards. It establishes the structure and design needed to build those features responsibly in later phases.
