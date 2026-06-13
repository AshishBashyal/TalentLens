# TalentLens

TalentLens is an AI-powered Job Market Intelligence Platform designed to help students, job seekers, recruiters, and businesses understand labor market trends through data.

The platform will collect job postings from multiple public sources, process them into structured datasets, extract insights from unstructured descriptions, and present business-grade intelligence about skills, salaries, hiring demand, technology adoption, and regional job market movement.

TalentLens is intentionally being built in phases. Phase 1 focuses on the foundation: project structure, documentation, database design, architecture, and a simple polished landing page. Advanced analytics, NLP, and machine learning will be introduced only after the data pipeline and storage layers are mature.

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

## Phase 1 Scope

Phase 1 includes:

- Professional project documentation.
- Scalable repository structure.
- Initial database design.
- High-level system architecture.
- Roadmap for future phases.
- Static landing page using HTML, CSS, and JavaScript.

Phase 1 does not include backend implementation, production data scraping, dashboards, NLP, or machine learning models.

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
├── api/
├── data/
│   ├── external/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── data_collection/
│   ├── connectors/
│   └── scrapers/
├── data_processing/
│   ├── cleaning/
│   ├── enrichment/
│   └── validation/
├── database/
│   ├── migrations/
│   ├── models/
│   └── seeds/
├── dashboard/
│   └── landing-page/
├── docs/
├── machine_learning/
│   ├── experiments/
│   ├── features/
│   └── models/
├── nlp/
│   ├── extraction/
│   └── taxonomies/
├── reports/
├── scripts/
├── tests/
├── ARCHITECTURE.md
├── DATABASE_DESIGN.md
├── PROJECT_VISION.md
├── README.md
└── ROADMAP.md
```

Each folder is intentionally separated by responsibility so the platform can grow without mixing scraping logic, processing logic, database assets, API code, analytics, and ML experiments.

## Opening the Landing Page

Open the static landing page at:

```text
dashboard/landing-page/index.html
```

No backend server is required for Phase 1.

## Current Status

TalentLens is in Phase 1: foundation and planning.

Next phases should begin only after reviewing and approving the documentation, structure, and landing page.

