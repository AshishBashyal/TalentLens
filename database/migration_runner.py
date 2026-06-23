from pathlib import Path


def migration_files(migrations_dir: str | Path) -> list[Path]:
    """Return SQL migration files in deterministic order."""

    return sorted(Path(migrations_dir).glob("*.sql"))


def apply_migrations(connection: object, migrations_dir: str | Path) -> list[str]:
    """Apply SQL migration files to a PostgreSQL connection."""

    applied_files = []

    with connection.cursor() as cursor:
        for migration_file in migration_files(migrations_dir):
            cursor.execute(migration_file.read_text(encoding="utf-8"))
            applied_files.append(migration_file.name)

    connection.commit()
    return applied_files

