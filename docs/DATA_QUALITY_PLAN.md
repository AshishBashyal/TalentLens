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

## Cohesion And Coupling Rules

- Connectors read source data only.
- Validation modules report record quality only.
- Enrichment modules add structured context only.
- Transformers shape records for database loading only.
- Loaders write records only.
- Scripts orchestrate these pieces without owning business logic.

