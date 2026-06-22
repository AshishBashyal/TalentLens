from data_collection.contracts import RawJobPosting, ValidationIssue


REQUIRED_RAW_FIELDS = (
    "source",
    "title",
    "company",
    "location",
    "employment_type",
    "description",
)


def validate_raw_job(raw_job: RawJobPosting) -> list[ValidationIssue]:
    """Validate the minimum fields required before normalization."""

    issues: list[ValidationIssue] = []

    for field_name in REQUIRED_RAW_FIELDS:
        value = getattr(raw_job, field_name)
        if not value or not value.strip():
            issues.append(
                ValidationIssue(
                    field=field_name,
                    message=f"{field_name} is required",
                )
            )

    return issues
