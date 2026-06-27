# TalentLens Phase Plan

TalentLens is being built as a staged platform. Each phase has subphases with distinct tasks so the project grows without mixing concerns.

## Phase 1: Foundation

Status: Complete

Subphases:

1. Project vision and README.
2. Architecture documentation.
3. Database design documentation.
4. Roadmap documentation.
5. Scalable folder structure.
6. Static landing page.

## Phase 2: Data Collection And Storage

Status: In progress

Subphases:

1. Dataset license and source review.
2. Dataset profiling and assessment.
3. Raw and normalized data contracts.
4. Source connector interface.
5. Local synthetic sample connector.
6. Kaggle dataset connector.
7. Data validation rules.
8. Data quality audit.
9. Data enrichment from structured skill lookups.
10. Database schema migrations.
11. Database-shaped transformation preview.
12. Small-batch PostgreSQL loader.
13. Database load verification.
14. Reproducible local PostgreSQL setup.
15. Ingestion documentation.

Phase 2 completion criteria:

- PostgreSQL runs locally.
- Migrations apply cleanly.
- A small Kaggle batch loads with `--apply`.
- Verification reports expected counts.
- Data quality limitations are documented.

## Phase 3: Analytics Layer

Status: Planned

Subphases:

1. Skill demand SQL views.
2. Salary coverage and salary trend queries.
3. Location hiring demand queries.
4. Company hiring activity queries.
5. Industry trend queries.
6. Remote versus onsite analysis.
7. Exportable analytics datasets.
8. Analytics report scripts.
9. Analytics documentation.

## Phase 4: NLP Layer

Status: Planned

Subphases:

1. Skill taxonomy design.
2. Description cleaning pipeline.
3. Rule-based skill extraction.
4. spaCy extraction pipeline.
5. Technology extraction.
6. Certification extraction.
7. Experience requirement parsing.
8. NLP evaluation dataset.
9. Extraction quality reporting.

## Phase 5: Machine Learning Layer

Status: Planned

Subphases:

1. Feature engineering from normalized jobs.
2. Job clustering.
3. Salary prediction prototype.
4. Trend forecasting prototype.
5. Skill-gap analysis.
6. Career recommendation prototype.
7. Model evaluation.
8. Experiment documentation.
9. ML limitations and responsible use notes.

## Phase 6: Advanced AI And Business Intelligence

Status: Planned

Subphases:

1. Market intelligence report generation.
2. Career recommendation interface.
3. Recruiter insight workflows.
4. Business workforce planning workflows.
5. API endpoints for analytics.
6. Dashboard integration.
7. Scheduled refresh workflow.
8. Deployment preparation.
9. Final documentation and portfolio polish.

