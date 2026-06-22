from pathlib import Path

from data_collection.connectors.csv_sample import CsvSampleConnector
from data_processing.cleaning.jobs import (
    normalize_job_posting,
    normalize_posted_date,
    normalize_title,
    split_skills,
)
from data_processing.validation.jobs import validate_raw_job


def test_csv_sample_connector_loads_sample_jobs() -> None:
    connector = CsvSampleConnector(Path("data/samples/sample_jobs.csv"))

    jobs = connector.fetch()

    assert len(jobs) == 10
    assert jobs[0].source == "sample_csv"
    assert jobs[0].title == "Data Analyst Intern"


def test_raw_sample_jobs_are_valid() -> None:
    connector = CsvSampleConnector(Path("data/samples/sample_jobs.csv"))

    for job in connector.fetch():
        assert validate_raw_job(job) == []


def test_normalized_title_is_search_friendly() -> None:
    assert normalize_title("Junior Python Developer") == "junior python developer"
    assert normalize_title("Data-Analyst Intern!") == "data analyst intern"


def test_skills_are_split_and_normalized() -> None:
    assert split_skills("Python, SQL,  Tableau ") == ("python", "sql", "tableau")


def test_epoch_milliseconds_are_normalized_to_iso_date() -> None:
    assert normalize_posted_date("1713397508000.0") == "2024-04-17"


def test_raw_job_can_be_normalized() -> None:
    connector = CsvSampleConnector(Path("data/samples/sample_jobs.csv"))

    normalized = normalize_job_posting(connector.fetch()[0])

    assert normalized.normalized_title == "data analyst intern"
    assert normalized.company == "InsightWorks"
    assert normalized.employment_type == "internship"
    assert normalized.skills == ("sql", "excel", "python", "tableau")
