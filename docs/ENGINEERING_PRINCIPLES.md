# Engineering Principles

TalentLens should maintain high cohesion and low coupling as it grows.

## High Cohesion

Each module should have one clear responsibility.

- `data_collection` reads source data.
- `data_processing.validation` checks data quality.
- `data_processing.cleaning` normalizes fields.
- `data_processing.enrichment` adds structured context from related source files.
- `data_processing.transformers` shapes records for downstream systems.
- `database` owns migrations, connections, loaders, and verification queries.
- `api` exposes application interfaces.
- `scripts` orchestrate workflows but should not own business logic.

## Low Coupling

Modules should communicate through stable contracts and function inputs, not through hidden global state or source-specific assumptions.

Current contracts:

- `RawJobPosting`
- `NormalizedJobPosting`
- `ValidationIssue`

Rules:

- Connectors should not write to the database.
- Loaders should not parse raw CSV files.
- API routes should not contain ingestion logic.
- Analytics should read from normalized database tables or views.
- NLP and ML should depend on processed data, not connector internals.
- Scripts should stay thin and call reusable modules.

## Dependency Direction

Preferred flow:

```text
data_collection -> data_processing -> database -> api -> dashboard
```

Avoid reverse dependencies. For example, data collection should not import API routes, and database loaders should not know about UI code.

## Review Checklist

Before adding a new module, ask:

- Does this module have one clear responsibility?
- Is business logic reusable outside a CLI script?
- Does this depend on a stable contract instead of source-specific fields?
- Can this be tested without external services?
- Does this change belong in docs as well as code?

