# Data Quality Plan

TalentLens should treat data quality as part of the ingestion pipeline, not as a cleanup afterthought.

## Goals

- Identify invalid records before database loading.
- Track missing required fields.
- Detect duplicate source job IDs.
- Measure salary and skill coverage.
- Keep audit logic separate from connectors and loaders.

## Current Required Fields

Raw job postings currently require:

- `source`
- `title`
- `company`
- `location`
- `employment_type`
- `description`

Records missing these fields should be skipped during normalized loading until a source-specific fallback is approved.

## Current Audit Tool

Run:

```powershell
python scripts/audit_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 1000
```

Write a local markdown report:

```powershell
python scripts/audit_kaggle_jobs.py "C:\Users\ashis\Downloads\Datasets" --limit 1000 --output reports/kaggle_quality_audit.md
```

Generated reports in `reports/` are ignored by Git.

## Quality Metrics

The current audit reports:

- Total records.
- Valid records.
- Invalid records.
- Valid rate.
- Missing required fields.
- Duplicate source job IDs.
- Empty salary records.
- Empty skills records after structured enrichment.
- Remote records.

## Skill Quality Rule

Kaggle structured skill mappings from `job_skills.csv` and `skills.csv` are preferred over `skills_desc` text because `skills_desc` can contain long prose fragments.

When structured mappings are unavailable, fallback skill text is conservatively filtered:

- Empty labels are removed.
- Very long labels are removed.
- Labels with more than six words are removed.
- Sentence-like fragments are removed.

The PostgreSQL loader also removes orphan skills after refreshing job-skill links, so old messy skill records do not remain in analytics queries after a reload.

## Cohesion And Coupling Rules

- Connectors read source data only.
- Validation modules report record quality only.
- Enrichment modules add structured context only.
- Transformers shape records for database loading only.
- Loaders write records only.
- Scripts orchestrate these pieces without owning business logic.
