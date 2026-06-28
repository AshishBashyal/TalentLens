from typing import Any


VERIFICATION_QUERIES = {
    "job_sources": "SELECT COUNT(*) FROM job_sources;",
    "companies": "SELECT COUNT(*) FROM companies;",
    "locations": "SELECT COUNT(*) FROM locations;",
    "jobs": "SELECT COUNT(*) FROM jobs;",
    "salaries": "SELECT COUNT(*) FROM salaries;",
    "skills": "SELECT COUNT(*) FROM skills;",
    "job_skills": "SELECT COUNT(*) FROM job_skills;",
    "industries": "SELECT COUNT(*) FROM industries;",
    "job_industries": "SELECT COUNT(*) FROM job_industries;",
    "job_benefits": "SELECT COUNT(*) FROM job_benefits;",
}


QUALITY_QUERIES = {
    "jobs_missing_company": """
        SELECT COUNT(*)
        FROM jobs
        WHERE company_id IS NULL;
    """,
    "jobs_missing_location": """
        SELECT COUNT(*)
        FROM jobs
        WHERE location_id IS NULL;
    """,
    "jobs_without_skills": """
        SELECT COUNT(*)
        FROM jobs j
        LEFT JOIN job_skills js ON js.job_id = j.id
        WHERE js.job_id IS NULL;
    """,
    "jobs_without_salary": """
        SELECT COUNT(*)
        FROM jobs j
        LEFT JOIN salaries s ON s.job_id = j.id
        WHERE s.job_id IS NULL;
    """,
    "orphan_skills": """
        SELECT COUNT(*)
        FROM skills s
        LEFT JOIN job_skills js ON js.skill_id = s.id
        WHERE js.skill_id IS NULL;
    """,
}


def fetch_single_value(cursor: object, query: str) -> Any:
    cursor.execute(query)
    return cursor.fetchone()[0]


def verify_database_counts(connection: object) -> dict[str, int]:
    """Return table counts for the current TalentLens database."""

    with connection.cursor() as cursor:
        return {
            name: int(fetch_single_value(cursor, query))
            for name, query in VERIFICATION_QUERIES.items()
        }


def verify_database_quality(connection: object) -> dict[str, int]:
    """Return basic quality counts for loaded TalentLens job data."""

    with connection.cursor() as cursor:
        return {
            name: int(fetch_single_value(cursor, query))
            for name, query in QUALITY_QUERIES.items()
        }
