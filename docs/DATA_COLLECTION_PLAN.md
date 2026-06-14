# Data Collection Plan

TalentLens will collect job posting data incrementally and responsibly.

## Phase 2 Objective

The goal of Phase 2 is to establish a reliable data collection and storage foundation, not to scrape every source immediately.

Initial work should focus on:

- Choosing one source for the first ingestion workflow.
- Capturing raw source data before transformation.
- Normalizing key job fields.
- Loading validated records into PostgreSQL.
- Documenting source-specific constraints and assumptions.

## Responsible Collection Guidelines

Before building a connector for any source:

- Review the source terms and access rules.
- Prefer official APIs, exports, or permitted public access.
- Respect robots policies where applicable.
- Use rate limits and retries.
- Store source URLs and collection timestamps.
- Avoid collecting private or account-protected data.

## Planned Sources

Initial candidate sources:

- LinkedIn.
- Indeed.
- Wellfound.
- Internshala.
- Naukri.

Each source should receive its own connector or scraper module only after the access method is approved.

## Raw Data Contract

Raw collected records should preserve source-specific fields where possible.

Minimum raw metadata:

- Source name.
- Source job ID when available.
- Original job URL.
- Collection timestamp.
- Raw title.
- Raw company.
- Raw location.
- Raw salary.
- Raw description.
- Raw posting date.

## Normalized Job Contract

Cleaned records should map toward the database schema:

- Job title.
- Normalized title.
- Company.
- Location.
- Salary.
- Experience requirements.
- Description.
- Skills when available.
- Posting date.
- Source metadata.

## Next Implementation Step

After this foundation is approved, the next step is to select the first source and create a minimal connector interface with a small sample ingestion workflow.

