# TalentLens Roadmap

## Roadmap Philosophy

TalentLens will be built incrementally. The project should avoid jumping straight into advanced machine learning before the data foundation is reliable.

Each phase should produce usable, reviewable progress while keeping the architecture ready for future expansion.

## Phase 1: Foundation

Status: Complete

Goals:

- Create professional project documentation.
- Define the project vision.
- Design scalable folder structure.
- Document system architecture.
- Draft initial database design.
- Build a polished static landing page.

Deliverables:

- `README.md`
- `PROJECT_VISION.md`
- `ARCHITECTURE.md`
- `DATABASE_DESIGN.md`
- `ROADMAP.md`
- Static landing page in `dashboard/landing-page/`
- Empty scalable folders for future implementation

Out of scope:

- Backend implementation.
- Real data collection.
- Dashboards.
- NLP extraction.
- Machine learning models.

## Phase 2: Data Collection and Storage

Status: Started

Goals:

- Implement responsible data collection from selected sources.
- Define source-specific ingestion patterns.
- Store raw collected data.
- Create initial PostgreSQL schema and migrations.
- Load normalized job postings into the database.

Candidate deliverables:

- Python and FastAPI project foundation.
- Local setup documentation.
- Initial PostgreSQL migration draft.
- Seed data for planned job sources.
- Responsible data collection plan.
- Source connector interfaces.
- Initial collection scripts.
- Raw data storage conventions.
- Database migrations.
- Basic duplicate detection.
- Data ingestion documentation.

## Phase 3: Data Cleaning and Analytics

Goals:

- Clean and normalize job posting data.
- Parse salary, location, experience, and employment type fields.
- Generate initial analytics datasets.
- Create repeatable reporting queries.

Candidate deliverables:

- Cleaning pipelines.
- Validation rules.
- Analytical SQL views.
- Skill frequency analysis using simple rules.
- Salary trend summaries.
- Location demand summaries.

## Phase 4: NLP

Goals:

- Extract structured information from job descriptions.
- Build skill and technology taxonomies.
- Identify certifications and experience requirements.
- Improve extraction confidence and explainability.

Candidate deliverables:

- spaCy-based extraction pipeline.
- Rule-based skill matcher.
- Skill taxonomy files.
- Evaluation dataset for extraction quality.
- NLP documentation.

## Phase 5: Machine Learning

Goals:

- Add predictive and clustering features once data volume is sufficient.
- Build models that produce explainable and useful outputs.

Candidate deliverables:

- Job clustering.
- Salary prediction prototype.
- Trend forecasting experiments.
- Skill-gap analysis prototype.
- Model evaluation reports.

## Phase 6: Advanced AI and Business Intelligence

Goals:

- Turn TalentLens into a more complete intelligence platform.
- Support recommendations, reports, and strategic planning workflows.

Candidate deliverables:

- Career recommendation engine.
- Automated market intelligence reports.
- Personalized learning path suggestions.
- Recruiter and business dashboards.
- API-driven insight delivery.
- Scheduled data refreshes.

## Milestone Review Gates

Each phase should end with a review before moving forward.

Review questions:

- Is the current phase complete?
- Are outputs documented?
- Are assumptions clear?
- Are there tests or validation checks where appropriate?
- Is the next phase still aligned with the product vision?

## Near-Term Next Step

After Phase 1 approval, the next logical step is to select the first job source and design a minimal data collection workflow that respects source policies and stores raw data safely.
