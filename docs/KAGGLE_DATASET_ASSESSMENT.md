# Kaggle Dataset Assessment

This document summarizes the local CSV files currently being evaluated for TalentLens ingestion.

Raw dataset path inspected:

```text
C:\Users\ashis\Downloads\Datasets
```

The raw CSV files should not be committed to the repository unless the dataset license clearly allows redistribution and the file size is appropriate for Git. The current `postings.csv` file is about 493 MB, so it should stay outside Git even if the license allows use.

## License Status

No Kaggle metadata or license file was found in the downloaded folder.

Before using this dataset publicly, check the Kaggle dataset page for the license. Prefer:

- `CC0` or Public Domain.
- `CC BY 4.0` with attribution.

Avoid committing or redistributing the raw data if the license is unknown, restrictive, or unclear.

## File Summary

| File | Rows | Purpose |
| --- | ---: | --- |
| `postings.csv` | 123,849 | Core job postings fact table |
| `companies.csv` | 24,473 | Company dimension table |
| `company_specialities.csv` | 169,387 | Company speciality tags |
| `employee_counts.csv` | 35,787 | Company employee and follower counts over time |
| `skills.csv` | 35 | Skill lookup table |
| `salaries.csv` | 40,785 | Structured salary records |
| `job_skills.csv` | 213,768 | Job-to-skill relationship table |
| `job_industries.csv` | 164,808 | Job-to-industry relationship table |
| `industries.csv` | 422 | Industry lookup table |
| `benefits.csv` | 67,943 | Job benefits table |

## Core Tables

### `postings.csv`

Columns:

```text
job_id, company_name, title, description, max_salary, pay_period, location,
company_id, views, med_salary, min_salary, formatted_work_type, applies,
original_listed_time, remote_allowed, job_posting_url, application_url,
application_type, expiry, closed_time, formatted_experience_level, skills_desc,
listed_time, posting_domain, sponsored, work_type, currency, compensation_type,
normalized_salary, zip_code, fips
```

This is the main table for TalentLens. It contains the job title, description, company reference, location, work type, salary fields, posting URL, posting time, and engagement fields.

Sparse fields under 50 percent populated include:

- `max_salary`
- `pay_period`
- `med_salary`
- `min_salary`
- `applies`
- `remote_allowed`
- `closed_time`
- `skills_desc`
- `currency`
- `compensation_type`
- `normalized_salary`

### `companies.csv`

Columns:

```text
company_id, name, description, company_size, state, country, city, zip_code, address, url
```

This should map into the TalentLens company dimension.

### `job_skills.csv` and `skills.csv`

`job_skills.csv` maps `job_id` to `skill_abr`.

`skills.csv` maps `skill_abr` to `skill_name`.

These files are useful immediately because they provide structured skill labels before we build NLP extraction.

### `job_industries.csv` and `industries.csv`

`job_industries.csv` maps `job_id` to `industry_id`.

`industries.csv` maps `industry_id` to `industry_name`.

These files support industry-level hiring analysis.

### `salaries.csv`

Columns:

```text
salary_id, job_id, max_salary, med_salary, min_salary, pay_period, currency, compensation_type
```

This can supplement or normalize salary fields from `postings.csv`.

### `benefits.csv`

Columns:

```text
job_id, inferred, type
```

This is useful for later compensation and benefits analytics.

## Recommended Ingestion Order

1. Load lookup tables: `skills.csv`, `industries.csv`.
2. Load company dimension: `companies.csv`.
3. Load core jobs: `postings.csv`.
4. Load relationship tables: `job_skills.csv`, `job_industries.csv`.
5. Load supplementary tables: `salaries.csv`, `benefits.csv`, `employee_counts.csv`, `company_specialities.csv`.

## Mapping to TalentLens

| Kaggle field | TalentLens target |
| --- | --- |
| `postings.job_id` | `jobs.source_job_id` |
| `postings.company_id` | `companies` join key |
| `postings.company_name` | `companies.name` fallback |
| `postings.title` | `jobs.title` |
| `postings.description` | `jobs.description` |
| `postings.location` | `locations.raw_location` |
| `postings.formatted_work_type` | `jobs.employment_type` |
| `postings.formatted_experience_level` | Future experience normalization |
| `postings.job_posting_url` | `jobs.job_url` |
| `postings.listed_time` | `jobs.posted_date` after timestamp parsing |
| `salaries.*` | `salaries` |
| `job_skills.skill_abr` + `skills.skill_name` | `skills` and `job_skills` |
| `job_industries.industry_id` + `industries.industry_name` | Future industry dimension |

## Next Engineering Step

Create a real database loading pipeline after reviewing the database-shaped preview output.

The connector now reads the local dataset directory and converts a limited sample of `postings.csv` into the existing `RawJobPosting` contract.

Preview command:

```powershell
python scripts/preview_kaggle_ingestion.py "C:\Users\ashis\Downloads\Datasets" --limit 10
```

Database mapping preview:

```powershell
python scripts/preview_kaggle_database_mapping.py "C:\Users\ashis\Downloads\Datasets" --limit 25
```

This preview builds database-shaped records for companies, locations, jobs, salaries, skills, and job-skill relationships without inserting into PostgreSQL.
