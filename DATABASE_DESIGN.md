# TalentLens Database Design

## Overview

TalentLens will use PostgreSQL as the primary structured data store. The database design should support job posting storage, source traceability, skill extraction, salary analysis, location trends, company activity, and future machine learning workflows.

The initial design began as conceptual Phase 1 planning. Phase 2 now includes the first SQL migration draft at `database/migrations/001_initial_schema.sql`.

## Design Principles

- Preserve source metadata for traceability.
- Normalize repeated entities such as companies, locations, skills, and sources.
- Keep raw job descriptions available for NLP.
- Support many-to-many relationships between jobs and skills.
- Store parsed salary information separately from raw salary text.
- Design for analytics without prematurely optimizing.

## Core Entities

### `job_sources`

Stores information about each data source.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `id` | UUID / BIGSERIAL | Primary key |
| `name` | TEXT | Source name, such as LinkedIn or Internshala |
| `base_url` | TEXT | Source website or API base URL |
| `collection_method` | TEXT | API, scraper, manual import, or partner feed |
| `is_active` | BOOLEAN | Whether the source is currently used |
| `created_at` | TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | Record update time |

### `companies`

Stores normalized company information.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `id` | UUID / BIGSERIAL | Primary key |
| `name` | TEXT | Normalized company name |
| `website` | TEXT | Company website when available |
| `industry` | TEXT | Optional industry category |
| `company_size` | TEXT | Optional size range |
| `created_at` | TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | Record update time |

### `locations`

Stores normalized location information.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `id` | UUID / BIGSERIAL | Primary key |
| `raw_location` | TEXT | Original location string |
| `city` | TEXT | City |
| `state` | TEXT | State or region |
| `country` | TEXT | Country |
| `is_remote` | BOOLEAN | Whether the role is remote |
| `created_at` | TIMESTAMP | Record creation time |

### `jobs`

Stores normalized job postings.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `id` | UUID / BIGSERIAL | Primary key |
| `source_id` | FK | Links to `job_sources` |
| `company_id` | FK | Links to `companies` |
| `location_id` | FK | Links to `locations` |
| `source_job_id` | TEXT | Job ID from source when available |
| `job_url` | TEXT | Original posting URL |
| `title` | TEXT | Job title |
| `normalized_title` | TEXT | Standardized title |
| `description` | TEXT | Full job description |
| `employment_type` | TEXT | Full-time, internship, contract, part-time |
| `experience_min_years` | NUMERIC | Minimum experience |
| `experience_max_years` | NUMERIC | Maximum experience |
| `posted_date` | DATE | Posting date |
| `collected_at` | TIMESTAMP | Collection timestamp |
| `created_at` | TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | Record update time |

### `salaries`

Stores parsed salary information.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `id` | UUID / BIGSERIAL | Primary key |
| `job_id` | FK | Links to `jobs` |
| `raw_salary_text` | TEXT | Original salary text |
| `currency` | TEXT | Currency code, such as INR or USD |
| `min_salary` | NUMERIC | Parsed minimum salary |
| `max_salary` | NUMERIC | Parsed maximum salary |
| `salary_period` | TEXT | Monthly, yearly, hourly, stipend |
| `is_estimated` | BOOLEAN | Whether value is inferred |
| `created_at` | TIMESTAMP | Record creation time |

### `skills`

Stores normalized skills and technologies.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `id` | UUID / BIGSERIAL | Primary key |
| `name` | TEXT | Skill name |
| `category` | TEXT | Programming, cloud, database, analytics, soft skill, etc. |
| `is_technology` | BOOLEAN | Whether the skill is a technology/tool |
| `created_at` | TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | Record update time |

### `job_skills`

Many-to-many relationship between jobs and skills.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `job_id` | FK | Links to `jobs` |
| `skill_id` | FK | Links to `skills` |
| `extraction_method` | TEXT | Manual, rule-based, NLP, model |
| `confidence_score` | NUMERIC | Optional extraction confidence |
| `created_at` | TIMESTAMP | Record creation time |

### `certifications`

Stores certifications extracted from postings.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `id` | UUID / BIGSERIAL | Primary key |
| `name` | TEXT | Certification name |
| `provider` | TEXT | Issuing provider when known |
| `created_at` | TIMESTAMP | Record creation time |

### `job_certifications`

Many-to-many relationship between jobs and certifications.

Suggested fields:

| Field | Type | Description |
| --- | --- | --- |
| `job_id` | FK | Links to `jobs` |
| `certification_id` | FK | Links to `certifications` |
| `confidence_score` | NUMERIC | Optional extraction confidence |
| `created_at` | TIMESTAMP | Record creation time |

## Analytical Query Examples

The database should eventually support questions such as:

- What are the top skills requested for data analyst roles?
- Which cities have the highest demand for Python?
- How are salary ranges changing for machine learning engineers?
- Which companies are hiring most actively in a given month?
- Which skills commonly appear together?
- Which technologies are emerging across entry-level roles?

## Indexing Strategy

Future implementation should consider indexes on:

- `jobs.posted_date`
- `jobs.normalized_title`
- `jobs.source_id`
- `jobs.company_id`
- `jobs.location_id`
- `skills.name`
- `job_skills.skill_id`
- `salaries.currency`
- `locations.city`
- `locations.country`

Full-text search indexes may be useful for job descriptions once search features are introduced.

## Data Quality Rules

Initial quality checks should include:

- Job title must not be empty.
- Source must be known.
- Duplicate postings should be detected by source job ID, URL, title, company, and location.
- Salary values must be logically valid when parsed.
- Experience maximum should not be less than experience minimum.
- Skill names should map to a normalized taxonomy.

## Migration Status

The first migration draft creates:

- Job sources.
- Companies.
- Locations.
- Jobs.
- Salaries.
- Skills.
- Job-to-skill relationships.
- Certifications.
- Job-to-certification relationships.
- Initial analytical indexes.

Seed data for planned sources lives in `database/seeds/job_sources.sql`.

These SQL files are ready for review before database automation is added.
