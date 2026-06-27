from database.verification import QUALITY_QUERIES, VERIFICATION_QUERIES


def test_verification_queries_cover_core_tables() -> None:
    expected_tables = {
        "job_sources",
        "companies",
        "locations",
        "jobs",
        "salaries",
        "skills",
        "job_skills",
        "industries",
        "job_industries",
        "job_benefits",
    }

    assert set(VERIFICATION_QUERIES) == expected_tables


def test_quality_queries_cover_core_loader_gaps() -> None:
    assert set(QUALITY_QUERIES) == {
        "jobs_missing_company",
        "jobs_missing_location",
        "jobs_without_skills",
        "jobs_without_salary",
    }

