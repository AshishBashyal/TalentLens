ALTER TABLE companies
ADD COLUMN IF NOT EXISTS source_company_id TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS idx_companies_source_company_id
ON companies(source_company_id)
WHERE source_company_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS industries (
    id BIGSERIAL PRIMARY KEY,
    source_industry_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS job_industries (
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    industry_id BIGINT NOT NULL REFERENCES industries(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (job_id, industry_id)
);

CREATE TABLE IF NOT EXISTS job_benefits (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    benefit_type TEXT NOT NULL,
    is_inferred BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS company_specialities (
    company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    speciality TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (company_id, speciality)
);

CREATE TABLE IF NOT EXISTS employee_counts (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    employee_count INTEGER,
    follower_count INTEGER,
    time_recorded TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_industries_name ON industries(name);
CREATE INDEX IF NOT EXISTS idx_job_industries_industry_id ON job_industries(industry_id);
CREATE INDEX IF NOT EXISTS idx_job_benefits_job_id ON job_benefits(job_id);
CREATE INDEX IF NOT EXISTS idx_company_specialities_speciality ON company_specialities(speciality);
CREATE INDEX IF NOT EXISTS idx_employee_counts_company_id ON employee_counts(company_id);

