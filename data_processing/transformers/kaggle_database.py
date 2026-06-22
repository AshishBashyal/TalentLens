from data_collection.contracts import NormalizedJobPosting


def build_database_record_preview(jobs: list[NormalizedJobPosting]) -> dict[str, list[dict[str, object]]]:
    """Build database-shaped records for review before real inserts."""

    companies = {}
    locations = {}
    skills = {}
    job_records = []
    salary_records = []
    job_skill_records = []

    for job in jobs:
        companies.setdefault(job.company, {"name": job.company})
        locations.setdefault(job.location, {"raw_location": job.location})

        job_records.append(
            {
                "source_job_id": job.source_job_id,
                "title": job.title,
                "normalized_title": job.normalized_title,
                "company_name": job.company,
                "raw_location": job.location,
                "employment_type": job.employment_type,
                "description": job.description,
                "job_url": job.job_url,
                "posted_date": job.posted_date,
            }
        )

        if job.salary:
            salary_records.append(
                {
                    "source_job_id": job.source_job_id,
                    "raw_salary_text": job.salary,
                }
            )

        for skill in job.skills:
            skills.setdefault(skill, {"name": skill})
            job_skill_records.append(
                {
                    "source_job_id": job.source_job_id,
                    "skill_name": skill,
                    "extraction_method": "kaggle_structured",
                }
            )

    return {
        "companies": list(companies.values()),
        "locations": list(locations.values()),
        "jobs": job_records,
        "salaries": salary_records,
        "skills": list(skills.values()),
        "job_skills": job_skill_records,
    }

