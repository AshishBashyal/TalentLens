from typing import Any


DatabasePreview = dict[str, list[dict[str, Any]]]


class JobIngestionLoader:
    """Insert database-shaped job records into PostgreSQL."""

    def __init__(self, connection: object, source_name: str) -> None:
        self.connection = connection
        self.source_name = source_name

    def load(self, preview: DatabasePreview) -> dict[str, int]:
        """Load preview records and return inserted/upserted record counts."""

        with self.connection.cursor() as cursor:
            source_id = self._upsert_source(cursor)
            company_ids = self._upsert_companies(cursor, preview["companies"])
            location_ids = self._upsert_locations(cursor, preview["locations"])
            skill_ids = self._upsert_skills(cursor, preview["skills"])
            job_ids = self._upsert_jobs(cursor, source_id, preview["jobs"], company_ids, location_ids)
            salary_count = self._insert_salaries(cursor, preview["salaries"], job_ids)
            job_skill_count = self._upsert_job_skills(cursor, preview["job_skills"], job_ids, skill_ids)

        self.connection.commit()

        return {
            "companies": len(company_ids),
            "locations": len(location_ids),
            "jobs": len(job_ids),
            "salaries": salary_count,
            "skills": len(skill_ids),
            "job_skills": job_skill_count,
        }

    def _upsert_source(self, cursor: object) -> int:
        cursor.execute(
            """
            INSERT INTO job_sources (name, collection_method)
            VALUES (%s, %s)
            ON CONFLICT (name)
            DO UPDATE SET updated_at = NOW()
            RETURNING id
            """,
            (self.source_name, "local_dataset"),
        )
        return cursor.fetchone()[0]

    def _upsert_companies(self, cursor: object, records: list[dict[str, Any]]) -> dict[str, int]:
        company_ids = {}
        for record in records:
            name = record["name"]
            cursor.execute(
                """
                INSERT INTO companies (name)
                VALUES (%s)
                ON CONFLICT (name)
                DO UPDATE SET updated_at = NOW()
                RETURNING id
                """,
                (name,),
            )
            company_ids[name] = cursor.fetchone()[0]

        return company_ids

    def _upsert_locations(self, cursor: object, records: list[dict[str, Any]]) -> dict[str, int]:
        location_ids = {}
        for record in records:
            raw_location = record["raw_location"]
            cursor.execute(
                """
                SELECT id FROM locations
                WHERE raw_location = %s
                LIMIT 1
                """,
                (raw_location,),
            )
            existing = cursor.fetchone()
            if existing:
                location_ids[raw_location] = existing[0]
                continue

            cursor.execute(
                """
                INSERT INTO locations (raw_location)
                VALUES (%s)
                RETURNING id
                """,
                (raw_location,),
            )
            location_ids[raw_location] = cursor.fetchone()[0]

        return location_ids

    def _upsert_skills(self, cursor: object, records: list[dict[str, Any]]) -> dict[str, int]:
        skill_ids = {}
        for record in records:
            name = record["name"]
            cursor.execute(
                """
                INSERT INTO skills (name)
                VALUES (%s)
                ON CONFLICT (name)
                DO UPDATE SET updated_at = NOW()
                RETURNING id
                """,
                (name,),
            )
            skill_ids[name] = cursor.fetchone()[0]

        return skill_ids

    def _upsert_jobs(
        self,
        cursor: object,
        source_id: int,
        records: list[dict[str, Any]],
        company_ids: dict[str, int],
        location_ids: dict[str, int],
    ) -> dict[str, int]:
        job_ids = {}
        for record in records:
            source_job_id = record["source_job_id"]
            cursor.execute(
                """
                INSERT INTO jobs (
                    source_id,
                    company_id,
                    location_id,
                    source_job_id,
                    job_url,
                    title,
                    normalized_title,
                    description,
                    employment_type,
                    posted_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_id, source_job_id)
                DO UPDATE SET
                    company_id = EXCLUDED.company_id,
                    location_id = EXCLUDED.location_id,
                    job_url = EXCLUDED.job_url,
                    title = EXCLUDED.title,
                    normalized_title = EXCLUDED.normalized_title,
                    description = EXCLUDED.description,
                    employment_type = EXCLUDED.employment_type,
                    posted_date = EXCLUDED.posted_date,
                    updated_at = NOW()
                RETURNING id
                """,
                (
                    source_id,
                    company_ids[record["company_name"]],
                    location_ids[record["raw_location"]],
                    source_job_id,
                    record["job_url"],
                    record["title"],
                    record["normalized_title"],
                    record["description"],
                    record["employment_type"],
                    record["posted_date"] or None,
                ),
            )
            job_ids[source_job_id] = cursor.fetchone()[0]

        return job_ids

    def _insert_salaries(
        self,
        cursor: object,
        records: list[dict[str, Any]],
        job_ids: dict[str, int],
    ) -> int:
        inserted = 0
        for record in records:
            job_id = job_ids.get(record["source_job_id"])
            if not job_id:
                continue

            cursor.execute("DELETE FROM salaries WHERE job_id = %s", (job_id,))
            cursor.execute(
                """
                INSERT INTO salaries (job_id, raw_salary_text)
                VALUES (%s, %s)
                """,
                (job_id, record["raw_salary_text"]),
            )
            inserted += 1

        return inserted

    def _upsert_job_skills(
        self,
        cursor: object,
        records: list[dict[str, Any]],
        job_ids: dict[str, int],
        skill_ids: dict[str, int],
    ) -> int:
        upserted = 0
        for record in records:
            job_id = job_ids.get(record["source_job_id"])
            skill_id = skill_ids.get(record["skill_name"])
            if not job_id or not skill_id:
                continue

            cursor.execute(
                """
                INSERT INTO job_skills (job_id, skill_id, extraction_method)
                VALUES (%s, %s, %s)
                ON CONFLICT (job_id, skill_id)
                DO UPDATE SET extraction_method = EXCLUDED.extraction_method
                """,
                (job_id, skill_id, record["extraction_method"]),
            )
            upserted += 1

        return upserted

