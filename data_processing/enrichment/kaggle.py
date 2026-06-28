import csv
from collections import defaultdict
from dataclasses import replace
from pathlib import Path

from data_collection.contracts import RawJobPosting


def load_skill_lookup(dataset_dir: str | Path) -> dict[str, str]:
    skills_file = Path(dataset_dir) / "skills.csv"
    if not skills_file.exists():
        return {}

    with skills_file.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return {
            row["skill_abr"]: row["skill_name"]
            for row in reader
            if row.get("skill_abr") and row.get("skill_name")
        }


def load_job_skill_map(dataset_dir: str | Path, skill_lookup: dict[str, str]) -> dict[str, tuple[str, ...]]:
    job_skills_file = Path(dataset_dir) / "job_skills.csv"
    if not job_skills_file.exists():
        return {}

    grouped_skills: dict[str, list[str]] = defaultdict(list)
    with job_skills_file.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            job_id = row.get("job_id", "")
            skill_abr = row.get("skill_abr", "")
            skill_name = skill_lookup.get(skill_abr)
            if job_id and skill_name:
                grouped_skills[job_id].append(skill_name)

    return {job_id: tuple(skills) for job_id, skills in grouped_skills.items()}


def enrich_jobs_with_kaggle_skills(
    raw_jobs: list[RawJobPosting],
    dataset_dir: str | Path,
) -> list[RawJobPosting]:
    skill_lookup = load_skill_lookup(dataset_dir)
    job_skill_map = load_job_skill_map(dataset_dir, skill_lookup)
    enriched_jobs = []

    for raw_job in raw_jobs:
        mapped_skills = job_skill_map.get(raw_job.source_job_id, ())
        if mapped_skills:
            enriched_jobs.append(replace(raw_job, skills=", ".join(mapped_skills)))
        else:
            enriched_jobs.append(raw_job)

    return enriched_jobs
