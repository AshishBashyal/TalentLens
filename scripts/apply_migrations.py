import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.config import get_settings
from database.connection import open_connection
from database.migration_runner import apply_migrations


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply TalentLens database migrations.")
    parser.add_argument(
        "--migrations-dir",
        default=PROJECT_ROOT / "database" / "migrations",
        type=Path,
        help="Directory containing SQL migration files.",
    )
    args = parser.parse_args()

    settings = get_settings()
    with open_connection(settings.database_url) as connection:
        applied_files = apply_migrations(connection, args.migrations_dir)

    print(f"Applied {len(applied_files)} migrations")
    for file_name in applied_files:
        print(f"- {file_name}")


if __name__ == "__main__":
    main()

