# Dataset Specification

TalentLens needs job posting datasets that are rich enough for data engineering, analytics, NLP, and future machine learning work.

## Dataset Types

### Raw Job Posting Dataset

The raw dataset preserves source-shaped records with minimal transformation. It supports traceability and reprocessing.

Required fields:

- `source`: Platform or source name.
- `source_job_id`: Source-specific job identifier when available.
- `job_url`: Original posting URL.
- `title`: Raw job title.
- `company`: Raw company name.
- `location`: Raw location text.
- `salary`: Raw salary or stipend text.
- `experience`: Raw experience requirement.
- `employment_type`: Internship, full-time, contract, part-time, or similar.
- `skills`: Source-provided or manually tagged comma-separated skills when available.
- `description`: Full job description.
- `posted_date`: Original posting date.

### Normalized Job Dataset

The normalized dataset prepares records for PostgreSQL and analytics.

Expected normalized fields:

- Source metadata.
- Cleaned title.
- Normalized title.
- Normalized company.
- Normalized location.
- Parsed salary fields.
- Parsed experience fields.
- Employment type.
- Cleaned description.
- Split and normalized skills.
- Posting and collection dates.

### Future Analytical Dataset

After ingestion and cleaning are stable, TalentLens will derive analytical datasets for:

- Skill demand trends.
- Salary trends.
- Location demand.
- Company hiring activity.
- Role and technology trends.

## Current Synthetic Sample

The current sample file is:

```text
data/samples/sample_jobs.csv
```

It is intentionally synthetic. Its purpose is to test ingestion, validation, normalization, and documentation before connecting any real source.

The sample includes multiple roles, locations, employment types, salary formats, experience ranges, and skill groups.

## External Kaggle Dataset Candidate

The local Kaggle files inspected on June 22, 2026 include:

- `postings.csv`
- `companies.csv`
- `company_specialities.csv`
- `employee_counts.csv`
- `skills.csv`
- `salaries.csv`
- `job_skills.csv`
- `job_industries.csv`
- `industries.csv`
- `benefits.csv`

The assessment is documented in `docs/KAGGLE_DATASET_ASSESSMENT.md`.

This dataset is strong for Phase 2 because it includes a core job postings table plus normalized supporting tables for companies, skills, industries, salaries, and benefits.

The raw CSVs should stay outside Git unless the license clearly allows redistribution.

## Quality Requirements

A useful job posting dataset should:

- Have non-empty title, company, location, employment type, and description.
- Preserve original source URLs and source IDs where possible.
- Include posting dates for time-series trend analysis.
- Keep raw salary and experience text even before parsing.
- Include enough description text for NLP extraction.
- Avoid private, account-protected, or unauthorized data.
